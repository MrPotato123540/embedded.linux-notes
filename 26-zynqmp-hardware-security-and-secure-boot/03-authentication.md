# Boot Image Authentication (RSA)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Key hierarchy

ZynqMP authentication uses a primary/secondary key hierarchy. **PPK** and **SPK** mean Primary Public Key and Secondary Public Key. Their private counterparts sign the required structures. Device policy can anchor the primary public-key hash in eFUSE and apply supported revocation controls.

Keep the primary signing authority separated from routine release signing where the chosen flow permits. Record key selection, identifiers and revocation state with the device provisioning record.

## BIF and verification

Bootgen authentication attributes select the image's signed structure and key inputs. Use the ZynqMP-specific format; a generic OpenSSL signature is not a replacement for the required boot certificate layout.

Boot-header authentication can support development without the same eFUSE trust enforcement used in production. Do not describe that test mode as equivalent to a provisioned hardware root of trust.

Test a valid image, modified payload, incorrect key and revoked-key case using disposable test devices and keys. A successful valid-image boot tests only the positive path.

> [!NOTE]
> **Not run on the reference setup:** authenticated boot and revocation tests.

## References

- AMD UG1283 (2024.1), ZynqMP Authentication Support, PPK/SPK and authentication examples

---

<sub>← [Chain of Trust](02-chain-of-trust.md) · [Chapter index](README.md) · [Boot Image Encryption (AES-GCM)](04-encryption.md) →</sub>
