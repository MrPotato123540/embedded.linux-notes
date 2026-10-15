# Power-On Reset and the PMU ROM

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Reset before software

Power-on reset starts before the FSBL can print anything. Supply sequencing, reference clocks and reset signals must be valid before software diagnosis becomes useful.

`PS_POR_B` and `PS_SRST_B` have different purposes. A system reset is not a substitute for a complete power-on reset. Some state can survive a narrower reset, so reproduce a failure with the reset type recorded.

The PMU ROM performs early platform work and coordinates the release of the CSU. Its responsibilities include initialization and supported self-test/repair sequences. BISR means **Built-In Self-Repair**; LBIST means **Logic Built-In Self-Test**. Their actual use depends on the device and boot configuration.

## Diagnosis

For a silent board, check power-good signals, clock presence, reset deassertion and boot-mode straps before changing Linux. If JTAG is available, inspect the reset and error status using the documented registers. Save their values before a later stage clears or changes them.

A reset-reason value only describes the recorded hardware state. It does not by itself identify the faulty software component. Correlate it with watchdog configuration and the last serial output.

> [!NOTE]
> **Not run on the reference setup:** power sequencing, physical reset timing and silicon self-test behavior. QEMU cannot establish that these electrical conditions are correct.

## References

- UG1085 (v2.5), PMU, reset and Boot and Configuration chapters
- [Reset diagnosis](../03-zynqmp-architecture/07-clocks-power-and-reset.md)

---

<sub>← [Boot Modes](02-boot-modes.md) · [Chapter index](README.md) · [CSU BootROM](04-csu-bootrom.md) →</sub>
