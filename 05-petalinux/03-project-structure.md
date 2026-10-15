# Project Structure: A Real 2024.1 Project Dissected

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Project map

| Directory | What it contains | Maintenance rule |
| --- | --- | --- |
| `project-spec/configs` | Project and rootfs selections | Keep intentional configuration changes |
| `project-spec/hw-description` | Imported hardware description and generated inputs | Tie to the hardware export revision |
| `project-spec/meta-user` | Product recipes, patches and configuration | Treat as maintained source |
| `components/yocto` | Build-system layers and SDK support | Record origins; avoid untracked edits |
| `components/plnx_workspace` | Generated component workspace | Do not use as the only copy of a change |
| `build` | Build configuration, tasks and temporary output | Regeneratable build state |
| `images/linux` | Newly built deployable files | Publish with checksums and a manifest |
| `pre-built/linux` | Prebuilt BSP artifacts | Not proof of a successful local build |
| `hardware` | BSP hardware assets | Preserve provenance |
| `.petalinux` | Tool metadata | Follow the project's ignore rules |

The hardware directory can contain the XSA, bitstream and processor initialization files. Their exact placement depends on how the project was created and imported. Inspect the project rather than assuming every generated file exists before configuration.

## What belongs in Git

The inspected BSP ignores `build/`, `images/linux/`, `pre-built/linux/`, `components/plnx_workspace` and `components/yocto`. It preserves `.petalinux/metadata` while ignoring most other `.petalinux` content.

Keep recipes, patches, configuration and a reference to the exact hardware export. Large release images can live in artifact storage. An ignored directory may still contain valuable uncommitted debugging work; move that work into a maintained recipe before cleaning it.

## Debugging

When a change vanishes, identify whether you edited source policy or generated output. Trace from `project-spec` through the generated build configuration to the final artifact. Never use file modification time alone as proof that the board booted the intended image.

## References

- Inspected `xilinx-zcu106-2024.1:.gitignore` and project directory tree
- AMD UG1144 (2024.1), project structure

---

<sub>← [Installation and Host Setup](02-installation-and-host-setup.md) · [Chapter index](README.md) · [Commands and Workflow](04-commands-and-workflow.md) →</sub>
