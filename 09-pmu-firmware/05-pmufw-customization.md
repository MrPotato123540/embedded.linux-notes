# Customizing PMU Firmware

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot

## Build-time customization

PMU firmware features are controlled by source configuration and compiler definitions. Flags such as `ENABLE_EM`, `ENABLE_SCHEDULER`, `ENABLE_RECOVERY` and `ENABLE_ESCALATION` select different support paths. Check their dependencies in the pinned source rather than enabling names independently.

In a PetaLinux build, maintain changes through the selected `pmu-firmware` recipe and append files. Inspect how that recipe passes `YAML_COMPILER_FLAGS` and other build arguments before overriding them. Replacing a whole variable can accidentally remove required defaults.

## Custom modules

A module should have a narrow responsibility, bounded callbacks and explicit error handling. Register the callbacks through the framework and document which IPI or event sources it owns. Avoid hidden dependencies on Linux startup order.

PMU memory is limited. Check the ELF's sections, stack needs and link map after adding features. File size alone does not show runtime memory use. Test normal management traffic while the custom feature runs.

> [!NOTE]
> **Not run on the reference setup:** a customized PMU firmware build, footprint measurement and stress test.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/xpfw_config.h`, `xpfw_default.h`
- `meta-xilinx-tools@rel-v2024.1`, PMU firmware recipes

---

<sub>← [Communicating With the PMU](04-communicating-with-the-pmu.md) · [Chapter index](README.md) · [Error Management, Recovery and Watchdogs](06-error-management-and-watchdogs.md) →</sub>
