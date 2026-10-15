# Debugging Applications

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Match code and symbols

Remote debugging commonly uses `gdbserver` on the target and the SDK's debugger on the host. The host needs the exact executable, shared libraries and debug symbols corresponding to the running process.

| Tool | Useful evidence |
| --- | --- |
| GDB | Threads, stack, variables and breakpoints |
| Core dump | State at a process crash |
| strace | System calls and error returns |
| ltrace | Supported dynamic-library call tracing |
| Valgrind | Supported memory diagnostics, with substantial overhead |

IDE integrations such as VS Code or Vitis still depend on those same paths and symbols. Debug packages often separate symbols from runtime files; preserve them by build identifier.

Do not expose a debugger service to an untrusted network. Use a controlled connection and remove temporary debug access after testing. Timing-sensitive hardware interactions may change when a process stops at a breakpoint.

> [!NOTE]
> **Not run on the reference setup:** a new remote-debug or memory-analysis session.

## References

- GDB manual, remote debugging and separate debug files
- Yocto 4.1.4 SDK and debugging documentation

---

<sub>← [Cross-Compiling Applications](01-cross-compiling-applications.md) · [Chapter index](README.md) · [Profiling and Performance](03-profiling-and-performance.md) →</sub>
