# UBI and UBIFS in Practice

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## UBI and UBIFS are different layers

**Unsorted Block Images (UBI)** manages volumes over MTD, including wear and bad-block handling. **UBIFS** is a filesystem on a UBI volume. A UBIFS image is not the same as a complete UBI image.

Image generation must use the target's page and erase geometry. `ubinize` assembles a UBI image description; `ubiformat` prepares/programs suitable flash; `ubiattach` attaches an MTD device; `ubimkvol` creates a volume. Their roles should not be confused.

## Boot integration

The kernel needs the MTD driver, UBI and UBIFS support early enough to mount root. The root argument identifies a UBI volume, while attachment identifies the underlying MTD partition. Check both.

Filesystem recovery protects its internal structure, not every application transaction. Applications still need correct write ordering and durable update design.

> [!WARNING]
> Formatting or recreating volumes can erase data. Test geometry and recovery on a controlled device first.

> [!NOTE]
> **Not run on the reference setup:** UBIFS image deployment to raw flash.

## References

- Linux 6.6 [UBIFS documentation](https://docs.kernel.org/6.6/filesystems/ubifs.html)
- mtd-utils UBI tool manuals

---

<sub>← [MTD and Flash Memory](01-mtd-and-flash.md) · [Chapter index](README.md) · [SD and eMMC](03-sd-and-emmc.md) →</sub>
