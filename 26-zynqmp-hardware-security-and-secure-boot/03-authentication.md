# Boot Image Authentication (RSA)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Key hierarchy

ZynqMP authentication uses a primary/secondary key hierarchy. **PPK** and **SPK** mean Primary Public Key and Secondary Public Key. Their private counterparts sign the required structures. Device policy can anchor the primary public-key hash in eFUSE and apply supported revocation controls.

Keep the primary signing authority separated from routine release signing where the chosen flow permits. Record key selection, identifiers and revocation state with the device provisioning record.

## BIF and verification

Bootgen authentication attributes select the image's signed structure and key inputs. Use the ZynqMP-specific format; a generic OpenSSL signature is not a replacement for the required boot certificate layout.

Boot-header authentication can support development without the same eFUSE trust enforcement used in production. Do not describe that test mode as equivalent to a provisioned hardware root of trust.

Test a valid image, modified payload, incorrect key and revoked-key case using disposable test devices and keys. A successful valid-image boot tests only the positive path.

> [!NOTE]
> **Not run on the reference setup:** authenticated hardware boot and device revocation tests. Host verification is recorded below.

## Follow the 2024.1 verifier

ZynqMP boot authentication uses RSA-4096 in the device-specific certificate format. The primary private key authorizes the secondary public key; the secondary private key signs the relevant image structures. The device checks the primary key against its configured trust policy. Keep this hierarchy separate from the X.509 certificate chains used by TLS.

The pinned FSBL implementation is `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_authentication.c`. Read the checks as separate failure boundaries:

| Function or path | Question it answers | Failure meaning |
| --- | --- | --- |
| `XFsbl_PpkVer()` | Does the primary key meet the device's key and revocation policy? | A mathematically valid signature is not enough to establish device trust |
| `XFsbl_SpkVer()` | Was the secondary key authorized, and does its identifier meet the enabled policy? | Secondary-key authorization or identifier/revocation failure |
| `XFsbl_PartitionSignVer()` | Does the protected partition match its signature? | The signed bytes and loaded bytes do not agree, or the signature structure is invalid |
| `XFsbl_Authentication()` | Do the required subordinate checks succeed? | The caller must propagate failure instead of continuing the handoff |

The source contains different hash-padding selections for different structures. Do not replace this format with a generic command that signs a file using an arbitrary RSA padding mode. Bootgen and the ROM/firmware verifier must agree about the certificate layout, byte order, covered range and padding.

## Key identifiers are policy, not comments

In `XFsbl_SpkVer()`, when eFUSE RSA enforcement is enabled, the SPK-eFUSE selection compares the image SPK identifier with the configured identifier. The user-eFUSE selection uses the supported identifier range and checks the corresponding revocation bit. These are different rules. A larger identifier is not automatically a newer software release.

Bootgen's `auth_params` selects such policy inputs. A release record should preserve the chosen PPK selection, SPK selection and SPK identifier together with the public-key fingerprints. Preserve the generated BIF as well. A filename such as `production.pem` does not identify a key reliably.

Revocation also changes recovery. Before retiring a key, establish that the remaining accepted key can boot every required maintenance image. Test that transition on a suitable development device before making irreversible production changes.

## Executed host experiment: valid and changed payloads

On 16 October 2026, the reference host generated two temporary RSA-4096 keys and used Vivado's Bootgen 2024.1 to sign a fixture containing the BSP FSBL. The following BIF is the tested structure with temporary directory names shortened:

```text
lab:
{
    [fsbl_config] bh_auth_enable
    [pskfile] primary.pem
    [sskfile] secondary.pem
    [bootloader, destination_cpu=a53-0, authentication=rsa] zynqmp_fsbl.elf
}
```

This is a single-FSBL authentication fixture, not a complete Linux boot image. The actual run used absolute input paths. The key files were created in a private temporary directory and removed after the test. No private key is stored in this repository.

The executed verification commands are shown with the captured directory name:

```console
$ /tools/Xilinx2024.1/Vivado/2024.1/bin/bootgen -arch zynqmp -verify /tmp/guide-auth-eqozf07_/signed.bin
...
    Header Signature Verified
...
    BootHeader Signature Verified
    SPK Signature Verified
    Partition Signature Verified
...
$ /tools/Xilinx2024.1/Vivado/2024.1/bin/bootgen -arch zynqmp -verify /tmp/guide-auth-eqozf07_/changed.bin
...
    Header Signature Verified
...
    BootHeader Signature Verified
    SPK Signature Verified
    Partition Signature Verification Failed
[ERROR]  : Authentication verification failed on bootimage /tmp/guide-auth-eqozf07_/changed.bin
```

The valid file returned exit status 0. The changed file returned exit status 1. The test changed one payload byte at file offset `0x2900`; it left the certificate and header structures intact. This explains why the early checks still pass while the partition check fails. The offset was derived from this fixture's partition header and is not a reusable offset for other images.

The full local capture is `reference-setup/captures/bootgen-auth-host-lab-2026-10-16.txt`, outside the repository. This experiment establishes host-side detection of a changed signed payload. It does not establish that a board accepts the intended PPK, rejects a revoked SPK or enforces secure boot after reset.

## Why development authentication is insufficient

Bootgen 2024.1 documents `bh_auth_enable` as a mode that excludes PPK-hash and SPK-ID verification. It is useful for testing image authentication mechanics without the equivalent provisioned trust policy. An attacker who can replace the whole development image can also supply another self-consistent key hierarchy unless device policy anchors it elsewhere.

Production acceptance therefore needs additional negative cases: an otherwise valid image under an untrusted primary key, an unauthorized secondary key, a revoked key and an unsigned alternative boot path. Each case tests a different decision. Keep their results separate from the host corruption test above.

If a signature fails, first compare artifact hashes at packaging, storage and load time. A wrong key and a damaged read are different causes. Preserve the earliest verification error; a later fallback or reset message can hide the original boundary that rejected the image.

## References

- AMD UG1283 (2024.1), ZynqMP Authentication Support, PPK/SPK and authentication examples

---

<sub>← [Chain of Trust](02-chain-of-trust.md) · [Chapter index](README.md) · [Boot Image Encryption (AES-GCM)](04-encryption.md) →</sub>
