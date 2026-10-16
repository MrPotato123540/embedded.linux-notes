# 26 · ZynqMP Hardware Security and Secure Boot

**Part XIV: Security** · Work package [WP-26](../ROADMAP.md#wp-26) · Status: 👀 In review

The root of trust, boot image authentication and encryption, eFUSE/BBRAM, and an end-to-end chain of trust from the BootROM to the root filesystem.

**Prerequisites:** [06 · Boot Sequence](../06-boot-sequence/README.md) · [07 · Boot Images, BIF and Bootgen](../07-boot-images-and-bootgen/README.md) · [25 · Security Fundamentals and Cryptography](../25-security-fundamentals-and-cryptography/README.md)

All eight sections have advanced-depth revisions covering hardware policy, handoff trust, RSA verification, encrypted-image structure, provisioning, verified Linux boot and TEE boundaries. Bootgen 2024.1 accepted a signed host fixture and rejected a changed payload. Hardware secure boot, key provisioning and isolation tests remain open.

## Sections

| # | Section | Status |
| ---: | --- | --- |
| 1 | [Hardware Security Features](01-hardware-security-features.md) | 👀 In review |
| 2 | [Chain of Trust](02-chain-of-trust.md) | 👀 In review |
| 3 | [Boot Image Authentication (RSA)](03-authentication.md) | 👀 In review |
| 4 | [Boot Image Encryption (AES-GCM)](04-encryption.md) | 👀 In review |
| 5 | [eFUSE and BBRAM Programming](05-efuse-and-bbram-programming.md) | 👀 In review |
| 6 | [Secure Boot With PetaLinux](06-secure-boot-in-petalinux.md) | 👀 In review |
| 7 | [Verified Boot Beyond U-Boot](07-verified-boot-beyond-u-boot.md) | 👀 In review |
| 8 | [TrustZone and OP-TEE](08-trustzone-and-op-tee.md) | 👀 In review |

---

<sub>← [25 · Security Fundamentals and Cryptography](../25-security-fundamentals-and-cryptography/README.md) · [Guide contents](../README.md#contents) · [27 · Linux and Network Security](../27-linux-and-network-security/README.md) →</sub>
