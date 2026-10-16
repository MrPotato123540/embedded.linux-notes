# Xilinx Device Tree Generator (DTG)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree


## Generation translates exported hardware into software input

AMD's **Device Tree Generator (DTG)** uses a hardware export and generation scripts to produce device-tree source for the selected software flow. The hardware export provides processing-system and programmable-logic information. Board wiring and product-specific decisions can still require maintained user input.

A generated node is not independent evidence that the loaded bitstream matches it. If the XSA describes one PL address map and the boot package loads another design, the tree can compile perfectly while directing Linux to the wrong registers.

Treat the XSA, generator revision, generated source, user overrides and final DTB as one traceable chain. Record changes at each boundary rather than treating `system.dtb` as an unexplained binary output.

## The local 2024.1 recipe path

The inspected BSP uses `meta-xilinx-tools/recipes-bsp/device-tree/device-tree.inc`. It inherits `xsctdt` and `xsctyaml`, selects the `device-tree` application and uses the XSCT workspace output as the device-tree source path.

Its release include selects `DT_RELEASE_VERSION = "2024.1"`, branch `xlnx_rel_v2024.1`, and source revision `e30e471c0b466c0d6f51fa5c9611cb7ad2c83da1` for `device-tree-xlnx`. These exact values are stronger provenance than a repository's moving default branch.

The recipe adds release-specific board and binding include directories. It sets DTB padding to `0x1000` and adds the compiler's `-@` option when its overlay-generation setting is enabled. Padding and symbols serve different purposes: spare blob space helps later edits, while symbols support label-based overlay resolution.

## Follow the reference include chain

The generated reference `system-top.dts` includes `zynqmp.dtsi`, `zynqmp-clk-ccf.dtsi`, `zcu106-reva.dtsi` and `pcw.dtsi`. It later includes `system-user.dtsi`. This is the observed chain for the supplied project, not a promise that every project has identical filenames.

The SoC include describes common devices. The clock include supplies the platform clock structure. The board include describes board-level connections and external components. The processing-system configuration reflects exported settings. User input applies project-specific additions or overrides.

A `pl.dtsi` is common when the flow generates PL device nodes, but do not claim it is included merely because a tutorial lists it. Read the actual top-level source. A file present in the workspace but absent from the include chain has no effect on the resulting DTB.

## Keep user intent outside generated outputs

The local project has `project-spec/meta-user/recipes-bsp/device-tree/files/system-user.dtsi`. Its first include brings in `system-conf.dtsi`. Place maintained additions in the intended user layer and recipe inputs so regeneration can reproduce them.

Override the smallest required property. Copying a whole generated UART or Ethernet node into the user file creates duplicate maintenance and can retain old clocks or interrupts after the next hardware export. A targeted label reference makes the intended difference easier to review.

The label must still exist in the generated source. If a generator update renames or removes it, the build should expose that mismatch. Replacing the reference with a numeric phandle from an old DTB is not a stable repair.

## Worked change: moving a PL register window

Assume a design moves a custom PL peripheral from one AXI address window to another. This is a design example, not a modified reference bitstream.

The XSA must represent the new address map. DTG should produce the new `reg` information in the relevant source. A user override must not overwrite it with the old value. The final compiled DTB must contain the new address. The boot package must then load the matching bitstream and this DTB.

If Linux still accesses the old address, inspect those boundaries in order. An old XSA produces old generated source. A stale user override can replace a correct generated value. An old deployed DTB can hide a correct build. A mismatched bitstream can make even the correct new DTB unsafe.

The same review applies to interrupt connections, clock inputs and reset topology. Address equality alone does not establish full hardware compatibility.

## Generated output still needs binding review

A generator can describe hardware facts it understands, but a Linux driver may require a property that depends on board wiring or software integration. External PHY delays, regulators, fixed clocks and reset GPIOs are common examples of information that needs careful board-level review.

Use the binding from the selected kernel release. A generator and kernel from different release families can disagree about names or required properties. Inspect the final driver's resource requests when schema or probe behavior is unclear.

Do not solve an unsupported IP block by assigning a compatible string from a superficially similar device. Compatibility must cover the register interface and behavior expected by the driver.

## Validate source, artifact and live state

Compare generated source after a hardware import, then inspect the compiled DTB. If the DTB is included inside FIT, inspect the payload selected by that FIT configuration too. A standalone `system.dtb` can be correct while `image.ub` still contains an older tree.

At runtime, compare the live tree because U-Boot can apply fixups or overlays. A difference between source and runtime can be intentional, but it needs an identified producer. This prevents a bootloader change from being misdiagnosed as a failed DTG update.

> [!NOTE]
> **Not run on the reference setup:** a new XSA import and DTG rebuild for changed hardware. The local recipe, generated include chain and supplied DTB were inspected. Existing compiler warnings were not converted into a claim of schema-clean output.

## References

- Local BSP: `meta-xilinx-tools/recipes-bsp/device-tree/{device-tree.inc,device-tree-2024.1.inc}`.
- [Pinned 2024.1 DTG source](https://github.com/Xilinx/device-tree-xlnx/tree/e30e471c0b466c0d6f51fa5c9611cb7ad2c83da1).
- Reference `components/plnx_workspace/device-tree/device-tree/system-top.dts` and `project-spec/meta-user/recipes-bsp/device-tree/files/system-user.dtsi`.

---

<sub>← [Bindings and Driver Matching](02-bindings-and-driver-matching.md) · [Chapter index](README.md) · [System Device Tree and Lopper](04-system-device-tree-and-lopper.md) →</sub>
