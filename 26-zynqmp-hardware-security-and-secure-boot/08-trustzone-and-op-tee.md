# TrustZone and OP-TEE

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Trusted applications

OP-TEE places a small trusted OS and selected applications in the Secure world. A Linux client asks for a defined service. The trusted application should validate command identifiers, buffer lengths and data before acting.

Keep the trusted code small. Moving a large parser into the Secure world increases the code that must be trusted. Avoid services that simply expose arbitrary secure memory or unrestricted hardware operations.

## Memory and storage

Secure memory requires hardware isolation and correct reservations. Shared memory is intentionally visible across the boundary and must be treated as untrusted input. Do not assume a caller leaves shared data unchanged during processing.

Secure storage depends on the chosen backend and key derivation. Replay/rollback resistance is a separate property; encrypted files on a normal filesystem do not automatically provide it. Device-bound secrets also need a lifecycle for replacement and factory reset.

> [!NOTE]
> **Not run on the reference setup:** trusted-application execution, secure storage and physical isolation tests.

## References

- OP-TEE core and secure-storage documentation
- [Exception levels and TrustZone](../03-zynqmp-architecture/10-exception-levels-and-trustzone.md)

---

<sub>← [Verified Boot Beyond U-Boot](07-verified-boot-beyond-u-boot.md) · [Chapter index](README.md) · Next chapter: [27 · Linux and Network Security](../27-linux-and-network-security/README.md) →</sub>
