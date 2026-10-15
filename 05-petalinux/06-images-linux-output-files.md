# Output Files in images/linux

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-05](../ROADMAP.md#wp-05). The outline below is the agreed scope and will be replaced by the full text.

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Planned content

- Every file explained: `BOOT.BIN`, `bootgen.bif`, `boot.scr`, `image.ub`, `Image`, `Image.gz`, `vmlinux`, `system.dtb`, `system.bit`, `u-boot*.elf/bin`, `bl31.*`, `pmufw.elf`, `pmu-conf.bin`, `zynqmp_fsbl.elf`
- Root filesystem artifacts: `rootfs.*`, `ramdisk.*`, `*.manifest`, `petalinux-sdimage.wic.xz`
- Auxiliary outputs: `dtbos/`, `pxelinux.cfg/`, `openamp.dtb`, QEMU DTBs and `pmu_rom_qemu_sha3.elf`
- Which file goes where: SD BOOT/ROOT partitions, QSPI, JTAG, QEMU
- Which recipe produces each file

---

<sub>← [The Configuration System](05-configuration-system.md) · [Chapter index](README.md) · [Customizing Through meta-user](07-meta-user-customization.md) →</sub>
