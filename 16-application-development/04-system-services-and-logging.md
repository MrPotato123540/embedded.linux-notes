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

## References

- systemd.service(5), systemd.exec(5), journald.conf(5)
- [Error management and watchdogs](../09-pmu-firmware/06-error-management-and-watchdogs.md)

---

<sub>← [Profiling and Performance](03-profiling-and-performance.md) · [Chapter index](README.md) · [Python and High-Level Frameworks](05-python-and-high-level-frameworks.md) →</sub>
