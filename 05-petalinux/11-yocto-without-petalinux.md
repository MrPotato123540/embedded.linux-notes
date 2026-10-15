# Yocto Without PetaLinux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Moving to direct Yocto

PetaLinux and plain Yocto can use the same underlying AMD recipes. The migration task is to make all generated and implicit inputs explicit. Start with a working PetaLinux image and record its selected providers, versions, machine configuration and package manifest.

Map each product change to a maintained layer: kernel patches, device-tree additions, firmware options, services and image policy. Preserve the hardware export and the tools needed to process it. Do not copy only `meta-user` and assume the hardware-generation path follows automatically.

## System Device Tree

A **System Device Tree (SDT)** describes a wider hardware system than one Linux instance. Domain-specific processing can produce the descriptions needed by different software environments. Machine-configuration generation connects hardware information with the build system.

This does not make all older hardware flows obsolete inside a pinned release. PetaLinux 2024.1 projects and newer AMD examples can expect different tools and generated files. Select one documented release flow and keep its components together.

## Acceptance criteria

Compare boot firmware, kernel configuration, device tree, root filesystem and SDK. Test real peripherals, reboot, update and recovery. A matching kernel version alone is not equivalence: the machine configuration and firmware may still differ.

> [!NOTE]
> **Not run on the reference setup:** a complete plain-Yocto replacement build or migration to a later SDT flow. This section defines the work and checks; it does not claim release parity.

## References

- `meta-xilinx@rel-v2024.1`, `meta-xilinx-tools@rel-v2024.1`, `meta-petalinux@rel-v2024.1`
- AMD UG1144 (2024.1), Yocto build environment
- [System Device Tree and Lopper](../12-device-tree/04-system-device-tree-and-lopper.md)

---

<sub>← [BSP Packaging and Reproducible Builds](10-bsp-packaging-and-reproducible-builds.md) · [Chapter index](README.md) · Next chapter: [06 · Boot Sequence](../06-boot-sequence/README.md) →</sub>
