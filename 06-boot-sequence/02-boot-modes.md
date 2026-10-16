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

## Decode the mode before interpreting the board switches

The mode table describes logic values at the device interface. A board manual translates those values into switch positions, pull resistors and signal names. Switch labels can be reversed relative to bit numbering, and an ON position can pull a signal low. Copying a photograph from another board revision is therefore unreliable.

Identify the exact board and revision, then trace each relevant switch to its mode bit. Record the resulting binary value and the reset used for the test. This produces an unambiguous report that another engineer can compare with the device manual.

The selected mode controls the initial boot path. It does not force every later stage to use the same medium. A QSPI boot can start U-Boot, which then loads Linux over the network or from eMMC. Linux can then mount a root filesystem from yet another source. Name all three choices when describing a product's boot flow.

## Boot interface and runtime device support are separate

BootROM has a fixed set of supported interfaces and procedures. Linux drivers are later software with different capabilities. A storage device working under Linux does not prove that BootROM can use it in the selected mode. Similarly, a bootable SD device does not prove the kernel has the required controller and filesystem drivers to mount it as root.

For QSPI, the mode distinction includes address handling. Flash geometry, addressing behavior and the board connection must match the supported boot flow. Do not treat the 24-bit and 32-bit modes as interchangeable settings chosen only by the size of the file you want to store.

For SD/eMMC, wiring, voltage and controller selection matter. The table's SD1 level-shifter mode expresses a hardware condition, not a general software workaround for an unreadable card. Verify the board design before changing that mode.

## Reset scope affects the experiment

Mode values are latched according to the device's reset behavior. A warm reboot is not automatically equivalent to a full power-on reset. Software overrides and retained state can also affect what the next boot sees.

When a mode change appears ineffective, record whether you changed physical straps, a software override or both. Then check which reset makes that change effective. Repeatedly rebooting Linux cannot substitute for the required hardware reset event.

This distinction also matters during debugging. A debugger can initialize registers and memory before continuing execution. The resulting boot may succeed even if the cold-start path is wrong. Always repeat the final validation from the reset condition the product will experience.

## Interpret U-Boot's boot-mode report

The saved reference log reports `JTAG_MODE`. The QEMU launch uses loader devices to place firmware and OS inputs into memory. This gives a concrete example of a later stage reporting a mode while the host tool supplies much of the loading work.

The report is useful, but it is not a photograph of board straps and does not prove a physical JTAG cable sequence. Read it together with the launch command. Likewise, a board report should be correlated with reset state and bootloader source rather than treated as the only evidence of physical switch settings.

## A controlled storage-boot diagnosis

First confirm that the device selected the intended primary interface. Next confirm the physical connection and supported medium behavior. Then inspect the boot image's presence, location and format. Only after the initial firmware runs should you move to later bootloader file selection.

If FSBL appears but U-Boot cannot find the kernel, the mode selection has already achieved part of its job. Investigate the selected device, partition and script at the U-Boot stage. If no firmware output appears, the problem may still be power, reset, console configuration or initial image processing; mode straps are one candidate among several.

For a design with a recovery image, verify how boot-mode selection interacts with multiboot and fallback. A recovery path stored on an unavailable primary interface cannot help until that interface works. A later U-Boot recovery policy cannot repair a failure that prevents U-Boot from executing.

**Validation boundary:** this is a device/board review procedure. Physical switch positions, voltage levels and reset sampling were not tested on the reference QEMU system. Use UG1085 and the exact board guide for those facts.

## References

- UG1085 (v2.5), Chapter 11, Table 11-1 and Boot Mode section
- [Clocks, power and reset](../03-zynqmp-architecture/07-clocks-power-and-reset.md)

---

<sub>← [Boot Flow at a Glance](01-boot-overview.md) · [Chapter index](README.md) · [Power-On Reset and the PMU ROM](03-power-on-reset-and-pmu-rom.md) →</sub>
