# Chain of Trust

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Trust must continue through every stage

A **root of trust** is the starting point whose behavior and trust material the design relies on. Each verified stage must authenticate the next stage before giving it control or trusting its data.

For a ZynqMP Linux product, examine the whole path: BootROM → FSBL → resident firmware/U-Boot → kernel/device tree/initramfs → root filesystem and application. The exact verifier for each partition depends on the supported boot flow.

A signed `BOOT.BIN` does not automatically authenticate a kernel later loaded from a writable SD partition. A trusted kernel also needs a policy for modules, rootfs integrity and mutable configuration.

## Verified and measured boot

Verified boot enforces an acceptance decision. Measured boot records evidence of what was loaded for later assessment. Recording a hash without a trusted reference or attestation design does not stop an unapproved image from running.

Define rollback policy as well as signature policy. An old vulnerable image can have a valid signature.

## References

- AMD UG1283 (2024.1), boot-time security
- [Verified boot beyond U-Boot](07-verified-boot-beyond-u-boot.md)

---

<sub>← [Hardware Security Features](01-hardware-security-features.md) · [Chapter index](README.md) · [Boot Image Authentication (RSA)](03-authentication.md) →</sub>
