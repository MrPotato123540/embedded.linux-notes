# Roadmap and Work Packages

The guide is written in **work packages (WPs)**. Each work package delivers one chapter: WP-NN corresponds to chapter NN. A work package is finished only when its content has been checked against the 2024.1 sources and, where possible, run on hardware.

## How a work package is executed

1. **Scope.** Review the planned outline in the chapter's section files, then add, drop or reorder topics.
2. **Research.** Read the primary sources at the pinned 2024.1 tags (cloned outside this repository) and the real BSP projects.
3. **Draft.** Write the sections following [CONTRIBUTING.md](CONTRIBUTING.md).
4. **Verify.** Run every command. Check every address, register and default value against its source. Anything not yet verified carries an *Unverified* warning.
5. **Review.** Read through the chapter and make corrections.
6. **Close.** Update the status here and in the chapter index, then commit as `WP-NN: <summary>`.

## Status legend

| Mark | Meaning |
| --- | --- |
| 🚧 | Planned: outline agreed, no content yet |
| ✍️ | In progress |
| 👀 | In review |
| ✅ | Done: written and verified |

## Phases

| Phase | Work packages | Goal |
| --- | --- | --- |
| 0 · Scaffolding | WP-00 | Repository structure, README, roadmap, writing rules |
| 1 · Core platform | WP-01 to WP-16 | From Linux basics to a fully understood, customizable PetaLinux 2024.1 system: hardware, build, boot chain, device tree, kernel, rootfs and applications. |
| 2 · Advanced subsystems | WP-17 to WP-24 | PL integration and DFX, acceleration, graphics and video, RPU/OpenAMP, networking, production topics and bring-up. |
| 3 · Security | WP-25 to WP-27 | Security and cryptography fundamentals, ZynqMP secure boot and hardware security, Linux and network hardening. |
| 4 · Appendices and final review | WP-28 | Glossary, cheat sheets, register quick reference, references and a full consistency pass. |

## Overview

