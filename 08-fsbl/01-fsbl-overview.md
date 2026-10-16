# FSBL Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot


## The contract between BootROM and later software

The **First Stage Boot Loader (FSBL)** turns a partly initialized chip into a system that can run later software. On the usual Cortex-A53 flow, the Configuration Security Unit BootROM loads the FSBL into On-Chip Memory (OCM). The FSBL cannot depend on working external DDR at its entry point: preparing DDR is part of its own job.

This order explains why a Linux boot failure can start in an older hardware export. A changed DDR part, clock setup or pin assignment can change the generated initialization code. Rebuilding only Linux leaves that early code unchanged. The processor may fail before Linux has any chance to report the problem.

The FSBL is a standalone program from AMD (formerly Xilinx), in `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src`. It has its own linker layout, board support code and device drivers. Its normal A53 build runs at Secure exception level 3 (EL3). The Cortex-R5 FSBL is a different processor flow; the A53 exception-level model does not apply to it.

## Four states, with different evidence at each boundary

The main loop in `xfsbl_main.c` uses four normal stages. These stages form useful fault boundaries.

| Stage | Main operation | What success establishes |
| --- | --- | --- |
| 1 | `XFsbl_Initialize()` | Required system and processor initialization completed |
| 2 | `XFsbl_BootDeviceInitAndValidate()` | Boot-device access and boot-image headers are usable for this flow |
| 3 | `XFsbl_PartitionLoad()` | The selected later partition passed its loading path |
| 4 | `XFsbl_Handoff()` | The FSBL prepares or performs the next processor handoff |

Stage 3 repeats for later partitions. A successful SD-card initialization does not prove that every file block or partition is valid. A successful partition copy does not prove that its entry address, security state or target processor is correct. Keep these claims separate when reading logs.

The JTAG path is different. Stage 2 can return `XFSBL_STATUS_JTAG`, which sends the state machine directly to handoff. A debugger can supply images separately. Therefore, a working JTAG session does not prove that the storage image headers or storage transfer path work. See the exact branches in [the pinned main loop](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c).

## A worked memory example from the BSP

The reference `zynqmp_fsbl.elf` was inspected with the host `readelf` tool. Its entry address is `0xFFFC0000`. The first loadable segment has file size `0x1F448` and memory size `0x25368`. It starts at the same address.

The end-exclusive runtime address of that segment is therefore `0xFFFE5368`. Its memory requirement exceeds its initialized file bytes by `0x5F20`. That difference includes sections such as zero-initialized data, heap and stack. Copying only the bytes visible in a file is not a complete memory-lifetime analysis.

Two more loadable segments start at `0xFFFE9E00` and `0xFFFF0040`. Both have zero file size, but need `0x88` and `0xFC00` bytes of memory. Their section names are `.handoff_params` and `.bitstream_buffer`. The first communicates image information; the second is temporary loading storage. They are real allocations even though they add no initialized data bytes to the ELF.

These are measurements of this BSP image, not universal FSBL sizes. The tagged `lscript.ld` defines the region limits. A custom build can use a different script, configuration or compiler. Review its program headers and map file again instead of copying the reference measurements into a new design.

## Initialization is a hardware dependency chain

`XFsbl_Initialize()` reaches system initialization, processor setup, memory preparation and board-specific work. `XFsbl_SystemInit()` calls `XFsbl_HookPsuInit()`. The default hook reaches the generated `psu_init()` flow, with separate handling when supported DDR self-refresh behavior is enabled.

A clock must be usable before software relies on a peripheral that uses it. Pins must have the correct multiplexing before UART output can reach the connector. DDR must be ready before later images can safely be copied there. This dependency order is why moving a custom register write earlier can break boot even if the value itself is correct.

A banner is evidence that execution reached a print path and that some console setup works. It does not establish the full DDR map or every interface. Conversely, no banner can mean a console mismatch rather than a processor that never entered the FSBL.

## Ownership changes after loading

The FSBL reads partitions, checks their metadata and loads them for their destination. For programmable logic, loading uses the configuration path. For processor software, the handoff must describe entry state as well as an address. Trusted Firmware-A (TF-A) then provides the resident EL3 runtime services in the common Linux flow.

The FSBL can set up a device so that the next stage can use it. Linux later needs its own accurate device-tree description and driver. An early GPIO or clock setting does not create a Linux device, express a dependency, or grant a second operating system permission to control the resource.

Some OCM contents also matter to restart flows. Do not treat all first-stage memory as free immediately after U-Boot appears. Check which restart design is enabled and which firmware data must survive. Resident TF-A storage is a separate lifetime and remains required for runtime calls.

## What to compare when hardware changes

Treat the hardware export, generated initialization, FSBL ELF and packaged `BOOT.BIN` as one traceable set. A correct source patch has no effect if the packaging step still uses an older ELF. The boot-image file records what was packaged; the build directory records what could have been packaged. They answer different questions.

For a failed new board build, compare the old and new generated initialization before changing the loader state machine. If stage 1 fails, investigate initialization and reset context. If stage 2 fails, investigate the selected boot device and headers. If one later partition fails, inspect that partition's source bytes, destination and protection settings. If stage 4 fails, inspect handoff metadata and the next-stage memory.

> [!NOTE]
> **Not run on the reference setup:** a rebuilt FSBL on physical ZCU106 hardware, DDR training after hardware changes, and warm-restart retention tests. The memory example above is a host inspection of the supplied ELF.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/{xfsbl_main.c,xfsbl_initialization.c,xfsbl_handoff.c,xfsbl_hooks.c,lscript.ld}`.
- `xilinx-zcu106-2024.1:pre-built/linux/images/zynqmp_fsbl.elf`, host ELF-header and program-header inspection.
- [AMD UG1137, 2024.1](https://docs.amd.com/r/2024.1-English/ug1137-zynq-ultrascale-mpsoc-swdev), first-stage boot and software-stack sections.

---

<sub>[Chapter index](README.md) · [FSBL Source Walkthrough](02-fsbl-source-walkthrough.md) →</sub>
