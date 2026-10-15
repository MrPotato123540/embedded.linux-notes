# Processing System (PS) and Programmable Logic (PL)

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-03](../ROADMAP.md#wp-03). The outline below is the agreed scope and will be replaced by the full text.

**[03 · Zynq UltraScale+ MPSoC Architecture](README.md)** · Part II: Zynq UltraScale+ MPSoC Hardware

## Planned content

- What lives in the PS and what lives in the PL
- PS-PL AXI interfaces: `M_AXI_HPM0/1_FPD`, `M_AXI_HPM0_LPD`, `S_AXI_HP0-3_FPD`, `S_AXI_HPC0/1_FPD`, `S_AXI_ACP_FPD`, `S_AXI_ACE_FPD`, `S_AXI_LPD`
- PL clocks (`pl_clk0-3`), resets (`pl_resetn`), PL-to-PS interrupts, EMIO
- The PL power domain and what happens while the PL is not configured
- Choosing the right port: bandwidth, latency, coherency

---

<sub>← [Device Family Overview](01-device-family-overview.md) · [Chapter index](README.md) · [Processing Units: APU, RPU, PMU, CSU, GPU and VCU](03-processing-units.md) →</sub>
