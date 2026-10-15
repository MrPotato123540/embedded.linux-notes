# BL31 on ZynqMP

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot

## Platform services

The ZynqMP port lives under `plat/xilinx/zynqmp`. Platform setup prepares the runtime environment and interprets the FSBL handoff information. Power-management code implements PSCI operations and platform-specific services.

The **Power State Coordination Interface (PSCI)** covers operations such as starting a CPU, CPU power-down, suspend and system reset. Platform-specific calls add functions outside that standard interface. Some calls communicate with PMU firmware through IPI.

## Memory placement

BL31 can use an appropriate OCM or DDR region. The reference `BOOT.BIN` places it at `0xFFFEA000`. That is an observed image address, not a requirement for every build.

A DDR placement needs memory reserved from Linux and other users. The ELF link address, load address, handoff metadata and reservation must agree. Debug builds can have a larger footprint and different placement requirements.

## Debugging

If a firmware service fails, identify whether the call reached TF-A, whether its function is supported and whether PMUFW accepted the request. A Linux error code may represent a lower-layer rejection.

> [!NOTE]
> **Not run on the reference setup:** relocation of BL31 and processor suspend/resume validation.

## References

- TF-A v2.10 ZynqMP documentation, memory placement and FSBL handoff
- `reference-setup/captures/bootgen-2024.1-read.txt`

---

<sub>← [TF-A Overview](01-tfa-overview.md) · [Chapter index](README.md) · [Building and Customizing TF-A](03-tfa-customization.md) →</sub>
