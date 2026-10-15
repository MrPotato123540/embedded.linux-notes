# BL32 and OP-TEE (Overview)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot

## Secure operating system

**OP-TEE (Open Portable Trusted Execution Environment)** provides a trusted OS at Secure EL1, with trusted applications at Secure EL0. Linux clients communicate through a kernel TEE driver and the secure monitor. Shared memory transports requests; the Secure side must validate data received from the Non-secure side.

OP-TEE is optional in the ZynqMP boot chain. TF-A running at EL3 does not prove that OP-TEE is present. The build must include a compatible Secure payload, the correct TF-A dispatcher and suitable memory reservations.

## Integration requirements

Keep secure code/data memory separate from normal Linux allocations. Define shared memory deliberately, and ensure hardware access policy matches the intended isolation. Package the image with the correct handoff metadata.

Test the client driver, userspace support and a trusted application together. A Secure OS banner is only one step; session opening, parameter checking and failure handling must also work.

> [!NOTE]
> **Not run on the reference setup:** OP-TEE integration. The existing reference boot captures do not establish that a Secure OS was loaded.

## References

- [OP-TEE core architecture](https://optee.readthedocs.io/en/latest/architecture/core.html)
- [TrustZone and OP-TEE integration](../26-zynqmp-hardware-security-and-secure-boot/08-trustzone-and-op-tee.md)

---

<sub>← [Building and Customizing TF-A](03-tfa-customization.md) · [Chapter index](README.md) · Next chapter: [11 · U-Boot](../11-u-boot/README.md) →</sub>
