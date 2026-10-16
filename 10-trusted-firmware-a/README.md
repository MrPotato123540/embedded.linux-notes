# 10 · Trusted Firmware-A (BL31)

**Part IV: Boot** · Work package [WP-10](../ROADMAP.md#wp-10) · Status: 👀 In review

TF-A (formerly ATF) on ZynqMP: the EL3 runtime that provides PSCI, forwards platform management calls and hosts secure services.

**Prerequisites:** [03 · Zynq UltraScale+ MPSoC Architecture](../03-zynqmp-architecture/README.md) · [06 · Boot Sequence](../06-boot-sequence/README.md)

All four sections now cover source-level handoff, runtime services, measured BL31 sections, build-dependent placement and OP-TEE call lifetimes. No new Secure payload, relocated firmware or physical isolation test is claimed.

## Sections

| # | Section | Status |
| ---: | --- | --- |
| 1 | [TF-A Overview](01-tfa-overview.md) | 👀 In review |
| 2 | [BL31 on ZynqMP](02-bl31-on-zynqmp.md) | 👀 In review |
| 3 | [Building and Customizing TF-A](03-tfa-customization.md) | 👀 In review |
| 4 | [BL32 and OP-TEE (Overview)](04-op-tee-overview.md) | 👀 In review |

---

<sub>← [09 · PMU and PMU Firmware](../09-pmu-firmware/README.md) · [Guide contents](../README.md#contents) · [11 · U-Boot](../11-u-boot/README.md) →</sub>
