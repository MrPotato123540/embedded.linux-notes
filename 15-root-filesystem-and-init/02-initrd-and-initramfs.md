# initrd vs. initramfs

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Two early-root models

An **initrd** traditionally contains a filesystem image used through a RAM block device. An **initramfs** is a cpio archive extracted into the kernel's initial rootfs. That rootfs uses ramfs or tmpfs according to kernel configuration; it is not always tmpfs.

An initramfs can be linked into the kernel or supplied externally. Its `/init` becomes PID 1 and can prepare storage, unlock or verify a root volume, then switch to the persistent root. The handoff must replace the early init process correctly.

## Build and packaging

Yocto's `INITRAMFS_IMAGE` selects an image used for early userspace; bundling is a separate choice. A `.cpio.gz.u-boot` file adds a U-Boot image wrapper around the archive. Do not pass the wrapper where a loader expects the raw archive.

The inspected reference FIT includes an initramfs image. Its presence does not mean every `rootfs.*` file in the directory is embedded in the FIT.

## Diagnosis

If `/init` fails, check executable format, interpreter, permissions and dependencies. Distinguish that failure from failure to find the later root device.

## The early archive is a boot program, not just storage

An initramfs contains the files needed before the final root is available. The kernel expands its supported cpio stream into the initial rootfs. The early `/init` then owns policy: locating a device, loading needed modules, validating an image, mounting the final root and starting its init system.

The pinned `init/initramfs.c` contains archive parsing and population. `init/main.c` starts with `/init` as the early userspace choice. If it cannot access that early init, the kernel can follow its normal root-mount path. If an early init does run, its process must finish the userspace handoff. Returning from PID 1 is not a successful way to continue boot.

An archive supplied externally and one linked into the kernel reach related unpacking machinery, but packaging and trust boundaries differ. A separately loaded archive needs a reserved memory range until the kernel consumes it. A bundled archive changes the kernel artifact itself and usually its signed measurement or image hash.

## Follow a two-stage root transition

Consider an illustrative design that starts from a small initramfs and later uses an ext4 partition. The early image contains an init program, its interpreter and libraries, mount support, storage drivers if they are modules, and any verification tools. A module needed here cannot exist only on the later ext4 root.

Early init first establishes essential virtual filesystems and access to devices. It waits for the intended storage identity, validates policy and mounts the final root at a temporary location. It then moves or recreates the required mounts and replaces itself with the final init. The final init must see the intended root as `/` and must remain PID 1.

`switch_root` is designed for this kind of handoff. Its exact behavior depends on the implementation. The initial rootfs has special lifetime rules, so treating it like an ordinary mounted filesystem and applying an arbitrary `pivot_root` recipe is not equivalent. Do not write an improvised recursive deletion sequence into a product boot script.

Failure before mounting the final root should leave a controlled diagnostic or recovery state. Failure after partially moving mounts is harder: paths, console access and cleanup may already have changed. Design an explicit success boundary rather than assuming every mount operation succeeds.

## Wrapper, compression and payload are separate layers

The reference image directory contains raw compressed cpio archives and U-Boot-wrapped variants. A FIT can describe a ramdisk payload with metadata and hashes. A legacy `.u-boot` wrapper adds another header. The consumer must know which representation it receives.

A useful review separates three questions: where the container starts, how its payload is compressed, and what that decompressed payload represents. A gzip signature alone does not tell you whether the content is a cpio archive or a filesystem image. A filename alone is even weaker evidence.

The existing FIT listing confirms that the supplied FIT includes a ramdisk entry. It does not establish that the larger `rootfs.ext4` or every file named `rootfs` is loaded during that boot. Follow the selected FIT configuration and bootloader handoff addresses.

## Memory peaks during unpacking

During boot, the compressed archive and extracted data can coexist. Decompression also uses working memory, and the kernel already occupies memory. The maximum early-boot footprint can therefore exceed the archive's compressed size by a large factor.

After a correct handoff, the early image's files should no longer retain unnecessary memory. Open file descriptors, current directories and mounts can keep objects alive. A process left running from early userspace can keep an old root reachable even when the visible `/` has changed.

Ramfs has no backing store for reclaiming file data. Tmpfs has different limits and swap behavior. Neither should be treated as persistent storage. An application that writes unlimited logs into early RAM storage can make the machine fail before persistent storage is mounted.

## Diagnose the exact handoff stage

| Observation | Interpretation to test |
| --- | --- |
| Archive unpack error | Container offset, compression support, corruption or cpio format |
| `/init` exists but exec fails | ELF architecture, interpreter, script shebang and permissions |
| Early shell works, final device absent | Controller driver, device discovery and root identity |
| Final root mounts, final init fails | Libraries, mounts and pathname visibility in the new root |
| Boot succeeds but RAM remains unexpectedly high | Old-root references, retained processes and archive lifetime |

The init program should record stage-specific failures using the early console. A single “boot failed” message cannot distinguish a missing storage driver from a missing dynamic loader.

> [!NOTE]
> **Not run on the reference setup:** replacing the supplied initramfs or testing a new two-stage root script. The transition described here is a design walkthrough, not a captured successful boot.

## References

- [linux-xlnx@xilinx-v2024.1:init/initramfs.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/init/initramfs.c) and [init/main.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/init/main.c).
- [Pinned ramfs/rootfs/initramfs explanation](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/filesystems/ramfs-rootfs-initramfs.rst).

- Linux 6.6 [ramfs, rootfs and initramfs](https://docs.kernel.org/6.6/filesystems/ramfs-rootfs-initramfs.html)
- Reference FIT inspection

---

<sub>← [Root Filesystem Fundamentals](01-rootfs-fundamentals.md) · [Chapter index](README.md) · [Filesystem Types for Embedded Systems](03-filesystem-types.md) →</sub>
