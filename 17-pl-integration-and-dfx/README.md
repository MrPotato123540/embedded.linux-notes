# 17 · PL Integration, FPGA Manager and DFX

**Part VIII: Programmable Logic and Acceleration** · Work package [WP-17](../ROADMAP.md#wp-17) · Status: 👀 In review

Using the programmable logic from Linux: hardware handoff, PL peripherals, the FPGA manager, Dynamic Function eXchange (partial reconfiguration), dfx-mgr and PS-PL DMA.

**Prerequisites:** [03 · Zynq UltraScale+ MPSoC Architecture](../03-zynqmp-architecture/README.md) · [12 · Device Tree](../12-device-tree/README.md) · [14 · Kernel Modules and Device Drivers](../14-kernel-modules-and-drivers/README.md)

All six sections now cover hardware/software compatibility, register protocols, the FPGA firmware load path, DFX state transitions, release-pinned dfx-mgr packaging and DMAengine source flow. Physical programming, isolation, DMA and recovery tests remain open. All sections remain **In review**; advanced draft coverage does not close the hardware validation work.

## Sections

| # | Section | Status |
| ---: | --- | --- |
| 1 | [Hardware Handoff: From Vivado to Linux](01-hardware-handoff.md) | 👀 In review |
| 2 | [Accessing PL Peripherals From Linux](02-accessing-pl-peripherals.md) | 👀 In review |
| 3 | [Linux FPGA Manager](03-fpga-manager.md) | 👀 In review |
| 4 | [DFX: Dynamic Function eXchange](04-dfx-dynamic-function-exchange.md) | 👀 In review |
| 5 | [dfx-mgr and Accelerator Packages](05-dfx-mgr.md) | 👀 In review |
| 6 | [DMA Between PS and PL](06-dma-between-ps-and-pl.md) | 👀 In review |

---

<sub>← [16 · Application Development](../16-application-development/README.md) · [Guide contents](../README.md#contents) · [18 · XRT and Hardware Acceleration](../18-xrt-and-acceleration/README.md) →</sub>
