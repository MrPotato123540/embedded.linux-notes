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

## Start from the acceptance decision

Suppose a device receives an update payload and a digest. Recomputing the digest detects a transfer error if the expected digest is trustworthy. If an attacker can replace both payload and digest, the same calculation accepts the attacker's pair. A bare hash therefore identifies content; it does not identify who approved it.

A message authentication code adds a secret key to the acceptance decision. HMAC lets parties sharing that key detect unauthorized changes. Every party that can create a valid HMAC can also impersonate another holder of the same key. A shared fleet-wide key therefore creates a broad compromise domain.

A digital signature separates signing authority from verification. Devices can verify with a public key without receiving the private signing key. The device must still trust that public key and restrict what the signer is authorized to approve. Replacing both an image and its public key defeats verification unless the key is anchored elsewhere.

## Authenticate context as well as payload

An update can be valid for one board and dangerous for another. A command can be valid in a test role and invalid in a production role. Bind these meanings into the authenticated data, using a defined encoding. Ambiguous concatenation can make two different field combinations produce the same byte string.

Authenticated encryption with associated data (**AEAD**) protects plaintext confidentiality and checks integrity of both ciphertext and associated context. Associated data is authenticated but remains visible. Device type, protocol version and message role are examples of context, provided the protocol defines their encoding and validation.

Acceptance must precede use of the plaintext as trusted input. A streaming decryption interface can produce bytes before final authentication succeeds; the application must not apply their effects early. An API that returns plaintext only after tag verification makes this boundary easier to maintain.

## Nonce uniqueness is a lifecycle requirement

A nonce distinguishes encryption operations under a key. AES-GCM requires a suitable unique nonce for each encryption with that key. Reusing a nonce can break confidentiality and authentication, even if the plaintexts differ only slightly.

A counter design must survive crashes, concurrent writers and restore from backups. A random design needs a collision budget and sound randomness. Key rotation can change the nonce domain, but rotating only a visible key identifier while reusing the same underlying key does not create a new domain.

The teaching example below encrypts exactly once under a fresh in-memory key and uses a fresh 12-byte nonce. That simple lifecycle is deliberate. It is not a persistence scheme for a device that encrypts millions of messages across restarts.

## Executed API experiment

The repository contains [crypto_boundaries.py](examples/crypto_boundaries.py). It uses Python's standard hash/HMAC interfaces and the installed `cryptography` library. All keys are created in memory for the run; it writes no files and touches no hardware or network.

```console
$ python3 25-security-fundamentals-and-cryptography/examples/crypto_boundaries.py
PASS: a payload change changes its SHA-256 digest
PASS: HMAC accepts the original bytes with the same key
PASS: HMAC rejects changed bytes against the original tag
PASS: AES-GCM accepts the original ciphertext and context
PASS: AES-GCM rejects a modified authentication tag
PASS: AES-GCM rejects the wrong associated context
PASS: AES-GCM rejects truncated input
PASS: RSA-PSS accepts the original signed bytes
PASS: RSA-PSS rejects changed signed bytes
PASS: RSA-PSS rejects the wrong verification key
```

This was run with `cryptography` 3.4.8 on the host. It checks API behavior and the application's acceptance boundaries. It is not a proof of the algorithms, a performance measurement or a test of ZynqMP crypto hardware.

The RSA-PSS example uses a temporary 2048-bit RSA key and SHA-256. This teaching choice is **not** the ZynqMP BootROM certificate format or key-size requirement. ZynqMP boot authentication uses its own supported RSA-4096 format, discussed in the next chapter.

## Key derivation and purpose separation

A key derivation function converts suitable input key material into keys for defined uses. Include a context that separates roles such as transport encryption, storage encryption and authentication. Reusing one raw key everywhere couples the compromise of otherwise separate interfaces.

A password is not uniformly random key material. Password-based derivation needs an appropriate password-hardening design and parameters. Applying a fast ordinary hash once to a password does not create the same protection as a purpose-designed password KDF.

A salt is usually public and helps separate derivations or precomputation domains. A nonce is usually public and serves a protocol-specific uniqueness requirement. Neither should be confused with the secret key. Their exact requirements come from the selected construction.

## Errors and implementation details matter

Use established high-level library interfaces instead of implementing padding, tag comparison or elliptic-curve arithmetic in application code. Compare authentication values with the library's intended verification function; an ordinary early-exit byte comparison can reveal information through timing.

Handle authentication failure as a normal invalid-input result without leaking partial plaintext. Bound input sizes before expensive cryptographic work so a valid algorithm does not become an easy resource-exhaustion path. Avoid error messages that expose secret-dependent internal state.

Finally, separate correctness tests from security assurance. Known-answer and negative tests can detect integration errors. They cannot establish resistance to every side channel, weak entropy source or compromised key store. Those require their own analysis and evidence.

## References

- NIST FIPS 197, FIPS 180-4 and FIPS 202
- [NIST SP 800-38D, GCM](https://csrc.nist.gov/pubs/sp/800/38/d/final)

---

<sub>← [Security Principles and Threat Modeling](01-security-principles-and-threat-modeling.md) · [Chapter index](README.md) · [PKI and Certificates](03-pki-and-certificates.md) →</sub>
