# How U-Boot Boots the Linux Kernel

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot

## Preparing kernel entry

U-Boot loads the kernel and supporting data, prepares the device tree and enters Linux according to the Arm64 boot protocol. `booti` handles an Arm64 Image; `bootm` handles supported containers such as FIT.

Compressed images need enough temporary and destination space. Settings such as `kernel_comp_addr_r` are relevant to supported compressed-Image flows. Account for the decompressed size and U-Boot's own live memory, not only the compressed file size.

## Device-tree fixups

Before handoff, U-Boot can update `/chosen`, memory information and other properties. `bootargs` and initrd boundaries may therefore differ from the DTB stored on disk. Inspect the final tree when debugging Linux's view.

An external initramfs must remain intact until Linux consumes it. If no ramdisk is supplied, the boot command's syntax must express that correctly. A stale address from an earlier load can point to unrelated memory.

## Validation

Compare the loaded sizes, final addresses, selected FIT configuration and command line. Then separate early-kernel failures from root-filesystem failures.

## References

- U-Boot v2024.01 `booti` and `bootm` documentation
- Linux 6.6 AArch64 boot protocol
- [Boot address map](../06-boot-sequence/12-boot-address-map.md)

---

<sub>← [FIT Images and image.ub](04-fit-images.md) · [Chapter index](README.md) · [Customizing U-Boot](06-u-boot-customization.md) →</sub>
