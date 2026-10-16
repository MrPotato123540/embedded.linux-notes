# Customizing U-Boot

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot


## Choose the layer that owns the behavior

A U-Boot change can belong to Kconfig, a device tree, default environment, boot-script metadata or C source. Choosing the correct layer makes the change smaller and easier to reproduce.

Enable an existing command or driver through configuration when possible. Describe board wiring and resources through the appropriate device tree. Change boot selection in the maintained script or environment source. Patch C code when the required behavior is not already represented by those interfaces.

A runtime `setenv` experiment is useful for understanding behavior, but it is not a reproducible product change by itself. Move the accepted result into tracked build inputs and account for persistent environments that may override compiled defaults.

## Establish the exact 2024.1 source baseline

The local recipe uses U-Boot `v2024.01`, branch `xlnx_rebase_v2024.01`, and commit `fbed1010e50d75e7d25acc1c2d09e1c34cb7e882`. AMD's tree contains platform changes beyond the upstream version label.

Keep source patches against that baseline. A patch that applies cleanly to upstream v2024.01 can still conflict with AMD's board behavior or later recipe patches. The effective recipe, append order and selected configuration determine the actual build.

Do not edit `tmp/work` as the permanent source of a change. BitBake can recreate the directory, and another developer cannot reproduce an untracked work-tree edit from the project repository.

## Kconfig dependencies are part of the result

A command can require a core subsystem, a driver and supporting libraries. Enabling only its visible symbol may not create a usable interface if dependencies select a different result or the hardware description is absent.

The final `.config` is stronger evidence than the fragment you requested. Review it after configuration. Also check the built help or symbol presence where appropriate. A command omitted by configuration cannot be fixed by changing a boot script that tries to invoke it.

Keep production size and attack surface in mind as concrete design constraints. A diagnostic command may allow unrestricted memory writes or persistent storage changes. Decide whether it belongs in the shipped interface instead of carrying every development option forward automatically.

## Worked change: an additional boot source

Assume a product adds a supported network recovery path. This is a design example, not an implemented recovery image. The change needs the Ethernet driver, PHY description, network commands, server policy, artifact names and a safe destination layout.

First verify that U-Boot's own control tree describes the controller and PHY correctly. A Linux DTB change alone may not affect this driver. Then verify the required command configuration and a network transfer with a known artifact.

Next, add the script path with explicit error checks. A failed transfer must not boot stale RAM. The recovery image must carry a compatible kernel, DTB and root filesystem plan. Finally, decide how the path is selected and whether its artifacts need authentication under the product's boot policy.

This sequence separates driver support from boot policy. Replacing the whole board file to add a filename would create more maintenance work than the behavior requires.

## Custom drivers must respect bootloader lifetimes

U-Boot's driver model and allocation environment change across early initialization and relocation. A device used before relocation may need the appropriate early availability and memory behavior. A pointer into temporary early storage cannot be assumed valid forever after relocation.

The generic source in `common/board_f.c` reserves runtime objects and prepares relocation, while `common/board_r.c` continues later initialization. Inspect the stage where the custom driver is called before deciding which services and memory are available.

Keep probe work bounded and return meaningful errors. A driver that waits forever for an absent device can prevent the recovery console from appearing. If a device is optional, define how boot continues when it is absent; if it is required, make the failure visible at the correct boundary.

## Patch the handoff only with a complete contract

Changes near `arch/arm/lib/bootm.c` affect the kernel entry protocol. A board-specific workaround that skips cache cleanup or leaves DMA running can produce intermittent Linux corruption. An apparently faster jump is not a successful optimization if it violates ownership at the boundary.

For device-tree fixups, modify the working Linux tree deliberately and preserve enough space for changes. Check return values from tree operations. A failed property update must not silently leave stale initramfs bounds or incorrect memory information.

A fixup also needs version compatibility. If a property is required by a newer kernel binding, decide what happens with an older recovery kernel and its driver. Bootloader, DTB and kernel updates should be reviewed as a set.

## Review deployed behavior, not only compilation

After building, record the executable, configuration, control-tree input, boot-script output and hashes. Confirm that `BOOT.BIN` uses the new U-Boot ELF and that the boot medium contains the intended script and OS artifacts.

A persistent environment can hide a changed default. Test with the intended environment state and explicitly review migration behavior. Do not erase a user's persistent configuration merely to make the new default appear correct.

For a source change, test the affected path and at least one meaningful failure case. A new storage path needs missing-media or missing-file behavior. A new driver needs absent-device behavior. A boot-policy change needs recovery behavior when its primary input fails.

> [!NOTE]
> **Not run on the reference setup:** a custom U-Boot rebuild, the illustrative recovery path and persistent-environment migration. The 2024.1 recipe baseline, generic initialization and handoff sources were inspected.

## References

- Local BSP: `meta-xilinx-core/recipes-bsp/u-boot/{u-boot-xlnx-2024.1.inc,u-boot-xlnx-common.inc,u-boot-xlnx-scr.bb}`.
- [2024.1 ZynqMP board implementation](https://github.com/Xilinx/u-boot-xlnx/blob/xilinx-v2024.1/board/xilinx/zynqmp/zynqmp.c).
- `u-boot-xlnx@xilinx-v2024.1:common/{board_f.c,board_r.c}` and `arch/arm/lib/bootm.c`.

---

<sub>← [How U-Boot Boots the Linux Kernel](05-how-u-boot-boots-linux.md) · [Chapter index](README.md) · Next chapter: [12 · Device Tree](../12-device-tree/README.md) →</sub>
