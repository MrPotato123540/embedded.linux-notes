# Build Systems Landscape

> **Applies to:** PetaLinux 2024.1 · Yocto 4.1 · Zynq UltraScale+ MPSoC

**[02 · Embedded Linux Concepts](README.md)** · Part I: Foundations

## In short

- An embedded Linux build system turns source code into the pillars from [section 01](01-anatomy-of-an-embedded-linux-system.md): boot loader, kernel, device tree and root filesystem, built with a matching toolchain.
- The main options are building by hand, **Buildroot**, the **Yocto Project / OpenEmbedded**, and **Debian-based** image builders. PetaLinux and AMD's EDF are AMD's distributions built with Yocto.
- For ZynqMP, Yocto with AMD's `meta-xilinx` layers (directly, or through PetaLinux or EDF) is the path AMD supports. Buildroot has community configurations for ZCU10x and Kria boards that boot differently, with U-Boot SPL instead of the FSBL.
- Choose by product lifetime, update model, team skills and how much of AMD's tooling you want to keep.

## Concepts

### What every build system must do

1. Build or provide a **cross toolchain** and a sysroot.
2. Fetch, patch, configure and compile the **boot chain**, the **kernel** and the **device tree** for one specific board.
3. Build hundreds of **user-space packages** in dependency order, against the sysroot.
4. Assemble the **root filesystem** with users, configuration and services, and produce **images** in the right formats (ext4, cpio, UBI, WIC, `BOOT.BIN`).
5. Ideally: produce an SDK, license manifests and source archives, and do it **reproducibly**.

### The options

**By hand.** Cross-compile BusyBox, the kernel and U-Boot yourself and assemble a root filesystem with shell scripts. Instructive, and fine for a first experiment, but nobody can maintain it for a product: you would be writing your own build system.

**Buildroot.** A Makefile- and Kconfig-based system that produces a root filesystem image and a toolchain from one `make menuconfig` configuration.

- Simple to learn; a full build is relatively fast.
- No package manager on the target: the image is the unit of deployment.
- Releases every three months (`YYYY.02`, `.05`, `.08`, `.11`). At the time of writing, the long-term support series is 2025.02.x, maintained until March 2028.
- ZynqMP: Buildroot 2025.02.x ships `zynqmp_zcu102_defconfig`, `zynqmp_zcu104_defconfig`, `zynqmp_zcu106_defconfig` and `zynqmp_kria_kv260_defconfig`. They use AMD's `linux-xlnx` and `u-boot-xlnx` trees, TF-A for the `zynqmp` platform, and PMU firmware built from `embeddedsw`. They boot through **U-Boot SPL** (`BR2_TARGET_UBOOT_SPL=y`) instead of the FSBL, which is a different boot chain from the one this guide describes.

**Yocto Project / OpenEmbedded.** A framework for building your own distribution from **layers** of metadata ([chapter 04](../04-yocto-project/README.md)).

- Very flexible: anything from a 5 MB initramfs to a full desktop. Package feeds, SDKs, multiple machines and multiple configurations from one tree.
- Strong compliance tooling: license manifests, source archives, SPDX SBOMs, CVE checks.
- Steep learning curve, long first builds (hours) and large disk usage (tens to hundreds of GB), mitigated by the shared-state cache.
- Releases every six months, in April and October. Every second April release is a long-term support (LTS) release maintained for four years: Scarthgap 5.0 (April 2024, until April 2028) and Wrynose 6.0 (April 2026, until April 2030). Other releases are maintained for roughly six months only. Langdale 4.1, used by PetaLinux 2024.1, was such a non-LTS release (October 2022) and is end-of-life.
- ZynqMP: AMD maintains `meta-xilinx`, `meta-xilinx-tools` and related layers. These build the complete AMD boot chain: FSBL, PMU firmware, TF-A, U-Boot, device tree, bitstream and `BOOT.BIN`.

**PetaLinux.** AMD's command-line tools and distribution on top of Yocto ([chapter 05](../05-petalinux/README.md)). It imports the hardware description (XSA) from Vivado, generates the Yocto machine configuration, and wraps BitBake behind `petalinux-*` commands. Everything underneath is Yocto, which is why this guide teaches both.

