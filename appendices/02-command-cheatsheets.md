# Command Cheat Sheets

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[Appendices](README.md)** · Appendices

## Use the correct environment

Commands below are an interface index. Availability depends on the image and configuration. Only commands identified as executed in their chapter are recorded tests; a tool name here is not evidence of a completed hardware operation.

| Environment | Interface | Purpose |
| --- | --- | --- |
| PetaLinux 2024.1 | `petalinux-create project/apps/modules` | Create project components |
| PetaLinux 2024.1 | `petalinux-config -c` | Configure a component |
| PetaLinux 2024.1 | `petalinux-build -c`, `-x`, `--sdk` | Build component, task or SDK |
| PetaLinux 2024.1 | `petalinux-package boot` | Boot packaging; inspect subcommand help |
| BitBake | `-e`, `-g`, `-c` | Environment, dependency graph, selected task |
| devtool | `modify`, `build`, `finish` | Source development and recipe integration |
| U-Boot | `help`, `version`, `printenv`, `bdinfo` | Inspect capabilities and state |
| U-Boot | `tftpboot`, `fatload`, `ext4load` | Load selected files |
| U-Boot | `booti`, `bootm` | Enter a supported kernel/image format |
| Linux | `uname`, `dmesg`, `ip`, `ss`, `lsmod` | Inspect system, network and modules |
| XSDB | `targets`, `mrd` | Select/inspect a debug target |
| Bootgen | `-arch zynqmp -read` | Decode a boot image |
| FIT tools | `dumpimage -l` | List FIT content |
| Device tree | `dtc -I dtb -O dts` | Decompile a DTB |

## Preserve evidence

Before changing hardware state, save logs, versions and artifact hashes. Verify the selected device and address range. Flash writes, memory tests, reset operations and security provisioning are deliberately not reduced to blind copy-paste shortcuts.

For executed examples, see [boot-image inspection](../06-boot-sequence/05-boot-image-format.md), [FIT inspection](../11-u-boot/04-fit-images.md), [SSH](../01-linux-fundamentals/07-ssh.md) and [certificate validation](../25-security-fundamentals-and-cryptography/03-pki-and-certificates.md).

---

<sub>← [Glossary](01-glossary.md) · [Chapter index](README.md) · [Register Quick Reference](03-register-quick-reference.md) →</sub>
