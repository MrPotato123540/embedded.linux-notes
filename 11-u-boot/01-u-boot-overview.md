# U-Boot Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot


## U-Boot prepares an operating-system handoff

U-Boot loads the operating-system artifacts, selects a boot policy, prepares the hardware description and enters the kernel under its boot protocol. In the common ZynqMP A53 flow, FSBL and Trusted Firmware-A have already run before U-Boot receives control.

This position matters. U-Boot can access DDR because earlier software prepared it. It can request platform services from resident firmware. It does not replace the FSBL's hardware initialization, and it does not replace the Linux drivers that will later own devices.

The saved reference console reports U-Boot 2024.01 and `EL Level: EL2`. The local 2024.1 recipe selects AMD's `xlnx_rebase_v2024.01` branch at commit `fbed1010e50d75e7d25acc1c2d09e1c34cb7e882`. Keep the source revision, build configuration and deployed ELF together; the version banner alone does not identify local patches.

## Initialization has an important relocation boundary

The generic early flow in `common/board_f.c` runs `init_sequence_f`. It establishes the state needed before relocation and reserves memory for U-Boot, allocation areas, board/global data, device-tree storage and stacks as enabled by the configuration.

Relocation moves the running image to its selected runtime address and adjusts references. Later initialization continues through `common/board_r.c`, then reaches the command and automatic-boot loop. This is why an address printed from the linked ELF need not equal the address of a function in a running, relocated U-Boot.

For debugging after relocation, account for `gd->reloc_off` and the actual relocation address. A breakpoint placed using only the link address can miss the running code. Likewise, a memory load near the top of DDR can overwrite relocated U-Boot or its heap even when it does not overlap the kernel's planned address.

## Two device-tree roles can coexist

U-Boot can use a control device tree for its own driver model. It also prepares the device tree that Linux will receive. These trees can be related, but they are not automatically the same object with the same contents and lifetime.

Changing the Linux DTB does not necessarily change which driver U-Boot uses for storage or Ethernet. Changing U-Boot's control tree does not automatically update the DTB passed to Linux. When a peripheral works in one stage but fails in the other, identify which tree and driver each stage uses.

The driver model binds devices from available descriptions and probes them when required by the flow. A device listed in the model may not yet have completed probe. A successful probe in U-Boot also does not establish Linux's configuration or driver support.

## Boot policy is data plus control flow

The environment holds values such as `bootcmd`, `bootargs` and load addresses. A boot command can invoke other variables through `run`, load a script, or scan boot targets. The final behavior is the complete executed path, not only the first value of `bootcmd`.

A storage operation can succeed while selecting the wrong file. A network setup can succeed while file transfer fails. A script can find a kernel but pass an old device tree. Record the selected source, filenames, sizes and configuration so that “booted successfully” has an exact meaning.

The local `u-boot-xlnx-scr.bb` generates `boot.scr` from a source template. It has separate defaults for kernel, device tree, ramdisk and FIT load addresses. These are recipe defaults; board configuration and environment values can change the actual path.

## One real network session shows the boundaries

The saved `cap-wp01-uboot.txt` records a DHCP exchange that receives address `10.0.2.16`. The automatic TFTP attempt then fails because the default filename `0A000210.img` is not found. This is a useful example: DHCP success does not imply file-transfer success.

The same capture later sets the server address and explicitly loads `Image` at `0x200000`, transferring 24,269,312 bytes. It loads `system.dtb` at `0x100000`, transferring 54,985 bytes. A ping to the server succeeds afterward.

Those observations establish the QEMU session's network and transfers. They do not measure physical Ethernet performance, validate every DTB property or prove the transferred kernel was entered. Each next boundary needs its own evidence.

## Loading and booting are different operations

A load command puts bytes into memory. A boot command interprets those bytes according to an image format, prepares supporting data and eventually transfers control. For AArch64, `booti` handles the raw Image flow; `bootm` handles supported image containers such as FIT.

The distinction matters when a file has been renamed. A file called `Image` can still contain the wrong format. An `image.ub` is normally a FIT container in this BSP, not a raw kernel with a special extension. Inspect metadata rather than choosing a command from the filename alone.

A successful transfer also does not guarantee safe placement. Include the uncompressed kernel footprint, DTB growth, initramfs, resident firmware and U-Boot's own allocations in the memory plan.

## The final transfer changes device ownership

Before entering Linux, U-Boot must satisfy the AArch64 boot requirements. It prepares the final DTB and initramfs information, handles the required cache/MMU state and transfers with the DTB address in `x0`. DMA-capable devices must not continue corrupting memory after Linux starts.

Linux then initializes its own drivers and memory model. U-Boot's network or storage success is a useful hardware clue, but not a guarantee that Linux's pinctrl, clocks, interrupts or driver configuration are correct.

> [!NOTE]
> **Not run on the reference setup:** a custom U-Boot build, physical relocation debugging and physical storage/network qualification. This section combines the saved QEMU transcript with pinned source and local recipe inspection.

## References

- [2024.1 early U-Boot initialization](https://github.com/Xilinx/u-boot-xlnx/blob/xilinx-v2024.1/common/board_f.c), adjacent `board_r.c`, and `board/xilinx/zynqmp/zynqmp.c`.
- Local BSP: `meta-xilinx-core/recipes-bsp/u-boot/{u-boot-xlnx-2024.1.inc,u-boot-xlnx-scr.bb}`.
- Saved `cap-wp01-uboot.txt` and `boot-manual-1.log`.

---

<sub>[Chapter index](README.md) · [Essential U-Boot Commands](02-essential-commands.md) →</sub>
