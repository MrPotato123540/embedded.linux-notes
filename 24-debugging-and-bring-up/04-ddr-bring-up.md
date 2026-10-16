# DDR Bring-Up and Memory Testing

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## Initialization, training and testing answer different questions

**Double Data Rate (DDR)** memory needs controller configuration, PHY configuration and a valid board-level electrical design. Initialization establishes the protocol state. Training adjusts supported timing relationships. A memory test checks selected read/write behavior after initialization.

A successful training status is not a complete memory-integrity test. A successful short memory test is not proof of margin across voltage, temperature, frequency and traffic patterns. Keep these claims separate so a passed early stage does not hide untested operating conditions.

The processing-system DDR controller and a PL-connected memory controller are different paths. The local ZCU106 hardware design includes a `vcu_ddr4_controller` in PL, while processing-system initialization has its own DDR functions. Passing a PS DDR test does not validate that PL memory path or its clocks.

## Trace configuration into the firmware

The local `project-spec/hw-description/psu_init.c` contains `psu_ddr_init_data()` and `psu_ddr_phybringup_data()`. Its initialization sequence calls these among the clock and peripheral setup stages. These generated settings reflect the hardware configuration that produced the export.

The inspected FSBL calls `XFsbl_HookPsuInit()`. Under `XPAR_DYNAMIC_DDR_ENABLED`, it also uses `XFsbl_DdrInit()` to obtain and apply memory information through the supported dynamic path. Do not assume every board uses either only fixed generated values or only dynamic discovery.

Preserve the XSA hash, generated initialization files, FSBL configuration and final ELF hash together. If the memory part or topology changes, rebuilding only Linux cannot update the DDR settings used before Linux starts.

## Capacity and topology must be correct

Controller settings include more than total capacity. Device width, ranks, row/column/bank organization, timing parameters and board topology affect address decoding and training. Two parts with equal capacity can still require different configuration.

An address-decoding error can make different CPU addresses refer to the same physical location. A simple test that writes and immediately reads one address may miss this aliasing. A better pattern writes distinct values to several locations before reading them back, including locations that differ in important address bits.

For an original example, write unique patterns to two test locations separated by a suspected address-bit boundary, then verify both. If writing the second changes the first, aliasing is a candidate. This is a proposed controlled test on a reserved region, not a command to write arbitrary live memory.

## Test only memory you own

A bootloader memory test writes the selected region. Linux, firmware, stacks, page tables, framebuffers and DMA buffers can occupy memory that appears unused from another component's view. Overwriting any of them can crash the system or silently corrupt data.

> [!WARNING]
> Memory-test writes are destructive to the selected RAM contents. Use a documented test region with no live owner, keep the executing code and stack outside it, and stop other masters that can access it. No such test was run in this revision.

A userspace memory tester normally exercises pages allocated to its process. That is useful but does not cover every physical address or early-boot access pattern. A low-level test can cover a different region but requires stronger ownership control. Neither should be presented as exhaustive without a defined coverage map.

## Cache can hide the memory you intended to test

A CPU can satisfy a read from cache rather than external DDR. Writing and immediately rereading a small region may mainly test cache behavior. A valid test strategy accounts for cache state, memory attributes and required maintenance.

Disabling caches changes timing and access patterns, so it is not automatically the strongest test. Combine controlled uncached or cache-maintained patterns with realistic cached workloads where appropriate. Include DMA and multi-master traffic if the product relies on those paths.

Use architectural barriers and supported cache operations correctly. Arbitrary delays do not guarantee that a write reached DDR. A debugger memory view may also use a different access path from the CPU, which can explain differences between what the debugger reads and what software observes.

## Pattern coverage and stress coverage differ

Walking-bit and address-dependent patterns can expose stuck data bits and address aliasing. Randomized patterns can broaden coverage. Burst, stride and concurrent-master patterns stress controller scheduling and signal activity differently.

A finite test suite cannot prove the absence of every memory fault. State tested ranges, pattern families, duration, rate, temperature and concurrent load. Keep reproducible seeds for randomized tests so a failure can be repeated.

If failures occur only at high load, separate CPU/cache defects, DDR errors and DMA coherency bugs. A stale DMA buffer caused by missing cache synchronization can look like bad RAM while the memory device is operating correctly. Compare a CPU-only test with a correctly mapped DMA test before changing DDR timings.

## ECC changes both setup and interpretation

**Error-correcting code (ECC)** can detect and correct certain memory errors when supported and configured. Memory may need initialization so stored data and ECC bits are consistent before normal checking. The FSBL source includes conditional DDR ECC initialization paths; their presence does not prove the reference image enables them.

Corrected errors and uncorrectable errors require different responses. Preserve address, syndrome and count information exposed by the supported driver. A growing corrected-error rate can indicate a margin problem even when applications still run. A zero counter can also mean the reporting path is inactive, so verify the monitoring configuration.

Do not inject errors or alter ECC controls on a live system without a specific validation procedure. The test can affect unrelated data and availability. Use the device documentation and a dedicated test environment for that work.

## Diagnose patterns, not only pass/fail

Failures at a consistent address bit suggest decoding or topology. Failures tied to a data bit suggest a lane or data-path issue. Temperature/frequency dependence suggests margin. Failures only after suspend or warm reset suggest retention and reinitialization sequencing.

The saved QEMU log reports memory ranges and available Linux memory, but emulation does not exercise physical DDR training or signal integrity. Treat it as address-map/software evidence only. A real board qualification needs measurements and repeated tests on representative hardware.

> [!NOTE]
> **Not run on the reference setup:** physical DDR training, destructive memory tests, ECC injection and environmental stress. Generated initialization and FSBL source were inspected without accessing target memory.

## References

- Inspected `xilinx-zcu106-2024.1:project-spec/hw-description/psu_init.c` and hardware design `config_bd.tcl`.
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_initialization.c`, DDR and ECC integration.
- AMD UG1085, DDR controller architecture; use the board's exact DDR component data sheet and exported configuration for timing and topology.

---

<sub>← [Custom Board Bring-Up](03-custom-board-bring-up.md) · [Chapter index](README.md) · [Common Failures and Fixes](05-common-failures.md) →</sub>
