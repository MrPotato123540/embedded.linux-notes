# Linux Distributions and Linux-Based Operating Systems

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · any Linux host

**[01 · Linux Fundamentals](README.md)** · Part I: Foundations

## In short

- A distribution decides **which versions** of the kernel and user-space software you get, **how** they are built and configured, and **for how long** you get fixes.
- Desktop and server distributions (Debian, Ubuntu, Fedora, RHEL) ship **prebuilt binary packages**. Embedded systems are usually **built from source** for one specific board, with tools such as Yocto or Buildroot.
- On ZynqMP you can run AMD's Yocto-based distributions (PetaLinux, and its successor EDF), your own Yocto distribution, or Ubuntu (certified on Kria SOMs). The choice drives your update model, footprint and support lifetime.

## Concepts

### What a distribution decides for you

| Decision | Example (host: Ubuntu 22.04) | Example (target: PetaLinux 2024.1) |
| --- | --- | --- |
| Kernel | Ubuntu kernel 6.8 (HWE) | `linux-xlnx` 6.6.10 |
| C library | glibc 2.35 | glibc 2.36 |
| Init system | systemd | systemd 251 |
| Package format and tool | `.deb`, apt | `.rpm`, dnf |
| Who builds it | Canonical, prebuilt for all amd64/arm64 machines | AMD prebuilt BSP, or **you**, with Yocto, for one board |
| Update source | `archive.ubuntu.com` | AMD feed `petalinux.xilinx.com`, or your own feed |

Both systems identify themselves in `/etc/os-release`:

```console
$ grep -E '^(NAME|VERSION|ID)=' /etc/os-release
NAME="Ubuntu"
VERSION="22.04.5 LTS (Jammy Jellyfish)"
ID=ubuntu
target$ grep -E '^(NAME|VERSION|ID)=' /etc/os-release
ID=petalinux
NAME="PetaLinux"
VERSION="2024.1+release-S05201002 (langdale)"
```

### Distribution families

Most distributions descend from a few families and share their package formats and tools:

| Family | Members | Package format / tool | Release model | Typical use |
| --- | --- | --- | --- | --- |
| Debian | Debian, Ubuntu, Raspberry Pi OS, Linux Mint | `.deb` / apt | Debian: stable release about every 2 years; Ubuntu: every 6 months, LTS every 2 years | Servers, desktops, development hosts, increasingly embedded |
| Red Hat | Fedora, RHEL, CentOS Stream, AlmaLinux, Rocky Linux | `.rpm` / dnf | Fedora: about every 6 months; RHEL: about 10 years of support per major version | Enterprise servers |
| SUSE | openSUSE Leap and Tumbleweed, SLES | `.rpm` / zypper | Fixed releases and rolling | Enterprise servers |
| Arch | Arch Linux, Manjaro | `.pkg.tar.zst` / pacman | Rolling (no versions) | Desktops for enthusiasts |
| Alpine | Alpine Linux | `.apk` / apk | Every 6 months | Containers: musl libc and BusyBox make it tiny |

### Embedded-oriented systems

| System | What it is | Typical use |
| --- | --- | --- |
| **Yocto Project / OpenEmbedded** | A framework for **building your own** distribution from source ([chapter 04](../04-yocto-project/README.md)). Poky is its reference distribution | Industrial and commercial products; the base of PetaLinux, AMD EDF and Automotive Grade Linux |
| **PetaLinux** | AMD's Yocto-based distribution and tool wrapper for its SoCs ([chapter 05](../05-petalinux/README.md)) | ZynqMP, Versal, Zynq-7000 and MicroBlaze designs |
| **Buildroot** | A simpler, Makefile-based build system that produces a root filesystem image, without a package manager on the target | Small, single-purpose devices |
| **OpenWrt** | A distribution for routers and network devices | Networking equipment |
| **Android** | Linux kernel plus Google's own user space (Bionic libc, ART runtime) | Phones, tablets, infotainment |

### Debian and Ubuntu

**Debian** is a community project. It publishes a stable release about every two years and supports each one for about five years in total (regular security support, then Debian LTS). It is known for conservative, well-tested packages and strict license policies.

**Ubuntu** is Canonical's distribution, built from Debian packages. It releases every April and October. The April release of even years is a **long-term support (LTS)** release with five years of standard support, which a Ubuntu Pro subscription extends. The reference host runs Ubuntu 22.04 LTS. Canonical also publishes Ubuntu images certified for AMD's **Kria** SOMs, which lets Kria users install packages with apt instead of rebuilding an image.

