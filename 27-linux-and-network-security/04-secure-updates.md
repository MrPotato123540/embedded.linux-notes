# Secure Software Updates

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[27 · Linux and Network Security](README.md)** · Part XIV: Security

## Verify before activation

An update bundle needs authenticated metadata and payloads, a target-compatibility check and a controlled installation transaction. Transport encryption protects the download channel; it does not replace a release signature that can be checked offline.

A valid signature does not prove freshness. Define rollback protection and where the accepted version state is stored. If an attacker can replace that state together with the image, the rollback check may have no effect.

## RAUC and SWUpdate integration

Connect the selected updater to the real slot layout and boot-success mechanism. Keep verification keys trusted by the existing image and provide a planned rotation path. Test interrupted download, interrupted write, invalid signature, wrong hardware target and failed first boot.

The recovery image must enforce compatible security policy. An unsigned recovery path can bypass a signed normal path.

> [!NOTE]
> **Not run on the reference setup:** secure updater integration and rollback/power-loss negative tests.

## Authenticate a release decision

An update is more than a new rootfs image. It is a claim that specific payloads are approved for a particular product and version. The authenticated metadata should bind those properties together: component digests, hardware compatibility, dependencies and the release/version policy.

Imagine two board revisions with the same CPU but different PL register layouts. A bundle can have a valid signature and still be unsafe for the wrong board. A compatibility check must use a trustworthy device identity and authenticated bundle metadata. A user-editable text file should not be the sole authority for a security-relevant board match.

Separate release authority from delivery infrastructure. A CDN or web server distributes bytes; it should not gain permission to approve new firmware merely because it hosts the file. TLS protects the transport session. A release signature can remain checkable after the bundle is copied through another approved channel.

## Bind metadata to every payload

The installer must verify the signed description and then verify each payload against that description. If the descriptor is signed but a payload digest is missing or not checked, the installer may accept replacement bytes. If the payload is checked but the target slot or script is untrusted, installation behavior can still change.

Review hooks and scripts with the same care as executable firmware. An installer hook often runs with broad storage privileges. It should come from the authenticated release or from trusted installed policy, and it should receive tightly defined parameters.

Preserve the final verified object until installation completes. Downloading to a writable shared path, verifying it, then reopening a replaceable path creates a time-of-check/time-of-use gap. Use an update architecture that keeps identity and ownership of the verified data stable.

## An A/B update is a controlled transaction

| State | Durable fact | Safe response to interruption |
| --- | --- | --- |
| Current slot active | Existing release is bootable | Continue using it |
| Candidate received | Bundle is complete but not yet activated | Discard or revalidate it |
| Inactive slot written | Candidate payload and metadata are durable | Keep current slot until selection is committed |
| Trial boot selected | Bootloader has a bounded trial policy | Try candidate or return to approved previous slot |
| Candidate confirmed | Required health checks passed | Commit the release according to rollback policy |

This is a design model, not a claim that the BSP already implements these states. The storage layout, bootloader environment handling and updater must implement compatible transitions. [Update strategies](../23-storage-updates-and-production/04-software-update-strategies.md) explains the storage side.

Confirmation should mean useful product operation. Reaching a login prompt may not prove that the PL driver, remote processor or network identity works. Define health checks for the critical function and give them a bounded time. A broken candidate must not mark itself healthy merely because its startup process ran.

## Rollback protection changes fallback choices

Availability encourages keeping an older working slot. Security may forbid that slot after a vulnerability is fixed. These requirements need a joint policy. Decide which older releases remain allowed and when a protected minimum version advances.

The minimum version must be bound to trusted state. Storing it in the same replaceable filesystem as the image lets an attacker restore both together. A hardware key-revocation field is also not an unlimited general software-version database; use only supported semantics.

Power loss at version advancement deserves a specific test. If the minimum advances before the new slot is durable, neither slot may be accepted. If the new slot is confirmed without updating the protected minimum, an old signed image may remain bootable. The design must explain both cases rather than assume one write makes a multi-component transaction atomic.

## RAUC and SWUpdate need product integration

RAUC's bundle verification and slot model can support signed update flows. Its documentation explains keyring-based trust and certificate rotation patterns. SWUpdate also provides signed-image support with selected cryptographic backends. Neither project's existence proves that a particular PetaLinux image has a complete secure updater.

Pin the selected updater version and review its exact bundle format, required signature configuration and error behavior. Connect the boot-success mechanism to the real bootloader and storage layout. Do not mix configuration examples from unrelated releases or assume that enabling a signing library forces signatures for every install path.

The references describe integration options. No RAUC or SWUpdate deployment was built or tested for this revision. Product-specific configuration should be added only with evidence from the chosen release and board.

## Rotate keys without stranding devices

A common staged design first distributes trust in both old and new authorities, then signs future releases under the new authority, then removes the old one when recovery and offline-device policy permit. The currently trusted release must authorize each trust-store change.

Account for devices that miss several updates. They may need an approved bridge release before they understand the new key. Also account for recovery images with older trust stores. A rotated normal image and a stale recovery image can disagree about which releases are acceptable.

Emergency compromise handling may intentionally skip the normal overlap period, but that changes availability risk. Keep the authority to revoke a key separate from routine build permissions, and preserve an auditable release decision.

## Test rejection and interruption separately

Corrupted data, wrong signer, wrong board, old version, full storage and power loss exercise different paths. For each, define whether the device should continue the old release, retry, enter verified recovery or stop. Record the selected slot and version after the next reboot.

Finally, test the download and installer entry points themselves. A valid signature on accepted bundles does not prevent denial of service from enormous downloads, repeated retries or parser bugs. Bound resource use before expensive work and preserve enough failure evidence for support without logging credentials.

## References

- [RAUC 1.11.3 advanced topics](https://rauc.readthedocs.io/en/v1.11.3/advanced.html), conceptual signing/key-rotation reference; not an installed BSP version claim
- [RFC 9019: Firmware Update Architecture](https://www.rfc-editor.org/rfc/rfc9019.html)
- SWUpdate signed-image documentation
- [Update architecture](../23-storage-updates-and-production/04-software-update-strategies.md)

---

<sub>← [Network Security](03-network-security.md) · [Chapter index](README.md) · [Vulnerability Management](05-vulnerability-management.md) →</sub>
