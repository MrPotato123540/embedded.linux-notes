# FSBL Stage

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## FSBL sequence

The **First Stage Boot Loader (FSBL)** turns the reset-time platform into a system ready to load later software. Its main state machine separates initialization, boot-device and header processing, partition loading, and handoff.

Generated `psu_init` code configures the processing system, including clocks, pins and DDR settings from the hardware design. Board-specific code adds work not fully described by the processor export. Using initialization from another board can fail before any useful DDR test runs.

## Loading and handoff

Partition metadata describes the destination processor, load address, entry address, exception level and security attributes. The FSBL checks and loads each supported partition. A programmable-logic partition is sent through the configuration path rather than executed as CPU code.

The FSBL prepares handoff information for TF-A and transfers control. This handoff is more than a branch to an address: the next stage also expects the correct processor state and image metadata.

## Debugging

Use the stage and error code together. A storage read error, DDR write failure and handoff error require different investigations. Enable only the debug detail needed; added logging changes image size and boot timing.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c`
- Same directory: `xfsbl_initialization.c`, `xfsbl_partition_load.c`, `xfsbl_handoff.c`
- [FSBL source walkthrough](../08-fsbl/02-fsbl-source-walkthrough.md)

---

<sub>← [Boot Image Format](05-boot-image-format.md) · [Chapter index](README.md) · [PMU Firmware at Boot](07-pmufw-stage.md) →</sub>
