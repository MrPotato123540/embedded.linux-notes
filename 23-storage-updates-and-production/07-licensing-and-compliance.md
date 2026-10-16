# Licensing and Compliance

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Start from what the product distributes

A PetaLinux product can distribute Linux, U-Boot, TF-A, applications, libraries, firmware, fonts, media assets and FPGA-related artifacts. These components do not all have the same license. A recipe's license field is useful build metadata, but the component's actual license text and the way it is distributed determine the obligations.

This section explains the technical records needed for a compliance review. It does not determine the legal status of a particular combined product. The responsible legal or licensing reviewer should resolve questions about linking, derivative works, written offers and proprietary redistribution terms using the exact components and distribution model.

Begin with the shipped image and update payloads, then map their files to packages and source inputs. A list of recipes built on a workstation includes tools that may never ship, while a manually copied firmware blob may ship without appearing in the normal package manifest.

## Keep four different artifacts

| Artifact | Question it answers | What it does not replace |
| --- | --- | --- |
| Package/file manifest | What bytes and packages ship? | Actual license terms |
| License notices and texts | Which terms and attributions accompany them? | Corresponding source |
| Software bill of materials | Which components and relationships are recorded? | A complete source-delivery process |
| Source/build archive | Which sources, patches and build inputs produced covered binaries? | Review of distribution obligations |

A **software bill of materials (SBOM)** is an inventory. **SPDX** provides a standard way to represent package, file and license information. Generating an SPDX document is valuable evidence, but it does not automatically provide every required source file or satisfy every license condition.

## Read GPL obligations at the correct boundary

GPLv2 section 3 describes conditions for distributing object or executable code, including corresponding-source and written-offer routes with specific requirements. The source definition includes relevant build and installation scripts, subject to the license's stated scope and exceptions. An upstream project URL alone may not provide the modified source and scripts for the exact shipped binary. [GNU GPLv2 text](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html).

Do not use a general statement such as "all Linux applications must be GPL." The Linux kernel's documented syscall exception addresses ordinary userspace use of kernel services. Kernel modules and linked libraries raise different questions that require their actual code, interfaces and licenses to be reviewed. A `MODULE_LICENSE` string is kernel metadata, not a complete legal analysis. [Kernel licensing rules](https://www.kernel.org/doc/html/v6.6/process/license-rules.html).

Static and dynamic linking can affect the materials and conditions that apply under a particular library license. Neither linking method is a universal exemption. Preserve link inputs, library versions and build flags so the reviewer can analyze the actual combination rather than infer it from a package name.

## Yocto metadata provides useful checks

`LICENSE` declares a recipe's license expression. `LIC_FILES_CHKSUM` checks selected license text content. A checksum change should trigger review of the changed text; updating the checksum merely to silence a build failure removes the value of the check.

The installed 2024.1 layer's `meta/classes-global/license.bbclass` also handles `LICENSE_FLAGS` and `LICENSE_FLAGS_ACCEPTED`. Accepting a flag permits a build under configured policy. It does not purchase rights, sign an agreement or establish redistribution permission.

`license_image.bbclass` uses `COPY_LIC_MANIFEST` and `COPY_LIC_DIRS` to control copying license materials into an image. `LICENSE_CREATE_PACKAGE` supports license packages. These are inspected class interfaces, not a claim that the reference image enabled every option.

Review per-package license metadata where a recipe splits outputs with different content. A broad recipe label can hide a mixed set of libraries, data and firmware. Keep upstream copyright notices and exceptions with the exact files to which they apply.

## Generate source records deliberately

The inspected `archiver.bbclass` supports original, patched, configured and mirror source modes. Its default source mode is `patched`. Options can also preserve recipes, configuration dumps and diffs. Choose the archive content from the delivery requirement and validate the resulting archive, not just the class inheritance line.

The local `create-spdx.bbclass` includes `SPDX_INCLUDE_SOURCES`, `SPDX_ARCHIVE_SOURCES` and `SPDX_ARCHIVE_PACKAGED`; their inspected defaults are zero. Enabling basic SPDX generation therefore does not imply that source and package archives are included. [Yocto 4.1.4 SBOM documentation](https://docs.yoctoproject.org/4.1.4/ref-manual/classes.html#create-spdx-bbclass).

Keep local patches, configuration fragments, generated build inputs needed for the covered work and exact source revisions. A download cache is not a reviewed source package: it can contain unused versions, omit local changes and depend on a build directory that will later disappear.

## Work a concrete VCU inventory example

The installed 2024.1 VCU recipes show different license declarations: `kernel-module-vcu` uses `GPL-2.0-or-later`; `libvcu-xlnx` and `libomxil-xlnx` use `MIT`; `vcu-firmware` uses `Proprietary`. These are inspected recipe declarations and must be checked against the corresponding source/license files and actual distribution permissions.

This example shows why one label for "the video stack" is insufficient. The firmware's presence in a public repository does not itself grant every desired redistribution right. Conversely, a proprietary firmware component does not change the declared license of separate open-source modules. Inventory each component and its relationship accurately.

## Validate the release package, then retain it

For an original release workflow, freeze the image manifest, map shipped files to sources, collect notices and required source materials, then have a clean environment exercise the documented build path. Compare the rebuilt component or explain known reproducibility differences. This provides technical evidence that the source archive corresponds to the intended release.

Retain the archive and the policy record for the applicable support and license periods. A future update needs its own matching set, even if only one component changes. If a written offer is used, its wording, availability and fulfillment process need review; a build system does not create that operational process automatically.

Track unresolved findings explicitly: missing source revision, unknown blob terms, absent notice or unreviewed linking relationship. A build that passes license checksum checks can still have those gaps. Close them with evidence tied to the shipping artifact.

> [!NOTE]
> **Not run on the reference setup:** a complete product license audit, source-offer process or regenerated compliance archive. Kernel license texts and local Yocto class/recipe metadata were inspected. No legal-compliance guarantee is made.

## References

- Inspected `linux-xlnx@xilinx-v2024.1:LICENSES/preferred/GPL-2.0`, `LICENSES/exceptions/Linux-syscall-note` and `Documentation/process/license-rules.rst`.
- Inspected `xilinx-zcu106-2024.1:components/yocto/layers/poky/meta/classes/{archiver,create-spdx}.bbclass`, `classes-global/license.bbclass` and `classes-recipe/license_image.bbclass`.
- [Yocto license workflow](https://docs.yoctoproject.org/4.1.4/dev-manual/common-tasks.html#working-with-licenses), build support and review responsibilities.

---

<sub>← [Reliability and Field Diagnostics](06-reliability-and-field-diagnostics.md) · [Chapter index](README.md) · [CI and Reproducible Builds](08-ci-and-reproducible-builds.md) →</sub>
