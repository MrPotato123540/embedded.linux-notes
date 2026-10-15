# FSBL Source Walkthrough

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot

## Source map

| File | Main responsibility |
| --- | --- |
| `xfsbl_main.c` | Stage machine and top-level error flow |
| `xfsbl_initialization.c` | Processor and platform initialization |
| `xfsbl_partition_load.c` | Partition processing and loading |
| `xfsbl_image_header.c` | Image-header interpretation |
| `xfsbl_handoff.c` | Handoff data and next-stage transfer |
| `xfsbl_board.c` | Board-specific operations |
| `xfsbl_hooks.c` | Supported customization hooks |

The inspected main source moves through `XFSBL_STAGE1` to `XFSBL_STAGE4`, with an error path. Follow the assigned next stage and status return rather than reading the file as one straight sequence. Early handoff can change the path.

## Generated initialization

`psu_init` comes from the hardware design flow. It is responsible for settings such as DDR and processing-system clocks. Keep the generated source tied to the XSA revision. Hand-editing it without preserving the change in the hardware/build flow makes regeneration unsafe.

## Following a failure

Start from the printed status or failing stage. Follow the function that returned the error, then inspect its inputs: boot headers, destination address or peripheral status. For handoff failures, compare the FSBL's recorded destination with the ELF entry and BIF attributes.

## References

- Locally inspected 2024.1 copies of `xfsbl_main.c`, `xfsbl_initialization.c`, `xfsbl_partition_load.c`, `xfsbl_handoff.c`
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/`

---

<sub>← [FSBL Overview](01-fsbl-overview.md) · [Chapter index](README.md) · [Building the FSBL](03-building-the-fsbl.md) →</sub>
