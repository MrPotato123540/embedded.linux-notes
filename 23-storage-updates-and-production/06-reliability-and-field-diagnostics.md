# Reliability and Field Diagnostics

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Reliability starts with observable state

A field failure report should identify the running release, hardware revision, boot source, reset reason and important subsystem state. Without those facts, two devices with similar symptoms can be running different kernels, bitstreams or configuration schemas.

Create a release identifier that maps to exact artifact hashes and build inputs. Include the kernel/module set, DTB, firmware, PL design and application version. A single application version string cannot identify the whole ZynqMP system.

Diagnostics also need context over time. A reset counter, previous pending-update state and recent storage errors can distinguish a one-time power loss from a repeated crash loop. Keep counters bounded and update them with a storage method that does not create excessive wear or a new corruption risk.

## A watchdog tests progress only if its owner does

A watchdog resets the system when it is not serviced within the configured interval. If a healthy timer thread feeds it while the main application is deadlocked, the watchdog proves only that the timer thread still runs.

Define a supervisor that checks meaningful progress from required components. For an original acquisition product, it could require advancing frame sequence, a responsive control task and bounded output-queue age. A process existing in the task list is weaker evidence than completing its work.

The saved QEMU boot log reports two Cadence watchdog instances with 60-second and 10-second timeouts. These are captured initialization messages, not proof that either watchdog was armed, tested or configured as the product's supervisor. Device registration and active watchdog policy are separate states.

The Linux watchdog API also has close and nowayout behavior that depends on the driver and configuration. A service must understand what happens when it exits, restarts or loses its descriptor. Do not assume closing the device always disables the timer. [Linux watchdog API](https://www.kernel.org/doc/html/v6.6/watchdog/watchdog-api.html).

## Preserve the failure before reboot removes it

Ordinary RAM logs disappear on reset. Persistent logging can retain more evidence, but storage may be the component that failed, and synchronous logging can disturb timing. Use several bounded channels where the product needs them: serial capture during development, a persistent ring of important events and crash storage where supported.

Linux pstore can expose persistent crash records from a backend. Ramoops uses a reserved RAM region that survives suitable resets. It requires a correct reserved-memory layout and a reset path that preserves that memory. It is not guaranteed to survive power removal.

The existing reference log says the systemd persistent-storage archival service was skipped because `/sys/fs/pstore` was empty. That is evidence of no records for that condition at that time. It is not a verified ramoops configuration or a successful crash-capture test. [Ramoops documentation](https://www.kernel.org/doc/html/v6.6/admin-guide/ramoops.html).

## Classify reset causes and failure scope

A software reboot, watchdog reset, brownout and external reset can leave different evidence. Read reset-cause information through the supported platform path early enough that later code does not clear or replace it. Record the interpretation and relevant firmware version.

A CPU crash does not necessarily stop every DMA engine or remote processor. Recovery must bring the complete hardware ownership state back to a known condition. An R5 may continue running while Linux restarts, which requires protocol generation handling rather than blindly clearing shared memory.

For a repeated reset loop, limit automatic retries and retain the first useful failure record. A system that overwrites its only log on every boot can erase the evidence before support receives it. Recovery mode should provide enough identity and diagnostics to understand the failed normal path.

## Make logs useful without making them unbounded

Record timestamps with their clock domain, event IDs, component version and bounded context. Wall-clock time may be wrong before synchronization, so a monotonic time and boot identifier can be valuable. Avoid comparing timestamps across boots without an explicit relationship.

Rate-limit repeated errors and count suppressed occurrences. A broken peripheral that emits thousands of lines per second can fill storage and alter scheduling, creating secondary failures. Preserve the first event, a count and a small recent sample rather than unlimited duplicate text.

Separate diagnostic content from secrets and user payloads. Device certificates, private keys and sensitive application data do not belong in ordinary support bundles. A useful report can include public identity hashes and configuration version without exporting credential material.

## Health checks need failure injection

A meaningful test deliberately removes a required input or stalls a component and confirms the expected response. For example, stop new application progress while leaving the supervisor alive, then verify whether it detects the condition within the intended bound. This is a proposed test, not a result from this revision.

Also test the diagnostic path under storage-full, read-only-root, network-loss and clock-not-synchronized conditions. If a support bundle requires the failed service to be healthy, it is least useful when needed most.

Measure recovery time and retained evidence together. A rapid reset that loses every useful record may make a rare failure impossible to diagnose. A long crash dump can delay recovery beyond the product deadline. Choose the balance from the system requirement.

## Build a bounded support record

A practical record joins artifact identities, boot history, reset causes, kernel errors, relevant counters and selected configuration. Add device-specific evidence such as ECC trends, network drops, queue high-water marks or remote-processor restart counts.

Each counter needs a definition: lifetime since boot, lifetime since service start or persistent lifetime. Otherwise a value of zero can mean either no failures or a recent reset. State collection limits and dropped records so missing evidence is not mistaken for success.

Keep the collection process read-only where possible. A diagnostic action that resets a device or changes a clock can remove the failure state. Such actions belong in a separate recovery procedure with their effects recorded.

> [!NOTE]
> **Not run on the reference setup:** watchdog expiry, deliberate crashes, ramoops recovery and field fault injection. Existing watchdog and pstore messages were inspected without claiming operational validation.

## References

- `linux-xlnx@xilinx-v2024.1:Documentation/watchdog/watchdog-api.rst` and `Documentation/admin-guide/ramoops.rst`, inspected locally.
- Existing `reference-setup/captures/boot-prebuilt3.log`, watchdog registration and empty-pstore service condition.
- [Software update recovery](04-software-update-strategies.md) and [RPU restart ownership](../21-rpu-and-openamp/05-ipi-and-shared-memory.md).

---

<sub>← [Boot-Time Optimization](05-boot-time-optimization.md) · [Chapter index](README.md) · [Licensing and Compliance](07-licensing-and-compliance.md) →</sub>
