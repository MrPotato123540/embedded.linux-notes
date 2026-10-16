# AMP vs. SMP Concepts

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Separate the execution models

In **symmetric multiprocessing (SMP)**, one operating system schedules work across compatible CPU cores and manages their shared resources. Linux on the Cortex-A53 application processing unit (APU) normally follows this model. Threads can move between eligible CPUs while the kernel manages their address spaces and synchronization.

In **asymmetric multiprocessing (AMP)**, separate software instances run on different processors. Linux on the APU and a standalone or real-time application on a Cortex-R5 in the real-time processing unit (RPU) form an AMP system. They can share physical memory and peripherals, but they do not share one scheduler or one ordinary process address space.

**Open Asymmetric Multi-Processing (OpenAMP)** supplies software components for communication and remote-processor management. It does not automatically divide all hardware resources or prove real-time behavior. Linux `remoteproc`, RPMsg, firmware resource tables and the R5 application cooperate, but board-level ownership remains a system design task.

## Start with an ownership map

For each peripheral, memory region, interrupt, clock and reset, name the component that may change it. Ownership means more than who calls a driver. If Linux changes a shared parent clock, an R5-owned device may be affected even when Linux never touches its data registers.

| Resource | Example owner | Contract needed |
| --- | --- | --- |
| R5 code, stack and heap | R5 firmware | Linux must not allocate this memory |
| Message pool | Both sides in different states | Buffer handoff and cache rules |
| UART used for R5 logs | R5 firmware | Linux driver must not compete for it |
| Device interrupt | One designated service path | Routing and acknowledgement policy |
| Shared clock/reset | System-level manager | Changes must respect both users |

A device-tree `status = "disabled"` can stop a Linux driver from binding, but it is not a hardware access-control boundary. Reserved memory stops normal Linux allocation of the declared range; it does not authenticate remote firmware or prevent all bus masters from accessing that range.

For systems that need isolation, review hardware protection, firmware permissions and DMA reachability as separate mechanisms. A correct message protocol is useful only after these lower-level ownership decisions are clear.

## Split mode and lockstep solve different problems

In split mode, the R5 cores can run separate workloads. In lockstep mode, the cores execute the same workload with comparison support. Lockstep does not provide two independent application processors or twice the application throughput.

The inspected 2024.1 Linux driver defaults to lockstep when `xlnx,cluster-mode` is absent. Its `zynqmp_r5_cluster_init()` accepts split value 0 and lockstep value 1. Although the matching binding schema also lists value 2, this driver's implementation rejects it. A schema-accepted value is therefore not sufficient evidence that this release implements the mode. [Pinned driver](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/remoteproc/xlnx_r5_remoteproc.c).

Mode selection affects memory interpretation and startup. Choose it with the firmware linker layout and remoteproc nodes. Changing a configuration file after boot cannot safely transform a running pair of processors into a different execution model. The binding documents mode changes as a reset-time decision.

## Work a control-and-data example

Consider an original teaching application: the R5 samples an industrial sensor and Linux writes batches to storage. The R5 owns sampling timing and the sensor peripheral. Linux owns the filesystem and network interface. Shared memory carries batches. RPMsg carries control, status and completion messages.

Define a batch by a shared-memory offset, length, sequence number and format version. Linux validates that the range lies inside the agreed region and that arithmetic cannot overflow. The R5 keeps that batch unchanged until Linux explicitly returns ownership. Sending a message successfully means the transport accepted it, not that Linux already stored the data durably.

If Linux pauses for 200 ms and the R5 produces 10,000 samples/s, at least 2,000 samples accumulate before accounting for normal queueing. At four bytes per sample, that is 8,000 payload bytes. These are illustrative calculations. The design must choose whether a full queue stops acquisition, drops old samples, drops new samples or enters a fault state.

An unbounded buffer is not a real solution. Memory is finite, and a permanently slower consumer eventually catches up with any finite queue. State the overflow behavior in the protocol so both sides can detect data loss.

## Independent software also needs coordinated restart

Linux can restart without the R5 restarting, or the R5 can fault while Linux remains alive. A stale ring entry can then look like a current message. Add a session or generation identifier and define which side initializes shared structures.

On a new session, stop using old descriptors, negotiate compatible protocol versions and establish clean ownership. Do not clear memory while the other processor may still be using it. A restart policy needs a way to confirm quiescence, or a controlled reset that makes the old owner unable to access the region.

A process crash on Linux is another lifetime boundary. The remote processor may continue producing data after its application endpoint disappears. The Linux service should define reconnect, timeout and outstanding-request behavior. A channel appearing again does not prove that previous commands were never executed.

## Real-time claims require a bounded path

The R5 can avoid Linux scheduling delays for local work, but shared DDR traffic, peripheral contention, interrupts and firmware services can still affect timing. Put the time-critical working set in appropriate memory and measure the complete worst-case path under realistic concurrent load.

Average RPMsg round-trip time is not a deadline guarantee. Report the workload, message sizes, queue occupancy, interrupt priorities and tail latency. Separate local R5 control-loop timing from Linux response timing; they have different sources of delay.

For a missed deadline, ask whether the R5 was late before sending, whether transport buffers were unavailable, or whether Linux delayed handling after reception. A single end-to-end number cannot separate these causes. Add timestamps or sequence observations at the ownership boundaries, with a clear relationship between the two clocks.

> [!NOTE]
> **Not run on the reference setup:** concurrent APU/RPU operation, isolation checks and real-time stress tests. The sensor example is an original design exercise. The release mode behavior was checked in pinned source.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/remoteproc/xlnx_r5_remoteproc.c`, cluster initialization and resource ownership.
- [2024.1 R5 binding](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/devicetree/bindings/remoteproc/xlnx,zynqmp-r5fss.yaml).
- [OpenAMP project documentation](https://openamp.readthedocs.io/), architecture; use the component revisions selected by the 2024.1 build.

---

<sub>[Chapter index](README.md) · [Programming the RPU](02-rpu-programming.md) →</sub>