### Binary distributions vs. source-built distributions

| | Binary distribution (Debian, Ubuntu) | Source-built distribution (Yocto, Buildroot) |
| --- | --- | --- |
| Getting started | Fast: flash an image, `apt install` | Slower: first build takes hours, needs a capable host |
| Footprint | Hundreds of MB to several GB | From a few MB upwards; you include only what you need |
| Hardware support | Generic kernel; vendor drivers and the device tree need extra work | Built for one machine, with the vendor kernel and device tree |
| Reproducibility | Depends on the state of the mirror on install day | Every version is pinned in metadata; the same inputs give the same image |
| Updates | Per-package from the distribution archive | You build and publish updates (package feeds or whole images) |
| License compliance | Source packages are available from the distribution | Yocto generates manifests and source archives for you |
| Security fixes | The distribution's security team | Your team, possibly helped by the vendor |

## On ZynqMP

The Cortex-A53 cores implement Armv8-A, so any **arm64 (aarch64)** distribution can run in user space. The hard parts are the **boot chain** (FSBL, PMU firmware, TF-A, U-Boot), the **kernel** (AMD drivers for PS and PL IP) and the **device tree**, which a generic distribution does not provide. The options in practice:

| Option | Boot chain and kernel | User space | Support |
| --- | --- | --- | --- |
| PetaLinux 2024.1 | AMD, built by PetaLinux | Yocto Langdale packages | AMD, for the 2024.1 release |
| AMD EDF (2025.1 and later) | AMD, built with Yocto | Yocto packages | AMD; it succeeds PetaLinux |
| Your own Yocto distribution with `meta-xilinx` | AMD layers, your configuration | Your choice of Yocto packages | Your team, with AMD's layers |
| Ubuntu for Kria | Canonical, with AMD kernel | Ubuntu arm64 archive | Canonical and AMD, Kria SOMs only |
| Debian or Ubuntu root filesystem on a custom board | You assemble AMD's boot chain and kernel | Debian/Ubuntu arm64 archive | Your team |

> [!NOTE]
> **Release difference:** AMD states that its Yocto-based **Embedded Development Framework (EDF)**, introduced with the 2025.1 tools, supersedes PetaLinux, and that PetaLinux is on a retirement path. Everything in this guide that is about Yocto, the boot chain and the kernel applies to EDF as well. See the [PetaLinux product page](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html) for AMD's current schedule.

### Choosing for a product

Ask these questions, in this order:

1. **How long must the product be maintained?** Ten years of field life needs a plan for security fixes long after the distribution release is out of support. PetaLinux 2024.1 is built on Yocto 4.1 "Langdale", a non-LTS release that is already end-of-life upstream. Whoever ships it owns its maintenance.
2. **How are updates delivered?** Per-package updates (apt, dnf) suit lab and development systems. Fielded devices usually get whole, signed, atomic image updates ([chapter 23](../23-storage-updates-and-production/04-software-update-strategies.md)).
3. **How small and how fast must it be?** A source-built image can boot in a few seconds from a few tens of MB. A general-purpose distribution cannot.
4. **What does your team already know?** Ubuntu on Kria is the shortest way to a working prototype. Yocto has a steeper learning curve but gives full control.

## Pitfalls

- **Mixing packages from different distributions.** A `.deb` built for Ubuntu 22.04 expects Ubuntu's library versions. Installing it on another system, or copying binaries between distributions, leads to missing libraries and symbol-version errors.
- **Assuming "arm64 support" means "ZynqMP support".** A generic arm64 distribution has no FSBL, no PMU firmware, no device tree for your board and no drivers for your PL IP.
- **Treating the prebuilt BSP as a product.** AMD prints this when the reference target boots: "The PetaLinux source code and images provided/generated are for demonstration purposes only."

## References

- Debian release information: [debian.org/releases](https://www.debian.org/releases/)
- Ubuntu release cycle: [ubuntu.com/about/release-cycle](https://ubuntu.com/about/release-cycle)
- Yocto Project releases: [yoctoproject.org/development/releases](https://www.yoctoproject.org/development/releases/) (Langdale 4.1: October 2022, end-of-life)
- AMD, [PetaLinux tools page](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html) (EDF and PetaLinux retirement)
- Captured on the reference setup: `/etc/os-release` on host and target, boot banner of the ZCU106 2024.1 prebuilt image

---

<sub>← [What Is Linux?](01-what-is-linux.md) · [Chapter index](README.md) · [Package Management: apt, dpkg, dnf, rpm and opkg](03-package-management.md) →</sub>
