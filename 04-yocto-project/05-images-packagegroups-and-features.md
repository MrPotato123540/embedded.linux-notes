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

## Read image composition as a dependency calculation

An image recipe does not copy every file from every built recipe. It supplies a package selection to the root filesystem task. The package manager then resolves required dependencies, considers recommendations according to policy, checks conflicts and installs files. This means the installed set is normally larger than the initial `IMAGE_INSTALL` list.

A packagegroup is useful because it names a product capability using package dependencies. The packagegroup itself can be empty. The inspected `packagegroup.bbclass` enables empty packages and removes source-fetching, compilation and installation tasks that a dependency-only group does not need. Its purpose is to express composition, not to compile another executable.

Consider a product with measurement, maintenance and development functions. A measurement group might depend on the application and its runtime data. A maintenance group might contain field diagnostics. A development group might contain debuggers and tracing tools. Selecting these groups separately gives the release image a clear policy and prevents a debugger from becoming an accidental dependency of the main application.

Here is an original packagegroup fragment. It illustrates metadata structure; the named application packages are examples and this fragment has not been built:

```bitbake
SUMMARY = "Measurement application runtime"
LICENSE = "MIT"
inherit packagegroup

RDEPENDS:${PN} = "sensor-service sensor-config"
```

Both named packages must exist in the active layer set. A group cannot manufacture a missing package. If the dependencies vary by hardware, review the package architecture rather than leaving a machine-dependent group marked as architecture-independent. The shipped class documents this distinction explicitly.

## Features can change packages or build behavior

`IMAGE_FEATURES` is interpreted by image classes. Some entries map to packagegroups. Others change root filesystem policy. In the inspected `core-image.bbclass`, `ssh-server-openssh` maps to an SSH packagegroup and replaces the Dropbear image feature. `package-management` requests package-management support and preserves its database. These are policies implemented by metadata, not arbitrary feature names recognized by the kernel.

`DISTRO_FEATURES` works at a broader level. Recipes may inspect it to enable or disable build options. Adding a distribution capability can therefore rebuild software without adding that software to an image. Conversely, installing a package does not guarantee it was built with the feature the application needs. Trace both package selection and recipe configuration.

`MACHINE_FEATURES` advertises hardware-related capabilities to metadata. It does not create hardware and does not replace the device tree. If a board lacks a connection or a peripheral clock, a feature string cannot make the driver work. Keep hardware description, build policy and runtime discovery separate when diagnosing a missing function.

## Root filesystem formats are separate from package content

The same installed file tree can produce more than one output format. An archive, an ext4 image and a flash-oriented filesystem have different uses and storage assumptions. Selecting a format changes how files are represented and deployed; it does not automatically change which boot device Linux selects.

For an SD-card product, partition layout, boot files and the root filesystem must agree with the bootloader configuration. For an initramfs design, the early userspace content must provide the tools and drivers needed before any later root filesystem is mounted. For a read-only design, applications need explicit writable locations for state, logs and temporary files.

A read-only root filesystem also changes package installation expectations. Work normally deferred to first boot may need to complete during image construction. A successful package build does not prove that its first-boot scripts are suitable for a read-only target.

## Diagnose image growth with evidence

When an image becomes larger, compare manifests and package sizes first. A small package-selection change can pull in a large dependency tree. Development headers, debug symbols, locale data and package-manager metadata can also change image size without changing the main application.

Separate file content from filesystem overhead and free space. The apparent size of an image file is not the same as the sum of application files. Filesystem metadata, alignment, reserved space and sparsity affect storage use. A filesystem can have enough total free bytes yet lack the layout or inodes required by a workload.

For a controlled comparison, keep the machine, distribution, layer revisions and image format fixed. Change one packagegroup or feature, build both images, and record package additions and removals. Then inspect the files responsible for the size change. This produces an explanation that a release reviewer can reproduce.

## Verify the final consumer

For the sensor-service example, a useful acceptance test follows the complete chain: the package owns the executable, the image manifest lists that package, the deployed root filesystem contains the expected file, and the service starts with the intended user and configuration. A package file in `tmp/deploy` proves only that packaging occurred.

Finally, test the image as delivered. Installing a missing library manually during development can make the current target work while leaving the release image broken. Record such changes and move their requirements into metadata before calling the image complete.

**Source trail:** local `poky/meta/classes-recipe/packagegroup.bbclass`, `core-image.bbclass`, `image.bbclass`, and `poky/meta/recipes-core/images/core-image-minimal.bb`. The source inspection is complete; the product-image examples above remain design exercises until built and tested.

## References

- `meta-petalinux@rel-v2024.1:recipes-core/images/petalinux-image-minimal.bb`
- Local BSP: `poky/meta/classes-recipe/packagegroup.bbclass`, `poky/meta/classes-recipe/image.bbclass`
- Yocto 4.1.4 [image features](https://docs.yoctoproject.org/4.1.4/ref-manual/features.html)

---

<sub>← [BitBake Tasks and the Build Process](04-bitbake-tasks-and-build-process.md) · [Chapter index](README.md) · [Machine and Distro Configuration](06-machine-and-distro-configuration.md) →</sub>
