# JTAG, XSDB and XSCT

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## The debugger changes the system it observes

**Joint Test Action Group (JTAG)** names the test/debug access interface used by the tools. The **Xilinx System Debugger (XSDB)** provides target discovery, processor control, memory access and other debug operations. **Xilinx Software Command-Line Tool (XSCT)** also includes software-development workflows. Tool names alone do not describe which target is selected or whether an operation is read-only.

A ZynqMP connection can expose several processors and debug components. Selecting an A53, an R5 or the PMU changes the meaning of subsequent processor operations. A target number can change across connections, so a script should identify the intended component by stable properties and verify its selection.

The hardware server provides the host connection to the probe/target. A successful server connection proves transport access to some debug infrastructure. It does not prove that DDR is initialized, a processor is running valid code or the board's boot image is correct.

## Establish a state record before intervention

Record board revision, power state, boot mode, tool version, hardware export and the last UART output. Determine whether the board booted normally, is held in reset or was already modified by an earlier debugger session. A warm state can hide missing initialization that fails on cold boot.

For each planned operation, identify its effect: inspect, halt, resume, reset, load memory, execute initialization or program PL. Loading an ELF writes its segments to memory. Running a generated initialization script can change clocks, resets and memory-controller state. These are not harmless forms of inspection.

A useful debugging session has one owner of processor and device state. If another tool or an automated service resets the same board, register observations and breakpoints lose their meaning. Preserve a transcript with the selected target and action order.

## Use symbols from the exact binary

An ELF supplies symbols and address information for source-level debugging. The symbols must match the bytes actually loaded. A stale ELF with the same filename can place breakpoints at the wrong instructions or show misleading source lines.

Keep the executable hash, build flags and linker map with the symbol file. Optimization can inline functions, remove variables and reorder instructions. A source line may therefore correspond to several machine locations or none. Inspect the disassembly and program counter when source-level stepping appears surprising.

For a crash, identify the active exception level and translation state before interpreting addresses. A CPU virtual address, physical address and device register address are not interchangeable. The current page tables and exception context determine how a memory access is translated.

## Halting one core does not halt every actor

Linux can run on several A53 cores. Halting one core can leave other CPUs, DMA engines and the RPU active. A stopped CPU may hold a lock needed by the others. The resulting system-wide stall is then caused by the debugger rather than the original bug.

External peripherals also continue according to their own clocks. A watchdog may reset the system while the CPU is halted unless the platform explicitly handles debug behavior. A DMA engine can continue changing a buffer while you inspect it, producing a snapshot that never existed as one coherent state.

Choose whether the investigation needs one-core halt, coordinated halt or nonintrusive tracing. Each has different effects. Record which components remain active so a register or memory dump can be interpreted correctly.

## Generated initialization must match the board

The local BSP contains `project-spec/hw-description/psu_init.c` and `psu_init.tcl`. They come from the hardware configuration and include processing-system initialization. The C source contains `psu_ddr_init_data()` and `psu_ddr_phybringup_data()` among other stages.

Those files are not universal ZynqMP startup scripts. DDR part, timing, clocks and pin configuration depend on the board. Running a ZCU106 initialization sequence on a custom board can create invalid settings even if the SoC family matches.

Do not rerun DDR initialization while Linux or another processor uses DDR. Reprogramming the memory controller can invalidate the execution environment immediately. For an early-boot investigation, use a deliberate reset/start sequence with a known execution region and a clear owner of initialization.

## Follow a handoff failure through evidence

Consider an original case where FSBL prints a final message but U-Boot does not appear. First determine which payload should run next from the BIF and firmware handoff design. Check the loaded ELF entry, destination processor and exception/security state. Then inspect whether execution reached that entry with the matching symbols.

If the PC never reaches the intended entry, investigate loading or handoff. If it reaches the entry and immediately faults, inspect initial register state, stack, memory mapping and required firmware services. If execution progresses but UART stays silent, inspect console selection and clock/pin configuration instead of assuming the CPU stopped.

A breakpoint on an early entry point can alter timing enough to hide a race. Confirm the conclusion with a less intrusive observation or repeatable trace where possible. Debugger-assisted execution and unattended boot are separate validation modes.

## Treat register reads as device operations

Some registers clear status on read, consume FIFO data or have other side effects. A bulk register dump can change the failure you are trying to diagnose. Use the hardware reference manual to identify safe status registers and required access widths.

The same caution applies to writes suggested by old troubleshooting notes. A literal address/value pair can depend on silicon revision, current power state and a previous sequence. Prefer the release's driver or firmware interface when it already owns that resource.

A successful manual register adjustment can be diagnostic evidence, but the final fix belongs in the correct initialization or driver path. Otherwise the product depends on an undocumented debugger step.

## Save enough to reproduce the conclusion

Retain selected target identity, reset sequence, loaded artifact hashes, breakpoints, register context and UART output. State whether the result came from cold boot, warm reset or an already initialized board. If you changed state, record the change before interpreting later observations.

> [!NOTE]
> **Not run on the reference setup:** physical JTAG attachment, target halt/reset, ELF download and register access. Generated initialization files were inspected only. No debugger command is presented as executed against hardware.

## References

- AMD UG1400 (2024.1), XSCT/XSDB target control and debugging reference; use installed 2024.1 command help for exact syntax.
- Inspected `xilinx-zcu106-2024.1:project-spec/hw-description/{psu_init.c,psu_init.tcl}`.
- [Exception levels](../03-zynqmp-architecture/10-exception-levels-and-trustzone.md), processor-state context; [DDR bring-up](04-ddr-bring-up.md), initialization constraints.

---

<sub>[Chapter index](README.md) · [QEMU Emulation](02-qemu-emulation.md) →</sub>
