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

## Separate electrical readiness from software readiness

Before a processor can execute the first useful instruction, its power and clock conditions must be valid and reset must be released correctly. Software logs begin only after several of these conditions already hold. A silent UART is therefore an observation at the end of a chain, not proof that the first software stage is defective.

For a custom board, use the schematic and power-sequencing requirements to identify the relevant rails, reference clocks and reset signals. Measure them with suitable equipment and record timing. A debugger connection can confirm some digital behavior, but it cannot establish power integrity or clock quality under load.

Do not use Linux configuration changes to compensate for an unexplained reset-time failure. Linux has not started at that point. First establish which hardware domain and processor are alive and which stage has actually been reached.

## PMU ROM and PMU firmware have different roles

PMU ROM is fixed early code associated with the platform's startup path. PMU firmware is a separately built program loaded later in the supported boot arrangement. The firmware adds runtime platform-management behavior and can be configured or replaced as part of the software release.

This distinction matters when reading logs. A PMU ROM version and a PMU firmware version describe different components. A successful firmware banner does not mean the programmable firmware performed every earlier ROM operation. Conversely, an early platform startup failure may occur before the replaceable firmware is running.

Built-in self-test and repair terms describe hardware-supported procedures. Their use depends on the device and configuration. Do not infer a production test result from a normal boot banner or from an emulator. Physical memory and logic reliability need the appropriate hardware validation.

## Reset types define what remains

A power-on reset, a system reset and a narrower subsystem reset affect different scopes. Some registers, memories or peripherals may retain state across a limited reset. The resulting system can behave differently from a completely cold start even when the same software files are used.

Consider a driver that depends on a clock or reset sequence. A warm boot might inherit a useful state from the previous run and hide a missing initialization step. A cold boot removes that accidental help. The reverse can also occur: retained error or watchdog state can make a warm restart fail while a full power cycle succeeds.

Record reset scope as part of every reproducible failure report. “Rebooted the board” is too vague when the failure depends on retained state.

## Preserve reset and error evidence early

Reset-reason and error-status registers can help classify the event. Their interpretation requires the exact register definition, reset value and clear behavior. Some status can be changed by later firmware or by another reset, so capture it before modifying the system further.

A watchdog indication tells you that a watchdog-related event occurred. It does not by itself tell you why software failed to service the watchdog. The original cause can be a deadlock, a long interrupt-disabled interval, a lost clock or an intentional recovery policy. Correlate status with the last log, watchdog ownership and elapsed time.

Likewise, an error flag can be a consequence of an earlier failure. Preserve the full status set and its capture time rather than reporting only one decoded bit. Avoid writing to status registers during initial diagnosis unless the documented procedure requires it.

## Use a staged investigation

| Observation | Next evidence | What remains unproven |
| --- | --- | --- |
| Rails and clocks are valid | Reset waveform and strap levels | Boot image readability |
| Debug interface responds | Target/reset status and program counter | Correct firmware initialization |
| Early firmware prints | Stage and error information | Correct DDR operation |
| U-Boot runs | Memory map and selected boot inputs | Linux and peripheral correctness |
| Warm boot works only | Cold/warm state comparison | Which initialization dependency is missing |

The table is an investigation order, not a guarantee that every board exposes all these observations. Security configuration can restrict debug access. Production diagnosis must use the permitted interfaces for that device.

## QEMU's useful limit

QEMU helps test software sequencing and some platform interfaces. It supplies a model of memory and devices rather than the board's analog behavior. A successful emulator boot cannot validate supply ramp timing, oscillator startup, DDR training margins or reset wiring.

Use the emulator result to narrow software hypotheses, then test the electrical and silicon-dependent requirements on the real board. Keep the two evidence sets separate in the release report. This section adds the reasoning needed to choose those tests; it does not claim they have been performed.

## References

- UG1085 (v2.5), PMU, reset and Boot and Configuration chapters
- [Reset diagnosis](../03-zynqmp-architecture/07-clocks-power-and-reset.md)

---

<sub>← [Boot Modes](02-boot-modes.md) · [Chapter index](README.md) · [CSU BootROM](04-csu-bootrom.md) →</sub>
