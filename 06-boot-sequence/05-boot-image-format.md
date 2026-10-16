# Boot Image Format

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Header and partition structure

`BOOT.BIN` is a structured container. Its boot header gives the BootROM enough information to locate initial firmware. Image and partition tables describe later payloads. Padding, certificates and optional security data are part of the format.

The table below is a **selected field map**, checked by decoding the reference file with Bootgen 2024.1. Offsets are byte offsets from the boot-header start.

| Offset | Field | Reference value |
| --- | --- | --- |
| `0x20` | Width detection | `0xAA995566` |
| `0x24` | Image identifier | `0x584C4E58` |
| `0x2C` | FSBL execution address | `0xFFFC0000` |
| `0x30` | Initial source offset | `0x2800` |
| `0x34` | PMU firmware length | `0x1FAE0` |
| `0x3C` | FSBL length | `0x1F448` |
| `0x44` | Attributes | `0x800` |
| `0x48` | Header checksum | `0xFD164DF1` |
| `0x98` | Image-header-table offset | `0x8C0` |
| `0x9C` | Partition-header-table offset | `0x1100` |

These values describe one file, not universal load settings. Other fields include total lengths, key/IV data and register-initialization information. Use the full UG1283 field definitions when implementing a parser.

## Inspection

The executed inspection was:

```console
$ /tools/Xilinx2024.1/Vivado/2024.1/bin/bootgen -arch zynqmp -read /home/anado/Downloads/xilinx-zcu106-2024.1/pre-built/linux/images/BOOT.BIN
```

The complete output is saved outside the guide in `reference-setup/captures/bootgen-2024.1-read.txt`. Some table fields use word offsets while others use byte addresses. Preserve the units when checking bounds or following a table pointer.

## Follow a pointer using the correct unit

A structured boot image has several coordinate systems. A boot-header field can name a byte offset from the image start. A later table field can store an offset in 32-bit words. Load and entry addresses refer to the processor's memory map instead of the file. A parser must retain the unit and base for every value.

The reference Bootgen output marks some pointers with `(W)`. For example, the first image header's next-header value is `0x250` words. Multiplying by four gives byte offset `0x940`. Reading byte offset `0x250` instead would interpret unrelated bytes as a header and produce misleading values.

Before following any pointer, check that the resulting range lies inside the file. Use an overflow-safe calculation for `offset + length`. Validate alignment and the expected structure before reading fields. This matters even for a diagnostic parser: a malformed file should produce a clear bounds error rather than a plausible but false memory map.

## Reconcile PMU firmware and FSBL lengths

The inspected file is 1,838,720 bytes long. Its boot header reports PMU firmware length `0x1FAE0` and FSBL length `0x1F448`. A read-only Python inspection of the binary confirmed these values and the first partition length field:

```text
PMUFW length: 0x1fae0 129760
FSBL length: 0x1f448 128072
Combined length: 0x3ef28 257832
First partition length words: 0xfbca
First partition length bytes: 0x3ef28 257832
```

The arithmetic is `0x1FAE0 + 0x1F448 = 0x3EF28`, and `0xFBCA × 4 = 0x3EF28`. This explains why the first partition's reported length is larger than the FSBL file-data length alone in this layout. The special PMU firmware form participates in the initial image representation.

This is a consistency check for the actual BSP image. It is not a general formula for every encrypted, authenticated or padded image. Those modes add format-specific lengths and data. Use the relevant total-length fields and documented rules when inspecting them.

## Count inputs, images and partitions separately

The BIF contains five file inputs: FSBL, PMUFW, BL31, a DTB and U-Boot. The image header table reports four images. PMUFW is supplied through `[pmufw_image]`, so a one-line-one-image assumption is wrong for this file.

An ELF input can also contain several loadable regions. Packaging decides how the supported ELF information is represented in partitions. Inspect both the original ELF and the packaged output when a load address or size is surprising. The file's entry point is not necessarily the lowest address represented by an ELF program header.

For the reference BL31, `readelf -l` reports entry `0xFFFEA000`, while the ELF load segment begins at `0xFFFE0000` because of its segment layout. Section inspection places `.text` at `0xFFFEA000`. Bootgen reports the packaged BL31 partition load and entry at `0xFFFEA000`. These observations are consistent once the ELF layout and packaging are distinguished.

## Stored bytes are not the whole runtime footprint

ELF sections such as `.bss`, stacks and translation tables can occupy memory without corresponding initialized bytes in the file. The reference BL31 ELF contains such `NOBITS` sections. A boot-image file length therefore cannot be used as the sole memory-reservation size.

For the reference BL31, section inspection extends through `.coherent_ram` ending at `0xFFFFE000`. Its executable content starts earlier at `0xFFFEA000`. The runtime ownership analysis must account for that wider region and the firmware's platform layout, even though only initialized content is stored in the partition.

The same principle applies to decompression and temporary buffers. A small compressed kernel can require a much larger destination. A temporary source buffer and its destination can conflict while a loader is still copying. Include lifetimes as well as address ranges in an overlap analysis.

## Validate format and policy independently

Bootgen decoding proves the tool can interpret the file. Header and payload checks can detect structural damage. They do not establish that the chosen processor, exception level, trust state or hardware revision is appropriate for the product.

Review those attributes against the next-stage contract. Then test the packaged file through the intended boot path. A debugger loading the original ELFs bypasses some container processing and cannot by itself validate the boot image stored in flash.

**Evidence:** Bootgen 2024.1 output, direct read-only field inspection, and `readelf -l`/`readelf -S` on the supplied firmware ELFs. No boot-image bytes were modified during these checks.

## References

- AMD [UG1283 (2024.1), ZynqMP boot-image layout](https://docs.amd.com/r/2024.1-English/ug1283-bootgen-user-guide)
- Bootgen 2024.1 inspection of the reference BSP's `BOOT.BIN`

---

<sub>← [CSU BootROM](04-csu-bootrom.md) · [Chapter index](README.md) · [FSBL Stage](06-fsbl-stage.md) →</sub>
