# Verified Boot Beyond U-Boot

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Extend verification past the bootloader

Signed FIT configurations can bind kernel, device tree and other selected payloads together. U-Boot must contain a trusted verification key and enforce the intended signature policy. An unsigned fallback path can defeat the policy.

Kernel module signing controls which loadable code the kernel accepts when enforcement is configured. Preserve the trusted key configuration and test rejection, not only successful signing.

**dm-verity** checks a read-only block device through a hash tree. Its root hash must come from a trusted source; accepting an attacker-supplied root hash also accepts the attacker's data. Mutable data needs a separate design.

**IMA** and **EVM** support file measurement/appraisal and metadata protection with explicit policy. Enabling their configuration symbols alone does not define what gets checked or how failure is handled.

> [!NOTE]
> **Not run on the reference setup:** enforced FIT, module-signature, dm-verity or IMA/EVM negative tests.

## References

- U-Boot v2024.01 FIT signature documentation
- Linux 6.6 [module signing](https://docs.kernel.org/6.6/admin-guide/module-signing.html) and [dm-verity](https://docs.kernel.org/6.6/admin-guide/device-mapper/verity.html)

---

<sub>← [Secure Boot With PetaLinux](06-secure-boot-in-petalinux.md) · [Chapter index](README.md) · [TrustZone and OP-TEE](08-trustzone-and-op-tee.md) →</sub>
