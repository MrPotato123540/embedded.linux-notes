# Package Management: apt, dpkg, dnf, rpm and opkg

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · Ubuntu/Debian hosts

**[01 · Linux Fundamentals](README.md)** · Part I: Foundations

## In short

- A **package** is an archive of files plus metadata: name, version, architecture, dependencies, license and install scripts.
- Each family has two layers of tools. A **low-level** tool installs one package file and keeps the database (`dpkg`, `rpm`). A **high-level** tool resolves dependencies and downloads from repositories (`apt`, `dnf`).
- Your Ubuntu host uses `.deb` with dpkg and apt. PetaLinux 2024.1 builds `.rpm` packages (`PACKAGE_CLASSES = "package_rpm"`), and the reference image ships rpm and dnf on the target.
- Installing packages on a target at runtime is great in the lab. Production devices are usually updated with whole images instead ([chapter 23](../23-storage-updates-and-production/04-software-update-strategies.md)).

## Concepts

### What is inside a package

| Part | Example (`openssh-sshd` on the target) |
| --- | --- |
| Files | `/usr/sbin/sshd`, configuration under `/etc/ssh/` |
| Name, version, release | `openssh-sshd`, `9.0p1`, `r0.0` |
| Architecture | `cortexa72_cortexa53` (built for this CPU tuning), `noarch` (scripts, data) |
| Dependencies | Libraries and other packages that must be installed first |
| Scripts | Run before or after install and removal (`%post` in RPM, `postinst` in Debian) |
| License | `BSD-2-Clause & BSD-3-Clause & ISC & MIT` |

The package manager records every installed file in a database, so it can answer "which package owns this file?", remove packages cleanly and detect conflicts.

### Two layers of tools

| Task | Low level (one file, no network) | High level (repositories, dependencies) |
| --- | --- | --- |
| Debian family | `dpkg` | `apt` (and the older `apt-get`, `apt-cache`) |
| Red Hat family | `rpm` | `dnf` (formerly `yum`) |
| Embedded, ipk | `opkg` does both | `opkg` |

Use the high-level tool for anything that touches a repository. Use the low-level tool to query the database or to install a single local file.

## Debian and Ubuntu: dpkg and apt

The host of the reference setup is Ubuntu 22.04. Repositories are configured in `/etc/apt/sources.list` and `/etc/apt/sources.list.d/`.

Which package owns a file, and what does that package contain?

```console
$ dpkg -S /usr/bin/rsync
rsync: /usr/bin/rsync
$ dpkg -L rsync | grep bin/
/usr/bin/rrsync
/usr/bin/rsync
/usr/bin/rsync-ssl
```

Which version is installed, which one is available, and where does it come from?

```console
$ apt-cache policy rsync
rsync:
  Installed: 3.2.7-0ubuntu0.22.04.7
  Candidate: 3.2.7-0ubuntu0.22.04.7
  Version table:
 *** 3.2.7-0ubuntu0.22.04.7 500
        500 http://tr.archive.ubuntu.com/ubuntu jammy-updates/main amd64 Packages
        500 http://security.ubuntu.com/ubuntu jammy-security/main amd64 Packages
        100 /var/lib/dpkg/status
     3.2.3-8ubuntu3 500
        500 http://tr.archive.ubuntu.com/ubuntu jammy/main amd64 Packages
```

The version table shows the original 22.04 release version (`jammy`) and the newer one from the updates and security pockets (`jammy-updates`, `jammy-security`). The installed version (`***`) came from an update. The numbers (`500`, `100`) are pin priorities. apt installs the highest version among the sources with the highest priority.

What does it depend on?

```console
$ apt-cache depends rsync
rsync
  PreDepends: init-system-helpers
  Depends: lsb-base
  Depends: libacl1
  Depends: libc6
  Depends: liblz4-1
  Depends: libpopt0
  Depends: libssl3
  Depends: libxxhash0
  Depends: libzstd1
  Depends: zlib1g
  Suggests: openssh-client
```

Everyday commands:

```bash
sudo apt update                 # refresh the package lists from all repositories
sudo apt upgrade                # install available updates
sudo apt install picocom        # install a package and its dependencies
sudo apt remove picocom         # remove it (configuration files stay)
apt search serial terminal      # search names and descriptions
sudo dpkg -i ./some-package.deb # install a local file (dependencies are not resolved)
sudo apt install ./some-package.deb  # install a local file and resolve dependencies
```

> [!NOTE]
> **Not run on the reference setup:** the `sudo` commands above change the host and were not executed while writing this section. The query commands were.

## Red Hat family and PetaLinux: rpm and dnf

### On the target

The reference target has 962 RPM packages installed. Querying works like on any RPM-based system:

