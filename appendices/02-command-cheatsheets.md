# Command Cheat Sheets

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[Appendices](README.md)** · Appendices

## Use the correct environment

Commands below are an interface index. Availability depends on the image and configuration. Only commands identified as executed in their chapter are recorded tests; a tool name here is not evidence of a completed hardware operation.

| Environment | Interface | Purpose |
| --- | --- | --- |
| PetaLinux 2024.1 | `petalinux-create project/apps/modules` | Create project components |
| PetaLinux 2024.1 | `petalinux-config -c` | Configure a component |
| PetaLinux 2024.1 | `petalinux-build -c`, `-x`, `--sdk` | Build component, task or SDK |
| PetaLinux 2024.1 | `petalinux-package boot` | Boot packaging; inspect subcommand help |
| BitBake | `-e`, `-g`, `-c` | Environment, dependency graph, selected task |
| devtool | `modify`, `build`, `finish` | Source development and recipe integration |
| U-Boot | `help`, `version`, `printenv`, `bdinfo` | Inspect capabilities and state |
| U-Boot | `tftpboot`, `fatload`, `ext4load` | Load selected files |
| U-Boot | `booti`, `bootm` | Enter a supported kernel/image format |
| Linux | `uname`, `dmesg`, `ip`, `ss`, `lsmod` | Inspect system, network and modules |
| XSDB | `targets`, `mrd` | Select/inspect a debug target |
| Bootgen | `-arch zynqmp -read` | Decode a boot image |
| FIT tools | `dumpimage -l` | List FIT content |
| Device tree | `dtc -I dtb -O dts` | Decompile a DTB |

## Preserve evidence

Before changing hardware state, save logs, versions and artifact hashes. Verify the selected device and address range. Flash writes, memory tests, reset operations and security provisioning are deliberately not reduced to blind copy-paste shortcuts.

For executed examples, see [boot-image inspection](../06-boot-sequence/05-boot-image-format.md), [FIT inspection](../11-u-boot/04-fit-images.md), [SSH](../01-linux-fundamentals/07-ssh.md) and [certificate validation](../25-security-fundamentals-and-cryptography/03-pki-and-certificates.md).
## Choose a command from a question

A useful command sheet starts with the unknown. “Why does boot fail?” is too broad. “Which ELF entry address is packaged?”, “Which FIT configuration is selected?” and “Did the network obtain a route?” each lead to different evidence.

| Question | Inspection interface | What the result does not establish |
| --- | --- | --- |
| Are these two artifacts identical? | `sha256sum` | Whether either artifact is approved or bootable |
| What CPU and entry point does an ELF use? | `readelf -h` | Whether its entire runtime memory fits |
| Which ranges does the ELF loader need? | `readelf -lW`, `readelf -SW` | Whether another stage overwrites them later |
| What does Bootgen see in the container? | The 2024.1 `bootgen -read` interface | Successful execution on the board |
| Which objects does a FIT describe? | `dumpimage -l` and FDT inspection | Enforcement of signature policy |
| What does a compiled device tree contain? | `dtc`, `fdtget` | Correct physical wiring or driver behavior |
| Which package versions were included? | The image's `rootfs.manifest` | The current deployed state after field changes |
| Which recipe value wins? | BitBake environment inspection | That an old prebuilt artifact used that metadata |

The linked chapters contain the executed forms and their output. Tool availability is context-specific: a command installed on the development host may be absent from the target image.

## Executed artifact identity and ELF checks

The following read-only commands were run from the reference BSP's `pre-built/linux/images` directory on 16 October 2026. Paths are relative to that directory.

```console
$ sha256sum BOOT.BIN image.ub zynqmp_fsbl.elf bl31.elf
97363bab9a28ecda6713840aa55986b98b09fd51b016b030224064f04af612ff  BOOT.BIN
cdb0f83e458bf471ddbf333ed40e2a5912325ae46c5f57da3ba9a8113203fc84  image.ub
e0b2346b76f65ff97b7d56b309315b078baced1b10132f7e94e06eef0ff443ad  zynqmp_fsbl.elf
9c9380fa4fdbb3196420662bc6871b8223ccc53224ddc006b3e33bcb8f86c7b2  bl31.elf
$ readelf -h bl31.elf
ELF Header:
...
  Class:                             ELF64
  Data:                              2's complement, little endian
...
  Machine:                           AArch64
...
  Entry point address:               0xfffea000
...
```

