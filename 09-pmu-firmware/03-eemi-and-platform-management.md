# EEMI and Platform Management

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot


## Requests express requirements and ownership

The **Embedded Energy Management Interface (EEMI)** gives software a platform-management request model. A client identifies a resource, describes the operation or requirement, and receives a result. Firmware checks the request within the system's resource policy.

This is more than remote register access. A shared device can have multiple users, a power transition can depend on child resources, and a reset can affect another processor. The request interface lets firmware account for these relationships before changing hardware state.

In the pinned PMU firmware, `pm_core.c` dispatches management operations and includes `PmRequestNode()`, `PmReleaseNode()` and `PmSetRequirement()`. The names expose a lifetime model: request use, adjust the requirement if needed, and release use when finished.

## Work through one shared-resource example

Assume two permitted masters need a resource represented by one managed node. This is a reasoning example, not a measured board transaction. Master A requests it for active use. Master B later requests it too. The firmware tracks their requirements under the configured policy.

When A releases the node, the correct result is not necessarily a powered-off device. B can still require it. The final hardware state follows the remaining requirements and supported state transitions. A driver that expects every release call to remove power misunderstands the interface.

Now suppose B was never permitted to use the node. Its request should fail. The driver must stop or unwind its probe path instead of continuing with register access. Replacing the failed request with a raw clock or reset write bypasses the management model and can break the permitted owner's work.

The exact permissions come from the platform configuration and firmware behavior. A node number copied from another release or device family is not a portable resource identity.

## CPU management and device management are related but distinct

Linux uses the **Power State Coordination Interface (PSCI)** for standard CPU power operations. On the common ZynqMP stack, Trusted Firmware-A presents that interface at EL3 and cooperates with platform management for the required transitions.

Clock, reset, pin and device-resource operations can use ZynqMP-specific management calls. They have different identifiers and argument formats from PSCI. A working PSCI version query does not validate every device-management operation.

The same principle applies to call transport. The saved device tree selects `method = "smc"` for the ZynqMP firmware interface. A virtualized guest can need a Hypervisor Call (HVC) path, but only when the hypervisor provides the expected service. Changing the string does not create that service.

## Follow Linux's wrapper and return conversion

In `linux-xlnx@xilinx-v2024.1:drivers/firmware/xilinx/zynqmp.c`, `zynqmp_pm_invoke_fn()` checks feature support, builds the service identifier and packs management arguments into the firmware-call registers. It then uses the selected SMC or HVC function pointer.

The SMC wrapper extracts returned words from the result registers. `zynqmp_pm_ret_code()` translates firmware status into Linux errors. For example, `XST_PM_NO_ACCESS` becomes `-EACCES`, while unsupported-feature and unsupported-version cases have different mappings. Several other statuses map to `-EINVAL`.

This translation loses some detail. A Linux `-EINVAL` does not prove that the immediate driver passed an ordinary malformed argument; it can represent several platform errors. When available, preserve the firmware response as well as the translated Linux value.

The driver treats `XST_PM_DOUBLE_REQ` as success. This is a release-specific implementation detail, not a reason to ignore resource-lifetime balance. Higher-level code must still use the owning framework correctly and avoid mismatched request/release behavior.

## Synchronous completion is not always the whole operation

Some management APIs include acknowledgement choices or asynchronous notification behavior. Read the specific operation's contract before assuming that return means the final physical state is already reached. “Request accepted” and “transition completed” are different events.

A client waiting for completion needs a defined timeout and a recovery decision. It also needs to handle a response that arrives after the timeout. Reusing a buffer for a new request while an older response is still possible can associate the wrong result with the new operation.

Do not generalize one API's acknowledgement field to every firmware service. Check the wrapper signature, the TF-A forwarding path and the PMU handler for that operation in the same release.

## Diagnose support, permission and transport separately

A useful investigation starts with whether the firmware interface initialized. If no conduit was selected, Linux's default call function returns `-ENODEV`. That failure occurs before a valid management transaction can reach PMUFW.

If version or feature queries succeed, the transport is working for those requests. An operation-specific rejection then points toward support, arguments or access policy. A request that never returns requires a different investigation: handler progress, IPI acknowledgement, interrupt delivery and firmware health.

For a power transition, add the resource's parent and current users to the record. For a reset, add which software owns the device and whether transfers were stopped. These facts separate a legitimate refusal from a firmware defect.

## Integration with Linux frameworks

Applications should normally use the device's Linux interface. Drivers should normally use clock, reset, runtime-power and other kernel frameworks. Those frameworks maintain their own reference counts and ordering, then reach the platform firmware where needed.

A parallel userspace control path can make the kernel's model false. For example, changing a clock behind the driver can leave its cached rate or timing setup stale. Keep one clear owner for a managed resource and design any diagnostic interface around that ownership.

> [!NOTE]
> **Not run on the reference setup:** conflicting A53/R5 requests, denied-resource injection and asynchronous transition timing. The request lifecycle and status mappings above were checked in the pinned Linux and PMU sources.

## References

- [ZynqMP Linux firmware driver, 2024.1](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/firmware/xilinx/zynqmp.c).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/pm_core.c`, request, release, requirement and dispatch paths.
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/plat_psci.c` and `plat/xilinx/common/pm_service/pm_api_sys.c`.

---

<sub>← [PMU Firmware Architecture and Source](02-pmufw-architecture-and-source.md) · [Chapter index](README.md) · [Communicating With the PMU](04-communicating-with-the-pmu.md) →</sub>
