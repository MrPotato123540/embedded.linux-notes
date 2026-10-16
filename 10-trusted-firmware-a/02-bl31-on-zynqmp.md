# BL31 on ZynqMP

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot


## Start with the platform entry structures

The ZynqMP implementation is in `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/bl31_zynqmp_setup.c`. It keeps separate `entry_point_info_t` objects for BL32 and BL33. Each describes a next-stage entry, including its program counter, saved processor state and security attributes.

`bl31_early_platform_setup2()` sets up the console and platform configuration, initializes those structures, and reads the FSBL handoff address from `PMU_GLOBAL_GEN_STORAGE6`. This happens before later architectural setup creates the monitor's memory mappings.

The handoff address points to data; it is not the U-Boot entry address itself. The data must have the format and lifetime expected by `xbl_handover()`. A correct register value that points to overwritten memory is still a broken handoff.

## Storage boot and JTAG take different branches

For non-JTAG boot, the platform calls `xbl_handover()` to fill the next-image structures from the first-stage handoff data. If it does not report success, the platform panics. Therefore, a malformed or unavailable handoff can stop execution before U-Boot begins.

For JTAG mode, the code calls `bl31_set_default_config()`. This sets BL32's program counter from `BL32_BASE`, obtains BL33's entry through `plat_get_ns_image_entrypoint()`, and prepares a Non-secure AArch64 EL2 state with the selected stack mode and exceptions masked.

This is a real behavior difference. A debugger session can work with defaults while storage boot requires valid first-stage metadata. When JTAG succeeds and SD fails, compare the handoff branch before assuming that a new compiler or a damaged U-Boot executable explains the difference.

## Decode the reference Secure-entry message correctly

The saved log includes `Secure code at 0x60000000`. The source prints that address from `bl32_image_ep_info.pc`. The prefix identifies BL31 as the program printing the line, while the value describes BL32's prepared entry.

In the tagged platform header, the default BL32 base is `0x60000000`. The JTAG default helper assigns it even though this reference boot package has no BL32 payload. The message therefore proves neither that BL31 resides at that address nor that OP-TEE was loaded there.

To establish a Secure payload, inspect the actual package input, destination memory, dispatcher configuration and trusted-OS runtime evidence. A nonzero default entry field is weaker evidence than a loaded and initialized image.

## A worked BL31 ELF inspection

Host `readelf -l` and `readelf -SW` were run on the supplied `bl31.elf`. The ELF entry and `.text` start are `0xFFFEA000`. The sections show the following runtime ownership:

| Section | Address | Size | Meaning |
| --- | --- | --- | --- |
| `.text` | `0xFFFEA000` | `0x8000` | Executable code |
| `.rodata` | `0xFFFF2000` | `0x1000` | Read-only data section |
| `.data` | `0xFFFF3000` | `0x3092` | Initialized data |
| `.stacks` | `0xFFFF60C0` | `0x1100` | Runtime stacks |
| `.bss` | `0xFFFF71C0` | `0xE40` | Zero-initialized state |
| `.xlat_table` | `0xFFFF8000` | `0x5000` | Translation tables |
| `.coherent_ram` | `0xFFFFD000` | `0x1000` | Coherent runtime storage |

The last four are `NOBITS`: they need memory but do not store their initial contents as ordinary file bytes. The section range reaches the end-exclusive address `0xFFFFE000`.

The ELF loadable segment starts earlier, at aligned address `0xFFFE0000`, and includes headers/alignment before `.text`. This shows why segment base, entry point, section address and Bootgen partition placement must not be treated as synonyms. Inspect the boot image's actual load metadata as well as the ELF.

## Architectural setup creates the monitor's mappings

`bl31_plat_arch_setup()` initializes the interconnect and enters coherency, then builds memory-map regions. It maps the BL31 runtime region, code, read-only data and coherent memory with their intended attributes before enabling the EL3 memory-management unit.

The code and read-only mappings matter beyond performance. They describe which pages are executable or writable in the monitor's own translation regime. The ELF program header's broad flags do not alone describe the final runtime page permissions.

When a custom service accesses a new device or buffer, its physical range must be represented by an appropriate mapping. Mapping a peripheral as normal cached memory can change access behavior. Mapping arbitrary caller-provided ranges into Secure firmware without validation creates a much larger problem than a missing device access.

## Platform setup and runtime setup are separate

`bl31_platform_setup()` prepares the device tree and initializes the interrupt controller. `bl31_plat_runtime_setup()` handles optional runtime interrupt registration, custom runtime setup and the console's runtime state.

A console available during early boot may have different runtime behavior. A message that appears before U-Boot does not prove that later firmware-call diagnostics use the same console state or level. Check the runtime console configuration when a service fails silently.

The optional watchdog-restart interrupt handling is also build-dependent. Read its feature condition before expecting those handlers or assuming an interrupt is routed to the normal-world kernel.

## Failure diagnosis from the exact transition

If the first BL31 message is absent, inspect its actual entry and console initialization. If early setup runs but panics before the Non-secure image, inspect the handoff branch and data. If U-Boot begins but later firmware calls fail, inspect resident memory, service registration and PMU cooperation.

A delayed corruption case needs a memory-lifetime review. The `.bss`, stacks and translation tables remain required after boot. Excluding only the initialized image bytes from later allocations is insufficient.

## References

- [2024.1 BL31 ZynqMP setup](https://github.com/Xilinx/arm-trusted-firmware/blob/xilinx-v2024.1/plat/xilinx/zynqmp/bl31_zynqmp_setup.c).
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/include/platform_def.h`.
- Reference `pre-built/linux/images/bl31.elf`, executed host ELF inspections, and saved `ttyPS1-tfa.log`.

No new BL31 binary or hardware handoff test was executed for this section.

---

<sub>← [TF-A Overview](01-tfa-overview.md) · [Chapter index](README.md) · [Building and Customizing TF-A](03-tfa-customization.md) →</sub>
