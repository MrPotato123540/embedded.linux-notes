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

## Separate the packager from the firmware compiler

Bootgen consumes already prepared inputs. It does not compile the FSBL, synthesize the PL or check that a Linux driver matches a register map. It interprets the BIF and input formats, creates the architecture-specific container and applies requested packaging/security operations.

A generation error therefore needs to be classified. A missing input path is a packaging-input problem. An invalid BIF attribute is a format/configuration problem. An ELF whose placement does not fit the intended memory map may require a firmware build change. A runtime failure after successful generation can be outside Bootgen's validation scope.

Select `-arch zynqmp` explicitly for this platform. Other AMD device families use different boot structures and firmware roles. A similarly named output file is not proof that the correct architecture was selected.

## Executed regeneration experiment

On 16 October 2026, the reference BIF was copied to a fresh temporary directory. Its five payload paths were changed to absolute paths under the supplied BSP's `pre-built/linux/images`. No firmware binary or BIF attribute was changed. The following command was executed:

```console
$ /tools/Xilinx2024.1/Vivado/2024.1/bin/bootgen -arch zynqmp -image /tmp/bootgen-guide-uwzueztd/reference.bif -o /tmp/bootgen-guide-uwzueztd/BOOT.BIN
[INFO]   : Bootimage generated successfully
```

The temporary directory name identifies this recorded run; it is not a persistent project path. Both the supplied and regenerated files were then hashed and decoded.

| Artifact | Size | SHA-256 |
| --- | ---: | --- |
| Supplied BSP `BOOT.BIN` | 1,838,720 bytes | `97363bab9a28ecda6713840aa55986b98b09fd51b016b030224064f04af612ff` |
| Regenerated `BOOT.BIN` | 1,838,720 bytes | `97363bab9a28ecda6713840aa55986b98b09fd51b016b030224064f04af612ff` |

The files are byte-for-byte identical by this hash comparison. This demonstrates reproducible packaging from the supplied binaries with this Bootgen build. It does not demonstrate reproducible compilation of those binaries, secure-boot enforcement or physical-board execution.

The complete generation and decode record is saved in the local reference setup as `captures/bootgen-regeneration-2026-10-16.txt`, outside this repository. The original BSP files were read only; output went to the fresh temporary directory.

## Interpret the decode before comparing binary bytes

The decoded boot header shows initial firmware information and table locations. Image headers identify image records. Partition headers describe lengths, destination addresses and attributes. Read these structures in order to understand a difference between two outputs.

A changed whole-file hash can result from a changed executable, altered metadata, padding or security data. The hash identifies the exact file but does not explain the difference. Compare the BIF and input hashes first, then decoded fields, then payload bytes where necessary.

Pay attention to units. The decode labels word-based pointers with `(W)`. A partition length represented in words must be converted before comparison with a byte count. Load addresses belong to target memory and must not be used as offsets into the host file.

## Keep overwrite behavior deliberate

Generate release candidates into distinct output locations or use an explicit overwrite policy. Replacing the only known-good file makes comparison and recovery harder. Preserve the successful command, BIF and input manifest with each candidate.

An output pathname also does not define deployment. Producing `/tmp/.../BOOT.BIN` does not write flash, update an SD card or change the running board. Programming and boot validation are separate stages with their own device and range checks.

## Security options need a coherent policy

Authentication and encryption affect the generated format and the device's expectations. Key selection, accepted algorithms, certificate structure and provisioning policy must agree. A generated encrypted file is not proof that the target has the required key or that authentication is enforced.

Keep private key material out of ordinary build logs and shared examples. Preserve public verification material and the policy needed to understand the release. Do not infer a secure production result from this unsigned regeneration experiment.

**Evidence:** locally executed Bootgen 2024.1 generation and decode, SHA-256 comparison, and installed command help. The matching source-level format reference is UG1283 2024.1.

## References

- Executed Bootgen 2024.1 `-read` inspection; saved `bootgen-2024.1-read.txt`
- AMD UG1283 (2024.1), command reference

---

<sub>← [The BIF File Format](01-bif-file-format.md) · [Chapter index](README.md) · [BOOT.BIN Anatomy](03-boot-bin-anatomy.md) →</sub>
