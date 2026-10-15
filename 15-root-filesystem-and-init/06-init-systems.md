# Init Systems: SysVinit, systemd and BusyBox init

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## PID 1 and dependencies

An init system starts services and coordinates shutdown. Systemd uses units and targets; SysVinit uses scripts and runlevels. Select the init manager through the release's distribution/image configuration, then verify the actual PID 1.

A systemd service's ordering is separate from its dependency. `After=` controls order when both units start; it does not by itself pull the other unit in. `Wants=` and `Requires=` express different dependency strength. A network target also does not guarantee that a remote service is reachable.

## Application service design

Run as a dedicated user where possible. Define the executable, working directory, environment, restart policy and writable paths. Keep configuration outside the binary. Readiness should reflect the application's ability to serve requests, not merely process creation.

For SysVinit, use the supported `update-rc.d` integration in the recipe and return meaningful status from scripts. Do not install both service styles without deciding which is active.

## Validation

Test start, stop, restart, dependency failure and shutdown while busy. Read the journal or syslog for the first failure.

## References

- Local BSP: `poky/meta/classes-recipe/systemd.bbclass`, `update-rc.d.bbclass`
- systemd.service(5), systemd.unit(5) for the target's installed version

---

<sub>← [Rootfs Configuration and Packagegroups](05-rootfs-configuration-and-packagegroups.md) · [Chapter index](README.md) · [BusyBox](07-busybox.md) →</sub>
