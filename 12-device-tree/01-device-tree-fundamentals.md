# Device Tree Fundamentals

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree


## A hardware description with a defined binary encoding

A device tree describes hardware and its connections to software. A source file (`.dts`) can include shared source fragments (`.dtsi`). The build preprocesses and compiles them into a **flattened device tree blob (DTB)**, which the bootloader passes to Linux.

The tree is not executable initialization code. A node describes a device; a driver interprets its binding and performs operations. Adding a node cannot create missing programmable logic, power a disconnected board component or implement a driver that the kernel does not contain.

The same hardware can have different descriptions for different software domains. U-Boot's control tree and Linux's hardware tree also have different roles. Establish which tree you are reading before treating a property as the active Linux configuration.

## Nodes, properties, labels and phandles

A node has a name and properties. A unit address, such as `serial@ff000000`, identifies the node's address under its parent bus rules. The `reg` property describes the corresponding address and size tuples.

A source label such as `uart0:` lets other source fragments refer to a node. A **phandle** is the numeric reference used in the compiled tree. Decompilation usually shows numeric values where the original source used readable labels.

Those numeric values are not stable device identifiers across builds. If an earlier node is added, assigned phandles can change while the hardware stays the same. Compare the referenced nodes and their meaning, not only the printed number.

The optional `__symbols__` data produced for overlay use can preserve label-to-path information. It is not the same as the normal phandle reference itself.

## Decode a real reg property

The saved reference tree contains `/axi/serial@ff000000` with:

```dts
reg = <0x00 0xff000000 0x00 0x1000>;
```

The relevant bus uses two address cells and two size cells. Each cell is 32 bits. Combining the first pair gives address `0x00000000FF000000`; combining the second gives size `0x1000`, or 4096 bytes.

The unit address matches the device's bus address. On a bus with address translation, the CPU physical address can require applying the parent's `ranges`. Do not assume every `reg` tuple is already a CPU physical address, especially for devices below bridges.

An I2C child's `reg` commonly represents its bus address rather than a memory window. A PCI device follows its bus binding. The property name is shared, but its encoding depends on the parent bus and binding.

## References carry provider-specific arguments

The same UART node has two clock references and `clock-names = "uart_clk", "pclk"` in source-equivalent form. Each clock reference contains a provider phandle and the argument cells required by that provider's `#clock-cells` value.

Its interrupt property is `<0x00 0x15 0x04>` under the selected interrupt controller. The meaning of those cells comes from that controller's binding. The value is not directly a Linux virtual IRQ number, and the final cell is a trigger/type description rather than an arbitrary priority.

Power domains, resets, GPIOs and IOMMUs follow similar provider-reference patterns. The consumer binding says which named resources it requires; the provider binding says how to encode each reference. A syntactically valid list can still use the wrong provider or argument.

## Source inclusion determines the final property

The reference `system-top.dts` includes SoC definitions, clock definitions, the ZCU106 board include and processing-system configuration, then includes `system-user.dtsi`. Later source fragments can update an existing labeled node.

This makes small board-specific overrides practical, but it also means the first property occurrence is not necessarily final. Search the full include chain when a value appears to be ignored. Decompile the final DTB to confirm the resolved result.

The compiler catches syntax and many structural inconsistencies. Schema checks validate binding rules. Neither proves that the loaded bitstream or physical wiring matches the description. Hardware identity is a separate input to validation.

## Boot-time use and runtime use

Early Linux reads selected flat-tree information before the normal device model is ready. It needs memory ranges, reserved regions and boot parameters to construct its initial environment. Later, the tree becomes the kernel's in-memory node structure and bus/device population uses it.

This order explains why a bad `/memory` or reservation can fail much earlier than a missing peripheral driver. A malformed device node may leave one peripheral unavailable, while an incorrect RAM range can cause broad memory corruption.

The bootloader can also modify `/chosen`, memory information and initramfs bounds before entry. The DTB file from the build and the live tree seen by Linux can therefore differ legitimately. Compare both when debugging a boot-time override.

## A compile success has limits

The supplied `system.dtb` was decompiled during the reference work. The process produced warnings that remain part of the evidence; it was not reported as a schema-clean tree. Decompilation proves that the tool can parse the blob, not that all bindings or board resources are correct.

For a new device, validate its address range, interrupt route, clocks, resets and power dependencies against the hardware design. Then check the final DTB, driver match and probe result. These steps establish different parts of the same device path.

## References

- [2024.1 Linux flat-tree handling](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/of/fdt.c), plus `drivers/of/address.c` and `drivers/of/irq.c`.
- Reference `components/plnx_workspace/device-tree/device-tree/system-top.dts` and saved `reference-setup/captures/system.dts`.
- [DeviceTree specification](https://www.devicetree.org/specifications/), node, cell and reference model.

---

<sub>[Chapter index](README.md) · [Bindings and Driver Matching](02-bindings-and-driver-matching.md) →</sub>
