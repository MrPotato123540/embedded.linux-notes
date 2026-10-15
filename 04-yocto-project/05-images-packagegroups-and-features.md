# Images, Packagegroups and Features

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Concepts

An **image recipe** selects a root filesystem. A **packagegroup** groups runtime dependencies into a named package. The group usually contains little or no useful file content itself: its dependency list brings in the software.

| Setting | Meaning |
| --- | --- |
| `IMAGE_INSTALL` | Packages requested for this image |
| `IMAGE_FEATURES` | Image policies translated into packages or configuration |
| `EXTRA_IMAGE_FEATURES` | Additional features commonly set by build configuration |
| `IMAGE_FSTYPES` | Output filesystem and archive formats |
| `DISTRO_FEATURES` | Distribution capabilities considered by recipes |
| `MACHINE_FEATURES` | Hardware capabilities advertised by the machine |

A feature is not always a package name. Enabling a distribution feature may change how a recipe builds without installing that recipe. Installing a package may pull in further runtime dependencies.

## PetaLinux 2024.1 specifics

The inspected `petalinux-image-minimal.bb` includes `petalinux-image-common.inc`. Follow that include before deciding what “minimal” contains. `core-image-minimal` is the OE-Core starting image; it is not identical to AMD's image.

For product software, create a packagegroup with `inherit packagegroup` and list required runtime packages in `RDEPENDS:${PN}`. Keep unrelated optional tools in separate groups. This makes it possible to remove development tools without removing the product application.

PetaLinux's rootfs menu exposes package selections and packagegroups. The actual image manifest is the final evidence. A menu choice or recipe filename alone does not prove that a package is installed.

## Validation

Compare manifests before and after a change. Check unexpected dependencies, debug packages and package-manager inclusion. Build history can record package and image changes over time; store it with the build identifier so differences can be explained.

> [!NOTE]
> **Not run on the reference setup:** a new packagegroup build. The BSP image recipe was inspected; package selection changes still need an image build and target check.

## References

- `meta-petalinux@rel-v2024.1:recipes-core/images/petalinux-image-minimal.bb`
- Local BSP: `poky/meta/classes-recipe/packagegroup.bbclass`, `poky/meta/classes-recipe/image.bbclass`
- Yocto 4.1.4 [image features](https://docs.yoctoproject.org/4.1.4/ref-manual/features.html)

---

<sub>← [BitBake Tasks and the Build Process](04-bitbake-tasks-and-build-process.md) · [Chapter index](README.md) · [Machine and Distro Configuration](06-machine-and-distro-configuration.md) →</sub>
