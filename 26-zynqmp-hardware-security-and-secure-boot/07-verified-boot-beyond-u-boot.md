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

## Bind the selected FIT configuration

A Flattened Image Tree (FIT) can contain several kernels, device trees and ramdisks. A product boots one selected configuration. The security question is whether that complete selection is approved, not merely whether one payload has a valid standalone signature.

U-Boot's v2024.01 FIT signature documentation distinguishes image signatures from configuration signatures. A required configuration-signature policy helps bind the selected component references and their hashes. The verification key must be present in trusted U-Boot control data. A key supplied only inside an attacker-replaceable FIT cannot establish its own authority.

Keep the U-Boot control device tree separate from the device tree passed to Linux. The control tree configures U-Boot and can hold verification keys. The OS tree describes the platform to the kernel. Protecting the OS tree does not automatically protect the control tree, and adding a key to the wrong tree does not enable the intended verification.

In the reference FIT, a default configuration selects a compressed kernel, a device tree and an initramfs. Its existing hash nodes are useful for integrity inspection. They are not evidence that a required public-key signature policy is enforced. See [the FIT source and listing](../11-u-boot/04-fit-images.md) for the actual component selection.

## Close the policy around the verifier

Required keys and rejection behavior matter as much as signature generation. Audit every allowed boot command and fallback. If a user can switch from the checked FIT path to loading an arbitrary raw kernel, the signature policy does not cover the whole boot interface.

Also protect values that alter the verified system's behavior: root-device selection, integrity metadata, an external initramfs and relevant boot arguments. Mutable calibration data may be acceptable, but it should not be able to replace the executable root or select an unrestricted maintenance program.

A useful negative case keeps every component individually valid but combines components from different releases. The system should reject an unauthorized combination when the product relies on configuration binding. This case detects a gap that a simple one-byte corruption test may miss.

## How dm-verity connects blocks to trust

Device-mapper verity exposes a read-only block device whose reads are checked against a hash tree. A leaf hash covers data blocks; higher levels cover lower hash blocks. A trusted root digest anchors the tree. A changed data block or hash block then fails verification against that root.

For an illustrative layout with 4 KiB hash blocks and 32-byte digests, one hash block has space for 128 digests before considering the format's detailed layout. That fan-out explains why a large data image can be checked with a much smaller tree. Use the selected verity format and tool output for real offsets and sizes; the arithmetic is an explanation, not a generated layout.

The root digest, salt, block sizes and device mapping must come from trusted policy. If an attacker can replace the root digest alongside the filesystem, they can build a valid tree for their own content. A signed manifest or verified boot object can supply the needed anchor.

Verity checks reads rather than proving that every physical sector was scanned at boot. Decide how corruption is handled when it is discovered: fail the read, restart or enter another documented policy. Test that behavior with the real rootfs and recovery design. Do not claim confidentiality; the underlying data remains readable unless separately encrypted.

## Mutable state needs a separate contract

A read-only verified root does not make `/data` trustworthy. Applications may load scripts, plugins, certificates or service configuration from writable storage. If those objects can change execution or authority, include them in the trust model.

An overlay filesystem can also shadow trusted lower files with writable upper files. It is useful for development, but a production design must define which paths may be overridden. An executable copied into an upper layer is not protected merely because the lower image has a valid verity tree.

Separate persistent device identity, user data and executable release content. Give each its own update and recovery policy. A factory reset should not accidentally clone an identity, restore revoked credentials or remove the only metadata needed for rollback decisions.

## Module signing and file appraisal cover other entry points

The pinned Linux documentation at `Documentation/admin-guide/module-signing.rst` describes signature verification for loadable modules. A permissive configuration can accept an unsigned module while recording the condition; an enforced configuration must reject it. Verify the actual kernel settings and a real negative load test before claiming enforcement.

Sign the final module bytes after transformations such as stripping. Changing those signed bytes invalidates the signature. A supported packaging flow can compress the signed module afterward, provided decompression restores the exact signed bytes before verification. Built-in drivers do not pass through the module loader; their trust comes from the kernel image's earlier verification.

Integrity Measurement Architecture (IMA) can measure files and, with appraisal policy, enforce integrity decisions. Extended Verification Module (EVM) protects relevant integrity metadata. These mechanisms depend on policy, keys, filesystem support and the selected hooks. They are not interchangeable with dm-verity's block-level read-only model.

For a product review, enumerate executable entry points: modules, firmware requests, interpreters, plugins, early userspace and maintenance tools. Assign each to an enforced mechanism or an explicit allowed-mutable policy. Then test both approved content and changed content. None of these target enforcement tests was executed in this revision.

## References

- U-Boot v2024.01 FIT signature documentation
- Linux 6.6 [module signing](https://docs.kernel.org/6.6/admin-guide/module-signing.html) and [dm-verity](https://docs.kernel.org/6.6/admin-guide/device-mapper/verity.html)

---

<sub>← [Secure Boot With PetaLinux](06-secure-boot-in-petalinux.md) · [Chapter index](README.md) · [TrustZone and OP-TEE](08-trustzone-and-op-tee.md) →</sub>
