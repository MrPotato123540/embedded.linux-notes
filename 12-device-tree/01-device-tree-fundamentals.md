# Device Tree Fundamentals

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree

## Data describing hardware

A device tree describes hardware that software cannot discover automatically. **DTS** is source text, **DTSI** is included source, **DTB** is the compiled binary, and **DTC** is the compiler. The tree does not create hardware or implement a driver.

A node contains properties and child nodes. Its unit address normally identifies its first address on the parent bus. Labels are source references; phandles connect compiled nodes. A numeric phandle is not a stable identifier across builds.

| Property | Interpretation |
| --- | --- |
| `compatible` | Ordered hardware compatibility identifiers |
| `status` | Availability of the device |
| `reg` | Address/size tuples in the parent bus format |
| `#address-cells`, `#size-cells` | Number of cells in child address/size fields |
| `ranges` | Translation between bus and parent addresses |
| `interrupts`, `clocks`, `resets`, `gpios` | References encoded according to provider bindings |
| `power-domains` | Managed power dependency |

`/memory` describes RAM. `/reserved-memory` keeps ranges out of ordinary allocation. `/chosen` carries boot information. `/aliases` provides selected stable aliases.

## Pitfall

A two-cell address is not two separate addresses. Decode the tuple using the parent binding before comparing it with the hardware map.

## References

- [Devicetree Specification](https://www.devicetree.org/specifications/)
- `linux-xlnx@xilinx-v2024.1:arch/arm64/boot/dts/xilinx/zynqmp.dtsi`

---

<sub>[Chapter index](README.md) · [Bindings and Driver Matching](02-bindings-and-driver-matching.md) →</sub>
