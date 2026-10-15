# TF-A BL31 Stage

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## BL31 entry and lifetime

Trusted Firmware-A (TF-A), previously called ATF, provides the EL3 runtime layer. Its BL31 stage initializes the platform's secure-monitor services, uses FSBL handoff data and enters the next Non-secure image.

PSCI supplies standard processor power operations. Silicon-provider services expose platform-specific operations. Some requests are handled in TF-A; others require communication with PMU firmware. TF-A therefore remains relevant after the U-Boot banner disappears.

## Reference boot

The reference BIF marks `bl31.elf` for A53-0, EL3 and Secure execution. It marks `u-boot.elf` for EL2. The saved U-Boot output confirms EL2 entry.

The separately saved TF-A console log may come from a QEMU launch arrangement with different load addresses. Do not combine its addresses with `BOOT.BIN` partition addresses without checking the launch configuration.

## Debugging

If the FSBL completes but U-Boot never appears, check BL31 placement, image entry metadata, memory overlap and console routing. A silent TF-A build does not prove that execution never reached TF-A. Use the matching ELF and a debugger if the serial evidence is insufficient.

## References

- TF-A v2.10 [ZynqMP platform documentation](https://trustedfirmware-a.readthedocs.io/en/v2.10/plat/xilinx-zynqmp.html)
- Reference `bootgen.bif`, `boot-manual-1.log`, `ttyPS1-tfa.log`

---

<sub>← [PMU Firmware at Boot](07-pmufw-stage.md) · [Chapter index](README.md) · [U-Boot Stage](09-u-boot-stage.md) →</sub>
