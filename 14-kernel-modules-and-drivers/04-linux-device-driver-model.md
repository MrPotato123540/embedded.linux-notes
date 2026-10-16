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

## Read the example in resource-acquisition order

The teaching driver's first operation obtains resource zero and checks that it covers a 32-bit register. This checks the software description's length. It cannot prove that an interconnect route exists or that the PL block is powered. The later identity read is meaningful only after the hardware contract is already safe to access.

`devm_kzalloc()` allocates device-owned private state. `devm_platform_ioremap_resource()` reserves and maps the resource as MMIO. The returned pointer has the `__iomem` annotation to distinguish it from ordinary RAM. `IS_ERR()` checks the encoded error pointer; treating it as `NULL` alone would miss failures.

`readl()` accesses the declared little-endian register. If the value differs from the teaching identity, probe returns `-ENODEV`. The driver does not publish a user interface first and then discover that it owns the wrong device. This ordering makes the successful probe boundary useful.

Only after validation does `platform_set_drvdata()` associate private state with the device, and `devm_device_add_groups()` publish the attribute group. The sysfs callback recovers that state through the device. The user sees one textual value, formatted by `sysfs_emit()` within sysfs's buffer rules.

## Why this example needs no explicit remove callback

Managed actions release in reverse order. Here, the interface is registered after the mapping and allocation, so cleanup removes the interface before releasing those resources. Sysfs removal coordinates active operations through its own lifetime rules. This narrow arrangement works because the driver has no interrupt, timer, worker, DMA job or retained open character-device context.

A real streaming driver cannot copy this absence of a remove callback. Managed memory only knows when to free an allocation. It does not know that a PL bus master still holds its DMA address. Freeing the allocation before stopping that master can corrupt an unrelated allocation that later reuses the memory.

Likewise, a managed interrupt registration releases the handler registration, but your design must stop the device from generating new work and account for callbacks that queue work elsewhere. A resource helper solves one ownership problem. It does not prove the entire shutdown sequence.

## Probe failure is partial removal

Imagine a larger driver that enables a clock, maps registers, allocates a ring, requests an interrupt and finally registers an interface. Failure at each point leaves a different set of acquired resources. Managed helpers reduce the number of explicit labels, but the hardware state still needs a defined rollback.

If the ring is already active when interface registration fails, rollback must stop DMA before the buffer can be released. If hardware stop needs a live clock, disable the clock after the stop. If reset destroys completion status, capture diagnostic state before reset when that is safe. These constraints determine cleanup order.

Probe should leave hardware idle until the driver has enough resources to handle its events. Enabling interrupts before state and synchronization objects exist can call a handler on a half-built object. Allocate and initialize software state before exposing any path that can use it.

## User interfaces outlive individual calls

A character-device open file can retain private data after device removal. The design needs a reference count or equivalent lifetime arrangement, a disconnected state, and a policy for blocked readers. Removing the device node stops future pathname opens but does not revoke existing file descriptors.

Memory mappings are more difficult. A userspace virtual memory area can remain after the file descriptor closes. The mapping's open/close operations and page lifetime must protect backing memory. For MMIO, removal or reconfiguration can also make the underlying address unsafe. Prevent replacement while mapped, or implement a well-defined revocation mechanism; do not assume closing one process removes all mappings.

An ioctl interface should use fixed-width fields, explicit lengths and reserved fields for growth. Validate every user-controlled count and offset before arithmetic. Avoid copying raw kernel pointers or compiler-dependent structures across the boundary. Compatibility with 32-bit userspace requires separate attention on a 64-bit kernel.

## Locking follows the context

A mutex can protect a request queue in process context, where sleeping is allowed. A hard interrupt handler cannot take that mutex. A spinlock can protect short shared state, but code inside the locked region cannot perform operations that sleep. Choosing a threaded interrupt changes what the thread may do; it does not remove the need to protect shared data.

For a completion interrupt, separate acknowledgment, state transition and notification. Acknowledge according to the register specification, record exactly which job completed, then wake the waiting path. A shared Boolean such as `done` can lose completions when multiple jobs overlap. Use queue entries, sequence numbers or the subsystem's established request objects.

The example's single read-only register avoids these races by design. Extending it with a start register is a new concurrency contract, not a small cosmetic change.

## References

- [linux-xlnx@xilinx-v2024.1:Documentation/driver-api/driver-model/devres.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/driver-model/devres.rst).
- [linux-xlnx@xilinx-v2024.1:drivers/base/dd.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/base/dd.c), probe and unbind implementation.

- Linux 6.6 [device model](https://docs.kernel.org/6.6/driver-api/driver-model/overview.html)
- Linux 6.6 driver API: managed resources, platform drivers and interrupt handling

---

<sub>← [Adding Modules to a PetaLinux Project](03-modules-in-petalinux.md) · [Chapter index](README.md) · [Accessing Hardware From User Space](05-user-space-hardware-access.md) →</sub>
