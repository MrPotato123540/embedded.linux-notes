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

## Kernel registration precedes naming policy

A driver registers a device with the kernel's device model. When the device exposes a character or block interface, a device number identifies the kernel endpoint. A device node in `/dev` contains that identity and permissions. The node itself is not the driver and does not prove that hardware is operational.

With devtmpfs enabled and mounted, the kernel can maintain a basic set of device nodes. Userspace device management adds policy: permissions, ownership, stable symlinks and actions in response to events. If a node appears before a custom udev rule runs, that is expected separation of mechanism and policy.

`drivers/base/devtmpfs.c` in the pinned source implements the kernel side. Device events and sysfs attributes provide userspace with information about the registered device. The supplied image packages udev at version `251.8`, matching its systemd generation.

## Stable names should express identity

Enumeration names such as numbered serial ports can change when discovery order changes. A stable symlink should use a property that matches the intended identity: physical connection, hardware serial number or a documented function. Each choice has tradeoffs.

A serial-number-based name follows the device when moved between ports. A topology-based name follows the connector when the device is replaced. A product must decide which behavior is correct. Matching only a broad vendor ID can make two identical devices compete for the same symlink.

For a PL device, a stable path can depend on the static design, device-tree node or subsystem identity. Runtime reconfiguration may remove and recreate the device. Applications must handle that lifecycle instead of holding a pathname as if it were a permanent object.

## Event ordering is not application readiness

A device-add event means the kernel published the device at a particular stage. It does not mean an external peer is connected, a removable medium is ready, or a calibration operation has completed. An application still needs the subsystem's operational readiness checks.

Rules can run before all related devices are available. Avoid building long dependency chains through event scripts that assume a global discovery order. Use the service manager to start longer-lived work and let the application report the actual readiness of its device.

Long-running tasks are unsuitable inside ordinary device-event rule execution. They can block processing or be terminated under the event manager's lifecycle policy. Keep rules focused on naming and permissions; hand service work to a manager with an explicit lifetime.

## A worked permission design

Suppose an acquisition service should use one sensor interface. Create a dedicated account and group in image metadata. Give the relevant device node the minimum group access, and run the service with that group. The application then uses the normal driver interface without needing unrestricted root privileges.

The rule must match the correct device. A broad rule granting write access to all memory or all accelerator nodes expands the application's authority beyond the intended sensor. Review the final node ownership after the rule runs and after the device is recreated.

Permissions on the node control opening the device. They do not fully describe what an already open descriptor can do. If the driver exposes arbitrary DMA or privileged ioctls, group membership can still grant broad hardware authority. The kernel interface design and userspace permission policy must agree.

## Removal invalidates resources, not just names

Removing a node stops new path-based opens, but existing file descriptors remain kernel objects. The driver decides how operations fail after disconnect and how outstanding work completes. Applications should treat disconnection as a state transition and close/reopen when a compatible device returns.

A recreated node can have the same pathname but represent a new device instance. Keeping old mmap pointers or cached DMA handles across reconfiguration can therefore be unsafe. Revalidate identity and rebuild per-device state after reconnection.

For a USB or hotplug test, separate rapid unplug/replug from normal startup. For a PL design, remove software consumers before changing hardware, as explained in chapter 17. The naming layer cannot make stale hardware access safe.

## Evidence that separates failures

If the device is absent from sysfs, investigate discovery and driver binding. If it exists in sysfs but not in `/dev`, inspect the interface registration and devtmpfs mount. If the node exists with wrong permissions, inspect rules and matching properties. If access succeeds but operations fail, investigate the driver and hardware protocol.

A manually created node can help identify a node-management issue, but it does not register a missing driver. A chmod workaround can prove a permission hypothesis, but a permanent fix belongs in the image's account and rule policy.

> [!NOTE]
> **Not run on the reference setup:** custom udev rule deployment, physical hotplug and PL device removal. The packaged manager and pinned devtmpfs source were inspected.

## References

- [linux-xlnx@xilinx-v2024.1:drivers/base/devtmpfs.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/base/devtmpfs.c).
- [systemd v251:udev.xml](https://github.com/systemd/systemd/blob/v251/man/udev.xml), rule matching and event execution.
- Inspected BSP `pre-built/linux/images/rootfs.manifest`.

- udev(7), udevadm(8) for the image's version
- Linux 6.6 driver model and devtmpfs implementation

---

<sub>← [BusyBox](07-busybox.md) · [Chapter index](README.md) · [Users, Passwords and Login](09-users-and-login.md) →</sub>
