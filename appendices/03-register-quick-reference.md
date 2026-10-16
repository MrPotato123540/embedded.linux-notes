# Register Quick Reference

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[Appendices](README.md)** · Appendices

## Selected register addresses

These addresses are for the ZynqMP system view. Check processor access, security permissions and register semantics before reading. The table is a navigation aid, not a programming sequence.

| Address | Register | Main use | Source cross-reference |
| --- | --- | --- | --- |
| `0xFF5E0200` | `CRL_APB.BOOT_MODE_USER` | Software-visible boot-mode selection | UG1087, CRL_APB `BOOT_MODE_USER`; FSBL `CRL_APB_BOOT_MODE_USER` |
| `0xFF5E0220` | `CRL_APB.RESET_REASON` | Recorded reset causes | UG1087, CRL_APB `RESET_REASON`; FSBL `CRL_APB_RESET_REASON` |
| `0xFFCA0010` | `CSU.CSU_MULTI_BOOT` | Multiboot selection state | UG1087, CSU `CSU_MULTI_BOOT`; FSBL `CSU_CSU_MULTI_BOOT` |

The addresses were cross-checked against the pinned FSBL header and the existing architecture notes. Register access semantics and complete bit definitions must be checked in UG1087 before a write. The multiboot value is interpreted by the boot flow; it is not a universal byte offset.

Error diagnosis also uses CSU/PMU status registers. Select the documented register for the failing stage instead of treating one generic “error register” as sufficient. Save values before reset or software clears them.

> [!NOTE]
> **Not run on the reference setup:** a new physical read/write validation of this table. Existing QEMU observations do not prove silicon reset behavior.

## Derive an address before interpreting a value

The pinned FSBL header defines `CRL_APB_BASEADDR` as `0xFF5E0000` and `CSU_BASEADDR` as `0xFFCA0000`. A register address is the selected block base plus its byte offset. For example, `0xFF5E0000 + 0x200 = 0xFF5E0200` locates `BOOT_MODE_USER` in the system address view.

That calculation is useful when comparing a manual, a C macro and a device-tree resource. It does not authorize every processor to access the address. Security policy, power state and the processor's mapping still apply. A Linux driver normally maps the described resource and uses an offset from its mapped base; it does not dereference the system physical address as an ordinary pointer.

Keep width and byte order explicit. A register's documented access width is not necessarily the width of a C pointer on an AArch64 processor. The platform's MMIO accessors express I/O semantics that a plain memory load/store does not fully replace.

## Selected masks from the pinned FSBL header

| Register | Source macro | Mask | Limited interpretation |
| --- | --- | --- | --- |
| `BOOT_MODE_USER` | `CRL_APB_BOOT_MODE_USER_BOOT_MODE_MASK` | `0x0000000F` | Low boot-mode field used by this FSBL path |
| `RESET_REASON` | `CRL_APB_RESET_REASON_PMU_SYS_RESET_MASK` | `0x00000004` | PMU system-reset indication tested by the FSBL |
| `RESET_REASON` | `CRL_APB_RESET_REASON_PSONLY_RESET_REQ_MASK` | `0x00000008` | PS-only reset-request indication tested by the FSBL |

These are selected source definitions, not a complete register specification. The low-field mask is not permission to ignore every other field in `BOOT_MODE_USER`. Alternative-mode controls and reset behavior must be interpreted from UG1087 and the boot flow.

For a purely illustrative value `0x0000000C`, both listed reset masks test nonzero: `0x0C & 0x04 = 0x04` and `0x0C & 0x08 = 0x08`. This demonstrates mask arithmetic only. It is not a captured register value or a claim that this combination occurs on the reference board.

Do not compare an entire status register to one mask when several bits may be set. Conversely, do not infer a complete reset history from only these two masks. Other fields and software clearing behavior can change the interpretation.

## Read, write and acknowledge are different operations

A normal read/write control register may permit read-modify-write, subject to reserved-bit rules. A write-one-to-clear status register behaves differently: writing back all the bits you just read can acknowledge every pending status bit. A read-to-clear register changes state even without a write.

Before accessing a register, identify its documented access type, reset value, valid width, reserved fields and side effects. Also identify who else owns it. A debugger changing a clock/reset control while Linux or PMU firmware manages the same resource can create a race outside either component's normal state machine.

This appendix does not classify the three selected registers as interchangeable examples of those access types. Consult each named UG1087 register page for its exact behavior. The distinction is the reason a generic “read value, OR bit, write value” recipe is unsafe as a universal register procedure.

## Register address, file offset and bus address

The boot-image format uses some offsets measured in 32-bit words. A value in such a field must be multiplied by four before it becomes a byte offset in `BOOT.BIN`. That result is still a file offset, not the destination address where the partition executes.

An ELF separately describes loadable memory ranges and an entry point. Device-tree `reg` values describe resources according to parent cell counts and address translation. DMA APIs return addresses for a device's view. These numbers can look similar while belonging to different spaces.

For example, the reference BL31 entry `0xFFFEA000` is a runtime address. Its boot-container partition offset is a location within a file. Comparing the two directly to detect overlap is meaningless. Compare file ranges with file ranges and runtime allocations with runtime allocations, including each allocation's lifetime.

## Boot mode and multiboot need context

The visible boot-mode field participates in selecting the boot path, but software overrides and reset history affect the full decision. Capture the reset context and the earliest software interpretation along with a register value. A later Linux read may observe state after firmware has changed it.

`CSU_MULTI_BOOT` is also interpreted by the boot flow. Its value is not a universal byte address for every storage medium. See [multiboot and fallback](../06-boot-sequence/13-multiboot-and-fallback.md) for the medium-specific relationship and recovery behavior.

If a device repeatedly falls back, preserve the failing image location, first error and resulting multiboot state. Resetting immediately and reporting only the eventual working image loses evidence about why the first candidate was rejected.

## Interrupt numbers are another translation problem

A device-tree interrupt specifier is not generally identical to the Linux IRQ number printed in diagnostics. A controller binding describes the cells and numbering domain. The interrupt controller and Linux IRQ domain translate that information into the runtime interrupt.

For a GIC-backed device, check the binding's interrupt type and number conventions before comparing a schematic, device tree and `/proc/interrupts`. A mismatch can leave a driver fully probed but waiting forever for completion. [Interrupts and the GIC](../03-zynqmp-architecture/08-interrupts-and-gic.md) explains the actual numbering rules.

## A useful register capture includes state

Record who read the register, when it was read relative to reset, whether the block was powered and which software owned it. For a repeated test, use the same ordering so observations are comparable. Read status before an operation that may clear or overwrite it, when the documented semantics permit that read.

A value of zero is not automatically “healthy.” It may mean a cleared status, a reset block, the wrong address or a failed access reported through another channel. Compare it with a known allowed operation and the controlling firmware's log.

The addresses and masks above were checked against the 2024.1 source. No new physical register reads or writes were performed. That boundary preserves the difference between a correct reference calculation and a measured board state.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_hw.h`
- UG1087 Zynq UltraScale+ Devices Register Reference, named register pages
- [Memory map](../03-zynqmp-architecture/04-memory-map.md) and [reset behavior](../03-zynqmp-architecture/07-clocks-power-and-reset.md)

---

<sub>← [Command Cheat Sheets](02-command-cheatsheets.md) · [Chapter index](README.md) · [References and Sources](04-references.md) →</sub>
