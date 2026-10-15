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

## References

- Linux 6.6 [ramfs, rootfs and initramfs](https://docs.kernel.org/6.6/filesystems/ramfs-rootfs-initramfs.html)
- Reference FIT inspection

---

<sub>← [Root Filesystem Fundamentals](01-rootfs-fundamentals.md) · [Chapter index](README.md) · [Filesystem Types for Embedded Systems](03-filesystem-types.md) →</sub>