| WP | Chapter | Sections | Phase | Depends on | Status |
| --- | --- | ---: | ---: | --- | --- |
| [WP-00](#wp-00) | Repository scaffolding | – | 0 | – | ✅ |
| [WP-01](#wp-01) | [01 · Linux Fundamentals](01-linux-fundamentals/README.md) | 8 | 1 | – | 👀 |
| [WP-02](#wp-02) | [02 · Embedded Linux Concepts](02-embedded-linux-concepts/README.md) | 4 | 1 | [WP-01](#wp-01) | 👀 |
| [WP-03](#wp-03) | [03 · Zynq UltraScale+ MPSoC Architecture](03-zynqmp-architecture/README.md) | 10 | 1 | – | 👀 |
| [WP-04](#wp-04) | [04 · The Yocto Project](04-yocto-project/README.md) | 8 | 1 | [WP-01](#wp-01), [WP-02](#wp-02) | 🚧 |
| [WP-05](#wp-05) | [05 · PetaLinux 2024.1](05-petalinux/README.md) | 11 | 1 | [WP-04](#wp-04) | 🚧 |
| [WP-06](#wp-06) | [06 · Boot Sequence](06-boot-sequence/README.md) | 15 | 1 | [WP-03](#wp-03) | 🚧 |
| [WP-07](#wp-07) | [07 · Boot Images, BIF and Bootgen](07-boot-images-and-bootgen/README.md) | 6 | 1 | [WP-06](#wp-06) | 🚧 |
| [WP-08](#wp-08) | [08 · First Stage Boot Loader (FSBL)](08-fsbl/README.md) | 5 | 1 | [WP-06](#wp-06), [WP-07](#wp-07) | 🚧 |
| [WP-09](#wp-09) | [09 · PMU and PMU Firmware](09-pmu-firmware/README.md) | 6 | 1 | [WP-03](#wp-03), [WP-06](#wp-06) | 🚧 |
| [WP-10](#wp-10) | [10 · Trusted Firmware-A (BL31)](10-trusted-firmware-a/README.md) | 4 | 1 | [WP-03](#wp-03), [WP-06](#wp-06) | 🚧 |
| [WP-11](#wp-11) | [11 · U-Boot](11-u-boot/README.md) | 6 | 1 | [WP-06](#wp-06) | 🚧 |
| [WP-12](#wp-12) | [12 · Device Tree](12-device-tree/README.md) | 6 | 1 | [WP-03](#wp-03) | 🚧 |
| [WP-13](#wp-13) | [13 · The Linux Kernel](13-linux-kernel/README.md) | 6 | 1 | [WP-02](#wp-02), [WP-12](#wp-12) | 🚧 |
| [WP-14](#wp-14) | [14 · Kernel Modules and Device Drivers](14-kernel-modules-and-drivers/README.md) | 6 | 1 | [WP-12](#wp-12), [WP-13](#wp-13) | 🚧 |
| [WP-15](#wp-15) | [15 · Root Filesystem and Init](15-root-filesystem-and-init/README.md) | 9 | 1 | [WP-13](#wp-13) | 🚧 |
| [WP-16](#wp-16) | [16 · Application Development](16-application-development/README.md) | 6 | 1 | [WP-04](#wp-04), [WP-05](#wp-05) | 🚧 |
| [WP-17](#wp-17) | [17 · PL Integration, FPGA Manager and DFX](17-pl-integration-and-dfx/README.md) | 6 | 2 | [WP-03](#wp-03), [WP-12](#wp-12), [WP-14](#wp-14) | 🚧 |
| [WP-18](#wp-18) | [18 · XRT and Hardware Acceleration](18-xrt-and-acceleration/README.md) | 4 | 2 | [WP-17](#wp-17) | 🚧 |
| [WP-19](#wp-19) | [19 · Graphics and Display](19-graphics-and-display/README.md) | 3 | 2 | [WP-13](#wp-13), [WP-14](#wp-14) | 🚧 |
| [WP-20](#wp-20) | [20 · Video and Multimedia](20-video-and-multimedia/README.md) | 5 | 2 | [WP-14](#wp-14), [WP-17](#wp-17) | 🚧 |
| [WP-21](#wp-21) | [21 · RPU and OpenAMP](21-rpu-and-openamp/README.md) | 6 | 2 | [WP-03](#wp-03), [WP-12](#wp-12) | 🚧 |
| [WP-22](#wp-22) | [22 · Networking and Peripherals](22-networking-and-peripherals/README.md) | 6 | 2 | [WP-12](#wp-12), [WP-13](#wp-13) | 🚧 |
| [WP-23](#wp-23) | [23 · Storage, Updates and Production](23-storage-updates-and-production/README.md) | 8 | 2 | [WP-07](#wp-07), [WP-15](#wp-15) | 🚧 |
| [WP-24](#wp-24) | [24 · Debugging and Board Bring-Up](24-debugging-and-bring-up/README.md) | 5 | 2 | [WP-06](#wp-06) | 🚧 |
| [WP-25](#wp-25) | [25 · Security Fundamentals and Cryptography](25-security-fundamentals-and-cryptography/README.md) | 4 | 3 | – | 🚧 |
| [WP-26](#wp-26) | [26 · ZynqMP Hardware Security and Secure Boot](26-zynqmp-hardware-security-and-secure-boot/README.md) | 8 | 3 | [WP-06](#wp-06), [WP-07](#wp-07), [WP-25](#wp-25) | 🚧 |
| [WP-27](#wp-27) | [27 · Linux and Network Security](27-linux-and-network-security/README.md) | 5 | 3 | [WP-01](#wp-01), [WP-25](#wp-25) | 🚧 |
| [WP-28](#wp-28) | [Appendices](appendices/README.md) | 4 | 4 | – | 🚧 |

Total: 28 chapters, 180 sections.

## Recommended writing order

Writing in reading order means every chapter can link back to finished material instead of forward to placeholders.

| Step | Work packages | Why |
| ---: | --- | --- |
| 1 | WP-01, WP-02 | Foundations. Quick to write; lets us lock in tone, depth and formatting before the heavy chapters. |
| 2 | WP-03 | Architecture and address map. Almost every later chapter refers to it. |
| 3 | WP-04, WP-05 | Yocto and PetaLinux, dissected on the real 2024.1 project: where every file comes from. |
| 4 | WP-06, WP-07 | Boot sequence and boot images: the backbone of the guide. |
| 5 | WP-08 to WP-11 | FSBL, PMUFW, TF-A, U-Boot deep dives, with the 2024.1 sources cloned and read. |
| 6 | WP-12 to WP-16 | Device tree, kernel, modules and drivers, rootfs, applications. End of Phase 1. |
| 7 | WP-17 to WP-24 | Advanced subsystems (Phase 2), in any order driven by project needs. |
| 8 | WP-25 to WP-27 | Security (Phase 3). |
| 9 | WP-28 | Appendices and the final review. |

## Work package details

<a id="wp-00"></a>

### WP-00 · Repository Scaffolding

**Status:** ✅ Done

**Deliverables**

- [README.md](README.md): scope, reference platform, learning paths, table of contents
- [ROADMAP.md](ROADMAP.md): this file
- [CONTRIBUTING.md](CONTRIBUTING.md): writing rules and the section template
- Skeleton for 28 chapters with 180 outlined sections

**Verified while scaffolding**

- Yocto 4.1.4 "Langdale", Linux 6.6.10, U-Boot v2024.01 and TF-A v2.10 read from the layers of the real `xilinx-zcu106-2024.1` BSP project
- The 2024.1 tags and branches of `embeddedsw`, `linux-xlnx`, `u-boot-xlnx`, `arm-trusted-firmware`, `device-tree-xlnx`, `meta-xilinx`, `meta-xilinx-tools` and `meta-petalinux` confirmed on GitHub with `git ls-remote`

<a id="wp-01"></a>

### WP-01 · Linux Fundamentals

**Chapter:** [01 · Linux Fundamentals](01-linux-fundamentals/README.md) · **Phase:** 1 · **Depends on:** – · **Status:** 👀 In review

What Linux is, the distribution landscape, package managers, the filesystem hierarchy, and the console, SSH and network tools used every day with a target board.

**Deliverables**

- [What Is Linux?](01-linux-fundamentals/01-what-is-linux.md)
- [Linux Distributions and Linux-Based Operating Systems](01-linux-fundamentals/02-linux-distributions.md)
- [Package Management: apt, dpkg, dnf, rpm and opkg](01-linux-fundamentals/03-package-management.md)
- [Filesystem Hierarchy, Processes and Permissions](01-linux-fundamentals/04-filesystem-hierarchy-and-processes.md)
- [Shell and Essential Tools for Embedded Work](01-linux-fundamentals/05-shell-and-essential-tools.md)
- [Serial Console](01-linux-fundamentals/06-serial-console.md)
- [SSH: Secure Shell](01-linux-fundamentals/07-ssh.md)
- [Networking for Development](01-linux-fundamentals/08-networking-for-development.md)

**Primary sources**

- Debian, Ubuntu and Fedora administrator documentation
- OpenSSH manual pages (`ssh`, `sshd`, `ssh_config`, `sshd_config`, `ssh-keygen`)
- Filesystem Hierarchy Standard 3.0
- Bootlin embedded Linux training materials (CC BY-SA)

**Validation**

- Every command is run on the Ubuntu 22.04 host and on a PetaLinux 2024.1 target (board or QEMU)
- SSH examples tested against both Dropbear and OpenSSH images

**Open items** (marked *Not run on the reference setup* in the text)

- USB-UART port identification and `dialout` setup on a physical board ([06 · Serial Console](01-linux-fundamentals/06-serial-console.md))
- Host package installs with `sudo apt install` ([03 · Package Management](01-linux-fundamentals/03-package-management.md))
- `nmcli` static address for a direct cable; NFS server setup and an NFS-root boot ([08 · Networking](01-linux-fundamentals/08-networking-for-development.md))
- VS Code Remote-SSH against the target ([07 · SSH](01-linux-fundamentals/07-ssh.md))

<a id="wp-02"></a>

### WP-02 · Embedded Linux Concepts

**Chapter:** [02 · Embedded Linux Concepts](02-embedded-linux-concepts/README.md) · **Phase:** 1 · **Depends on:** [WP-01](#wp-01) · **Status:** 👀 In review

The building blocks of every embedded Linux system, plus the toolchains, build systems and workflows that produce and deploy them.

**Deliverables**

- [Anatomy of an Embedded Linux System](02-embedded-linux-concepts/01-anatomy-of-an-embedded-linux-system.md)
- [Cross-Compilation and Toolchains](02-embedded-linux-concepts/02-cross-compilation-and-toolchains.md)
- [Build Systems Landscape](02-embedded-linux-concepts/03-build-systems-landscape.md)
- [Development Workflow](02-embedded-linux-concepts/04-development-workflow.md)

**Primary sources**

- Bootlin embedded Linux training materials (CC BY-SA)
- Yocto Project and Buildroot manuals
- GCC and binutils documentation

**Validation**

- Cross-compile and run a hello-world with the PetaLinux 2024.1 SDK and with a distro cross-compiler

**Open items** (marked *Not run on the reference setup* in the text)

- `git lfs track` for hardware files ([04 · Development Workflow](02-embedded-linux-concepts/04-development-workflow.md))

<a id="wp-03"></a>

### WP-03 · Zynq UltraScale+ MPSoC Architecture

**Chapter:** [03 · Zynq UltraScale+ MPSoC Architecture](03-zynqmp-architecture/README.md) · **Phase:** 1 · **Depends on:** – · **Status:** 👀 In review

PS and PL, the processing units, the full address map, on-chip memories, interconnect and coherency, clocks, power, reset, interrupts and exception levels: the hardware knowledge every BSP engineer needs.

**Deliverables**

- [Device Family Overview](03-zynqmp-architecture/01-device-family-overview.md)
- [Processing System (PS) and Programmable Logic (PL)](03-zynqmp-architecture/02-ps-and-pl.md)
- [Processing Units: APU, RPU, PMU, CSU, GPU and VCU](03-zynqmp-architecture/03-processing-units.md)
- [System Address Map](03-zynqmp-architecture/04-memory-map.md)
- [On-Chip Memories: OCM, TCM and Friends](03-zynqmp-architecture/05-on-chip-memories.md)
- [Interconnect, Cache Coherency and the SMMU](03-zynqmp-architecture/06-interconnect-coherency-and-smmu.md)
- [Clocks, Power Domains and Reset](03-zynqmp-architecture/07-clocks-power-and-reset.md)
- [Interrupts and the GIC](03-zynqmp-architecture/08-interrupts-and-gic.md)
- [Peripherals, MIO and EMIO](03-zynqmp-architecture/09-peripherals-mio-emio.md)
- [Exception Levels and TrustZone](03-zynqmp-architecture/10-exception-levels-and-trustzone.md)

**Primary sources**

- UG1085 Zynq UltraScale+ Device Technical Reference Manual
- UG1087 Zynq UltraScale+ Devices Register Reference
- UG1137 Zynq UltraScale+ MPSoC Software Developer Guide
- Device tree sources in `linux-xlnx@xilinx-v2024.1:arch/arm64/boot/dts/xilinx/`

**Validation**

- Every address and register cross-checked against UG1085/UG1087
- Selected registers read live with `devmem` on the target and `mrd` in XSDB
- Address map compared with the XSA and generated device tree of the real 2024.1 BSP

**Review status and open items**

- All ten sections are drafted. Section 10 uses B1–B2 English and cites architecture documentation, the pinned Linux firmware driver and saved reference captures.
- Review sections 01–09 against their sources and the B1–B2 language rule; their existing command transcripts were not rerun in this continuation.
- Check physical register access through XSDB, SMMU translation and reset behavior on hardware (see the notes in sections 04, 06 and 07).
- Validate OP-TEE, HVC guest calls and Secure memory/peripheral isolation on a suitable setup (section 10). Saved QEMU boot logs do not prove hardware isolation.
- Keep WP-03 in review until these checks are complete.

<a id="wp-04"></a>

### WP-04 · The Yocto Project

**Chapter:** [04 · The Yocto Project](04-yocto-project/README.md) · **Phase:** 1 · **Depends on:** [WP-01](#wp-01), [WP-02](#wp-02) · **Status:** 🚧 Planned

OpenEmbedded, BitBake, layers, recipes, tasks, images and packagegroups: the machinery underneath PetaLinux.

**Deliverables**

- [Yocto Project, OpenEmbedded, Poky and BitBake](04-yocto-project/01-yocto-openembedded-bitbake.md)
- [Layers and the Layer Model](04-yocto-project/02-layers.md)
- [Recipes and Metadata Syntax](04-yocto-project/03-recipes-and-metadata-syntax.md)
- [BitBake Tasks and the Build Process](04-yocto-project/04-bitbake-tasks-and-build-process.md)
- [Images, Packagegroups and Features](04-yocto-project/05-images-packagegroups-and-features.md)
- [Machine and Distro Configuration](04-yocto-project/06-machine-and-distro-configuration.md)
- [devtool Workflow](04-yocto-project/07-devtool-workflow.md)
- [SDK and Extensible SDK](04-yocto-project/08-sdk-and-esdk.md)

**Primary sources**

- Yocto Project 4.1 (Langdale) Reference Manual and Development Tasks Manual
- BitBake User Manual
- The layers shipped in a real project: `components/yocto/layers/` of the 2024.1 BSP
- `meta-xilinx`, `meta-xilinx-tools`, `meta-petalinux` at branch `rel-v2024.1`

**Validation**

- Every BitBake/devtool command is run inside the real ZCU106 2024.1 project
- Variable values shown with `bitbake -e` output from that project

<a id="wp-05"></a>

### WP-05 · PetaLinux 2024.1

**Chapter:** [05 · PetaLinux 2024.1](05-petalinux/README.md) · **Phase:** 1 · **Depends on:** [WP-04](#wp-04) · **Status:** 🚧 Planned

PetaLinux tools in depth, dissected on a real 2024.1 project: file hierarchy, commands, configuration, every output file and how to customize the system.

**Deliverables**

- [What Is PetaLinux?](05-petalinux/01-what-is-petalinux.md)
- [Installation and Host Setup](05-petalinux/02-installation-and-host-setup.md)
- [Project Structure: A Real 2024.1 Project Dissected](05-petalinux/03-project-structure.md)
- [Commands and Workflow](05-petalinux/04-commands-and-workflow.md)
- [The Configuration System](05-petalinux/05-configuration-system.md)
- [Output Files in images/linux](05-petalinux/06-images-linux-output-files.md)
- [Customizing Through meta-user](05-petalinux/07-meta-user-customization.md)
- [Adding Applications and Libraries](05-petalinux/08-adding-applications-and-libraries.md)
- [Hardware Updates and XSA Re-Import](05-petalinux/09-hardware-updates.md)
- [BSP Packaging and Reproducible Builds](05-petalinux/10-bsp-packaging-and-reproducible-builds.md)
- [Yocto Without PetaLinux](05-petalinux/11-yocto-without-petalinux.md)

**Primary sources**

- UG1144 PetaLinux Tools Documentation: Reference Guide (2024.1)
- Real BSP projects: `xilinx-zcu104-2024.1`, `xilinx-zcu106-2024.1` (including their `README`)
- `meta-petalinux` and `meta-xilinx-tools` at `rel-v2024.1`

**Validation**

- Create, configure and build a project from the ZCU106 2024.1 BSP and document every step
- Every file in `images/linux` traced back to the recipe that produced it

<a id="wp-06"></a>

### WP-06 · Boot Sequence

**Chapter:** [06 · Boot Sequence](06-boot-sequence/README.md) · **Phase:** 1 · **Depends on:** [WP-03](#wp-03) · **Status:** 🚧 Planned

From power-on reset to the login prompt, step by step, with every processor, exception level, load address and handoff.

**Deliverables**

- [Boot Flow at a Glance](06-boot-sequence/01-boot-overview.md)
- [Boot Modes](06-boot-sequence/02-boot-modes.md)
- [Power-On Reset and the PMU ROM](06-boot-sequence/03-power-on-reset-and-pmu-rom.md)
- [CSU BootROM](06-boot-sequence/04-csu-bootrom.md)
- [Boot Image Format](06-boot-sequence/05-boot-image-format.md)
- [FSBL Stage](06-boot-sequence/06-fsbl-stage.md)
- [PMU Firmware at Boot](06-boot-sequence/07-pmufw-stage.md)
- [TF-A BL31 Stage](06-boot-sequence/08-tfa-bl31-stage.md)
- [U-Boot Stage](06-boot-sequence/09-u-boot-stage.md)
- [Linux Kernel Boot](06-boot-sequence/10-linux-kernel-boot.md)
- [User-Space Startup](06-boot-sequence/11-user-space-startup.md)
- [Boot Memory Map: Who Loads What, Where](06-boot-sequence/12-boot-address-map.md)
- [Multiboot, Fallback and Golden Images](06-boot-sequence/13-multiboot-and-fallback.md)
- [JTAG Boot](06-boot-sequence/14-jtag-boot.md)
- [Boot Troubleshooting](06-boot-sequence/15-boot-troubleshooting.md)

**Primary sources**

- UG1085 chapters on boot and configuration, CSU, PMU and the address map
- UG1137 boot and configuration chapters
- `embeddedsw@xilinx_v2024.1`: `lib/sw_apps/zynqmp_fsbl`, `lib/sw_apps/zynqmp_pmufw`
- `arm-trusted-firmware@xilinx-v2024.1`: `plat/xilinx/zynqmp`
- `u-boot-xlnx@xilinx-v2024.1`: `board/xilinx/zynqmp`, `include/configs/xilinx_zynqmp.h`
- `linux-xlnx@xilinx-v2024.1`: `Documentation/arch/arm64/booting.rst`
- Real `bootgen.bif`, `boot.scr` and boot logs from the 2024.1 BSP

**Validation**

- An annotated, timestamped boot log from a ZCU10x board covering every stage
- Load and entry addresses verified against BIF, linker scripts and U-Boot environment
- Boot mode, reset reason and multiboot registers read on hardware

<a id="wp-07"></a>

### WP-07 · Boot Images, BIF and Bootgen

**Chapter:** [07 · Boot Images, BIF and Bootgen](07-boot-images-and-bootgen/README.md) · **Phase:** 1 · **Depends on:** [WP-06](#wp-06) · **Status:** 🚧 Planned

How BOOT.BIN is described in a BIF, built with Bootgen, inspected, combined with bitstreams and written to flash.

**Deliverables**

- [The BIF File Format](07-boot-images-and-bootgen/01-bif-file-format.md)
- [Bootgen](07-boot-images-and-bootgen/02-bootgen.md)
- [BOOT.BIN Anatomy](07-boot-images-and-bootgen/03-boot-bin-anatomy.md)
- [Bitstreams: .bit and .bin](07-boot-images-and-bootgen/04-bitstreams.md)
- [Generating Boot Images With PetaLinux](07-boot-images-and-bootgen/05-petalinux-package-boot.md)
- [Flash Layouts and Programming](07-boot-images-and-bootgen/06-flash-layouts-and-programming.md)

**Primary sources**

- UG1283 Bootgen User Guide
- `github.com/Xilinx/bootgen` source
- Real `bootgen.bif`, `BOOT.BIN` and `flash_parts.txt` from the 2024.1 BSP

**Validation**

- `bootgen -read` and `-dump` output of the real `BOOT.BIN`, annotated
- Rebuild `BOOT.BIN` manually from a hand-written BIF and boot it

<a id="wp-08"></a>

### WP-08 · First Stage Boot Loader (FSBL)

**Chapter:** [08 · First Stage Boot Loader (FSBL)](08-fsbl/README.md) · **Phase:** 1 · **Depends on:** [WP-06](#wp-06), [WP-07](#wp-07) · **Status:** 🚧 Planned

The ZynqMP FSBL from embeddedsw xilinx_v2024.1: source walkthrough, build flows, hooks, customization and debugging.

**Deliverables**

- [FSBL Overview](08-fsbl/01-fsbl-overview.md)
- [FSBL Source Walkthrough](08-fsbl/02-fsbl-source-walkthrough.md)
- [Building the FSBL](08-fsbl/03-building-the-fsbl.md)
- [Customizing the FSBL](08-fsbl/04-fsbl-customization.md)
- [FSBL Debugging](08-fsbl/05-fsbl-debugging.md)

**Primary sources**

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/`
- UG1137 FSBL chapter
- `meta-xilinx-tools@rel-v2024.1`: `fsbl-firmware` recipes and bbappends

**Validation**

- Build a customized FSBL (hook + debug flags) through PetaLinux and boot it on hardware
- Map every printed FSBL message to the source line that emits it

<a id="wp-09"></a>

### WP-09 · PMU and PMU Firmware

**Chapter:** [09 · PMU and PMU Firmware](09-pmu-firmware/README.md) · **Phase:** 1 · **Depends on:** [WP-03](#wp-03), [WP-06](#wp-06) · **Status:** 🚧 Planned

The platform management unit: power, reset and error management, the EEMI interface, how to send requests to the PMU and how to extend its firmware.

**Deliverables**

- [PMU Overview](09-pmu-firmware/01-pmu-overview.md)
- [PMU Firmware Architecture and Source](09-pmu-firmware/02-pmufw-architecture-and-source.md)
- [EEMI and Platform Management](09-pmu-firmware/03-eemi-and-platform-management.md)
- [Communicating With the PMU](09-pmu-firmware/04-communicating-with-the-pmu.md)
- [Customizing PMU Firmware](09-pmu-firmware/05-pmufw-customization.md)
- [Error Management, Recovery and Watchdogs](09-pmu-firmware/06-error-management-and-watchdogs.md)

**Primary sources**

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/`
- UG1200 Embedded Energy Management Interface (EEMI) API
- UG1137 PMU firmware and power management chapters; UG1085 PMU chapter
- `linux-xlnx@xilinx-v2024.1:drivers/firmware/xilinx/`

**Validation**

- Issue PM calls from Linux (debugfs/sysfs) and from U-Boot, and trace them to PMUFW
- Build PMUFW with a custom module that answers an IPI request, called end to end

<a id="wp-10"></a>

### WP-10 · Trusted Firmware-A (BL31)

**Chapter:** [10 · Trusted Firmware-A (BL31)](10-trusted-firmware-a/README.md) · **Phase:** 1 · **Depends on:** [WP-03](#wp-03), [WP-06](#wp-06) · **Status:** 🚧 Planned

TF-A (formerly ATF) on ZynqMP: the EL3 runtime that provides PSCI, forwards platform management calls and hosts secure services.

**Deliverables**

- [TF-A Overview](10-trusted-firmware-a/01-tfa-overview.md)
- [BL31 on ZynqMP](10-trusted-firmware-a/02-bl31-on-zynqmp.md)
- [Building and Customizing TF-A](10-trusted-firmware-a/03-tfa-customization.md)
- [BL32 and OP-TEE (Overview)](10-trusted-firmware-a/04-op-tee-overview.md)

**Primary sources**

- `arm-trusted-firmware@xilinx-v2024.1` (`xlnx_rebase_v2.10`): `plat/xilinx/zynqmp`, `plat/xilinx/common`
- TF-A documentation (trustedfirmware.org): porting guide, SMC Calling Convention, PSCI
- `meta-xilinx@rel-v2024.1`: `arm-trusted-firmware` recipes

**Validation**

- Rebuild TF-A with `DEBUG=1` and a changed console through PetaLinux; boot and compare logs
- Add and call a custom SiP SMC from Linux

<a id="wp-11"></a>

### WP-11 · U-Boot

**Chapter:** [11 · U-Boot](11-u-boot/README.md) · **Phase:** 1 · **Depends on:** [WP-06](#wp-06) · **Status:** 🚧 Planned

U-Boot on ZynqMP: essential commands, environment, boot.scr and uEnv.txt, FIT images, exactly how it loads and starts Linux, and how to customize it.

**Deliverables**

- [U-Boot Overview](11-u-boot/01-u-boot-overview.md)
- [Essential U-Boot Commands](11-u-boot/02-essential-commands.md)
- [Environment, boot.scr and uEnv.txt](11-u-boot/03-environment-and-boot-scripts.md)
- [FIT Images and image.ub](11-u-boot/04-fit-images.md)
- [How U-Boot Boots the Linux Kernel](11-u-boot/05-how-u-boot-boots-linux.md)
- [Customizing U-Boot](11-u-boot/06-u-boot-customization.md)

**Primary sources**

- `u-boot-xlnx@xilinx-v2024.1` (v2024.01): `board/xilinx/`, `configs/xilinx_zynqmp_virt_defconfig`, `include/configs/xilinx_zynqmp.h`
- U-Boot documentation (docs.u-boot.org): standard boot, FIT, commands
- `meta-xilinx@rel-v2024.1`: `u-boot-xlnx` and `u-boot-xlnx-scr` recipes
- Real `boot.scr`, `platform-top.h` and `bsp.cfg` from the 2024.1 BSP

**Validation**

- Every command in the command reference executed on a ZCU10x board
- TFTP boot, custom `boot.scr` and a hand-built FIT image booted on hardware

<a id="wp-12"></a>

### WP-12 · Device Tree

**Chapter:** [12 · Device Tree](12-device-tree/README.md) · **Phase:** 1 · **Depends on:** [WP-03](#wp-03) · **Status:** 🚧 Planned

Describing hardware to software: DTS syntax, bindings, the Xilinx Device Tree Generator, System Device Tree, overlays (DTBO) and debugging.

**Deliverables**

- [Device Tree Fundamentals](12-device-tree/01-device-tree-fundamentals.md)
- [Bindings and Driver Matching](12-device-tree/02-bindings-and-driver-matching.md)
- [Xilinx Device Tree Generator (DTG)](12-device-tree/03-xilinx-device-tree-generator.md)
- [System Device Tree and Lopper](12-device-tree/04-system-device-tree-and-lopper.md)
- [Device Tree Overlays (DTBO)](12-device-tree/05-device-tree-overlays.md)
- [Device Tree Debugging](12-device-tree/06-device-tree-debugging.md)

**Primary sources**

- Devicetree Specification (devicetree.org)
- `linux-xlnx@xilinx-v2024.1:Documentation/devicetree/`
- `device-tree-xlnx@xilinx_v2024.1`; lopper (`github.com/devicetree-org/lopper`)
- Generated device tree of the real 2024.1 BSP (`components/plnx_workspace/device-tree`)

**Validation**

- Trace a PL IP from the XSA to the generated `pl.dtsi` and to the bound driver
- Apply and remove an overlay at runtime on hardware

<a id="wp-13"></a>

### WP-13 · The Linux Kernel

**Chapter:** [13 · The Linux Kernel](13-linux-kernel/README.md) · **Phase:** 1 · **Depends on:** [WP-02](#wp-02), [WP-12](#wp-12) · **Status:** 🚧 Planned

Kernel fundamentals, linux-xlnx, kernel image formats (Image, Image.gz, image.ub), configuration, building, debugging and real-time Linux.

**Deliverables**

- [Kernel Fundamentals](13-linux-kernel/01-kernel-fundamentals.md)
- [linux-xlnx and Kernel Versions](13-linux-kernel/02-linux-xlnx-and-kernel-versions.md)
- [Kernel Image Formats](13-linux-kernel/03-kernel-image-formats.md)
- [Configuring and Building the Kernel](13-linux-kernel/04-configuring-and-building.md)
- [Kernel Debugging](13-linux-kernel/05-kernel-debugging.md)
- [Real-Time Linux](13-linux-kernel/06-real-time-linux.md)

**Primary sources**

- `linux-xlnx@xilinx-v2024.1` (6.6.10, `xlnx_rebase_v6.6_LTS`) and its `Documentation/`
- `meta-xilinx@rel-v2024.1`: `linux-xlnx` recipes
- kernel.org documentation: admin guide, kbuild, dev-tools, trace

**Validation**

- Build the kernel with a config fragment in PetaLinux and outside Yocto with the SDK
- Decode a deliberately triggered oops with `vmlinux`

<a id="wp-14"></a>

### WP-14 · Kernel Modules and Device Drivers

**Chapter:** [14 · Kernel Modules and Device Drivers](14-kernel-modules-and-drivers/README.md) · **Phase:** 1 · **Depends on:** [WP-12](#wp-12), [WP-13](#wp-13) · **Status:** 🚧 Planned

Built-in (static) vs. loadable (dynamic) modules, in-tree vs. out-of-tree, kernel headers, adding modules to PetaLinux, the driver model, user-space hardware access and DMA.

**Deliverables**

- [Kernel Modules](14-kernel-modules-and-drivers/01-kernel-modules.md)
- [Kernel Headers and Building Modules](14-kernel-modules-and-drivers/02-kernel-headers-and-module-builds.md)
- [Adding Modules to a PetaLinux Project](14-kernel-modules-and-drivers/03-modules-in-petalinux.md)
- [The Linux Device Driver Model](14-kernel-modules-and-drivers/04-linux-device-driver-model.md)
- [Accessing Hardware From User Space](14-kernel-modules-and-drivers/05-user-space-hardware-access.md)
- [DMA, CMA and Memory Management](14-kernel-modules-and-drivers/06-dma-and-memory-management.md)

**Primary sources**

- `linux-xlnx@xilinx-v2024.1:Documentation/` (kbuild, driver-api, core-api/dma-api)
- `meta-petalinux@rel-v2024.1` module templates; Yocto `module.bbclass`
- Bootlin kernel driver development materials

**Validation**

- Out-of-tree module built by PetaLinux, autoloaded at boot
- Platform driver and UIO variant for a custom AXI-Lite IP, tested on hardware

<a id="wp-15"></a>

### WP-15 · Root Filesystem and Init

**Chapter:** [15 · Root Filesystem and Init](15-root-filesystem-and-init/README.md) · **Phase:** 1 · **Depends on:** [WP-13](#wp-13) · **Status:** 🚧 Planned

What a root filesystem is, initrd vs. initramfs, filesystem types (ext4, UBIFS, JFFS2, ...), rootfs configuration and packagegroups, init systems and BusyBox.

**Deliverables**

- [Root Filesystem Fundamentals](15-root-filesystem-and-init/01-rootfs-fundamentals.md)
- [initrd vs. initramfs](15-root-filesystem-and-init/02-initrd-and-initramfs.md)
- [Filesystem Types for Embedded Systems](15-root-filesystem-and-init/03-filesystem-types.md)
- [Root Filesystem Boot Options in PetaLinux](15-root-filesystem-and-init/04-rootfs-boot-options.md)
- [Rootfs Configuration and Packagegroups](15-root-filesystem-and-init/05-rootfs-configuration-and-packagegroups.md)
- [Init Systems: SysVinit, systemd and BusyBox init](15-root-filesystem-and-init/06-init-systems.md)
- [BusyBox](15-root-filesystem-and-init/07-busybox.md)
- [Device Management: devtmpfs, udev and mdev](15-root-filesystem-and-init/08-device-management-and-udev.md)
- [Users, Passwords and Login](15-root-filesystem-and-init/09-users-and-login.md)

**Primary sources**

- `linux-xlnx@xilinx-v2024.1:Documentation/filesystems/` (ramfs-rootfs-initramfs, ubifs) and `Documentation/admin-guide/initrd.rst`
- linux-mtd documentation for UBI/UBIFS and JFFS2
- systemd and BusyBox documentation; Yocto init manager documentation
- `meta-petalinux@rel-v2024.1`: image recipes and packagegroups

**Validation**

- Boot the same build with INITRD, INITRAMFS, EXT4 (SD) and NFS root
- Packagegroup catalogue generated from the 2024.1 layers, not from memory

<a id="wp-16"></a>

### WP-16 · Application Development

**Chapter:** [16 · Application Development](16-application-development/README.md) · **Phase:** 1 · **Depends on:** [WP-04](#wp-04), [WP-05](#wp-05) · **Status:** 🚧 Planned

Cross-compiling, debugging and profiling applications, and integrating them into the system as proper services.

**Deliverables**

- [Cross-Compiling Applications](16-application-development/01-cross-compiling-applications.md)
- [Debugging Applications](16-application-development/02-debugging-applications.md)
- [Profiling and Performance](16-application-development/03-profiling-and-performance.md)
- [System Services and Logging](16-application-development/04-system-services-and-logging.md)
- [Python and High-Level Frameworks](16-application-development/05-python-and-high-level-frameworks.md)
- [Containers on ZynqMP](16-application-development/06-containers.md)

**Primary sources**

- Yocto Project Application Development and the Extensible SDK manual
- GDB, perf and systemd documentation
- UG1400 Vitis Embedded Software Development (remote debugging)

**Validation**

- Remote debug session with gdbserver from the host and from VS Code
- Application installed as a systemd service by a PetaLinux recipe

<a id="wp-17"></a>

### WP-17 · PL Integration, FPGA Manager and DFX

**Chapter:** [17 · PL Integration, FPGA Manager and DFX](17-pl-integration-and-dfx/README.md) · **Phase:** 2 · **Depends on:** [WP-03](#wp-03), [WP-12](#wp-12), [WP-14](#wp-14) · **Status:** 🚧 Planned

Using the programmable logic from Linux: hardware handoff, PL peripherals, the FPGA manager, Dynamic Function eXchange (partial reconfiguration), dfx-mgr and PS-PL DMA.

**Deliverables**

- [Hardware Handoff: From Vivado to Linux](17-pl-integration-and-dfx/01-hardware-handoff.md)
- [Accessing PL Peripherals From Linux](17-pl-integration-and-dfx/02-accessing-pl-peripherals.md)
- [Linux FPGA Manager](17-pl-integration-and-dfx/03-fpga-manager.md)
- [DFX: Dynamic Function eXchange](17-pl-integration-and-dfx/04-dfx-dynamic-function-exchange.md)
- [dfx-mgr and Accelerator Packages](17-pl-integration-and-dfx/05-dfx-mgr.md)
- [DMA Between PS and PL](17-pl-integration-and-dfx/06-dma-between-ps-and-pl.md)

**Primary sources**

- UG909 Vivado Design Suite User Guide: Dynamic Function eXchange
- UG1144 FPGA manager chapter
- `linux-xlnx@xilinx-v2024.1:drivers/fpga/` and `Documentation/driver-api/fpga/`
- `github.com/Xilinx/dfx-mgr` at the 2024.1 release
- Firmware recipes (`recipes-firmware/`) in the real ZCU106 2024.1 BSP

**Validation**

- Load a full bitstream plus overlay at runtime and bind its drivers
- Swap reconfigurable modules with dfx-mgr on hardware

<a id="wp-18"></a>

### WP-18 · XRT and Hardware Acceleration

**Chapter:** [18 · XRT and Hardware Acceleration](18-xrt-and-acceleration/README.md) · **Phase:** 2 · **Depends on:** [WP-17](#wp-17) · **Status:** 🚧 Planned

The Xilinx Runtime on embedded platforms: zocl, xclbin, Vitis acceleration platforms and AI inference with the DPU.

**Deliverables**

- [XRT Overview](18-xrt-and-acceleration/01-xrt-overview.md)
- [Embedded Platforms for Acceleration](18-xrt-and-acceleration/02-embedded-platforms-for-acceleration.md)
- [Running Accelerated Applications](18-xrt-and-acceleration/03-running-accelerated-applications.md)
- [Vitis AI and the DPU (Overview)](18-xrt-and-acceleration/04-vitis-ai-and-dpu.md)

**Primary sources**

- XRT documentation (`xilinx.github.io/XRT`) and `github.com/Xilinx/XRT` at 2024.1
- UG1393 Vitis Unified Software Platform: Application Acceleration Development
- Vitis AI documentation

**Validation**

- Build an embedded platform with XRT/zocl and run a vector-add kernel on hardware

<a id="wp-19"></a>

### WP-19 · Graphics and Display

**Chapter:** [19 · Graphics and Display](19-graphics-and-display/README.md) · **Phase:** 2 · **Depends on:** [WP-13](#wp-13), [WP-14](#wp-14) · **Status:** 🚧 Planned

The DisplayPort subsystem, DRM/KMS and the Arm Mali-400 MP2 GPU, from kernel drivers to Wayland and Qt.

**Deliverables**

- [Display Subsystem and DRM/KMS](19-graphics-and-display/01-display-subsystem-and-drm-kms.md)
- [Arm Mali-400 MP2 GPU](19-graphics-and-display/02-mali-gpu.md)
- [Windowing Systems and UI Frameworks](19-graphics-and-display/03-windowing-systems-and-ui-frameworks.md)

**Primary sources**

- UG1085 DisplayPort and GPU chapters
- `linux-xlnx@xilinx-v2024.1:drivers/gpu/drm/xlnx/` and the DRM documentation
- `meta-xilinx@rel-v2024.1`: `libmali-xlnx` and `kernel-module-mali` recipes

**Validation**

- `modetest`, `kmscube` and `es2gears`/`glmark2` on the ZCU106 DisplayPort output

<a id="wp-20"></a>

### WP-20 · Video and Multimedia

**Chapter:** [20 · Video and Multimedia](20-video-and-multimedia/README.md) · **Phase:** 2 · **Depends on:** [WP-14](#wp-14), [WP-17](#wp-17) · **Status:** 🚧 Planned

V4L2, the media controller, media-ctl and v4l2-ctl, GStreamer and the VCU: building camera and video pipelines.

**Deliverables**

- [V4L2 Fundamentals](20-video-and-multimedia/01-v4l2-fundamentals.md)
- [Media Controller and Tools: media-ctl, v4l2-ctl, yavta](20-video-and-multimedia/02-media-controller-and-tools.md)
- [GStreamer](20-video-and-multimedia/03-gstreamer.md)
- [VCU: Video Codec Unit](20-video-and-multimedia/04-vcu-video-codec-unit.md)
- [Audio (Overview)](20-video-and-multimedia/05-audio.md)

**Primary sources**

- `linux-xlnx@xilinx-v2024.1:Documentation/userspace-api/media/` and `drivers/media/platform/xilinx/`
- GStreamer documentation
- PG252 H.264/H.265 Video Codec Unit product guide

**Validation**

- Capture, display, encode and stream pipelines run on a ZCU104/ZCU106 (both have a VCU)

<a id="wp-21"></a>

### WP-21 · RPU and OpenAMP

**Chapter:** [21 · RPU and OpenAMP](21-rpu-and-openamp/README.md) · **Phase:** 2 · **Depends on:** [WP-03](#wp-03), [WP-12](#wp-12) · **Status:** 🚧 Planned

Asymmetric multiprocessing with the Cortex-R5F cluster: firmware on the RPU, remoteproc, RPMsg, libmetal, IPI and shared memory.

**Deliverables**

- [AMP vs. SMP Concepts](21-rpu-and-openamp/01-amp-concepts.md)
- [Programming the RPU](21-rpu-and-openamp/02-rpu-programming.md)
- [remoteproc and RPMsg](21-rpu-and-openamp/03-remoteproc-and-rpmsg.md)
- [OpenAMP in PetaLinux](21-rpu-and-openamp/04-openamp-in-petalinux.md)
- [IPI and Shared Memory Patterns](21-rpu-and-openamp/05-ipi-and-shared-memory.md)
- [Xen Hypervisor (Overview)](21-rpu-and-openamp/06-xen-hypervisor.md)

**Primary sources**

- UG1186 Libmetal and OpenAMP User Guide
- `meta-openamp` as shipped with PetaLinux 2024.1
- `linux-xlnx@xilinx-v2024.1`: `drivers/remoteproc/xlnx_r5_remoteproc.c`, `Documentation/staging/remoteproc.rst`

**Validation**

- Run the OpenAMP echo test with firmware loaded from Linux via remoteproc

<a id="wp-22"></a>

### WP-22 · Networking and Peripherals

**Chapter:** [22 · Networking and Peripherals](22-networking-and-peripherals/README.md) · **Phase:** 2 · **Depends on:** [WP-12](#wp-12), [WP-13](#wp-13) · **Status:** 🚧 Planned

Ethernet, network configuration, USB, PCIe, low-speed buses and time synchronization: device tree, drivers and user-space tools.

**Deliverables**

- [Ethernet (GEM)](22-networking-and-peripherals/01-ethernet.md)
- [Network Configuration on the Target](22-networking-and-peripherals/02-network-configuration.md)
- [USB Host and Gadget](22-networking-and-peripherals/03-usb.md)
- [PCIe](22-networking-and-peripherals/04-pcie.md)
- [I2C, SPI, UART, CAN and GPIO](22-networking-and-peripherals/05-low-speed-buses.md)
- [Time Synchronization: PTP and TSN](22-networking-and-peripherals/06-time-sync-ptp-tsn.md)

**Primary sources**

- UG1085 peripheral chapters
- `linux-xlnx@xilinx-v2024.1` driver documentation and DT bindings (macb, dwc3, pcie, cadence, i2c, spi)
- linuxptp documentation; `meta-xilinx-tsn` as shipped with PetaLinux 2024.1

**Validation**

- Ethernet, USB gadget and low-speed bus examples run on hardware

<a id="wp-23"></a>

### WP-23 · Storage, Updates and Production

**Chapter:** [23 · Storage, Updates and Production](23-storage-updates-and-production/README.md) · **Phase:** 2 · **Depends on:** [WP-07](#wp-07), [WP-15](#wp-15) · **Status:** 🚧 Planned

Flash management (MTD, UBI/UBIFS, SD/eMMC), software update strategies, boot-time optimization, reliability, licensing and CI.

**Deliverables**

- [MTD and Flash Memory](23-storage-updates-and-production/01-mtd-and-flash.md)
- [UBI and UBIFS in Practice](23-storage-updates-and-production/02-ubi-and-ubifs.md)
- [SD and eMMC](23-storage-updates-and-production/03-sd-and-emmc.md)
- [Software Update Strategies](23-storage-updates-and-production/04-software-update-strategies.md)
- [Boot-Time Optimization](23-storage-updates-and-production/05-boot-time-optimization.md)
- [Reliability and Field Diagnostics](23-storage-updates-and-production/06-reliability-and-field-diagnostics.md)
- [Licensing and Compliance](23-storage-updates-and-production/07-licensing-and-compliance.md)
- [CI and Reproducible Builds](23-storage-updates-and-production/08-ci-and-reproducible-builds.md)

**Primary sources**

- linux-mtd documentation (MTD, UBI, UBIFS)
- RAUC, SWUpdate and Mender documentation
- Yocto Project licensing, SPDX and CVE-check documentation

**Validation**

- UBIFS rootfs on flash, and an A/B update cycle demonstrated on hardware

<a id="wp-24"></a>

### WP-24 · Debugging and Board Bring-Up

**Chapter:** [24 · Debugging and Board Bring-Up](24-debugging-and-bring-up/README.md) · **Phase:** 2 · **Depends on:** [WP-06](#wp-06) · **Status:** 🚧 Planned

JTAG, XSDB/XSCT, QEMU, DDR bring-up and a systematic approach to bringing up a custom board.

**Deliverables**

- [JTAG, XSDB and XSCT](24-debugging-and-bring-up/01-jtag-xsdb-and-xsct.md)
- [QEMU Emulation](24-debugging-and-bring-up/02-qemu-emulation.md)
- [Custom Board Bring-Up](24-debugging-and-bring-up/03-custom-board-bring-up.md)
- [DDR Bring-Up and Memory Testing](24-debugging-and-bring-up/04-ddr-bring-up.md)
- [Common Failures and Fixes](24-debugging-and-bring-up/05-common-failures.md)

**Primary sources**

- UG1400 Vitis Embedded Software Development (XSDB/XSCT)
- UG1169 Xilinx Quick Emulator (QEMU) User Guide
- UG1228 Zynq UltraScale+ MPSoC Embedded Design Methodology Guide

**Validation**

- XSDB scripts tested on hardware; QEMU boot of the 2024.1 BSP

<a id="wp-25"></a>

### WP-25 · Security Fundamentals and Cryptography

**Chapter:** [25 · Security Fundamentals and Cryptography](25-security-fundamentals-and-cryptography/README.md) · **Phase:** 3 · **Depends on:** – · **Status:** 🚧 Planned

Security principles, threat modeling and the cryptography needed to design secure embedded products. No prior security experience is assumed.

**Deliverables**

- [Security Principles and Threat Modeling](25-security-fundamentals-and-cryptography/01-security-principles-and-threat-modeling.md)
- [Cryptography Primer](25-security-fundamentals-and-cryptography/02-cryptography-primer.md)
- [PKI and Certificates](25-security-fundamentals-and-cryptography/03-pki-and-certificates.md)
- [Key Management](25-security-fundamentals-and-cryptography/04-key-management.md)

**Primary sources**

- NIST SP 800-57 (key management), FIPS 197 (AES), FIPS 180-4 / FIPS 202 (SHA-2/SHA-3), FIPS 186-5 (signatures)
- OpenSSL documentation
- OWASP and Microsoft STRIDE threat modeling material

**Validation**

- Every cryptographic operation demonstrated with OpenSSL commands on the host and target

<a id="wp-26"></a>

### WP-26 · ZynqMP Hardware Security and Secure Boot

**Chapter:** [26 · ZynqMP Hardware Security and Secure Boot](26-zynqmp-hardware-security-and-secure-boot/README.md) · **Phase:** 3 · **Depends on:** [WP-06](#wp-06), [WP-07](#wp-07), [WP-25](#wp-25) · **Status:** 🚧 Planned

The root of trust, boot image authentication and encryption, eFUSE/BBRAM, and an end-to-end chain of trust from the BootROM to the root filesystem.

**Deliverables**

- [Hardware Security Features](26-zynqmp-hardware-security-and-secure-boot/01-hardware-security-features.md)
- [Chain of Trust](26-zynqmp-hardware-security-and-secure-boot/02-chain-of-trust.md)
- [Boot Image Authentication (RSA)](26-zynqmp-hardware-security-and-secure-boot/03-authentication.md)
- [Boot Image Encryption (AES-GCM)](26-zynqmp-hardware-security-and-secure-boot/04-encryption.md)
- [eFUSE and BBRAM Programming](26-zynqmp-hardware-security-and-secure-boot/05-efuse-and-bbram-programming.md)
- [Secure Boot With PetaLinux](26-zynqmp-hardware-security-and-secure-boot/06-secure-boot-in-petalinux.md)
- [Verified Boot Beyond U-Boot](26-zynqmp-hardware-security-and-secure-boot/07-verified-boot-beyond-u-boot.md)
- [TrustZone and OP-TEE](26-zynqmp-hardware-security-and-secure-boot/08-trustzone-and-op-tee.md)

**Primary sources**

- UG1085 security chapter; UG1283 Bootgen security sections; UG1137 security chapter
- XAPP1319 Programming BBRAM and eFUSEs
- `embeddedsw@xilinx_v2024.1:lib/sw_services/xilskey`, `xilsecure`
- U-Boot FIT signature, kernel module signing, dm-verity and IMA documentation; OP-TEE documentation

**Validation**

- Authenticated (and optionally encrypted) boot demonstrated with boot-header authentication or BBRAM keys, never by burning eFUSEs on shared boards

<a id="wp-27"></a>

### WP-27 · Linux and Network Security

**Chapter:** [27 · Linux and Network Security](27-linux-and-network-security/README.md) · **Phase:** 3 · **Depends on:** [WP-01](#wp-01), [WP-25](#wp-25) · **Status:** 🚧 Planned

Hardening the operating system and its network exposure: SSH in depth, firewalls, TLS, VPNs, secure updates and vulnerability management.

**Deliverables**

- [Linux System Hardening](27-linux-and-network-security/01-linux-hardening.md)
- [SSH in Depth and Hardening](27-linux-and-network-security/02-ssh-in-depth-and-hardening.md)
- [Network Security](27-linux-and-network-security/03-network-security.md)
- [Secure Software Updates](27-linux-and-network-security/04-secure-updates.md)
- [Vulnerability Management](27-linux-and-network-security/05-vulnerability-management.md)

**Primary sources**

- OpenSSH documentation and Mozilla OpenSSH guidelines
- nftables, OpenSSL, WireGuard documentation
- `meta-security` as shipped with PetaLinux 2024.1; Yocto `cve-check` documentation
- Kernel Self Protection Project recommended settings

**Validation**

- Hardened image audited with `ss`, `nmap` and `ssh-audit` before and after

<a id="wp-28"></a>

### WP-28 · Appendices and Final Review

**Chapter:** [Appendices](appendices/README.md) · **Phase:** 4 · **Depends on:** – · **Status:** 🚧 Planned

Glossary, command cheat sheets, a register quick reference and the full list of references, plus a final consistency pass over the whole guide.

**Deliverables**

- [Glossary](appendices/01-glossary.md)
- [Command Cheat Sheets](appendices/02-command-cheatsheets.md)
- [Register Quick Reference](appendices/03-register-quick-reference.md)
- [References and Sources](appendices/04-references.md)

**Primary sources**

- All chapters

**Validation**

- Every link resolves; every register value cross-checked with UG1087; glossary covers every acronym used

## Findings to carry forward

Facts discovered while writing finished work packages that belong in later chapters. Each one was observed on the reference setup.

| Finding | Evidence | Use in |
| --- | --- | --- |
| In the ZCU106 2024.1 BSP, TF-A prints to UART1; PMUFW, FSBL, U-Boot and Linux use UART0 | `CONFIG_SUBSYSTEM_TF-A_SERIAL_PSU_UART_1_SELECT=y`; UART1 log shows only `NOTICE: BL31` lines | [WP-06](#wp-06), [WP-10](#wp-10) |
| BL31 reports `Secure code at 0x60000000`, `Non secure code at 0x8000000` | UART1 log | [WP-06](#wp-06), [WP-10](#wp-10) |
| `petalinux-boot qemu --prebuilt 3` loads DTB at `0x100000`, `Image` at `0x200000`, ramdisk at `0x4000000`, `boot.scr` at `0x20000000` | QEMU command line printed by `petalinux-boot` | [WP-06](#wp-06), [WP-11](#wp-11), [WP-24](#wp-24) |
| `petalinux-boot qemu` attaches `rootfs.ext4` as SD card and resizes it to a power of two in place | `boot_qemu.py` (`MakePowerof2`), `Image resized.` message | [WP-24](#wp-24) |
| The prebuilt BSP image boots a 5.4 MB `petalinux-initramfs-image`, which switches to `rootfs.ext4` on `/dev/mmcblk0` | boot log, `/proc/cmdline` (`root=/dev/ram0`), `mount` | [WP-15](#wp-15) |
| Sending `system_reset` on the A53 QEMU monitor hangs the multi-arch (A53 + PMU) QEMU; a guest `reboot` works | QEMU at 300 % CPU, no console output | [WP-24](#wp-24) |
| UART1 is `ttyPS2` because alias `serial1` is `/dcc` | decompiled `system.dtb`, `dmesg` | [WP-12](#wp-12), [WP-22](#wp-22) |
| BusyBox `inetd` serves telnet (23) and FTP (21); `/bin/busybox` is setuid root; the package feed is HTTP with `gpgcheck=0` and unsigned RPMs | `netstat -tln`, `find -perm -4000`, `/etc/yum.repos.d/`, `rpm -qi` | [WP-27](#wp-27) |
| `/var/log` and `/var/tmp` are on tmpfs (`/var/volatile`); the journal is lost at reboot | `ls -l /var`, `mount` | [WP-15](#wp-15), [WP-23](#wp-23) |
| `KillUserProcesses=yes` (compiled-in default): processes started from SSH sessions die at logout | `logind.conf`, test with `nohup` and `systemd-run` | [WP-15](#wp-15), [WP-16](#wp-16) |
| Switching networkd from a static file back to DHCP with `networkctl reconfigure` left no default route; restarting `systemd-networkd` fixed it | `ip route` before and after | [WP-22](#wp-22) |
| Machine-specific feed repositories (`zcu106_zynqmp`, `xilinx_zcu106`) return 404; `petalinux.xilinx.com` redirects to `edf.amd.com` | `dnf install` output | [WP-05](#wp-05) |
| The project's `components/yocto/environment-setup-*` points to `components/yocto/tmp/sysroots/...`, which does not exist in the BSP as shipped | `ls components/yocto` | [WP-04](#wp-04), [WP-16](#wp-16) |
| The project's `project-spec/configs` were changed after the prebuilt images were made (e.g. `dnf` is in the image but not selected in `rootfs_config`); do not infer the prebuilt image's configuration from the project files | `rootfs.manifest` vs. `rootfs_config` | [WP-05](#wp-05) |
| Buildroot 2025.02.x ZynqMP configurations boot through U-Boot SPL instead of the FSBL | `configs/zynqmp_zcu106_defconfig` | [WP-08](#wp-08) |

## Coverage map

### Topics from the original request

Each topic from the original request, and where the guide covers it.

| Topic | Covered in |
| --- | --- |
| What SSH is and how to use it | [01 · SSH: Secure Shell](01-linux-fundamentals/07-ssh.md)<br>[27 · SSH in Depth and Hardening](27-linux-and-network-security/02-ssh-in-depth-and-hardening.md) |
| File hierarchy of a PetaLinux project | [05 · Project Structure: A Real 2024.1 Project Dissected](05-petalinux/03-project-structure.md) |
| What Yocto is; what PetaLinux is | [04 · Yocto Project, OpenEmbedded, Poky and BitBake](04-yocto-project/01-yocto-openembedded-bitbake.md)<br>[05 · What Is PetaLinux?](05-petalinux/01-what-is-petalinux.md) |
| What a device tree is; what DTG is | [12 · Device Tree Fundamentals](12-device-tree/01-device-tree-fundamentals.md)<br>[12 · Xilinx Device Tree Generator (DTG)](12-device-tree/03-xilinx-device-tree-generator.md) |
| What Bootgen is | [07 · Bootgen](07-boot-images-and-bootgen/02-bootgen.md) |
| What the kernel is | [13 · Kernel Fundamentals](13-linux-kernel/01-kernel-fundamentals.md) |
| Files generated in `images/linux` | [05 · Output Files in images/linux](05-petalinux/06-images-linux-output-files.md) |
| The boot sequence, from addresses to every step | [06 · Boot Sequence](06-boot-sequence/README.md) |
| BIF file; what BOOT.BIN is and contains | [07 · The BIF File Format](07-boot-images-and-bootgen/01-bif-file-format.md)<br>[07 · BOOT.BIN Anatomy](07-boot-images-and-bootgen/03-boot-bin-anatomy.md)<br>[06 · Boot Image Format](06-boot-sequence/05-boot-image-format.md) |
| U-Boot and FSBL: what they do | [08 · FSBL Overview](08-fsbl/01-fsbl-overview.md)<br>[11 · U-Boot Overview](11-u-boot/01-u-boot-overview.md)<br>[06 · FSBL Stage](06-boot-sequence/06-fsbl-stage.md)<br>[06 · U-Boot Stage](06-boot-sequence/09-u-boot-stage.md) |
| Basic U-Boot commands; customizing U-Boot | [11 · Essential U-Boot Commands](11-u-boot/02-essential-commands.md)<br>[11 · Customizing U-Boot](11-u-boot/06-u-boot-customization.md) |
| What can be added to the FSBL; FSBL customization | [08 · Customizing the FSBL](08-fsbl/04-fsbl-customization.md) |
| PMU: what it is, how to send it requests, how to customize it | [09 · PMU Overview](09-pmu-firmware/01-pmu-overview.md)<br>[09 · Communicating With the PMU](09-pmu-firmware/04-communicating-with-the-pmu.md)<br>[09 · Customizing PMU Firmware](09-pmu-firmware/05-pmufw-customization.md) |
| `Image`, `image.ub`, `Image.gz` | [13 · Kernel Image Formats](13-linux-kernel/03-kernel-image-formats.md)<br>[11 · FIT Images and image.ub](11-u-boot/04-fit-images.md) |
| rootfs, initrd, initramfs | [15 · Root Filesystem Fundamentals](15-root-filesystem-and-init/01-rootfs-fundamentals.md)<br>[15 · initrd vs. initramfs](15-root-filesystem-and-init/02-initrd-and-initramfs.md) |
| UBIFS, JFFS2 | [15 · Filesystem Types for Embedded Systems](15-root-filesystem-and-init/03-filesystem-types.md)<br>[23 · UBI and UBIFS in Practice](23-storage-updates-and-production/02-ubi-and-ubifs.md) |
| `boot.scr` and `uEnv.txt` | [11 · Environment, boot.scr and uEnv.txt](11-u-boot/03-environment-and-boot-scripts.md) |
| Bitstream (`.bit`) files | [07 · Bitstreams: .bit and .bin](07-boot-images-and-bootgen/04-bitstreams.md) |
| BootROM | [06 · CSU BootROM](06-boot-sequence/04-csu-bootrom.md) |
| TF-A / ATF BL31 | [10 · BL31 on ZynqMP](10-trusted-firmware-a/02-bl31-on-zynqmp.md)<br>[06 · TF-A BL31 Stage](06-boot-sequence/08-tfa-bl31-stage.md) |
| Init systems; BusyBox | [15 · Init Systems: SysVinit, systemd and BusyBox init](15-root-filesystem-and-init/06-init-systems.md)<br>[15 · BusyBox](15-root-filesystem-and-init/07-busybox.md) |
| Recipes; Yocto layer structure | [04 · Recipes and Metadata Syntax](04-yocto-project/03-recipes-and-metadata-syntax.md)<br>[04 · Layers and the Layer Model](04-yocto-project/02-layers.md) |
| How the kernel is built | [13 · Configuring and Building the Kernel](13-linux-kernel/04-configuring-and-building.md) |
| Adding a kernel module to a PetaLinux project | [14 · Adding Modules to a PetaLinux Project](14-kernel-modules-and-drivers/03-modules-in-petalinux.md) |
| Adding an application to a PetaLinux project | [05 · Adding Applications and Libraries](05-petalinux/08-adding-applications-and-libraries.md) |
| BitBake build process | [04 · BitBake Tasks and the Build Process](04-yocto-project/04-bitbake-tasks-and-build-process.md) |
| OpenEmbedded and BitBake | [04 · Yocto Project, OpenEmbedded, Poky and BitBake](04-yocto-project/01-yocto-openembedded-bitbake.md) |
| dnf, apt; Debian, Ubuntu | [01 · Package Management: apt, dpkg, dnf, rpm and opkg](01-linux-fundamentals/03-package-management.md)<br>[01 · Linux Distributions and Linux-Based Operating Systems](01-linux-fundamentals/02-linux-distributions.md) |
| Linux in general; Linux-based operating systems and their uses | [01 · What Is Linux?](01-linux-fundamentals/01-what-is-linux.md)<br>[01 · Linux Distributions and Linux-Based Operating Systems](01-linux-fundamentals/02-linux-distributions.md) |
| Boot modes | [06 · Boot Modes](06-boot-sequence/02-boot-modes.md) |
| Rootfs settings | [15 · Rootfs Configuration and Packagegroups](15-root-filesystem-and-init/05-rootfs-configuration-and-packagegroups.md)<br>[15 · Root Filesystem Boot Options in PetaLinux](15-root-filesystem-and-init/04-rootfs-boot-options.md) |
| Packagegroups: what they install and why | [04 · Images, Packagegroups and Features](04-yocto-project/05-images-packagegroups-and-features.md)<br>[15 · Rootfs Configuration and Packagegroups](15-root-filesystem-and-init/05-rootfs-configuration-and-packagegroups.md) |
| Module types: in-tree, out-of-tree, static (built-in), dynamic (loadable) | [14 · Kernel Modules](14-kernel-modules-and-drivers/01-kernel-modules.md) |
| `lsmod`, `rmmod` | [14 · Kernel Modules](14-kernel-modules-and-drivers/01-kernel-modules.md) |
| Kernel headers | [14 · Kernel Headers and Building Modules](14-kernel-modules-and-drivers/02-kernel-headers-and-module-builds.md) |
| How U-Boot loads the kernel | [11 · How U-Boot Boots the Linux Kernel](11-u-boot/05-how-u-boot-boots-linux.md) |
| OCM, TCM and other on-chip memories | [03 · On-Chip Memories: OCM, TCM and Friends](03-zynqmp-architecture/05-on-chip-memories.md) |
| Using the Arm Mali GPU | [19 · Arm Mali-400 MP2 GPU](19-graphics-and-display/02-mali-gpu.md) |
| PS and PL | [03 · Processing System (PS) and Programmable Logic (PL)](03-zynqmp-architecture/02-ps-and-pl.md) |
| DFX | [17 · DFX: Dynamic Function eXchange](17-pl-integration-and-dfx/04-dfx-dynamic-function-exchange.md)<br>[17 · dfx-mgr and Accelerator Packages](17-pl-integration-and-dfx/05-dfx-mgr.md) |
| DTBO | [12 · Device Tree Overlays (DTBO)](12-device-tree/05-device-tree-overlays.md) |
| XRT | [18 · XRT and Hardware Acceleration](18-xrt-and-acceleration/README.md) |
| GStreamer | [20 · GStreamer](20-video-and-multimedia/03-gstreamer.md) |
| V4L2, media-ctl and related tools | [20 · V4L2 Fundamentals](20-video-and-multimedia/01-v4l2-fundamentals.md)<br>[20 · Media Controller and Tools: media-ctl, v4l2-ctl, yavta](20-video-and-multimedia/02-media-controller-and-tools.md) |
| Security, cryptography, network security, SSH (later phase) | [25 · Security Fundamentals and Cryptography](25-security-fundamentals-and-cryptography/README.md)<br>[26 · ZynqMP Hardware Security and Secure Boot](26-zynqmp-hardware-security-and-secure-boot/README.md)<br>[27 · Linux and Network Security](27-linux-and-network-security/README.md) |

### Topics added for an advanced embedded Linux engineer

These were not in the original request, but an advanced engineer working on ZynqMP is expected to know them.

| Topic | Covered in |
| --- | --- |
| Cross-compilation, toolchains and sysroots | [02 · Cross-Compilation and Toolchains](02-embedded-linux-concepts/02-cross-compilation-and-toolchains.md) |
| System address map and key register blocks | [03 · System Address Map](03-zynqmp-architecture/04-memory-map.md) |
| Interconnect, cache coherency, SMMU, XMPU/XPPU | [03 · Interconnect, Cache Coherency and the SMMU](03-zynqmp-architecture/06-interconnect-coherency-and-smmu.md) |
| Clocks, power domains and reset | [03 · Clocks, Power Domains and Reset](03-zynqmp-architecture/07-clocks-power-and-reset.md) |
| GIC and interrupt numbering | [03 · Interrupts and the GIC](03-zynqmp-architecture/08-interrupts-and-gic.md) |
| MIO/EMIO and PS peripherals | [03 · Peripherals, MIO and EMIO](03-zynqmp-architecture/09-peripherals-mio-emio.md) |
| Exception levels and TrustZone | [03 · Exception Levels and TrustZone](03-zynqmp-architecture/10-exception-levels-and-trustzone.md) |
| Boot image format at byte level | [06 · Boot Image Format](06-boot-sequence/05-boot-image-format.md) |
| Multiboot, fallback and golden images | [06 · Multiboot, Fallback and Golden Images](06-boot-sequence/13-multiboot-and-fallback.md) |
| JTAG boot and boot troubleshooting | [06 · JTAG Boot](06-boot-sequence/14-jtag-boot.md)<br>[06 · Boot Troubleshooting](06-boot-sequence/15-boot-troubleshooting.md) |
| Flash layouts and programming | [07 · Flash Layouts and Programming](07-boot-images-and-bootgen/06-flash-layouts-and-programming.md) |
| FIT images | [11 · FIT Images and image.ub](11-u-boot/04-fit-images.md) |
| System Device Tree and Lopper | [12 · System Device Tree and Lopper](12-device-tree/04-system-device-tree-and-lopper.md) |
| devtool, SDK and eSDK | [04 · devtool Workflow](04-yocto-project/07-devtool-workflow.md)<br>[04 · SDK and Extensible SDK](04-yocto-project/08-sdk-and-esdk.md) |
| Linux device driver model, UIO, DMA/CMA | [14 · The Linux Device Driver Model](14-kernel-modules-and-drivers/04-linux-device-driver-model.md)<br>[14 · Accessing Hardware From User Space](14-kernel-modules-and-drivers/05-user-space-hardware-access.md)<br>[14 · DMA, CMA and Memory Management](14-kernel-modules-and-drivers/06-dma-and-memory-management.md) |
| Kernel debugging and real-time Linux | [13 · Kernel Debugging](13-linux-kernel/05-kernel-debugging.md)<br>[13 · Real-Time Linux](13-linux-kernel/06-real-time-linux.md) |
| udev, users and login policy | [15 · Device Management: devtmpfs, udev and mdev](15-root-filesystem-and-init/08-device-management-and-udev.md)<br>[15 · Users, Passwords and Login](15-root-filesystem-and-init/09-users-and-login.md) |
| Application debugging, profiling, services, containers | [16 · Application Development](16-application-development/README.md) |
| FPGA manager and PS-PL DMA | [17 · Linux FPGA Manager](17-pl-integration-and-dfx/03-fpga-manager.md)<br>[17 · DMA Between PS and PL](17-pl-integration-and-dfx/06-dma-between-ps-and-pl.md) |
| DisplayPort, DRM/KMS, Wayland and Qt | [19 · Display Subsystem and DRM/KMS](19-graphics-and-display/01-display-subsystem-and-drm-kms.md)<br>[19 · Windowing Systems and UI Frameworks](19-graphics-and-display/03-windowing-systems-and-ui-frameworks.md) |
| VCU (hardware video codec) | [20 · VCU: Video Codec Unit](20-video-and-multimedia/04-vcu-video-codec-unit.md) |
| RPU, OpenAMP, remoteproc, RPMsg, Xen | [21 · RPU and OpenAMP](21-rpu-and-openamp/README.md) |
| Ethernet, USB, PCIe, PTP/TSN | [22 · Networking and Peripherals](22-networking-and-peripherals/README.md) |
| MTD/UBI, software updates, boot-time optimization, licensing, CI | [23 · Storage, Updates and Production](23-storage-updates-and-production/README.md) |
| JTAG/XSDB, QEMU, custom board and DDR bring-up | [24 · Debugging and Board Bring-Up](24-debugging-and-bring-up/README.md) |