**AMD EDF (Embedded Development Framework).** AMD's Yocto-based successor to PetaLinux, introduced with the 2025.1 tools. AMD has announced that PetaLinux is on a retirement path. EDF builds the same components with standard Yocto workflows, driven by the System Device Tree ([chapter 12](../12-device-tree/04-system-device-tree-and-lopper.md)).

**Debian-based builders.** Instead of compiling user space, they install prebuilt Debian or Ubuntu packages for arm64 into a root filesystem: `debootstrap` (by hand), or integrated tools such as ISAR (developed by ilbers with Siemens; uses BitBake to drive Debian packaging) and debos. You still have to provide AMD's boot chain, kernel and device tree. On Kria SOMs, Canonical's Ubuntu images take this approach with an AMD-provided boot chain.

### Comparison

| | By hand | Buildroot | Yocto / PetaLinux / EDF | Debian-based |
| --- | --- | --- | --- | --- |
| Learning curve | Low to start, endless later | Low | High | Medium |
| First build time | Short | Short to medium | Long (hours) | Short (packages are prebuilt) |
| Image size range | Any | Small to medium | Any | Medium to large |
| Package manager on target | No | No | Optional (rpm/deb/ipk) | Yes (apt) |
| AMD boot chain for ZynqMP | You | Community (SPL-based) | AMD-supported | You (or Canonical on Kria) |
| SDK for application developers | No | Toolchain only | Full SDK and eSDK | Native or cross toolchains from the distribution |
| License compliance tooling | No | Yes (legal-info) | Yes (manifests, archiver, SPDX) | Source packages from Debian |
| Reproducibility | Poor | Good | Very good | Depends on archive snapshots |
| Who fixes security issues | You | You, with Buildroot's LTS | You, with Yocto LTS and vendor layers | Debian/Ubuntu security teams for user space |

## On ZynqMP

### A decision guide

Ask the questions in order; the first clear answer usually decides.

1. **Do you need AMD support for the boot chain, the PL tooling and the device tree generation?** Use the Yocto-based AMD flow: PetaLinux up to its final releases, EDF for new work.
2. **Is it a Kria SOM, and do you want apt and a desktop-like environment?** Canonical's Ubuntu for Kria is the quickest start. Plan how you will update and secure it in the field.
3. **Is the product small, single-purpose, with a small team and no need for package feeds?** Buildroot is a serious option. Accept that its ZynqMP boot chain differs from AMD's (SPL instead of FSBL) and that AMD tools such as bootgen-based secure boot need extra integration.
4. **Must you maintain the product for many years, with SBOMs and CVE tracking?** Yocto on an LTS release, with your own distribution layer. PetaLinux 2024.1 sits on a non-LTS Yocto release, so a long-lived product should plan a migration to an LTS-based release.

> [!TIP]
> Whatever you choose, keep the hardware-specific parts (device tree changes, kernel configuration, U-Boot environment, bitstreams) in version control and documented. They are what you will need to carry over when you change build systems.

## Pitfalls

- **Choosing by the first-day experience.** Ubuntu boots in an afternoon; maintaining a secure, updatable product for ten years is where the real cost is.
- **Treating PetaLinux as something other than Yocto.** Every PetaLinux problem beyond the basics is a Yocto problem. Learn [chapter 04](../04-yocto-project/README.md).
- **Mixing boot chains.** A Buildroot SPL-based boot and an AMD FSBL-based `BOOT.BIN` are not interchangeable. Pick one per product.

## References

- Buildroot: [download page](https://buildroot.org/download.html) (release series and LTS end-of-life), `buildroot@2025.02.x:configs/zynqmp_*_defconfig`
- Yocto Project: [releases](https://www.yoctoproject.org/development/releases/)
- AMD: [PetaLinux tools page](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html) (EDF and PetaLinux retirement)
- ISAR: [github.com/ilbers/isar](https://github.com/ilbers/isar); debos: [github.com/go-debos/debos](https://github.com/go-debos/debos)

---

<sub>← [Cross-Compilation and Toolchains](02-cross-compilation-and-toolchains.md) · [Chapter index](README.md) · [Development Workflow](04-development-workflow.md) →</sub>
