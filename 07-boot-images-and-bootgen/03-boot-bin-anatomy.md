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

## Walk the actual tables

The reference file begins with the boot header. Its image-header-table offset is `0x8C0`; its partition-header-table offset is `0x1100`. The image-header table reports four images. The image records identify FSBL, BL31, the DTB and U-Boot.

These are host-file offsets. The DTB's target load address `0x00100000` belongs to a different address space. A parser that seeks to that position in the file has confused storage layout with runtime placement.

The image-header links use word-based values. For example, a pointer value of `0x250` words identifies byte offset `0x940`. Apply the documented unit to each field independently; do not assume every offset in every structure uses the same unit.

## Reconcile the special initial payload

The boot header gives PMU firmware length `0x1FAE0` and FSBL length `0x1F448`. Their sum is `0x3EF28` bytes. The first partition header reports `0xFBCA` words, which is also `0x3EF28` bytes. This matches the special `pmufw_image` arrangement selected by the BIF.

The arithmetic explains an apparent mismatch between the FSBL ELF's file-backed size and the first partition's stored length. It also explains why PMUFW is not represented as a fifth ordinary image header in this file. Count the structures produced by the format instead of imposing a one-input-one-record model.

For an authenticated or encrypted image, additional lengths, certificates and padding need their own interpretation. The unsigned example is a useful starting point, but its arithmetic must not be generalized without the relevant format rules.

## Inspect one later partition

The reference BL31 partition offset field is `0x105D0` words, giving byte position `0x41740`. Its total-length field is `0x3025` words, or `0xC094` bytes. The range therefore ends at byte offset `0x4D7D4` before later alignment and layout details are considered.

The same partition reports load and entry address `0xFFFEA000`. These values are unrelated to the byte position `0x41740` except that the loader obtains bytes from one and places them at the other. The target execution attributes identify Secure EL3 on A53-0.

Inspecting a data partition provides a useful contrast. The DTB has a destination address but is not an executable entry point. A zero or unused execution field must not be interpreted as an instruction to branch to address zero.

## ELF and packaged representations serve different consumers

Bootgen reads ELF metadata to construct supported partitions. The original ELF can include symbols, debug information, padding and uninitialized regions that are not copied verbatim into the boot container. Comparing an entire ELF file with a partition's bytes is therefore not a general validation method.

Use program headers and sections to understand the executable's memory model. Use Bootgen's decode to understand the packaged load representation. Keep the original ELF for debugging because the boot container is not a substitute for its symbol table.

For resident firmware, include runtime memory beyond initialized partition data. The reference BL31 has stacks, BSS, translation tables and coherent memory. Their lifetime continues after the initial handoff.

## A robust inspection checks bounds before meaning

For each structure, validate that its bytes are available. Check counts before iterating, pointer units before seeking, and length arithmetic before slicing. Reject a structure that points beyond the file instead of printing whatever bytes happen to be present.

Then check semantic relationships: expected architecture, processor destination, security state, load region and entry point. A file can pass structural checks while still describing an unsuitable boot arrangement. A valid signature can authorize content that is incompatible with the board if the release process selected the wrong hardware revision.

## Compare releases at several levels

Keep the whole-file checksum for identity. Keep decoded metadata for layout comparison. Keep input hashes and the BIF for provenance. Keep build configuration and source revisions for the firmware's origin. Each level answers a different question.

The local regeneration experiment reproduced this exact file from the supplied binaries. That is a strong check of the packaging interpretation. It remains separate from firmware compilation and physical boot validation.

**Evidence:** direct read-only parsing of the supplied bytes, Bootgen 2024.1 decode, firmware ELF inspection, and the regeneration capture described in the previous section.

## References

- Bootgen 2024.1 decode of the reference `BOOT.BIN`
- [Selected header fields](../06-boot-sequence/05-boot-image-format.md)
- AMD UG1283 (2024.1), ZynqMP image and partition headers

---

<sub>← [Bootgen](02-bootgen.md) · [Chapter index](README.md) · [Bitstreams: .bit and .bin](04-bitstreams.md) →</sub>
