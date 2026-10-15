# Device Tree Debugging

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree

## Compare three views

Keep separate copies of the source tree, deployed DTB and live tree. The source may differ from the deployed file, and U-Boot or overlays may change the live tree further.

The live tree is available through `/sys/firmware/devicetree/base` and commonly `/proc/device-tree`. Properties are binary values, not ordinary text files. Strings, cells and byte arrays require different decoding.

## Inspection performed

The reference `system.dtb` was decompiled locally with DTC. Compilation/decompilation can emit warnings even when an output file is produced. Review warnings instead of treating a zero exit status as full binding validation.

A decompiled tree usually loses source labels and comments. Compare meaningful properties and paths; changing phandle numbers alone does not establish a hardware change.

## Fault checklist

| Failure | Check |
| --- | --- |
| No device | Parent population, `status`, compatible string |
| Probe deferred | Clock, regulator, reset and power providers |
| Wrong register access | Parent cell sizes, `reg`, `ranges` |
| No interrupt | Controller binding, index and trigger type |
| Old configuration persists | Actual DTB selected by the boot script |

## References

- Executed DTC decompilation of the reference BSP `system.dtb`
- `linux-xlnx@xilinx-v2024.1:Documentation/devicetree/`
- Saved `reference-setup/captures/system.dts`

---

<sub>← [Device Tree Overlays (DTBO)](05-device-tree-overlays.md) · [Chapter index](README.md) · Next chapter: [13 · The Linux Kernel](../13-linux-kernel/README.md) →</sub>
