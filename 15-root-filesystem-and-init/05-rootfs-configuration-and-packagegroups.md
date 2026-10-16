# Rootfs Configuration and Packagegroups

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Package selection

The rootfs menu records image choices. `user-rootfsconfig` can expose custom selections, but the selected package still needs a visible recipe and valid dependencies. Confirm the final manifest rather than relying on a checked menu item.

The locally inspected 2024.1 packagegroups include:

| Group | Direct content observed |
| --- | --- |
| `packagegroup-petalinux-networking-debug` | tcpdump and Wireshark |
| `packagegroup-petalinux-v4lutils` | v4l-utils and yavta |
| `packagegroup-petalinux-audio` | ALSA libraries/tools, SoX; conditional PulseAudio packages |
| `packagegroup-petalinux-openamp` | libmetal, OpenAMP and demo groups, with machine-dependent firmware additions |

Dependencies can expand this list. Machine and distribution overrides can change it further.

## Image size and production

Measure installed sizes and identify why a package is pulled in before removing it. Split development tools from product runtime requirements. A smaller image is not automatically safer if it removes recovery or diagnostics needed in the field.

Check that required licenses, firmware and configuration files remain after trimming. Reboot from the rebuilt image to avoid testing a target that still contains manually installed packages.

## Package selection is a dependency closure

A rootfs is built from selected packages plus their dependencies and image policy. A packagegroup is a recipe that collects package relationships; it is not usually a directory of application binaries. Its value is that one selection can represent a supported feature set.

Build dependencies and runtime dependencies are different. `DEPENDS` provides inputs needed to compile a recipe. `RDEPENDS` identifies packages needed after deployment. A header-only library may be needed at build time but not on the target, while a dynamically loaded plugin can be required at runtime without appearing in the executable's normal shared-library dependencies.

Recommendations are weaker than hard dependencies and can be affected by image policy. A feature that cannot function without a package should not rely only on an optional recommendation. Conversely, using hard dependencies for every convenient diagnostic tool can make a small image much larger than intended.

## A release-specific packagegroup example

The supplied `meta-petalinux/recipes-core/packagegroups/packagegroup-petalinux-vitis-acceleration.bb` creates essential and recommended groups. For ZynqMP, the essential dependency override selects `xrt` and `zocl`. The recommended group includes development and diagnostic tools such as `gdb`, `valgrind`, `htop` and `iperf3`.

The machine override is important. Reading only the generic assignment can produce the wrong picture of what a ZynqMP image includes. BitBake evaluates overrides, appends and configuration before tasks run. Review the effective value for the chosen machine, not merely the first line matching a variable name.

The observed BSP manifest includes both `xrt` and `zocl` at `202410.2.17.0`. That is package-delivery evidence. It does not demonstrate that a compatible accelerator exists in the running PL or that an accelerated application completed.

## Image configuration should express intent

Keep rootfs selections and user-layer metadata in version control. A menu change is useful only if the resulting configuration is retained. A package copied manually into one target is not represented in the next clean image build.

Use recipes to install configuration files, service units, permissions and directories. Use packagegroups to collect coherent capabilities. Avoid hiding product-critical dependencies inside an interactive post-boot script that downloads whatever version happens to be available.

For PetaLinux 2024.1, the project rootfs configuration and `meta-user` layer participate in this process. Generated menus and task work directories should be treated as outputs unless the documented workflow says otherwise. A change that disappears after regeneration was probably made at the wrong layer.

## Why installed size grows unexpectedly

A small application can pull in a large runtime through a shared library, language interpreter or packagegroup. Recommended packages can add debugging tools. Development packages can bring headers and static libraries that are unnecessary for normal operation.

Follow the dependency chain from the new selection to the installed package list. Compare image manifests between builds. This separates intentional functionality from accidental dependencies and gives an explanation for size changes that a total byte count cannot provide.

The compressed output size can also change because of compression, filesystem metadata and duplicate files. For memory planning, account for how the image is used: an initramfs expands into RAM, while a disk root normally demand-loads file pages. Equal archive sizes do not imply equal boot footprints.

## Package installation and first boot are different stages

Some package actions can run during image creation. Others are deferred to the target because they need target state or a running system. This distinction matters for read-only images: a deferred action that writes into the immutable root can fail at first boot even though the image task completed.

The local `libmali-xlnx.bb`, for example, contains target-side handling for library alternatives. Its backend selection and writable-state assumptions need review when creating a read-only product image. Installing the package is not enough evidence that every post-installation action has completed in the intended environment.

Keep first-boot behavior deterministic. Generate machine identity and keys using an explicit product policy rather than accidentally cloning build-time state. Record whether provisioning has completed so a failed first boot can recover without silently repeating an irreversible action.

## Release evidence and update safety

A useful rootfs record includes the image hash, package manifest, build configuration and layer revisions. The manifest is a bill of installed package versions, not a complete record of all source patches or runtime configuration.

For updates, preserve compatibility between applications and shared libraries. Replacing one library while leaving dependent executables from another release can introduce symbol-version failures. Whole-image updates reduce some mixing risks, but persistent configuration and user data still need migration rules.

> [!NOTE]
> **Not run on the reference setup:** rebuilding package selections and validating first-boot post-install actions. The packagegroup, recipes and supplied manifest were inspected directly.

## References

- Inspected BSP `meta-petalinux/recipes-core/packagegroups/packagegroup-petalinux-vitis-acceleration.bb`.
- Inspected BSP `meta-xilinx/meta-xilinx-core/recipes-graphics/libgles/libmali-xlnx.bb` and `pre-built/linux/images/rootfs.manifest`.

- Inspected `meta-petalinux@rel-v2024.1:recipes-core/packagegroups/`
- Reference `rootfs.manifest`

---

<sub>← [Root Filesystem Boot Options in PetaLinux](04-rootfs-boot-options.md) · [Chapter index](README.md) · [Init Systems: SysVinit, systemd and BusyBox init](06-init-systems.md) →</sub>
