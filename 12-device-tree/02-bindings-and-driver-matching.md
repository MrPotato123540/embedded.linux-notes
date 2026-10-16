# Bindings and Driver Matching

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree


## A binding is the contract between hardware description and driver

A device-tree **binding** defines the accepted node structure: compatible strings, required properties, resource encodings and constraints. Modern Linux bindings commonly use YAML schemas. The driver then consumes those properties through kernel APIs.

A compatible string identifies a hardware programming interface or a specific compatible variant. It is not an arbitrary product label chosen only to make a driver load. Claiming compatibility promises that the driver's register layout and behavior are valid for that device.

An ordered compatible list can name a specific implementation followed by a compatible fallback. The driver and binding decide which match data applies. A fallback is valid only when the hardware actually preserves that programming interface.

## Device creation and driver matching are separate steps

In `drivers/of/platform.c`, `of_platform_populate()` and related helpers create platform devices for eligible nodes and buses. Availability checks consider node status. A disabled node does not become a normal active device simply because its compatible string matches a compiled driver.

In `drivers/base/platform.c`, `platform_match()` considers the platform matching paths, including `of_driver_match_device()` for device-tree matching. A driver's `of_match_table` supplies the compatible entries and can attach variant data.

The matched driver's probe function then acquires resources and initializes the device. A successful compatible match is only the start of probe. Missing clocks, reset controls, interrupts, regulators or firmware services can still make probe fail or defer.

## Work through the reference UART

The saved `/axi/serial@ff000000` node contains compatible strings corresponding to `xlnx,zynqmp-uart` and `cdns,uart-r1p12`. It also contains a register window, interrupt reference, two named clocks, a power-domain reference and pinctrl settings.

This set describes more than the UART's address. The clock provider must exist and offer the requested outputs. The interrupt controller must interpret the specifier. The power domain must permit the device's required state. The pin configuration must connect the intended signals to the board pins.

If you copy only `compatible` and `reg` into a new board tree, matching can occur while the device remains unusable. The driver may fail to obtain a required clock or may initialize internal registers without any signal reaching the connector.

## Resource APIs translate the description

A driver normally asks for resources through APIs rather than hard-coding a physical address. Address translation follows parent-bus rules. Interrupt translation follows the selected interrupt domain. Clock and reset APIs reach their provider drivers.

This indirection makes the same driver usable across boards, but it also creates dependencies. A clock request can fail because the clock provider has not probed, even when the consumer node is correct. A power-domain request can reach firmware and receive an access-policy error.

Preserve return codes from these APIs. Replacing a failed resource acquisition with a guessed constant can hide the dependency failure and make later behavior much harder to diagnose.

## Deferred probe means “a dependency may appear later”

`-EPROBE_DEFER` tells the driver core that the device may become usable after another provider is ready. It is different from a permanent invalid configuration or unsupported device.

A useful diagnosis identifies the missing supplier and follows its own probe path. If the supplier is disabled, absent from the kernel configuration or itself waiting on a broken dependency, repeated deferral will not solve the problem.

Avoid arbitrary sleeps in the consumer probe as a substitute for dependency handling. A delay can make one boot appear to work while leaving ordering undefined. Use the framework's resource and deferred-probe mechanisms.

## Schema validation and runtime validation catch different errors

A schema can reject a misspelled property, an invalid item count or a missing required resource. It can also constrain compatible combinations and names. This is stronger than a DTB compile that only establishes valid syntax and structure.

A schema cannot prove that the board's oscillator really runs at the declared frequency or that an interrupt wire reaches the chosen input. Runtime probe and functional tests provide that evidence. Keep schema success and hardware success as separate results.

A driver may tolerate a property that the binding does not document, but that is not a good reason to depend on it. Undocumented behavior can change and may not be accepted by other kernels. Prefer the release's documented binding and inspect the implementation when behavior is unclear.

## Designing a new binding

For a new PL device, define a vendor-qualified compatible string that describes its register interface. Specify register windows, interrupts, clocks and resets as required by the hardware. Separate immutable hardware facts from changeable policy such as application modes.

Version the interface when incompatible register semantics change. A bitstream with the same base address but a different register layout is not automatically compatible. An identity/version register can help a driver reject the wrong design, but it does not replace a correct binding.

The synthetic PL-ID example in [the driver chapter](../14-kernel-modules-and-drivers/README.md) is a teaching interface. Its invented compatible and identity value must not be presented as a real ZCU106 peripheral.

## Diagnose the exact missing step

If no device appears, inspect node availability and parent-bus population. If a device exists without a driver, inspect the match table, module availability and aliases. If the driver probes and returns an error, inspect its first failed resource or hardware check.

If probe succeeds but no data arrives, inspect functional configuration, pin routing and interrupts. A bound driver is not a complete functional test. Record the relevant node path, matched driver, probe result and hardware observation together.

## References

- [2024.1 platform-bus matching](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/base/platform.c).
- `linux-xlnx@xilinx-v2024.1:drivers/of/{platform.c,address.c,irq.c}` and `Documentation/devicetree/bindings/`.
- Saved reference `system.dts`, UART node and resource references.

No new driver probe or physical UART validation was performed for this section.

---

<sub>← [Device Tree Fundamentals](01-device-tree-fundamentals.md) · [Chapter index](README.md) · [Xilinx Device Tree Generator (DTG)](03-xilinx-device-tree-generator.md) →</sub>
