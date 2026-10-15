# What Is PetaLinux?

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Concepts

PetaLinux combines an AMD-supported tool set with Yocto layers, hardware import and project configuration. It helps turn an exported hardware design into boot firmware, a kernel, a device tree and a root filesystem.

The wrapper does not replace BitBake. A PetaLinux build still follows recipes, task dependencies, package rules and shared-state signatures. When a build fails inside a recipe, the BitBake log is usually more useful than the final wrapper error.

## Tools and responsibilities

| Tool | Main job |
| --- | --- |
| `petalinux-create` | Create a project, application or module |
| `petalinux-config` | Import hardware and configure the project or components |
| `petalinux-build` | Build images, components or SDKs |
| `petalinux-package` | Package boot files, disk images and BSPs |
| `petalinux-boot` | Start supported JTAG or QEMU boot flows |
| `petalinux-devtool` | Connect source development with recipes |
| `petalinux-upgrade`, `petalinux-util` | Release-specific maintenance and utility operations |

The **Xilinx Support Archive (XSA)** contains exported hardware information. PetaLinux uses it to generate hardware-related inputs. It cannot infer all external board wiring or product policy from that archive.

## Choosing a flow

Use PetaLinux when its supported project flow fits the team. Use plain Yocto when you need direct control over layers and automated build policy. Both require correct hardware metadata. Newer AMD flows may use a System Device Tree; do not mix their instructions into a 2024.1 project without checking release support.

## References

- AMD [UG1144, PetaLinux 2024.1](https://docs.amd.com/r/2024.1-English/ug1144-petalinux-tools-reference-guide)
- Locally executed 2024.1 tool help: `petalinux-create`, `petalinux-config`, `petalinux-build`, `petalinux-package`, `petalinux-boot`

---

<sub>[Chapter index](README.md) · [Installation and Host Setup](02-installation-and-host-setup.md) →</sub>
