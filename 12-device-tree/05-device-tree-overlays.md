# Device Tree Overlays (DTBO)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree


## An overlay changes a tree, not the hardware by itself

A device-tree overlay describes changes to an existing tree. It can add nodes or update properties, and it can be applied before kernel entry or through a supported live-kernel integration. These two cases have different driver-lifetime consequences.

A `.dtbo` does not automatically load a bitstream, stop DMA or make a driver safe to remove. A platform manager may coordinate those actions, but the overlay is only one part of that flow. The hardware must match the description at the point where drivers can access it.

The pinned Linux implementation is `drivers/of/overlay.c`, with behavior documented in `Documentation/devicetree/overlay-notes.rst` and `dynamic-resolution-notes.rst`.

## Labels require resolution information

A source overlay can target a label from the base tree. Compiling the base with `dtc -@` preserves symbols that let the resolver find the target path. The overlay contains fixup information for references that cannot be resolved until the base is available.

A target-path overlay can name an explicit path instead, but that path becomes part of its compatibility requirement. A label survives a node's move only if the base preserves the label; a path survives only if the hierarchy stays the same.

Phandle values can need adjustment when trees are combined. The resolver handles local references and external fixups under the overlay format. Copying numeric phandles from a decompiled base into a hand-written overlay bypasses that model and is fragile across builds.

## An offline experiment that was executed

The following small sources were compiled and merged on the host. They are synthetic data for a tree experiment and do not describe a real peripheral.

Base source:

```dts
/dts-v1/;
/ {
    compatible = "example,offline-tree";
    model = "Offline overlay exercise";
    demo: demo {
        status = "disabled";
        label = "before";
    };
};
```

Overlay source:

```dts
/dts-v1/;
/plugin/;
&demo {
    status = "okay";
    label = "after";
};
```

The executed tools compiled both inputs with `dtc -@`, merged them with `fdtoverlay`, and read the result with `fdtget`. The output properties were:

```text
okay
after
```

The source and binary files are kept outside the guide at `reference-setup/experiments/dt-overlay/`. This proves that the host resolver applied these two property changes. It does not prove a Linux driver probe, bitstream load or runtime overlay removal.

## Bootloader application avoids some runtime problems

When U-Boot applies an overlay before Linux starts, the kernel sees the resulting tree as its initial hardware description. Drivers have not yet claimed the changed device through Linux's normal probe path.

The base blob still needs enough writable space for the changes, and the bootloader must pass the merged result rather than the original base. A successful overlay operation on one buffer is irrelevant if the final boot command uses another DTB address.

The overlay must match the base tree and loaded hardware. A correctly resolved target can still describe the wrong interrupt or register map. Resolution success is a structural result, not hardware validation.

## Live application creates and removes device state

The in-kernel API `of_overlay_fdt_apply()` creates and applies a changeset and returns an identifier for the applied overlay. `of_overlay_remove()` removes a selected changeset subject to dependency rules. A stacked overlay that depends on another prevents removing the lower one first.

New active device nodes can cause devices to be registered and matching drivers to probe. Removal can require device deregistration and driver cleanup. A driver that assumes its device exists forever may not support this safely even when the tree operation itself is valid.

Do not assume the standard upstream kernel exposes a universal configfs interface for arbitrary overlays. User-facing loading mechanisms are integration choices. Verify the actual kernel patches, configuration and platform manager used by the product.

## Removal is a memory-lifetime boundary

The Linux overlay documentation warns that pointers into overlay nodes or property data must not survive removal. After the post-remove notification, the overlay memory is freed. A driver or notifier that retains such a pointer can later access freed memory.

Copy required data into storage with the appropriate lifetime or retain it through supported APIs only when those APIs guarantee the needed ownership. A raw pointer obtained during probe is not automatically safe after the tree changes.

Device activity has a similar lifetime. Stop userspace access, DMA and interrupt work before removing the hardware description or reconfiguring its PL region. Otherwise, a delayed interrupt or transfer can reach a device that no longer exists.

## Order a PL reconfiguration transaction

A product flow should stop new requests, wait for or cancel active work, quiesce the device and remove the old software instance. It can then change the hardware under the platform's isolation/reset rules, apply the matching description and probe the new device.

If any step fails, define the recovery state. For example, a loaded bitstream with no valid overlay is different from an old driver still bound to a changed register map. The system should not resume application traffic until hardware and software agree again.

## Diagnose overlay failures precisely

An unresolved symbol points to missing base symbols or a mismatched target. A no-space failure points to blob capacity. A successful merge followed by failed probe points to binding/resources/driver behavior. A crash during removal points toward lifetime and quiescing problems rather than syntax.

> [!NOTE]
> **Not run on the reference setup:** live overlay application/removal, PL reconfiguration and active-DMA teardown. Only the synthetic host merge above was executed.

## References

- [Linux 2024.1 overlay notes](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/devicetree/overlay-notes.rst).
- `linux-xlnx@xilinx-v2024.1:drivers/of/overlay.c` and `Documentation/devicetree/dynamic-resolution-notes.rst`.
- Executed host experiment: `reference-setup/experiments/dt-overlay/`.

---

<sub>← [System Device Tree and Lopper](04-system-device-tree-and-lopper.md) · [Chapter index](README.md) · [Device Tree Debugging](06-device-tree-debugging.md) →</sub>
