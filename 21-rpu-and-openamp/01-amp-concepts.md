# AMP vs. SMP Concepts

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Independent processors

**Asymmetric Multiprocessing (AMP)** runs separate software environments on different processors. On ZynqMP, Linux commonly runs on the A53 APU while bare-metal or RTOS firmware runs on the R5 **Real-Time Processing Unit (RPU)**.

This can isolate a time-critical function from Linux scheduling delays. It does not automatically guarantee safety or timing: shared DDR, interconnects, clocks and reset domains still create dependencies.

## Resource ownership

Assign memory, peripherals, interrupts and DMA channels explicitly. Do not let Linux and R5 firmware independently reconfigure the same device. Reserve shared and remote memory so Linux cannot allocate it for unrelated data.

Define startup, shutdown and recovery. If Linux restarts, decide whether the RPU continues, resets or waits for a new handshake. Include protocol version and state in that handshake so stale shared memory is not mistaken for a valid new session.

## References

- UG1085 (v2.5), RPU and system-interconnect chapters
- [Remoteproc and RPMsg](03-remoteproc-and-rpmsg.md)

---

<sub>[Chapter index](README.md) · [Programming the RPU](02-rpu-programming.md) →</sub>
