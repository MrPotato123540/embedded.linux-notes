# Configuring and Building the Kernel

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers

## Configuration flow

Kconfig expresses feature choices and dependencies. A defconfig selects a baseline; configuration fragments add product choices. The final `.config` is the effective result. A requested symbol may be disabled when its dependencies are not satisfied.

PetaLinux exposes kernel configuration through `petalinux-config -c kernel` and component builds through `petalinux-build -c kernel`. These interfaces were checked in local 2024.1 help. In direct Yocto, the selected `virtual/kernel` provider supplies the recipe.

## Source and configuration changes

Keep source patches and configuration fragments in a maintained layer. Check the patch task and final `.config` after the build. `savedefconfig` records differences from defaults, so its output is not a complete substitute for archiving the full configuration.

An out-of-Yocto build needs the correct cross-toolchain, architecture, source revision and output directory. It also needs a matching module installation and device-tree deployment plan. Compiling an Image alone does not update the root filesystem's modules.

> [!NOTE]
> **Not run on the reference setup:** a fresh kernel build in this continuation. The recipe and tool interfaces were inspected.

## References

- `linux-xlnx@xilinx-v2024.1:Documentation/kbuild/`
- AMD UG1144 (2024.1), kernel configuration

---

<sub>← [Kernel Image Formats](03-kernel-image-formats.md) · [Chapter index](README.md) · [Kernel Debugging](05-kernel-debugging.md) →</sub>
