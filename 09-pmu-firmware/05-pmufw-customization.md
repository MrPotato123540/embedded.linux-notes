# Customizing PMU Firmware

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot


## Decide whether the PMU is the right owner

PMU firmware is appropriate for system-management work that must cooperate with power, reset or platform events. It is not a convenient place for arbitrary application processing. A long custom calculation can delay other firmware work, and a bug can affect more than one operating system.

Begin with the required lifetime. Must the function work before Linux starts, while an A53 subsystem restarts, or while another processor sleeps? Which hardware and memory remain available in those states? A service that depends on Linux-owned DDR data may fail exactly when its management role is most important.

Write down the allowed callers, controlled resources, failure action and execution-time limit. These become the service contract and the basis for review.

## Extend the module model

The tagged PMU core offers module creation plus configuration, event and IPI callback registration. `XPfw_UserStartUp()` is the startup integration point used by `xpfw_main.c` before core configuration.

A custom module needs a successful `XPfw_CoreCreateMod()` result, then successful callback registration. The fixed module list can run out of capacity. Propagate that failure visibly instead of leaving a partly registered service.

The configuration handler should establish initial state. The event handler should react to registered platform events. The IPI handler should validate and dispatch requests from other processors. A scheduled callback should perform bounded periodic work. Keeping these roles clear makes it easier to reason about which operations can run before or during another event.

## Worked design: a bounded health sampler

Assume a custom product needs the PMU to sample a board-health input and report the latest state. This is a design example, not an implemented or tested ZCU106 module.

The configuration phase checks that the input hardware is available and initializes the stored state to “not sampled.” A periodic task takes one bounded sample, records the result and returns. An IPI request reads the latest stored sample together with its age and status. It does not start an unbounded measurement while the caller waits.

This split matters when the sensor fails. The periodic task records a timeout or invalid sample without blocking every other service. A caller can distinguish a fresh healthy value from stale data. Returning the last good value with no age information would hide the failed measurement path.

The state also needs concurrency rules. If an interrupt handler can read or modify it while a task updates it, use the core's suitable synchronization approach and keep the critical section short. A multiword sample must not be exposed half-updated.

## Feature switches form a dependency graph

`xpfw_config.h` defines features such as `ENABLE_PM`, `ENABLE_EM`, `ENABLE_SCHEDULER`, `ENABLE_RECOVERY` and `ENABLE_WDT`, often through `_VAL` settings. They are not all synonyms for “enable PMU support.” Each includes a different behavior.

The source also contains feature dependencies. For example, some runtime features enable related module or IOCTL support. DDR-dependent suspend options reject a design without the required DDR component. Check the full preprocessor path when changing a flag.

Do not assume that defining a macro to zero disables code guarded by `#ifdef`. The tested condition can be the existence of the macro rather than its numerical value. Follow the pattern used by the configuration header and confirm the effective compile command.

## The PetaLinux 2024.1 build path

The base PMU recipe lives under `meta-xilinx/meta-xilinx-standalone/recipes-bsp/embeddedsw`. It selects the PMU application and MicroBlaze environment. The local `meta-xilinx-tools` append inherits `xsctapp` and `xsctyaml`, selects `ZynqMP PMU Firmware`, and targets `psu_pmu`.

That append adds `-DDEBUG_MODE -DXPFW_DEBUG_DETAILED` through its debug flags and appends `-DENABLE_SCHEDULER` to the compiler flags. It deploys both ELF and binary output from the generated application. These settings can differ from reading the upstream header alone.

Carry source changes in tracked patches and metadata. Do not rely on edits inside the generated XSCT application directory. A clean rebuild can replace it, and a colleague needs the same inputs to recreate the firmware.

## Check code size and runtime storage separately

The supplied `pmufw.elf` is a MicroBlaze executable. A replacement must use the correct processor configuration and linker memory map. Large tables, logging and library calls can consume limited firmware storage even when the source change looks small.

A successful link checks declared region limits, but not every dynamic stack path. Avoid large local arrays and recursion in a management callback. Shared buffers need clear ownership, address validity and cache behavior, especially when an A53 client supplies them.

Adding detailed prints also changes service latency. For a watchdog-sensitive path, measure the worst relevant operation with its real logging level. A debug-only success does not establish that the release image has equivalent timing, and a debug-only failure can come from added delay.

## Package and test a complete firmware set

PMUFW cooperates with FSBL, TF-A and Linux. Keep these versions together when changing a custom request or power behavior. A caller update without the matching handler can produce unsupported-operation errors or, worse, a different interpretation of the same payload.

The minimum test plan includes startup with the module enabled, a valid request, an invalid length, an unsupported operation, a missing external device and repeated requests. For a service that must survive A53 restart, test that restart while preserving the PMU's intended state.

> [!NOTE]
> **Not run on the reference setup:** the health-sampler example, a custom PMU build and cross-processor restart tests. The module interfaces, feature guards and 2024.1 recipes were inspected; no custom firmware success is claimed.

## References

- [2024.1 PMU configuration](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_pmufw/src/xpfw_config.h).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/{xpfw_main.c,xpfw_core.c}`.
- Local BSP: `meta-xilinx-tools/recipes-bsp/embeddedsw/pmu-firmware_2024.1.bbappend` and `meta-xilinx-standalone/recipes-bsp/embeddedsw/pmu-firmware.inc`.

---

<sub>← [Communicating With the PMU](04-communicating-with-the-pmu.md) · [Chapter index](README.md) · [Error Management, Recovery and Watchdogs](06-error-management-and-watchdogs.md) →</sub>
