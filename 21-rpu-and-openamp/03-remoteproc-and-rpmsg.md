# remoteproc and RPMsg

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Management and messaging are separate layers

Linux **remoteproc** manages a remote processor's firmware and lifecycle. **Remote Processor Messaging (RPMsg)** provides message channels and endpoints. A remote processor can run a local application without RPMsg. A running remoteproc state therefore does not prove that a messaging channel exists.

The 2024.1 R5 driver makes this distinction explicit. `zynqmp_r5_parse_fw()` calls `rproc_elf_load_rsc_table()`. When it receives `-EINVAL`, this driver logs that no resource table was found and continues, supporting simple non-IPC firmware. Do not generalize that behavior to every platform driver or interpret the message as proof that an intended RPMsg setup is healthy.

## The resource table describes shared infrastructure

A resource table is firmware metadata that Linux reads while preparing the remote application. It has a header, entry offsets and typed resource entries. A virtio device entry can describe the RPMsg transport and its vrings. A vring is a shared queue structure containing buffer descriptors and producer/consumer information.

The table is not a C pointer exchange between processes. Its fields form an interface understood by both sides. Addresses refer to the documented remote or shared address space, not an arbitrary Linux userspace pointer. The loader must be able to map the declared locations safely.

The relevant layouts live in `include/linux/remoteproc.h`; parsing and resource handling live in `remoteproc_core.c` and `remoteproc_elf_loader.c`. Their checks are useful review targets when a firmware image loads but communication resources do not appear. [Pinned resource definitions](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/include/linux/remoteproc.h).

## Follow one message through the transport

For an original request/reply example, Linux sends a small request to an R5 service. The transport obtains an available transmit buffer, writes the RPMsg header and payload, places a descriptor on the appropriate virtqueue and notifies the remote side. The R5 consumes the entry, handles the request and returns buffers through the agreed queue protocol.

The notification is a doorbell. The payload lives in shared memory. One interrupt can lead the receiver to process several available entries, so interrupt count and application-message count need not be equal.

On the Linux side, `rpmsg_send_offchannel_raw()` handles the transport send path in `virtio_rpmsg_bus.c`. Receive handling validates an incoming message and finds its destination endpoint before invoking the callback. The callback's data has a transport-managed lifetime. Copy needed data or use a supported ownership mechanism before returning; do not save a borrowed pointer indefinitely.

## Message size comes from the selected transport

The inspected 2024.1 driver uses a default 512-byte transport buffer when `CONFIG_RPMSG_VIRTIO_BUF_SIZE` does not override it. Its RPMsg header takes 16 bytes, leaving 496 payload bytes in that configuration. This is a driver/configuration result, not a universal RPMsg limit.

Use the transport's supported maximum transmission unit where the API exposes it, and keep both sides compatible. Increasing a Linux setting alone does not prove that the remote implementation allocated matching buffers. The number of buffers also depends on vring capacity and the driver's limits.

A 4096-byte application record cannot fit into a 496-byte payload. It needs at least nine payload messages before adding an application fragmentation header, or a separate shared-data region with bounded descriptors. Define record IDs, offsets, total length, duplicate handling and timeout behavior if you fragment. Otherwise a dropped or restarted session can join pieces from different records.

## Channel discovery and endpoint addresses

A channel name identifies a service. Endpoint source and destination addresses identify message destinations within the transport. A name-service announcement can lead Linux to create a channel and match a driver. Channel creation, driver binding and application readiness are distinct events.

A missing character device does not always mean the R5 failed to start. The channel may not have been announced, its name may not match a driver, or the selected RPMsg userspace interface may require another endpoint-creation step. Inspect the actual RPMsg driver and userspace ABI selected by the image instead of assuming every example creates the same `/dev` node.

Service names and numeric addresses are protocol inputs. Do not silently change a firmware service name while keeping a Linux application configured for the old one. Store the service version and compatibility rules in the application protocol, not only in a filename.

## Back pressure and restart are normal cases

Transmit buffers are finite. Blocking send operations can wait for a buffer; nonblocking operations report that no buffer is available. The kernel RPMsg API documents different behavior for send and try-send operations. Call them only from a context that permits their waiting behavior. [Linux 6.6 RPMsg API](https://www.kernel.org/doc/html/v6.6/staging/rpmsg.html).

A successful send is not an application acknowledgement. If a command changes a physical output, use a request ID and explicit result. On timeout, a retry may execute twice unless the receiver detects duplicates. On restart, a generation identifier prevents a late reply from the old session from satisfying a new request.

Remove endpoints and stop consumers in an order that prevents callbacks from reaching released application state. Remoteproc teardown removes transport objects, but application threads can still hold stale assumptions. Reopen and renegotiate after a remote restart rather than trusting old endpoint identities.

## Debug the chain of evidence

Check firmware loading first, then resource-table discovery, virtio creation, vring setup, mailbox notifications, channel announcement, driver binding and application request/reply. Stop at the first missing step. A later userspace error can be only a symptom of an earlier transport failure.

If notifications arrive but no message completes, inspect shared addresses, ring indices, descriptor lengths and cache visibility. If messages work in one direction only, compare each direction's queue and mailbox setup separately. If the first few work and then stop, buffer return or callback lifetime is a strong candidate.

> [!NOTE]
> **Not run on the reference setup:** remoteproc startup and RPMsg traffic. The 512/16/496-byte relationship was checked against pinned source; the fragmented-record example is a calculation, not a benchmark.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/rpmsg/virtio_rpmsg_bus.c`, inspected header, size selection, send and receive paths.
- `linux-xlnx@xilinx-v2024.1:drivers/remoteproc/{remoteproc_core,remoteproc_elf_loader,xlnx_r5_remoteproc}.c`.
- [Linux 6.6 remoteproc framework](https://www.kernel.org/doc/html/v6.6/staging/remoteproc.html).

---

<sub>← [Programming the RPU](02-rpu-programming.md) · [Chapter index](README.md) · [OpenAMP in PetaLinux](04-openamp-in-petalinux.md) →</sub>
