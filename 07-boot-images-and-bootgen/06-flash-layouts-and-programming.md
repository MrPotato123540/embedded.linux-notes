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

## References

- AMD UG1144 (2024.1), flash partitioning and programming
- [MTD and flash](../23-storage-updates-and-production/01-mtd-and-flash.md)

---

<sub>← [Generating Boot Images With PetaLinux](05-petalinux-package-boot.md) · [Chapter index](README.md) · Next chapter: [08 · First Stage Boot Loader (FSBL)](../08-fsbl/README.md) →</sub>
