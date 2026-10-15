# Custom Board Bring-Up

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## Bring-up order

Start with power rails, clocks, reset and boot straps. Then establish UART or JTAG visibility. Validate processor initialization and DDR before adding a complex Linux image.

Use a hardware export for the actual board, including memory and pin settings. An evaluation-board BSP may provide useful software structure, but its electrical assumptions are not a custom-board specification.

## Controlled progression

Boot a minimal known image, confirm storage and console, then add peripherals one at a time. For each peripheral, verify power/reset, clocks, pin routing, device-tree description, driver binding and real traffic.

Keep a bring-up log with board revision, rework, firmware versions and measured signals. Separate failures that reproduce after cold power-on from those requiring warm reset or sustained load.

> [!NOTE]
> **Not run on the reference setup:** custom-board electrical and peripheral validation.

## References

- UG1085 (v2.5), reset, clocks, memory and boot
- Device data sheet and the actual board schematic

---

<sub>← [QEMU Emulation](02-qemu-emulation.md) · [Chapter index](README.md) · [DDR Bring-Up and Memory Testing](04-ddr-bring-up.md) →</sub>
