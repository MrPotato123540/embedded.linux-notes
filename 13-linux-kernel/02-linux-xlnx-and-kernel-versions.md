# linux-xlnx and Kernel Versions

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers

## Version is more than a number

Mainline development, stable maintenance and vendor integration are different source histories. A vendor kernel can contain selected fixes that are absent from its base version and omit other fixes available upstream.

The inspected 2024.1 recipe selects:

| Field | Value |
| --- | --- |
| `LINUX_VERSION` | `6.6.10` |
| `KBRANCH` | `xlnx_rebase_v6.6_LTS` |
| `SRCREV` | `3af4295e00efdced3e8c6973606a7de55f6bf7dc` |

The saved target banner contains the same abbreviated commit. Record the recipe, configuration and local patches as well as `uname -r`.

## Backports

To assess a fix, find the upstream change, check whether equivalent code already exists, and review its dependencies. Applying one patch without its prerequisite can compile successfully but change behavior incorrectly.

Test the affected subsystem and a representative product workload. For security fixes, map the issue to actual configuration and reachable code rather than deciding from the version string alone.

## References

- Inspected `meta-xilinx@rel-v2024.1:meta-xilinx-core/recipes-kernel/linux/linux-xlnx_2024.1.bb`
- Saved target kernel banner

---

<sub>← [Kernel Fundamentals](01-kernel-fundamentals.md) · [Chapter index](README.md) · [Kernel Image Formats](03-kernel-image-formats.md) →</sub>
