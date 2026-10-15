# The Linux Device Driver Model

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[14 · Kernel Modules and Device Drivers](README.md)** · Part VI: Linux Kernel and Drivers

## Devices and drivers

A bus describes how devices and drivers match. A platform device commonly represents a memory-mapped block described by firmware. The driver's probe function acquires resources and prepares the device; removal must stop activity and release ownership.

Managed `devm_*` helpers simplify cleanup, but they do not stop DMA or cancel work automatically in every design. Use the clock, reset, pinctrl and regulator frameworks instead of unexplained register writes. Regmap can provide structured register access where the hardware fits its model.

## Interface design

Choose an existing subsystem when possible. Use IIO for suitable measurement devices, GPIO for simple lines, and other established classes for standard hardware. A misc or character device is useful for a custom interface, but its read/write/ioctl contract needs clear sizes, permissions and concurrency rules.

Interrupt handlers should acknowledge the correct condition and keep bounded work. Threaded handlers can perform work unsuitable for hard-interrupt context. Always follow the hardware's clear-on-read or write-one-to-clear semantics.

## Custom AXI-Lite driver checklist

A complete driver requires the actual register specification: resource length, access width, reset state, interrupt acknowledgment and device lifetime. Without that specification, a guessed “complete” driver would be unsafe. Define the binding, map the resource, enable dependencies, validate the hardware ID, register the interface, and implement removal/error cleanup. Test concurrent access and removal while busy.

> [!NOTE]
> **Not run on the reference setup:** a board-specific custom AXI-Lite driver. No register contract was supplied for such a peripheral.

## Complete read-only teaching driver

The [driver source](examples/pl-id/pl_id.c), [Kbuild Makefile](examples/pl-id/Makefile) and [device-tree example](examples/pl-id/example.dts) form a minimal platform-driver example. They use an **invented teaching IP contract**, not an undocumented AMD register map:

| Design rule | Value or requirement |
| --- | --- |
| Register offset | `0x00` |
| Register width | 32 bits, little-endian |
| Identity value | `0x504C4944`, chosen for this example |
| Read side effects | None |
| Interrupts and DMA | None |
| Power, clock and reset | Already active before probe; remain active while bound |
| Example bus address | `0xA0000000`, only for the synthetic design |

The probe function checks the resource size, reserves/maps it through `devm_platform_ioremap_resource()`, reads the ID and rejects a mismatch. It then exposes a read-only `identity` sysfs attribute. `readl()` performs MMIO access; an ordinary pointer dereference is not a substitute.

Managed resources are released in reverse order. The sysfs group is registered after the mapping, so it is removed before the mapping and private state are released. This example has no pending work or DMA to cancel. A real streaming driver needs explicit shutdown for those resources.

The module was compiled against the host's **Linux 6.8.0-138 x86-64 headers** in a temporary directory. Compilation completed. The build reported a compiler-version difference and skipped BTF generation because `vmlinux` was unavailable. The example DTS also compiled with DTC without warnings.

> [!IMPORTANT]
> This is a host compile check, not an Arm64/PetaLinux 2024.1 runtime test. The module was **not loaded**. Build it against the exact target kernel before use. Do not apply the example address to a board unless the actual hardware implements this contract; even a read from absent PL hardware can stall the bus.

## References

- Linux 6.6 [device model](https://docs.kernel.org/6.6/driver-api/driver-model/overview.html)
- Linux 6.6 driver API: managed resources, platform drivers and interrupt handling

---

<sub>← [Adding Modules to a PetaLinux Project](03-modules-in-petalinux.md) · [Chapter index](README.md) · [Accessing Hardware From User Space](05-user-space-hardware-access.md) →</sub>
