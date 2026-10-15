# Root Filesystem Fundamentals

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## What the root filesystem supplies

The root filesystem supplies the files userspace needs after kernel initialization: init, applications, configuration, libraries and the dynamic loader. A dynamically linked executable can exist and still fail with “not found” when its requested loader is missing.

`/dev` exposes device nodes. `/proc` and `/sys` expose kernel information and control interfaces through virtual filesystems. They are not ordinary static directories whose saved contents reproduce a running system.

## Image assembly

Yocto's `do_rootfs` installs selected packages and applies image policy. The manifest records package selection. Manual changes made after boot are outside that build record unless converted into recipes or configuration.

A read-only root simplifies recovery and prevents accidental system-file changes. Applications still need explicit writable locations for state, logs and temporary files. An overlay can provide writable behavior, but persistent overlay data needs migration and capacity management.

## Validation

Check init, the loader, required libraries, mounts and permissions. Test startup with an empty writable-data partition as well as an upgraded one.

## References

- Local BSP image recipes and `rootfs.manifest`
- Linux 6.6 filesystem documentation

---

<sub>[Chapter index](README.md) · [initrd vs. initramfs](02-initrd-and-initramfs.md) →</sub>
