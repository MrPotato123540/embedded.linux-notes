# Kernel Image Formats

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers


## The kernel has several artifacts for different consumers

A kernel build produces more than one useful file. `vmlinux` is the linked ELF used for symbols and debugging. `Image` is the AArch64 boot image. A compressed `Image` needs a boot path that decompresses it. A FIT container such as the reference `image.ub` packages selected payloads and their metadata.

A filename extension does not define the format. Renaming an ELF to `Image` does not produce an AArch64 boot image, and renaming a gzip stream to `image.ub` does not create a FIT. Match the consumer to the bytes and metadata.

Keep `vmlinux` from the exact deployed build. A bootable `Image` usually lacks the rich symbol/debug information needed to decode a crash accurately. A similar source version can map the same address to a different function after configuration or compiler changes.

## The AArch64 Image header is an input to placement

The pinned `Documentation/arch/arm64/booting.rst` describes a 64-byte Image header. It includes `text_offset`, `image_size`, flags and the magic value `0x644D5241`. The relevant multibyte fields use the specified little-endian encoding for this format.

The effective `image_size` describes the memory the kernel needs from its start, not merely the file's initialized bytes. Placement uses a 2 MiB-aligned base plus `text_offset`, with additional constraints described by the flags and protocol.

This is why a memory plan based only on the transferred file size can be wrong. Zero-initialized and other runtime needs still occupy memory after the bootloader finishes copying bytes.

## A header inspection that was executed

A host Python inspection read the reference `pre-built/linux/images/Image`. It decoded the three 64-bit fields at byte offset 8 and the 32-bit magic at byte offset 56. The measured values were:

| Field | Observed value |
| --- | --- |
| File size | 24,269,312 bytes (`0x1725200`) |
| `text_offset` | `0x0` |
| `image_size` | `0x17A0000` |
| Flags | `0xA` |
| Magic | `0x644D5241` |

The flags encode the relevant page-size and placement information according to the boot protocol. For this image, a zero text offset makes the recorded `0x200000` load address consistent with the aligned-base rule.

The required end-exclusive runtime address is `0x200000 + 0x17A0000 = 0x19A0000`. The file-transfer end is only `0x1925200`. The difference, `0x7AE00` bytes, must not be treated as free space for a DTB or another payload.

This is an artifact-specific calculation. Recheck the header after changing the configuration or kernel. Do not turn the measured size into a fixed product constant.

## Compression adds a source and destination lifetime

The reference FIT stores a gzip-compressed kernel of 10,439,067 bytes and requests load/entry at `0x00200000`. U-Boot must preserve the compressed source until decompression consumes it and provide enough destination memory for the resulting image and required runtime area.

A small compressed file can expand into a much larger kernel. A layout that fits the FIT container and ramdisk can still fail if the output overlaps the source or another live object. Check the actual decompression path and its temporary-storage requirements.

AArch64 Linux does not provide the same built-in raw-image decompressor model as some other architecture boot formats. The selected bootloader path must handle compressed input appropriately. For raw `booti`, compression support and related buffer configuration depend on the U-Boot build.

## FIT metadata selects a complete boot combination

The reference `image.ub` has kernel, FDT and ramdisk nodes and default configuration `conf-system-top.dtb`. Its configuration chooses which objects belong together. The container's kernel metadata does not replace the kernel's own header requirements.

Hash and signature nodes also have different meanings. A hash detects a byte mismatch against its recorded digest. Signature verification under a protected trust anchor can authenticate the selected content and configuration under the configured policy.

The ramdisk's FIT compression field describes U-Boot handling of that payload. The payload can still contain a compressed initramfs archive for Linux. Do not infer archive format from the container field alone.

## Modules and device trees remain separate deployment inputs

Replacing `Image` does not update `/lib/modules` in the root filesystem. A new kernel release string or changed exported interfaces can make old modules unusable. Conversely, replacing modules without their matching kernel can leave the system unable to load a critical driver.

A DTB can be deployed separately or embedded in a FIT. Confirm which one the boot path uses. A new kernel may require a corrected binding, while an old recovery kernel may still need compatible input.

A release manifest should therefore identify kernel image, symbol ELF, configuration, modules, DTB/FIT selection and root filesystem together. The boot artifact is one member of that set.

## Diagnose format, integrity and execution separately

If the bootloader rejects the header, inspect format and truncation. If decompression fails, inspect bytes, algorithm support and destination capacity. If validation succeeds but entry fails, inspect placement, processor state and DTB.

If the kernel runs but a module fails to load, move to build compatibility and symbol/version evidence. Do not keep repackaging `BOOT.BIN` when the failing object is a root-filesystem module.

## References

- [Pinned AArch64 boot protocol](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/arch/arm64/booting.rst).
- Reference `pre-built/linux/images/Image`, executed host header inspection.
- Saved `fit-image-list.txt` and `cap-wp01-uboot.txt`.
- `u-boot-xlnx@xilinx-v2024.1:cmd/booti.c` and `boot/image-fit.c`.

---

<sub>← [linux-xlnx and Kernel Versions](02-linux-xlnx-and-kernel-versions.md) · [Chapter index](README.md) · [Configuring and Building the Kernel](04-configuring-and-building.md) →</sub>
