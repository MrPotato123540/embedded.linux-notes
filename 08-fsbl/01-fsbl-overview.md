# FSBL Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot

## Role and execution environment

The **First Stage Boot Loader (FSBL)** initializes hardware and loads later partitions. The common A53 flow starts in On-Chip Memory at EL3. An R5-based flow has different execution and memory constraints; do not apply A53 exception-level terminology to it.

The source is `embeddedsw/lib/sw_apps/zynqmp_fsbl`. Its build combines platform initialization, boot-device access, partition handling, security support and handoff code. Build-time choices affect which features are included.

## What the FSBL owns

The FSBL uses the exported hardware settings to prepare clocks, pins and DDR. It can configure programmable logic, load processor firmware and prepare TF-A handoff data. Fallback and restart handling depend on the boot flow and enabled features.

It is not the Linux device driver layer. Early setup may be required to reach Linux, but Linux later controls many of the same resources through its own drivers and firmware interfaces. An early register write is not a substitute for a correct device tree.

## Validation

Confirm that the FSBL matches the hardware export and memory layout. Keep its ELF and map file with the packaged image. When changing features, check both footprint and boot behavior.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/`
- UG1085 (v2.5), boot and configuration

---

<sub>[Chapter index](README.md) · [FSBL Source Walkthrough](02-fsbl-source-walkthrough.md) →</sub>
