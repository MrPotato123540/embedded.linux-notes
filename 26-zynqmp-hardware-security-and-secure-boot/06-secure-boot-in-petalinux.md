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

## Start with the actual PetaLinux artifacts

The reference `xilinx-zcu106-2024.1` BSP provides a useful unsigned baseline. Its recorded boot image uses five binary inputs: FSBL, PMU firmware, TF-A, device tree and U-Boot. The `pmufw_image` input has special boot-image handling, so five inputs do not mean five ordinary image headers. There is no PL bitstream partition in this particular BIF.

That detail matters when introducing security. Adding authentication to the existing partitions does not protect a PL image loaded later from a separate file. Adding a bitstream to the BIF also changes memory use, image size and the partition-loading path. Review the actual generated container, not only the command that was intended to create it.

The earlier packaging experiment regenerated the supplied `BOOT.BIN` using Bootgen 2024.1 and the unchanged inputs. Both files were 1,838,720 bytes with SHA-256 `97363bab9a28ecda6713840aa55986b98b09fd51b016b030224064f04af612ff`. This establishes packaging reproducibility for those files. It does not mean the firmware was rebuilt or that secure boot was enabled.

## Use a staged integration matrix

| Stage | Input | Required evidence before moving on |
| --- | --- | --- |
| Baseline | Known unsigned BSP artifacts | Reproducible packaging and a known boot log |
| Host authentication | Development keys and explicit BIF | Valid verification plus changed-payload rejection |
| Device authentication | Signed full image and intended test-device policy | Boot acceptance and wrong-key/unsigned-image rejection |
| Later verified boot | Required FIT policy and trusted rootfs metadata | Kernel, device-tree and rootfs negative tests |
| Optional encryption | Supported key source and protected container | Decryption, retention and incompatible-key-source tests |
| Production lifecycle | Final keys, update and recovery policy | Rotation, rollback, power-loss and recovery evidence |

The first two rows have host evidence in this guide. The hardware rows remain open. Keeping these stages separate makes failure diagnosis easier: an encryption integration error should not be mixed with an unproven basic boot flow.

## Separate build outputs from signing authority

A normal build worker produces unsigned artifacts and an inventory of their digests. A signing service accepts a release request only after checking that inventory, the intended board family and the authorized release policy. It returns protected artifacts together with public signing metadata.

This boundary matters even when the private key stays in an HSM. If any build worker can ask the HSM to sign arbitrary bytes, the worker still has effective release authority. The signing request must bind the artifact to its product, version and purpose.

PetaLinux packaging is the assembly step. It must receive the intended firmware and attributes, and it must preserve the generated BIF or an equivalent complete record. Avoid a release process that rebuilds or modifies firmware after approval and then signs the new bytes under an old approval record.

The final deployment digest belongs to the signed/encrypted container. The unsigned-input digests belong to the build record. Preserve both. Encryption or signatures can change the container without changing the underlying source build, so one digest cannot answer both questions.

## Configuration spans several components

Secure boot is not one PetaLinux menu setting. The FSBL must include the required security support. Bootgen must create the supported authenticated partitions. Device provisioning must establish the intended trust policy. U-Boot must enforce the later FIT policy. The kernel and root filesystem must enforce their part of the chain.

Inspect generated configuration and actual binaries, not only project defaults. The reference BSP's project configuration and prebuilt images were not always created at the same time. A current configuration file cannot prove which options exist in an older prebuilt FSBL or kernel.

Use the FSBL build map and size report after enabling additional features. OCM has limited capacity and parts of the early boot memory are reused by later stages. An enlarged authenticated FSBL must still fit the selected memory layout. Link-time success and boot-container generation are necessary checks, but they do not establish correct runtime lifetimes.

## Make a failure report identify the boundary

If no FSBL output appears, preserve BootROM-visible status and the exact image used. If FSBL starts but rejects a partition, record the first authentication/decryption error and partition identity. If U-Boot starts but rejects Linux, focus on the FIT key, configuration and covered data. If Linux starts but root mounting fails, inspect the trusted root hash and storage mapping.

This sequence avoids replacing keys to solve an unrelated storage read error. It also avoids treating a successful early authentication message as proof that every later payload was protected.

For each negative test, record the expected last successful boundary. A changed FIT payload should not be diagnosed as an FSBL authentication failure when the FIT is loaded later from SD. A changed FSBL should be rejected before its own log can be trusted. These expectations make the test report useful to another engineer.

## Release acceptance includes alternate paths

Review serial-console access, U-Boot command access, network boot, fallback slots and factory recovery under the final policy. Decide which are disabled, restricted or independently verified. Preserve the same rules after a factory reset and after a failed update.

The single-FSBL host fixture in [authentication](03-authentication.md) used temporary development keys and boot-header authentication. It is intentionally not a production BIF. The next milestone is a complete signed image on the intended hardware, followed by rejection and recovery tests. That milestone is not claimed by the host verification result.

## References

- AMD UG1144 and UG1283 (2024.1), secure boot and packaging
- Reference `boot-manual-1.log`

---

<sub>← [eFUSE and BBRAM Programming](05-efuse-and-bbram-programming.md) · [Chapter index](README.md) · [Verified Boot Beyond U-Boot](07-verified-boot-beyond-u-boot.md) →</sub>
