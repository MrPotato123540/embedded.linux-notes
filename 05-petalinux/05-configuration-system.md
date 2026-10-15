# The Configuration System

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Configuration layers

PetaLinux configuration combines project choices, generated hardware settings and Yocto policy. The top-level menu covers hardware, device-tree generation, bootloader settings, image packaging, firmware and build-system options.

The project configuration is an input to generation. Files such as `build/conf/plnxtool.conf` carry the translated settings into BitBake. `project-spec/meta-user/conf/petalinuxbsp.conf` supplies maintained user overrides. Editing only a generated file risks losing the change during the next configuration run.

## Root filesystem selection

`rootfs_config` records package and feature selections. `user-rootfsconfig` can expose additional choices in the menu. A recipe must exist and be visible to BitBake before its package can be included successfully. Use the final image manifest to confirm the result.

## Hardware and boot policy

The machine name selects the platform metadata. Hardware import and machine-generation tools can create settings from the XSA. Check the generated value rather than assuming that `YOCTO_MACHINE_NAME`, an XSA filename and a layer machine identifier all match.

Boot-device choices affect more than the kernel command line. Flash partitions, bootloader search behavior and image packaging must agree. For example, moving the root filesystem from RAM to eMMC requires a root-device description and the necessary storage driver early enough in boot.

## Review method

Compare the maintained configuration before and after using a menu. Then inspect the generated BitBake settings and image output. A menu default may change after importing a different BSP. Keep the configuration diff with the reason for the change.

## References

- Inspected `xilinx-zcu106-2024.1:project-spec/configs/`, `build/conf/plnxtool.conf`
- Inspected `project-spec/meta-user/conf/petalinuxbsp.conf`
- AMD UG1144 (2024.1), project and rootfs configuration

---

<sub>← [Commands and Workflow](04-commands-and-workflow.md) · [Chapter index](README.md) · [Output Files in images/linux](06-images-linux-output-files.md) →</sub>
