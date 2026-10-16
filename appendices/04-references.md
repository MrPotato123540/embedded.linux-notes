# References and Sources

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[Appendices](README.md)** · Appendices

## AMD documents

| Document | Use |
| --- | --- |
| UG1085, Device Technical Reference Manual | Hardware mechanisms, boot, processors and controllers |
| UG1087, Register Reference | Register addresses, fields and access behavior |
| UG1137, Software Developer Guide | ZynqMP software stack and platform management |
| UG1144, PetaLinux Tools Reference Guide | Project configuration, builds and packaging |
| UG1283, Bootgen User Guide | Boot-container format, BIF and security |
| UG1400, Vitis Embedded Software Development | Application and debug flows |
| UG909, Dynamic Function eXchange | DFX design and implementation |
| PG252, Video Codec Unit | VCU interfaces and supported configurations |
| DS891, Device Family Overview | Variant capabilities |

Use the 2024.1 software/tool editions. The locally available UG1085 hardware reference is v2.5; hardware-document revision and software-release version are different labels.

## Pinned source families

| Repository | Release reference |
| --- | --- |
| `embeddedsw`, `device-tree-xlnx` | `xilinx_v2024.1` |
| `linux-xlnx`, `u-boot-xlnx`, `arm-trusted-firmware` | `xilinx-v2024.1` |
| `meta-xilinx`, `meta-xilinx-tools`, `meta-petalinux` | `rel-v2024.1`; archive exact commits for reproduction |
| Poky/OE-Core in the BSP | Inspect shipped metadata; reference identifies Yocto 4.1.4 Langdale |

Tags use different separators. Do not silently replace underscores with hyphens when checking out sources.

## Upstream references

