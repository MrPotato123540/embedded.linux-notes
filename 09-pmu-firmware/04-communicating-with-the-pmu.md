# Communicating With the PMU

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[09 · PMU and PMU Firmware](README.md)** · Part IV: Boot


## Choose the highest supported interface

Linux drivers normally communicate with platform management through the ZynqMP firmware driver. They should not independently claim the same inter-processor interrupt (IPI) resources already used by firmware. Bare-metal clients can use the platform-management library, while the low-level IPI driver provides transport operations.

These layers solve different problems. The transport moves words and signals another processor. The protocol defines what those words mean, who may send them, how completion works and what an error means. A successful interrupt does not establish a valid management request.

Diagnostic sysfs or debugfs interfaces, when present in a build, are not automatically a stable application interface. Their availability and accepted operations can change. Product applications should use a deliberate driver interface with defined permissions and lifetime rules.

## A concrete Linux-to-firmware packing example

The pinned Linux `zynqmp_pm_invoke_fn()` accepts up to fourteen 32-bit management arguments. It puts the service identifier in the first 64-bit SMC argument and packs pairs of 32-bit values into each remaining argument. The low word goes in bits 31:0 and the next word goes in bits 63:32.

As a purely arithmetic example, arguments `0x11223344` and `0x55667788` produce a packed value of `0x5566778811223344`. This is not a valid command by itself; it illustrates the word order in the inspected wrapper. Sending the two words in reverse order can produce a syntactically delivered call with the wrong resource or operation.

The SMC wrapper returns response words from `a0` and `a1`, and converts the status to a Linux error. This is why a client must use the matching wrapper signature. A 64-bit physical address often needs a defined low/high-word representation; casting it to one 32-bit argument loses information.

## The PMU dispatch identity is a separate layer

In `xpfw_core.c`, PMU IPI dispatch matches the upper 16 bits of the first payload word to a registered module's `IpiId`. The power-management module registers ID 0. A custom service needs a coordinated ID and message format that do not collide with existing modules.

The hardware channel, source mask, module ID and operation ID are separate identities. Record all of them in a protocol design. If the message reaches the wrong handler, changing the shared buffer's contents may not fix the routing problem.

`xpfw_ipi_manager.c` provides message and response read/write helpers. Their existence does not remove the caller's obligation to obey maximum lengths, channel ownership and acknowledgement rules.

## Design a custom request as a complete transaction

A useful custom protocol specifies a version, operation, request identity, payload length, response status and response data. These are design requirements, not a prescribed wire layout for the standard PM API.

The receiver validates the length before reading fields. It checks the operation and version before acting. It checks caller permissions before touching a resource. It returns a defined error for unsupported operations rather than silently interpreting them as something else.

A request identity helps distinguish retries and delayed responses. Suppose a caller times out, sends another request, and then receives the old response. Without an identity or a strict one-outstanding-request rule, it can report the old result as the new result.

An operation that changes state also needs a retry rule. Reading a counter can usually be repeated. Advancing a state machine or toggling a reset may not be safe to repeat without knowing whether the first request completed. Define idempotent behavior where practical, or expose enough state to recover safely.

## Buffer visibility and notification ordering

When a protocol uses shared DDR in addition to the small IPI message, both endpoints must agree on physical addresses, sizes and cache policy. A virtual address in Linux is not automatically meaningful to the PMU. A valid physical address is not automatically permitted or safely mapped for every participant.

The sender writes the payload, makes it visible under the chosen coherency rules, then sends the notification. The receiver observes the notification, makes the buffer visible to its CPU if needed, and validates the contents. After completion, buffer ownership returns according to the protocol.

An interrupt does not flush caches for you. A memory barrier orders accesses; it does not by itself perform every required cache-maintenance operation. Use the platform's supported coherent or DMA memory interfaces rather than mixing cached pointers with unexplained flush calls.

## Timeouts must leave a defined state

A timeout tells the caller that completion was not observed within a limit. It does not prove that the PMU never received the request or that the operation did not occur. This distinction matters for resets, power changes and persistent operations.

After a timeout, keep the request buffer owned until the protocol says it can be reused, or cancel/reset the channel through a defined recovery path. Do not free shared memory while firmware may still access it. The same rule applies when a Linux process exits while its kernel request is active.

Keep handlers bounded. A handler that waits for a response from a caller that is itself blocked waiting for that handler creates a deadlock. Split long operations into explicit phases when the firmware execution model requires it.

## Diagnose one boundary at a time

Start with Linux conduit selection and feature support. Then inspect TF-A service routing. Then inspect the IPI source and module selection. Finally, inspect operation decoding and the response path. A failure at an earlier boundary makes later debugging irrelevant.

For a custom service, record a small trace of request identity, source, operation, accepted length and final status at both ends. This can distinguish “never delivered,” “delivered but rejected,” and “completed but response lost.” Avoid dumping secret payloads or large buffers merely to show progress.

> [!NOTE]
> **Not run on the reference setup:** a custom end-to-end IPI service or shared-DDR protocol. The standard Linux packing and PMU dispatch paths were inspected directly; the custom protocol above is design guidance.

## References

- [2024.1 Linux firmware call implementation](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/firmware/xilinx/zynqmp.c).
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_pmufw/src/{xpfw_core.c,xpfw_ipi_manager.c,xpfw_mod_pm.c}`.
- `embeddedsw@xilinx_v2024.1:lib/sw_services/xilpm/` and `XilinxProcessorIPLib/drivers/ipipsu/`.

---

<sub>← [EEMI and Platform Management](03-eemi-and-platform-management.md) · [Chapter index](README.md) · [Customizing PMU Firmware](05-pmufw-customization.md) →</sub>
