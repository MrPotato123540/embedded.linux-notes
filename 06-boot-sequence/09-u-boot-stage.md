# U-Boot Stage

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## U-Boot's part of the chain

U-Boot initializes its runtime environment, relocates as required and binds devices through its driver model. It then chooses a boot target. Environment variables and scripts control which files are loaded and how Linux is started.

Do not assume that an SD card is selected simply because it contains `BOOT.BIN`. The initial boot source and U-Boot's later target search are separate choices. Inspect the actual environment and script for the image being tested.

## Linux inputs

U-Boot must provide a kernel, a valid device tree and, when required, an initramfs or initrd. `bootargs` carries the kernel command line. The root filesystem may instead be on a block device or network server.

`booti` starts an Arm64 Image, with supported compressed forms depending on configuration. `bootm` handles image formats such as FIT. Choose according to the loaded format, not the filename extension alone.

## Failure boundaries

A successful load only proves that bytes reached memory. Check size, addresses and image format before execution. If a script changes the device tree, inspect the final tree passed to Linux. If networking fails, separate DHCP address assignment from TFTP file retrieval; the saved reference session demonstrates that DHCP can succeed while the requested file is missing.

## References

- U-Boot v2024.01 [booti documentation](https://docs.u-boot.org/en/v2024.01/usage/cmd/booti.html)
- Saved `cap-wp01-uboot.txt`
- `u-boot-xlnx@xilinx-v2024.1:board/xilinx/zynqmp/`

---

<sub>← [TF-A BL31 Stage](08-tfa-bl31-stage.md) · [Chapter index](README.md) · [Linux Kernel Boot](10-linux-kernel-boot.md) →</sub>
