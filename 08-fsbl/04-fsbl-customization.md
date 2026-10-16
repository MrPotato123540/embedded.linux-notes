# Customizing the FSBL

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot


## Place a change where its dependencies are ready

A First Stage Boot Loader (FSBL) customization often looks small: release a reset, configure a board switch, check a device identity or choose a hardware-initialization variant. Its position in the boot sequence can matter more than its line count.

Before adding code, write down what the operation needs. Does it require initialized DDR, an I2C clock, configured pins, a loaded bitstream or a running PMU firmware service? Then find a hook whose caller already guarantees those conditions. An operation that needs a programmable-logic register cannot safely run before the corresponding design exists and its interface clock and reset are ready.

The supported hook file is `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_hooks.c`. Read each hook together with its call site. The function name describes intent; the call site establishes actual order and error handling.

## Choose the narrowest hook

| Hook | Suitable purpose | Main boundary to respect |
| --- | --- | --- |
| `XFsbl_HookPsuInit()` | Select or extend processing-system initialization | Preserve required DDR retention and initialization behavior |
| `XFsbl_HookBeforeBSDownload()` | Prepare external conditions for bitstream loading | PL logic is not yet available |
| `XFsbl_HookAfterBSDownload()` | Check or complete work after configuration | A loaded design may still need clocks and reset release |
| `XFsbl_HookBeforeHandoff()` | Final board preparation before a transfer | May participate in early handoff as well as final handoff |
| `XFsbl_HookBeforeFallback()` | Record or prepare recovery actions | The system is already on an error path |

The bitstream hooks are conditional on included bitstream support. Adding code to a function that is excluded from the build cannot affect boot. Also, a boot image without a bitstream may never visit that path. Select the hook from the product's complete boot design, including recovery images.

## Worked design: checking a PL identity

Assume a custom design exposes a read-only identity register after its bitstream is loaded. This is a design example; it is not a measured ZCU106 register or a tested hook implementation.

The check needs four facts: the expected address range, the loaded design revision, the required clock state and the reset state. The address must come from the matching hardware export. The identity value must come from the IP specification. A value copied from an unrelated design is not a valid test.

The after-bitstream hook is a possible location only if the bus interface is already accessible. If the clock or reset depends on later setup, move the check or establish that dependency first. An AXI read to an unavailable target can hang or fault; a timeout around later software logic does not automatically make the bus access bounded.

The check should return a defined failure when it reads an unexpected identity. Returning success and printing a warning permits later software to use an incompatible register map. Decide whether recovery should load a different image or stop; that decision belongs to the boot policy.

## Preserve the existing initialization contract

The default `XFsbl_HookPsuInit()` does more than call a single generated function. The tagged source handles DDR I/O retention, supports a DDR self-refresh branch when enabled, checks the initialization status and completes a system-monitor setting.

Replacing the whole hook with a minimal custom function can silently remove those actions. Prefer a narrow patch with a clear reason for each changed step. If selecting between two generated initialization variants, keep each variant tied to a documented hardware configuration and a reliable board-identification method.

A board-identification read can itself need pins and clocks that the selected initialization is supposed to configure. Resolve that dependency explicitly. A circular plan—read an I2C device to choose the I2C initialization—cannot work without a common safe early setup.

## Return values belong to the caller's state machine

The FSBL expects status returns from hooks. Follow the call site's handling to decide what an error means. In the partition path, a failed hook can stop loading; in handoff, it can prevent the next image from starting. Do not replace a failure with success only to obtain a later banner.

`XFsbl_HookBeforeHandoff()` receives `EarlyHandoff`. An early handoff may allow another processor to start while the FSBL continues other work. Code that disables shared clocks, resets shared devices or invalidates shared buffers can break that concurrency.

Design the hook to be safe for every supported invocation. If it should run once, the state used to enforce that rule must itself have the correct lifetime across the relevant resets. A static variable initialized on a cold boot is not automatically a valid warm-restart protocol.

## Keep operations bounded and memory use visible

An unbounded polling loop can turn a recoverable hardware failure into a permanent silent boot stop. Where the hardware interface permits it, use a bounded wait and preserve the last observed status. The limit must be based on the device's timing requirements and available timer behavior, not an unexplained loop count.

Avoid large local buffers in a small first-stage stack. A scratch buffer also needs a lifetime: it must not overlap a loaded image, handoff data or an active transfer buffer. The reference FSBL uses a separate `.bitstream_buffer` allocation, showing why temporary storage is part of the memory plan.

Logging changes timing and code size. Print the minimum facts needed to distinguish failures: operation, expected state, observed state and return code. Large dumps before a watchdog deadline can create the failure you are trying to measure.

## Carry the patch through the PetaLinux build

Store the change as a tracked patch and include it from the project layer's FSBL recipe append. Confirm the active recipe path first: the local 2024.1 BSP uses `meta-xilinx-tools` to create the XSCT application and deploy its output. An override intended for the standalone make flow may not affect this application flow in the same way.

After building, inspect the ELF and map, then confirm that the boot package uses this ELF. A useful review artifact contains the patch, the relevant caller context, changed memory usage and an expected failure case. The design should state what happens when the peripheral is absent, not only when it works.

> [!NOTE]
> **Not run on the reference setup:** the illustrative PL identity check, custom hook failure injection and warm-reset behavior. The hook names, conditions and callers were checked in the tagged source.

## References

- [2024.1 FSBL hooks](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_fsbl/src/xfsbl_hooks.c).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/{xfsbl_partition_load.c,xfsbl_handoff.c,xfsbl_main.c}`.
- Local BSP: `meta-xilinx-tools/recipes-bsp/embeddedsw/fsbl-firmware_2024.1.bbappend`.

---

<sub>← [Building the FSBL](03-building-the-fsbl.md) · [Chapter index](README.md) · [FSBL Debugging](05-fsbl-debugging.md) →</sub>