Use the hashes to identify the exact inspected artifacts. They are not universal hashes for every ZCU106 build. Changing source, configuration or protection metadata can change them legitimately.

The entry point tells you where BL31 begins executing. It is not its whole allocation. Compare program-header memory sizes and section placement before deciding whether another component can use nearby OCM. [TF-A BL31](../10-trusted-firmware-a/02-bl31-on-zynqmp.md) follows that calculation.

## Identify the container before choosing the loader

This command was also run against the same supplied files:

```console
$ file Image image.ub rootfs.cpio.gz
Image:          Linux kernel ARM64 boot executable Image, little-endian, 4K pages
image.ub:       Device Tree Blob version 17, size=15961184, boot CPU=0, string block size=116, DT structure block size=15960152
rootfs.cpio.gz: gzip compressed data, max compression, from Unix, original size modulo 2^32 862212608
```

The FIT reports a device-tree container because FIT uses that binary structure. This does not make it the same object as the board's standalone device tree. The gzip result identifies compression; the decompressed archive format needs its own inspection.

The gzip size field is reported modulo 2^32. For arbitrary large files, it is not a sufficient independent size proof. Similarly, a file extension is a naming convention rather than a validated format. Choose the parser and boot command from the actual format and the documented loading path.

## Keep execution contexts visible

| Prompt | Where it runs | Typical state to record first |
| --- | --- | --- |
| `$` | Host shell | Working directory, tool path/version, SDK environment |
| `target$` | Target Linux as a normal user | Running release, user, device permissions |
| `target#` | Target Linux as root | Same information plus intended privileged scope |
| `ZynqMP>` | U-Boot | Version, environment and currently loaded RAM ranges |
| `xsdb%` | XSDB debugger | Selected target, core state and reset context |

Do not copy a host path into a target command and assume it names the same file. An SDK sysroot is a host-side directory used for target compilation. It is not automatically the root filesystem mounted by the board.

A sourced SDK also changes compiler and linker selection. Preserve the environment identity with a build record. If an ELF unexpectedly reports an x86 machine type, first check the compiler actually invoked rather than modifying the target bootloader.

## Diagnose by the last confirmed boundary

For boot, move from container decode to stage entry, partition load, handoff and kernel/rootfs initialization. For networking, move from link to address, route, transport and application authentication. For drivers, move from hardware description to device creation, matching, probe and first transaction.

This order prevents misleading fixes. DHCP success does not prove that a TFTP filename exists. A created device node does not prove that the hardware completed a DMA transfer. A signed container does not prove the board uses its intended trust anchor.

The guide's recorded examples are in [boot troubleshooting](../06-boot-sequence/15-boot-troubleshooting.md), [network configuration](../22-networking-and-peripherals/02-network-configuration.md) and [the driver model](../14-kernel-modules-and-drivers/04-linux-device-driver-model.md). Check their validation notes before treating a proposed procedure as a completed experiment.

## Capture evidence before changing state

Preserve the exact command, working directory, tool version, exit status and relevant output. For a long log, keep the first failure and enough earlier context to locate the stage. A final reset message can hide the actual verification or storage error.

Memory reads are not automatically side-effect-free. Registers can be read-to-clear, FIFOs can advance and a powered-down block can fault. Debugger writes, resets and device reprobes also change the evidence. Use the [register reference](03-register-quick-reference.md) to establish semantics before access.

For security tests, keep private keys and credentials out of the capture. Record public fingerprints and artifact digests instead. The [crypto API lab](../25-security-fundamentals-and-cryptography/examples/crypto_boundaries.py) can be rerun without hardware or persistent keys; the Bootgen authentication capture is a separate host experiment with explicit limits.


---

<sub>← [Glossary](01-glossary.md) · [Chapter index](README.md) · [Register Quick Reference](03-register-quick-reference.md) →</sub>
