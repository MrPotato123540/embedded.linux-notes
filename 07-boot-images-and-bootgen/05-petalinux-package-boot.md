# Generating Boot Images With PetaLinux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[07 · Boot Images, BIF and Bootgen](README.md)** · Part IV: Boot

## Packaging inputs

PetaLinux boot packaging selects firmware, bootloader and optional programmable-logic files, then calls Bootgen with a generated description. Inspect that BIF before assuming the result contains the files you intended.

The installed 2024.1 tool exposes the `petalinux-package boot` subcommand. Older documentation may show `petalinux-package --boot`. Use the installed subcommand help for exact options and defaults.

The reference BIF contains no bitstream partition even though `system.bit` exists beside it. This demonstrates why directory contents are not an image manifest.

## Output types

`BOOT.BIN` is the boot container. An MCS file represents programming data in a different format. A WIC image describes a partitioned disk. A QSPI programming layout additionally needs explicit offsets and capacity checks. These outputs are not interchangeable.

Repackage whenever a contained ELF, data file or BIF attribute changes. Compare the decoded partition list and input hashes, then test the new image. Rebuilding the kernel does not require replacing every boot partition unless the packaging design includes it there.

> [!NOTE]
> **Not run on the reference setup:** a new boot-image generation in this continuation. Installed help and the supplied BIF were inspected.

## References

- Executed `petalinux-package boot --help` from PetaLinux 2024.1
- Reference `bootgen.bif` and Bootgen decode
- AMD UG1144 (2024.1), boot and WIC packaging

---

<sub>← [Bitstreams: .bit and .bin](04-bitstreams.md) · [Chapter index](README.md) · [Flash Layouts and Programming](06-flash-layouts-and-programming.md) →</sub>
