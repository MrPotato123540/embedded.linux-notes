# Error Management, Recovery and Watchdogs

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot


## Detection, action and recovery are separate designs

A watchdog detects missing progress by requiring a refresh before a deadline. Error-management logic receives hardware error indications and selects a response. Recovery software then tries to return the system to a usable state. Enabling one of these parts does not automatically produce a complete recovery design.

On ZynqMP, distinguish the watchdog used to supervise an A53/Linux subsystem from the PMU firmware's own watchdog support. Their refresh owners, reset scope and failure evidence differ. A Linux watchdog daemon cannot supervise a PMU callback that blocks the firmware scheduler in the same way that a PMU watchdog can.

The pinned implementation is under `lib/sw_apps/zynqmp_pmufw/src`, especially `xpfw_mod_em.c`, `xpfw_mod_wdt.c` and `xpfw_config.h`. Read the feature guards before assuming any handler is active in the deployed image.

## What the source defaults establish

The tagged configuration defaults set `ENABLE_EM_VAL`, `ENABLE_RECOVERY_VAL`, `ENABLE_ESCALATION_VAL` and `ENABLE_WDT_VAL` to zero. Other compile flags or board-specific conditions can enable them. This means that “the PMU firmware is present” is not evidence that all these recovery features are active.

The PMU watchdog configuration defines a default timeout of 90 milliseconds and longer 500-millisecond settings for several specific operations. In `xpfw_mod_wdt.c`, the periodic refresh interval is 50 milliseconds. These are source values, not a measurement of a running board's exact expiry time.

The watchdog count calculation uses the input clock, prescaler and a shift when programming the counter. Integer rounding and hardware timing affect the final interval. An old nearby source comment mentioning a different duration is weaker evidence than the active expression and configuration value.

## Follow the PMU watchdog refresh path

When included, the watchdog module creates its module object and installs a configuration handler. Initialization finds the watchdog configuration, initializes the driver, programs the counter and schedules the refresh callback. `XPfw_WdtRestart()` calls the watchdog driver's refresh function.

The callback runs through the firmware scheduler. Therefore, scheduler progress is part of the watchdog's health condition. A custom task that blocks for longer than the available margin can cause expiry even if the main processor is healthy.

As an arithmetic illustration, a nominal 90-millisecond timeout and a 50-millisecond refresh interval leave only a nominal 40-millisecond gap after a refresh becomes due. That is not a safe execution budget by itself. Interrupt delays, task ordering, clock tolerance and counter quantization also consume margin. Measure the worst case under the real build.

## Error events reach policy handlers

The error-management module registers handlers for platform error events. Its event handler reads the relevant error state and selects configured actions. The source includes handlers such as `SwdtHandler()` and `RpuLsHandler()`, but the compiled behavior depends on enabled features and action settings.

An error bit is evidence of a detected condition, not automatically its root cause. A bus fault can follow a powered-off target, an illegal access or a failing device. Preserve the first status and the operating context before a reset removes the evidence.

The software-watchdog action configuration also changes with recovery support. In the inspected header, `SWDT_EM_ACTION` selects a custom action when `ENABLE_RECOVERY` is enabled; otherwise its default selects system reset behavior. Review the actual handler and reset scope before enabling this in a product.

## Recovery scope determines what must survive

An APU-subsystem restart can leave other processors running. A processing-system reset and a full system reset affect a wider set of state. The correct choice depends on which resources are shared and which failure is being contained.

Suppose Linux owns a DMA-capable device and the A53 subsystem restarts while another processor continues running. The device must not keep writing into memory that the new Linux instance will reuse. Recovery needs device quiescing or reset, memory ownership rules and a clean reinitialization path. Restarting the CPU alone does not solve that problem.

Escalation adds another state machine: if a narrow restart repeatedly fails, a wider reset may follow. Define what counts as a healthy boot, how the attempt count is retained, and when it is cleared. Otherwise, a system can loop forever or erase the evidence on every attempt.

## A meaningful watchdog test

A useful test begins with a known refresh owner and a recorded timeout. First prove normal refresh under the intended workload. Then stop the intended progress source in a controlled test and observe the expiry indication, selected reset action and next boot's reset cause.

Do not use a busy loop without checking what it actually blocks. A userspace loop may leave the watchdog daemon running. A kernel deadlock can leave some interrupt paths alive. A PMU scheduled callback blockage tests a different failure boundary again.

Record the first failing progress marker, the reset source, elapsed time and recovered services. “The board rebooted” is insufficient: a brownout, external reset or unrelated watchdog could produce the same visible result.

## Debugging repeated resets

If resets begin only after adding a PMU module, compare its worst callback duration with the watchdog path. If resets occur during long security or FPGA operations, inspect the operation-specific timeout handling. If recovery starts but fails before Linux, inspect FSBL restart handling and the retained hardware state.

If the wrong subsystem resets, inspect error-action policy before changing the watchdog period. A longer timeout cannot correct the wrong reset target. If the system repeatedly restarts after apparent success, inspect healthy-boot acknowledgement and retained attempt state.

> [!NOTE]
> **Not run on the reference setup:** watchdog expiry, hardware error injection, APU recovery and escalation. These tests change live system state and require a controlled physical test plan; the values above are pinned source observations.

## References

- [2024.1 PMU watchdog implementation](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_pmufw/src/xpfw_mod_wdt.c).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/{xpfw_mod_em.c,xpfw_config.h,xpfw_core.c}`.
- [FSBL debugging and reset evidence](../08-fsbl/05-fsbl-debugging.md).

---

<sub>← [Customizing PMU Firmware](05-pmufw-customization.md) · [Chapter index](README.md) · Next chapter: [10 · Trusted Firmware-A (BL31)](../10-trusted-firmware-a/README.md) →</sub>
