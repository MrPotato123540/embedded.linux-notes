# System Services and Logging

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Service lifecycle

Run the product application under a service manager with explicit startup, stop and restart behavior. A restart loop can hide a permanent configuration problem, so apply a sensible rate limit and preserve the original error.

Log through journald or syslog, or use a clearly managed application log. Include build version and operation context without writing secrets. Set storage limits and rotation so diagnostics cannot fill the root filesystem.

## Watchdog integration

A watchdog heartbeat should represent useful progress. Tie it to the health conditions that matter: event-loop progress, required worker response or valid hardware communication. A timer that continues while the application is dead gives false confidence.

Test shutdown during an active operation and restart after corrupted configuration. Define whether persistent data is recoverable and whether recovery needs operator action.

> [!NOTE]
> **Not run on the reference setup:** application-specific service and watchdog fault tests.

## Package the execution environment with the application

A service consists of an executable, configuration, runtime identity, dependency policy and shutdown behavior. A unit file or init script is part of that product interface. Installing only the executable leaves the rest dependent on manual setup.

The supplied image uses systemd 251.8. In the local Yocto layer, `systemd.bbclass` handles service-file integration and package enablement policy. A recipe should install its unit in the configured unit directory and identify it through the class variables. Hard-coded host paths can fail when target layout or distribution policy differs.

Keep application state out of the executable directory. Configuration, durable data, temporary files and logs have different ownership and update lifetimes. Define those paths explicitly so a read-only rootfs or account restriction does not break startup unexpectedly.

## Readiness must describe useful operation

A process can start before it is able to serve requests. A service that needs a database and a device should report ready only after those resources reach the required state. With notification-based service startup, the application must implement the manager's notification contract; adding the unit setting alone is not enough.

For a simple foreground process, the service manager tracks the process lifetime. If the program forks into the background without the matching service model, the manager can track the wrong process or consider startup complete too early. Prefer a foreground mode designed for supervision.

Hardware readiness can change after startup. A device may disconnect or be reconfigured. The application needs a runtime state machine, not only a one-time pre-start check. It should reject new work cleanly while the device is unavailable and rebuild resources after a compatible device returns.

## An illustrative service lifecycle

A telemetry service starts under a dedicated account. It opens its state directory, validates configuration, connects to the sensor interface and then accepts requests. Each accepted request has an identifier carried into its log messages and output records.

On termination, the service stops accepting new work, completes or cancels active requests, writes required state and closes resources. A timeout policy defines how long shutdown may take. If the manager eventually kills the process, recovery on the next start must detect incomplete transactions.

The stop path should not wait forever for hardware that disappeared. A blocking device operation needs cancellation or a bounded error path. A service-manager timeout is a last boundary, not a substitute for correct driver and application cancellation.

## Logs should identify the failing boundary

Record image/application version, request identity and the operation that failed. Include the actual error code and relevant resource name. “Device error” is weak evidence; “request17 failed while waiting for DMA completion” points to a specific stage without exposing private payload data.

Use a consistent timestamp strategy. Wall-clock time helps compare machines, while a monotonic clock measures durations without clock-correction jumps. Boot-relative time can correlate userspace with kernel events. State which timebase appears in a performance capture.

Avoid logging a success before the operation's durable or hardware completion point. A “saved” message after buffering data in memory can mislead a power-loss investigation. A “job done” message after submission can mislead an accelerator timeout investigation.

## Journal storage is a capacity decision

System logs may be volatile or persistent depending on configuration and available paths. A reboot can therefore remove evidence if the product uses only RAM-backed logging. Persistent logging improves post-reboot diagnosis but consumes storage and write endurance.

Set a bounded policy and test behavior when storage fills. An application should not deadlock because its diagnostic output blocks indefinitely. High-rate logs can also change timing and reduce the life of flash storage. Rate limiting and structured event summaries are often more useful than logging every sample.

A read-only software image can still have a dedicated persistent log location. Keep that decision separate from whether the root filesystem itself is writable.

## Restart and watchdog policy need discrimination

An automatic restart should preserve enough evidence to explain the previous failure. A crash loop caused by invalid configuration should eventually become visible as a stable failed state, not consume the whole CPU with repeated startup.

A watchdog notification should depend on meaningful progress. If the service's main work is stalled but a timer still sends notifications, the watchdog cannot detect that failure. Conversely, a legitimate long operation needs a designed progress or timeout policy so it is not killed merely for being slow.

> [!NOTE]
> **Not run on the reference setup:** installing a new service, validating shutdown under device loss, or exercising log limits. The systemd 251 documentation and supplied packaging integration were inspected.

## References

- [systemd v251:systemd.service.xml](https://github.com/systemd/systemd/blob/v251/man/systemd.service.xml) and [systemd.exec.xml](https://github.com/systemd/systemd/blob/v251/man/systemd.exec.xml).
- Inspected BSP `poky/meta/classes-recipe/systemd.bbclass` and `rootfs.manifest`.

- systemd.service(5), systemd.exec(5), journald.conf(5)
- [Error management and watchdogs](../09-pmu-firmware/06-error-management-and-watchdogs.md)

---

<sub>← [Profiling and Performance](03-profiling-and-performance.md) · [Chapter index](README.md) · [Python and High-Level Frameworks](05-python-and-high-level-frameworks.md) →</sub>
