# The BIF File Format

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[07 · Boot Images, BIF and Bootgen](README.md)** · Part IV: Boot

## BIF structure

A **Boot Image Format (BIF)** file describes the payloads passed to Bootgen. It contains an image name, braces and a list of input files with attributes. It is a build input, not a script executed by the board.

The reference BSP supplies this partition order: FSBL, PMU firmware, TF-A, device tree and U-Boot. Its PMU firmware uses `pmufw_image`; the device tree has `load=0x100000`. TF-A uses `exception_level=el-3` and `trustzone`; U-Boot uses `exception_level=el-2`.

| Attribute | Meaning |
| --- | --- |
| `bootloader` | Identifies the first-stage loader |
| `pmufw_image` | Selects BootROM handling of PMU firmware |
| `destination_cpu` | Processor receiving the partition |
| `destination_device` | Selects a supported non-CPU destination, such as PL |
| `exception_level`, `trustzone` | Handoff execution attributes |
| `load`, `startup` | Memory placement and execution entry |
| `offset`, `alignment` | Placement inside the output image |
| `partition_owner` | Stage responsible for partition handling |

An ELF supplies segment and entry information; a data file needs suitable placement metadata. Do not confuse `offset` in the output file with `load` in target memory.

## Design variants

Add a bitstream only when the early boot flow should configure the PL. R5 firmware needs the correct RPU mode and memory layout. A data partition must not be handed off as executable code. Multiple images require explicit ownership and startup policy.

## References

- Inspected `xilinx-zcu106-2024.1:pre-built/linux/images/bootgen.bif`
- AMD UG1283 (2024.1), BIF syntax and attribute reference

---

<sub>[Chapter index](README.md) · [Bootgen](02-bootgen.md) →</sub>
