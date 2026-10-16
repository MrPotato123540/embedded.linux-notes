# Hardware Security Features

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Hardware building blocks

ZynqMP's Configuration Security Unit provides boot-security functions using AES-GCM, RSA and SHA-3-related hardware. Device key storage and policy involve eFUSE, battery-backed RAM (**BBRAM**) and supported Physical Unclonable Function (**PUF**) flows.

These blocks have different roles. Authentication checks approved origin and integrity. Encryption protects confidentiality. Runtime isolation uses processor security state and protection units such as XMPU/XPPU.

## System policy

A secure product also needs debug-port policy, update verification, key lifecycle and error response. Closing JTAG does not fix an unauthenticated network update, and secure boot does not remove runtime driver bugs.

Review silicon revision and the exact device documentation before choosing key sources or programming controls. Some settings are irreversible and some recovery paths depend on the initial provisioning plan.

> [!NOTE]
> **Not run on the reference setup:** silicon security provisioning, tamper response and protected debug behavior.

## Follow an asset through the hardware

Consider a product whose PL design contains a valuable signal-processing algorithm. The boot medium holds firmware, a bitstream and Linux files. Three different questions apply. Can an attacker read the algorithm from storage? Can they replace the design with another one? Can a Linux process read or change protected memory after boot?

Encryption addresses the first question. Signature verification addresses the second. Memory and peripheral access controls address the third. Each needs its own keys, policy and test evidence. An encrypted bitstream can still expose a powerful DMA interface after it loads. A signed driver can still contain a bounds-checking bug.

The Configuration Security Unit (CSU) is part of the early hardware trust boundary. Its BootROM code starts before the replaceable FSBL. The CSU security engines support the device-specific authentication and decryption flows. Bootgen prepares the matching data structures on the host. The host tool does not program the device's security policy merely by generating an image.

This split gives you two independent inputs to a boot decision: image metadata and device state. The image can request authentication, but a production device must also reject an image that tries to avoid required authentication. Inspect both sides when reviewing a design.

## Separate the control planes

| Control plane | Important state | What a review must establish |
| --- | --- | --- |
| Boot acceptance | Trusted key hashes, security policy, partition attributes | Unapproved code cannot become the next trusted stage |
| Confidentiality | AES key source and encrypted partition format | Protected bytes are readable only through the intended flow |
| Processor isolation | Secure/Non-secure state and memory mappings | Normal-world software cannot directly access Secure resources |
| Bus access | XMPU/XPPU configuration and relevant master identities | Other processors and DMA masters obey the resource policy |
| Debug and recovery | Debug access, boot modes, maintenance credentials | Service paths preserve the same trust requirements |

An exception level is a CPU privilege level. TrustZone security state is a separate property. Linux running at Non-secure EL1 does not become Secure because it has a root user. Likewise, an IOMMU mapping for a DMA device is not the same object as a CPU page-table mapping. See [exception levels](../03-zynqmp-architecture/10-exception-levels-and-trustzone.md) and [interconnect protection](../03-zynqmp-architecture/06-interconnect-coherency-and-smmu.md).

The Xilinx Memory Protection Unit (XMPU) protects memory regions using the supported access attributes. The Xilinx Peripheral Protection Unit (XPPU) controls peripheral access. These controls need a defined owner. If less-trusted code can later widen the policy, the initial configuration has a limited lifetime. Review which firmware can change it and which reset clears it.

## Isolation must survive transitions

A typical failure appears during an otherwise normal operation. Linux stops a PL accelerator, the system loads a new partial bitstream, and the new hardware begins DMA. A policy that covered only the original accelerator may now be wrong. The DFX manager must coordinate hardware identity, address permissions, buffers and driver ownership.

Power management creates another transition. A powered-down block may lose configuration. Restoring its clock does not prove that protection registers were restored before traffic resumed. Firmware must restore the required policy in the right order. This is why a cold-boot security test cannot replace suspend/resume or subsystem-reset tests.

Shared memory needs a precise purpose. A Linux-to-RPU buffer may be intentionally accessible to both sides, while firmware code and keys remain private. Describe separate regions for executable code, shared descriptors and payload data. Avoid a single large shared region simply because it makes address translation easier.

## Key storage is not a complete key service

eFUSE and BBRAM can provide supported hardware key sources. They are not general filesystems for application secrets. A Linux application cannot assume that a boot-encryption key is available as a general AES service. That depends on the documented firmware interfaces and the selected access policy.

A Physical Unclonable Function (PUF) supports device-bound key protection through a defined enrollment and reconstruction flow. Helper data participates in that flow. Its availability, integrity requirements and recovery handling belong in the product design. Losing required helper data can prevent key reconstruction even though the silicon is intact.

Do not reduce physical attack resistance to one feature name. Debug policy, power behavior, board access and the lifetime of plaintext copies also matter. Set the threat model first; then identify which supported mechanism addresses each attack capability.

## Evidence for a security claim

For each protected resource, record an allowed requester, a denied requester and the stage that installs the rule. A useful test observes both successful authorized use and rejected unauthorized use. A failed access alone is weak evidence: the device might simply be held in reset.

For example, a denied DMA write is meaningful only after you establish that the engine is clocked, configured and able to write an allowed buffer. Compare the allowed and denied cases with the same engine and transfer size. Keep the access-fault evidence alongside buffer contents and firmware logs.

These are proposed board tests. QEMU boot logs establish software flow for the reference image; they do not establish silicon enforcement, PUF behavior or physical attack resistance. The hardware feature descriptions here follow UG1085's CSU and protection-unit chapters, while the exact image format follows UG1283 2024.1.

## References

- UG1085 (v2.5), CSU and security chapters
- AMD UG1283 (2024.1), ZynqMP authentication/encryption

---

<sub>[Chapter index](README.md) · [Chain of Trust](02-chain-of-trust.md) →</sub>
