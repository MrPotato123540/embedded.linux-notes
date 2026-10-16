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

## The wrapper chooses inputs before Bootgen sees them

PetaLinux's boot packaging command translates its options and project defaults into a BIF and tool invocation. The first review question is therefore which files were selected. A command that succeeds with a default path can package an older file than the one you intended.

The inspected 2024.1 help exposes `--fsbl`, `--pmufw`, `--tfa`, `--dtb`, `--u-boot`, `--fpga` and other inputs. Some options allow an optional explicit pathname and document a default. Read the exact subcommand help rather than assuming that merely mentioning a flag selects a particular custom file.

The help also states that `--bif` supplies a custom BIF and overrides the other settings. That is an important boundary: when using a custom BIF, inspect that file as the assembly contract instead of assuming separate payload flags still determine the result.

## Review input identity and role

| Input | Review before packaging | Review after decoding |
| --- | --- | --- |
| FSBL | Hardware initialization revision and ELF footprint | Initial-loader identity and destination |
| PMU firmware | Build/configuration and intended loading form | Boot-header or partition representation |
| TF-A | Platform options and entry layout | Secure EL3 attributes and placement |
| U-Boot | Board configuration and environment policy | Non-secure next-stage attributes |
| DTB | Intended consumer and hardware revision | Load address and selected tree identity |
| PL data | Early versus late loading policy | Presence and supported destination |

The kernel may be loaded separately or included through a selected packaging arrangement. Do not infer its location from the presence of `image.ub` in the directory. Follow the generated BIF and boot script.

## A real example of an omitted input

The reference directory contains `system.bit`, but the supplied BIF has no PL partition. It contains FSBL, special PMU firmware input, BL31, a DTB and U-Boot. This is enough to show that a directory listing is not a boot-image manifest.

The same applies after rebuilding. Updating a loose file does not change an existing container. If a changed file is part of the BIF, regenerate the container and verify the new result. If it is loaded separately by U-Boot, update that delivery path instead.

## Understand output format boundaries

The help lists `BIN`, `MCS` and `DOWNLOAD.BIT` formats, with platform-specific limits. A ZynqMP binary boot image is not a complete SD-card image. An MCS representation is programming data for a supported flow. A MicroBlaze download bitstream uses different integration concepts and must not be generalized to ZynqMP.

WIC packaging is a separate disk-layout operation. It can place boot files and root filesystem content into partitions. Flash programming additionally needs erase geometry, device selection and explicit regions. Producing one format does not implicitly perform all later stages.

## Validate the wrapper result at the Bootgen boundary

Preserve the generated BIF and the tool invocation. Decode the resulting `BOOT.BIN` with Bootgen 2024.1 and compare its image list, addresses and attributes with the intended contract. Hash the input files and output container.

A direct Bootgen experiment in this chapter regenerated the supplied boot image byte-for-byte from its five source inputs. This validates the observed assembly relationship. The PetaLinux wrapper itself was inspected through its installed help; a fresh wrapper-driven generation was not run during this pass.

That distinction matters. A direct BIF test cannot prove which defaults the wrapper would choose in a changed project. For a product release, run the actual wrapper or controlled direct-generation path used by the release pipeline and preserve its evidence.

## Deploy and boot the exact candidate

Copy or program the candidate through the intended delivery process, verify the written content and boot from the required reset state. Capture the first-stage and later-stage identity evidence. If a loader can choose several media or slots, record which one it selected.

Keep a known recovery path before replacing physical boot storage. A valid container can still contain firmware that does not initialize the board correctly. Packaging success ends at the file-format boundary; physical boot and product readiness are later validation stages.

**Source trail:** captured `petalinux-package boot --help`, the real BIF, Bootgen decode and the new direct-generation capture. No storage device was written during this work.

## References

- Executed `petalinux-package boot --help` from PetaLinux 2024.1
- Reference `bootgen.bif` and Bootgen decode
- AMD UG1144 (2024.1), boot and WIC packaging

---

<sub>← [Bitstreams: .bit and .bin](04-bitstreams.md) · [Chapter index](README.md) · [Flash Layouts and Programming](06-flash-layouts-and-programming.md) →</sub>
