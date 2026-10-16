# Device Tree Debugging

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree


## Find which tree is wrong before editing it

A device-tree problem can occur in source generation, preprocessing, compilation, packaging, bootloader modification or runtime driver use. Editing `system-user.dtsi` helps only if that source actually reaches the tree used by the failing kernel.

Identify the source include chain, compiled DTB, selected FIT configuration and live tree. Record their identities. A correct standalone DTB can coexist with an old copy inside `image.ub`, and U-Boot can boot a different file than the one you just rebuilt.

The reference workspace contains generated source, a supplied `system.dtb` and a saved decompiled `system.dts`. These are useful comparison points, but they do not eliminate the need to inspect the actual runtime tree for a new boot.

## Separate syntax, binding and hardware errors

A syntax error prevents compilation. A structural warning can indicate an inconsistent address/cell relationship even when compilation completes. A schema failure means the node does not meet the selected binding. A functional failure can remain after all three checks pass.

For example, an interrupt specifier can have the correct number of cells and valid flag values while selecting the wrong physical input. A clock frequency can be valid as an integer while being wrong for the oscillator fitted to the board.

Preserve warnings instead of suppressing them to obtain clean-looking output. The supplied DTB's decompilation produced warnings during the reference work. That observation was not treated as a schema-clean result.

## Trace one peripheral through five boundaries

For a UART, first locate the node in the final tree. Check its `status` and the status of relevant parents. Next, confirm that its bus population path creates a device. Then check driver matching, probe return and the functional console path.

The reference `/axi/serial@ff000000` contains a compatible list, `reg`, interrupt data, two clocks, a power domain and pinctrl. If the node is present but no driver binds, inspect the compatible table and kernel configuration. If probe defers, inspect the missing provider. If probe succeeds but no characters appear, inspect pin routing, clock rate and console selection.

This order prevents changing a valid interrupt property when the real problem is that the UART driver was never built.

## Decode resources using their providers

A `reg` property's cell count comes from the parent bus. Combine cells correctly, then apply `ranges` where required. A decompiled number that looks like a CPU address can still be a child-bus address.

For `interrupts`, resolve `interrupt-parent` and read its binding. For `clocks`, resolve each provider and its `#clock-cells`. For GPIOs, distinguish controller line number and flags from any Linux userspace numbering scheme.

Do not compare raw phandle numbers across two DTBs as though they were stable hardware IDs. Resolve both references to their target nodes. The same provider can receive a different phandle after unrelated source changes.

## Probe errors often describe dependency failures

The Linux device model can defer probe when a required supplier is not ready. Identify the supplier rather than repeatedly rebuilding the consumer. A missing firmware node can affect clocks, resets or power domains used by many devices.

The ZynqMP firmware node's `method` selects SMC or HVC in the pinned driver. A missing or invalid method prevents a valid conduit from being selected. A peripheral that later reports a firmware error may be the first visible consumer of that earlier problem.

Keep the first meaningful error in the boot log. Later failures can be consequences. A long list of unpowered devices can have one common platform-management dependency.

## Compare source and runtime changes deliberately

The reference generated top-level source includes user configuration last. A later user override can replace a correct generated value. U-Boot can then change `/chosen`, memory and initramfs properties before kernel entry.

When the live tree differs, identify the producer of each difference. Source include order explains build-time changes; boot scripts and board fixups explain handoff changes; overlays explain dynamic changes. A difference is not automatically corruption, but an unexplained difference is a debugging lead.

For a FIT boot, inspect the configuration's FDT reference. Updating a file beside `image.ub` does not alter the FDT payload already inside that container.

## Use a minimal change to test a specific hypothesis

If a device is disabled, enable it only after confirming its resources and hardware presence. If a clock name is wrong, correct the name required by the binding and inspect probe again. If a PL address changed, update the hardware export and matching bitstream/DTB set.

Avoid changing address, interrupt, clock and driver all at once. A successful boot after several unrelated edits does not reveal which assumption was wrong, and it leaves unnecessary changes in the product.

A small offline overlay experiment can test symbol resolution without touching hardware. The [overlay section](05-device-tree-overlays.md) records such an executed host test. It establishes tree manipulation only; driver and hardware behavior still need their own checks.

## Reserve memory with the right purpose

A memory-related failure needs a map of the kernel, initramfs, DTB, resident firmware, DMA buffers and other processors' storage. A reserved region keeps Linux's normal allocator away when described correctly. It does not automatically establish hardware access protection or a DMA-coherency policy.

If failures appear only under load, inspect whether a missing reservation lets Linux reuse another component's memory. If failures begin only after overlay removal, inspect stale pointers and active device work. These patterns point to lifetime errors that a successful DTS compile cannot catch.

## A useful issue report

Include the kernel and firmware versions, final node path, relevant properties with resolved providers, driver name, first probe error and exact artifact identities. For a PL device, include the matching hardware-design identity and bitstream provenance.

> [!NOTE]
> **Not run on the reference setup:** new physical peripheral tests, schema validation of every reference binding and live-overlay fault diagnosis. The source/DTB chain and selected implementation paths were inspected; existing warnings remain acknowledged.

## References

- [2024.1 device-tree platform population](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/of/platform.c).
- `linux-xlnx@xilinx-v2024.1:drivers/of/{address.c,irq.c,fdt.c,overlay.c}` and `drivers/firmware/xilinx/zynqmp.c`.
- Reference generated `system-top.dts`, supplied `system.dtb`, and saved `reference-setup/captures/system.dts`.

---

<sub>← [Device Tree Overlays (DTBO)](05-device-tree-overlays.md) · [Chapter index](README.md) · Next chapter: [13 · The Linux Kernel](../13-linux-kernel/README.md) →</sub>
