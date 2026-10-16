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

## Inventory keys by authority and failure domain

A key inventory should describe what an attacker can do with each key, not only where the key file lives. A release-signing key authorizes software. A device-identity key authenticates one device. A data-encryption key protects stored content. A wrapping key protects another key. These roles have different users, lifetimes and recovery needs.

For each entry, record the algorithm and key identifier, owner, allowed operation, storage location, affected devices, activation state and revocation path. Record public fingerprints where useful, but never place private material in the inventory itself.

Separate development and production keys. A tutorial key or shared laboratory credential must not become a production trust anchor through image cloning. The teaching crypto example in this chapter creates temporary keys only in process memory and has no authority outside its run.

## A signing service needs an authorization boundary

Moving a private key into an HSM prevents some export paths. It does not determine whether a submitted binary is an approved release. If a compromised build worker can submit arbitrary bytes to an unrestricted signing endpoint, the key can remain physically protected while malicious software receives a valid signature.

Bind a signing request to the artifact digest, product/hardware identity, release version, purpose and approval record. The service should enforce which callers may request which signing role. Preserve an audit trail of the approved digest and resulting signature without exposing private key material.

Use a manifest or another unambiguous format for the approved context. A human review of a filename is weak if the underlying file can change before signing. The signer should operate on the exact immutable input whose identity was approved.

## Separate signing, encryption and identity keys

Signature verification uses public information, so every device need not possess a release-signing secret. Shared-secret authentication instead gives every verifier holding the secret some ability to create authentic data. Choose the model based on authority, not only performance.

Device-specific encryption limits the impact of one extracted key but complicates manufacturing and recovery. A shared fleet key simplifies distribution but broadens compromise. Key wrapping can protect stored key material, while the unwrapping authority and its access policy become part of the trusted system.

Do not use a device serial number as a secret or as the sole source of key entropy. It can be a public identity/context field in a supported derivation design, but secrecy and randomness must come from the actual key material.

## Rotation is a transition across device states

Consider a fleet that trusts signing key A and must move to key B. The transition must first establish trust in B through an already trusted path. Then devices must receive a release that uses the intended new policy. Only after the required devices and recovery paths accept B can the design retire A under its chosen policy.

| Fleet state | Required capability | Main risk |
| --- | --- | --- |
| A only | Verify an authorized transition | Revoking A too early blocks the transition |
| A and B accepted | Install/test B-signed releases | Old A authority remains usable until removed |
| B accepted, A retired | Update and recover under B | Offline devices may still be stranded on A |

This is a conceptual lifecycle, not a universal ZynqMP fuse-programming sequence. Hardware key slots, revocation controls and rollback rules impose additional constraints. Model those constraints before manufacturing.

## Recovery must preserve the same trust policy

Prepare for loss of a signing service, deletion of a private key, device replacement and compromise of an operator account. Backups of key material require at least the same access control as the original. Backup recovery should be tested with non-production keys and recorded procedures.

An unprotected emergency signing key defeats ordinary controls. A recovery role can be deliberately different, but its authority, storage and allowed artifacts need explicit limits. The recovery image must also remain acceptable after key rotation and anti-rollback updates.

For encrypted data, distinguish recovering the software from recovering the data key. Restoring a bootable image does not restore access to data encrypted under a lost key. Conversely, retaining old data keys indefinitely may conflict with the intended deletion policy.

## Destruction and compromise response

Deleting a pathname does not prove all key copies are gone. Keys can remain in backups, logs, build artifacts, process memory or device storage. Design which copies are allowed and how they are retired. Managed-language memory also limits claims about reliable immediate zeroization of application objects.

After suspected compromise, identify the affected authority and products. Stop unauthorized signing or authentication, issue the controlled transition, and monitor which devices actually receive it. A server-side database flag is not enough to revoke an offline device's locally trusted key.

Keep incident exercises separate from production provisioning. The guide has not rotated a fleet key or programmed security storage. These procedures explain the decisions and evidence a real lifecycle must supply.

## References

- [NIST SP 800-57 Part 1 Rev. 5](https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final)

---

<sub>← [PKI and Certificates](03-pki-and-certificates.md) · [Chapter index](README.md) · Next chapter: [26 · ZynqMP Hardware Security and Secure Boot](../26-zynqmp-hardware-security-and-secure-boot/README.md) →</sub>
