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

## U-Boot turns a platform into an OS-loading environment

Early firmware has already established enough hardware state for U-Boot to execute. U-Boot then prepares its own runtime, devices, memory allocations and command environment. Its driver model and configuration determine which storage, network and console operations are available at this stage. Linux driver support does not automatically add the same support to U-Boot.

The reference log reports U-Boot 2024.01 and entry at EL2. It also reports its board model, memory view, devices and console. Read these as observations about this specific executable and control device tree. A Linux DTB loaded later can describe a different set of enabled devices.

Relocation is another boundary. U-Boot can move itself and reserve memory for its runtime use. A hard-coded load address that does not collide with the original ELF placement can still collide with relocated code, the stack, allocations or another loaded payload. Inspect the runtime memory layout before choosing large staging areas.

## The environment is executable boot policy

Environment variables can choose boot targets, filenames, load addresses and the kernel command line. Scripts can contain loops, fallbacks and conditional device selection. The presence of a file on one medium does not prove the script will read it.

The reference capture says `Loading Environment from nowhere... OK`. This indicates that the tested build uses its compiled environment arrangement rather than demonstrating successful recovery of a persistent environment from storage. Do not assume a change made interactively will survive reset on every configuration.

Before saving an environment on a physical product, understand where it is stored and how it interacts with update/recovery policy. A persistent old value can override an improved compiled default after a software update. Release testing must include both fresh and previously configured devices when that distinction exists.

## Loading, verification and execution are separate steps

A file-transfer command moves bytes into RAM. It does not by itself validate the kernel boot protocol or establish trust in the image. Record the actual transferred size and compare it with the expected artifact. Then inspect the container or raw image as appropriate.

For a FIT, a configuration selects related payloads. Loading the file does not tell you which configuration will be used. For a raw Arm64 kernel, the boot command needs a valid DTB and optional initramfs information. Mixing a newly built kernel with an old tree can produce a failure that looks like a driver regression.

Authentication is also separate from ordinary hash checking. A payload hash stored in the same untrusted container is useful for corruption detection, but it is not an authorization policy. Verified boot requires a trust anchor and the intended signature-enforcement behavior.

## Follow the reference handoff

The saved QEMU boot loads an initramfs from the legacy-image address `0x04000000` and starts with a DTB at `0x00100000`. U-Boot then reports moving the ramdisk and device tree to other RAM locations before printing `Starting kernel ...`.

This shows why the kernel's final input addresses can differ from the initial script addresses. The loader is allowed to prepare a suitable final layout. For a memory-overlap investigation, capture both the staging layout and the final handoff layout.

The DTB can also be modified before handoff. Boot arguments, memory descriptions and initramfs bounds may be supplied or updated by the loader. Inspect the final tree when the source DTS does not explain Linux's observed inputs.

## Diagnose at the failing interface

If DHCP succeeds but TFTP reports a missing file, the network address setup has progressed further than file retrieval. Check server path, filename, permissions and transfer behavior. Changing PHY configuration without evidence can move the problem backward.

If storage enumeration works but a filesystem cannot be read, inspect partition selection and supported filesystem format. If a file loads but `booti` rejects it, inspect image format and the selected command. If the command reaches `Starting kernel ...` but no Linux output follows, inspect the Arm64 entry contract and console path.

These boundaries make experiments smaller. Test a known readable file before investigating kernel execution. Test a known bootable kernel/tree pair before changing memory placement. Preserve the environment and full log so another engineer can reproduce the exact selection path.

**Evidence:** saved U-Boot sessions and `boot-prebuilt3.log`. The reference is an emulator development flow; persistent-environment updates and physical storage boot were not newly tested here.

## References

- U-Boot v2024.01 [booti documentation](https://docs.u-boot.org/en/v2024.01/usage/cmd/booti.html)
- Saved `cap-wp01-uboot.txt`
- `u-boot-xlnx@xilinx-v2024.1:board/xilinx/zynqmp/`

---

<sub>← [TF-A BL31 Stage](08-tfa-bl31-stage.md) · [Chapter index](README.md) · [Linux Kernel Boot](10-linux-kernel-boot.md) →</sub>
