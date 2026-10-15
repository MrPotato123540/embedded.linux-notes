# Commands and Workflow

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Workflow

A complete build flow has five stages: create, import hardware, configure, build and package. Boot testing comes after packaging. Record the input hardware revision before starting.

The installed 2024.1 help uses **subcommands** for creation and packaging. For example, project creation is `petalinux-create project`; boot packaging is `petalinux-package boot`. Older guides often show `-t project` or `--boot`. Use the installed release help as the authority for accepted syntax.

| Operation | Relevant interface |
| --- | --- |
| Create from BSP | `project` subcommand with `--source` |
| Create for ZynqMP | `project` subcommand with `--template zynqMP` |
| Import hardware | `petalinux-config --get-hw-description` |
| Configure a component | `petalinux-config -c` |
| Build one component | `petalinux-build -c` |
| Select a BitBake task | `petalinux-build -x` |
| Build an SDK | `petalinux-build --sdk` |
| Build an extensible SDK | `petalinux-build --esdk` |

These interfaces were checked through local help. They are not a transcript of a newly completed image build.

## Iterating safely

After a recipe change, rebuild the component and then the image that includes its package. After a boot-firmware change, regenerate the boot image. A successful component build does not update an SD card automatically.

Packaging has separate boot, WIC disk-image, BSP and prebuilt purposes. QEMU and JTAG also have different boot inputs. Select the flow first, then check its subcommand help.

Cleaning removes evidence and may require large rebuilds. Preserve patches and logs before using clean tasks. Treat a release upgrade as a controlled migration: rebuild from pinned inputs and test hardware behavior again.

## References

- Executed help from `/opt/pkg/petalinux24.1`: create, config, build, package and boot tools
- AMD UG1144 (2024.1), command-line reference

---

<sub>← [Project Structure: A Real 2024.1 Project Dissected](03-project-structure.md) · [Chapter index](README.md) · [The Configuration System](05-configuration-system.md) →</sub>
