# Custom Board Bring-Up

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## Bring-up is a sequence of evidence gates

A custom board combines power, clocks, reset, memory, boot storage, pin routing and software. A late Linux error can be caused by an earlier electrical or initialization error. Build a sequence in which each stage proves a smaller contract before the next stage depends on it.

Start with the exact board revision, assembly options and component population. A schematic revision alone is not enough if pull resistors, oscillators or memory parts differ on the assembled unit. Keep the hardware export and software artifacts linked to that board identity.

An evaluation-board BSP is a useful reference for software structure. It is not a safe default for custom DDR timing, MIO voltage, PHY reset or boot-storage layout. The SoC family can match while the board-level assumptions are completely different.

## Establish power, reset and clock behavior first

Before executing complex software, verify the required rails, sequencing, reset release and reference clocks with appropriate instruments and board documentation. A JTAG connection or one UART message does not validate every power domain or operating condition.

Observe cold power-on and warm reset separately. A component initialized by an earlier debug session can retain state across a warm reset. A design that works only after JTAG initialization has not demonstrated autonomous cold boot.

Document measured values and tolerances from the component specifications. This section does not invent universal rail values or timing limits: those come from the selected device, board power design and current AMD electrical documentation.

## Use the smallest useful software path

First establish a reliable console or debug observation from memory that does not depend on unproven DDR. Then validate processing-system initialization and DDR. Only after that should a larger bootloader or Linux image rely on external memory.

The 2024.1 FSBL path calls `XFsbl_HookPsuInit()` during initialization. The local hardware export supplies `psu_init.c` and related generated files. If dynamic DDR support is enabled, the inspected FSBL also has an `XFsbl_DdrInit()` path. The generated design and build configuration determine which initialization applies.

This source-level path gives a concrete place to compare the hardware export with the binary. A new XSA file does not update an already built FSBL by itself. Rebuild and identify the firmware that actually contains the new initialization data.

## Keep one memory map for the complete system

List bootloader relocation, firmware, kernel, initramfs, device tree, reserved memory, RPU regions, DMA pools and any PL-accessible windows. Include file load addresses, runtime addresses and sizes. Label each address space and lifetime.

For an original overlap example, a compressed kernel can fit below an initramfs at load time but expand into it during decompression. A map that records only file sizes misses the collision. Similarly, a remote ELF can require more memory than its file-backed segment bytes because of BSS, heap and stacks.

A Linux memory node should describe usable physical memory accurately. Reserved regions then exclude areas owned by other components. Reporting more DDR than is physically present can produce a system that boots and fails only when allocations reach the nonexistent range.

## Bring up one peripheral dependency chain

For Ethernet, follow controller clock/reset, pin route, PHY power/reset, management address, MAC/PHY interface mode and network configuration. For SD/eMMC, follow power, bus width, voltage, clocking, detect/reset signals and image layout. For a PL device, include bitstream configuration and interconnect/reset/clock readiness before driver access.

Do not enable every possible peripheral in the first device tree. A node can cause a driver to access unpowered or unimplemented hardware and obscure the first failure. Add devices in controlled groups with a recorded acceptance test.

The final board description should still be complete for its intended use. Minimal bring-up is a diagnostic stage, not permission to leave required clocks, regulators or reset relationships undocumented in the production tree.

## Device-tree and hardware-export changes have different scopes

A device-tree edit can describe a peripheral, its resources and dependencies. It cannot change the MIO pin mux already established by early firmware or create a PL IP block missing from the bitstream. A hardware-export change can require regenerated initialization and rebuilt software as well as a new DTB.

For example, moving a UART route can affect early console output before Linux reads its device tree. Updating only the Linux `stdout-path` may leave FSBL and U-Boot on the old path. Review every boot stage that uses the peripheral.

Keep board-specific changes in tracked project files rather than editing generated output without a regeneration rule. A clean import/build should reproduce the intended configuration. If a generated file needs a temporary diagnostic edit, record it as temporary evidence and move the final correction to its source.

## Use failure signatures to choose the next test

A completely silent board calls for power/reset/boot-mode and console-path checks before kernel debugging. Early firmware that stops during DDR setup calls for memory initialization evidence. U-Boot that runs but cannot read storage calls for controller, media and layout checks. Linux that starts but cannot mount root calls for the actual command line and required driver/filesystem availability.

A failure that moves when logging is added can indicate timing, stack use or memory corruption. A failure that tracks temperature or clock rate can indicate margin. A failure tied to one artifact revision suggests software/configuration provenance. These are hypotheses to test, not automatic diagnoses.

Avoid changing power, DDR rate, boot image and device tree at once. Preserve the last known state and change one contract so the result has explanatory value.

## Acceptance includes repeated and unattended operation

After a controlled successful boot, test unattended cold starts, warm resets and recovery paths. Exercise required peripherals concurrently, because shared clocks, memory bandwidth and reset domains can reveal conflicts absent in isolated tests.

Record board sample count and environmental conditions. One prototype at room temperature does not establish production margin. Keep hardware-validation limits explicit while software integration progresses.

> [!NOTE]
> **Not run on the reference setup:** custom-board electrical measurements, cold boot, DDR validation and peripheral acceptance. FSBL and generated initialization sources were inspected; this is a proposed bring-up method, not a board qualification report.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_initialization.c`, inspected PSU and optional dynamic-DDR paths.
- Inspected `xilinx-zcu106-2024.1:project-spec/hw-description/` and hardware-export artifacts.
- AMD UG1085, *Zynq UltraScale+ Device Technical Reference Manual*, boot, clock/reset and memory architecture; board electrical limits require the matching data sheet.

---

<sub>← [QEMU Emulation](02-qemu-emulation.md) · [Chapter index](README.md) · [DDR Bring-Up and Memory Testing](04-ddr-bring-up.md) →</sub>
