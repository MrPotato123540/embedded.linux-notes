# Hardware Updates and XSA Re-Import

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## What a hardware update changes

An XSA update can change addresses, interrupts, clocks, resets, processor initialization and programmable-logic content. Treat it as an interface change between hardware and software. A new bitstream with an old device tree can expose the wrong registers even when Linux boots.

Before importing, record the hardware revision and preserve the current project configuration. After import, compare generated processor initialization and device-tree inputs. Review custom includes for renamed nodes or changed addresses.

## Bitstream loading choices

A bitstream inside `BOOT.BIN` can be loaded by the FSBL before Linux starts. A Linux FPGA-manager flow loads it later under software control. These choices affect when a peripheral exists and when its driver may safely probe.

For late loading, coordinate the bitstream, overlay and application. For early loading, confirm the packaged boot image actually includes the new partition. Updating `system.bit` on disk does not alter a previously generated `BOOT.BIN`.

## Review checklist

- Compare hardware address ranges and interrupt routes.
- Check clocks, resets and external board connections.
- Rebuild affected firmware and device trees.
- Repackage the boot image when its inputs change.
- Test both boot and real peripheral traffic.

Keep user changes as small overrides or patches so generated files can be replaced cleanly. If a node disappears, resolve the hardware change instead of restoring the old node blindly.

> [!NOTE]
> **Not run on the reference setup:** importing a new board XSA and validating the resulting hardware behavior. This procedure requires the matching design and board.

## Treat the XSA as an interface revision

The XSA is not only a convenient file for the import command. It carries a version of the hardware/software interface. A register block can move, an interrupt can be rerouted, a clock can change, or a processor initialization sequence can become different. Software built for the previous interface may still compile and boot while accessing the wrong resource.

Give each exported hardware design an immutable identity. Record the hardware source revision, export tool version and XSA checksum. Keep the matching bitstream and any initialization data associated with that export. A filename such as `latest.xsa` cannot establish which design a field image uses.

Before import, preserve the current project inputs and note the working baseline. After import, review the changed generated data. A large generated diff can contain both harmless ordering changes and one critical address or clock change. Compare the hardware contract, not only the number of changed lines.

## Map hardware changes to software consumers

| Hardware change | Software that can be affected | Failure that a boot-only test can miss |
| --- | --- | --- |
| Register base or range | Device tree, driver resource mapping, userspace interfaces | Access to the wrong block |
| Interrupt route or trigger | Device tree and interrupt handling | Lost interrupts or an interrupt storm |
| Clock frequency or source | Initialization data, clock provider and timing setup | Incorrect bus timing or sample rate |
| Reset connection | Driver reset sequence and power management | First access hangs after a restart |
| DMA path or address width | Driver DMA setup, reserved memory and translation | Corruption under sustained traffic |
| PL image layout | Early boot package or FPGA-manager firmware set | Driver probes hardware that is not present |

This table gives a review direction. The exact affected files depend on the IP and generation flow. Follow the binding and driver source for the component rather than applying one generic fix to all PL peripherals.

## Preserve external board knowledge

An XSA describes the exported design, but the Linux board description may include external devices and product wiring. A sensor on I2C, a PHY reset GPIO or a regulator relationship can be maintained outside generated hardware data. After import, confirm those user additions still refer to the correct labels and resources.

If a generated node disappears, first determine whether the hardware was removed, renamed or moved to another loading domain. Copying its old node back into the user tree can make the DTS compile while describing hardware that no longer exists. Compilation validates syntax and some structural rules, not the physical board contract.

Generated processor initialization must also match the new design. Changes to clocks, memory or pin configuration can affect early firmware before Linux reads the device tree. A Linux-only rebuild may therefore be insufficient even when the visible change seems to concern one peripheral.

## Early PL loading and late PL loading have different lifetimes

With early loading, the boot package makes the PL design available before Linux starts. The base device tree can describe devices expected at that time. The FSBL and boot package must contain the correct PL data, and the hardware must reach a usable clock/reset state before drivers access it.

With late loading, Linux coordinates firmware loading and device creation. The bitstream, overlay and application form a compatible set. Drivers must not access the old design while it is being replaced, and no active DMA engine may continue using resources that are disappearing.

Changing from one policy to the other is more than moving a file. Review when devices become visible, who owns resets and clocks, how applications detect readiness, and what happens when loading fails. A partially configured system needs a defined recovery path.

## Follow one address-change example

Imagine a teaching peripheral whose register window moves to a new AXI address. First, the exported hardware must report the new range. The generated device-tree node must reflect it. Any user include must stop overriding the old range. The driver's resource mapping should use the firmware-described resource rather than a hard-coded physical address.

Next, inspect any userspace code that bypasses the driver. A program with the old address embedded in a `/dev/mem` mapping will not be repaired by a correct device tree. This is one reason a stable driver interface is easier to maintain than applications that know physical register addresses.

Finally, test the actual new block with a safe identification or status read defined by its specification. Do not probe arbitrary addresses to guess where it moved. The example here is a reasoning exercise, not a recorded modification of the reference board.

## Release and regression evidence

Rebuild every affected component and inspect the resulting DTB, firmware and boot package. Keep their checksums with the new hardware identity. Boot from reset using the intended medium, then test the changed peripheral under realistic traffic and restart conditions.

Include negative checks: an old application should fail clearly if its hardware interface is incompatible, and a failed PL load should not leave userspace using stale resources. For DMA or timing changes, a successful register read is only an initial check. Sustained transfers, cache ownership and interrupt behavior need separate evidence.

No new XSA was imported in this writing pass. The expanded procedure explains the dependency and lifetime checks required for a real board update; it does not turn the existing BSP inspection into hardware-validation evidence.

## References

- AMD UG1144 (2024.1), updating hardware configuration
- `xilinx-zcu106-2024.1:project-spec/hw-description/`, `project-spec/meta-user/`

---

<sub>← [Adding Applications and Libraries](08-adding-applications-and-libraries.md) · [Chapter index](README.md) · [BSP Packaging and Reproducible Builds](10-bsp-packaging-and-reproducible-builds.md) →</sub>
