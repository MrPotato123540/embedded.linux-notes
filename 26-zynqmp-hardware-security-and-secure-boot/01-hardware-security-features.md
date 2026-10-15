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

## References

- UG1085 (v2.5), CSU and security chapters
- AMD UG1283 (2024.1), ZynqMP authentication/encryption

---

<sub>[Chapter index](README.md) · [Chain of Trust](02-chain-of-trust.md) →</sub>
