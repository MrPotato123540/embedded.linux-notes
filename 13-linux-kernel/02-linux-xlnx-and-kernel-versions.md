# linux-xlnx and Kernel Versions

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers


## A version string is only part of the source identity

Linux mainline development, stable maintenance and vendor integration are different histories. AMD's `linux-xlnx` adds and maintains platform support on a selected upstream baseline. A vendor kernel can include backported changes that are newer than its base version while retaining other older code.

The inspected PetaLinux 2024.1 recipe selects:

| Field | Local recipe value |
| --- | --- |
| `LINUX_VERSION` | `6.6.10` |
| `KBRANCH` | `xlnx_rebase_v6.6_LTS` |
| `SRCREV` | `3af4295e00efdced3e8c6973606a7de55f6bf7dc` |
| Kernel metadata branch | `yocto-6.6` |
| `SRCREV_meta` | `5d0809d0d939c7738cb6e5391126c73fd0e4e865` |

These are values read from `meta-xilinx-core/recipes-kernel/linux/linux-xlnx_2024.1.bb`. The recipe include and project appends can add patches and configuration. The Git revision is therefore necessary provenance, but not the whole build identity.

## Connect recipe identity to the deployed image

The saved FIT description contains `6.6.10-xilinx-v2024.1+gitAUTOINC+3af4295e00`. The abbreviated revision matches the recipe's source revision prefix. This is useful evidence that the supplied artifact belongs to the expected source family.

It does not prove that every local patch is absent or that two images with the same displayed release are byte-identical. Build configuration, compiler, generated inputs and local modifications can differ without a sufficiently unique release string.

Record the final image hash, full source revision, patch series, final `.config`, toolchain identity and recipe/layer revisions. For modules, keep the matching build outputs and symbol information. For boot debugging, also keep the DTB and firmware set.

## Tags, branches and commits answer different questions

A branch is a line of development that can move. A tag names a selected point according to project practice. A commit identifies exact repository content. A recipe with a fixed `SRCREV` avoids silently following later branch changes, but downloaded patches and other inputs still need fixed identities.

Use the release tag as a readable source-navigation reference and the resolved recipe commit as build provenance. If the recipe commit and tag differ, inspect that difference rather than assuming the names are interchangeable.

A source archive copied from another workstation needs the same care. A directory called `xilinx-v2024.1` is not proof of its contents unless its origin or hashes are recorded. The source snapshots used in this guide were downloaded from pinned release paths for inspection.

## Backport a behavior, not just a patch filename

Suppose an upstream fix changes how a driver releases a DMA buffer during removal. First find the failing behavior and the fix's prerequisites. Then compare the vendor implementation: equivalent logic may already exist under a different commit, or surrounding APIs may differ.

A clean patch application only proves textual compatibility. A successful compile only proves one set of build constraints. The important question is whether the updated lifecycle is correct in this tree, including error paths and concurrent callbacks.

Review related commits when the fix depends on a prior refactor or helper change. Applying only the final patch can leave the code with a subtle semantic mismatch even when every symbol exists.

## Kernel interfaces have different stability promises

Linux preserves its userspace ABI with strong compatibility goals. Internal driver interfaces are a different matter. An out-of-tree module can need source changes when the kernel changes, and binary compatibility depends on the exact build and configuration.

The device-tree binding is also an interface between hardware description and driver behavior. A kernel update can expose previously ignored invalid properties or change which supported binding variant is selected. Review the DTB together with the driver change.

Firmware interfaces form another boundary. The kernel's platform-management wrappers may request features that an older PMUFW or TF-A does not support. A kernel upgrade that boots is not complete until relevant runtime firmware operations are exercised.

## Evaluate a reported defect from reachable code

A base version number alone cannot establish whether a particular fix is present. Inspect the relevant code and patch history. Also check whether the affected subsystem is enabled and whether the product can reach the faulty path.

Configuration can remove one exposure, but it does not replace understanding the issue. A disabled driver today may become enabled in another product variant. Keep the analysis tied to an exact configuration and artifact rather than a broad statement that all 2024.1 images are equivalent.

For security-related maintenance, use the vendor and upstream records for the specific issue and preserve the evidence behind the decision. This section does not provide a current vulnerability inventory for the reference image.

## Plan upgrades as a compatibility set

A controlled upgrade compares source changes, configuration changes, device-tree bindings, modules, firmware interfaces and userspace behavior. Keep an old known artifact set available for diagnosis and compare the same workload on both versions.

Start with the subsystem affected by the update, then test boot, storage, networking and the product's critical paths as appropriate. A change in scheduler or memory behavior can expose a driver race that was already present. A failure after an upgrade is not automatically proof that the new upstream code introduced the original bug.

## References

- Local BSP: `meta-xilinx/meta-xilinx-core/recipes-kernel/linux/linux-xlnx_2024.1.bb` and `linux-xlnx.inc`.
- [Pinned AMD Linux source revision](https://github.com/Xilinx/linux-xlnx/tree/3af4295e00efdced3e8c6973606a7de55f6bf7dc).
- Saved `reference-setup/captures/fit-image-list.txt` and target boot banner.

No kernel upgrade or backport was applied as part of this documentation revision.

---

<sub>← [Kernel Fundamentals](01-kernel-fundamentals.md) · [Chapter index](README.md) · [Kernel Image Formats](03-kernel-image-formats.md) →</sub>
