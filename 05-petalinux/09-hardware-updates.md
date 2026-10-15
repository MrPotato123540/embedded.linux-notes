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

## References

- AMD UG1144 (2024.1), updating hardware configuration
- `xilinx-zcu106-2024.1:project-spec/hw-description/`, `project-spec/meta-user/`

---

<sub>← [Adding Applications and Libraries](08-adding-applications-and-libraries.md) · [Chapter index](README.md) · [BSP Packaging and Reproducible Builds](10-bsp-packaging-and-reproducible-builds.md) →</sub>
