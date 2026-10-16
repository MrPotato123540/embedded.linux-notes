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

## Place OP-TEE in the real boot flow

TrustZone separates Secure and Non-secure execution and resource access. OP-TEE is software that uses that boundary to provide a trusted OS and trusted applications. On an Armv8-A system, a typical arrangement places the secure monitor at EL3, OP-TEE core at Secure EL1 and Linux at Non-secure EL1. Trusted applications can run at Secure EL0 under OP-TEE's control.

The boot chain must load and authenticate the secure payload, reserve its memory and select a compatible TF-A dispatcher. Merely building a Linux TEE driver does not create that payload or configure the hardware isolation it needs.

The reference TF-A log contains a secure entry address associated with the platform's BL32 defaults. As explained in [BL31 on ZynqMP](../10-trusted-firmware-a/02-bl31-on-zynqmp.md), that message is not proof that OP-TEE is installed or running. Establish that from the actual boot partitions, TF-A configuration, OP-TEE initialization and a client transaction.

## Follow one client request

Consider a service that signs a device-specific challenge. The normal-world application opens a TEE session for a named trusted application. It submits a command identifier and parameters through the Linux TEE interface. The kernel driver converts the request into the selected secure-call ABI. TF-A switches execution to the Secure world.

OP-TEE validates the session and dispatches to the trusted application's command handler. The handler checks parameter types, sizes, command authorization and the meaning of the requested operation. It returns a result through the same path. A successful transport call is not necessarily a successful trusted-application operation; preserve the returned status and its origin.

The Linux 2024.1 source paths `drivers/tee/optee/call.c` and `drivers/tee/optee/smc_abi.c` show the call and SMC ABI handling. The exact transport is a platform integration choice. Do not apply a different platform's OP-TEE transport configuration without checking the chosen TF-A and OP-TEE builds.

## Shared memory is an input channel

The Normal world can own or influence shared buffers. Treat lengths, offsets and contents as untrusted even when Linux passes them through a kernel driver. Check arithmetic before computing an end address; `offset + length` can overflow. Validate the whole requested range against the object that was actually shared.

Avoid validating a shared command and later rereading it as if it were unchanged. Another normal-world thread or device may modify it between those steps. Copy small security-sensitive control data into private memory, validate that copy and use it consistently. Large payloads need an explicit streaming and authentication design.

A response buffer also has an ownership lifetime. Do not return pointers to Secure memory. Do not retain a shared-buffer reference after its session or registration ends. Clearing a session should remove any authority associated with it, not only free the user-visible handle.

## A trusted service must limit authority

“Sign any supplied bytes” is often too powerful for a device-identity key. A compromised Linux client could ask it to sign another protocol's message. Define a purpose-specific input format, fixed context and allowed operation. The trusted application should construct the signed message from validated fields rather than accept an unrestricted digest.

Caller identity also needs care. A user ID supplied as ordinary input is only a claim. Decide which identity information the TEE framework and platform authenticate, and which properties remain under normal-world control. The application protocol should remain safe under the threat model actually supported by that identity mechanism.

This design reduces the trusted code base. Keep large file formats, network parsers and UI logic outside the Secure world where possible. Pass a small, clearly defined request across the boundary. Moving the entire Linux application into a trusted application increases the amount of code whose bugs can expose the key.

## Storage confidentiality and freshness differ

OP-TEE supports secure-storage designs using normal-world filesystem storage and, on supported platforms, Replay Protected Memory Block (RPMB) storage. The normal-world storage service can still deny access or lose files. Encryption and integrity checks can protect content, but rollback resistance depends on the backend and platform guarantees.

A useful threat scenario is restoring an old complete disk snapshot. If the secure service accepts an older encrypted object as current, the object may be confidential and intact but stale. That matters for counters, revoked credentials and minimum software versions. Test replay behavior against the selected backend instead of inferring it from the phrase “secure storage.”

Device-bound key derivation makes copying storage to another unit less useful, but it changes replacement and recovery. A failed board may make its protected data unavailable on a replacement. Decide whether data is intentionally non-migratable or has an authorized export/recovery design.

## Runtime isolation and availability

Secure memory needs both correct software reservations and hardware access restrictions. A `reserved-memory` node tells Linux not to allocate a range in the relevant way; it is not by itself proof that a DMA master cannot read it. Check the actual interconnect and protection-unit configuration.

Normal-world services such as `tee-supplicant` may participate in filesystem or other RPC work. A trusted application must handle failure or delay from those services. A TEE does not make Linux scheduling, storage or power reliable. Include timeout, cancellation and restart behavior in the client protocol.

The OP-TEE architecture references below explain these concepts; they do not identify a tested OP-TEE build in the reference BSP. No trusted application, secure-storage backend or physical isolation test was run for this guide revision.

## References

- [OP-TEE 3.21 core architecture](https://optee.readthedocs.io/en/3.21.0/architecture/core.html) and [secure storage](https://optee.readthedocs.io/en/3.21.0/architecture/secure_storage.html)
- `linux-xlnx@xilinx-v2024.1:drivers/tee/optee/call.c` and `smc_abi.c`
- [Exception levels and TrustZone](../03-zynqmp-architecture/10-exception-levels-and-trustzone.md)

---

<sub>← [Verified Boot Beyond U-Boot](07-verified-boot-beyond-u-boot.md) · [Chapter index](README.md) · Next chapter: [27 · Linux and Network Security](../27-linux-and-network-security/README.md) →</sub>
