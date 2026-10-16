# Accessing PL Peripherals From Linux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Standard and custom IP

For standard AMD IP, first check the exact IP version and Linux binding. AXI GPIO, UART Lite, IIC, SPI and Ethernet families have different drivers and configuration requirements. A similarly named controller is not automatically register-compatible.

A custom AXI-Lite block can use UIO for a simple controlled interface or a dedicated kernel driver for stronger lifecycle, interrupt and subsystem integration. DMA usually needs more than a raw register mapping.

## Interrupt path

Trace the signal from the IP through any PL interrupt controller or concatenation, into the PS interrupt input and GIC, then into the device-tree interrupt specifier. The Linux IRQ number is allocated by the kernel and need not equal the hardware interrupt ID.

Check trigger type and acknowledgment behavior. A level interrupt remains asserted until the device condition is cleared. Clearing only the GIC state cannot fix a device that keeps requesting service.

> [!NOTE]
> **Not run on the reference setup:** traffic and interrupts from a custom physical PL peripheral.

## The access path has independent control points

A CPU load reaches a PL peripheral through a virtual mapping, the processing-system interconnect, a PS-to-PL interface and the PL address decode. The peripheral must have a valid clock and reset state. A correct pointer is only one part of this path.

Linux also needs a software owner for the resource. A platform driver normally reserves the address range, maps it with device access semantics, acquires dependencies and exposes a controlled interface. Bypassing that owner can make two paths change the same hardware without agreeing on state.

The address in a device-tree `reg` property follows the parent bus's cell and translation rules. It is not automatically a CPU pointer or a userspace virtual address. Review the parent address/size cells and ranges when a node moves under a different bus.

## Use the teaching identity device carefully

Chapter 14 includes a synthetic PL-ID platform driver. Its example address and identity value are invented teaching inputs. They are not a claim about the supplied ZCU106 design. The source was host-compiled, but no corresponding hardware was programmed or read.

The driver demonstrates a useful ordering: validate resource size, reserve/map, read the known safe identity, and only then publish the read-only sysfs attribute. This prevents userspace from seeing a successfully registered interface for the wrong identity.

A real device must specify whether identity reads are safe during reset, whether the clock must first be enabled and whether the bus can report an error for absent hardware. Without that information, even the first read is not a safe discovery mechanism.

## Register semantics define the software algorithm

A status register may be read-only, clear-on-read or write-one-to-clear. A control register may contain self-clearing bits. A read-modify-write sequence that is correct for an ordinary configuration register can lose events or clear unrelated status when used on a different type.

Consider an illustrative write-one-to-clear interrupt status. Reading the status and writing the same active bits acknowledges those conditions. Writing a guessed all-ones value can clear events the driver did not handle. Combining that register with an ordinary read-modify-write helper can therefore be wrong even though the address and width are correct.

Multiword counters add another problem. If a 64-bit value is exposed through two 32-bit registers, the hardware specification must define a stable-read sequence or latch mechanism. Two independent reads can combine halves from different counter values. Do not invent a high/low read order without the IP contract.

## Polling and interrupts change ownership

Polling repeatedly reads state until a condition changes. It needs a bounded timeout and an error path. A busy loop can consume a core and increase interconnect traffic; a sleeping poll changes latency. Choose the method from the operation's timing requirements.

Interrupt-driven work needs correct routing, trigger type and acknowledgment. The interrupt tells the driver to inspect state; it does not always identify one completed request. Coalesced events or multiple status bits require a queue-aware completion model.

The interrupt handler and process context share data. Protect request state using synchronization valid in each context. Do not sleep in a hard interrupt handler or wait for completion while holding a lock the completion path needs.

## Memory ordering is part of the protocol

Kernel MMIO accessors encode architecture-aware access behavior. An ordinary C pointer dereference is not a replacement. When a device reads descriptors from memory after a doorbell write, the driver must also make descriptor contents visible and ordered before the doorbell.

An MMIO readback is sometimes required to ensure a posted write reached a particular device, but that requirement comes from the bus/device protocol. It is not a universal substitute for DMA cache synchronization. Keep register ordering, shared-memory ordering and cache ownership as separate review items.

For userspace mappings, document the allowed access widths and ordering approach. `volatile` only addresses part of compiler behavior; it does not create a safe DMA or removal protocol.

## Reconfiguration ends the old instance

A PL replacement can remove the device while a process still holds a file descriptor or mapping. Reusing the same physical address for a new peripheral does not make the old handle valid. The driver and application must stop work, release resources and establish a new instance.

A raw userspace mapping is especially difficult to revoke safely. If the product allows DFX, prefer an interface that can reject new requests and coordinate buffer lifetime. Prevent reconfiguration while unrevocable mappings remain in use, or implement a documented alternative.

## Diagnose from the lowest confirmed boundary

No device binding suggests a description or matching problem. A probe that defers suggests a supplier dependency. An identity mismatch suggests the wrong design or register contract. Correct register access with no completion suggests interrupt, DMA or functional protocol. A failure only after reconfiguration points to lifetime and stale-state handling.

These observations narrow the next investigation. Repeated arbitrary register reads do not add reliable evidence and can make the original failure harder to reproduce.

## References

- [Teaching driver and explicit synthetic contract](../14-kernel-modules-and-drivers/04-linux-device-driver-model.md).
- [linux-xlnx@xilinx-v2024.1:Documentation/devicetree/overlay-notes.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/devicetree/overlay-notes.rst).
- [DMA API ordering and ownership](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/core-api/dma-api-howto.rst).

- `linux-xlnx@xilinx-v2024.1:Documentation/devicetree/bindings/`
- [Interrupts and GIC](../03-zynqmp-architecture/08-interrupts-and-gic.md)

---

<sub>← [Hardware Handoff: From Vivado to Linux](01-hardware-handoff.md) · [Chapter index](README.md) · [Linux FPGA Manager](03-fpga-manager.md) →</sub>