```console
target$ rpm -qa | wc -l
962
target$ rpm -qf /usr/sbin/sshd /bin/busybox /bin/mount.util-linux
openssh-sshd-9.0p1-r0.0.cortexa72_cortexa53
busybox-1.35.0-r0.0.cortexa72_cortexa53
util-linux-mount-2.38.1-r0.0.cortexa72_cortexa53
target$ rpm -qi openssh-sshd | head -14
Name        : openssh-sshd
Version     : 9.0p1
Release     : r0.0
Architecture: cortexa72_cortexa53
Install Date: Tue Apr  5 23:14:36 2011
Group       : console/network
Size        : 1765691
License     : BSD-2-Clause & BSD-3-Clause & ISC & MIT
Signature   : (none)
Source RPM  : openssh-9.0p1-r0.0.src.rpm
Build Date  : Thu Apr  7 04:51:46 2022
Build Host  : reproducible
Packager    : AMD AECG <meta-xilinx@yoctoproject.org>
URL         : http://www.openssh.com/
```

Three details in this output come from Yocto rather than from Red Hat conventions:

- **Architecture `cortexa72_cortexa53`.** Yocto names package architectures after the CPU tuning they were compiled for. Packages that work on any Armv8-A CPU use `armv8a` or `aarch64`, and machine-specific ones use the machine name ([chapter 04](../04-yocto-project/06-machine-and-distro-configuration.md)).
- **Dates in 2011 and 2022, build host `reproducible`.** These are fixed values for reproducible builds, not real dates.
- **`Signature: (none)`.** The packages are not signed. Keep this in mind for the next part.

### Repositories: the PetaLinux package feed

dnf reads its repositories from `/etc/yum.repos.d/`. The reference image points at AMD's public feed:

```console
target# ls /etc/yum.repos.d/; cat /etc/yum.repos.d/* | head -10
oe-remote-repo-sswreleases-rel-v2024-generic-rpm.repo
[oe-remote-repo-sswreleases-rel-v2024-generic-rpm-all]
name=OE Remote Repo: sswreleases rel-v2024 generic rpm all
baseurl=http://petalinux.xilinx.com/sswreleases/rel-v2024/generic/rpm/all
gpgcheck=0

[oe-remote-repo-sswreleases-rel-v2024-generic-rpm-any]
name=OE Remote Repo: sswreleases rel-v2024 generic rpm any
baseurl=http://petalinux.xilinx.com/sswreleases/rel-v2024/generic/rpm/any
gpgcheck=0
...
```

This file is generated at build time from two Yocto variables. `meta-petalinux` sets their defaults in `conf/distro/include/petalinux-feed.conf`:

```text
PACKAGE_FEED_URIS ?= "http://petalinux.xilinx.com/sswreleases/rel-v${@d.getVar('XILINX_VER_MAIN').split('.')[0]}/generic/rpm"
PACKAGE_FEED_ARCHS ?= "${@d.getVar('PACKAGE_ARCHS').replace('-','_')}"
```

Yocto creates one repository section per package architecture (`all`, `any`, `noarch`, `aarch64`, `armv8a`, ..., `cortexa72_cortexa53`, the machine names). In a PetaLinux project you override the URIs and architectures with the `package-feed-uris` and `package-feed-archs` options of `petalinux-config -c rootfs`.

Install a package from the feed:

```console
target# dnf -y install libgpiod-tools
...
Errors during downloading metadata for repository 'oe-remote-repo-sswreleases-rel-v2024-generic-rpm-zcu106_zynqmp':
  - Status code: 404 for https://edf.amd.com/sswreleases/rel-v2024/generic/rpm/zcu106_zynqmp/repodata/repomd.xml (IP: 104.96.161.7)
...
Ignoring repositories: oe-remote-repo-sswreleases-rel-v2024-generic-rpm-zcu106_zynqmp, oe-remote-repo-sswreleases-rel-v2024-generic-rpm-xilinx_zcu106
Last metadata expiration check: 0:00:39 ago on Thu Oct 15 12:06:15 2026.
Dependencies resolved.
=============================================================================================================================
 Package          Architecture         Version    Repository                                                             Size
=============================================================================================================================
Installing:
 libgpiod-tools   cortexa72_cortexa53  1.6.3-r0.4 oe-remote-repo-sswreleases-rel-v2024-generic-rpm-cortexa72_cortexa53   23 k
Installing dependencies:
 libgpiod2        cortexa72_cortexa53  1.6.3-r0.4 oe-remote-repo-sswreleases-rel-v2024-generic-rpm-cortexa72_cortexa53   20 k

Transaction Summary
=============================================================================================================================
Install  2 Packages

Total download size: 43 k
Installed size: 462 k
...
target# gpiodetect
gpiochip0 [firmware:zynqmp-firmware:gpio] (4 lines)
gpiochip1 [zynqmp_gpio] (174 lines)
gpiochip2 [0-0020] (16 lines)
gpiochip3 [0-0021] (16 lines)
```

What happened here:

- `petalinux.xilinx.com` now redirects to `edf.amd.com`.
- The two machine-specific repositories (`zcu106_zynqmp`, `xilinx_zcu106`) do not exist on the server. dnf reports a 404 and ignores them, because only packages built for a specific board would be there. Generic packages still install.
- The first install on a fresh system also downloads the metadata of every repository. On the reference target, `dnf -y install i2c-tools rsync` took 1 min 40 s, almost all of it spent on metadata.

Some packages install a tool under a name that another package could also provide. They use **update-alternatives**, which you see in the install scripts:

