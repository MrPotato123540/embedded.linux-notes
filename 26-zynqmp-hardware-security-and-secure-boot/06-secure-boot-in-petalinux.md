# Secure Boot With PetaLinux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## End-to-end integration plan

Start from a known bootable unsigned image on the intended board. Freeze the XSA, firmware, kernel and rootfs versions. Define which stage verifies each later artifact, including data that can change boot behavior.

Use separate development keys to generate a signed boot image through the supported Bootgen/PetaLinux flow. Inspect the BIF and decoded metadata. Keep signing outside ordinary build workers when production keys are involved.

## Acceptance tests

1. Confirm the intended image boots under the intended device policy.
2. Modify a protected payload and confirm rejection.
3. Test incorrect key and unsupported/revoked key cases.
4. Confirm recovery remains available according to policy.
5. Verify the later kernel/rootfs path and rollback rules.

Encryption, if required, adds key-source and retention tests. It does not remove authentication or recovery requirements.

> [!NOTE]
> **Not run on the reference setup:** a signed/encrypted ZCU10x hardware boot. The existing BSP reports unauthenticated, unencrypted boot. This is an integration procedure, not a claimed successful secure-boot session.

## References

- AMD UG1144 and UG1283 (2024.1), secure boot and packaging
- Reference `boot-manual-1.log`

---

<sub>← [eFUSE and BBRAM Programming](05-efuse-and-bbram-programming.md) · [Chapter index](README.md) · [Verified Boot Beyond U-Boot](07-verified-boot-beyond-u-boot.md) →</sub>
