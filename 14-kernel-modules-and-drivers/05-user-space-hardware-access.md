# Accessing Hardware From User Space

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[14 · Kernel Modules and Device Drivers](README.md)** · Part VI: Linux Kernel and Drivers

## Choose the narrowest useful interface

`/dev/mem` exposes physical memory subject to kernel policy. A `devmem` access bypasses the device driver's locking and lifecycle. Reading a register can have side effects, and accessing an unclocked or absent peripheral can fault or stall.

**Userspace I/O (UIO)** can expose mapped device resources and interrupt notification to a userspace driver. It works best for simple, controlled devices. It does not automatically provide a safe DMA buffer-management API.

| Hardware function | Prefer |
| --- | --- |
| GPIO lines | libgpiod character-device interface |
| Supported SPI/I2C transactions | spidev or i2c-dev where appropriate |
| Measurement channels | IIO |
| Standard device behavior | Existing kernel subsystem |
| Simple custom register block | UIO after ownership and interrupt design |
| Complex DMA/lifecycle | Kernel driver with the relevant APIs |

Binding a generic interface still requires correct device-tree and kernel support. Do not force-bind a device already owned by another driver.

> [!WARNING]
> Direct register writes can reset active hardware or corrupt memory. Use the hardware specification and a controlled test design.

## References

- Linux 6.6 UIO HOWTO and userspace driver documentation
- [DMA and memory management](06-dma-and-memory-management.md)

---

<sub>← [The Linux Device Driver Model](04-linux-device-driver-model.md) · [Chapter index](README.md) · [DMA, CMA and Memory Management](06-dma-and-memory-management.md) →</sub>
