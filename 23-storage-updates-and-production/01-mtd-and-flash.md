# MTD and Flash Memory

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Raw flash interface

The **Memory Technology Device (MTD)** subsystem exposes raw flash properties and operations. NOR and NAND have different behavior. Erase size, write size, ECC and bad-block handling affect image layout and programming.

An MTD partition is a range of flash, not automatically a filesystem. The partition table must agree with bootloader offsets and update policy. A block-style view does not remove raw-flash constraints.

## Tools

`mtdinfo` reports geometry. `flash_erase` erases regions. `flashcp` and `nandwrite` serve different programming cases; choose according to the media and image format. Do not replace a NAND-aware programming flow with a blind byte copy.

> [!WARNING]
> Erase/program operations can destroy boot firmware and persistent data. Confirm device identity, geometry, range and recovery access before use.

Read back the result and test cold boot. Include bad-block behavior and interrupted programming in the production test plan.

> [!NOTE]
> **Not run on the reference setup:** physical MTD programming and power-failure tests.

## References

- Linux 6.6 MTD documentation and mtd-utils manuals
- UG1085 (v2.5), QSPI and NAND controllers

---

<sub>[Chapter index](README.md) · [UBI and UBIFS in Practice](02-ubi-and-ubifs.md) →</sub>
