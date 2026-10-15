# Root Filesystem Boot Options in PetaLinux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Root selection

The kernel command line and early userspace determine the final root. `root=` identifies the device or supported root source. `rootfstype=` can constrain the filesystem. `rootwait` waits for a root device to appear; it does not repair an incorrect device name. `ro` and `rw` select the initial mount intent.

Block roots need storage and filesystem support before mounting. NFS root needs early network configuration. UBIFS needs the correct UBI attachment and volume. An initramfs can perform more complex discovery before switching root.

## SD and eMMC

A WIC image carries a partition layout and filesystem contents. Manual preparation must reproduce the layout, boot files, filesystem metadata and root selection. Use stable identifiers where the boot flow supports them; device enumeration can change when hardware is added.

> [!WARNING]
> Partitioning or writing a whole-disk image can erase the selected device. Verify the physical device identity and preserve required data first.

## Diagnosis

Read the root-mount error and compare it with the detected devices. A missing controller driver, unsupported filesystem and wrong partition identifier can produce similar user-visible symptoms.

> [!NOTE]
> **Not run on the reference setup:** new SD/eMMC preparation or NFS-root boot during this continuation.

## References

- Linux 6.6 kernel-parameter and NFS-root documentation
- AMD UG1144 (2024.1), rootfs and WIC configuration

---

<sub>← [Filesystem Types for Embedded Systems](03-filesystem-types.md) · [Chapter index](README.md) · [Rootfs Configuration and Packagegroups](05-rootfs-configuration-and-packagegroups.md) →</sub>
