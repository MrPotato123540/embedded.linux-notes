# Ethernet (GEM)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## MAC, PHY and board link

A GEM Ethernet controller provides the MAC side. A PHY handles the external link. MDIO manages the PHY; RGMII or SGMII carries the data connection according to the board design.

The device tree must identify the PHY or fixed-link arrangement and the correct interface mode. RGMII delay placement is especially important: both missing and duplicated delays can cause packet errors even when link negotiation succeeds.

## Debugging order

Check power/reset and clocks, PHY discovery, negotiated link, packet counters, IP configuration and finally application traffic. `ethtool` can expose link settings and driver statistics. A successful ping is a basic check, not a throughput or error-rate test.

PL Ethernet uses its own IP, DMA and driver requirements. Do not assume it has the same settings as a PS GEM interface.

> [!NOTE]
> **Not run on the reference setup:** physical Ethernet timing and load tests. Saved QEMU networking does not validate a board PHY.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/net/ethernet/cadence/`
- UG1085 (v2.5), GEM and pin-routing chapters

---

<sub>[Chapter index](README.md) · [Network Configuration on the Target](02-network-configuration.md) →</sub>
