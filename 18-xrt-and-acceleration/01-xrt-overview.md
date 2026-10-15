# XRT Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[18 · XRT and Hardware Acceleration](README.md)** · Part VIII: Programmable Logic and Acceleration

## XRT components

**Xilinx Runtime (XRT)** connects a host application with supported programmable-logic accelerators. On embedded platforms, userspace libraries cooperate with the `zocl` kernel driver and platform firmware.

An `xclbin` contains accelerator configuration and metadata. The metadata describes information needed to load and use the compiled design. It must match the platform; a runtime library cannot make an incompatible hardware design work.

## Programming models

The native XRT API exposes devices, kernels, runs and buffer objects. OpenCL provides another programming model where supported by the selected release. Keep application API use consistent with the installed runtime and build tools.

The runtime is not the accelerator itself. Compute behavior still comes from the hardware kernel and its interface contract. Check argument order, widths, memory groups and synchronization.

## References

- [XRT 2024.1 documentation](https://xilinx.github.io/XRT/2024.1/html/index.html)
- AMD XRT source and embedded `zocl` driver

---

<sub>[Chapter index](README.md) · [Embedded Platforms for Acceleration](02-embedded-platforms-for-acceleration.md) →</sub>
