# System Device Tree and Lopper

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree

## One system, several software views

A **System Device Tree (SDT)** describes resources across a system with multiple processors. Linux on the A53 and firmware on an R5 need different views of that system. Domain processing selects resources and produces descriptions for the intended software domain.

`sdtgen` generates system-level information from supported hardware inputs. **Lopper** processes trees and domain information. These tools do not automatically decide safe resource sharing: ownership of memory, interrupts and devices remains a design responsibility.

## Release boundaries

The inspected AMD layers include `meta-xilinx-core/gen-machine-conf/lib/gen-machineconf/sdt_flow.py` and Lopper support. Their presence does not mean a classic PetaLinux XSA project already uses that path. The file `device-tree-sdt.inc` mentioned in some other flows was not found in this BSP; do not assume it exists in the 2024.1 project.

Before changing flows, record the generator versions, input XSA, domain configuration and generated outputs. Compare the result with the existing device tree and firmware platform. A different domain view can remove a device that Linux previously owned.

> [!NOTE]
> **Not run on the reference setup:** an SDT domain-generation build in this continuation. Treat later-release tutorials as migration material until their tool requirements are checked.

## References

- Inspected `meta-xilinx@rel-v2024.1:meta-xilinx-core/gen-machine-conf/README.md` and `lib/gen-machineconf/sdt_flow.py`
- AMD [system-device-tree-xlnx](https://github.com/Xilinx/system-device-tree-xlnx)
- [Lopper project](https://github.com/devicetree-org/lopper)

---

<sub>← [Xilinx Device Tree Generator (DTG)](03-xilinx-device-tree-generator.md) · [Chapter index](README.md) · [Device Tree Overlays (DTBO)](05-device-tree-overlays.md) →</sub>
