# BOOT.BIN Anatomy

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[07 · Boot Images, BIF and Bootgen](README.md)** · Part IV: Boot

## Reading the container

The boot header comes first. Header tables connect image descriptions to partition descriptions. Payloads follow at aligned offsets. Security-enabled images can add certificates and encrypted structures, so visible byte boundaries depend on the selected format.

In the inspected reference image, the image-header table starts at `0x8C0`, and the partition-header table at `0x1100`. Bootgen reports four image headers: FSBL, BL31, device tree and U-Boot. PMU firmware is handled through the boot-header form selected by `pmufw_image`, so counting BIF lines is not a reliable way to predict the image-header count.

## Integrity and comparison

A header checksum detects certain accidental changes; it is not authentication. Compare files with cryptographic hashes to identify exact artifacts, and inspect decoded metadata to explain why two images differ.

Check that table pointers stay inside the file, that lengths use the documented units, and that load ranges do not overlap live memory. A word-based partition offset must be converted before comparing it with a byte file position.

Padding differences can change a whole-file hash without changing an executable. Conversely, matching filenames can hide completely different firmware. Store the BIF, input hashes and tool version with each release.

## References

- Bootgen 2024.1 decode of the reference `BOOT.BIN`
- [Selected header fields](../06-boot-sequence/05-boot-image-format.md)
- AMD UG1283 (2024.1), ZynqMP image and partition headers

---

<sub>← [Bootgen](02-bootgen.md) · [Chapter index](README.md) · [Bitstreams: .bit and .bin](04-bitstreams.md) →</sub>
