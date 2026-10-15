# Project Structure: A Real 2024.1 Project Dissected

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-05](../ROADMAP.md#wp-05). The outline below is the agreed scope and will be replaced by the full text.

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Planned content

- Top level: `.petalinux/`, `project-spec/`, `components/`, `build/`, `images/`, `pre-built/`, `hardware/`
- `project-spec/configs/`: `config`, `rootfs_config`, Kconfig fragments, `gen-machineconf.log`, `flash_parts.txt`
- `project-spec/hw-description/`: XSA, bitstream, `psu_init*`
- `project-spec/meta-user/`: device-tree, U-Boot, kernel and firmware recipes
- `components/yocto/` (layers, workspace, SDK sysroots) and `components/plnx_workspace/`
- What to put in Git: the `.gitignore` of a real BSP

---

<sub>← [Installation and Host Setup](02-installation-and-host-setup.md) · [Chapter index](README.md) · [Commands and Workflow](04-commands-and-workflow.md) →</sub>
