# 09 · PMU and PMU Firmware

**Part IV: Boot** · Work package [WP-09](../ROADMAP.md#wp-09) · Status: 👀 In review

The platform management unit: power, reset and error management, the EEMI interface, how to send requests to the PMU and how to extend its firmware.

**Prerequisites:** [03 · Zynq UltraScale+ MPSoC Architecture](../03-zynqmp-architecture/README.md) · [06 · Boot Sequence](../06-boot-sequence/README.md)

All six sections now follow PMU module dispatch, management-call packing, resource lifetimes, custom-service design and watchdog recovery in the pinned 2024.1 source. Physical power, IPI fault and watchdog tests remain open.

## Sections

| # | Section | Status |
| ---: | --- | --- |
| 1 | [PMU Overview](01-pmu-overview.md) | 👀 In review |
| 2 | [PMU Firmware Architecture and Source](02-pmufw-architecture-and-source.md) | 👀 In review |
| 3 | [EEMI and Platform Management](03-eemi-and-platform-management.md) | 👀 In review |
| 4 | [Communicating With the PMU](04-communicating-with-the-pmu.md) | 👀 In review |
| 5 | [Customizing PMU Firmware](05-pmufw-customization.md) | 👀 In review |
| 6 | [Error Management, Recovery and Watchdogs](06-error-management-and-watchdogs.md) | 👀 In review |

---

<sub>← [08 · First Stage Boot Loader (FSBL)](../08-fsbl/README.md) · [Guide contents](../README.md#contents) · [10 · Trusted Firmware-A (BL31)](../10-trusted-firmware-a/README.md) →</sub>
