# Cryptography Primer

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[25 · Security Fundamentals and Cryptography](README.md)** · Part XIV: Security

## Different tools solve different problems

| Primitive | Main use | Common mistake |
| --- | --- | --- |
| Symmetric encryption, such as AES | Confidentiality with a shared secret | Treating encryption alone as integrity |
| Hash, such as SHA-2/SHA-3 | Digest of data | Assuming anyone's digest authenticates a file |
| MAC/HMAC | Integrity/authenticity with a shared secret | Sharing one key with too many roles |
| RSA/ECDSA signature | Verification using a public key | Failing to protect the trusted public key |
| ECDH | Establishing shared secret material | Omitting peer authentication |
| Key derivation function | Deriving purpose-specific keys | Reusing raw input as several unrelated keys |

CBC and CTR require a complete authenticated design around them. GCM provides authenticated encryption, but nonce reuse under the same key can destroy its security. Follow the protocol's nonce and length requirements.

## Randomness and implementation

Use the operating system's cryptographic random interface and established libraries. Do not seed keys from a timestamp or device serial number. Separate keys by purpose, and verify authentication before using plaintext as trusted data.

Algorithm names are not a complete protocol. Formats, padding, validation, key storage and failure behavior matter as much as selecting AES or RSA.

## References

- NIST FIPS 197, FIPS 180-4 and FIPS 202
- [NIST SP 800-38D, GCM](https://csrc.nist.gov/pubs/sp/800/38/d/final)

---

<sub>← [Security Principles and Threat Modeling](01-security-principles-and-threat-modeling.md) · [Chapter index](README.md) · [PKI and Certificates](03-pki-and-certificates.md) →</sub>
