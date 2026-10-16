# PKI and Certificates

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[25 · Security Fundamentals and Cryptography](README.md)** · Part XIV: Security

## Certificate meaning

An X.509 certificate binds a public key to identity information under an issuer's signature. A **Certificate Authority (CA)** issues certificates. A **Certificate Signing Request (CSR)** asks for issuance and proves possession of the corresponding private key.

Validation checks the trust chain, validity period, intended use and requested identity. Revocation requires a defined mechanism and freshness policy. A certificate being parseable does not mean it is trusted.

## Recorded host experiment

A temporary self-signed certificate for `guide-demo.invalid` was created in `/tmp/guide-pki-lab`. Its private key stayed outside the repository. It is a one-day test fixture, not a production CA.

The following preparation commands were also run on the host. The key is deliberately temporary and unencrypted for this local exercise; it must not be used for a product identity or release signing.

```bash
mkdir -p /tmp/guide-pki-lab
openssl req -x509 -newkey rsa:2048 -sha256 -nodes \
  -keyout /tmp/guide-pki-lab/demo.key \
  -out /tmp/guide-pki-lab/demo.crt -days 1 \
  -subj '/CN=guide-demo.invalid' \
  -addext 'subjectAltName=DNS:guide-demo.invalid'
chmod 600 /tmp/guide-pki-lab/demo.key
```

```console
$ openssl verify -CAfile /tmp/guide-pki-lab/demo.crt -verify_hostname guide-demo.invalid /tmp/guide-pki-lab/demo.crt
/tmp/guide-pki-lab/demo.crt: OK
$ openssl verify -CAfile /tmp/guide-pki-lab/demo.crt -verify_hostname wrong.invalid /tmp/guide-pki-lab/demo.crt
CN = guide-demo.invalid
error 62 at 0 depth lookup: hostname mismatch
error /tmp/guide-pki-lab/demo.crt: verification failed
```

The first command explicitly trusts the test certificate. It does not establish trust from a public CA. The second demonstrates that identity checking is separate from trusting the issuer.

## Certificate parsing is only the first step

A certificate is a signed statement with a public key, issuer, subject and extensions. Reading those fields proves that the object is syntactically understandable. Trust requires a path to a configured trust anchor and successful policy checks.

The trust anchor is chosen by the relying system. It is not made trustworthy merely by being self-signed or arriving in the peer's certificate chain. In the recorded experiment, `-CAfile` explicitly supplies the test certificate as trusted input. That is why the result demonstrates a local test policy rather than public identity verification.

A server normally sends its leaf certificate and the intermediates needed to build a chain. The client should not accept a peer-provided root as a new trust anchor automatically. Otherwise the peer can invent its own chain and approve itself.

## Follow a server-authentication decision

First, build and validate a path according to the configured trust store. Check certificate signatures, validity, CA constraints and relevant key usages. Then check that the authenticated certificate is suitable for the intended service and matches the requested identity.

The name to verify comes from the application connection intent, not from an arbitrary name supplied by the peer. For a DNS service, this normally means the requested hostname and the certificate's appropriate subject alternative names. An IP-address connection needs the corresponding IP identity handling; a DNS name that happens to resolve to that address is not automatically equivalent.

The earlier host experiment deliberately keeps the trust input fixed while changing the requested hostname. The second verification fails with a hostname mismatch. This isolates identity checking from chain trust and shows why disabling name verification can undermine otherwise correct TLS encryption.

## Extensions constrain authority

Basic constraints distinguish a CA certificate from an end-entity certificate and can limit subordinate CA depth. Key usage and extended key usage describe permitted operations and roles. A certificate valid for one role should not be accepted for every other role simply because its signature verifies.

A CSR proves possession of the private key associated with the requested public key when its signature is verified. It does not independently prove that the requester owns a DNS name, belongs to a company or may act as a CA. The issuer's enrollment process must validate those claims.

For a device fleet, separate enrollment identity from long-term operating identity when appropriate. A factory credential might authorize one controlled enrollment operation. It should not silently become a permanent administrator credential for every service.

## Time and revocation are operational dependencies

Validity checks need a usable time model. A device that starts with an incorrect clock can reject valid certificates or accept certificates outside their intended period if checks are disabled. Design how the device establishes time and how it behaves before time is trustworthy.

Revocation also requires a policy. A certificate revocation list or an online status response has freshness and availability requirements. A disconnected device cannot obtain new revocation information merely because a library supports the protocol. Define offline operation, cached status lifetime and failure behavior explicitly.

Short-lived credentials can reduce the period of exposure, but they increase dependence on renewal and time. They do not remove the need to revoke a compromised enrollment authority or a signing service.

## Device identity and private-key ownership

A certificate is public; its private key is the sensitive identity material. Copying one private key into every manufactured image lets compromise of one device affect the whole group. Generate or provision identities through a controlled per-device process and record the binding between device and certificate.

A hardware-backed key can prevent ordinary private-key export while still allowing signing requests. That shifts the question from “can the attacker read the key?” to “can the attacker ask the key service to sign an unauthorized challenge?” Access control and request context still matter.

Replacing a device, restoring a backup and performing a factory reset all need explicit identity rules. A reset should not unexpectedly resurrect a revoked credential from a default filesystem image.

## TLS certificates and SSH certificates are different formats

OpenSSH has its own certificate format and trust model; it does not consume an X.509 server certificate as a host certificate by renaming the file. Likewise, a ZynqMP boot authentication certificate is not an ordinary web certificate.

Keep the terminology tied to the protocol. Each format defines what is signed, how keys are represented, which constraints apply and where trust anchors live. Reusing the same private key across formats can also couple roles unnecessarily.

## A useful validation matrix

| Case | Expected result | Property isolated |
| --- | --- | --- |
| Trusted issuer, right identity and valid time | Accept | Positive baseline |
| Same chain, wrong hostname | Reject | Peer identity |
| Unknown issuer | Reject | Trust-anchor selection |
| Expired or not-yet-valid certificate | Reject according to policy | Time validation |
| Wrong intended usage | Reject | Role restriction |
| Revoked credential with current status | Reject | Revocation integration |

Only the matching and mismatching hostname cases above were recorded in the existing local exercise. The other rows are proposed product tests. Keep that distinction when reporting test coverage.

## References

- Executed local OpenSSL verification, including expected failure
- [OpenSSL 3.0 verify manual](https://docs.openssl.org/3.0/man1/openssl-verify/)
- RFC 5280, certificate path validation

---

<sub>← [Cryptography Primer](02-cryptography-primer.md) · [Chapter index](README.md) · [Key Management](04-key-management.md) →</sub>
