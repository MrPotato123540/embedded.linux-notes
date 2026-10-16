# Boot Troubleshooting

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Find the last confirmed stage

| Symptom | First checks |
| --- | --- |
| No output | Power, reset, mode straps, UART selection and baud rate |
| FSBL error | Stage/error code, hardware export, storage and DDR initialization |
| FSBL finishes, no U-Boot | BL31 and U-Boot addresses, handoff state, console routing |
| U-Boot cannot load files | Selected device, partition, filesystem and filename |
| Stops at `Starting kernel ...` | Arm64 entry state, DTB and early console |
| Root-mount panic | Root argument, driver availability and filesystem format |
| Login works, application fails | Services, permissions, libraries and application logs |

## Evidence to keep

Save the complete serial log, tool versions, image checksums, boot mode and reset type. Record whether the test used prebuilt files or a new local build. “Same filename” is not enough to identify an image.

Read hardware error registers only through a documented access path and before a reset changes the evidence. Decode FSBL errors against the exact source release. A numeric code from another release may have a different meaning.

## Reduce the problem

Change one input at a time. Start with the reference BSP on the reference board when possible. Then add the new hardware export, firmware change or custom driver separately. Repeatedly cleaning the build cannot repair an electrical clock or reset problem.

For a stuck processor, JTAG can show the program counter and stack, but use the matching symbols. QEMU is useful for software sequencing; it cannot prove DDR margins or physical peripheral timing.

## Build a hypothesis from the last confirmed action

A boot log is a sequence of observations. The last printed line identifies code that reached a print path, but it may not identify the instruction that failed next. Buffered output, console changes and disabled logging can hide progress.

Write the smallest claim supported by the evidence. “U-Boot printed its kernel handoff line” is stronger and more precise than “Linux started.” “The storage command transferred the expected byte count” is different from “the loaded image is valid.” These distinctions keep the investigation focused.

Preserve the full log from reset, not only the final screen. Earlier firmware warnings, selected filenames and load addresses often explain a later panic. Keep the reset type, boot mode and artifact checksums with the log.

## Work through the handoff contracts

For a pre-FSBL silence, confirm electrical readiness, mode selection, initial image format and console routing. For an FSBL failure, decode the stage and error against the pinned source. For a post-FSBL silence, inspect next-image placement, handoff data and TF-A console selection.

At U-Boot, verify which device and partition the script selected. Check filenames and transferred sizes. Then inspect the image format, DTB and initramfs. If Linux begins printing, move the investigation to the specific kernel subsystem or userspace boundary rather than continuing to change early firmware without evidence.

A structured investigation can stop at a boundary and test its input independently. For example, inspect a FIT offline before trying another board boot. Decode `BOOT.BIN` before changing FSBL logging. Inspect the final DTB before patching a driver that never receives the expected resource.

## Separate common look-alike failures

| Observation | Competing explanations | Evidence that separates them |
| --- | --- | --- |
| No UART text | CPU never reached code, wrong UART, disabled logging | Debug state, console routing and matching build settings |
| No output after kernel handoff | Invalid entry state, damaged DTB, silent early console | Loaded memory, boot protocol and early-console configuration |
| Root mount fails | Wrong root identity, missing early driver, wrong filesystem | Kernel device discovery and command line |
| Init file exists but fails | Missing interpreter, wrong ABI, permissions | ELF/script format and exact execution error |
| Device never becomes ready | Missing provider, wrong binding, unavailable hardware | Probe messages, live tree and hardware state |
| Only warm boot works | Retained initialization or stale state | Controlled cold/warm comparison |

Do not choose a fix until the evidence separates the plausible causes. Otherwise, a workaround can hide one symptom while introducing another.

## Reduce variables without destroying evidence

Start from a known artifact set and change one input. If a new XSA breaks boot, keep firmware, kernel and application changes separate where possible. If a new driver breaks a peripheral, first confirm that the same hardware and device tree still work with the previous driver.

Before cleaning the build, save task logs, final configuration and any local source experiments. A broad clean can remove the only record of the failed compiler invocation or patch state. Rebuild after you have a hypothesis about which input should change.

Use hashes to identify files. Modification times can change when files are copied, and identical filenames can refer to different builds. For containers, inspect the payload identities rather than assuming the newest loose file was repackaged.

## Use a debugger to answer a specific question

A debugger is most useful when the question is narrow: did execution reach BL31, which next-image PC was prepared, which instruction faulted, or which register condition is a loop waiting for? Load the matching symbols and preserve relevant exception or status information.

Be aware that halting one processor may leave watchdogs, DMA engines or another processor active. Debugging can change timing and cause secondary failures. Record the intervention and distinguish it from the original symptom.

For an apparent memory corruption, build a map of live ranges and owners. Include decompressed images, runtime firmware, buffers and relocated bootloader state. Check lifetimes as well as static addresses.

## Confirm the fix through the original path

A workaround tested through JTAG is not complete evidence for a storage-boot defect. A kernel loaded manually is not complete evidence for a broken boot script. Repeat the original failing path after applying the correction, then test nearby cases such as cold boot, restart and recovery.

Record the initial symptom, evidence, root cause, changed input and final validation. A useful conclusion explains why the fix addresses the failed contract. “It works after rebuilding everything” is an observation that still needs an explanation.

The reference logs and source inspections support the reasoning here. Physical reset, media-error and peripheral tests remain explicitly open; the guide does not present emulator success as proof of those conditions.

## References

- UG1085 (v2.5), boot error status and reset sections
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_error.h`
- Saved reference boot and U-Boot captures

---

<sub>← [JTAG Boot](14-jtag-boot.md) · [Chapter index](README.md) · Next chapter: [07 · Boot Images, BIF and Bootgen](../07-boot-images-and-bootgen/README.md) →</sub>
