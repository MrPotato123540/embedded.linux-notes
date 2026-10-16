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

## PID 1 has a system-wide lifetime

The first userspace process supervises the system's transition into normal operation. It must remain alive and deal with child-process lifetime. Orphaned processes can be reparented to a suitable subreaper or ultimately the namespace's init process. Unreaped children retain process-table entries as zombies even though they are no longer running.

PID 1 also has special signal behavior. A program that works as an ordinary shell-launched process is not automatically a suitable init. A minimal custom init must install the required handlers, reap children and define shutdown behavior. Using a shell as an emergency init is a diagnostic technique, not a complete service manager.

The kernel source tries the early init and configured/default final init choices in `init/main.c`. Once the userspace init is running, service policy moves out of that kernel path. A failed application service is therefore a different stage from a kernel failure to start PID 1.

## The supplied image uses systemd

Archive inspection found `/sbin/init` pointing to `../lib/systemd/systemd`. The supplied manifest reports systemd `251.8`, and `/etc/inittab` was absent from that archive. These facts establish the packaged init choice. They do not prove which image a separately connected board currently runs.

BusyBox is also installed, but its presence does not make BusyBox init the active PID 1. One image can use BusyBox utilities with systemd supervision. Likewise, an init script in `/etc/init.d` is not sufficient evidence that the system boots under traditional SysV init.

When changing init systems, review image feature selection, service integration and expected runtime directories together. Replacing only the `/sbin/init` symlink can leave every service configured for a manager that no longer runs.

## Ordering is not requirement or readiness

In systemd, ordering relationships control when jobs run relative to each other. Requirement relationships control which units are pulled in and how failures affect them. An ordering rule alone does not necessarily start the named unit. A requirement alone does not necessarily establish the desired order.

Readiness is a third property. A service process can exist before its socket, hardware state or database is ready. A startup type that reports readiness through notification gives the manager a stronger boundary than merely observing that the process was spawned. The service must actually implement that notification protocol.

For an application that depends on a PL accelerator, “after boot” is too vague. Its real prerequisites may be a programmed design, a successfully bound driver, accessible device nodes and compatible runtime metadata. Represent those conditions through a controlled integration service and explicit application errors rather than an arbitrary delay.

## A worked dependency failure

Imagine a data-collection service that writes to a persistent volume. Its executable starts correctly, but the volume has not mounted yet. If it writes into the underlying empty mountpoint, it can fill the root filesystem. When the volume later mounts, those files disappear from the visible path while still consuming space underneath.

The fix is a mount dependency and startup validation of the intended storage, not a longer sleep. The service should fail clearly if its durable state directory is unavailable or points to the wrong filesystem. The supervisor can then report a dependency failure rather than repeatedly creating data in the wrong place.

Now consider shutdown. The collector must stop and flush before the volume unmounts. Startup and shutdown ordering are related, but the application's stop path still needs to finish its work within a defined timeout. A forced kill can leave an application-level transaction incomplete even on a healthy filesystem.

## Restart policies need a failure model

Automatic restart helps with transient failures. It can also hide permanent configuration errors and create a rapid crash loop. Distinguish clean completion, recoverable runtime errors and invalid configuration. Rate limits and diagnostic logs keep repeated failure observable.

A watchdog should measure useful progress. A loop that sends watchdog notifications while its worker is deadlocked proves only that the notification loop runs. Tie health to the actual service contract, such as fresh input processing or completed transactions, without making a slow but valid operation look like a hang.

Services should run in the foreground under the manager unless the selected service type explicitly expects daemonization. Double-forking without the correct manager contract can make the wrong process appear to be the service's main process.

## Diagnose the process boundary

First verify what PID 1 is. Then distinguish unit parsing, dependency scheduling, executable startup and runtime failure. A missing unit file differs from an executable whose loader is missing. A process killed by a resource limit differs from one that exits because its device node is absent.

Preserve the service's first error and exit status. Later restart messages often repeat the symptom without explaining it. For reproducible support, include the installed unit, environment, working directory and image version with the failure report.

## References

- Inspected BSP `rootfs.tar.gz`, `rootfs.manifest` and `poky/meta/recipes-core/systemd/systemd_251.8.bb`.
- [systemd v251:systemd.service.xml](https://github.com/systemd/systemd/blob/v251/man/systemd.service.xml) and [systemd.unit.xml](https://github.com/systemd/systemd/blob/v251/man/systemd.unit.xml), service types and dependency semantics.

- Local BSP: `poky/meta/classes-recipe/systemd.bbclass`, `update-rc.d.bbclass`
- systemd.service(5), systemd.unit(5) for the target's installed version

---

<sub>← [Rootfs Configuration and Packagegroups](05-rootfs-configuration-and-packagegroups.md) · [Chapter index](README.md) · [BusyBox](07-busybox.md) →</sub>
