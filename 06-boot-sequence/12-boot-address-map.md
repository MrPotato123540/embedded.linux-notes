# Boot Memory Map: Who Loads What, Where

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Addresses belong to a boot flow

A storage offset, load address and entry address are different values. Storage tells the loader where bytes are stored. The load address tells it where to place them. The entry address tells the processor where execution starts.

Bootgen 2024.1 decoded these addresses from the reference `BOOT.BIN`:

| Partition | Load address | Entry address |
| --- | --- | --- |
| FSBL | `0xFFFC0000` | `0xFFFC0000` |
| TF-A BL31 | `0xFFFEA000` | `0xFFFEA000` |
| Device tree | `0x00100000` | Not executable |
| U-Boot | `0x08000000` | `0x08000000` |

The saved U-Boot network session separately loads `Image` at `0x00200000` and `system.dtb` at `0x00100000`. Those are later-stage choices. They do not relocate the earlier firmware automatically.

## Overlap checks

For every live object, record the start address and full size. Include decompressed kernel size, ramdisk, DTB growth space, U-Boot relocation, stacks and resident firmware. Two files can have different starting addresses and still overlap.

Use half-open ranges `[start, start + size)` when calculating collisions. Also check which addresses are reachable by the loader and the destination processor. An address valid for an A53 view may mean something else to an R5.

Do not invent one universal table for script, FIT and ramdisk addresses: read the environment and script shipped with the chosen image.

## References

- `reference-setup/captures/bootgen-2024.1-read.txt`
- Saved `cap-wp01-uboot.txt`
- [System address map](../03-zynqmp-architecture/04-memory-map.md)

---

<sub>← [User-Space Startup](11-user-space-startup.md) · [Chapter index](README.md) · [Multiboot, Fallback and Golden Images](13-multiboot-and-fallback.md) →</sub>
