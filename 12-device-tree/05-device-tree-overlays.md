# Device Tree Overlays (DTBO)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree

## Overlay mechanism

A device-tree overlay changes an existing tree. It identifies a target node and supplies properties or child nodes to add or modify. Compiling with symbol support allows label-based references to be resolved against the base tree.

An overlay is metadata. It does not itself guarantee that matching programmable logic is configured, clocks are running or drivers can be removed safely.

## Applying changes

U-Boot can apply supported overlays before Linux starts. Linux has an in-kernel overlay mechanism, but a userspace configfs interface depends on the vendor kernel and configuration; it is not a universal upstream interface. FPGA-region and DFX management flows may coordinate overlays with configuration loading.

For a PL device, first establish the matching hardware design and loading sequence. Before removal, stop applications and DMA, detach users and ensure the driver supports removal. Removing a node while its memory or callbacks are still used can cause a crash.

## Debugging

Check target symbols, base-tree compatibility and dependency order. Then inspect the live tree and driver state. A successful overlay apply does not prove successful driver probe.

> [!NOTE]
> **Not run on the reference setup:** overlay application/removal with physical PL hardware.

## References

- Linux 6.6 [overlay notes](https://docs.kernel.org/6.6/devicetree/overlay-notes.html)
- `linux-xlnx@xilinx-v2024.1:drivers/of/overlay.c`

---

<sub>← [System Device Tree and Lopper](04-system-device-tree-and-lopper.md) · [Chapter index](README.md) · [Device Tree Debugging](06-device-tree-debugging.md) →</sub>
