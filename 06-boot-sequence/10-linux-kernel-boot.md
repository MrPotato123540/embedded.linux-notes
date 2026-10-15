# Linux Kernel Boot

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-06](../ROADMAP.md#wp-06). The outline below is the agreed scope and will be replaced by the full text.

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Planned content

- arm64 boot protocol requirements: MMU off, `x0` = DTB address, entry at EL2
- Early boot: `head.S`, `start_kernel`, `earlycon`
- Device tree unflattening, initcalls, driver probing, deferred probe
- Mounting the root filesystem (initramfs, initrd, block device, NFS) and executing init

---

<sub>← [U-Boot Stage](09-u-boot-stage.md) · [Chapter index](README.md) · [User-Space Startup](11-user-space-startup.md) →</sub>
