# USB Host and Gadget

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Controller role and wiring

ZynqMP USB support uses the DWC3 controller path with platform-specific clocks, resets and PHY configuration. Host, peripheral and dual-role operation require suitable board wiring and device-tree settings. A connector shape alone does not establish the active role.

## USB gadgets

In peripheral mode, configfs can assemble supported gadget functions such as serial, Ethernet or mass storage. Create descriptors and functions, connect them to a configuration, then bind the gadget to the selected USB Device Controller.

A mass-storage backing file or device must not be written simultaneously by the target filesystem and the USB host. That can corrupt it even when both operating systems report successful writes.

## Diagnosis

Check role selection, cable, power, PHY/link state and enumeration before debugging the function protocol. Preserve host-side enumeration logs as well as target logs.

> [!NOTE]
> **Not run on the reference setup:** USB host/device enumeration and gadget traffic on hardware.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/usb/dwc3/`
- Linux 6.6 USB gadget/configfs documentation

---

<sub>← [Network Configuration on the Target](02-network-configuration.md) · [Chapter index](README.md) · [PCIe](04-pcie.md) →</sub>
