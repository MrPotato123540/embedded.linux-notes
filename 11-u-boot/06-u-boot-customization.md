# Customizing U-Boot

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot

## Maintain configuration and code separately

Use the PetaLinux U-Boot configuration flow for supported menu options. Preserve the resulting fragments in `meta-user`. A defconfig provides the base; later fragments and recipe settings determine the final configuration.

Older board flows may use headers such as `platform-top.h` for defaults. Do not assume every option still belongs there. Check whether the pinned release uses a Kconfig symbol, environment source or board header.

## Source changes

Put patches to `board/xilinx/zynqmp` or command code in a recipe append. A custom command needs argument validation, clear failure returns and configuration integration. Avoid turning a diagnostic command into an unrestricted production interface accidentally.

U-Boot's control tree and the Linux handoff tree can differ. Verify both when changing pins, storage or early console settings. A working Linux driver does not prove that U-Boot supports the same hardware setup.

> [!NOTE]
> **Not run on the reference setup:** a custom U-Boot rebuild and cold-boot test. Use the [devtool workflow](../04-yocto-project/07-devtool-workflow.md) to preserve changes before image integration.

## References

- `u-boot-xlnx@xilinx-v2024.1:board/xilinx/zynqmp/`
- AMD UG1144 (2024.1), U-Boot configuration

---

<sub>← [How U-Boot Boots the Linux Kernel](05-how-u-boot-boots-linux.md) · [Chapter index](README.md) · Next chapter: [12 · Device Tree](../12-device-tree/README.md) →</sub>
