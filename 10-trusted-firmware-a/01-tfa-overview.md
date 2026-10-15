# TF-A Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot

## Boot-stage names

Trusted Firmware-A (**TF-A**, previously called ATF) provides trusted boot and runtime components. On ZynqMP, the platform's BootROM and FSBL perform the early boot roles; the main TF-A component used by the normal Linux flow is BL31.

| Name | Role in this flow |
| --- | --- |
| BL1/BL2 | Early boot roles supplied by the platform ROM and FSBL |
| BL31 | EL3 runtime firmware |
| BL32 | Optional Secure payload, such as a trusted OS |
| BL33 | Non-secure payload, commonly U-Boot |

BL31 remains resident. It handles defined monitor services when Non-secure software requests them. The **SMC Calling Convention (SMCCC)** defines how callers pass function identifiers, arguments and results. It is an interface contract, not permission to execute arbitrary Secure code.

## Version selection

The reference release uses TF-A 2.10 with AMD's platform changes. Pin the AMD `xilinx-v2024.1` source and recipe revision when reproducing the image. An upstream 2.10 tag and an AMD build with the same base version are not automatically identical.

## References

- TF-A v2.10 [ZynqMP port](https://trustedfirmware-a.readthedocs.io/en/v2.10/plat/xilinx-zynqmp.html)
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/`
- Saved TF-A console log

---

<sub>[Chapter index](README.md) · [BL31 on ZynqMP](02-bl31-on-zynqmp.md) →</sub>
