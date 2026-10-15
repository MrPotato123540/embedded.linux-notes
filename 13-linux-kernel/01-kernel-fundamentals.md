# Kernel Fundamentals

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers

## Kernel responsibilities

The kernel schedules tasks, manages memory, implements filesystems and networking, and controls devices. Applications request services through system calls. Kernel space and user space have different privileges and address mappings.

Linux uses a monolithic kernel design with loadable modules. A module runs with kernel privileges; it is not isolated like a normal process. A faulty driver can corrupt memory used by unrelated subsystems.

## Arm64 execution

On the ZynqMP Cortex-A53, normal Linux kernel execution is at Non-secure EL1 and applications run at EL0. Firmware and virtualization use other levels. Entering the kernel from U-Boot at EL2 does not mean ordinary kernel code remains there.

Virtual addresses used by the CPU are not automatically physical addresses or DMA addresses. Each interface must use the address type it expects. This matters when moving from bare-metal register access to Linux drivers.

## Configuration consequences

A feature can be built in, available as a module, or absent. Early boot requires its dependencies before the final root filesystem is mounted. A module stored only on that filesystem cannot provide the storage path needed to mount it.

## References

- `linux-xlnx@xilinx-v2024.1:init/`, `mm/`, `kernel/`, `drivers/`
- Linux 6.6 AArch64 boot protocol

---

<sub>[Chapter index](README.md) · [linux-xlnx and Kernel Versions](02-linux-xlnx-and-kernel-versions.md) →</sub>
