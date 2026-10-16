# PMU Firmware at Boot

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## When PMU firmware starts

The **Platform Management Unit firmware (PMUFW)** runs on the PMU processor and remains active during Linux operation. It handles platform services that outlive the FSBL.

The reference BIF uses `[pmufw_image] pmufw.elf`. This selects the BootROM-loading form. A normal partition with a PMU destination is loaded later by the FSBL. The two forms differ in startup timing and boot-image layout; they should not be treated as interchangeable spellings.

## Runtime initialization

PMUFW initializes its framework and enabled modules. Platform-management requests arrive through Inter-Processor Interrupts (IPI). The power-management configuration describes which resources and operations a subsystem may use. A running PMU processor alone does not prove that every requested service is permitted.

## Failure symptoms

Missing or incompatible firmware may appear as clock, reset, power-domain or processor-start failures in later stages. Read the PMU version and Linux firmware-driver errors before blaming the peripheral driver. Keep PMUFW and TF-A aligned with the release and hardware configuration.

> [!NOTE]
> **Not run on the reference setup:** replacing PMUFW and testing both loading methods. The saved boot log demonstrates only the supplied reference flow.

## Loading method affects when services exist

The special `[pmufw_image]` BIF form supplies PMU firmware to the initial ROM-loading arrangement. A later partition directed to the PMU is handled through a different point in the boot sequence. The distinction affects both image representation and the time at which other software can expect firmware services.

The reference boot header has a nonzero PMU firmware length, and its first partition-length accounting includes the special initial firmware representation described in the previous section. The BIF therefore needs to be read together with the decoded image, not treated as a generic list of equal partitions.

A debugger or QEMU launch can load PMU firmware directly. The saved reference launch starts a separate MicroBlaze QEMU instance and supplies the PMU ROM model and firmware ELF. That proves which inputs the emulator used; it does not demonstrate BootROM loading those bytes from physical storage.

## Separate transport, service implementation and policy

A platform request must pass several boundaries. The caller needs an available interface, the message must reach the intended processor, the firmware must implement the requested service, and the platform configuration must permit the operation. A working mailbox alone does not prove that the operation is allowed.

This separation helps diagnose errors. A timeout can indicate a transport or execution problem. An explicit rejection can mean the request reached firmware but violated policy or was unsupported. A successful return can still require the caller to observe the resulting hardware state according to the API contract.

For a Linux clock or power-domain failure, inspect the Linux firmware interface, TF-A service path and PMU firmware response together. Changing the peripheral driver's register code is unlikely to fix a platform request rejected before those registers are usable.

## Platform configuration describes ownership

Firmware may manage resources shared by several processors or subsystems. It needs to know which subsystem can request a resource and which transitions are allowed. The platform-management configuration provides part of that policy.

A system that uses Linux on A53 and firmware on R5 must agree on ownership. If both assume independent control of the same reset or power resource, one can disrupt the other. Shared memory and IPI channels also need a consistent assignment. A valid Linux device tree does not by itself establish the complete firmware policy.

Review the configuration after a hardware update or a change in processor use. A previously unused R5 becoming active changes the system's resource and lifetime assumptions even if the Linux application is unchanged.

## Firmware remains active after boot

PMU firmware handles runtime operations, so its correctness affects suspend, restart, processor start/stop and resource transitions. A successful login test exercises only part of this behavior. Test the operations used by the product, including repeated transitions and failure handling.

For example, a peripheral can work at initial boot and fail after a power cycle of its domain. This points toward state restoration, reset ordering or resource ownership. It is different from a driver that never bound. Preserve firmware and kernel messages around the transition.

Version information is useful for identifying the running implementation, but compatible version strings are not the entire configuration. Build options and platform data also influence which behavior is present. Keep the firmware ELF and configuration in the same release manifest.

## Diagnose missing firmware without guessing

First confirm which loading method the boot flow uses and which ELF it selects. Check the PMU console or other available execution evidence. Then confirm that the A53-side firmware interface is present and that its requests receive meaningful responses.

If services worked before a packaging change, inspect the packaged PMU firmware identity and boot-header fields. If they fail only under a debugger, inspect initialization order and target selection. If they fail after a hardware change, inspect platform policy and resource IDs.

Do not use an emulator's PMU firmware banner as evidence that a physical board's clocks, resets and power transitions have been validated. The emulator is valuable for sequencing and software-interface work, while the electrical and silicon behavior requires hardware testing.

**Evidence:** reference BIF, Bootgen header decode, and `boot-prebuilt3.log` launch arguments and PMU banner. PMU firmware replacement, both loading methods and runtime power-transition stress tests remain open.

## References

- `xilinx-zcu106-2024.1:pre-built/linux/images/bootgen.bif`
- AMD UG1283 (2024.1), PMU firmware loading examples
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/`

---

<sub>← [FSBL Stage](06-fsbl-stage.md) · [Chapter index](README.md) · [TF-A BL31 Stage](08-tfa-bl31-stage.md) →</sub>