```text
+ update-alternatives --install /usr/sbin/i2cdetect i2cdetect /usr/sbin/i2cdetect.i2c-tools 100
update-alternatives: Linking /usr/sbin/i2cdetect to /usr/sbin/i2cdetect.i2c-tools
```

```console
target# rpm -q --whatprovides /usr/sbin/i2cdetect
i2c-tools-4.3-r0.2.cortexa72_cortexa53
```

> [!WARNING]
> The default feed uses plain HTTP and `gpgcheck=0`, and the packages are unsigned (`Signature: (none)` above). Anyone who can tamper with the network path can make the target install arbitrary code as root. That is acceptable on a lab network. A product needs signed packages or signed images, served over TLS. [Chapter 27](../27-linux-and-network-security/04-secure-updates.md) covers how.

## opkg and ipk

`opkg` is a lightweight package manager from the OpenWrt world. It handles `.ipk` files, which are simple archives similar to `.deb`. It installs, removes and resolves dependencies in one small tool, which suits devices with little flash and RAM.

## How Yocto chooses the format

Yocto can produce `.rpm`, `.deb` or `.ipk` packages, selected with `PACKAGE_CLASSES`. The first class listed also decides the format used to assemble the root filesystem. PetaLinux sets it in the generated `build/conf/plnxtool.conf`:

```text
PACKAGE_CLASSES = "package_rpm"
```

The package manager is only present **on the target** when the image includes it, either through the `package-management` image feature or by adding packages such as `dnf` to the root filesystem. The prebuilt reference image contains `dnf 4.14.0` and `rpm 4.18.0`, as its `rootfs.manifest` shows.

> [!TIP]
> Even without a package manager on the target, you can install a single package by copying the `.rpm` from `build/tmp/deploy/rpm/` and running `rpm -ivh` on the target. This is handy for adding debug tools temporarily.

## Cheat sheet

| Task | apt / dpkg (host) | dnf / rpm (PetaLinux target) | opkg |
| --- | --- | --- | --- |
| Refresh repository metadata | `apt update` | `dnf makecache` | `opkg update` |
| Install with dependencies | `apt install <pkg>` | `dnf install <pkg>` | `opkg install <pkg>` |
| Remove | `apt remove <pkg>` | `dnf remove <pkg>` | `opkg remove <pkg>` |
| Upgrade everything | `apt upgrade` | `dnf upgrade` | `opkg upgrade` |
| Search | `apt search <text>` | `dnf search <text>` | `opkg find '*text*'` |
| List installed | `dpkg -l` | `rpm -qa` | `opkg list-installed` |
| Which package owns a file | `dpkg -S <file>` | `rpm -qf <file>` | `opkg search <file>` |
| Files in a package | `dpkg -L <pkg>` | `rpm -ql <pkg>` | `opkg files <pkg>` |
| Package details | `apt show <pkg>` | `rpm -qi <pkg>` | `opkg info <pkg>` |
| Install a local file | `apt install ./x.deb` | `dnf install ./x.rpm` or `rpm -ivh x.rpm` | `opkg install ./x.ipk` |
| Configured repositories | `/etc/apt/sources.list*` | `/etc/yum.repos.d/` | `/etc/opkg/*.conf` |

## Pitfalls

- **Installing packages from another release.** A package from the `rel-v2023` feed, or from Fedora's arm64 archive, was linked against different library versions. It may install and then crash, or not install at all.
- **Expecting a package manager in production images.** Many product images remove it on purpose to save space and reduce the attack surface.
- **Running out of space or memory.** dnf is a Python application and keeps large metadata caches in `/var/cache/dnf`. On small targets, prefer copying single packages or rebuilding the image.
- **Thinking that `dnf install` changes your build.** Runtime installs are lost the next time you flash an image. Anything you want to keep must go into the Yocto/PetaLinux configuration ([chapter 15](../15-root-filesystem-and-init/05-rootfs-configuration-and-packagegroups.md)).

## References

- `meta-petalinux@rel-v2024.1:conf/distro/include/petalinux-feed.conf` (`PACKAGE_FEED_URIS`, `PACKAGE_FEED_ARCHS`)
- `meta-xilinx@rel-v2024.1:meta-xilinx-core/gen-machine-conf/gen-machine-scripts/rootfsconfigs/` (`package-feed-uris`, `package-feed-archs` options)
- `xilinx-zcu106-2024.1:build/conf/plnxtool.conf` (`PACKAGE_CLASSES`)
- Yocto Project Reference Manual: `PACKAGE_CLASSES`, `PACKAGE_FEED_URIS`, `IMAGE_FEATURES`
- Man pages: `apt(8)`, `apt-cache(8)`, `dpkg(1)`, `rpm(8)`, `dnf(8)`
- Captured on the reference setup: host apt/dpkg queries; target rpm queries, `/etc/yum.repos.d/`, `dnf install` of `i2c-tools`, `rsync` and `libgpiod-tools`

---

<sub>← [Linux Distributions and Linux-Based Operating Systems](02-linux-distributions.md) · [Chapter index](README.md) · [Filesystem Hierarchy, Processes and Permissions](04-filesystem-hierarchy-and-processes.md) →</sub>
