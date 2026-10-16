# Customizing Through meta-user

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Maintained customization

`project-spec/meta-user` is the normal project location for user recipes and append files. Keep a change here when it must survive regeneration. A patch in a temporary source directory is only a debugging experiment until the recipe applies it.

| Change | Maintained input |
| --- | --- |
| Device-tree additions | `system-user.dtsi` and device-tree recipe inputs |
| Kernel options | Configuration fragments and kernel append |
| U-Boot options | U-Boot configuration fragment and append |
| Driver or firmware code | Source patch referenced by the appropriate recipe |
| Image-wide policy | Image configuration or `petalinuxbsp.conf` |

A `.bbappend` must match the recipe name and version pattern. A valid-looking file with the wrong name may never affect the build. Check the final source list and configuration after parsing.

## Device-tree boundaries

Add external board components and product policy in maintained includes. Generated nodes describe exported hardware. Avoid copying an entire generated tree into `system-user.dtsi`: future hardware changes then become difficult to merge.

Linux and U-Boot can use related but different device-tree build paths. A Linux-only property does not automatically configure U-Boot's driver behavior. Inspect both deployed trees when the change affects pre-kernel boot.

## Verification

For a configuration change, inspect the final `.config`. For a patch, inspect the unpacked source after patching. For an installed file, inspect the package and final root filesystem. Finally, confirm the board booted the newly packaged artifact.

> [!NOTE]
> **Not run on the reference setup:** rebuilding all firmware and device-tree providers with a new append. No example here claims a successful patched build.

## Keep the change at the narrowest durable boundary

The user layer extends vendor metadata. A small append can add a patch, a configuration fragment or a board include without copying the whole upstream recipe. This keeps the product change visible when the vendor recipe evolves.

A full recipe copy may be appropriate when the product deliberately takes ownership of that component's recipe. It also carries a larger maintenance burden. Future vendor fixes can be hidden because the copied recipe continues to win provider selection. Review the actual selected provider whenever both a replacement and an append exist.

## Follow the real device-tree append

The inspected device-tree append adds its `files` directory to `FILESEXTRAPATHS` and adds `system-user.dtsi` to `SRC_URI`. The first operation controls where BitBake looks for local inputs. The second declares that the file is an input. Both are needed for a durable recipe relationship.

`system-user.dtsi` includes generated system configuration and supplies user changes. For a board peripheral, a small override can set its status, references or external wiring. Avoid copying the whole generated node when only one property needs to change. A copied node can preserve an old address or interrupt after hardware import updates the original.

A label reference must resolve in the current include set. If a hardware change removes or renames the generated label, the user include must be reviewed. Restoring an old label blindly can reconnect software to a resource that no longer exists.

## A configuration fragment is a request, not the final result

Kernel and U-Boot configuration systems have dependencies. A fragment can request an option that is unavailable under the selected architecture or disabled by another prerequisite. After the build, inspect the final `.config`. The fragment's presence in `SRC_URI` is not proof the option became active.

For a kernel driver, also distinguish built-in and module configurations. A driver required to reach the root filesystem may need to be available before that filesystem is mounted. A module package stored only on the inaccessible root cannot solve the initial access problem. An initramfs can provide an alternative early-loading path when designed for it.

Keep fragments small and record why each option is needed. A complete copied configuration can freeze many unrelated defaults and make upgrades difficult to understand. The final generated configuration remains the authoritative build evidence.

## Source patches belong to the selected recipe

A patch must target the source revision actually used by the recipe. Record the base revision, apply the patch through metadata, and inspect the prepared source after the patch task. A patch in the source tree from a manual experiment is not enough for the next clean build.

Patch filenames and order should explain intent. Separate a functional fix from formatting changes and temporary debugging. Review context changes when a vendor update causes a patch to apply with offsets: successful application is not proof of semantic correctness.

For firmware, trace the patched build result into packaging. A new FSBL ELF can be generated successfully while a later boot package still names the vendor prebuilt ELF. The evidence chain must continue beyond compilation.

## Install files through a recipe

A product configuration file should have a package owner and installation permissions. Installing it manually on the development target hides that ownership from the image build. A recipe installation task stages the file under `${D}`, and packaging then assigns it to an output package.

Consider whether the file is immutable policy, a user-editable setting or runtime state. These have different update and preservation requirements. A release image should not overwrite device-specific state merely because it ships a new default configuration. The update strategy must define how defaults and persistent settings interact.

For a service unit, use the appropriate class and package metadata. The unit file, executable, runtime user and writable directories form one runtime contract. A unit that is enabled but references a missing user or read-only path still fails at startup.

## Review one customization end to end

For a device-tree change, inspect the source include, compiled DTB, selected boot artifact and live device. For a kernel option, inspect the fragment, final configuration, deployed kernel and driver availability. For an application file, inspect staged content, package ownership, image manifest and runtime path.

This method also prevents overbroad fixes. If a driver never binds because the compatible string is wrong, adding more kernel packages does not repair the binding. If a file is absent because its package is not selected, changing the source installation path may only create another defect.

**Source trail:** local `project-spec/meta-user/recipes-bsp/device-tree/device-tree.bbappend`, its `files/system-user.dtsi`, and the selected component recipe/class definitions. Full rebuild and board checks remain open; the metadata relationships were inspected directly.

## References

- `xilinx-zcu106-2024.1:project-spec/meta-user/`
- AMD UG1144 (2024.1), user layers, kernel and device-tree customization
- Yocto 4.1.4, append files and configuration fragments

---

<sub>← [Output Files in images/linux](06-images-linux-output-files.md) · [Chapter index](README.md) · [Adding Applications and Libraries](08-adding-applications-and-libraries.md) →</sub>
