# JTAG Boot

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## JTAG boot principles

JTAG allows a host debugger to control processors and load code without relying on a normal storage boot image. It does not remove initialization requirements. DDR still needs valid setup, and firmware still needs correct processor state and load addresses.

A typical supported sequence prepares the PMU, runs the FSBL, loads required firmware and U-Boot, then continues to Linux. Programmable logic must be configured before software accesses dependent devices. The exact order depends on the selected tool script and platform.

## Using the generated flow

Start with the PetaLinux 2024.1 JTAG boot flow for the board. Inspect its generated Tcl actions: target selection, resets, downloads and continue operations. This is safer than combining commands from different board tutorials.

Select targets by their actual identity. Debugger target numbers can change after reconnecting. Loading an ELF into the wrong processor can fail or corrupt memory without giving a useful boot error.

## Debugging boundaries

Keep symbols for the exact ELF files being loaded. Stop at stage entry points to determine which handoff failed. A warm debugger session may retain hardware state that a cold boot does not have, so repeat final validation from power-on.

> [!NOTE]
> **Not run on the reference setup:** physical JTAG boot. The existing QEMU debug connection does not validate a cable, board reset or hardware-server setup.

## References

- AMD UG1144 (2024.1), booting with JTAG
- AMD UG1400 (2024.1), XSDB and embedded debug flows

---

<sub>← [Multiboot, Fallback and Golden Images](13-multiboot-and-fallback.md) · [Chapter index](README.md) · [Boot Troubleshooting](15-boot-troubleshooting.md) →</sub>
