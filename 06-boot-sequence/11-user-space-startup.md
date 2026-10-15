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

## References

- `linux-xlnx@xilinx-v2024.1:init/main.c`
- Local BSP systemd package and unit files; saved `boot-ts.log`
- [Init systems](../15-root-filesystem-and-init/06-init-systems.md)

---

<sub>← [Linux Kernel Boot](10-linux-kernel-boot.md) · [Chapter index](README.md) · [Boot Memory Map: Who Loads What, Where](12-boot-address-map.md) →</sub>
