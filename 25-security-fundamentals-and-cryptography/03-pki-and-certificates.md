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

## References

- Executed local OpenSSL verification, including expected failure
- [OpenSSL 3.0 verify manual](https://docs.openssl.org/3.0/man1/openssl-verify/)
- RFC 5280, certificate path validation

---

<sub>← [Cryptography Primer](02-cryptography-primer.md) · [Chapter index](README.md) · [Key Management](04-key-management.md) →</sub>
