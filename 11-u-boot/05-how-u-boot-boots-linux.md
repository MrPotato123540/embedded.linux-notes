# How U-Boot Boots the Linux Kernel

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-11](../ROADMAP.md#wp-11). The outline below is the agreed scope and will be replaced by the full text.

**[11 · U-Boot](README.md)** · Part IV: Boot

## Planned content

- `booti` (`Image`/`Image.gz`) vs. `bootm` (FIT/legacy uImage)
- Decompression, relocation and `kernel_comp_addr_r`
- Device tree fixups: `/chosen`, `bootargs`, memory, reserved memory
- Initrd/initramfs handling and the final jump

---

<sub>← [FIT Images and image.ub](04-fit-images.md) · [Chapter index](README.md) · [Customizing U-Boot](06-u-boot-customization.md) →</sub>
