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

## Layer discovery and recipe selection are different operations

A layer becomes visible when its directory is listed in `BBLAYERS`. BitBake then reads the layer's `conf/layer.conf`. That file describes where to search for recipes and append files, which collection the layer belongs to, and which other layers it needs. A directory that merely exists beside the build is not automatically active.

Several variables have similar names but different jobs. `BBPATH` helps find configuration and class files. `BBFILES` gives patterns for recipe and append discovery. `BBFILE_COLLECTIONS` names the layer collections. `BBFILE_PATTERN_<collection>` associates paths with a collection, and `BBFILE_PRIORITY_<collection>` gives recipe precedence when candidates compete. `LAYERDEPENDS_<collection>` declares required layer collections. These are not all lists of directory paths.

In the shipped `meta-petalinux/conf/layer.conf`, the collection is `petalinux`, its priority is `6`, and compatibility is declared for `langdale`. The file also has `BBFILES_DYNAMIC` entries. These let some metadata become available when another named collection is present. This matters when a recipe appears on one project but not another: compare active collections before assuming the file was deleted.

Layer priority is not a universal rule that the last setting in the highest-priority directory wins. Provider selection, version preference, override syntax and parse order still matter. Two `.bbappend` files can both apply to the same selected recipe. Increasing a layer priority does not make every conflicting assignment in those files safe.

## A durable product-layer layout

For a product, separate the hardware description from general product policy. A board layer can contain machine configuration and board-specific device-tree changes. A product layer can contain the application, image recipe, service configuration and package groups. This lets a second board reuse the product software without inheriting the first board's hardware assumptions.

The following is an original layout example, not an output captured from the BSP:

```text
meta-product/
  conf/layer.conf
  recipes-core/images/product-image.bb
  recipes-core/packagegroups/packagegroup-product.bb
  recipes-apps/sensor-service/sensor-service_1.0.bb
  recipes-apps/sensor-service/files/sensor-service.service
  recipes-kernel/linux/linux-xlnx_%.bbappend
  recipes-kernel/linux/files/product.cfg
```

The application recipe owns the executable and service file. The package group owns the product package selection. The image recipe owns the root filesystem composition. The kernel append owns a small, reviewable change to the selected kernel recipe. This division gives each change one clear home.

Do not place a shared product policy only in a developer's `local.conf`. That file is useful for local build choices, but another developer may not have the same contents. In PetaLinux, `project-spec/meta-user` is the project customization layer. Follow its supported integration path before adding another layer; adding a layer does not remove the need to preserve project configuration.

## Why an append may have no effect

An append must match a recipe name and version pattern. A version-specific append can stop applying after a recipe version changes. A `%` pattern can survive a version change, but it also accepts versions whose implementation may have changed. A wide pattern is a maintenance decision, not proof of compatibility.

After confirming the name match, inspect the operation inside the append. A patch must be present in the file search path and listed in `SRC_URI`. A configuration file must reach the task that consumes it. A variable assignment can be overridden later or can apply only to a different machine. Merely seeing the append in a directory proves none of these conditions.

A useful diagnosis follows the same order every time:

1. Confirm that the layer is active in the generated build configuration.
2. Confirm that the intended recipe provider and version were selected.
3. Confirm that the append matches that recipe.
4. Inspect the final value and assignment history of the relevant variable.
5. Inspect the task inputs or staged files to see whether the change reached the build.

This sequence distinguishes a discovery failure from an expansion failure and from a task failure. Each needs a different correction.

## Compatibility and reproducibility

`LAYERSERIES_COMPAT` records the release series for which the layer claims compatibility. Editing that string does not port the layer. A real port must account for removed variables, changed override syntax, renamed classes, recipe version changes and task behavior. Treat a compatibility error as useful evidence about the selected combination.

Pin layer revisions together. A branch name records a moving line of development; a commit identifies one exact state. For a release record, keep each repository URL and commit, any local patches, the selected machine and distribution, and the project configuration. This is especially important when a BSP includes vendor modifications that differ from an upstream release tag.

When two teams both change a common recipe, prefer a small append whose reason is clear. Copying an entire vendor recipe into a product layer makes future updates harder to review because unchanged code hides the actual policy change. A replacement recipe is appropriate when you intentionally take ownership of the full implementation and its maintenance.

**Source trail:** local BSP `meta-petalinux/conf/layer.conf`, `poky/bitbake/doc/bitbake-user-manual/bitbake-user-manual-ref-variables.rst`, and the layer configuration files under `meta-xilinx/`. The priority and series values above were read from the shipped BSP; no new layer build is claimed.

## References

- `xilinx-zcu106-2024.1:build/conf/bblayers.conf`
- `meta-xilinx@rel-v2024.1:meta-xilinx-core/conf/layer.conf`
- Yocto 4.1.4 [Development Tasks Manual, layers](https://docs.yoctoproject.org/4.1.4/dev-manual/common-tasks.html#understanding-and-creating-layers)

---

<sub>← [Yocto Project, OpenEmbedded, Poky and BitBake](01-yocto-openembedded-bitbake.md) · [Chapter index](README.md) · [Recipes and Metadata Syntax](03-recipes-and-metadata-syntax.md) →</sub>
