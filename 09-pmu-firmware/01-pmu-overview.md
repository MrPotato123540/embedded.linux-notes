# PMU Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot

## PMU and its two software stages

The **Platform Management Unit (PMU)** is a dedicated control subsystem. Its MicroBlaze-based processor has redundancy for reliability and runs independently of the A53 application processors. PMU ROM performs early fixed tasks; PMU firmware adds configurable runtime behavior.

The PMU has local memory and communication/control interfaces, including general-purpose inputs/outputs and Inter-Processor Interrupts (IPI). These let it coordinate power and reset operations without depending on a Linux process.

## Runtime responsibility

Linux drivers request clocks, resets and power resources through the platform firmware interfaces. PMU firmware manages the platform policy and hardware sequences for supported operations. This is why apparently unrelated peripherals can fail when the firmware interface is missing.

The PMU is not a general replacement for the RPU application processors. Keep its firmware small and bounded so management requests and error handling remain responsive.

## Evidence

The reference serial capture reports `PMU Firmware 2024.1`. This identifies the running build family, but not every enabled feature. Feature checks and matching source/build flags are needed for a detailed capability claim.

## References

- UG1085 (v2.5), PMU and platform-management chapters
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/`
- Saved `boot-manual-1.log`

---

<sub>[Chapter index](README.md) · [PMU Firmware Architecture and Source](02-pmufw-architecture-and-source.md) →</sub>
