# TF-A Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot


## Runtime firmware between operating systems and the platform

**Trusted Firmware-A (TF-A)**, previously called ATF, supplies the EL3 runtime layer in the common ZynqMP A53 boot flow. EL3 is the highest exception level on the Cortex-A53. Linux normally runs in the Non-secure world at EL1, while the secure monitor remains available for defined firmware services.

TF-A is not finished when U-Boot starts. Linux later calls it for CPU power operations and platform services. Its code, stacks, translation tables and runtime state must remain valid for the whole period in which those calls are possible.

This lifetime explains a difficult failure pattern: boot succeeds, then CPU hotplug or suspend fails much later. The first boot path may not touch the same data that a later firmware call needs. An overwritten firmware region can therefore remain hidden until that call.

## Stage names describe roles

| Name | Role in this ZynqMP flow | Typical software |
| --- | --- | --- |
| BL31 | EL3 runtime firmware | TF-A |
| BL32 | Optional Secure payload | A trusted OS such as OP-TEE |
| BL33 | Non-secure next-stage image | U-Boot |

The platform uses its own BootROM and First Stage Boot Loader (FSBL) before BL31. A generic TF-A tutorial that builds and packages every TF-A boot stage does not directly describe the PetaLinux ZynqMP chain.

An image's stage identity is separate from its load address. The reference `bl31.elf` enters at `0xFFFEA000`. A TF-A console line can print the address of BL32 or BL33 rather than its own address. Always trace the printed variable before interpreting the number.

## What the secure monitor does during a call

A **Secure Monitor Call (SMC)** transfers control into the monitor under the Arm calling convention. The function identifier selects a service family and operation. Arguments arrive in defined registers, and return values use the corresponding result registers.

The monitor dispatches only supported operations. It does not grant the caller general Secure execution. A Linux root process still runs as a Non-secure userspace process; its driver can request a service, but the firmware must validate the request and enforce its own policy.

The implementation must preserve the required calling context and return to the correct security state and exception level. A custom service that corrupts saved state can fail after it appears to have completed its own register write.

## PSCI and platform-management paths

The **Power State Coordination Interface (PSCI)** defines standard processor-power operations. In the pinned ZynqMP platform code, `plat_psci.c` supplies operations such as power-domain on, off and suspend. These functions cooperate with PMU services for the platform work.

For example, `zynqmp_pwr_domain_on()` finds the target processor, prepares its platform wakeup and requests wakeup through `pm_req_wakeup()` using the secure entry point. The new CPU first needs the correct firmware entry path before it can reach its Non-secure software entry.

ZynqMP-specific platform services also exist. Linux's firmware driver builds a silicon-provider service identifier and calls TF-A through the conduit selected by the device tree. Some operations are answered in TF-A; others involve the PMU through inter-processor communication.

Do not use PSCI version discovery as proof that every platform service works. It verifies one interface boundary. Resource access policy, API support and PMU state can still make another request fail.

## The observed boot supports a limited conclusion

The saved reference U-Boot log reports `EL Level: EL2`. The Linux log reports PSCI discovery and that CPUs started at EL2. These observations are consistent with TF-A entering Non-secure U-Boot at EL2 and the bootloader entering Linux under the AArch64 protocol.

They do not show Linux's normal kernel execution remaining at EL2. They also do not prove authenticated boot. The same reference U-Boot log states that the boot is not authenticated and not encrypted. Execution privilege, TrustZone state and image authentication are different properties.

The reference BIF contains BL31 and U-Boot but no BL32 image. Therefore, the TF-A banner alone cannot establish that a trusted OS is present. The next section follows the source of the misleading-looking Secure-entry message.

## Trust also requires memory and bus policy

Keeping BL31 in a reserved memory range prevents a cooperating allocator from using that range. Hardware protection must enforce the intended access restrictions against Non-secure processors and other bus masters. Reservation and protection solve different problems.

A device tree can describe reserved memory for Linux, but it cannot by itself establish the whole TrustZone policy. Review the platform's memory and peripheral protection, DMA-capable devices and shared-memory design together with firmware placement.

Shared buffers passed to Secure services remain untrusted input. Validate addresses, lengths and arithmetic before access. If a value must stay stable during an operation, copy or otherwise protect the relevant data according to the service design; a prior range check does not stop the Non-secure side from changing its contents later.

## Compatibility is a set, not one banner

The local PetaLinux 2024.1 recipe selects TF-A version 2.10 from the AMD branch `xlnx_rebase_v2.10`, pinned to commit `4f82b6134e7b43722616c855e5016d42a3ea26d2`. That identifies the recipe input, while the deployed ELF and its build options identify the actual artifact.

Keep the FSBL handoff format, TF-A build, PMU firmware, U-Boot entry state and Linux firmware interface compatible. A new service may need changes at several boundaries. Updating only one component can leave an apparently healthy boot with broken runtime calls.

> [!NOTE]
> **Not run on the reference setup:** a new TF-A build, CPU hotplug stress, suspend/resume and physical Secure-memory isolation tests. The source flow and supplied boot evidence were inspected.

## References

- [2024.1 ZynqMP PSCI implementation](https://github.com/Xilinx/arm-trusted-firmware/blob/xilinx-v2024.1/plat/xilinx/zynqmp/plat_psci.c).
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/common/pm_service/{pm_svc_main.c,pm_api_sys.c}`.
- Local BSP: `meta-xilinx-core/recipes-bsp/arm-trusted-firmware/arm-trusted-firmware_2024.1.bb`.
- Saved `boot-manual-1.log`, `ttyPS1-tfa.log` and reference `bootgen.bif`.

---

<sub>[Chapter index](README.md) · [BL31 on ZynqMP](02-bl31-on-zynqmp.md) →</sub>
