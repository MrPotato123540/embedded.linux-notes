# Bindings and Driver Matching

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree

## Binding contracts

A binding defines the properties a hardware node may or must contain. Many Linux bindings use YAML schemas. The schema describes names, types, required fields and relationships; the driver implements the behavior.

A platform driver's `of_match_table` contains compatible strings. A matching string can select driver data as well as the driver itself. Matching is only the start: probe can still fail because a clock, reset, interrupt or regulator is missing.

## Validation layers

DTC checks syntax and structural rules. Schema validation checks the binding. Driver probing checks runtime dependencies. Real traffic checks actual hardware behavior. Passing one layer does not replace the others.

`dt_binding_check` validates binding schemas; `dtbs_check` validates built trees against schemas. Use the tools and bindings associated with the kernel release.

Drivers read properties through interfaces such as `of_*` and `device_property_*`. Reject malformed required data and propagate deferred-probe results when a provider is not ready. Do not silently use a guessed register size after a parsing failure.

## References

- `linux-xlnx@xilinx-v2024.1:Documentation/devicetree/bindings/`
- Linux 6.6 [device-tree usage model](https://docs.kernel.org/6.6/devicetree/usage-model.html)

---

<sub>← [Device Tree Fundamentals](01-device-tree-fundamentals.md) · [Chapter index](README.md) · [Xilinx Device Tree Generator (DTG)](03-xilinx-device-tree-generator.md) →</sub>
