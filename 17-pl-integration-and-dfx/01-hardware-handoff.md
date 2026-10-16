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

## Handoff is a versioned interface

An XSA describes a hardware export at one point in the design flow. Software generation uses its processor, address and peripheral information. The bitstream implements the programmable hardware. The device tree tells Linux which devices and resources software should expect. These artifacts describe related parts of one contract, but none can replace the others.

A bitstream can configure successfully while being incompatible with its device tree. For example, an address can still decode but now contain a different IP version. A driver may then read plausible values from the wrong register layout. Include a hardware identity/version check in custom IP where practical, but make the identity read itself safe through the integration contract.

AMD (formerly Xilinx) tool version alignment helps reproducibility, but matching the year and release number is not sufficient. Local design changes, IP settings and board revisions remain distinct inputs.

## Inspect the actual BSP export

The supplied `project-spec/hw-description/system.xsa` is a ZIP-format container. A read-only listing showed `project_2.hwh`, `project_2.bit`, `psu_init.c`, `psu_init.h`, `xsa.json`, `xsa.xml` and board metadata, along with further generated design files.

This is useful evidence: this particular export includes a bitstream and processing-system initialization material. It does not establish that every XSA includes a bitstream or that an unrelated file called `system.bit` is byte-identical. Follow the artifact actually imported and the one actually packaged.

The BSP also contains separate project1 and project2 firmware sources. A release procedure must select the intended board/design variant explicitly. File presence is not selection. Keep the chosen XSA path and hash with the software build record.

## Work through one peripheral contract

For an illustrative AXI-Lite status peripheral, begin with its address range in the hardware design. Then identify its bus clock, reset source and interrupt route if it has one. Determine whether the register interface is little-endian, which access widths are legal, and whether reads or writes have side effects.

The device-tree node must encode the correct resource range and dependencies using the binding expected by the driver. The driver's match table must accept the compatible string. Its probe must acquire resources in an order that makes register access safe.

The application sees the driver's userspace interface, not the XSA. If a new hardware version changes a status bit, either preserve the old software contract or version the driver/application interface. A regenerated device tree cannot repair application code that assumes the old meaning.

## Clock and reset are part of address validity

A mapped address can still be unsafe if the target clock is stopped or reset is asserted. The CPU's virtual-memory mapping only makes an address accessible through its page tables. It does not ensure the interconnect can complete the transaction.

Likewise, a working control path does not prove the data path works. An AXI-Lite register interface can use one clock while an AXI stream or memory master uses another. Reset sequencing and clock-domain crossings must be valid across the whole path.

For runtime replacement, identify which clocks and resets belong to the static design and which belong to the reconfigurable region. Shared resources must remain valid for devices that continue running. Resetting a shared DMA block while another client is active is a system-level ownership error.

## Generated files are review inputs

After importing a changed XSA, inspect the generated differences before building a release. Look for moved resources, renamed nodes, changed interrupt parents, clock references and disabled devices. A large generated diff can contain one critical compatibility change among many cosmetic changes.

Keep maintained overrides in the supported user layer. Editing generated files can make one build appear correct while the next regeneration removes the fix. If an override compensates for a generator limitation, document both the hardware fact and the generated behavior it replaces.

Do not assume a successful device-tree compile validates the hardware. DTC checks syntax and selected structural conditions. Schema checks add binding validation. Neither tool observes the bitstream loaded on the board or the actual clock waveform.

## Release and recovery records

A useful hardware/software manifest links the board revision, XSA, bitstream, device tree, kernel, driver package and application. For DFX, also link each partial image to its compatible static shell and slot. Hashes distinguish files with identical names.

A rollback plan should restore a compatible set. Reverting only the application can fail if the PL register interface changed. Reverting only the bitstream can fail if the device tree now points at moved resources. Make the compatible set the release unit even when its files are stored in different partitions or packages.

## Bound the validation claim

The XSA inspection establishes container contents. The previously decompiled device tree establishes the supplied software description. Physical validation must still confirm clocks, resets, interrupt delivery, data integrity and error recovery on the intended board revision.

Start with a documented safe identity read, then exercise the interface through its driver. Do not discover the memory map by scanning arbitrary MMIO addresses; an absent or side-effect register can stall or disturb the system.

## References

- Inspected BSP `project-spec/hw-description/system.xsa` ZIP entries and supplied firmware XSA paths.
- [linux-xlnx@xilinx-v2024.1:Documentation/driver-api/driver-model/binding.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/driver-model/binding.rst).

- AMD UG1144 (2024.1), hardware import
- Reference XSA and generated device-tree inputs

---

<sub>[Chapter index](README.md) · [Accessing PL Peripherals From Linux](02-accessing-pl-peripherals.md) →</sub>
