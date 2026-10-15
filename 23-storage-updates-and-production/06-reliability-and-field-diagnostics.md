# Reliability and Field Diagnostics

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Keep useful failure evidence

Record image version, reset reason, uptime and the first relevant failure. Persistent logs need bounded storage and a policy for sensitive data. A crash dump without matching symbols has limited value.

Watchdogs should detect loss of meaningful progress. Define recovery scope and escalation: restart a service, reset a subsystem or reboot the device according to the fault. Avoid an endless reboot loop that prevents diagnostics or updates.

## Field design

Provide a controlled diagnostic interface, not a permanent unrestricted debug shell. Include counters for recoverable errors and enough context to distinguish hardware, network and software failures.

Test disconnected networking, full storage, damaged configuration and repeated resets. Diagnostics must continue to work when the main application is unhealthy.

> [!NOTE]
> **Not run on the reference setup:** product fault injection and long-duration reliability tests.

## References

- Linux 6.6 watchdog, pstore and kdump documentation
- [PMU error management](../09-pmu-firmware/06-error-management-and-watchdogs.md)

---

<sub>← [Boot-Time Optimization](05-boot-time-optimization.md) · [Chapter index](README.md) · [Licensing and Compliance](07-licensing-and-compliance.md) →</sub>
