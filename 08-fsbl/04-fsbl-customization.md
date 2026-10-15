# Customizing the FSBL

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot

## Use a defined hook

FSBL hooks provide controlled points around operations such as bitstream loading, handoff and fallback. Prefer a small change at the correct hook over modifying unrelated stage logic. Check the exact hook names and return contract in the pinned source.

Board code may control external PHY resets, USB components or clock devices. These are board-specific operations: copying another evaluation board's sequence can drive the wrong pin or access a missing I2C device.

## A maintainable change

Describe the hardware requirement first, including when the resource becomes available. Add bounded waits and a meaningful error return. Keep the patch in the firmware recipe's maintained layer and rebuild through the normal flow.

For a timing marker, use a documented spare signal and record its effect on pin configuration. For early peripheral access, ensure clocks and resets are ready. Avoid long blocking operations before watchdog or recovery handling is established.

## Verification

Review the patch against the original source, verify that the recipe applies it, and check the resulting ELF. Test normal boot and the failure path. A hook that returns success after a failed peripheral operation can hide the real cause until Linux starts.

> [!NOTE]
> **Not run on the reference setup:** custom hook execution on hardware.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_hooks.c`, `xfsbl_board.c`
- [Maintained PetaLinux customization](../05-petalinux/07-meta-user-customization.md)

---

<sub>← [Building the FSBL](03-building-the-fsbl.md) · [Chapter index](README.md) · [FSBL Debugging](05-fsbl-debugging.md) →</sub>
