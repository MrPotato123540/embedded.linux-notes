# PMU Firmware Architecture and Source

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot


## A small event-driven firmware core

PMU firmware organizes work around a core, registered modules, hardware events, inter-processor interrupts (IPIs) and scheduled tasks. A module is a firmware object with callbacks. It is not a dynamically loaded Linux module, and the scheduler is not a general operating-system process scheduler.

Start at `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/xpfw_main.c`. After early setup and version printing, `main()` clears the previous firmware-error indication, registers an assert callback and calls `XPfw_CoreInit(0U)`. It then calls `XPfw_UserStartUp()` to add modules, handlers and tasks.

Next, `XPfw_CoreConfigure()` invokes module configuration handlers. Only after these steps does `XPfw_CoreLoop()` enter the long-running service loop. This order gives custom code a registration phase and a configuration phase. Hardware work that assumes all modules exist should not be placed before their registration.

## The module record is the routing point

`XPfw_CoreCreateMod()` allocates a record from the core's fixed module list. It returns `NULL` when the list is full or the core is unavailable. A customization must check that result before registering callbacks. Ignoring it can turn a configuration error into an invalid pointer access during startup.

The core exposes registration functions for configuration, event and IPI handlers. The configuration callback receives module context and configuration data. The event callback receives an event identity. The IPI callback receives channel information, the source mask, payload and length.

These arguments are part of the module contract. The source mask matters because several processors can send requests. The payload length matters because a service cannot safely read fields that were not supplied. A correct notification route does not prove that the message content is valid.

## How an IPI reaches a module

`XPfw_CoreDispatchIpi()` examines pending sources and reads message data through the IPI support layer. In the inspected source, it compares each module's registered `IpiId` with the upper 16 bits of the first payload word. Matching modules with a handler receive the request.

That field is a software routing identifier. It is different from the hardware interrupt channel and different from a command identifier inside the selected service. Confusing these three identities is a common reason for a message that reaches the PMU but never reaches the intended handler.

The power-management module registers its IPI handler with ID 0 in `xpfw_mod_pm.c`. Its `PmIpiHandler()` passes management work to `XPfw_PmIpiHandler()`. This is a concrete route from core dispatch into the management implementation, rather than a claim that any arbitrary IPI payload is a valid power request.

## Hardware events use a separate route

A module can register for selected events through `XPfw_CoreRegisterEvent()`. The PM module registers wake and sleep events for processor-related behavior. The error-management module registers error events when that feature is compiled in.

Event registration gives the core a list of interested handlers. An event can describe a hardware state change without carrying a full application request. The handler must read the relevant status under the source's rules, then perform the required action and acknowledgement.

Do not clear a shared status register before preserving the evidence needed by the handler or another owner. Also, clearing an event indication does not necessarily remove the hardware condition that caused it. A level condition can immediately assert again.

## Scheduled work has bounded execution needs

`XPfw_CoreLoop()` starts the scheduler when `ENABLE_SCHEDULER` is present. It enables the required tick interrupt after a successful start. Under `SLEEP_WHEN_IDLE`, the MicroBlaze can sleep until an interrupt arrives, then the loop processes scheduled work when enabled.

This architecture needs short, bounded callbacks. A callback that waits forever for another processor can prevent later scheduled work from running. It can also delay a watchdog refresh or make request latency much larger than expected.

A periodic task should perform one bounded unit of work and return. If a longer operation needs several phases, maintain an explicit state and continue on later events or ticks. The state must describe what owns each buffer and what happens if the external device never responds.

## Read feature guards as part of the implementation

The tagged `xpfw_config.h` enables the PM module and scheduler by default through their `_VAL` settings. Error management, recovery and the PMU watchdog have separate switches and are not all enabled by those two defaults.

Several module files provide an empty initialization function when their feature is excluded. A successful link can therefore contain a call such as `ModEmInit()` without an active error-management implementation. Check the preprocessor path and effective flags, not only the presence of the symbol name in source.

The local XSCT append adds debug flags and `-DENABLE_SCHEDULER`. It can differ from the standalone recipe and from a user-modified application. Capture resolved flags when diagnosing which modules are active in a deployed image.

## A source-reading example: a periodic watchdog refresh

`xpfw_mod_wdt.c` creates a module, installs its configuration handler and sets up the watchdog. Initialization schedules `XPfw_WdtRestart()` through `XPfw_CoreScheduleTask()`. The callback refreshes the watchdog through its driver instance.

The chain is therefore registration → configuration → scheduler task → refresh callback. If the watchdog later expires, inspect each boundary. Was the module included? Did configuration succeed? Did task registration succeed? Did the core keep processing tasks? A watchdog register value alone does not answer these software questions.

This example also shows why a custom blocking task can affect a seemingly unrelated module. The modules share a firmware execution environment even when their services have different names.

## References

- [PMU firmware main](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_pmufw/src/xpfw_main.c).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/{xpfw_core.c,xpfw_module.c,xpfw_ipi_manager.c,xpfw_mod_pm.c,xpfw_mod_em.c,xpfw_mod_wdt.c,xpfw_config.h}`.
- Local BSP: `meta-xilinx-tools/recipes-bsp/embeddedsw/pmu-firmware_2024.1.bbappend`.

This walkthrough is source inspection. No custom module or scheduler fault was executed on the target.

---

<sub>← [PMU Overview](01-pmu-overview.md) · [Chapter index](README.md) · [EEMI and Platform Management](03-eemi-and-platform-management.md) →</sub>
