# Device Management: devtmpfs, udev and mdev

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Device nodes and policy

`devtmpfs` supplies device nodes for registered kernel devices. A device manager such as udev handles events and applies userspace policy: permissions, symlinks and selected helper actions. BusyBox systems may use mdev with a different feature set.

A node's existence does not prove that the hardware is fully functional. It only shows that the relevant kernel object/interface was registered.

## Stable names and access

Match a device using stable attributes such as its bus path or documented identity, then create a meaningful symlink. Avoid rules that rely only on discovery order. Assign a dedicated group instead of making every device world-writable.

Rules should be short and avoid long-running work in the event handler. Start a service for complex processing. Test unplug/replug and multiple matching devices so the naming policy remains unambiguous.

## Diagnosis

Separate driver binding from device-node creation and userspace permissions. A permission error should not be “fixed” by bypassing the driver through `/dev/mem`.

## References

- udev(7), udevadm(8) for the image's version
- Linux 6.6 driver model and devtmpfs implementation

---

<sub>← [BusyBox](07-busybox.md) · [Chapter index](README.md) · [Users, Passwords and Login](09-users-and-login.md) →</sub>
