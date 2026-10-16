# Programming the RPU

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## A firmware image includes a memory contract

An R5 executable is more than application instructions. Its linker script places exception vectors, code, initialized data, zero-initialized data, stacks and heap. Startup code establishes the processor state needed before C code runs. The platform description supplies peripheral addresses, interrupts and clocks.

The hardware export, selected R5 core, operating mode and software domain must agree. A standalone application built for one memory map can still produce a valid executable file when that map is wrong for the actual loader. A successful link proves internal symbol placement, not safe placement in the complete ZynqMP system.

In PetaLinux 2024.1, distinguish an application built through the embedded software tools from a firmware image managed by Linux remoteproc. Both can target the RPU, but their startup ownership and packaging differ. Do not start the same core from a boot partition and then let Linux overwrite its memory as if it were stopped.

## Processor addresses and system addresses differ

The inspected Linux R5 driver contains explicit tightly coupled memory (**TCM**) mappings. In split mode, the R5-0 ATCM bank maps system address `0xFFE00000` to remote device address `0x00000000`, size `0x10000`. Its BTCM bank maps `0xFFE20000` to device address `0x00020000`, also size `0x10000`.

| Split-mode bank | System address | R5 device address | Size |
| --- | ---: | ---: | ---: |
| R5-0 ATCM | `0xFFE00000` | `0x00000000` | 64 KiB |
| R5-0 BTCM | `0xFFE20000` | `0x00020000` | 64 KiB |
| R5-1 ATCM | `0xFFE90000` | `0x00000000` | 64 KiB |
| R5-1 BTCM | `0xFFEB0000` | `0x00020000` | 64 KiB |

These are source-defined mappings in `zynqmp_tcm_banks_split[]`, not measured board values. The lockstep table combines banks into two 128-KiB mappings. The Linux loader uses registered carveouts to translate a remote device address into a host-accessible mapping. [Pinned mapping source](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/remoteproc/xlnx_r5_remoteproc.c).

This explains why an ELF segment linked near R5 address zero is not a request to overwrite Linux physical address zero. It also explains why replacing R5 addresses with APU-visible addresses in a linker script can break loading. Always label the address space in memory reviews.

## Review program headers, not only section names

An **Executable and Linkable Format (ELF)** file describes loadable segments through program headers. A segment can have a larger memory size than file size; the extra range commonly includes zero-initialized storage. A loader must account for the full memory range.

The Linux implementation in `remoteproc_elf_loader.c` walks loadable segments, translates their device addresses, copies file-backed data and clears the remaining memory. It checks size relationships and whether the segment fits an available mapping. The section table also matters for finding the resource table, but it is not a substitute for the load map.

For an original example, a segment with 20 KiB of file data and 28 KiB of memory needs the entire 28 KiB range reserved. Placing another object in the last 8 KiB because those bytes are absent from the file creates a runtime overlap. Add stacks, heap limits and any shared buffers to the same review.

## Linker choices affect determinism and capacity

TCM is useful for bounded local access, but capacity is limited. Put critical code and data there only after measuring their size. Large libraries, printf formatting and deep call paths can grow code or stack use unexpectedly. A firmware that fits at link time can still overflow its runtime stack.

DDR provides more space but introduces a shared-memory path and cache policy. If firmware executes from DDR, the loader, memory reservation and cache configuration must all support that layout. Treat code placement and shared message placement separately: their access patterns and ownership differ.

Use a linker map to review placement by object and section. Preserve it with the ELF and build configuration. If a new library moves a resource table or expands a stack region, that is a system integration change even when the application source looks small.

## Interrupts and shared devices need explicit ownership

The R5 application initializes only the hardware it owns. If Linux controls a device, another initialization sequence from the R5 can reset it or change shared clocks. The reverse is also possible during Linux probe, suspend or shutdown.

Interrupt IDs, trigger behavior and controller configuration must match the hardware export and software platform. An interrupt handler should acknowledge the correct source and leave long work to an appropriate execution context. A handler that clears only the controller state while leaving the peripheral source asserted can retrigger continuously.

For communication, keep firmware startup messages separate from protocol readiness. Reaching `main()` proves that some execution works. It does not prove that the resource table, vrings, mailbox and Linux endpoint agree. Publish readiness only after required buffers and transport state are initialized.

## Loading and stopping are system actions

Remoteproc startup requests power and memory resources, loads the image, prepares communication resources and starts the processor through platform operations. In the pinned driver, `zynqmp_r5_rproc_prepare()`, `zynqmp_r5_rproc_start()` and the matching teardown functions show this lifecycle.

Stopping a processor while it controls a peripheral can leave a DMA engine active or an output in its last state. The firmware and Linux service need a shutdown protocol where that matters. A core reset does not automatically prove that every independent bus master stopped accessing shared memory.

Similarly, changing the firmware filename does not prove a new image is running. Keep the loaded image hash, protocol version and remote-reported build identity together. Report both the requested firmware and the observed running version during a release test.

## Diagnose the first missing proof

A load-range error points to ELF addresses or carveout definitions. A start request that fails before execution points to platform permissions, RPU mode or resource preparation. A core that starts but faults quickly suggests vectors, stack, runtime initialization or invalid peripheral access.

If a simple local application works but RPMsg does not, avoid rewriting the linker layout without evidence. Compare the communication-specific sections and shared-memory contract first. If failures appear only after adding logging, check stack growth and timing before assuming the mailbox is unreliable.

> [!NOTE]
> **Not run on the reference setup:** R5 compilation, firmware loading, stopping and interrupt tests. No target processor was reset. TCM mappings and ELF loader behavior were checked in the pinned 2024.1 kernel source.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/remoteproc/{xlnx_r5_remoteproc,remoteproc_elf_loader}.c`, inspected locally.
- [AMD embedded software, 2024.1](https://github.com/Xilinx/embeddedsw/tree/xilinx_v2024.1), standalone startup and processor support.
- [remoteproc and RPMsg](03-remoteproc-and-rpmsg.md), resource tables and runtime transport.

---

<sub>← [AMP vs. SMP Concepts](01-amp-concepts.md) · [Chapter index](README.md) · [remoteproc and RPMsg](03-remoteproc-and-rpmsg.md) →</sub>
