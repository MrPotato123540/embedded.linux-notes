# FIT Images and image.ub

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot


## A FIT describes images and valid combinations

A **Flattened Image Tree (FIT)** uses a device-tree-based container to describe payloads and boot configurations. Its `/images` nodes describe objects such as a kernel, device tree and ramdisk. Its `/configurations` nodes select combinations of those objects.

This separation lets one container carry several hardware descriptions or boot choices without duplicating every payload. A configuration name is therefore part of the selected boot identity. Saying only “boot image.ub” can hide which kernel/DTB/ramdisk combination was chosen.

A FIT is not the same as the board's hardware DTB. Both use the flattened-tree encoding, but their schemas and purposes differ. The FIT can contain a hardware DTB as one payload. Passing the FIT root itself to Linux as its hardware description is not equivalent to selecting that payload.

## The actual reference image.ub

The saved host `dumpimage -l` inspection describes `image.ub` as a PetaLinux 6.6.10 FIT. It contains:

| Node | Stored size | Compression metadata | Role |
| --- | ---: | --- | --- |
| `kernel-1` | 10,439,067 bytes | gzip | AArch64 Linux kernel |
| `fdt-system-top.dtb` | 54,985 bytes | none | Hardware device tree |
| `ramdisk-1` | 5,464,979 bytes | none | Initramfs image payload |

The default configuration is `conf-system-top.dtb`. It references those three nodes. The kernel's load and entry addresses are both `0x00200000` in the inspected metadata.

The ramdisk's `compression = none` describes what U-Boot should do with that FIT payload. It does not prove that the payload contains an uncompressed filesystem. An initramfs archive can itself use a compression format that Linux later handles. Keep container-level compression and the payload's internal format separate.

## Loading the container is not its final memory layout

The local boot-script recipe defaults to loading the FIT at `0x10000000`. The kernel metadata asks for execution at `0x00200000`. Thus, source container storage and destination kernel storage are separate ranges in the normal flow.

U-Boot selects the configuration, finds the referenced image nodes, verifies required integrity/authentication information, handles compression and prepares the operating-system images. The compressed kernel's 10,439,067 bytes do not describe its full output footprint.

A memory review must include the FIT source, decompression destination, final kernel runtime region, DTB space and ramdisk. Overlap can corrupt a payload before it is consumed, even if each individual address is aligned. The order of copying and decompression matters as well as the final map.

## A hash checks bytes, not their trusted origin

The reference image nodes report SHA-256 hashes. A hash can detect a difference between payload bytes and the expected digest in the container. If an attacker can replace both payload and digest, an unsigned hash does not establish who supplied the image.

FIT signature verification adds a trust decision based on a trusted key and configured verification policy. The key used to establish trust must come from a protected location, such as the verified U-Boot control data in the intended chain. A key carried only inside an untrusted replacement image is not an independent trust anchor.

The policy must also require verification on the boot path. A build that supports signatures but allows another unauthenticated path does not enforce the same system property. Review the selected configuration, required signatures and alternative boot commands together.

## Why configuration verification matters

Authenticating only individual payloads can leave a question about their combination. A kernel and a DTB can each be valid signed objects but belong to different releases or hardware designs. A configuration signature can bind the intended relationships, subject to the FIT signing scheme and verification policy.

The implementation in `boot/image-fit.c` handles image/configuration lookup and hash processing. `boot/image-fit-sig.c` contains signature-verification logic. Read both when diagnosing a rejection; “bad FIT” can mean malformed structure, a missing referenced node, a hash mismatch, a signature failure or an unsupported algorithm.

A useful failure report names the selected configuration and the exact failed node or verification step. Otherwise, replacing the whole container can hide which policy or artifact was wrong.

## Build reproducibility and artifact identity

Maintain the FIT source description and payload inputs. Record the kernel, DTB and initramfs hashes before packaging, then record the final container hash. A successful build does not prove that the deployed `image.ub` uses the new DTB rather than an older copied file.

Time fields and build metadata can affect the final container identity. Reproducibility requires controlled inputs, not only the same kernel version string. For update systems, tie the configuration identity to the expected root filesystem and application release as well.

## Debug the container and the boot protocol separately

If listing the FIT fails, investigate file truncation or format first. If listing works but a configuration cannot be found, inspect its exact name and references. If verification fails, preserve the expected digest/key policy and actual bytes. If verification succeeds but Linux never prints, move to placement, DTB and AArch64 handoff analysis.

A verified container can still describe the wrong hardware. Cryptographic validity says that an authorized source approved the bytes under the configured policy; it does not independently prove electrical compatibility or driver correctness.

> [!NOTE]
> **Not run on the reference setup:** a newly signed FIT, key-enforcement negative tests and a modified FIT boot. The reference container was listed on the host; no signature-enforcement success is inferred from its SHA-256 hash nodes.

## References

- Saved `reference-setup/captures/fit-image-list.txt` from the supplied `image.ub`.
- [2024.1 FIT implementation](https://github.com/Xilinx/u-boot-xlnx/blob/xilinx-v2024.1/boot/image-fit.c) and adjacent `image-fit-sig.c`.
- [U-Boot 2024.01 FIT documentation](https://docs.u-boot.org/en/v2024.01/usage/fit/howto.html), container and configuration model.

---

<sub>← [Environment, boot.scr and uEnv.txt](03-environment-and-boot-scripts.md) · [Chapter index](README.md) · [How U-Boot Boots the Linux Kernel](05-how-u-boot-boots-linux.md) →</sub>
