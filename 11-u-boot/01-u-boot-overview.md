# U-Boot Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot

## U-Boot architecture

U-Boot is the final general-purpose loader in the reference boot chain. Board initialization prepares its runtime state, relocation moves it into a suitable memory region, and the driver model connects devices with drivers. Its control device tree describes hardware used before Linux starts.

Some platforms use a small **Secondary Program Loader (SPL)** before U-Boot proper. The reference ZynqMP flow uses the FSBL and TF-A instead. Do not add an SPL stage merely because another Arm board needs one.

## Release inputs

The saved banner reports U-Boot 2024.01. AMD's `u-boot-xlnx` release tag includes platform changes beyond the base upstream release. The selected machine recipe and final configuration determine the enabled commands and drivers.

A defconfig is a starting configuration, not a complete record of every selected symbol. Preserve the final `.config` and source revision when debugging a release.

## References

- `u-boot-xlnx@xilinx-v2024.1:board/xilinx/zynqmp/`, `configs/`
- Saved `cap-wp01-uboot.txt`
- [U-Boot v2024.01 documentation](https://docs.u-boot.org/en/v2024.01/)

---

<sub>[Chapter index](README.md) · [Essential U-Boot Commands](02-essential-commands.md) →</sub>
