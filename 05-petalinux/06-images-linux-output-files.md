# Output Files in images/linux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Artifact map

The reference BSP includes the following files. Availability in a new build depends on configuration.

| Artifact | Purpose or producer |
| --- | --- |
| `BOOT.BIN`, `bootgen.bif` | Packaged boot partitions and their Bootgen description |
| `zynqmp_fsbl.elf` | First Stage Boot Loader |
| `pmufw.elf`, `pmu-conf.bin` | PMU firmware and platform-management configuration data |
| `bl31.elf`, `bl31.bin` | TF-A runtime firmware, ELF and raw forms |
| `u-boot.elf`, `u-boot.bin`, `u-boot-dtb.*` | U-Boot executable variants |
| `Image`, `Image.gz`, `vmlinux` | Arm64 kernel, compressed kernel and ELF debugging image |
| `system.dtb` | Compiled device tree |
| `system.bit` | Programmable-logic configuration |
| `image.ub` | FIT container; inspect which components it includes |
| `boot.scr` | U-Boot script with an image header |
| `rootfs.*`, `ramdisk.*` | Filesystem images or archives in selected formats |
| `*.manifest` | Installed package inventory |
| `petalinux-sdimage.wic.xz` | Compressed partitioned disk image |
| `dtbos/`, `openamp.dtb` | Overlays and an alternative device-tree configuration |
| `pxelinux.cfg/` | Network-boot configuration |
| `zynqmp-qemu-*.dtb`, `pmu_rom_qemu_sha3.elf` | QEMU-specific machine and boot support |

## Choosing the correct file

A raw kernel is not an ELF debugging image. A filesystem archive is not necessarily a disk image. A `.wic` image includes a partition layout; `rootfs.ext4` represents a filesystem. Writing one where the other is expected changes the interpretation of every offset.

The kernel recipe produces kernel outputs; device-tree recipes produce DTBs; firmware recipes produce their ELF files; image recipes assemble root filesystems. Boot packaging combines selected outputs. Check recipe deploy directories and package logs when provenance is unclear.

For SD boot, the boot partition and root partition serve different purposes. QSPI requires explicit offsets and erase geometry. JTAG and QEMU load files through their own launch flow. The filename alone does not define where a file belongs.

## Distinguish a payload from its container

A raw executable image, an ELF file and a container can hold related code but serve different consumers. ELF includes program headers and may include symbols needed by linkers and debuggers. A raw `Image` is arranged for the Arm64 kernel boot protocol. A FIT container describes selected payloads and configurations for U-Boot. `BOOT.BIN` uses the ZynqMP boot-image format for the early boot chain.

Do not rename one format to obtain another. A loader decides how to interpret bytes from the format and the command used. Passing an ELF where a raw image is expected can make the loader treat ELF headers as executable code. Passing a filesystem image where a whole-disk image is expected shifts the meaning of storage offsets.

The same distinction applies to compression. A compressed file needs a consumer that understands its compression format and has space for the expanded content. File extension and filename are hints; inspect the actual header and the selected boot command.

## The real BSP FIT contains three payloads

The saved `dumpimage -l` inspection of the reference `image.ub` reports this configuration:

| FIT node | Type | Stored data size | Relevant metadata |
| --- | --- | ---: | --- |
| `kernel-1` | AArch64 Linux kernel | 10,439,067 bytes | gzip; load and entry `0x00200000` |
| `fdt-system-top.dtb` | Flattened device tree | 54,985 bytes | Uncompressed |
| `ramdisk-1` | Initramfs payload | 5,464,979 bytes | FIT compression property reports uncompressed |

The default configuration is `conf-system-top.dtb` and references all three nodes. The ramdisk description identifies `petalinux-initramfs-image`. This matters when comparing it with the much larger main root filesystem: they are different image products.

The kernel's stored compressed size is not its full memory requirement after decompression. The FIT staging area, extracted payloads, kernel destination, DTB and initramfs must remain compatible with the bootloader's memory use. A load address that worked for an older kernel can become unsafe after growth.

The FIT lists SHA-256 hashes for the payloads. A hash detects a mismatch against the stored expected value. A hash alone does not establish who authorized that value. Authentication requires an appropriate signature and trusted verification key, addressed in the secure-boot chapters.

## `BOOT.BIN` is a different packaging layer

The Bootgen 2024.1 inspection of the reference boot image reports an image header for FSBL, TF-A, the DTB and U-Boot. The PMU firmware is described through dedicated boot-header handling in this layout. Therefore, counting input files in a BIF is not the same as counting image headers.

The reference boot package and the FIT can both contain device-tree material. That does not prove both copies are identical or both are used at the same stage. U-Boot can use a control tree for its own drivers and later pass an OS tree to Linux. Inspect the boot flow before replacing one copy and expecting all stages to change.

A bitstream file next to `BOOT.BIN` is not proof that the boot image contains it. Inspect the BIF and packaged headers. A Linux FPGA-manager flow may intentionally load PL content later. The artifact list must be interpreted together with the chosen loading policy.

## Filesystem image, archive and disk image

A root filesystem archive records files and metadata for extraction or an initramfs path. An ext4 image represents a filesystem with its own superblock and allocation structures. A WIC image can contain a partition table and several filesystem regions. These objects require different deployment operations.

For a partitioned SD card, the boot partition may hold firmware and bootloader-readable files while a separate partition holds the Linux root filesystem. A raw `rootfs.ext4` image belongs to a filesystem region; it does not describe the complete card partition layout. Always verify the intended destination before writing any storage image.

An archive also needs suitable extraction semantics. Ownership, permissions, links and device nodes can matter. Copying only visible regular files into a destination directory is not equivalent to reproducing a root filesystem.

## Identify the artifact that actually ran

Record checksums at publication and at deployment. Preserve the corresponding kernel configuration, module set, DTB and package manifest. For debugging, keep `vmlinux` and application symbols associated with the exact runtime binaries.

At boot, capture the loader's selected filenames or FIT configuration and the kernel version string. For a device-tree issue, inspect the tree passed to Linux. For a package issue, inspect the installed root filesystem. An output directory can contain old files that were not regenerated by the latest component build.

A reliable release manifest answers five questions for each artifact: which input revision produced it, which tool produced it, which format it uses, which consumer loads it, and where it is deployed. This is more useful than a directory listing alone.

**Evidence:** saved `fit-image-list.txt` and `bootgen-2024.1-read.txt` from the actual BSP. The capture files are kept in the local reference setup outside this guide repository. The values above are transcribed observations, not predicted output from a new build.

## References

- Inspected `xilinx-zcu106-2024.1:pre-built/linux/images/`
- AMD UG1144 (2024.1), generated images and packaging

---

<sub>← [The Configuration System](05-configuration-system.md) · [Chapter index](README.md) · [Customizing Through meta-user](07-meta-user-customization.md) →</sub>
