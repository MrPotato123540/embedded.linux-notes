# Embedded Platforms for Acceleration

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[18 · XRT and Hardware Acceleration](README.md)** · Part VIII: Programmable Logic and Acceleration

## Platform agreement

A Vitis embedded platform combines hardware and software components. The hardware defines accelerator interfaces, clocks, memory and interrupts. The software image supplies the kernel driver, runtime libraries, firmware and application dependencies.

For PetaLinux, include the matching XRT and `zocl` support and verify the generated device-tree requirements. Enabling a packagegroup alone does not prove that the driver is bound or that memory resources are correct.

## Compatibility record

Record the hardware platform identifier, tool release, XRT version, kernel build and xclbin build. Test the platform with a known small accelerator before integrating a complex application.

Do not mix PCIe-card instructions with the embedded ZynqMP flow. Their drivers and device discovery differ even when the application-level API looks similar.

> [!NOTE]
> **Not run on the reference setup:** a Vitis platform build and accelerator deployment.

## References

- XRT 2024.1 embedded platform documentation
- Inspected `meta-petalinux@rel-v2024.1` Vitis acceleration packagegroup

---

<sub>← [XRT Overview](01-xrt-overview.md) · [Chapter index](README.md) · [Running Accelerated Applications](03-running-accelerated-applications.md) →</sub>
