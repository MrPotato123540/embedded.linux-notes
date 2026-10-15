# Output Files in images/linux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Artifact map

The reference BSP includes the following files. Availability in a new build depends on configuration.

| Artifact | Purpose or producer |
| --- | --- |
| `BOOT.BIN`, `bootgen.bif` | Packaged boot partitions and their Bootgen description |
| `zynqmp_fsbl.elf` | First Stage Boot Loader |
| `pmufw.elf`, `pmu-conf.bin` | PMU firmware and platform-management configuration data |
| `bl31.elf`, `bl31.bin` | TF-A runtime firmware, ELF and raw forms |
| `u-boot.elf`, `u-boot.bin`, `u-boot-dtb.*` | U-Boot executable variants |
| `Image`, `Image.gz`, `vmlinux` | Arm64 kernel, compressed kernel and ELF debugging image |
| `system.dtb` | Compiled device tree |
| `system.bit` | Programmable-logic configuration |
| `image.ub` | FIT container; inspect which components it includes |
| `boot.scr` | U-Boot script with an image header |
| `rootfs.*`, `ramdisk.*` | Filesystem images or archives in selected formats |
| `*.manifest` | Installed package inventory |
| `petalinux-sdimage.wic.xz` | Compressed partitioned disk image |
| `dtbos/`, `openamp.dtb` | Overlays and an alternative device-tree configuration |
| `pxelinux.cfg/` | Network-boot configuration |
| `zynqmp-qemu-*.dtb`, `pmu_rom_qemu_sha3.elf` | QEMU-specific machine and boot support |

## Choosing the correct file

A raw kernel is not an ELF debugging image. A filesystem archive is not necessarily a disk image. A `.wic` image includes a partition layout; `rootfs.ext4` represents a filesystem. Writing one where the other is expected changes the interpretation of every offset.

The kernel recipe produces kernel outputs; device-tree recipes produce DTBs; firmware recipes produce their ELF files; image recipes assemble root filesystems. Boot packaging combines selected outputs. Check recipe deploy directories and package logs when provenance is unclear.

For SD boot, the boot partition and root partition serve different purposes. QSPI requires explicit offsets and erase geometry. JTAG and QEMU load files through their own launch flow. The filename alone does not define where a file belongs.

## References

- Inspected `xilinx-zcu106-2024.1:pre-built/linux/images/`
- AMD UG1144 (2024.1), generated images and packaging

---

<sub>← [The Configuration System](05-configuration-system.md) · [Chapter index](README.md) · [Customizing Through meta-user](07-meta-user-customization.md) →</sub>
