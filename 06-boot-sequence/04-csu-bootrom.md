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

## Why the first loader runs from on-chip memory

External DDR requires configuration before it can be used reliably. The initial boot path therefore needs memory that is available before normal DDR initialization. In the common A53 arrangement, BootROM places the FSBL into OCM and starts it there. The FSBL then performs the platform work needed to load later images.

This creates a size and placement constraint on the first-stage program. Adding debug output, libraries or features can increase its footprint. A source change that compiles successfully can still exceed the intended memory layout or collide with another resident object. Inspect the ELF layout and boot-image metadata when changing early firmware.

The initial executable's entry address and its source position inside the boot image are different quantities. BootROM reads from storage, places bytes in memory according to the supported format and transfers control. A correct storage offset cannot repair an invalid execution address.

## The boot header enables initial interpretation

The boot header contains the fields BootROM needs before it can process the later image structure. The reference decode includes width-detection and image-identification values, FSBL information, PMU firmware lengths, attributes and table offsets. These fields are format inputs, not a general-purpose manifest for arbitrary software.

A damaged header can prevent the system from reaching any FSBL message. This is why checking only the ELF file is insufficient: the packaged representation and its storage location also matter. Use the matching Bootgen release to inspect the actual file deployed to the medium.

The reference `BOOT.BIN` has a nonzero PMU firmware length in its boot header. Its BIF uses the special `pmufw_image` form. This is a concrete example of initial-image handling that differs from an ordinary later partition. Do not count BIF lines and assume each becomes an identical kind of partition entry.

## Fixed ROM behavior and programmable recovery

BootROM is fixed device code. A patch to FSBL cannot change what BootROM does before FSBL begins. If the failure concerns initial medium support, image search or initial authentication, investigate the ROM-defined interface and boot configuration first.

FSBL and U-Boot can add later recovery policies, but only after they execute. A robust product can have several recovery layers: ROM image search, first-stage fallback, bootloader slot selection and userspace health confirmation. Each layer detects a different class of failure and has different available state.

A runtime application hang may leave every boot header and signature valid. ROM-level format checks cannot detect that condition. A watchdog and a higher-level attempt/health policy are needed if the product must recover from it.

## Integrity, authentication and confidentiality

A structural checksum detects certain accidental changes to a header. A cryptographic hash identifies whether bytes match an expected digest. A signature can bind content to an authorized key. Encryption protects content confidentiality under its key assumptions. These mechanisms answer different questions.

A boot image can be well-formed yet unauthorized, authenticated yet incompatible with the board, or encrypted with a key unavailable on the device. Diagnose the failed policy rather than treating every rejection as file corruption.

The reference development image is not authenticated or encrypted. Its successful inspection demonstrates format readability by the tool. The QEMU boot log demonstrates a development launch path. Neither is evidence of secure BootROM enforcement on provisioned silicon.

## Investigate a pre-FSBL failure

Begin with the last confirmed physical and digital state: power, reset, selected mode and console wiring. Confirm that the deployed file is the expected boot image and that its layout matches the selected medium. Inspect it offline with Bootgen and compare its input identities with the release manifest.

If permitted debug access is available, capture documented boot and error status before resetting again. Decode it against the matching device documentation. An unreadable image, an unsupported layout and a security-policy rejection can all occur before an FSBL banner, but their corrective actions differ.

Do not infer a fallback guarantee from one successful corrupted-file experiment. Search behavior depends on medium, image placement and error class. Security policy can constrain which alternatives are accepted. The complete recovery design needs explicit tests for the failures it claims to handle.

**Evidence boundary:** the boot header and PMU firmware observations come from the actual Bootgen 2024.1 decode and reference BIF. Physical ROM search, secure boot and media-error handling remain untested on hardware in this guide's reference work.

## References

- UG1085 (v2.5), Chapter 11, CSU BootROM flow, image search and error tables
- AMD UG1283 (2024.1), PMU firmware load by BootROM and by FSBL

---

<sub>← [Power-On Reset and the PMU ROM](03-power-on-reset-and-pmu-rom.md) · [Chapter index](README.md) · [Boot Image Format](05-boot-image-format.md) →</sub>
