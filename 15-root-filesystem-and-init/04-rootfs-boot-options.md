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

## The root argument is a dependency declaration

The kernel command line identifies how the final root should be located and mounted. A block-device root needs its controller, partition parser and filesystem implementation available at the time of the mount. A network root needs its network hardware, addressing and protocol support ready at that point. Bootloader success does not establish any of these Linux dependencies.

A name such as `/dev/mmcblk0p2` depends on device enumeration. A partition identifier can avoid some naming changes, but it must match the deployed media and the parser supported by the selected boot path. Filesystem UUID resolution performed by an initramfs tool is not identical to every identifier understood directly by the kernel.

Read the actual selected command line and early userspace policy. A bootloader environment variable that is never used to construct the final command line has no effect. Similarly, changing a generated boot script on the host does not change a different script already stored on the boot medium.

## Why `rootwait` sometimes helps and sometimes cannot

Some controllers discover devices asynchronously. Waiting for the root device can be necessary when the device is valid but not yet registered. It cannot load a driver that exists only inside that unavailable root. It also cannot repair a wrong partition identity or make unsupported storage hardware appear.

A fixed delay can hide timing variation during development. It provides weak evidence because a slower card, a changed driver or another boot task can shift discovery again. Prefer a wait condition tied to the intended resource, with useful diagnostics and a recovery policy.

The pinned `init/do_mounts.c` provides the direct kernel root-mount path. An initramfs with its own `/init` may implement additional lookup and waiting. When behavior differs from the kernel source, establish which component actually mounts the root before drawing conclusions.

## Follow a local block-root boot

In an illustrative SD-card design, the boot firmware reads boot artifacts from a boot partition. Linux later enumerates the MMC controller and card, discovers partitions, locates the selected root and mounts its filesystem. These are separate reads by different software components.

A boot partition can be readable by U-Boot while the Linux root partition is unavailable because the Linux MMC driver or pin configuration is wrong. Conversely, Linux can discover the whole card but fail to mount the root because the selected partition contains an archive instead of a filesystem image.

After mounting, the kernel or early init still has to start the final init executable. A log ending with “cannot execute init” has already passed a different boundary than a log ending with “cannot open root device.” Preserve the last successful boundary when reporting the failure.

## Network root adds two boot-time contracts

An NFS root needs a working network path and a correctly exported server filesystem. The client must establish its address and route, then negotiate the supported NFS transport/version and export. A successful Ethernet link indication proves only a lower layer.

The server's ownership mapping and export policy affect the client root. Root-squash behavior can change the permissions seen by privileged client operations. A directory that is readable from the host's local account is not automatically a valid NFS root for the target.

Network root is useful for development because files can be updated centrally. It changes failure and trust assumptions: server availability, network timing and deployment consistency become part of boot. If an application or library is replaced while the target is using it, results may not match a clean image boot.

## Separate software identity from writable state

For an A/B root design, boot selection chooses a software slot while persistent state may live elsewhere. Both slots need the required kernel/modules combination and a clear compatibility contract with that state. A root switch alone does not make firmware, device tree and PL design compatible.

A rollback should restore a known set of boot artifacts and root software. Record the selected slot and image version early enough to diagnose an unexpected fallback. Avoid storing the only rollback decision in the same filesystem that may be damaged.

This section does not provide an untested partition rewrite procedure. Preparing real boot media needs the exact device identity, partition layout and backup policy; the source inspection here does not establish those inputs.

## Use a boundary table during diagnosis

| Last confirmed event | Next evidence to collect |
| --- | --- |
| Bootloader loaded kernel | Actual kernel command line and device tree |
| Storage controller probed | Device enumeration and partition identities |
| Root device located | Filesystem support, image format and mount error |
| Root mounted | Init symlink, interpreter and libraries |
| Init running | Service dependencies, permissions and writable paths |

This avoids replacing bootloader files for a userspace library problem or adding init scripts for a missing built-in storage driver.

## References

- [linux-xlnx@xilinx-v2024.1:init/do_mounts.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/init/do_mounts.c) and [init/main.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/init/main.c).
- Inspected BSP boot and rootfs artifacts under `pre-built/linux/images/`.

- Linux 6.6 kernel-parameter and NFS-root documentation
- AMD UG1144 (2024.1), rootfs and WIC configuration

---

<sub>← [Filesystem Types for Embedded Systems](03-filesystem-types.md) · [Chapter index](README.md) · [Rootfs Configuration and Packagegroups](05-rootfs-configuration-and-packagegroups.md) →</sub>
