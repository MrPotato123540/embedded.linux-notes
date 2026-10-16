# eFUSE and BBRAM Programming

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Provisioning is a manufacturing operation

Security provisioning changes the device's future boot and debug behavior. Use the supported `xilskey`/device security programming flow for the exact device and tool release. A generic register-write script is not an adequate replacement.

> [!CAUTION]
> eFUSE programming is irreversible. Wrong key hashes, revocation settings or access controls can permanently prevent intended boot or recovery. BBRAM key loss can also make encrypted images unusable until a supported reprovisioning path is available.

## Required record

Prepare the device identity, intended policy, public-key hashes, programming tool version, operator authorization and expected verification results. Keep private keys out of the device log. Verify the input calculations independently before programming.

Test the whole plan on a development device: valid boot, invalid boot, power-cycle, key retention and recovery. Only then freeze a production procedure with explicit pass/fail criteria.

> [!NOTE]
> **Not run on the reference setup:** any eFUSE or BBRAM write. This guide does not present untested irreversible commands as a recipe.

## Treat provisioning as a state transition

A production device moves through states: unprovisioned, prepared for verification, provisioned, tested and released. The allowed operations differ in each state. The central question is not whether a programming utility returns success. It is whether the device now enforces the intended policy and can still enter its approved recovery path.

eFUSE fields have one-time programming constraints. BBRAM has different retention and replacement properties. Do not describe BBRAM as a reversible version of every eFUSE operation: the available fields, consumers and policy effects are not the same. Select the documented storage mechanism for the specific key or control.

Keep the immutable device identity, board identity and manufacturing record linked. A workstation cable can be moved to another board. Verify target identity immediately before a security-changing operation, not only when the work order is opened.

## Separate input preparation from device programming

Prepare public-key material and the required device-format hash through the supported tools. A PEM file includes a textual wrapper and encoded structures. Hashing the PEM text with a general-purpose checksum command is not automatically the PPK hash expected by ZynqMP. Byte order and the exact public-key representation matter.

The preparation stage should produce a reviewed package containing the public information, selected security fields, tool versions and the expected resulting policy. It should also identify the signed test images used after programming. A second check should derive the public values independently from the approved key identity, rather than merely compare two copies of the same hand-entered string.

Private signing keys do not need to be embedded in the provisioning log. If a particular supported key-loading step handles a symmetric secret, isolate that step and its access rights. Disable ordinary diagnostic paths that would print or archive secret input. Preserve enough public evidence to audit the operation without making the audit trail a secret leak.

## A reviewable manufacturing record

| Record field | Why it matters |
| --- | --- |
| Device and board identity | Associates the operation with the physical unit |
| Silicon and tool version | Identifies supported behavior and known limitations |
| Previous policy state | Prevents applying a first-time procedure to a partly provisioned unit |
| Public-key fingerprint and device-format hash | Connects the signing authority to the programmed trust anchor |
| Intended key selections and revocation state | Explains which images should remain acceptable |
| Approved recovery-image digest | Makes recovery test results reproducible |
| Programming and readback results | Shows what the tool reported, including partial failures |
| Positive and negative boot results | Establishes enforcement rather than only storage success |

Avoid logging a secret under a field called “key ID.” A key identifier is a non-secret name or fingerprint; key bytes are a secret. Define the record format before implementing the manufacturing script.

## Order controls around recovery

A safe procedure must establish that the intended signed image is valid before enabling a policy that rejects alternatives. It must also establish that the recovery image uses an accepted key and compatible firmware. Only then should the procedure apply final restrictions in the order documented for the device.

This is a design rule, not a substitute for the exact programming sequence in the supported security library. Some controls depend on other programmed fields and some lock further access. Read the matching `embeddedsw@xilinx_v2024.1:lib/sw_services/xilskey/` implementation and device documentation with the chosen silicon revision.

Power loss during provisioning needs a named outcome. On restart, the station must inspect actual device state and resume only if the next operation is valid. Repeating the original sequence blindly can hide partial success or apply a later lock too early. A failed unit should enter a controlled review state rather than return to the normal production queue.

## Test the policy, not just the stored value

A public-hash readback can show that expected data was stored, where readback is supported. It cannot prove that every boot path enforces that data. Follow it with a valid-image boot and deliberate rejection cases under the final policy.

Use different test images for different boundaries. A one-byte payload change tests content integrity. A self-consistent image signed by another primary key tests the trust anchor. An image with a disallowed secondary key tests that policy. An older valid image tests rollback only if the product has defined a rollback mechanism.

After final debug restrictions, repeat the approved service procedure. A maintenance path that worked before restrictions may no longer exist. Record how an operator distinguishes “security rejection” from “power or UART failure” without reopening an unrestricted debug path.

## BBRAM retention and replacement

For a BBRAM-based design, qualify the backup supply across normal shutdown, storage and service. A board that retains a key during a short bench test may lose it during battery replacement or long storage. The resulting encrypted image can be structurally valid while the device no longer has the needed secret.

Decide whether replacement involves reprovisioning the same key, installing a new key and image, or returning the device to a controlled factory process. Each choice affects key exposure and field support. A backup of encrypted firmware does not replace a lost decryption key.

No eFUSE or BBRAM programming was performed for this revision. This section defines the evidence and failure handling needed before such a procedure can be accepted. It intentionally does not present untested register writes as a manufacturing recipe.

## References

- AMD UG1283 (2024.1), key sources and authentication
- `embeddedsw@xilinx_v2024.1:lib/sw_services/xilskey/`

---

<sub>← [Boot Image Encryption (AES-GCM)](04-encryption.md) · [Chapter index](README.md) · [Secure Boot With PetaLinux](06-secure-boot-in-petalinux.md) →</sub>
