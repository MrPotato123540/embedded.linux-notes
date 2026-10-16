# User-Space Startup

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## PID 1 takes control

After the kernel prepares the initial userspace environment, it starts an init program as process ID 1. PID 1 starts and supervises services, handles system shutdown and reaps orphaned child processes.

With systemd, unit dependencies and ordering control startup. With SysVinit, scripts and runlevel links provide the main structure. Neither model means that every service starts strictly one after another.

## Typical startup work

Userspace mounts additional filesystems, handles device events, configures networking and starts login services. A serial getty creates a login prompt; the kernel console alone does not do that. A working shell does not prove that networking or the product application is ready.

Device discovery can trigger services while other work is still running. A program should wait for its actual dependency instead of relying on an arbitrary delay.

## Measuring boot

Define the endpoint before measuring: login prompt, network connectivity or first valid application response. Systemd's timing tools can show userspace activation, but they do not account for every earlier firmware delay. Combine them with timestamped serial captures or an external signal.

> [!NOTE]
> **Not run on the reference setup:** a fresh boot-time benchmark. Existing timestamped captures are evidence of the recorded image only.

## Follow the kernel's init selection

The kernel does not start every service directly. It prepares an initial process and executes an init program. In the pinned `init/main.c`, the default early-userspace command is `/init`. Kernel parameters can change the early init or final init selection. The implementation then attempts the relevant command and handles failures before trying the normal fallback paths.

For the normal fallback sequence, the source tries `/sbin/init`, `/etc/init`, `/bin/init` and `/bin/sh`. An explicitly requested init command has different failure handling from simply finding no default init. Read the precise log and source branch before diagnosing all cases as a missing root filesystem.

Once the init program runs as PID 1, it becomes responsible for the normal userspace lifecycle. Its behavior is special: it coordinates shutdown and must deal with child-process lifecycle. An unexpected PID 1 exit is a system-level failure, not an ordinary service crash.

## A mounted root does not guarantee executable userspace

The root filesystem can mount successfully while init fails to execute. Check the file's permissions and executable format. For a script, check the interpreter named in its first line. For a dynamic ELF, check the loader and required libraries. A missing interpreter can make an existing file appear unexecutable.

This distinction is useful for a newly minimized image. Removing a package can remove the interpreter or library needed by init or an early script. The kernel and storage driver may be functioning correctly. Restoring arbitrary kernel options will not fix that userspace dependency.

An initramfs can add another root transition. Its `/init` may prepare the final root and replace itself with the final init system. Preserve early-userspace logs because failures before that transition may never reach the normal persistent journal.

## Ordering and requirement are separate relationships

A service can need another unit and can need to start after it. These are different statements. In systemd, dependency and ordering relationships are represented separately. A unit ordered after another unit does not necessarily cause that other unit to be started.

Read the installed unit files and their drop-ins rather than only the service name. Generated units, device units and mount units can also participate in startup. The resulting graph can run independent work concurrently.

This is why a fixed sleep is a weak readiness mechanism. A five-second delay can be unnecessarily long on one boot and too short on another. Wait for the real condition: a device, a mount, a successful protocol exchange or an application-specific ready state.

## Process start and service readiness differ

Starting an executable proves only that the service manager attempted execution. The program may still be reading configuration, opening hardware or connecting to another system. A product health check should observe the function the product needs, not merely the existence of a process ID.

For a measurement service, readiness might require valid configuration, an opened device and one successful sample. For a network service, it might require listening on the intended interface and completing a local request. Define this contract before using the service as the condition that marks a new software slot healthy.

A service can also fail after initial readiness. Restart policy, rate limits and watchdog behavior should match the failure model. Repeated automatic restarts can hide a persistent configuration error and fill logs without restoring useful operation.

## Console, login and network access are separate services

The kernel console displays kernel messages. A serial getty provides a login interaction. An SSH server provides remote login through the network stack and authentication policy. One can work while another fails.

If kernel output is visible but no login prompt appears, inspect the getty and userspace state. If serial login works but SSH does not, inspect network configuration, server startup, listening addresses and authentication logs. Do not assume the UART or kernel image is defective because one access method is unavailable.

The reference image uses systemd, as reflected in its generated project configuration. Another product image can use a different init policy. Keep init-specific commands and unit semantics tied to the actual image.

## Measure a defined endpoint

A boot-time number needs a start event and an end event. Power application to first valid application response is different from kernel entry to login prompt. Systemd activation timings cover userspace work and cannot account for every earlier firmware or bootloader delay.

Use timestamped serial capture or an external observable signal for end-to-end measurement. Record logging policy, storage state, network conditions and whether the test was cold or warm. Serial logging itself can affect timing, especially in early firmware.

The existing `boot-ts.log` documents the recorded reference run. It is not a new benchmark of a modified image. The source walk above clarifies the milestones so future measurements can state exactly what they measured.

## References

- `linux-xlnx@xilinx-v2024.1:init/main.c`
- Local BSP systemd package and unit files; saved `boot-ts.log`
- [Init systems](../15-root-filesystem-and-init/06-init-systems.md)

---

<sub>← [Linux Kernel Boot](10-linux-kernel-boot.md) · [Chapter index](README.md) · [Boot Memory Map: Who Loads What, Where](12-boot-address-map.md) →</sub>
