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

## A debugger supplies some of the loader's work

JTAG gives the host access to processor control and memory through the debug system. The host can download an ELF, set execution state and continue a target. This bypasses some normal storage-loading steps, but it does not create valid clocks, DDR configuration or firmware policy automatically.

The exact script determines which initialization is performed by the host and which is performed by downloaded firmware. Read that sequence before interpreting a successful test. A script that runs FSBL for initialization and then downloads U-Boot directly has not tested the same image parsing as BootROM and FSBL loading a packaged `BOOT.BIN`.

## Target identity is part of correctness

A ZynqMP debug connection can expose several processors and system targets. Numeric target IDs can change after reconnecting or resetting. Select the intended processor using its actual identity and state, and verify it before downloading code.

An A53 ELF, an R5 ELF and PMU firmware target different execution environments. Loading the right file into the wrong target is not a useful compatibility test. It can overwrite memory or leave the platform in a state that makes later errors difficult to explain.

Keep symbols from the exact downloaded ELF. A debugger can connect and show a program counter even when its loaded symbols belong to another build. Source lines and stack interpretation then become unreliable.

## Understand the FSBL JTAG branch

The pinned FSBL state machine treats `XFSBL_STATUS_JTAG` specially after boot-device initialization. It moves toward handoff instead of entering the ordinary later-partition loading path. The host sequence is expected to provide the appropriate next-stage setup.

TF-A also has a JTAG-specific path in `bl31_zynqmp_setup.c`, where it prepares default next-image information instead of consuming the normal first-stage handoff through `xbl_handover`. These two source observations explain why a JTAG success can coexist with a storage-boot handoff failure.

Use this difference diagnostically. If the same U-Boot ELF works when downloaded but not when packaged, inspect packaging attributes, load locations and handoff data. Do not immediately conclude that U-Boot source itself is broken.

## Initialization order must match resource availability

DDR must be initialized before the host or firmware relies on it. PMU firmware must be running and configured before operations requiring its services. PL-dependent accesses must wait until the correct design is configured and its clocks/resets are ready.

A script should make these dependencies explicit. Arbitrary delays can conceal a race on one host and fail on another. Use the supported flow's completion conditions and inspect the state when a step times out.

A halted processor can also affect the system around it. Other processors, DMA engines and watchdogs may keep running. Stopping one CPU is not equivalent to freezing the entire board. Consider the effect on shared-memory protocols and watchdog ownership before interpreting a timeout during debugging.

## Break at boundaries, then narrow the failure

Useful boundaries include FSBL initialization completion, partition handoff, TF-A next-image preparation, U-Boot entry and Linux entry. Confirm each boundary with the matching executable and expected processor state.

If the processor stops in an exception handler, preserve the exception state and fault address before resetting. If it waits in a polling loop, identify the hardware condition the loop expects. A raw program counter becomes useful only after it is connected to the exact code and state.

For a memory issue, compare the downloaded ELF layout with other live regions. A debugger can overwrite firmware or a shared buffer without the same checks performed by the normal loader. A successful download message means bytes were transferred, not that the complete system map remains valid.

## Repeat from a clean start

Warm debug sessions can retain initialized DDR, configured PL and peripheral state. A boot that succeeds only after another script ran has an undocumented dependency. Power-cycle or use the required complete reset and repeat the supported sequence before accepting the result.

Finally test the intended production boot medium. JTAG is valuable for finding the failing function and inspecting state, but it does not validate flash placement, boot-mode straps or BootROM search behavior. Physical JTAG and cold-boot validation remain open on the reference setup.

**Source trail:** pinned FSBL `xfsbl_main.c`, TF-A `bl31_zynqmp_setup.c`, and UG1144/UG1400 2024.1 debug-flow documentation. No fabricated XSDB transcript is presented.

## References

- AMD UG1144 (2024.1), booting with JTAG
- AMD UG1400 (2024.1), XSDB and embedded debug flows

---

<sub>← [Multiboot, Fallback and Golden Images](13-multiboot-and-fallback.md) · [Chapter index](README.md) · [Boot Troubleshooting](15-boot-troubleshooting.md) →</sub>
