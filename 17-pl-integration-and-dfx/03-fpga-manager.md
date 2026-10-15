# Linux FPGA Manager

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Framework and platform driver

The Linux FPGA-manager framework separates common programming control from device-specific loading. On ZynqMP, the platform driver uses the supported firmware path to configure the PL. Manager state describes the programming operation; it does not verify the application behavior of the loaded design.

A firmware file must have the format expected by the loader. Use supported bitstream conversion, full/partial flags and a matching device-tree description. Do not infer readiness from the filename.

## Runtime sequence

Stop users of the affected hardware, complete or cancel DMA, isolate the region as required, load the bitstream, then activate matching devices and applications. `fpgautil` and vendor packaging can coordinate supported operations, but their command syntax and available interfaces depend on the release.

A generic writable sysfs loading interface is not guaranteed by the upstream manager API. Check the actual vendor implementation before copying a sysfs command.

> [!NOTE]
> **Not run on the reference setup:** full bitstream loading through Linux on hardware.

## References

- Linux 6.6 [FPGA manager](https://docs.kernel.org/6.6/driver-api/fpga/fpga-mgr.html)
- `linux-xlnx@xilinx-v2024.1:drivers/fpga/zynqmp-fpga.c`

---

<sub>← [Accessing PL Peripherals From Linux](02-accessing-pl-peripherals.md) · [Chapter index](README.md) · [DFX: Dynamic Function eXchange](04-dfx-dynamic-function-exchange.md) →</sub>
