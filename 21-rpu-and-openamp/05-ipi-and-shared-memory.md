# IPI and Shared Memory Patterns

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Notification and data are separate

An **Inter-Processor Interrupt (IPI)** notifies another processor. Shared memory carries the data. A mailbox driver provides a managed transport interface, but the application protocol must still define who owns each buffer.

For a custom ring, define producer/consumer indices, capacity, wrap behavior and reset state. Publish data before publishing its availability, using the required memory barriers and cache operations. `volatile` alone does not provide interprocessor synchronization or cache coherency.

## Reliability

Bound message lengths and validate indices before access. Define overflow behavior: block, reject or drop with a visible counter. Use sequence numbers if the receiver must detect lost or repeated work.

Avoid sharing a channel already used by platform management. On restart, establish a new session before trusting old indices. Test under concurrent traffic and forced endpoint reset.

> [!NOTE]
> **Not run on the reference setup:** custom shared-memory ring validation on hardware.

## References

- `embeddedsw@xilinx_v2024.1:XilinxProcessorIPLib/drivers/ipipsu/`
- Linux 6.6 mailbox and memory-barrier documentation

---

<sub>← [OpenAMP in PetaLinux](04-openamp-in-petalinux.md) · [Chapter index](README.md) · [Xen Hypervisor (Overview)](06-xen-hypervisor.md) →</sub>
