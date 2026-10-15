# Kernel Image Formats

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers

## Kernel output formats

| File | Meaning |
| --- | --- |
| `vmlinux` | ELF kernel image used for symbols and debugging |
| `Image` | Raw Arm64 kernel image for the boot protocol |
| `Image.gz` | Compressed representation requiring a supported loader path |
| `zImage` | Common self-decompressing 32-bit Arm format; not the normal Arm64 output |
| `uImage` | Legacy U-Boot image container |
| `image.ub` | PetaLinux FIT container |
| `System.map` | Kernel symbol/address listing |

A file extension is not validation. Inspect the header and use the boot command supported for that format. `booti` and `bootm` have different input contracts.

## Embedded and separate data

An initramfs can be built into the kernel or supplied externally. A DTB is normally passed separately on Arm64 or selected from a container such as FIT. Do not assume a kernel binary contains either simply because the boot script supplies no obvious filename.

Keep `vmlinux` and debug information for the exact deployed kernel. A nearby build can give misleading stack addresses even when its version string looks similar.

## References

- Linux 6.6 AArch64 boot protocol
- Reference `pre-built/linux/images/` inventory and FIT inspection

---

<sub>← [linux-xlnx and Kernel Versions](02-linux-xlnx-and-kernel-versions.md) · [Chapter index](README.md) · [Configuring and Building the Kernel](04-configuring-and-building.md) →</sub>
