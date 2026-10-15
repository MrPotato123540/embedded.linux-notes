# Exception Levels and TrustZone

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · Cortex-A53 application processors

**[03 · Zynq UltraScale+ MPSoC Architecture](README.md)** · Part II: Zynq UltraScale+ MPSoC Hardware

## In short

- An **exception level (EL)** controls which CPU operations software can use.
- **Secure** and **Non-secure** are separate security states. A higher exception level does not automatically mean Secure state.
- Linux applications, the Linux kernel, a hypervisor and trusted firmware have different roles and levels.
- Boot logs show the level used to enter Linux. This can differ from the level used during normal kernel operation.

## Concepts

### Exception levels on the Cortex-A53

The **application processing unit (APU)** contains Cortex-A53 cores. Each core supports four exception levels. The table describes the usual AArch64 software arrangement on Zynq UltraScale+ MPSoC (ZynqMP).

| Level | Typical software | Purpose |
| --- | --- | --- |
| EL0 | Linux applications | Run programs with access controlled by the kernel |
| EL1 | Linux kernel | Manage processes, virtual memory and device drivers |
| EL2 | Hypervisor, such as Xen | Control virtual machines |
| EL3 | Trusted Firmware-A (TF-A), previously called ATF | Provide the secure monitor and runtime firmware services |

The **First Stage Boot Loader (FSBL)** normally runs at Secure EL3 in the A53 boot flow. U-Boot normally runs at Non-secure EL2 before it starts Linux. These levels describe the A53 flow; the Cortex-R5 and the MicroBlaze processors do not use this EL0–EL3 model. See AMD's [Linux Software Stack, UG1137 (2024.1)](https://docs.amd.com/r/2024.1-English/ug1137-zynq-ultrascale-mpsoc-swdev/Linux-Software-Stack).

An exception transfers control to a handler. A system call lets an application request a kernel service. An interrupt lets hardware request attention. Neither gives the application permanent kernel privileges.

### Security state is a separate choice

TrustZone separates Secure and Non-secure execution. On the Cortex-A53, EL0 and EL1 can exist in either state. EL2 is Non-secure, and EL3 is Secure. Secure EL2 belongs to later Arm architecture extensions; it is not available on this processor.

Linux normally uses Non-secure EL1. A root shell still runs at Non-secure EL0. The kernel checks its user identity and permissions when it requests a service. Becoming root does not move the shell into the Secure world.

The secure monitor manages transitions between worlds. A firmware call enters a defined service; it does not let the caller run arbitrary Secure code. See Arm's [TrustZone for Armv8-A (v1.0), sections 3.1, 3.2, 3.7 and 3.8](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/TrustZone%20for%20Armv8-A.pdf).

## On ZynqMP

### Where TF-A and OP-TEE fit

