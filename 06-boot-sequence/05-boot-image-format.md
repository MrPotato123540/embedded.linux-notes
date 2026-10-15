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

## References

- AMD [UG1283 (2024.1), ZynqMP boot-image layout](https://docs.amd.com/r/2024.1-English/ug1283-bootgen-user-guide)
- Bootgen 2024.1 inspection of the reference BSP's `BOOT.BIN`

---

<sub>← [CSU BootROM](04-csu-bootrom.md) · [Chapter index](README.md) · [FSBL Stage](06-fsbl-stage.md) →</sub>
