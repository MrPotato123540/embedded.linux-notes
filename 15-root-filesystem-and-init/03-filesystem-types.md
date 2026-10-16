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

## Begin with the storage interface

A filesystem must match the abstraction below it. An SD card or eMMC normally presents a block interface. Its internal controller manages raw flash details. Raw NAND presents eraseblocks, bad blocks and wear behavior through the Memory Technology Device (MTD) layer. A filesystem designed for block devices does not automatically manage those raw-flash properties.

UBI sits above suitable MTD flash and manages logical eraseblocks and wear. UBIFS builds a filesystem on UBI volumes. The source documentation explicitly separates these layers. A UBI image and a UBIFS image are related artifacts with different roles; writing one where the other is expected is a format error.

JFFS2 works through the MTD model and scans flash structures during mount. UBIFS has different indexing and recovery behavior. The choice depends on capacity, boot-time limits, update design and the actual flash type. Avoid choosing from a filename offered by the image build without checking the storage path.

## Read-only and writable images solve different problems

SquashFS stores a compressed read-only filesystem. It is useful when software changes as a whole image. Ext4 supports normal writable block storage, metadata journaling and familiar file operations. A writable filesystem is not necessarily the best place for immutable application binaries, while a read-only filesystem cannot directly store mutable application state.

A common design separates a read-only software image from a writable data partition. That narrows the update and recovery problem. It also makes capacity failure in logs less likely to damage the installed software. The design still needs quotas, cleanup policy and an explicit response when the writable volume fills.

An ext4 journal protects selected filesystem consistency properties. It does not turn several application writes into one application-level transaction. If an application writes a new configuration and then updates an index, a crash between those actions can leave a logically inconsistent pair even if the filesystem mounts cleanly.

## Durability follows the full write path

A successful userspace write often means data reached the kernel's buffers. It does not always mean the storage device has committed the bytes to persistent media. Filesystem writeback, device caches and the storage controller add further stages.

For an important state update, the application needs a defined durability protocol, including error checks and appropriate file/directory synchronization. An atomic rename can make a pathname replacement indivisible to readers, but durability of data and directory changes remains a separate question. The selected filesystem and storage stack must support the guarantees the protocol expects.

Power-cut testing should examine application records, not only whether the volume mounts. Use generation numbers or checksums to tell a valid old record from a partially updated new one. This is a proposed test design; no power interruption was performed for this revision.

## OverlayFS creates a merged view

OverlayFS combines a lower layer with an upper layer. Reading a file can use the lower object until a change requires an upper-layer copy. That copy-up operation can have much higher cost than the small write requested by the application. A tiny edit to a large lower file can therefore create unexpected storage use.

Deleting a lower-layer file needs a marker in the upper layer so that the merged view hides it. The original lower file still exists in the immutable image. This affects both space accounting and updates: replacing the lower image does not automatically remove old upper-layer changes or deletion markers.

The upper and work directories have filesystem and placement constraints, described in the pinned OverlayFS documentation. Do not assume any writable path can serve as an upper layer. The selected filesystem must provide the required features, and the work directory must follow the documented relationship to the upper filesystem.

## A worked update scenario

Suppose release A contains `/etc/app.conf` in a read-only lower image. A user changes it, which creates an upper copy. Release B introduces a new default and a required field. After replacing only the lower image, the old upper copy can still hide release B's file.

The application now runs new code with old configuration. That is not an OverlayFS bug. It is an unspecified migration policy. A correct updater can version the writable state, migrate it, or keep defaults in a versioned immutable location and store only explicit user settings separately.

Rollback needs the same thought. If B changes a database format, booting A again may fail unless data migration is reversible or each software slot has compatible state. Filesystem selection is therefore part of the release architecture.

## Match evidence to the failure

A mount failure on raw flash requires UBI/MTD evidence, volume geometry and image format. An ext4 recovery issue requires block-device errors and filesystem logs. An overlay “missing file” requires checking both layers and deletion markers. A write that succeeds but disappears after power loss requires application durability analysis.

For PetaLinux, preserve image type configuration and generated artifact names with the release. The supplied BSP includes several filesystem outputs, but their existence does not prove that all were boot-tested on every storage medium.

## References

- [linux-xlnx@xilinx-v2024.1:Documentation/filesystems/ubifs.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/filesystems/ubifs.rst).
- [Pinned OverlayFS implementation guide](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/filesystems/overlayfs.rst).

- Linux 6.6 filesystem and MTD documentation
- [UBI and UBIFS](../23-storage-updates-and-production/02-ubi-and-ubifs.md)

---

<sub>← [initrd vs. initramfs](02-initrd-and-initramfs.md) · [Chapter index](README.md) · [Root Filesystem Boot Options in PetaLinux](04-rootfs-boot-options.md) →</sub>
