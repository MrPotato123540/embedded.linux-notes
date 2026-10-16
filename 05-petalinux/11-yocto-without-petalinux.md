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

## Inventory the work performed by PetaLinux

A migration begins by identifying the functions that the wrapper currently performs. These include hardware import, machine configuration, provider selection, root filesystem selection, component configuration, deploy-file naming, boot packaging and launch support. Replacing only the top-level build command leaves many of these responsibilities unresolved.

Use a known working project as evidence. Record its final machine name, provider choices, source revisions, kernel configuration, device tree, image package manifest and boot-package inputs. Preserve the generated configuration for comparison, while moving durable policy into maintained layers in the new flow.

The reference project demonstrates why this matters. `plnxtool.conf` adds kernel FIT support, selects a separate initramfs image, defines boot addresses and deploy names, and supplies image-specific package selections. Copying only an application recipe would reproduce none of those decisions.

## Move policy, not temporary build state

Generated configuration is a useful specification of current behavior, but copying the entire build directory is not a maintainable migration. Identify the input responsible for each setting. Put hardware selection in machine/BSP metadata, distribution policy in distribution configuration, and product package selection in image or packagegroup recipes.

Preserve `meta-user` changes, but review their dependencies. An append may assume a provider, generated include file or class supplied by the PetaLinux layer set. If the new layer combination removes that provider, the append must be adapted. A file that still parses may also apply to a different version with different behavior.

Keep source patches narrow and record their base revisions. This makes it possible to distinguish a migration error from a vendor-source upgrade. Changing the build flow and updating every component at once makes failures much harder to isolate.

## Hardware generation remains a required subsystem

The hardware export must still reach the firmware and device-tree generation flow. Depending on the selected release path, this can involve XSCT-based processing or a System Device Tree workflow. Choose one supported flow for the pinned release and preserve its tools and inputs.

An SDT describes a system that may contain several software domains. A Linux description is one view of that system. Domain processing can select resources and generate inputs for different processors. It does not remove the need to define ownership of shared memory, interrupts and peripherals.

The local AMD layer set includes machine-configuration generation code under `meta-xilinx-core/gen-machine-conf/lib/gen-machineconf/`, including `sdt_flow.py`. Inspect the selected release's implementation and inputs rather than applying a newer tutorial to an older layer set. A similarly named generated file is not proof that two flows are equivalent.

## Build a migration comparison matrix

| Area | Compare before and after | Example of hidden divergence |
| --- | --- | --- |
| Early firmware | Source, configuration and packaged ELF identity | Different initialization data |
| Kernel | Provider, revision and final configuration | Driver built as a module instead of built-in |
| Device tree | Resources, chosen properties and reserved memory | Missing external board connection |
| Root filesystem | Packages, files, users and services | Runtime dependency absent |
| Boot packaging | BIF, payloads, addresses and media layout | Correct new kernel paired with old DTB |
| SDK | Sysroot libraries, headers and ABI | Application links against a different library feature set |

Use this matrix to decide which differences are intentional. Exact package equality may not be necessary if the migration deliberately changes policy, but every difference should be explained and tested. A matching kernel version string is far too narrow a criterion.

## Validate in stages

First make the new build reproduce the baseline boot and application behavior. Keep hardware and source revisions stable where possible. Then migrate one product customization at a time and verify its final consumer.

A boot test should use the actual delivery medium and packaging flow, not only a direct kernel load in an emulator. A peripheral test should exercise real traffic and failure recovery, not only driver binding. An update test should include rollback and interrupted-update behavior if the product depends on those features.

Also test the new developer workflow. Can a clean workstation recreate the build? Can an application developer use the published SDK? Can the team identify the source and symbols for a field artifact? These are part of replacing the previous build process, not optional administrative details.

## When direct Yocto is a useful choice

Direct Yocto can make layer ownership and automation more explicit. It also gives the team responsibility for the integration that PetaLinux previously supplied. The choice depends on the team's need for custom distribution policy, multiple products, release automation and control over hardware-generation tools.

Keep a clear boundary between migration and release upgrade. After the baseline is reproduced, a separate change can update the OpenEmbedded series or component versions. This makes regression results easier to interpret and rollback easier to manage.

No complete replacement build or SDT migration was executed in this pass. The section defines the missing integration work using inspected project settings and the pinned local layer structure; it does not claim parity with the working PetaLinux BSP.

## References

- `meta-xilinx@rel-v2024.1`, `meta-xilinx-tools@rel-v2024.1`, `meta-petalinux@rel-v2024.1`
- AMD UG1144 (2024.1), Yocto build environment
- [System Device Tree and Lopper](../12-device-tree/04-system-device-tree-and-lopper.md)

---

<sub>← [BSP Packaging and Reproducible Builds](10-bsp-packaging-and-reproducible-builds.md) · [Chapter index](README.md) · Next chapter: [06 · Boot Sequence](../06-boot-sequence/README.md) →</sub>
