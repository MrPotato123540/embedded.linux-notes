# Layers and the Layer Model

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Concepts

A **layer** is a collection of build metadata. Its `conf/layer.conf` registers recipe search paths, a collection name, dependencies and release compatibility. `bblayers.conf` selects which layer directories participate in a build. A layer on disk has no effect until it is enabled.

| File or variable | Role |
| --- | --- |
| `BBFILES` | Patterns used to find recipes and append files |
| `BBFILE_PRIORITY` | Priority used when recipes compete across layers |
| `LAYERSERIES_COMPAT` | Supported OpenEmbedded release series |
| `LAYERDEPENDS` | Required layer collections |
| `.bbappend` | Changes applied to a matching recipe |

Priority is not a universal rule for every variable. File parsing, overrides and provider selection also matter. Check the final recipe environment when two layers appear to disagree.

## PetaLinux 2024.1 specifics

The inspected BSP ships these useful groups:

| Layers | Main purpose |
| --- | --- |
| `poky`, `meta-openembedded` | Base system and additional software |
| `meta-xilinx`, `meta-xilinx-tools` | AMD hardware support and tool integration |
| `meta-petalinux`, `meta-kria` | PetaLinux distribution and Kria support |
| `meta-openamp`, `meta-virtualization` | Remote processors and virtualization |
| `meta-security`, `meta-xilinx-tsn` | Security components and time-sensitive networking |
| `meta-qt5`, `meta-jupyter` | UI and notebook software |

This is an inventory of shipped directories, not a promise that every layer is enabled. The generated `build/conf/bblayers.conf` is the relevant input for the selected project.

`meta-xilinx` contains multiple sub-layers for core support, boards, standalone software and vendor integration. In the inspected `meta-xilinx-core/conf/layer.conf`, the collection is `xilinx`, priority is `5`, and compatibility is `langdale`.

## Working method

Put product changes in a maintained layer. The `bitbake-layers` tool can create its basic structure and inspect active layers. Before adding it, check its dependencies and release branch. Keep the layer in version control; a copied build directory is not a reliable source of product policy.

> [!NOTE]
> **Not run on the reference setup:** creation and integration of a new standalone layer during this writing pass. The shipped layer files were inspected locally.

## References

- `xilinx-zcu106-2024.1:build/conf/bblayers.conf`
- `meta-xilinx@rel-v2024.1:meta-xilinx-core/conf/layer.conf`
- Yocto 4.1.4 [Development Tasks Manual, layers](https://docs.yoctoproject.org/4.1.4/dev-manual/common-tasks.html#understanding-and-creating-layers)

---

<sub>← [Yocto Project, OpenEmbedded, Poky and BitBake](01-yocto-openembedded-bitbake.md) · [Chapter index](README.md) · [Recipes and Metadata Syntax](03-recipes-and-metadata-syntax.md) →</sub>
