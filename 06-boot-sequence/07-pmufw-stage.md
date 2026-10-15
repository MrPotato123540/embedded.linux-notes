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

## References

- `xilinx-zcu106-2024.1:pre-built/linux/images/bootgen.bif`
- AMD UG1283 (2024.1), PMU firmware loading examples
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/`

---

<sub>← [FSBL Stage](06-fsbl-stage.md) · [Chapter index](README.md) · [TF-A BL31 Stage](08-tfa-bl31-stage.md) →</sub>
