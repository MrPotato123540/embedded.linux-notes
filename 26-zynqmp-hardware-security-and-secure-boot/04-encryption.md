# Boot Image Encryption (AES-GCM)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Encryption and key sources

Boot encryption protects partition confidentiality according to the supported ZynqMP flow. Key material can use BBRAM, eFUSE or supported wrapped-key arrangements. The BIF, device state and provisioning data must agree.

A red key is plaintext key material. A black key is protected using the supported PUF-derived wrapping flow. A gray/obfuscated key uses a different device-family protection mechanism; it is not another name for a PUF-wrapped black key. Check the exact supported mode and its security properties before choosing it.

Operational keys and key rolling limit how key material is used across a protected image. They require correct generation and metadata handling. Never invent an IV/nonce scheme or reuse key files without understanding the tool's requirements.

## Bitstreams

Encrypted programmable-logic content must be loaded through a path supporting its security format and key source. A normal raw-bitstream loading example is not automatically valid for an encrypted image.

> [!NOTE]
> **Not run on the reference setup:** encrypted boot or encrypted PL configuration.

## References

- AMD UG1283 (2024.1), Encrypting Zynq MPSoC Device Partitions, Operational Key, Black/PUF Keys and Gray/Obfuscated Keys

---

<sub>← [Boot Image Authentication (RSA)](03-authentication.md) · [Chapter index](README.md) · [eFUSE and BBRAM Programming](05-efuse-and-bbram-programming.md) →</sub>
