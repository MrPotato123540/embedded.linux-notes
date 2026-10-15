# Key Management

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[25 · Security Fundamentals and Cryptography](README.md)** · Part XIV: Security

## Key lifecycle

A key needs an owner, purpose, generation method, storage policy, rotation plan and destruction process. Record which devices and releases depend on it before replacing or revoking it.

Use separate keys for release signing, device identity and data encryption. Limit signing access, log requests and require review for production release operations. A build worker should not need unrestricted access to long-lived private signing keys.

A **Hardware Security Module (HSM)** can protect key material and perform operations without exporting it. It does not decide whether a malicious or incorrect image should be signed; authorization policy remains necessary.

## Recovery and rotation

Plan for a lost signing service, compromised key and disconnected device fleet. Rotation needs overlap or a trusted transition path. Revoking the only accepted key before devices accept a replacement can permanently block updates.

Backups of private keys need protection equal to the originals. Do not place secrets in Git, build logs or ordinary image artifacts. Test recovery with non-production keys before release.

## References

- [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)

---

<sub>← [PKI and Certificates](03-pki-and-certificates.md) · [Chapter index](README.md) · Next chapter: [26 · ZynqMP Hardware Security and Secure Boot](../26-zynqmp-hardware-security-and-secure-boot/README.md) →</sub>
