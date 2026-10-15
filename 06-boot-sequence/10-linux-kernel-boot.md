# Linux Kernel Boot

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Entry contract

The Arm64 boot protocol defines the state expected at the kernel entry point. The device-tree address is passed in `x0`; the MMU must be off, and cache and interrupt conditions must meet the protocol. Entry can be Non-secure EL1 or EL2. EL2 is recommended when available; it is not the only legal entry level.

Early assembly in `arch/arm64/kernel/head.S` prepares the execution environment before C initialization reaches `start_kernel`. Early console support can make failures visible before the normal serial driver is ready.

## Drivers and root filesystem

Linux reads the device tree and initializes subsystems through initcalls. Drivers probe devices when their dependencies are available. Deferred probing allows a consumer to wait for a clock, regulator or another provider; it is not always a driver bug.

Root startup depends on the selected model. An initramfs is unpacked into an early root filesystem. A block-device root requires its controller, filesystem and storage path. Network root requires working networking early enough. Drivers needed before the final root is mounted must be available at that point, either built in or in the early userspace image.

## Debugging

At `Starting kernel ...`, check the entry contract, DTB placement and console first. At a root-mount panic, check the root argument and early driver availability. These are different stages even if both look like a failed Linux boot.

## References

- Linux 6.6 [AArch64 boot protocol](https://docs.kernel.org/6.6/arch/arm64/booting.html)
- `linux-xlnx@xilinx-v2024.1:arch/arm64/kernel/head.S`, `init/main.c`

---

<sub>← [U-Boot Stage](09-u-boot-stage.md) · [Chapter index](README.md) · [User-Space Startup](11-user-space-startup.md) →</sub>
