# Xilinx Device Tree Generator (DTG)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree

## From hardware export to source

AMD's Device Tree Generator (DTG) uses the hardware description and generation scripts to produce software-facing hardware nodes. The XSA describes exported design information; external board components and product choices may still need user additions.

| Generated input | Typical purpose |
| --- | --- |
| `system-top.dts` | Top-level include structure |
| `pl.dtsi` | Programmable-logic devices |
| `pcw.dtsi` | Processing-system configuration |
| `zynqmp.dtsi` | SoC devices and shared definitions |
| `zynqmp-clk-ccf.dtsi` | Clock-related description |
| Board include | Board wiring and external components |

The exact include set depends on the flow. Inspect the generated top-level file instead of assuming every filename appears in every project.

## User changes

Keep additions in `system-user.dtsi` or maintained recipe inputs. Override the smallest necessary property. Regenerating hardware files should not erase your only copy of a board change.

After importing a new XSA, compare addresses, interrupts, clocks and node names. A generated tree can compile while still describing hardware that does not match the loaded bitstream.

## References

- `device-tree-xlnx@xilinx_v2024.1`, generation scripts
- `xilinx-zcu106-2024.1:components/plnx_workspace/device-tree/`
- AMD UG1144 (2024.1), device-tree generation

---

<sub>← [Bindings and Driver Matching](02-bindings-and-driver-matching.md) · [Chapter index](README.md) · [System Device Tree and Lopper](04-system-device-tree-and-lopper.md) →</sub>
