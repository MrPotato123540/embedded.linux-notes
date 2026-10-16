# FSBL Stage

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## FSBL sequence

The **First Stage Boot Loader (FSBL)** turns the reset-time platform into a system ready to load later software. Its main state machine separates initialization, boot-device and header processing, partition loading, and handoff.

Generated `psu_init` code configures the processing system, including clocks, pins and DDR settings from the hardware design. Board-specific code adds work not fully described by the processor export. Using initialization from another board can fail before any useful DDR test runs.

## Loading and handoff

Partition metadata describes the destination processor, load address, entry address, exception level and security attributes. The FSBL checks and loads each supported partition. A programmable-logic partition is sent through the configuration path rather than executed as CPU code.

The FSBL prepares handoff information for TF-A and transfers control. This handoff is more than a branch to an address: the next stage also expects the correct processor state and image metadata.

## Debugging

Use the stage and error code together. A storage read error, DDR write failure and handoff error require different investigations. Enable only the debug detail needed; added logging changes image size and boot timing.

## Walk the pinned state machine

The 2024.1 `xfsbl_main.c` uses an explicit stage variable. Reading this state machine gives a better diagnostic model than treating FSBL as one large initialization function.

| State | Main operation | Important transition |
| --- | --- | --- |
| `XFSBL_STAGE1` | `XFsbl_Initialize` | Initialization success advances to stage 2 |
| `XFSBL_STAGE2` | `XFsbl_BootDeviceInitAndValidate` | Storage boot proceeds to loading; JTAG follows a special path |
| `XFSBL_STAGE3` | `XFsbl_PartitionLoad` | Loads selected partitions and checks early handoff |
| `XFSBL_STAGE4` | `XFsbl_Handoff` | Transfers execution or returns to further loading for early handoff |
| Error stage | `XFsbl_ErrorLockDown` | Handles the recorded failure |

The storage path starts later-partition loading at partition number 1 because partition 0 represents the first-stage image in this flow. The JTAG status instead sends the state machine toward handoff without following the ordinary storage partition loop. This is a concrete reason that a debugger boot does not validate the same operations as an SD or flash boot.

Early handoff adds another branch. The code can hand off an application and then continue loading remaining partitions or handing off other applications. Do not assume every handoff means the FSBL has completed all work for all processors.

## Stage information changes the meaning of an error

The pinned `xfsbl_error.h` defines stage contributions `0x0000`, `0x2000`, `0x4000` and `0x6000` for stages 1 through 4. The main state machine adds the relevant stage contribution on several failure paths. Decode the complete status against the exact source, including where the failure was returned.

For example, a load-address error during partition processing is different from a DDR initialization failure before the image-loading loop. Both can eventually stop boot, but one points toward partition metadata and memory policy while the other points toward hardware initialization.

Do not map a number to a label using a table from another release without checking it. Error definitions and call paths are implementation details. Preserve the complete log around the error because the preceding operation may narrow the cause more than the final number.

## Initialization must match the exported hardware

The generated processing-system initialization data describes clocks, pin multiplexing, memory setup and other hardware choices. Board-specific hooks can add requirements outside the exported processor configuration. Both parts must agree with the actual board and revision.

If DDR initialization is wrong, the FSBL may still execute from OCM and print messages. A later partition write into DDR can then fail or corrupt data. This makes the last printed stage useful, but it does not mean the storage payload caused the underlying fault.

Keep the initialization source tied to the XSA identity. Rebuilding FSBL against an old hardware handoff while updating only the Linux device tree leaves the early hardware state inconsistent.

## Partition metadata controls destination and execution

For each partition, distinguish the source bytes, destination memory and eventual execution target. A DTB is data. A bitstream is configuration data for PL. An executable has an entry point and processor-state requirements. Their loading paths cannot be reduced to the same memory copy followed by a branch.

The reference BIF marks BL31 for A53-0, EL3 and Secure execution, and U-Boot for A53-0 at EL2. FSBL uses the image metadata and prepares handoff information consumed by later firmware. A correct ELF name does not compensate for incorrect BIF attributes.

The handoff data itself also occupies memory. Its lifetime must extend until the consumer reads it. Inspect the linker layout and handoff source when changing early firmware placement. Temporary buffers that can be reused later must not be confused with resident runtime firmware.

## Debugging should preserve the failure

Enable enough FSBL logging to identify the stage and partition. Record image identity and the hardware export used. If a debugger is available, use the matching ELF symbols to inspect the failing function and relevant memory rather than guessing from a raw program counter.

Extra logging changes code size and timing. The pinned performance-print path even notes that measured execution includes print time. Compare performance builds with the same logging policy, and verify that a debug build still fits its intended memory region.

Finally, repackage the rebuilt FSBL into the boot image and verify that the board ran it. A source-level fix tested only by a debugger may be correct while the deployed storage still contains an older first stage.

**Source:** [2024.1 FSBL state machine](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c), with `xfsbl_error.h`, `xfsbl_initialization.c`, `xfsbl_partition_load.c` and `xfsbl_handoff.c` from the same directory. These files were inspected directly; no newly compiled FSBL was booted.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c`
- Same directory: `xfsbl_initialization.c`, `xfsbl_partition_load.c`, `xfsbl_handoff.c`
- [FSBL source walkthrough](../08-fsbl/02-fsbl-source-walkthrough.md)

---

<sub>← [Boot Image Format](05-boot-image-format.md) · [Chapter index](README.md) · [PMU Firmware at Boot](07-pmufw-stage.md) →</sub>
