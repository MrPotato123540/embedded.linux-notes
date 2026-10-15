# PMU Firmware Architecture and Source

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot

## Framework structure

PMU firmware separates its core framework from modules that provide services. Initialization registers modules and their callbacks. Events, IPI messages and scheduled work dispatch into the relevant handlers.

| Source area | What to follow |
| --- | --- |
| `xpfw_core*` | Framework initialization and dispatch |
| `xpfw_module*` | Module creation and callbacks |
| `pm_*` | Platform-management nodes, requests and state |
| Error-management code | Error-source handling and configured actions |
| Scheduler/watchdog support | Timed work and supervision |

Build flags decide which modules and features exist. A source file in the repository does not prove its code is linked into the current firmware.

## Reading a request path

Find the incoming message handler, validate its argument decoding, then follow the operation into the platform-management state machine. Check the caller's permissions and the resource's current state before examining the register write.

Do not block a shared handler indefinitely while waiting for external hardware. A long custom operation can delay unrelated power or error requests. Use bounded work and a clear error result.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/xpfw_core.c`, `xpfw_module.c`
- Locally inspected `pm_core.c`, `pm_common.h`, `pm_defs.h`

---

<sub>← [PMU Overview](01-pmu-overview.md) · [Chapter index](README.md) · [EEMI and Platform Management](03-eemi-and-platform-management.md) →</sub>
