# FSBL Debugging

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot

## Start with stage evidence

Enable enough FSBL logging to identify the last completed operation. Confirm the UART instance, pin routing and console parameters before interpreting silence as a crash. A log can stop because the next stage uses another UART.

Decode errors using `xfsbl_error.h` from the same source revision. Preserve both the numeric code and the surrounding messages. A partition-load error can originate in media access, image metadata, security processing or destination memory.

## JTAG investigation

Use the exact FSBL ELF for symbols. Break at entry, the failing stage and the handoff path. Inspect the return status and relevant memory only after confirming the processor and address view.

A debugger can alter timing and retain state across runs. Validate a correction again from cold boot without breakpoints. If DDR initialization is suspect, first confirm the design export and board memory settings instead of changing random delay values.

## Evidence checklist

Keep the source revision, hardware revision, compiler flags, ELF hash, link map, BIF and serial log together. That set makes a boot failure reproducible for another engineer.

> [!NOTE]
> **Not run on the reference setup:** physical JTAG stepping and a deliberately failing FSBL image.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_error.h`, `xfsbl_debug.h`
- AMD UG1400 (2024.1), debugging standalone applications

---

<sub>← [Customizing the FSBL](04-fsbl-customization.md) · [Chapter index](README.md) · Next chapter: [09 · PMU and PMU Firmware](../09-pmu-firmware/README.md) →</sub>
