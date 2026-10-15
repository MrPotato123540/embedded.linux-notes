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

## References

- `linux-xlnx@xilinx-v2024.1:Documentation/devicetree/bindings/`
- [Interrupts and GIC](../03-zynqmp-architecture/08-interrupts-and-gic.md)

---

<sub>← [Hardware Handoff: From Vivado to Linux](01-hardware-handoff.md) · [Chapter index](README.md) · [Linux FPGA Manager](03-fpga-manager.md) →</sub>
