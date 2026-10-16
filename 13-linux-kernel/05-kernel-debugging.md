# Kernel Debugging

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers


## Preserve the first failure and the exact build

Kernel debugging starts with evidence that survives the fault. Keep the complete boot log, exact kernel image, matching `vmlinux`, configuration, modules, DTB and firmware identities. A crash address decoded with another build can point to convincing but incorrect source.

The first warning or fault is often more useful than the final panic. A driver can corrupt memory long before the allocator detects it. A missing provider can cause many later probe failures. Preserve timestamps and the whole surrounding sequence before filtering the log.

Also record workload, CPU affinity, reset type and whether the failure is repeatable. A cold-boot problem and a resume problem can share the final symptom while entering with different hardware state.

## Locate the failing boot boundary

Before the kernel banner, inspect the U-Boot handoff, Image placement, DTB pointer and early console. After the banner but before normal devices, inspect architecture and core initialization. During initcalls, inspect the first failing subsystem or driver. During root mount, inspect storage and filesystem support. After PID 1 starts, include userspace behavior.

The source provides concrete anchors. `arch/arm64/kernel/head.S` reaches `start_kernel()`. `init/main.c` later reaches `rest_init()`, `kernel_init_freeable()`, initcalls and userspace init execution. A message from a later boundary proves earlier control flow progressed, though it does not prove every earlier subsystem is correct.

“Starting kernel” is printed by U-Boot before the transfer. It is not evidence that Linux executed its first C function. Conversely, a missing normal console can hide a kernel that is already running.

## Choose instrumentation for a specific question

Kernel logging records explicit events chosen by the code. Dynamic debug can enable selected existing debug sites when built in. Tracepoints record structured events. Function tracing follows selected function execution. Each answers a different question and changes system overhead differently.

Use scheduler events when asking why a task did not run. Use interrupt events when asking whether an interrupt arrived and how long handling took. Use function tracing for a bounded call path when asking where time or control flow went.

Tracing everything can overwhelm buffers and alter timing. Select the smallest event set that separates the competing explanations. Record the trace clock and buffer-overrun information so missing events are not mistaken for missing execution.

## Interpret an oops as a structured record

An oops can report the faulting PC, link register, exception information, call trace, current task and loaded modules. Start with the first faulting instruction and the access it attempted. Determine whether it is a bad pointer, invalid mapping, permission fault or another exception class supported by the evidence.

Then inspect the object's lifetime. Was the device removed? Was work still queued? Could another CPU free or replace the object? A null check at the faulting line may suppress one symptom while leaving the ownership bug intact.

Address randomization and module load addresses affect symbol lookup. Use the captured address context and exact symbols. A raw offset without its module/build identity is not enough for reliable source attribution.

## Debug a deferred device without guessing delays

If a driver keeps deferring, identify the missing supplier and follow its probe. Clock, reset, regulator, interrupt and firmware dependencies can all matter. A device-tree node with the right compatible string can still lack a usable provider.

A successful probe followed by no interrupts is a different boundary. Inspect interrupt routing, trigger type, hardware status and acknowledgement. A counter that remains zero suggests no delivered interrupt; an increasing counter with no data suggests a later processing problem.

Avoid adding sleeps until a specific timing requirement is known. A delay can hide an initialization race and fail under a different CPU frequency or workload.

## Memory diagnostics expose different classes of bugs

Address sanitizers can detect classes of invalid memory access. Lock checking can expose inconsistent lock ordering and context misuse. Leak tools and allocation tracing help with retained objects. These facilities require suitable configuration and add cost.

A diagnostic kernel is not necessarily timing-equivalent to production. If instrumentation changes the failure, that observation itself is useful: the bug may depend on timing, layout or memory pressure. Keep both configurations and compare one controlled change at a time.

For DMA corruption, inspect mapping, buffer bounds, completion and cache synchronization as well as CPU code. A device can overwrite memory without leaving a direct CPU stack trace at the time of corruption.

## Persistent evidence needs planned storage

A crash can make the serial console or filesystem unavailable. Persistent logging mechanisms can preserve selected records across reboot when the platform is configured for them. Their backing memory or storage needs its own reservation and retention behavior.

Do not assume a RAM-backed crash record survives every reset type. Power removal, firmware initialization or another boot stage can clear it. Test the exact reset path used by the product's watchdog or recovery design.

A watchdog-triggered restart also needs the preceding progress evidence. The next boot's reset cause establishes why reset occurred, but it may not identify which task or device first stopped progressing.

## Turn a hypothesis into a discriminating test

Suppose a network workload crashes during driver removal. One hypothesis is that DMA continues after buffer release; another is that queued CPU work uses freed state. Instrument the stop/completion/free boundaries and the work-cancellation path separately.

A test that disables all networking cannot distinguish those causes. A test that proves DMA is stopped before free while queued work still runs can. Good debugging reduces the set of explanations rather than only making the symptom disappear.

> [!NOTE]
> **Not run on the reference setup:** a new fault injection, target ftrace session, sanitizer kernel or persistent-crash-log test. The source anchors and saved logs support the method; no fabricated crash trace is included.

## References

- [2024.1 kernel initialization source](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/init/main.c) and `arch/arm64/kernel/head.S`.
- [Linux 6.6 ftrace documentation](https://docs.kernel.org/6.6/trace/ftrace.html), event/function tracing and buffer controls.
- `linux-xlnx@xilinx-v2024.1:Documentation/admin-guide/` and `Documentation/dev-tools/`, tool-specific prerequisites and limits.

---

<sub>← [Configuring and Building the Kernel](04-configuring-and-building.md) · [Chapter index](README.md) · [Real-Time Linux](06-real-time-linux.md) →</sub>
