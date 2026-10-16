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

## What the encrypted container must agree on

AES-GCM combines encryption with an authentication tag. ZynqMP's boot format defines how protected data, keys, initialization vectors and headers reach the device. The AES key size in this flow is 256 bits. The boot container is not equivalent to an arbitrary file encrypted by a desktop AES command.

For decryption to work, the image's selected key source must match the device state. The image format must also match the loading path. A correct secret with the wrong source selection is still a failed integration. An encrypted partition that can be processed during boot is not automatically supported by every later Linux FPGA-loading interface.

Keep three records together: the exact encrypted image digest, the non-secret identity of the intended key/provisioning batch, and the BIF/tool version that produced the image. The key itself belongs in the controlled key system. Build logs should not become a second key store.

## Red, black and gray describe different protection

| Form | Meaning in the supported flow | Design consequence |
| --- | --- | --- |
| Red key | Plaintext secret key material | Any exported copy needs direct confidentiality protection |
| Black key | Key protected through the supported PUF-based wrapping flow | Enrollment, helper data and device binding affect recovery |
| Gray key | Key obfuscated using the device-family mechanism | Do not describe it as a unique per-device PUF key |

UG1283 2024.1 explains that the gray-key mechanism uses a family key built into the device family. That distinction matters when choosing a threat model: family-level obfuscation and device-bound wrapping are different security properties. Neither name tells you which software is allowed to request use of the key after boot.

A wrapped key also needs metadata and a compatible unwrap path. Copying only the encrypted key bytes into an image does not recreate the enrollment state. Treat provisioning records and helper-data lifecycle as part of the design, while keeping secrets out of ordinary logs.

## Read the host implementation before changing key files

The source `bootgen@xilinx_v2024.1:encryption-zynqmp.cpp` gives concrete checks. `ZynqMpEncryptionContext::GetEncryptionKeys()` requires the base AES key and IV. If the operational-key option is enabled, it also requires the corresponding operational key. Missing inputs cause explicit errors instead of silently selecting a different mode.

The file also checks key/IV relationships across the image's `.nky` files and calls `CheckForRepeatedKeyIVPairs()`. In the inspected path, `Key 0`, `IV 0` and an enabled operational key must follow the shared values expected by the format. These are format-level rules. They are not permission to reuse the same effective GCM key/nonce pair for unrelated encryptions.

This is an important distinction for release automation. A script that creates every partition's key file independently may violate the boot-format relationship. A script that blindly copies an old key file may violate the intended cryptographic lifecycle. Use the supported Bootgen generation flow and preserve its diagnostics rather than editing generated cryptographic fields by hand.

## Key rolling and operational keys

Key rolling changes the encryption key across protected blocks according to the supported image format. An operational key adds another level to the key-use design. Their purpose is to control how long and where a key is used; they do not remove the need to protect the root key or validate the image's origin.

The block layout, next-key information and authentication data must remain consistent. A change to payload size can change the protected structure. Rebuild the encrypted container after a firmware change; do not patch bytes inside the old ciphertext or assume an old signature remains valid.

Think about build reproducibility separately from ciphertext equality. A reproducible plaintext build can legitimately produce different protected containers when fresh cryptographic material is generated. Archive the unsigned artifact digest and the final protected artifact digest. This lets you distinguish a source/build change from a protection-stage change without exposing secrets.

## Diagnose without destroying the evidence

Suppose authentication succeeds but the encrypted partition does not load. Narrow the problem in order. Check the intended key-source selection, the provisioning batch, the encrypted partition attributes and the loading interface. Then inspect the stage's documented decryption error. Do not immediately reprogram key storage: that can remove the state needed to explain the original failure.

Another useful comparison is warm reset versus full power loss. A BBRAM-related problem may depend on key retention or board power conditions. Record how power was removed and whether the backup supply was present. A warm reset that works does not establish retention across the product's shipping and service conditions.

For PL content, keep the generated bitstream type and wrapper information. A `.bit` header, raw configuration bytes and an authenticated/encrypted boot partition serve different consumers. File extensions alone cannot establish compatibility. Follow [bitstream formats](../07-boot-images-and-bootgen/04-bitstreams.md) and the selected firmware/FPGA-manager interface.

## What the existing tests prove

The [cryptography lab](../25-security-fundamentals-and-cryptography/02-cryptography-primer.md) demonstrates generic AES-GCM rejection of changed tags and associated context. The [Bootgen lab](03-authentication.md) demonstrates RSA partition verification. Neither exercised a ZynqMP AES key source, PUF reconstruction, encrypted boot or encrypted PL configuration.

Those remaining tests require the intended hardware and a reviewed provisioning plan. Their success criteria must include correct decryption, rejection of incompatible input, power-cycle behavior and a usable recovery path. Keep this distinction in the release report so host experiments do not become accidental claims about silicon security.

## References

- `bootgen@xilinx_v2024.1:encryption-zynqmp.cpp`, key loading and image consistency checks

- AMD UG1283 (2024.1), Encrypting Zynq MPSoC Device Partitions, Operational Key, Black/PUF Keys and Gray/Obfuscated Keys

---

<sub>← [Boot Image Authentication (RSA)](03-authentication.md) · [Chapter index](README.md) · [eFUSE and BBRAM Programming](05-efuse-and-bbram-programming.md) →</sub>
