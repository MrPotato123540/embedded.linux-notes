# Hardware Handoff: From Vivado to Linux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Hardware/software contract

The XSA exports hardware information used by software tools. It can carry processor configuration, address maps and programmable-logic design data. It does not replace the external board schematic or an IP's register specification.

For each PL peripheral, record its address range, clock, reset, interrupt route and driver binding. These must agree across the Vivado design, generated device tree, bitstream and software image.

## Release procedure

Keep the XSA and bitstream tied to one hardware revision. Import that revision, regenerate hardware-dependent inputs and review the differences. Check renamed nodes and changed interrupt routes before rebuilding.

Publish a compatibility record with the application package. A file named `system.bit` from another build can load successfully while implementing a different register interface. A hardware version register can help detect that mismatch if the IP design includes one.

> [!NOTE]
> **Not run on the reference setup:** a new PL design import and physical validation.

## References

- AMD UG1144 (2024.1), hardware import
- Reference XSA and generated device-tree inputs

---

<sub>[Chapter index](README.md) · [Accessing PL Peripherals From Linux](02-accessing-pl-peripherals.md) →</sub>
