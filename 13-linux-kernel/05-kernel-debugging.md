# Kernel Debugging

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers

## Choose evidence by stage

Early failures need early-console support. Later failures can use the kernel log, dynamic debug, tracepoints and subsystem diagnostics. Debugfs is useful for investigation but is not a stable product API.

| Tool | Best use |
| --- | --- |
| `dmesg` / kernel journal | Messages and failure context |
| Dynamic debug | Enable selected diagnostic messages |
| ftrace / trace-cmd | Execution and timing events |
| kprobes | Targeted runtime instrumentation |
| `vmlinux`, `addr2line`, `decode_stacktrace.sh` | Resolve stack addresses |
| KGDB / JTAG | Controlled stops and memory inspection |
| kdump | Capture state after selected crash conditions |

Use exact symbols and account for address randomization when resolving a crash. Preserve the first error; later failures may be consequences.

## Measurement limits

Logging changes timing. Breakpoints can stop a processor while DMA and peripherals continue running. A bug disappearing under the debugger is evidence of changed timing, not proof that the code is correct.

> [!NOTE]
> **Not run on the reference setup:** KGDB, kdump and deliberate crash tests.

## References

- Linux 6.6 `Documentation/admin-guide/`, `Documentation/trace/`
- `linux-xlnx@xilinx-v2024.1:scripts/decode_stacktrace.sh`

---

<sub>← [Configuring and Building the Kernel](04-configuring-and-building.md) · [Chapter index](README.md) · [Real-Time Linux](06-real-time-linux.md) →</sub>
