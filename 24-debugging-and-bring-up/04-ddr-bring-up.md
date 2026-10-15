# DDR Bring-Up and Memory Testing

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## DDR depends on the board

DDR configuration must match device type, topology, widths, timing and board routing assumptions. Generated initialization comes from the hardware design settings. A parameter copied from another board can produce intermittent corruption rather than a clean failure.

## Test scope

U-Boot `mtest`, target `memtester` and standalone memory tests exercise different environments. A userspace test only covers memory it can allocate. It does not automatically test every physical address or all boot-time conditions.

> [!WARNING]
> Memory tests overwrite their test range. Exclude running code, stacks, firmware, device-tree data and other live buffers.

Use varied patterns, address ranges, temperatures and concurrent traffic. Compare cold boot, warm boot and long-duration behavior. Passing one short test does not establish signal-integrity margin.

> [!NOTE]
> **Not run on the reference setup:** physical DDR stress or electrical measurements. QEMU cannot validate them.

## References

- UG1085 (v2.5), DDR controller
- Vivado 2024.1 processing-system memory configuration documentation

---

<sub>← [Custom Board Bring-Up](03-custom-board-bring-up.md) · [Chapter index](README.md) · [Common Failures and Fixes](05-common-failures.md) →</sub>
