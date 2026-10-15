# PCIe

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Link and enumeration

PCIe requires valid reference clocks, reset timing, lane configuration and compatible root-port/endpoint roles. Link training happens before normal device enumeration. A missing device can therefore be a hardware/link problem rather than a driver issue.

PS PCIe and PL PCIe IP use different integration paths. XDMA and QDMA platforms have their own drivers and hardware contracts; do not apply their register layouts to the PS controller.

## Debugging

Use `lspci` to inspect discovered devices and resources. Check link width/speed and error reporting where supported. `setpci` writes configuration space and can change active device behavior; avoid unexplained writes from unrelated tutorials.

DMA-capable endpoints need correct address mapping, IOMMU policy and buffer ownership. Enumeration success does not validate DMA or reset recovery.

> [!NOTE]
> **Not run on the reference setup:** physical PCIe link training, endpoint DMA and reset tests.

## References

- UG1085 (v2.5), PCIe and PS-GTR sections
- Linux 6.6 PCI and DMA documentation

---

<sub>← [USB Host and Gadget](03-usb.md) · [Chapter index](README.md) · [I2C, SPI, UART, CAN and GPIO](05-low-speed-buses.md) →</sub>
