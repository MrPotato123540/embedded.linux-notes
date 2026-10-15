# CSU BootROM

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## BootROM responsibilities

The CSU BootROM is fixed device code. It locates and interprets the boot header, processes the initial firmware according to the boot policy, and transfers control to the FSBL. In the common A53 flow, the FSBL is placed in On-Chip Memory (OCM) because external DDR still needs initialization.

A PMU firmware image marked for BootROM loading is also handled at this stage. It is different from a normal later partition assigned to the PMU processor.

## Search and security

Image search depends on boot mode and multiboot state. The BootROM does not search every byte on every device in the same way. A flash layout must respect the documented search spacing, range and image-size restrictions.

If authentication is required, image validity includes cryptographic checks. If encryption is enabled, the correct key source and format are required. A valid header checksum cannot replace signature verification.

## Failure handling

BootROM errors occur before normal FSBL logging. Read documented boot/error status through a permitted debug path and compare it with UG1085's error tables. Depending on the error and security policy, the device may search another image or enter a failure state. Do not assume fallback always remains possible after a security failure.

> [!NOTE]
> **Not run on the reference setup:** physical BootROM fallback and authenticated/encrypted boot. The reference image is an unsigned development image.

## References

- UG1085 (v2.5), Chapter 11, CSU BootROM flow, image search and error tables
- AMD UG1283 (2024.1), PMU firmware load by BootROM and by FSBL

---

<sub>← [Power-On Reset and the PMU ROM](03-power-on-reset-and-pmu-rom.md) · [Chapter index](README.md) · [Boot Image Format](05-boot-image-format.md) →</sub>
