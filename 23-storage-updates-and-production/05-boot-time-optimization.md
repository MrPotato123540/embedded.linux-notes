# Boot-Time Optimization

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Define the event you are trying to improve

Boot time can mean power-on to first UART text, kernel entry, login prompt, network availability or the main application's useful output. These are different events. Pick a product-ready event and record intermediate boundaries so an improvement has a clear meaning.

ZynqMP startup includes hardware/ROM work, FSBL, PMU firmware, TF-A, U-Boot, kernel initialization, root-filesystem setup and userspace services. Some stages overlap or use different clocks. A timestamp from Linux starts after earlier boot work and cannot measure total power-on time by itself.

Use a common external clock or a well-defined capture system for end-to-end timing. Kernel timestamps and userspace monotonic timestamps are useful within their domains. Serial line arrival time adds buffering and output delay, especially under emulation.

## Extract a bounded result from the existing capture

The saved `boot-ts.log` includes host-side timestamps. Relevant observations are:

| Event | Captured host time |
| --- | --- |
| First PMU firmware line | `15:40:49.466` |
| First U-Boot banner line | `15:40:49.879` |
| `Starting kernel ...` | `15:40:53.109` |
| First Linux boot line | `15:40:53.128` |

The interval from the captured U-Boot banner to its kernel-start message is 3.230 seconds. The interval from the first PMU line to kernel-start is 3.643 seconds. These are calculations from an existing QEMU serial capture, not physical-board boot measurements and not power-on-to-ready time.

The log also shows SATA timeouts, USB scanning and an autoboot countdown before kernel entry. Those are concrete candidates for investigation if the product does not need those paths. The capture does not prove how much each would save on real hardware after a configuration change.

## Optimize the critical path

A dependency graph determines when the application can start. A long service that runs in parallel after readiness may not affect the target event. A short service that blocks a required mount or device can matter more.

For an original example, if application readiness waits for network-online, a missing cable can dominate boot even when local operation needs no network. The correct change may be to remove that unnecessary dependency or make the application's network use asynchronous. Reducing kernel compression time would not fix the dependency error.

Likewise, a storage scan in U-Boot may be unnecessary when production always boots from one verified location. Restricting search can reduce delay, but preserve a deliberate recovery entry. An optimized normal path without a usable recovery path is an incomplete product design.

## Kernel initialization needs measured attribution

Kernel initialization includes built-in driver initcalls, device probing, dependency deferral and root-device discovery. The `initcall_debug` boot parameter can provide initcall timing, but extra logging affects the measured system and does not directly cover every later asynchronous operation.

Inspect the first relevant delay and its dependency. A slow probe may wait for a regulator, clock, firmware file or missing device. Disabling an unrelated driver because it prints near a pause can remove functionality without reducing the real wait.

Built-in versus module placement changes when work occurs and what the root filesystem must contain. Moving a required storage driver to a module can prevent the root filesystem from becoming available unless an initramfs supplies it. Faster kernel entry is not a useful result if the required root path breaks.

## Image size, compression and media speed interact

A compressed image costs decompression time but reduces bytes read from storage. The faster choice depends on CPU performance, media throughput and compression ratio. Measure the full load-plus-decompress interval on the actual boot path.

Removing unused packages can reduce root-image transfer and filesystem work. Removing unused kernel drivers can reduce image size and probe activity. Keep the dependency review explicit: a seemingly unused firmware or module may be required only on a hardware variant or during recovery.

The reference boot capture loads an initramfs and later switches into its root environment. That flow differs from directly mounting a block root or network root. Comparing only image file sizes across those flows hides different mount and copy costs.

## Userspace parallelism needs correct readiness

Systemd starts units according to dependency and ordering rules. Ordering after a service does not always mean the service has completed its useful initialization; the service type and readiness protocol matter. A process that forks and reports startup early can make the timeline look fast while the application still waits internally.

Use explicit readiness where the product depends on it. Record the first successful application operation, not only the service manager's active state. For a camera product, that might be a valid frame with expected metadata; for a controller, it might be a safe initialized output and accepted command.

Do not remove filesystem checks, integrity verification or required hardware calibration solely because they take time. Understand the requirement and choose a design that reduces the work safely, such as immutable verified content or an appropriate retained-state strategy.

## Compare distributions and recovery paths

Measure repeated cold boots and warm resets separately. Media caches, device state, temperature and power sequencing can change results. Report the number of runs and maximum observed time as well as the average. A rare 30-second network wait can matter more than a 200-ms average improvement.

After each change, validate the same readiness event and required functions. Keep the old and new artifact hashes so a result can be reproduced. If several configuration changes are combined, the measurement cannot identify which one caused the improvement or regression.

Also time recovery: failed pending image, missing storage, absent network and damaged optional configuration. A product that starts quickly only in ideal conditions can still have an unacceptable field experience.

> [!NOTE]
> **Not run on the reference setup:** new optimized image builds, repeated timing experiments or physical power-on measurements. Existing QEMU timestamps were analyzed; no boot-time reduction is claimed.

## References

- Existing `reference-setup/captures/boot-ts.log`, inspected timestamped serial evidence.
- `linux-xlnx@xilinx-v2024.1:Documentation/admin-guide/kernel-parameters.txt`, `initcall_debug`; `init/main.c`, initialization sequence.
- [systemd-analyze documentation](https://github.com/systemd/systemd/blob/v251/man/systemd-analyze.xml), userspace timing interpretation for the reference image's systemd 251 family.

---

<sub>← [Software Update Strategies](04-software-update-strategies.md) · [Chapter index](README.md) · [Reliability and Field Diagnostics](06-reliability-and-field-diagnostics.md) →</sub>
