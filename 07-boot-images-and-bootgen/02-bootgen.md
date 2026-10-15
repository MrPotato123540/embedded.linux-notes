# Bootgen

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[07 · Boot Images, BIF and Bootgen](README.md)** · Part IV: Boot

## What Bootgen does

Bootgen reads a BIF, processes its payloads and emits a boot container for the selected device architecture. It can add headers, padding and supported authentication or encryption structures. A successful packaging operation does not prove that the board configuration or executable code is correct.

| Option | Purpose |
| --- | --- |
| `-arch zynqmp` | Select the ZynqMP format |
| `-image` | Select the BIF input |
| `-o` | Select output file |
| `-w` | Control output overwrite behavior |
| `-log` | Select logging |
| `-read` | Decode supported image structures |
| `-dump`, `-split` | Extract supported image data; check release-specific usage |
| `-process_bitstream bin` | Produce a binary bitstream form |

## Version control

The host's default `/usr/bin/bootgen` reports 2022.2. The guide's new inspection explicitly used `/tools/Xilinx2024.1/Vivado/2024.1/bin/bootgen`, which reports 2024.1. Record the executable version, not just the command name.

Before generating a release, verify all BIF input paths and preserve the generated report. When using security options, retain public verification material and policy records without exposing private keys in logs.

## References

- Executed Bootgen 2024.1 `-read` inspection; saved `bootgen-2024.1-read.txt`
- AMD UG1283 (2024.1), command reference

---

<sub>← [The BIF File Format](01-bif-file-format.md) · [Chapter index](README.md) · [BOOT.BIN Anatomy](03-boot-bin-anatomy.md) →</sub>
