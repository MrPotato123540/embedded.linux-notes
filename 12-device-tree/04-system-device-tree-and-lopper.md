# System Device Tree and Lopper

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[12 · Device Tree](README.md)** · Part V: Device Tree


## Describe the whole system before selecting one software view

A **System Device Tree (SDT)** describes resources across a heterogeneous system. A Linux domain on the A53, a bare-metal application on an R5 and platform firmware do not need identical views or ownership of that system.

Domain processing selects the resources and information intended for one software domain. **Lopper** is a tree-processing tool used in this flow. It can apply transformations and assists to produce outputs for selected software targets. The output tree is a derived view, not a new physical hardware design.

This distinction is useful for multi-processor systems. One source of system information can reduce duplicated address maps, but ownership policy still needs an explicit design. A tool cannot infer that two independent operating systems may safely program the same DMA controller.

## The 2024.1 evidence is a specific integration path

The local AMD layers contain `meta-xilinx-core/gen-machine-conf/lib/gen-machineconf/sdt_flow.py`. Its `ParseSDT()` entry rejects the `xsct` hardware-flow choice for the SDT path. This is direct evidence that the code distinguishes the flows rather than treating SDT as another name for classic XSCT generation.

The same source obtains machine information by running Lopper with `lop-machine-name.dts`. It obtains CPU information with `lop-xilinx-id-cpus.dts`, converts that information into a CPU dictionary and derives processor and SoC details when needed.

The command-line parser accepts a domain file in YAML or DTS form and offers PL-overlay generation options through the supported Lopper scripts. These facts describe the inspected 2024.1 tooling; they do not prove that the supplied classic PetaLinux project already uses this path.

The file `device-tree-sdt.inc` was not found in this BSP. A tutorial from another release that relies on that file must be treated as migration material until its layer and tool versions are matched.

## Follow the data through generation

The SDT flow starts with its hardware description and optional domain configuration. The code gathers machine and CPU information, generates hardware configuration data when the input changes, and uses that information to prepare machine/project outputs.

In the inspected code, hardware-file hashing participates in deciding when `Kconfig.syshw` must be regenerated. This shows that generated configuration is tied to the hardware input, not only to a manually selected board name.

A reproducible result needs the SDT input, any included files, domain file, Lopper version, assists and generation options. Recording only the final Linux DTS loses the policy and transformations that produced it.

## Worked ownership example: A53 Linux and an R5 application

Assume an R5 application owns one UART and a reserved DDR buffer, while Linux owns another UART and most remaining DDR. This is a design example, not a generated configuration supplied with the reference BSP.

The R5 view needs its UART, memory and required clocks or interrupt relationships. The Linux view must avoid claiming that same UART as an independent active device and must not allocate the R5 buffer as normal memory. Shared communication resources need a deliberate protocol and representation in both views.

Removing a device from Linux's tree prevents normal enumeration, but it is not hardware isolation. A privileged master or DMA device can still need protection rules. The system design must align device-tree ownership, firmware resource permissions and hardware access policy.

The same applies to interrupts. Assigning an interrupt to the R5 does not make it safe for Linux to configure the same peripheral's interrupt status or reset controls. Review the whole resource, including shared parents and resets.

## Dependencies can cross a domain boundary

A device can depend on a shared clock provider, power controller or interconnect path. Domain selection must preserve the information needed to use that device through the intended management interface without giving every domain unrestricted ownership of the provider.

A generated Linux node can look complete while its referenced provider was removed from the selected view. That produces unresolved references at build time or missing suppliers at runtime, depending on how the output was formed. Validate references and provider behavior after transformation.

Shared DDR is another dependency. Both domains must agree on physical ranges, cache attributes and ownership transitions. The SDT can describe the range, but it does not implement synchronization or cache maintenance for the application protocol.

## Migration requires comparison, not only compilation

When moving from a classic XSA/DTG flow, first preserve the existing working artifacts. Compare CPU selection, memory ranges, reserved regions, device status, interrupt routes and clock/reset references in the new outputs.

Then compare generated standalone platform inputs as well as Linux's tree. A change that improves the Linux description can still break the R5 application's generated headers or linker memory map. The complete multi-domain build is the unit of review.

A clean DTS compile checks syntax and structure. It does not prove equivalent resource policy or correct firmware permission data. Follow the new domain view into the runtime driver and platform-management paths.

## Debugging a missing generated device

Check whether the input SDT contains the device. If it does, inspect domain selection and the transformation or assist that filters it. If the output contains the node but a dependency is missing, inspect provider retention and reference rewriting.

If the output looks correct but Linux lacks the device, move to normal status, bus population, driver matching and probe diagnosis. Do not keep changing Lopper rules when the generated node has already reached the kernel correctly.

> [!NOTE]
> **Not run on the reference setup:** an SDT domain-generation build or the illustrative A53/R5 ownership plan. This section reports direct inspection of the local 2024.1 integration and explains the required review boundaries.

## References

- Local BSP: `meta-xilinx/meta-xilinx-core/gen-machine-conf/lib/gen-machineconf/sdt_flow.py` and `gen-machine-conf/README.md`.
- [AMD System Device Tree project](https://github.com/Xilinx/system-device-tree-xlnx), project context; match a release before adoption.
- [Lopper project](https://github.com/devicetree-org/lopper), transformation and domain-processing context.

---

<sub>← [Xilinx Device Tree Generator (DTG)](03-xilinx-device-tree-generator.md) · [Chapter index](README.md) · [Device Tree Overlays (DTBO)](05-device-tree-overlays.md) →</sub>
