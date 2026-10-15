# Error Management, Recovery and Watchdogs

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot

## Detection, recovery and escalation

An error source reports a condition. An error manager chooses an action. Recovery tries to restore service; escalation chooses a stronger action when recovery fails. These are separate policies and must be designed together.

A watchdog detects missing progress only if the system that feeds it represents meaningful health. Feeding it from an always-running timer can hide a dead application. Conversely, a timeout shorter than valid worst-case work can cause repeated resets.

## ZynqMP reset scope

The platform has watchdog and reset resources associated with different domains. A system restart and a PS-only restart do not affect every resource in the same way. Select the reset scope according to the fault and the state that must be cleared.

Before enabling automatic recovery, preserve error status and a restart reason in a durable diagnostic path. Test repeated failures so an escalation loop does not make recovery impossible.

> [!NOTE]
> **Not run on the reference setup:** physical watchdog expiry, error injection or reset escalation. QEMU boot success is not a safety validation.

## References

- UG1085 (v2.5), error management, watchdogs and reset
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/`
- [Field diagnostics](../23-storage-updates-and-production/06-reliability-and-field-diagnostics.md)

---

<sub>← [Customizing PMU Firmware](05-pmufw-customization.md) · [Chapter index](README.md) · Next chapter: [10 · Trusted Firmware-A (BL31)](../10-trusted-firmware-a/README.md) →</sub>
