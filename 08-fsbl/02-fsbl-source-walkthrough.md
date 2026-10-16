# FSBL Source Walkthrough

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot


## Read the control flow before the device drivers

The most useful starting point is `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c`. The main loop keeps `FsblStage`, `FsblStatus`, `PartitionNum` and `EarlyHandoff`. Together they tell you what the loader is doing, why it may stop, and whether it expects to return from a handoff operation.

The shared `FsblInstance` contains boot and partition state. It is not only a log record. Later functions use information stored there to choose device operations, interpret image headers and build handoff data. When inspecting it with a debugger, stop at a point where the related producer has already initialized each field.

A source walkthrough should follow one path completely. For an ordinary A53 storage boot, use initialization, device/header validation, repeated partition loading and final handoff. Then compare the JTAG and early-handoff branches. Reading every storage driver first hides the decisions that select them.

## Stage 1: from reset context to usable hardware

`XFsbl_Initialize()` lives in `xfsbl_initialization.c`. It examines reset context and performs system and processor initialization. The system path reaches `XFsbl_HookPsuInit()`, whose default implementation calls the generated processing-system initialization code.

The reset context matters because a restart is not always equivalent to power-on. Retained state may need to survive. Initialization that is safe after power-on can destroy retained DDR contents in a resume flow. This is why the source contains explicit reset and DDR self-refresh branches rather than one unconditional register sequence.

Follow each returned `Status` upward. If stage 1 returns a failure, `main()` adds `XFSBL_ERROR_STAGE_1` and enters the error stage. The later boot-device or partition-loading functions never run. A change in `xfsbl_partition_load.c` cannot fix a failure that occurs before it is called.

## Stage 2: selecting the storage implementation

`XFsbl_BootDeviceInitAndValidate()` calls the primary boot-device setup, validates headers, and considers a secondary boot device. The selected device fills the `DeviceOps` callbacks, including `DeviceInit`, `DeviceCopy` and `DeviceRelease`.

This indirection keeps the partition code mostly independent of whether bytes arrive through SD, QSPI or another supported source. It also gives you a precise debugging split: inspect the callback selection first, then inspect what the callback returns for a specific read.

For a storage boot, `main()` starts later partition loading at index 1 because partition 0 is the FSBL. This is a partition-header index, not the number of filenames in the BIF source. The reference BIF has five inputs, but its special `pmufw_image` entry is handled through boot-header fields; it is not a reason to expect five ordinary image headers.

For JTAG, the return value `XFSBL_STATUS_JTAG` takes a separate branch. The loader marks the RPU usage state for that flow and moves to stage 4. This explains why a breakpoint in the normal partition loop may never trigger during a debugger-driven boot.

## Stage 3: loading one partition completely

`XFsbl_PartitionLoad()` is in `xfsbl_partition_load.c`. Its input is the selected partition number plus the shared FSBL instance. The partition metadata controls destination, length, processor attributes and the relevant validation or security path.

Think of loading as a sequence of constraints. First, the metadata must describe a supported partition. Next, the source and destination must be valid for the selected flow. Then the transfer and any required checking must finish. Finally, the resulting entry information can be used during handoff. A memory copy alone does not establish all these conditions.

For a bitstream partition, the function reaches the programmable-logic configuration path and its before/after hooks. The destination is not an ordinary instruction entry point. For an executable partition, data placement and processor entry are separate facts. The ELF metadata can produce several loaded regions while still having one entry address.

After a successful load, `main()` marks used RPU cores and calls `XFsbl_CheckEarlyHandoff()`. If more partitions remain, it either increments `PartitionNum` or enters stage 4 for an early handoff. Thus, “handoff” is not always the last action in the whole boot image.

## Stage 4: a transfer with possible return paths

`XFsbl_Handoff()` in `xfsbl_handoff.c` receives the current partition and `EarlyHandoff`. It can return `XFSBL_STATUS_CONTINUE_PARTITION_LOAD`, causing the main loop to load the next partition. It can also return `XFSBL_STATUS_CONTINUE_OTHER_HANDOFF`, causing another handoff pass.

These return values are successful control decisions. Treating every nonzero value as an error would misread the state machine. By contrast, other unsuccessful returns receive the stage-4 error prefix and enter the error path.

The normal final transfer should not return as an ordinary C function. The source moves unexpected completion into the default exit behavior. This is useful when a debugger seems to reach code marked “should never be here”: first distinguish a supported continuation code from an unexpected final return.

## Trace one failure without guessing its origin

The error path calls `XFsbl_ErrorLockDown()`. It prints the composed status where logging allows, writes the FSBL error-status register, records the value in the instance, and applies the configured fallback behavior for supported boot modes.

`xfsbl_error.h` defines stage additions of `0x0000`, `0x2000`, `0x4000` and `0x6000` for stages 1–4. Decode an observed value using the exact build's header and the call that added the stage value. Do not interpret it as a Linux `errno`, and do not assume every error is a bitmask that can be decoded by arbitrary masking.

For example, a failure logged while loading partition 2 directs the investigation toward its header, transfer and checks. A stage-2 failure means the loader has not reached that partition loop. Preserve the first error before a fallback reset changes the visible boot sequence.

## Practical source-reading record

Keep a small trace table during debugging: current stage, selected device callback, partition index, raw return value and next state. This records control flow without requiring a large UART dump. Add the relevant source revision and ELF build identity so that another engineer can reproduce the reasoning.

The walkthrough above comes from direct inspection of the tagged sources. It does not claim a breakpoint session on the target. For physical debugging, use the same ELF that was packaged; optimization and link-time optimization can merge functions or change line stepping.

## References

- [2024.1 FSBL main state machine](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/{xfsbl_initialization.c,xfsbl_partition_load.c,xfsbl_handoff.c,xfsbl_error.h}`.
- Reference `bootgen.bif` and the Bootgen inspection in [BOOT.BIN Anatomy](../07-boot-images-and-bootgen/03-boot-bin-anatomy.md).

---

<sub>← [FSBL Overview](01-fsbl-overview.md) · [Chapter index](README.md) · [Building the FSBL](03-building-the-fsbl.md) →</sub>
