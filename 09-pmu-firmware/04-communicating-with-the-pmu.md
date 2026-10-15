# Communicating With the PMU

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot

## Select the supported interface

Linux normally reaches PMU services through the ZynqMP firmware driver. Its exported kernel interfaces serve clock, reset, power and other drivers. Debugfs/sysfs facilities depend on build configuration and are diagnostic interfaces, not a stable application protocol.

U-Boot provides supported operations through its ZynqMP command and firmware integration. Bare-metal software can use **xilpm** for platform-management requests. Raw **XIpiPsu** access provides a lower-level transport, but using the transport alone does not implement the management protocol.

## Custom communication

A custom IPI service needs a defined message format, ownership, request identifier, length checks, response status and timeout behavior. Both endpoints must agree on buffer use and notification ordering. Do not reuse an existing management message identifier for an unrelated operation.

Check whether the channel is already owned by Linux, TF-A or another processor. Shared memory also needs a clear cache/coherency policy. An interrupt indicates that work may be available; it does not validate the payload.

> [!NOTE]
> **Not run on the reference setup:** a custom end-to-end IPI handler. Registering one requires matching firmware and caller implementations; no fabricated response transcript is included.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/firmware/xilinx/zynqmp.c`
- `embeddedsw@xilinx_v2024.1:lib/sw_services/xilpm/`, `XilinxProcessorIPLib/drivers/ipipsu/`

---

<sub>← [EEMI and Platform Management](03-eemi-and-platform-management.md) · [Chapter index](README.md) · [Customizing PMU Firmware](05-pmufw-customization.md) →</sub>
