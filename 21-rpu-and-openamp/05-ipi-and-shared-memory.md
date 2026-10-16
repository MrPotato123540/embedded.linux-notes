# IPI and Shared Memory Patterns

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## An interrupt announces work; shared memory holds it

An **inter-processor interrupt (IPI)** lets one processor notify another. It is useful as a doorbell for shared state. It does not by itself define the message format, queue depth, ownership or cache policy.

In the inspected R5 remoteproc driver, `zynqmp_r5_rproc_kick()` copies a virtqueue identifier into a mailbox message and calls `mbox_send_message()`. The RPMsg payload remains in shared transport memory. The receive callback schedules work that checks virtqueues. This gives a concrete separation between notification and data transport.

Do not design an application around one interrupt per record. A receiver can observe several queued records after one notification, and repeated events can be combined. The queue state must tell the receiver what work exists. The interrupt only prompts it to look. [Pinned remoteproc source](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/remoteproc/xlnx_r5_remoteproc.c).

## Distinguish ordering from visibility

A memory barrier orders memory operations as required by the architecture and memory type. Cache cleaning makes dirty data visible beyond a cache when required. Cache invalidation removes stale local copies when required. These operations solve different problems.

The Cortex-A53 and Cortex-R5 software must agree on the shared region's attributes and supported coherency path. Do not assume normal APU SMP coherence automatically covers an arbitrary R5 shared-memory mapping. Use the platform's OpenAMP/libmetal mapping and cache operations rather than inventing ad hoc volatile pointers.

The C keyword `volatile` asks the compiler to preserve certain accesses. It is not a cross-processor lock, a cache-clean operation or a complete memory-ordering protocol. A shared flag can be visible while its payload is stale if publication and cache handling are wrong.

The same rule applies to Linux userspace mapping. A physical address in `/dev/mem` does not describe whether access is cacheable, coherent, reserved or safe. A purpose-built driver or supported shared-memory interface can enforce the actual ownership and mapping contract.

## Design a single-producer, single-consumer ring

For an original teaching ring, the producer owns its producer index and the consumer owns its consumer index. Each slot contains a sequence number, length and payload. The producer checks that a slot is free, fills it, makes the data visible, publishes the new producer position with the required ordering, then notifies the peer.

The consumer observes the published position with matching ordering, makes the payload visible to its CPU if required, validates the slot, processes it, then returns ownership by advancing its consumer position. It must finish reading before publishing that return.

One simple ring leaves one slot unused to distinguish full from empty. With eight slots, usable capacity is seven records. Another design uses monotonically advancing counters and a documented wrap rule. Do not mix the two schemes: their full/empty tests are different.

If a producer runs at 1000 records/s and the consumer can pause for 20 ms, at least 20 records can accumulate before normal queue depth is considered. An eight-slot ring cannot absorb that delay. This calculation identifies a capacity requirement; it does not prove that a larger ring meets the timing deadline.

## Cache-line ownership matters

If producer and consumer indices share a cache line, each side's maintenance can affect bytes the other side changes. Separate independently written fields according to the participating processors' cache-line and mapping requirements. Also avoid placing unrelated mutable application data in the same cache line as a shared descriptor.

A cache clean operates on cache-line granularity, not on the logical fields of a C structure. Padding a structure for one compiler does not automatically produce a cross-processor ABI. Define field widths, alignment and byte order explicitly, then verify structure layout on both builds.

Do not exchange native pointers or unbounded `size_t` values. Linux AArch64 and R5 builds can have different pointer sizes and alignment rules. Use an offset from an agreed base plus a bounded length. Validate `offset <= region_size` and `length <= region_size - offset`; this form avoids overflow in `offset + length`.

## Prevent lost wakeups

A receiver that sees an empty ring and goes to sleep can race with a producer publishing new work. A correct protocol coordinates the empty check, notification state and sleep transition, or uses a transport that already implements this coordination.

After waking, drain available entries until the queue state says no work remains. If the design suppresses notifications while the receiver is active, define exactly how the receiver reenables them and rechecks the queue. Otherwise one unlucky timing window can leave data queued forever with no new interrupt.

This is a reason to use the established virtio/RPMsg transport for ordinary messages. A custom ring may be appropriate for large data, but it brings a synchronization protocol that needs its own review and stress tests. Use RPMsg to carry bounded descriptors only after the data-region ownership rules are defined.

## Reset changes the meaning of every descriptor

A processor reset can leave old indices, partially written records and pending notifications in memory. Include a generation or session field. Agree which side initializes the region and how it proves that the previous owner stopped accessing it.

If a DMA engine remains active after its controlling core stops, clearing the ring is unsafe. Quiesce the device as part of recovery. A processor lifecycle and a peripheral lifecycle are not always the same thing.

Sequence numbers help detect skipped or repeated records. They do not prove that a record is authentic or within bounds. Validate lengths, offsets and protocol version even in a trusted firmware design, because a software fault can produce the same malformed descriptor as an incompatible peer.

## Diagnose publication before blaming interrupts

If an IPI counter increases but the consumer sees old data, inspect cache attributes, maintenance and publication order. If polling finds data but interrupts do not, inspect mailbox routing, acknowledgement and notification suppression. If the ring stops only after wraparound, inspect counter width and full/empty logic.

If data corruption appears only under load, inspect ownership return and cache-line sharing. A slow debug build can hide the timing window, so retain sequence checks in normal builds. Measure queue occupancy and dropped records alongside latency.

> [!NOTE]
> **Not run on the reference setup:** cross-core shared-memory and IPI stress tests. The custom ring is an explanatory design, not a ready-to-deploy implementation. Mailbox and remoteproc paths were inspected in 2024.1 source.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/mailbox/zynqmp-ipi-mailbox.c` and `drivers/remoteproc/xlnx_r5_remoteproc.c`, inspected notification path.
- [Linux circular-buffer documentation](https://www.kernel.org/doc/html/v6.6/core-api/circular-buffers.html), ownership and barrier model; platform cache maintenance remains an additional requirement.
- [Linux memory-barrier documentation](https://www.kernel.org/doc/html/v6.6/core-api/wrappers/memory-barriers.html).

---

<sub>← [OpenAMP in PetaLinux](04-openamp-in-petalinux.md) · [Chapter index](README.md) · [Xen Hypervisor (Overview)](06-xen-hypervisor.md) →</sub>
