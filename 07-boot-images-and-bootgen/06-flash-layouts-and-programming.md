# Flash Layouts and Programming

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[07 · Boot Images, BIF and Bootgen](README.md)** · Part IV: Boot

## Define the layout first

A flash layout assigns non-overlapping regions to boot firmware, environment, scripts, kernel and root filesystem. Align regions to the device's erase requirements, and leave enough space for future image growth and recovery.

The device tree's MTD partitions, PetaLinux flash settings and U-Boot offsets must describe the same layout. A correct `BOOT.BIN` written at the wrong offset is still unusable.

SD and eMMC commonly use a boot filesystem plus an ext4 root partition. Their partition table is separate from the files stored inside each partition. Record whether the bootloader selects a partition by index, label or UUID.

## Programming and verification

`program_flash`, U-Boot `sf` operations and Linux MTD tools act through different environments. Confirm the selected device, size, erase geometry and write range before using any of them.

> [!WARNING]
> Erasing or programming storage can remove the only bootable image and user data. Keep a tested recovery path and a copy of the existing layout before programming.

After writing, read back and compare the programmed range. Then power-cycle and test recovery. A programmer's success message proves neither the boot-mode selection nor the full application startup.

> [!NOTE]
> **Not run on the reference setup:** physical flash programming, readback and power-loss tests. No destructive command is presented as a tested example.

## A layout is an agreement between several readers

BootROM, FSBL, U-Boot, Linux MTD and the update application can all interpret the same storage. Their views must agree. A partition table in the Linux device tree does not automatically change a hard-coded bootloader offset, and a bootloader environment change does not move existing bytes on flash.

Record each region's start, capacity, erase alignment, owner and update policy. Distinguish capacity from the current artifact size. A region that fits today's image but leaves no planned growth can force a risky layout migration later.

For each interval `[start, start + capacity)`, check that it lies inside the device and does not overlap another live region. Then account for erase operations: erasing a block can affect bytes outside the current file length. Adjacent logical objects should not share an erase unit unless their update procedure explicitly preserves both.

## NOR, NAND and block storage need different assumptions

SPI NOR exposes erase/program constraints that differ from a normal block filesystem. NAND additionally needs bad-block and error-correction handling in the appropriate storage stack. A raw byte offset copied from a NOR example is not a complete NAND deployment strategy.

SD and eMMC present block storage, usually with a partition layout and filesystems. An eMMC device can also expose special boot areas distinct from its normal user area. Identify the exact area used by the board's supported boot flow before writing anything.

The programming tool's device name is only one part of that identity. Confirm capacity, geometry, selected chip or area, and the intended range. A successful write to the wrong device is still a destructive failure.

## Keep boot and runtime partition descriptions consistent

If U-Boot reads a kernel from a fixed flash offset, Linux's MTD partition definition should describe the same stored region. If Linux updates a named partition, its boundaries must preserve the bootloader's neighboring data. If an environment uses a filesystem UUID, the deployed filesystem must carry the expected identity.

A WIC image can define a whole-disk partition layout. A standalone ext4 image defines a filesystem. Writing the filesystem image at the beginning of a whole disk can destroy the partition table rather than populate the intended partition. Match the artifact type to the destination type explicitly.

Labels and UUIDs can reduce dependence on enumeration order, but they must be unique and maintained correctly. Cloning several images with identical identifiers can create ambiguity when devices are attached together.

## Programming has erase, write and verify phases

Erasing establishes the medium state needed for programming. Writing transfers the intended bytes. Verification checks the resulting readable content. These phases can fail independently, and a tool's final message may not establish every product requirement.

Read back the relevant programmed range using a supported method and compare it with the candidate. Account for the tool's representation, padding and any media-specific handling. Then boot from that medium after the required reset. A readback match proves stored bytes, not boot-mode selection or application health.

Avoid verification methods that accidentally read a cache or a different storage view from the one used by boot. Know which device path and offset each tool accesses.

## Preserve recovery across an interrupted update

Keep the currently accepted image and selection metadata outside the normal update's destructive range. Write the candidate into an inactive region, verify it, and update selection state through a procedure designed for interruption.

A golden image is useful only if the device can still reach it after the failure. Test the actual selector, reset behavior and security policy. A recovery image signed with a revoked key or stored in an erased shared block is not a viable recovery path.

Persistent user data also needs a migration policy. A successful software rollback can still fail if the new release changed data into a format the older release cannot read.

## A reviewable programming record

Record the device identity, original layout, candidate checksum, exact target range, erase range, tool version, readback result and cold-boot result. Keep the release's bootloader offsets and Linux partition descriptions with that record.

For a new board, first prove the layout using a recoverable development setup. Do not begin with irreversible provisioning or replacement of the only recovery image. The warning above applies to actual erase/program operations; no such operation was performed here.

The reference setup provides file and format evidence, not physical flash validation. Programming, readback, interrupted-update tests and cold boot remain required before this procedure can be called verified for a board.

## References

- AMD UG1144 (2024.1), flash partitioning and programming
- [MTD and flash](../23-storage-updates-and-production/01-mtd-and-flash.md)

---

<sub>← [Generating Boot Images With PetaLinux](05-petalinux-package-boot.md) · [Chapter index](README.md) · Next chapter: [08 · First Stage Boot Loader (FSBL)](../08-fsbl/README.md) →</sub>
