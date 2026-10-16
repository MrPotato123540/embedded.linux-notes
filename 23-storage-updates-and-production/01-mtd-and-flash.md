# MTD and Flash Memory

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Raw flash has an erase-before-write contract

The Linux **Memory Technology Device (MTD)** subsystem exposes raw flash characteristics that ordinary block storage hides. Erase size, minimum write size, bad-block behavior and error correction affect how an image must be prepared and updated.

NOR and NAND are different media. NOR commonly supports direct reads and relatively small program operations, with erase performed over larger regions. NAND has page-based programming, eraseblocks, bad blocks and error-correction requirements. A controller driver and the flash device together determine the available operations and reported geometry.

Do not infer the medium from a device filename alone. An eMMC device contains managed flash but normally appears as block storage; its internal controller handles mapping and wear. A raw MTD partition exposes a different contract and needs tools and filesystems designed for that contract.

## Geometry controls every boundary

An erase operation affects a complete erase region. If an update payload shares an eraseblock with another object, replacing the payload can destroy its neighbor even when the payload's byte range does not overlap it. Align partition boundaries and update units to the actual erase geometry.

For an original NOR example with 64-KiB eraseblocks, a 100-KiB object occupies parts of two blocks. Updating its last 36 KiB still requires managing the second whole eraseblock. If boot metadata lives in the unused portion, a naive erase-and-write operation loses that metadata.

Page and erase sizes are device properties, not universal ZynqMP constants. Read the actual MTD geometry and compare it with the flash data sheet, controller capabilities and image-generation settings. Hybrid erase layouts and controller limitations can change what an apparently simple offset means.

## A partition name is not a protection mechanism

The saved QEMU boot log reports these partition ranges:

| Name | Start | End, exclusive | Calculated size |
| --- | ---: | ---: | ---: |
| `qspi-boot` | `0x00000000` | `0x01E00000` | 30 MiB |
| `qspi-bootenv` | `0x01E00000` | `0x01E40000` | 256 KiB |
| `qspi-kernel` | `0x01E40000` | `0x05A40000` | 60 MiB |

These values come from `reference-setup/captures/boot-prebuilt3.log`; they describe that emulated device-tree partition layout. They are not a verified production flash plan and do not authorize writing those ranges on a real board.

A label such as `qspi-bootenv` tells software which region is intended for an environment. It does not prove redundancy, atomic updates or write protection. Check how the bootloader and Linux each find the region, because they may use separate configuration sources.

## NAND adds bad blocks and ECC layout

**Error-correcting code (ECC)** allows the controller or device to detect and, within its capability, correct bit errors. Corrected reads and uncorrectable reads are different events. Track corrected-error trends as well as fatal errors; rising correction counts can provide evidence about media or signal quality.

NAND can contain factory bad blocks and develop more over time. A raw byte-for-byte assumption between image offsets and physical blocks is unsafe unless the format and writer explicitly define bad-block handling. Bad-block markers and out-of-band data also have layout rules.

The boot ROM, bootloader and Linux may use different reading paths. Their ECC and image-layout expectations must agree for data they share. A file read successfully through Linux does not prove the boot ROM can read a raw boot image programmed with incompatible layout rules.

Do not copy spare-area bytes from an unrelated device image as if they were portable payload. They can contain ECC, markers and metadata tied to the original geometry and controller policy.

## Updating raw flash is a transaction design

An erase followed by a write has a period during which the old data is gone and the new data is incomplete. Power loss in that period can leave an unusable object. A checksum detects some damage but does not restore the previous content.

A safer design uses independently valid copies or slots plus metadata that selects a complete candidate. The selector itself needs a recoverable update rule. If both data copies depend on one nonredundant eraseblock of metadata, that block remains a single failure point.

For a small configuration record, an append-only sequence of versioned records with length and integrity checks can avoid erasing the only valid record on every update. Garbage collection still needs a rule that preserves at least one complete record during erase. This is an original design pattern, not a ready-made format for the reference board.

## Linux interfaces expose different abstractions

The MTD character interface supports flash-aware operations. The `mtdblock` block view does not turn raw flash into an SSD with hidden wear leveling and robust atomic sector writes. Do not select an ordinary block filesystem merely because a block-style device node exists.

For writable raw NAND filesystems, UBI and UBIFS provide an appropriate additional layer, described next. For a boot partition, the format may instead be defined by BootROM and Bootgen. Each region can require a different writer and validation method.

Keep destructive programming procedures out of discovery steps. First identify the physical device, partition map, erase geometry, active boot source and recovery path. A production programmer must verify those inputs before any erase and retain a readback/integrity result afterward.

## Diagnose read, program and erase failures separately

A read failure can involve ECC, timing, address mode or the wrong partition. A program failure can involve alignment, write protection or attempting to change bits without erase. An erase failure can involve geometry, protection, power or worn media.

If failures begin above a certain address, inspect address-width and bank-selection behavior. If they appear only at a faster bus clock, inspect timing and board signal quality. If only one image consumer fails, compare that consumer's format and ECC expectations before replacing the flash.

> [!NOTE]
> **Not run on the reference setup:** flash erase/program, physical ECC behavior and power-loss recovery. Existing partition logs were inspected read-only. No MTD device was modified.

## References

- [Linux MTD documentation](https://www.kernel.org/doc/html/v6.6/driver-api/mtd/index.html), raw flash interfaces.
- Existing `reference-setup/captures/boot-prebuilt3.log`, partition layout evidence.
- `linux-xlnx@xilinx-v2024.1:drivers/mtd/`, controller and media implementation; the actual board's flash data sheet supplies device geometry.

---

<sub>[Chapter index](README.md) · [UBI and UBIFS in Practice](02-ubi-and-ubifs.md) →</sub>
