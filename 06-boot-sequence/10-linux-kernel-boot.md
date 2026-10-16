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

## The first instruction expects a precise machine state

The pinned Arm64 boot document requires the DTB physical address in `x0` and zero in `x1` through `x3`. The CPU must enter in Non-secure EL1 or EL2 with exceptions masked as specified. The MMU is off. Cache state must ensure the loaded kernel bytes are visible and no stale instruction data is used.

The DTB must be aligned to an 8-byte boundary and must not exceed 2 MiB under this protocol. Its placement must also respect the mapping restrictions described by the document. These are loader obligations; a kernel cannot reliably repair a corrupted or inaccessible pointer before it has established its own execution environment.

The raw Arm64 `Image` has a 64-byte header. Its `text_offset`, `image_size` and flags describe placement requirements. The loader places it at the specified offset from an appropriately aligned base and keeps the required range free. A compressed `Image.gz` requires decompression by a supporting loader; the raw kernel entry is not a generic gzip decoder.

## Device activity matters during the handoff

The boot protocol requires DMA-capable devices to be quiesced before entry. An old network or storage DMA operation can overwrite memory while Linux is establishing its own structures. This can create an intermittent early crash even when the kernel and DTB files are correct.

Timers and coherency also have entry requirements. The timer frequency and CPU state must be initialized consistently, and CPUs brought into Linux must share the required coherency domain. These requirements explain why directly jumping to `Image` from an arbitrary debugger state is weaker evidence than a correct firmware handoff.

Use the pinned boot document for the full contract. A short checklist cannot replace architecture-specific conditions, and requirements for other GIC or CPU versions should not be copied blindly into a ZynqMP procedure.

## From assembly entry to C initialization

`arch/arm64/kernel/head.S` establishes the early environment before normal C initialization. It preserves boot arguments and prepares the mappings and state needed to proceed. `start_kernel` then initializes core kernel subsystems. Later initialization creates the process that becomes userspace init.

An early console can produce output before the normal serial driver is ready. The reference log identifies the Cadence early console at `0xFF000000` and later switches to normal console handling. This gives two observation points. Failure before early-console output needs a different investigation from a serial-driver problem after core initialization.

The saved kernel version is `6.6.10-xilinx-v2024.1-g3af4295e00ef`. Keep the matching `vmlinux` for symbol lookup. Symbols from another kernel with the same broad version number can point to different code and produce misleading stack traces.

## Driver registration is not the same as successful probe

Subsystem initialization registers buses and drivers. Devices then bind according to their descriptions and matching rules. A probe can need a clock, reset, regulator, interrupt domain or another provider. If a dependency is not ready, deferred probing allows a later attempt.

A deferred probe is initially useful ordering behavior. A device that remains deferred needs investigation of the missing provider or invalid relationship. Rebuilding the consumer driver will not fix a regulator node that never exists or a clock provider that failed initialization.

For a root-storage controller, availability is time-critical. If the kernel needs the controller to reach the root filesystem, its driver and dependencies must be available before that root is accessible. A module stored only on that root creates a circular dependency unless early userspace supplies the module through another path.

## Early root and final root are different stages

An initramfs supplies an initial userspace tree. Its `/init` can locate, prepare and switch to a final root filesystem. Without a usable early init path, the kernel's root preparation follows the selected boot arguments and supported filesystem path.

In the pinned `init/main.c`, `kernel_init_freeable` checks the early init command and calls `prepare_namespace` when that path is unavailable. Later, `kernel_init` attempts the configured init programs. This separates root discovery from execution of userspace. A root-mount error and an inability to execute `/sbin/init` are different failures.

A visible init file can still fail to execute because its interpreter, architecture or required libraries are wrong. Preserve the exact error code and inspect the executable format. File existence alone is insufficient.

## Use the last confirmed boundary

For silence after U-Boot, verify the loaded image, DTB, state and early-console selection. For a root-mount panic, inspect the root argument, device discovery and built-in/early driver availability. For an init failure, inspect the root contents, permissions and executable interpreter. For a missing product service, continue into userspace diagnostics.

**Source:** pinned `linux-xlnx@xilinx-v2024.1:Documentation/arch/arm64/booting.rst`, `arch/arm64/kernel/head.S` and `init/main.c`, read directly. The log observations come from the supplied BSP boot; no modified kernel was booted during this pass.

## References

- Linux 6.6 [AArch64 boot protocol](https://docs.kernel.org/6.6/arch/arm64/booting.html)
- `linux-xlnx@xilinx-v2024.1:arch/arm64/kernel/head.S`, `init/main.c`

---

<sub>← [U-Boot Stage](09-u-boot-stage.md) · [Chapter index](README.md) · [User-Space Startup](11-user-space-startup.md) →</sub>
