# Building the FSBL

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot

## Build inputs

An FSBL build needs the matching hardware platform, standalone support libraries, compiler settings and source revision. Vitis/XSCT flows create an application for the selected processor. PetaLinux uses its firmware recipe and generated platform inputs.

In the AMD layers, trace the selected `fsbl-firmware` provider before adding a patch. A patch to an unused provider has no effect. Preserve the exact compiler flags and link map for release builds.

## Debug and size

The source provides debug levels such as `FSBL_DEBUG`, `FSBL_DEBUG_INFO` and `FSBL_DEBUG_DETAILED`. Increased detail adds code and changes timing. Feature-exclusion flags can reduce size, but removing boot-device, security or PL support changes behavior.

OCM space is shared with other boot requirements. Check the linked section ranges, stack and reserved areas; the filesystem size of the ELF is not the runtime memory footprint.

## Validation

Build the ELF, inspect the map, package it into a new boot image and confirm the new image is the one tested. Compare a normal boot with the debug build before using timing results.

> [!NOTE]
> **Not run on the reference setup:** a new Vitis or PetaLinux FSBL build and hardware boot in this continuation.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_debug.h`, `xfsbl_config.h`
- `meta-xilinx-tools@rel-v2024.1`, FSBL firmware recipes

---

<sub>← [FSBL Source Walkthrough](02-fsbl-source-walkthrough.md) · [Chapter index](README.md) · [Customizing the FSBL](04-fsbl-customization.md) →</sub>
