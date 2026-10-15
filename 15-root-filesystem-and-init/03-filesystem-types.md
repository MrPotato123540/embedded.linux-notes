# Filesystem Types for Embedded Systems

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Match the storage layer

| Filesystem | Suitable use | Main consideration |
| --- | --- | --- |
| ext4 | Block devices such as SD/eMMC | Journaling does not guarantee application-data consistency |
| FAT/vfat | Firmware-readable boot partition | Limited Unix metadata |
| f2fs | Supported flash-backed block devices | Requires matching kernel/tool support |
| squashfs | Compressed read-only system | Writable state needs another location |
| JFFS2 | Supported raw MTD use | Scaling and flash geometry matter |
| UBIFS over UBI | Raw flash volumes, especially NAND | Requires UBI geometry and bad-block handling |
| tmpfs | Temporary RAM-backed files | Memory limits and volatility |
| overlayfs | Combined lower/upper directory view | Upper-layer persistence and compatibility |
| NFS | Network root or shared development files | Server and network availability |

Raw NAND is not an ordinary disk. Its erase blocks, bad blocks and ECC requirements need the appropriate flash stack. Conversely, an eMMC controller already presents managed block storage; UBIFS is not the normal filesystem above it.

## Selection method

Decide whether the root must be writable, how updates work and what power loss can interrupt. Then select the filesystem and mount policy. Test full-storage behavior, interrupted writes and recovery on the actual device.

## References

- Linux 6.6 filesystem and MTD documentation
- [UBI and UBIFS](../23-storage-updates-and-production/02-ubi-and-ubifs.md)

---

<sub>← [initrd vs. initramfs](02-initrd-and-initramfs.md) · [Chapter index](README.md) · [Root Filesystem Boot Options in PetaLinux](04-rootfs-boot-options.md) →</sub>
