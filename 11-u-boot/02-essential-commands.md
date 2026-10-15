# Essential U-Boot Commands

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot

## Command groups

Command availability depends on the build. Start with `help` and inspect the actual environment before using a recipe from another board.

| Group | Useful commands | Main caution |
| --- | --- | --- |
| Information | `version`, `bdinfo`, `coninfo`, `dm tree`, `clk dump` | Some features are optional |
| Environment | `printenv`, `setenv`, `saveenv`, `run`, `env import/export` | Saving can change later boots |
| Memory | `md`, `mw`, `cp`, `cmp`, `crc32`, `mtest` | Writes and tests can destroy live data |
| Storage | `mmc`, `fatls`, `fatload`, `ext4load`, `sf`, `nand`, `usb`, `ums` | Device and partition selection matter |
| Network | `dhcp`, `tftpboot`, `ping`, `nfs` | Link, addressing and file service are separate |
| Boot | `booti`, `bootm`, `bootefi`, `boot`, `pxe` | Match the image format |
| Hardware | `i2c`, `gpio`, `fpga`, `zynqmp`, `fdt`, `reset` | Respect active devices and firmware ownership |

## Recorded example

The reference capture successfully loads a kernel through TFTP:

```console
ZynqMP> tftpboot 0x200000 Image
```

The recorded transfer size is 24,269,312 bytes. This verifies that specific QEMU session, not an arbitrary board network.

> [!WARNING]
> Memory tests, flash erase/write commands and USB mass-storage writes can overwrite running software or persistent data. Validate the exact range and recovery path first.

## References

- Saved `cap-wp01-uboot.txt`
- U-Boot v2024.01 command documentation and installed target help

---

<sub>← [U-Boot Overview](01-u-boot-overview.md) · [Chapter index](README.md) · [Environment, boot.scr and uEnv.txt](03-environment-and-boot-scripts.md) →</sub>
