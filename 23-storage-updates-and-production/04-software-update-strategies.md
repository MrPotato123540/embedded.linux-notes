# Software Update Strategies

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## An update changes a compatible set

A ZynqMP release can include boot firmware, a bitstream, device tree, kernel, modules, root filesystem, R5 firmware and application data. These artifacts have dependencies. A new kernel with old modules can fail to load them; a new bitstream with an old driver can change register meaning; a new application can migrate data that an older image cannot read.

The update unit should reflect those dependencies. A manifest records artifact hashes, target identity, version and compatibility requirements. Integrity checks detect corruption. Authentication establishes whether the update came from an accepted signer. Neither one alone proves that the artifact set is compatible with the board.

The source of a downloaded file and the source of trust are different. A secure channel helps transport, while a signed artifact can remain verifiable after storage and redistribution. The trust anchor, key rotation and rollback policy belong to the product's boot/update design.

## A/B slots are a state machine

An original two-slot design can use these states:

```text
confirmed A -> prepare B -> verify B -> mark B pending
            -> boot B with limited attempts -> health check -> confirm B
                                      \-> failure -> return to A
```

While preparing B, A remains the confirmed boot target. Only a complete and verified B becomes eligible. A successful first boot does not immediately erase A. Health confirmation occurs after the required services and data checks succeed.

The selector and attempt counter must survive power loss in a defined way. If one nonredundant metadata write selects B before B is complete, the two-slot storage layout has not solved the update problem. Use the chosen bootloader/framework's documented redundant or transactional metadata mechanism, then test it on the actual medium.

## Define what each interruption leaves behind

| Interruption point | Required recoverable state |
| --- | --- |
| Download incomplete | Continue using the confirmed slot |
| Inactive-slot write incomplete | Do not select that slot |
| Verification fails | Retain confirmed slot and failure reason |
| Pending metadata update interrupted | Resolve to a valid old or new record |
| New image boots but service fails | Consume an attempt and recover according to policy |
| Confirmation interrupted | Preserve an unambiguous retry/recovery rule |

This table is a design contract, not evidence that a particular updater meets it. Test actual resets and power cuts at these boundaries. Filesystem atomicity does not automatically cover bootloader environment storage, raw flash writes or a second device.

## Boot success must mean product readiness

Reaching the kernel or starting PID 1 is too early for many products. A useful health check can include reading required configuration, opening critical devices, starting the main service and confirming a controlled local function. It should have a bounded timeout and a clear failure result.

Avoid a circular dependency where the component being tested confirms itself before it performs real work. Also avoid requiring an unavailable external network service when the product must boot offline. Choose checks that reflect the intended deployment and distinguish local failure from temporary external conditions.

A watchdog can recover a hang, but someone must connect the resulting reset to boot-attempt policy. A device that endlessly boots the same bad pending image has a reset mechanism without a recovery mechanism.

## Persistent data can prevent rollback

Suppose version B changes a database schema that version A cannot read. Returning to A after B fails can then break the supposedly known-good system. Image slots alone do not preserve application compatibility.

Options include backward-compatible migrations, a versioned data store, delayed irreversible migration or a retained recoverable copy. Each has storage and complexity costs. State the migration boundary in the update manifest and test it together with rollback.

Do not roll back device identity, security counters or user data blindly with the root filesystem. Different data classes have different retention and security rules. A factory-reset action is not the same as software rollback.

## Boot-chain updates need separate treatment

Updating `BOOT.BIN` changes early stages that may run before the normal updater or slot selector. If power fails while replacing the only bootable early image, Linux-based recovery may never start. The board's boot mode, alternate boot locations and BootROM behavior determine possible recovery designs.

The reference BIF includes FSBL, PMU firmware, TF-A, a device tree and U-Boot. Treat that composition as a specific artifact set. It does not include the Linux kernel or root filesystem in the inspected file. An updater that replaces only `image.ub` is therefore changing a different part of the chain.

Keep secure-boot policy consistent with updates. An image accepted by the userspace updater may still be rejected by an earlier boot stage. Conversely, an unsigned mutable selector can undermine a stronger payload policy if it redirects execution to an unverified path. Review where each verification happens.

## Choose a framework by its actual integration

RAUC, SWUpdate and other update frameworks provide useful mechanisms, but each still needs board-specific storage, bootloader and health integration. A package in the Yocto layers does not mean that integration is complete.

For PetaLinux 2024.1, pin the selected updater and layer revisions, preserve its configuration and test the bootloader backend against the chosen U-Boot environment/storage layout. Do not mix examples from a newer framework release with an older installed daemon without reviewing format and option changes.

A full-image update gives a clear immutable release boundary. Package updates can be smaller but create more possible combinations and interruption states. Choose from the product's compatibility and bandwidth requirements, then keep the deployed package set observable.

## Evidence for a release candidate

Retain manifest verification, written-artifact hashes, selected-slot state, boot-attempt history, health results and rollback outcome. Include negative tests: wrong board, damaged payload, rejected signature, incompatible data and interrupted writes.

A successful happy-path update is necessary but does not test the state machine's most important failure paths. A test report should say which interruption points ran and which remain open, with the actual storage part and firmware versions.

> [!NOTE]
> **Not run on the reference setup:** deployment, slot switching, bootloader metadata writes, rollback and power-cut tests. The state machine is an original design example. No update framework is claimed to be integrated or verified.

## References

- [RAUC design documentation](https://rauc.readthedocs.io/en/latest/basic.html), slots and update concepts; pin a chosen release before implementation.
- [SWUpdate documentation](https://sbabic.github.io/swupdate/), handlers and bootloader integration; behavior depends on the selected build.
- [Boot image composition](../07-boot-images-and-bootgen/01-bif-file-format.md) and [raw flash update boundaries](01-mtd-and-flash.md).

---

<sub>← [SD and eMMC](03-sd-and-emmc.md) · [Chapter index](README.md) · [Boot-Time Optimization](05-boot-time-optimization.md) →</sub>
