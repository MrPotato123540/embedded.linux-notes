# Rootfs Configuration and Packagegroups

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Package selection

The rootfs menu records image choices. `user-rootfsconfig` can expose custom selections, but the selected package still needs a visible recipe and valid dependencies. Confirm the final manifest rather than relying on a checked menu item.

The locally inspected 2024.1 packagegroups include:

| Group | Direct content observed |
| --- | --- |
| `packagegroup-petalinux-networking-debug` | tcpdump and Wireshark |
| `packagegroup-petalinux-v4lutils` | v4l-utils and yavta |
| `packagegroup-petalinux-audio` | ALSA libraries/tools, SoX; conditional PulseAudio packages |
| `packagegroup-petalinux-openamp` | libmetal, OpenAMP and demo groups, with machine-dependent firmware additions |

Dependencies can expand this list. Machine and distribution overrides can change it further.

## Image size and production

Measure installed sizes and identify why a package is pulled in before removing it. Split development tools from product runtime requirements. A smaller image is not automatically safer if it removes recovery or diagnostics needed in the field.

Check that required licenses, firmware and configuration files remain after trimming. Reboot from the rebuilt image to avoid testing a target that still contains manually installed packages.

## References

- Inspected `meta-petalinux@rel-v2024.1:recipes-core/packagegroups/`
- Reference `rootfs.manifest`

---

<sub>← [Root Filesystem Boot Options in PetaLinux](04-rootfs-boot-options.md) · [Chapter index](README.md) · [Init Systems: SysVinit, systemd and BusyBox init](06-init-systems.md) →</sub>
