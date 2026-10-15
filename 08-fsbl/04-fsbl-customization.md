# Customizing the FSBL

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-08](../ROADMAP.md#wp-08). The outline below is the agreed scope and will be replaced by the full text.

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot

## Planned content

- Hooks: before/after bitstream download, before handoff, before fallback
- Board-specific init (`xfsbl_board.c`): PHY and USB resets, I2C clock setup
- Adding custom code: GPIO toggles, early peripheral init, boot-time measurement
- Applying changes in PetaLinux via bbappend and patches

---

<sub>← [Building the FSBL](03-building-the-fsbl.md) · [Chapter index](README.md) · [FSBL Debugging](05-fsbl-debugging.md) →</sub>
