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

## References

- `xilinx-zcu106-2024.1:project-spec/meta-user/`
- AMD UG1144 (2024.1), user layers, kernel and device-tree customization
- Yocto 4.1.4, append files and configuration fragments

---

<sub>← [Output Files in images/linux](06-images-linux-output-files.md) · [Chapter index](README.md) · [Adding Applications and Libraries](08-adding-applications-and-libraries.md) →</sub>
