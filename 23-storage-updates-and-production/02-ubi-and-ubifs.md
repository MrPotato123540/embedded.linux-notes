# UBI and UBIFS in Practice

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## UBI and UBIFS solve different layers

**Unsorted Block Images (UBI)** sits above raw MTD flash and manages logical-to-physical eraseblock mapping, wear leveling and bad-block handling. **UBI File System (UBIFS)** sits above a UBI volume and provides files, directories, indexing and a journal.

A physical eraseblock (**PEB**) is an erase unit on the flash. A logical eraseblock (**LEB**) is the data unit UBI exposes to a volume. They are not the same size because UBI needs on-flash headers and alignment. UBIFS image parameters must use the LEB geometry, not the raw eraseblock size.

This stack is different from ext4 on eMMC. UBI sees raw erase operations and bad blocks; an eMMC controller hides those details behind block addresses. Putting the wrong layer on the wrong medium loses the assumptions that make the design work.

## Derive the logical geometry

The inspected `drivers/mtd/ubi/build.c:io_init()` takes the physical erase size and minimum write size from MTD. It calculates aligned erase-counter and volume-identifier header placement, then aligns the data start. Finally, `leb_size = peb_size - leb_start`.

For an original NAND example, assume a 128-KiB PEB, 2048-byte minimum I/O, no smaller header subpage and default header offsets. The erase-counter header occupies the first aligned 2048-byte area. The volume-identifier header starts at offset 2048. Data starts at offset 4096, so the LEB is `131072 - 4096 = 126976` bytes, or 124 KiB.

That value is conditional. Smaller supported header subpages or an explicit supported header offset can change the data start. Do not paste 126976 into every UBIFS recipe. Derive it from the target geometry and compare it with the UBI attach report. [Pinned geometry calculation](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/mtd/ubi/build.c).

## Capacity is more than the sum of file sizes

UBI needs internal metadata and spare physical blocks for its management work. Bad-block reserve and existing bad blocks reduce available capacity. UBIFS needs its own index, journal, garbage-collection and metadata space. A directory with 100 MiB of file contents does not fit automatically into a nominal 100-MiB raw partition.

Image creation also has a maximum logical eraseblock count. That controls the filesystem's supported size assumptions. It is distinct from the current amount of file data and the physical block count. An autoresizing volume still needs an image and filesystem configuration compatible with the final size.

For an illustrative capacity review, first compute the raw partition's PEB count. Remove UBI overhead and reserves according to the selected configuration. Convert the remaining volume allocation to LEB bytes. Then budget UBIFS overhead and future growth. Keep each step visible so a media change does not silently reuse an invalid capacity estimate.

## Follow a file update through the stack

UBIFS writes new nodes and journal information rather than overwriting arbitrary old bytes in place. Its index and commit process determine which nodes form the current filesystem state. UBI maps logical eraseblocks to physical storage and moves data as required for flash management.

A crash can leave journal work that must be replayed. In the inspected `fs/ubifs/super.c`, mount processing calls `ubifs_replay_journal()` and handles recovery before completing the writable mount. This is a recovery mechanism, not a promise that every application write before power loss survives.

Application durability still needs the correct synchronization boundary. A successful buffered write can leave data in memory. If a configuration update must survive a reset, define the file and directory update sequence and use the filesystem's synchronization interfaces appropriately. A journal protects filesystem structure; it does not decide which of your application's several files belong to one logical transaction.

## Atomic volume replacement has its own state

UBI volume updates can mark a volume as being updated while data is replaced. An interrupted update can leave the volume unusable until recovery or a new complete update. Do not equate the update marker with an automatic backup of the old volume.

For whole-root-filesystem updates, separate inactive and active volumes can preserve a known-good copy. The boot selector and health-confirmation logic still need their own power-loss-safe design. A completed UBI write and a successful application boot are different acceptance stages.

Static and dynamic UBI volumes also serve different purposes. Their validation and update behavior differ. A writable UBIFS filesystem normally uses a suitable dynamic volume; selecting a volume type only because its name sounds safer is not a design method.

## Image generation must match installation

`mkfs.ubifs` creates filesystem content using the selected minimum I/O size, LEB size and maximum LEB count. `ubinize` wraps volume images in a UBI layout using the physical flash geometry and volume configuration. These tools produce different artifacts for different layers.

An image intended for a UBI volume is not automatically a raw partition image. A raw UBI image includes headers and geometry assumptions. The installer must know which layer it is writing and preserve bad-block handling. This section does not provide a generic erase command because a correct command depends on the identified target and recovery plan.

In PetaLinux, keep image-format and flash-geometry settings in tracked configuration or recipes. Preserve the resolved values and generated volume configuration with the release. A file extension alone cannot prove how an image was generated.

## Diagnose attach separately from mount

Failure to attach UBI points toward MTD selection, header offsets, geometry, image format or media errors. Successful attach with a missing volume points toward the volume table or expected name/ID. A present volume that UBIFS rejects points toward filesystem geometry, content, feature compatibility or damage.

An unexpectedly read-only result can be a deliberate recovery response or a volume/media limitation. Preserve the first error before repeated mounts hide it in later output. Read-only recovery and data extraction may be the right next step; repeated formatting destroys evidence and is not diagnosis.

> [!NOTE]
> **Not run on the reference setup:** UBI attach, UBIFS image generation, flash updates and power-cut tests. Geometry and recovery paths were inspected in pinned source. The 124-KiB LEB is a conditional calculation, not a board value.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/mtd/ubi/{build,io}.c` and `fs/ubifs/{super,journal}.c`, inspected locally.
- [Linux UBIFS documentation](https://www.kernel.org/doc/html/v6.6/filesystems/ubifs.html).
- [MTD UBI documentation](http://www.linux-mtd.infradead.org/doc/ubi.html), volume and on-flash concepts.

---

<sub>← [MTD and Flash Memory](01-mtd-and-flash.md) · [Chapter index](README.md) · [SD and eMMC](03-sd-and-emmc.md) →</sub>
