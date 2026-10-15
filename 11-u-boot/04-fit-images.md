# FIT Images and image.ub

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot

## FIT structure

A **Flattened Image Tree (FIT)** contains image nodes and configuration nodes. Image nodes describe payloads such as a kernel, device tree or ramdisk. A configuration chooses which payloads boot together. Hashes detect changes; signatures can authenticate content when verification is correctly enforced.

## Reference inspection

The local `dumpimage -l` inspection of `image.ub` reports:

| Node | Content |
| --- | --- |
| `kernel-1` | AArch64 gzip kernel, 10,439,067 bytes; load/entry `0x00200000` |
| `fdt-system-top.dtb` | Device tree, 54,985 bytes |
| `ramdisk-1` | `petalinux-initramfs-image`, 5,464,979 bytes |
| `conf-system-top.dtb` | Default configuration selecting all three |

Each listed payload has a SHA-256 hash. This listing alone does not demonstrate enforced signature verification.

An `.its` source describes the container; `mkimage` builds it. Keep the source, payload hashes and signing policy with the release. Do not infer FIT contents from the name `image.ub`.

## References

- Executed inspection saved as `reference-setup/captures/fit-image-list.txt`
- U-Boot v2024.01 [FIT documentation](https://docs.u-boot.org/en/v2024.01/usage/fit/index.html)

---

<sub>← [Environment, boot.scr and uEnv.txt](03-environment-and-boot-scripts.md) · [Chapter index](README.md) · [How U-Boot Boots the Linux Kernel](05-how-u-boot-boots-linux.md) →</sub>