- [Linux 6.6 documentation](https://docs.kernel.org/6.6/)
- [Yocto Project 4.1.4 documentation](https://docs.yoctoproject.org/4.1.4/)
- [U-Boot v2024.01 documentation](https://docs.u-boot.org/en/v2024.01/)
- [TF-A v2.10 documentation](https://trustedfirmware-a.readthedocs.io/en/v2.10/)
- [Devicetree specifications](https://www.devicetree.org/specifications/)
- [OpenAMP documentation](https://openamp.readthedocs.io/)
- [XRT 2024.1 documentation](https://xilinx.github.io/XRT/2024.1/html/index.html)

## Evidence and limits

The sibling `reference-setup/captures` directory contains earlier target sessions plus the new Bootgen decode, FIT listing and PetaLinux help captures. These are local reference artifacts, not files shipped inside this guide repository.

New chapters distinguish source-based explanation from executed tests. Notes marked **Not run on the reference setup** remain open validation work. No chapter should be marked fully verified merely because its outline has been replaced by prose.
## Choose the source that answers the question

| Engineering question | Best starting point | Necessary cross-check |
| --- | --- | --- |
| What does a register bit mean? | UG1087 named register page | UG1085 mechanism and the relevant driver access |
| Which branch does firmware take? | Matching tagged firmware source | Build options and the actual binary/log |
| Which recipe creates a file? | Shipped layer metadata and task outputs | Artifact identity in the release manifest |
| Is a device-tree property accepted? | Binding schema | Driver implementation in the selected release |
| Which runtime API is available? | Installed headers and package version | Loaded kernel/firmware and runtime result |
| Did the board enforce a security rule? | Controlled positive/negative target test | Device policy and exact artifact digests |

No single source answers every row. A manual describes intended hardware behavior. A source tree describes a particular implementation. A log describes one execution under particular conditions. A reliable explanation connects them without turning one kind of evidence into another.

## Source paths used for mechanism-level reading

| Area | Pinned source path or family | What to trace |
| --- | --- | --- |
| FSBL | `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/` | Stage transitions, partition loading, authentication and handoff |
| PMU firmware | `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/` | IPI dispatch, module handlers, power/reset ownership |
| TF-A | `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/` | Early setup, memory layout and secure/non-secure entry data |
| Bootgen | `bootgen@xilinx_v2024.1:authentication-zynqmp.cpp` and `encryption-zynqmp.cpp` | Host-side protected image construction and input validation |
| Linux boot | `linux-xlnx@xilinx-v2024.1:arch/arm64/kernel/head.S` and `init/main.c` | Architecture entry and transition to userspace |
| Linux drivers | `linux-xlnx@xilinx-v2024.1:drivers/` plus matching bindings | Probe, resource acquisition, runtime calls and teardown |
| Yocto security | Shipped `poky/meta/classes/cve-check.bbclass`, `create-spdx.bbclass` | Inventory generation, matching rules and report limits |

Repository locations are part of the citation. Bootgen's ZynqMP source files listed above are at the repository root in the inspected tag. Do not invent a path from a similar project layout. The underscore in `xilinx_v2024.1` and hyphen in `xilinx-v2024.1` are significant.

For moving release branches, preserve the exact commit. A branch name identifies a development line, not immutable content. Likewise, a layer directory copied into a BSP may have local patches or no complete Git history. Archive the actual source snapshot or its reproducible provenance.

## Software baseline and conceptual references

The guide's software baseline is PetaLinux 2024.1 with Linux 6.6.10, U-Boot 2024.01 and TF-A 2.10 from the corresponding AMD source families. The shipped Yocto metadata identifies Langdale 4.1.4. These version numbers do not imply that all associated projects use the same release numbering.

OP-TEE and updater documentation is used to explain architecture where no integrated target deployment is claimed. Each such section states that limit. A conceptual reference should not silently become a claim that its version is included in the BSP.

Hardware documents also have independent revision numbers. UG1085 v2.5 is not a software tool release called 2024.1. Product guides can describe IP revisions that need to be matched to the actual exported hardware design. Preserve the XSA and relevant IP configuration when validating a hardware-specific statement.

## How to resolve conflicting evidence

If a binding allows a value but a driver rejects it, report both and explain the effective implementation limit. If source defaults differ from a build recipe's overrides, identify the final build input. If a project configuration differs from a prebuilt image, use the image's own manifest and binary inspection to describe that image.

The revised chapters include concrete examples of these cases. They are not reasons to ignore documentation. They show why release-specific engineering needs a trace from specification to implementation to artifact.

When a captured output surprises you, first verify its provenance: target identity, image digest, tool version and command context. A correct log from another build can still lead to the wrong conclusion. Avoid “fixing” the explanation by assuming the output must match an expected default.

## Evidence classes in this repository

**Inspected source** means the relevant code or metadata was read at the named release or local BSP path. It supports an implementation explanation, subject to build configuration. **Inspected artifact** means a real binary/container/archive was decoded. It supports statements about that file.

**Executed host experiment** means a command or small program ran on the host. Examples include boot-image regeneration, the authentication corruption test and the cryptography API lab. **Captured target session** refers to an identified earlier QEMU/target record. **Proposed target procedure** describes work still requiring the named hardware or system setup.

The distinction matters for results. An offline overlay merge demonstrates device-tree tooling behavior; it does not demonstrate safe runtime driver removal. A host module compilation checks one build environment; it does not prove AArch64 target execution. A valid Bootgen signature check does not establish eFUSE trust enforcement.

## Preserve a reproducible evidence bundle

Keep tool versions, exact commands, exit status, input digests and output together. Include the source revision or BSP artifact identity that explains the result. Store secrets separately; public-key fingerprints normally provide the needed key identity without exposing private material.

The local `reference-setup/captures` directory is outside this Git repository. Essential findings and trimmed real outputs are reproduced in the relevant chapters so a reader can understand the claim without that directory. Full local captures remain supporting evidence, not repository download links.

External URLs can move and “latest” documentation can change. Prefer pinned versions for software behavior. Current legal dates or support guidance need a fresh official-source check and a stated check date. This revision consulted selected primary sources; it did not perform an exhaustive automated availability check of every external link.


---

<sub>← [Register Quick Reference](03-register-quick-reference.md) · [Chapter index](README.md)</sub>
