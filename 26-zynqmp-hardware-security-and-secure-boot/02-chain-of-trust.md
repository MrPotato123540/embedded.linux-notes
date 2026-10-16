# Chain of Trust

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Trust must continue through every stage

A **root of trust** is the starting point whose behavior and trust material the design relies on. Each verified stage must authenticate the next stage before giving it control or trusting its data.

For a ZynqMP Linux product, examine the whole path: BootROM → FSBL → resident firmware/U-Boot → kernel/device tree/initramfs → root filesystem and application. The exact verifier for each partition depends on the supported boot flow.

A signed `BOOT.BIN` does not automatically authenticate a kernel later loaded from a writable SD partition. A trusted kernel also needs a policy for modules, rootfs integrity and mutable configuration.

## Verified and measured boot

Verified boot enforces an acceptance decision. Measured boot records evidence of what was loaded for later assessment. Recording a hash without a trusted reference or attestation design does not stop an unapproved image from running.

Define rollback policy as well as signature policy. An old vulnerable image can have a valid signature.

## Build a verification contract for each handoff

A chain of trust is a sequence of decisions, not a list of signed filenames. Before stage A uses object B, A must know why B is acceptable. The decision can include a signature, hardware compatibility, version policy and bounds checks. Only after those checks may B control execution or supply trusted parameters.

Use the actual boot flow to draw the contract. The BSP's boot image includes the FSBL, PMU firmware, TF-A, a device tree and U-Boot inputs. Later, U-Boot loads a FIT image. The FIT may contain another device tree and an initramfs. Those objects have different roles even when their source names look similar.

| Boundary | Data that needs an acceptance rule | Trust material that must already be protected |
| --- | --- | --- |
| CSU BootROM to initial software | Initial boot structures and protected bootloader content | Device boot policy and hardware trust anchor |
| FSBL to later partitions | Firmware, executable partitions and applicable PL content | Authenticated FSBL and allowed partition keys |
| U-Boot to Linux | Selected kernel, device tree, initramfs and boot policy | Required FIT verification keys and trusted bootloader policy |
| Kernel to root filesystem | Executable files and security-relevant configuration | Verified root digest or another enforced integrity policy |
| Kernel to loadable code | Kernel modules and other enabled code-loading paths | Enforced key and loading policy |

The table describes ownership. It does not claim that every row is enabled in the supplied BSP. The recorded reference boot is not a production secure-boot demonstration.

## Trusted data matters as much as code

Imagine a signed kernel that accepts an attacker-controlled device tree. The device tree can describe memory regions, devices and boot arguments. Depending on the boot design, changed arguments may select another root filesystem or change early userspace behavior. Authenticating only the kernel leaves these decisions outside the checked boundary.

The same issue applies to an external initramfs. It may contain the first userspace program and the code that opens an encrypted volume or mounts the final root. If it is replaceable without verification, it can change the meaning of a later integrity check.

An environment variable can also become executable policy. A mutable U-Boot environment may select a different command, file or recovery path. A product must decide which settings may change and which must remain part of the trusted boot policy. Signing a file does not help if the bootloader is allowed to skip it.

## Verify the bytes that will actually run

The checked bytes must remain stable until use. This is a time-of-check/time-of-use problem: verification succeeds, then another actor changes the buffer before execution. Prevent competing writers during this interval. Consider other cores, DMA engines and shared-memory users as well as the current CPU.

Compression adds another boundary. A signature can cover the compressed object, while decompression writes a larger output into RAM. The verifier still needs bounds checks for the destination and a compatible image format. Authentication proves the signer approved the input; it does not make a malformed decompressor input safe to parse.

For a concrete trace, start with [the reference FIT listing](../11-u-boot/04-fit-images.md). Identify the selected configuration, its kernel reference, device-tree reference and ramdisk reference. Then identify where the verification key comes from. A hash node stored beside a payload detects accidental changes, but an attacker who replaces both has not crossed a trust boundary.

## Freshness is a separate state machine

Suppose releases 10 and 11 are both correctly signed, but release 10 contains a remotely exploitable bug. Signature verification accepts both unless policy also checks a trusted version rule. The version must be authenticated, and the minimum allowed version must resist replacement by the same attacker who controls the image.

Do not equate a release number with a hardware key identifier. The FSBL's supported SPK checks concern the configured key policy. A product-wide version policy may also cover Linux, application data and recovery. It needs its own design and cannot be inferred from a filename such as `release-11.bin`.

The update transaction must coordinate version advancement with recovery. Advancing a protected minimum before the replacement image is durable can reject the only working image. Advancing it too late can leave a downgrade window. The correct order depends on the available trusted state and slot design; document the power-loss outcome at each transition.

## Recovery belongs inside the chain

List every path that can reach execution: normal storage, fallback storage, network recovery, debug and factory service. For each path, identify the verifier and accepted keys. A recovery image may use a separate key authority, but its ability to replace normal software must be explicit.

A useful review exercise removes one normal artifact at a time. Does the device stop, use a verified alternate slot or enter a controlled service mode? If it enters an unrestricted shell that can boot arbitrary code, that path changes the security claim. It may be an intentional development policy, but it is not equivalent to an enforced production chain.

Measured boot can record these selected artifacts for a remote verifier. A trustworthy measurement report also needs protected measurement state, an authenticated reporting key and a freshness challenge. A text log containing hashes is useful diagnostic evidence; it is not by itself remote attestation.

## References

- AMD UG1283 (2024.1), boot-time security
- [Verified boot beyond U-Boot](07-verified-boot-beyond-u-boot.md)

---

<sub>← [Hardware Security Features](01-hardware-security-features.md) · [Chapter index](README.md) · [Boot Image Authentication (RSA)](03-authentication.md) →</sub>
