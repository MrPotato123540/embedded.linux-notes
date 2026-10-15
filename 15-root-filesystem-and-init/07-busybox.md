# BusyBox

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Multi-call design

BusyBox provides many commands through one executable. The invoked applet name selects the behavior. Symlinks can make it appear as `sh`, `mount`, `ls` and other tools while sharing common code.

Its command options and features depend on build configuration. A script tested with GNU tools on the host may fail on BusyBox even when the command names match. Check the target applet's help and avoid assuming every long option exists.

## PetaLinux configuration

The installed configuration tool supports selecting BusyBox as a component. Preserve intentional choices through the project configuration flow. Adding a full GNU utility can coexist with BusyBox through packaging/alternatives rules, but inspect which executable actually handles the command.

## Trade-off

BusyBox reduces footprint and dependencies. Full utilities may offer richer diagnostics or scripting features. Choose according to product requirements and test scripts on the actual image, including error paths and unusual filenames.

## References

- Local PetaLinux 2024.1 configuration help
- [BusyBox documentation](https://busybox.net/downloads/BusyBox.html)
- Local BSP BusyBox recipe and configuration

---

<sub>← [Init Systems: SysVinit, systemd and BusyBox init](06-init-systems.md) · [Chapter index](README.md) · [Device Management: devtmpfs, udev and mdev](08-device-management-and-udev.md) →</sub>
