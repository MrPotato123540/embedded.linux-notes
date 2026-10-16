# How U-Boot Boots the Linux Kernel

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot


## The handoff is a processor and memory contract

Starting Linux is more than branching to a file's first byte. The AArch64 boot protocol defines where the kernel may reside, how the device tree is passed, which CPU state is required and what earlier software must stop doing.

The Linux 6.6 protocol expects a prepared RAM layout, a valid device tree, decompression when needed and a correct kernel entry. The device tree's physical address is passed in `x0`; the remaining boot argument registers have their defined reserved state. The kernel enters in a supported Non-secure exception level with the required interrupt and MMU conditions.

For this guide, the implementation evidence is the pinned AMD `cmd/booti.c`, `arch/arm/lib/bootm.c` and Linux `Documentation/arch/arm64/booting.rst`. The protocol is the contract; those source files show how this release implements its side.

## Raw Image and FIT reach shared boot preparation

`booti` handles the AArch64 Image path. Its startup code determines the input address, considers supported compression, and uses the Image header to prepare placement. A compressed raw Image needs suitable decompression storage and enabled algorithm support.

`bootm` handles supported containers such as FIT. It selects image components and prepares a `bootm_headers` description of the kernel and supporting objects. Both paths eventually use architecture-specific Linux preparation and transfer logic.

The filename is not the format check. A gzip-compressed file renamed `Image`, an ELF renamed `image.ub`, or a FIT passed directly to the raw Image path can fail before the kernel executes.

## Follow the final architecture code

In `arch/arm/lib/bootm.c`, `boot_prep_linux()` prepares Linux's data, including the device-tree path through `image_setup_linux()`. `boot_jump_linux()` then uses the selected entry and performs the architecture transition.

The final sequence includes cleanup before entering the kernel. This boundary matters for caches and devices that can access memory. A network controller left doing DMA can corrupt the new kernel after the jump, producing a failure that appears to be inside Linux.

The exact transition also depends on the current exception level and configured architecture support. Use the actual build and boot log rather than assuming every U-Boot starts in the same state. The reference reports EL2, which is consistent with the intended TF-A handoff.

## The DTB can change before Linux sees it

U-Boot can update the working device tree with memory information, `/chosen` properties, command-line arguments and initramfs bounds. It may also apply board-specific fixups or overlays. Therefore, the DTB file on the boot medium is not always byte-identical to the tree Linux receives.

A source DTS with the correct `bootargs` does not prove that those arguments remain unchanged. Conversely, a value missing from the original file can be added during boot preparation. Inspect the final running tree or final handoff buffer when debugging a difference.

The control device tree used by U-Boot's own drivers is a separate role. Make sure an inspection command points to the intended working tree before interpreting its contents as Linux's future hardware description.

## A worked placement review from the reference artifacts

The recorded raw `Image` transfer starts at `0x200000` and has size `0x1725200`, ending at `0x1925200`. The recorded DTB starts at `0x100000` and has size `0xD6C9`, ending at `0x10D6C9`.

The two input files do not overlap. The kernel's effective memory requirement must still come from its Image header, and supporting objects must remain outside that required region. For the FIT path, the compressed kernel's stored size is smaller and its output is placed separately.

The AArch64 Image header contains `text_offset`, `image_size` and flags. The placement rule uses a 2 MiB-aligned base plus `text_offset`; it is not a universal rule that every kernel must execute at one hard-coded address. Respect the header for the actual image.

The DTB also has alignment and size requirements in the boot protocol. The 54,985-byte reference object is within the protocol's 2 MiB size limit, but size alone does not validate its contents or final placement attributes.

## Initramfs is a separate input with a lifetime

When an external initramfs is supplied, U-Boot records its start and end for Linux. The kernel must be able to read the complete archive before the memory is reused. An incorrect end address can truncate the archive or include unrelated bytes.

A FIT can provide the ramdisk through its selected configuration. A raw boot command can provide it separately. The root filesystem later mounted by userspace is another stage; a valid initramfs can still fail to locate or mount the intended persistent root.

If Linux reports an unpacking error, inspect the actual ramdisk bytes, length and format. If unpacking succeeds but the root device is missing, inspect storage drivers, device-tree dependencies and root-selection arguments rather than the kernel entry mechanism.

## Separate “Starting kernel” from kernel progress

U-Boot's final message shows that it is about to transfer control. It is not a kernel acknowledgement. A silence immediately afterward can come from wrong placement, invalid entry state, a bad DTB, wrong console arguments or an early kernel fault.

Use early-console support only when it matches the real UART and access method. A wrong console can hide a running kernel. If early output appears and later stops, locate the transition to the normal console or the last kernel init stage rather than assuming the original jump failed.

For a later secondary-CPU failure, inspect PSCI and firmware cooperation. That path can fail even when the primary CPU entered Linux correctly. Keep the first-CPU handoff and later CPU bring-up as separate tests.

> [!NOTE]
> **Not run on the reference setup:** a modified boot command, deliberately invalid entry state or DMA-handoff fault injection. The source paths and saved artifact sizes were checked; no new target boot is claimed here.

## References

- [2024.1 U-Boot ARM Linux handoff](https://github.com/Xilinx/u-boot-xlnx/blob/xilinx-v2024.1/arch/arm/lib/bootm.c) and `cmd/booti.c`.
- `linux-xlnx@xilinx-v2024.1:Documentation/arch/arm64/booting.rst`.
- [Linux 6.6 AArch64 boot protocol](https://docs.kernel.org/6.6/arch/arm64/booting.html).
- Saved `cap-wp01-uboot.txt` and `fit-image-list.txt`.

---

<sub>← [FIT Images and image.ub](04-fit-images.md) · [Chapter index](README.md) · [Customizing U-Boot](06-u-boot-customization.md) →</sub>
