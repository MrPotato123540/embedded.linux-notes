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

## Choose the ownership model before the access method

A process that can map registers gains direct control over the device. The key design question is who owns reset, interrupt acknowledgment, DMA buffers and removal. A mapping API does not answer these questions. A useful userspace driver architecture keeps the minimum trusted hardware management in the kernel and gives a process only the resources it needs.

For ordinary devices, an established subsystem is often the simplest stable interface. GPIO, IIO, networking, V4L2 and DRM already define concurrency and lifetime behavior. A custom register map should be justified by the device's actual contract, not by the short length of an `mmap()` example.

## Mapping arithmetic does not validate hardware

An MMIO mapping has a page-aligned base and a length that covers the needed register range. If a register block starts within a page, the process adds the within-page offset to the returned mapping. The mapping length must include that offset and the last accessed byte. Overflow checks are necessary before rounding or adding user-controlled lengths.

This arithmetic only establishes a valid virtual mapping request. It does not confirm access width, endianness, read side effects, device power or bitstream identity. A wrong-width access can be invalid even inside the mapped range. A read of a clear-on-read status register changes hardware state even if the mapping is read-only.

A compiler's `volatile` qualifier prevents some compiler transformations. It does not implement the kernel's DMA ownership protocol, configure cacheability, guarantee device ordering for every platform or prevent another process from accessing the same register. Userspace MMIO needs a documented architecture and device-specific access discipline.

## What UIO provides

Userspace I/O (UIO) exposes kernel-declared device memory regions and an interrupt event interface. The kernel still registers the device and controls the mapping. Userspace can inspect exported map metadata instead of assuming that every region has the same size or purpose.

For `uio_pdrv_genirq`, the pinned source shows a deliberately small generic handler. It disables the interrupt and records that disabled state. The userspace side must clear the actual device condition before asking the driver to enable the interrupt again. If the device source remains asserted, re-enabling can immediately trigger another event.

The generic UIO driver does not know which of your registers is write-one-to-clear. That knowledge remains in the userspace device driver. A crashed process may leave the interrupt disabled or the peripheral running, so the supervisor and kernel glue need a recovery policy.

The event counter allows the application to detect that interrupt activity occurred; it is not necessarily one event per completed buffer. Coalescing, shared status bits and hardware queue behavior can make that interpretation false. Read completion state from the device's specified protocol.

## UIO is not a DMA security boundary

Mapping a control register that accepts arbitrary bus addresses allows a process to direct DMA. Restricting the MMIO map's size does not restrict the memory addresses written into that register. A trusted application can still have a bug, and an untrusted process can intentionally program another address.

An I/O Memory Management Unit (IOMMU) can constrain device transactions when the full hardware path and driver model support it. VFIO builds on controlled device assignment and IOMMU groups. The group is an isolation boundary; do not infer isolation from a device name or a device-tree property alone. Embedded platform support must be checked for the actual integration.

A simpler custom kernel interface can allocate and map buffers itself, validate transfer lengths, and accept opaque buffer handles from userspace. This keeps DMA addresses out of application control. It still needs ownership transitions and correct cleanup when the process exits.

## Why `/dev/mem` is a poor product interface

`/dev/mem` exposes physical-address access subject to kernel configuration and policy. It bypasses the ordinary driver's resource ownership and subsystem API. Two components can then write the same device without coordinating resets or interrupts. The access may also be denied even for a privileged process when the configured policy restricts that range.

Use it only as a tightly controlled engineering tool when the register contract and ownership are already known. There are no arbitrary register-write examples here because the reference setup does not supply a safe board-specific PL contract. A convenient shell write is not evidence that a device is unused.

## Distinguish mapping, protocol and lifetime failures

A failed mapping points first to permissions, offsets, lengths and kernel policy. A mapping that succeeds but produces a bus fault points to address decode, clock/reset or access semantics. Correct register reads with stalled jobs point to interrupt, DMA or device protocol. A failure only after process restart points to hardware state left behind by the previous owner.

Test process termination while idle and while busy as separate cases on the real device. A sound design stops or safely transfers ownership before memory and interrupts are reused. Restarting the program should not require guessing whether the previous DMA request is still active.

## References

- [linux-xlnx@xilinx-v2024.1:Documentation/driver-api/uio-howto.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/uio-howto.rst).
- [linux-xlnx@xilinx-v2024.1:drivers/uio/uio_pdrv_genirq.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/uio/uio_pdrv_genirq.c).

- Linux 6.6 UIO HOWTO and userspace driver documentation
- [DMA and memory management](06-dma-and-memory-management.md)

---

<sub>← [The Linux Device Driver Model](04-linux-device-driver-model.md) · [Chapter index](README.md) · [DMA, CMA and Memory Management](06-dma-and-memory-management.md) →</sub>
