# Kernel Fundamentals

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers


## The kernel owns shared machine services

The Linux kernel manages processes, virtual memory, scheduling, filesystems, networking and device drivers. Applications request these services through system calls. On the common Cortex-A53 arrangement, applications run at Non-secure EL0 and the kernel normally runs at Non-secure EL1.

A system call enters a kernel handler with controlled arguments. It does not permanently move the application into kernel privilege. The kernel validates user memory and permissions, performs or schedules work, and returns a result through the userspace ABI.

The kernel also handles asynchronous work: interrupts arrive independently of the current application, timers expire, devices complete transfers and other CPUs update shared state. Driver correctness therefore depends on execution context and lifetime, not only on producing the right register value once.

## From the AArch64 entry to C initialization

The pinned `arch/arm64/kernel/head.S` begins through `primary_entry`. It preserves boot arguments, establishes the initial exception-level state and prepares early mappings before moving through `__primary_switch` and `__primary_switched` toward `start_kernel()`.

The device-tree pointer supplied in `x0` is preserved for early use. This is one reason the bootloader's handoff contract matters: an invalid pointer can fail before normal drivers or a full console exist.

`start_kernel()` in `init/main.c` initializes core services in a deliberate order. It disables local interrupts early, identifies the boot CPU, runs architecture setup, processes the command line and prepares memory, scheduler and interrupt facilities. A function that is safe later in boot may depend on services that do not exist at this point.

## Initialization order is visible in the source

The source calls `sched_init()` before enabling the normal timer-interrupt environment. It initializes early workqueue structures before normal worker execution becomes available. Later `kernel_init_freeable()` calls `workqueue_init()`, performs SMP-related setup and runs basic setup and initcalls.

This distinguishes “a work item can be queued” from “a worker can already run it.” Similar distinctions appear throughout boot. When adding early code, identify whether memory allocation, sleeping, interrupts and worker threads are available at that exact point.

`rest_init()` creates the kernel's init task and the kernel-thread infrastructure. `kernel_init()` later attempts the configured userspace init paths. Reaching the kernel banner is much earlier than successfully executing PID 1.

## Three execution contexts need different rules

Process context can usually sleep when the specific call path and held locks allow it. Hard-interrupt context must not perform operations that can sleep. Deferred work can move longer processing into a suitable context, but it adds scheduling and lifetime requirements.

For a device interrupt, a short handler can acknowledge the condition and arrange later work. The later work must still own the data and device state it uses. Removing the device while work is pending can create an access-after-free bug even when the interrupt handler itself is correct.

Locking must match the contexts that share state. A mutex is useful for sleepable serialization, while low-level interrupt paths need the appropriate non-sleeping rules. PREEMPT_RT changes some lock implementations, so do not infer context safety from a lock's name alone.

## Virtual addresses, physical addresses and DMA addresses

A process pointer belongs to its virtual address space. A kernel pointer belongs to kernel mappings. A physical address names memory in the CPU's physical view. A DMA address is the address a device is told to use and can differ because of bus translation or an IOMMU.

These values can happen to look similar on a simple system, but they are not interchangeable types. Casting a userspace pointer to a device register does not make it a DMA buffer. The driver must use the relevant memory and DMA APIs.

Cache visibility is another part of ownership. A CPU can have newer cached data than memory visible to a noncoherent device. The DMA API expresses mapping and synchronization needs; an arbitrary barrier does not automatically perform the required cache maintenance.

## Built-in drivers and modules share kernel privilege

A built-in driver is linked into the kernel image. A module is loaded later into the running kernel. Both execute with kernel privileges and can corrupt the system if their code or lifetime rules are wrong.

A module needs a compatible build interface, configuration and exported symbols. Merely compiling a `.ko` against a directory named “6.6” does not establish compatibility with this vendor kernel. Keep the exact kernel build artifacts and module version information together.

A driver needed to reach the root filesystem must be available before that filesystem can provide modules. It can be built in or included with its dependencies in the initramfs. Placing the only storage driver on the storage device it is needed to mount creates a dependency loop.

## Follow one boot failure to the correct subsystem

If the kernel starts but cannot mount root, inspect root selection, storage enumeration and filesystem support. If root mounts but PID 1 cannot execute, inspect the file, permissions, executable architecture and interpreter. If a peripheral is absent, inspect device-tree population and probe.

These failures occur after different successful boundaries. Replacing the FSBL to fix a missing userspace dynamic linker is unlikely to help. Preserve the first meaningful error and the last completed boot stage.

The reference kernel identifies itself as the PetaLinux 2024.1 AMD 6.6.10 build. The sections that follow connect that source identity to image formats, configuration and debugging so that a source change can be traced into the running system.

## References

- [2024.1 Linux initialization](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/init/main.c).
- `linux-xlnx@xilinx-v2024.1:arch/arm64/kernel/head.S` and `Documentation/arch/arm64/booting.rst`.
- [Device-tree driver matching](../12-device-tree/02-bindings-and-driver-matching.md) and [kernel modules](../14-kernel-modules-and-drivers/README.md).

The boot flow above was read from pinned source and compared with saved boot evidence; no new kernel was built or booted for this section.

---

<sub>[Chapter index](README.md) · [linux-xlnx and Kernel Versions](02-linux-xlnx-and-kernel-versions.md) →</sub>
