# TF-A BL31 Stage

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## BL31 entry and lifetime

Trusted Firmware-A (TF-A), previously called ATF, provides the EL3 runtime layer. Its BL31 stage initializes the platform's secure-monitor services, uses FSBL handoff data and enters the next Non-secure image.

PSCI supplies standard processor power operations. Silicon-provider services expose platform-specific operations. Some requests are handled in TF-A; others require communication with PMU firmware. TF-A therefore remains relevant after the U-Boot banner disappears.

## Reference boot

The reference BIF marks `bl31.elf` for A53-0, EL3 and Secure execution. It marks `u-boot.elf` for EL2. The saved U-Boot output confirms EL2 entry.

The saved TF-A console message `Secure code at 0x60000000` identifies the prepared BL32 entry, not BL31 itself. In the pinned source, JTAG mode initializes that value from `BL32_BASE`. It does not prove that a secure OS was loaded. Match each printed address to its source variable before comparing it with the boot-image layout.

## Debugging

If the FSBL completes but U-Boot never appears, check BL31 placement, image entry metadata, memory overlap and console routing. A silent TF-A build does not prove that execution never reached TF-A. Use the matching ELF and a debugger if the serial evidence is insufficient.

## BL31 is the monitor, BL32 and BL33 are next-stage identities

TF-A uses stage names to describe roles. BL31 is the EL3 runtime firmware. BL32 denotes an optional Secure payload, such as a trusted OS. BL33 denotes the Non-secure payload, normally U-Boot in this flow. A log line printed by BL31 can describe BL32 or BL33 rather than BL31 itself.

This distinction resolves the reference message `Secure code at 0x60000000`. In `bl31_zynqmp_setup.c`, the printed value comes from `bl32_image_ep_info.pc`. The Non-secure message comes from `bl33_image_ep_info.pc`. The prefix identifies the program printing the message, not the owner of every address that follows it.

The reference BIF contains BL31 and U-Boot but no BL32 payload. The secure-entry message alone therefore cannot establish that OP-TEE was packaged or started. To prove a trusted OS is running, inspect its actual image, handoff configuration and runtime evidence.

## The pinned platform code has a JTAG branch

`bl31_early_platform_setup2` first initializes the console and platform configuration. It prepares entry-point structures for Secure and Non-secure images and reads the handoff address from `PMU_GLOBAL_GEN_STORAGE6`.

The next step depends on boot mode. In JTAG mode, the platform calls `bl31_set_default_config`. Otherwise, it calls `xbl_handover` with the prepared entry structures and handoff address; an unsuccessful result leads to a panic. This is a real control-flow difference, not only a different way to download the same files.

The default helper assigns BL32's program counter from `BL32_BASE` and obtains BL33's entry from `plat_get_ns_image_entrypoint`. It prepares the Non-secure saved processor state for AArch64 EL2 with the selected stack mode and exceptions masked. The saved U-Boot log's EL2 report is consistent with that intended handoff.

A debugger session can therefore use default entry information where a normal storage flow consumes first-stage handoff data. If storage boot fails after FSBL while JTAG works, inspect that difference before assuming the ELFs are identical in every relevant respect.

## Handoff includes processor state

The entry-point structure contains more than a program counter. The next stage needs the correct security attributes, saved processor state and arguments. EL3 firmware uses this information when it exits to the next exception level.

A raw branch to the U-Boot address would not establish the same contract. The monitor must prepare the transition between security and exception-level contexts. An invalid state can cause an exception before the next stage's console becomes available.

When debugging, inspect the prepared entry structure and the relevant saved state using the matching symbols. Do not infer the complete transition solely from the load address printed by a packaging tool.

## BL31 memory remains owned at runtime

The inspected reference BL31 ELF enters at `0xFFFEA000`. Its sections include code, data, stacks, BSS, translation tables and coherent memory. Some regions have no initialized bytes in the file but still require runtime storage. Their space cannot be reclaimed merely because U-Boot and Linux have started.

Linux can invoke EL3 services later. If another stage overwrites monitor code or data, the first visible failure may occur during a CPU power operation or platform-management call rather than during initial boot. This delayed failure makes ownership and reservation review essential.

Use the ELF and platform linker layout to understand the full footprint, and use the actual boot package to understand what was loaded. File size, partition size and runtime memory size answer different questions.

## Runtime calls and firmware cooperation

PSCI standardizes processor power-management calls. Platform-specific services cover other device operations. Some requests can be handled in the monitor; others depend on PMU firmware. Keep the caller, service implementation and platform policy aligned.

A device driver reporting a firmware error may have reached this interface successfully and received a rejection. That is different from a missing transport or a crashed monitor. Preserve the return code and trace the selected call path before changing unrelated hardware configuration.

## Console silence is not proof of missing execution

The reference TF-A messages were captured on a separate console stream. A board can route firmware and Linux output differently, and build settings can change logging. If FSBL completes but no familiar banner appears, confirm console routing before concluding the processor never entered BL31.

Use the matching ELF to place a breakpoint at the platform setup or next-image preparation path when permitted. Then check entry data, memory contents and the actual next-stage PC. This gives stronger evidence than adding arbitrary delays to boot scripts.

**Source:** [2024.1 ZynqMP BL31 setup](https://github.com/Xilinx/arm-trusted-firmware/blob/xilinx-v2024.1/plat/xilinx/zynqmp/bl31_zynqmp_setup.c), read directly alongside the reference BIF, firmware ELF and saved console logs. No new TF-A build or secure-payload boot was performed.

## References

- TF-A v2.10 [ZynqMP platform documentation](https://trustedfirmware-a.readthedocs.io/en/v2.10/plat/xilinx-zynqmp.html)
- Reference `bootgen.bif`, `boot-manual-1.log`, `ttyPS1-tfa.log`

---

<sub>← [PMU Firmware at Boot](07-pmufw-stage.md) · [Chapter index](README.md) · [U-Boot Stage](09-u-boot-stage.md) →</sub>
