# FSBL Debugging

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot


## Establish the last proven boundary

A First Stage Boot Loader (FSBL) failure should be described by the last completed operation, not only by the last visible banner. The UART can be quiet because of logging options, console routing or a clock change. A processor can also fail before the UART is ready. These cases need different evidence.

Start with the exact `BOOT.BIN`, matching FSBL ELF, hardware export, boot mode and reset type. Preserve the first serial output from reset. If fallback starts another attempt, a later successful-looking banner can hide the original failure. Record the whole sequence before narrowing the capture.

The source state machine provides four boundaries: initialization, device/header setup, partition loading and handoff. Locate the last observed message in `xfsbl_main.c`, then find the operation immediately after it. This gives a testable interval rather than a broad claim that “the FSBL hangs.”

## Logging is a build-time choice

The tagged `xfsbl_debug.h` combines message classes according to `FSBL_DEBUG`, `FSBL_DEBUG_INFO` and `FSBL_DEBUG_DETAILED`. Detailed logging includes the less detailed classes. The defaults in `xfsbl_config.h` keep the optional debug values off, while mandatory printing has its own control.

The local 2024.1 XSCT recipe append adds `-DFSBL_DEBUG_INFO`. Therefore, establish the actual compile flags before changing the source header. A command-line definition can already select the desired level, and a later append can change it again.

Logging is not free. Extra messages change boot time, code size and the point at which buffers empty. The tagged handoff source includes UART FIFO handling before transfer. If the final characters are missing or mixed with the next stage, inspect that boundary before adding arbitrary delays everywhere.

## Decode an error with the same release

`xfsbl_error.h` defines stage additions: stage 1 adds `0x0000`, stage 2 adds `0x2000`, stage 3 adds `0x4000`, and stage 4 adds `0x6000`. The main loop adds the relevant value when a stage returns an error.

Use the exact observed value and find the underlying function return in that release. Do not decode the number from an old forum post without checking the source. Error definitions and call paths can change. Also, the composition is an addition in the code; treating all bits as independent flags can produce a false explanation.

`XFsbl_ErrorLockDown()` writes the error status and applies fallback for supported boot modes. If the UART fails, the status register may still provide evidence through a debugger. Reading it is useful only with the correct reset context: a new attempt or other software can change the value.

## A symptom table that separates causes

| Observation | More precise next check | What it can distinguish |
| --- | --- | --- |
| No banner after reset | PC and entry symbols from the matching ELF; console selection | No execution versus no usable output |
| Initialization stops | Generated PS initialization and reset branch | Hardware-export mismatch versus later image problem |
| Device setup fails | Selected `DeviceOps` callback and header read result | Boot-mode mismatch versus data corruption |
| One partition fails | Partition index, metadata, transfer return and destination | Bad source bytes versus unsupported attributes or memory placement |
| All partitions load but U-Boot is absent | Handoff structures, BL31 entry and console stream | Loader completion versus next-stage failure |
| JTAG works but SD fails | Compare JTAG shortcut with normal stage-2/3 flow | Download success versus storage/header correctness |

This order prevents a common mistake: replacing a good kernel while the FSBL is failing to read a boot header. Match each action to the failing boundary.

## Use the ELF to make debugger observations meaningful

The reference FSBL ELF was inspected on the host. It is AArch64 and enters at `0xFFFC0000`. Its main segment extends in memory to `0xFFFE5368`, while its handoff data and bitstream buffer occupy separate ranges. Use these facts as a baseline for this supplied artifact only.

A breakpoint at `main()` proves entry into the C application after its startup path. A breakpoint at `XFsbl_PartitionLoad()` proves the normal partition loop is active. A breakpoint at `XFsbl_Handoff()` proves the loader has reached a transfer decision; it does not prove the destination executed successfully.

Optimization can make source stepping surprising. A line can be merged, moved or removed, and link-time optimization can alter function boundaries. Inspect the disassembly and current PC when source-level stepping gives an unclear result. Do not switch to an unoptimized binary and assume its size and timing match the failing build.

## Debug a silent handoff as a state transition

After a successful load, the next stage still needs a valid entry address, processor state and memory contents. In the common flow, the FSBL transfers to Trusted Firmware-A, which later enters U-Boot. The FSBL's final message and U-Boot's first message therefore have a firmware stage between them.

Check whether BL31 is present at its expected address and whether the handoff data matches the packaged image attributes. Then inspect the prepared Non-secure entry. A BL31 log about a Secure payload address is not the BL31 load address; the reference `Secure code at 0x60000000` message describes BL32 entry information.

Also compare console routes. The reference captures include TF-A output on a separate stream. One silent terminal cannot establish that every firmware stage is silent.

## Measure timing without changing the conclusion

The source supports performance measurement under `XFSBL_PERF`, controlled by configuration. Its total-time reporting explicitly includes print time. Compare builds with equivalent logging when evaluating a speed change. Otherwise, reducing UART output can look like a faster storage or DDR algorithm.

For a timeout, identify the start event, end event and clock source. A loop count is not automatically a stable duration across clock configurations or compiler settings. For a watchdog reset, preserve reset cause and the last progress marker before changing timeout values.

> [!NOTE]
> **Not run on the reference setup:** physical JTAG breakpoints, register capture after a real boot failure and fault-injected fallback. The state and error analysis above is based on the pinned source and supplied ELF, not a claim that those hardware tests passed.

## References

- [2024.1 FSBL error definitions](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_fsbl/src/xfsbl_error.h).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/{xfsbl_main.c,xfsbl_debug.h,xfsbl_config.h,xfsbl_handoff.c}`.
- Saved `reference-setup/captures/ttyPS1-tfa.log` and supplied `zynqmp_fsbl.elf`.

---

<sub>← [Customizing the FSBL](04-fsbl-customization.md) · [Chapter index](README.md) · Next chapter: [09 · PMU and PMU Firmware](../09-pmu-firmware/README.md) →</sub>