TF-A supplies the EL3 runtime layer on ZynqMP. **BL31** is the TF-A stage. **BL32** is an optional Secure payload. **BL33** is the Non-secure software, usually U-Boot in this flow. The FSBL passes image information to TF-A so it can enter the next software stage. See [TF-A v2.10, ZynqMP platform documentation](https://trustedfirmware-a.readthedocs.io/en/v2.10/plat/xilinx-zynqmp.html).

**OP-TEE (Open Portable Trusted Execution Environment)** can provide a Secure operating system at EL1. Trusted applications run at Secure EL0. A Linux client requests a service through the Linux TEE driver. The request then passes through the secure monitor to OP-TEE. Shared memory carries request data between the two worlds; the Secure service must check that data before using it. See the [OP-TEE core architecture](https://optee.readthedocs.io/en/latest/architecture/core.html).

OP-TEE is optional. A working TF-A boot does not prove that an OP-TEE image was loaded. This section does not assume that the reference image includes it.

### How Linux reaches firmware

Two instructions are relevant here:

| Instruction | Full name | Role in this software stack |
| --- | --- | --- |
| SMC | Secure Monitor Call | Request a service from EL3 firmware; a hypervisor may intercept the call |
| HVC | Hypervisor Call | Request a service from an EL2 hypervisor |

The PetaLinux 2024.1 ZynqMP firmware driver selects its call method from the device tree. In `drivers/firmware/xilinx/zynqmp.c`, `do_fw_call_smc()` uses `arm_smccc_smc()`, while `do_fw_call_hvc()` uses `arm_smccc_hvc()`. Here **SMCCC** means SMC Calling Convention: the rules for passing function identifiers, arguments and results. See the [pinned 2024.1 driver](https://raw.githubusercontent.com/Xilinx/linux-xlnx/xilinx-v2024.1/drivers/firmware/xilinx/zynqmp.c).

The **Power State Coordination Interface (PSCI)** supplies standard CPU power services. ZynqMP also has platform management services. They use separate device-tree nodes even when both use SMC.

The saved reference device tree contains these two settings (trimmed from `reference-setup/captures/system.dts`):

```dts
psci {
    compatible = "arm,psci-0.2";
    method = "smc";
};
```

The node `/firmware/zynqmp-firmware` also has `method = "smc"`. These are observations from the saved BSP image, not settings that every guest should copy. Changing a guest to `hvc` only works if its hypervisor provides the required service.

### Memory and peripheral protection

TrustZone also affects system transactions. A request carries a security attribute, and the hardware checks whether the destination allows that access. CPU privilege alone does not describe the whole access path: other bus masters can access memory too. See Arm's [TrustZone system architecture, section 4](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/TrustZone%20for%20Armv8-A.pdf).

On ZynqMP, review the **Xilinx Memory Protection Unit (XMPU)** and **Xilinx Peripheral Protection Unit (XPPU)** settings as part of this design. The [interconnect and protection section](06-interconnect-coherency-and-smmu.md) explains the platform mechanisms and cites UG1085. Memory reserved in a Linux device tree still needs the appropriate hardware protection if it must be hidden from Non-secure bus masters.

## Hands-on: reading the saved boot evidence

These excerpts come from the existing reference captures. They were not captured again during this section's writing.

The U-Boot banner in `reference-setup/captures/boot-manual-1.log` includes:

```text
EL Level:	EL2
Secure Boot:	not authenticated, not encrypted
```

Later in the same boot, Linux reports:

```text
[    0.000000] psci: PSCIv1.1 detected in firmware.
[    0.000000] psci: Using standard PSCI v0.2 function IDs
[    0.000000] psci: MIGRATE_INFO_TYPE not supported.
[    0.000000] psci: SMC Calling Convention v1.4
```

It also reports:

```text
[    0.070889] CPU: All CPU(s) started at EL2
```

The last line describes the CPU entry level. It does **not** say that the normal Linux kernel stays at EL2. On Cortex-A53, normal kernel execution is at EL1; virtualization support can use EL2 separately. The AArch64 boot protocol allows entry at Non-secure EL1 or EL2 and recommends EL2 when available. See [Linux 6.6: Booting AArch64 Linux, “CPU mode”](https://docs.kernel.org/6.6/arch/arm64/booting.html).

The PSCI lines show that firmware reports version 1.1 while keeping the standard function identifiers introduced in version 0.2. The device-tree compatible string and the reported runtime version answer different questions.

> [!NOTE]
> **Not run on the reference setup:** an OP-TEE service call, a guest using HVC, and hardware tests of Secure memory or peripheral access. The saved QEMU logs show the boot arrangement, but do not validate physical isolation.

## PetaLinux 2024.1 specifics

When you change the boot arrangement, review the parts together:

1. The boot image must contain the required firmware and software images.
2. The handoff must use the security state and exception level expected by each image.
3. The device-tree call method must match the available firmware or hypervisor interface.
4. Memory used by resident firmware must stay available to that firmware after Linux starts.

For implementation details, continue with [the boot sequence](../06-boot-sequence/README.md), [TF-A](../10-trusted-firmware-a/README.md) and [TrustZone and OP-TEE](../26-zynqmp-hardware-security-and-secure-boot/08-trustzone-and-op-tee.md). These chapters now contain written material; their hardware validation notes remain open.

## Pitfalls and debugging

| Symptom or assumption | What to check |
| --- | --- |
| “Root can read every physical address” | Linux permissions, address mappings and hardware access policy are separate checks |
| “Started at EL2 means Linux stays at EL2” | Separate kernel entry from normal execution |
| Firmware calls fail after adding a hypervisor | Compare the guest call method with the services the hypervisor provides |
| TF-A starts, but a Secure application is unavailable | Check that the Secure payload was built, loaded and initialized |
| “EL3 proves secure boot is enabled” | Check boot authentication separately; the saved image reaches this software stack without authenticated boot |

## References

- AMD, [UG1137 (2024.1), Linux Software Stack](https://docs.amd.com/r/2024.1-English/ug1137-zynq-ultrascale-mpsoc-swdev/Linux-Software-Stack)
- Arm, [TrustZone for Armv8-A (v1.0)](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/TrustZone%20for%20Armv8-A.pdf), sections 3 and 4
- [TF-A v2.10: ZynqMP platform](https://trustedfirmware-a.readthedocs.io/en/v2.10/plat/xilinx-zynqmp.html), runtime stages and FSBL parameter passing
- [OP-TEE core architecture](https://optee.readthedocs.io/en/latest/architecture/core.html), execution levels and shared memory; used for architecture, not a claim about the BSP's OP-TEE version
- `linux-xlnx@xilinx-v2024.1:drivers/firmware/xilinx/zynqmp.c`, firmware call wrappers and probe method selection
- [Linux 6.6 AArch64 boot protocol](https://docs.kernel.org/6.6/arch/arm64/booting.html), CPU entry mode
- Saved reference evidence outside the guide repository: `reference-setup/captures/boot-manual-1.log`, `system.dts` and `ttyPS1-tfa.log`

---

<sub>← [Peripherals, MIO and EMIO](09-peripherals-mio-emio.md) · [Chapter index](README.md) · Next chapter: [04 · The Yocto Project](../04-yocto-project/README.md) →</sub>
