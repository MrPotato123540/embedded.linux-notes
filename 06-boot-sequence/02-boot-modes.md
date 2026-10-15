# Boot Modes

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Boot-mode selection

The BootROM uses the latched mode-pin value to select its initial boot interface. The following encodings come from UG1085 (v2.5), Table 11-1. Values are binary `MODE[3:0]`, not board-switch positions.

| Mode | Value |
| --- | --- |
| PS JTAG | `0000` |
| QSPI, 24-bit addressing | `0001` |
| QSPI, 32-bit addressing | `0010` |
| SD0 | `0011` |
| NAND | `0100` |
| SD1 | `0101` |
| eMMC, 1.8 V | `0110` |
| USB0 | `0111` |
| PJTAG on MIO option 0 | `1000` |
| PJTAG on MIO option 1 | `1001` |
| SD1 with level shifter | `1110` |

The boot interface must match physical wiring, voltage and supported memory behavior. QSPI24 and QSPI32 differ in address handling. SD1-LS requires the appropriate level-shifter design.

## Primary and later storage

The primary device supplies the initial boot image. Later software can load remaining partitions or Linux from another device. For example, a board can start from QSPI and load its kernel or root filesystem from storage selected by U-Boot.

The boot-mode register and software override controls are separate from the physical switch. A software override must be interpreted with the reset type that makes it effective. Do not assume every reboot resamples the board pins.

## Board checks

Use the exact ZCU10x board guide or Kria carrier/SOM documentation to translate mode bits into switch settings. Switch numbering and ON polarity are board details. The reference QEMU capture reports `JTAG_MODE`; it does not validate a physical switch position.

> [!NOTE]
> **Not run on the reference setup:** physical mode-switch changes and runtime boot-mode overrides.

## References

- UG1085 (v2.5), Chapter 11, Table 11-1 and Boot Mode section
- [Clocks, power and reset](../03-zynqmp-architecture/07-clocks-power-and-reset.md)

---

<sub>← [Boot Flow at a Glance](01-boot-overview.md) · [Chapter index](README.md) · [Power-On Reset and the PMU ROM](03-power-on-reset-and-pmu-rom.md) →</sub>
