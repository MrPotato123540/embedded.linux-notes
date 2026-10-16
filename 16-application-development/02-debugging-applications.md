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

## Debug the process that actually runs

A source tree, an executable and debug information form a matched set. The debugger uses addresses and debug records from that exact build. Loading symbols from a later rebuild can produce believable but wrong source lines and variable values.

Keep the executable's build ID, image version, source revision and separate debug files. For a shared-library failure, retain the libraries too. A correct application binary with mismatched target libraries can still create an incorrect stack interpretation or symbol lookup.

The runtime environment matters as much as the binary. Record the service account, supplementary groups, working directory, environment variables, device permissions and command arguments. A program launched from an interactive root shell may bypass the condition that causes the service to fail.

## Remote debugging separates control and symbols

A target-side debug server controls the process through the target kernel. A host debugger presents symbols and source. They communicate using a remote protocol. The host therefore does not need to execute the target's machine code, but it must understand the architecture and use the target's matching binary information.

The debugger's sysroot and library search configuration should point to the release's target files. Host `/lib` is not a substitute. Position-independent executables and address-space randomization mean runtime addresses can differ between runs; the debugger needs the actual loaded mappings.

Attaching to an existing process preserves its current state but can disturb timing. Starting it under the debugger changes startup timing even more. For race conditions and hardware deadlines, record that disturbance and prefer tracing or captured evidence when stopping the process invalidates the experiment.

## A crash is often the last symptom

A segmentation fault identifies an invalid memory access, not necessarily the original bug. A buffer overwrite can corrupt a pointer long before the program follows it. The faulting line may be correct code using damaged state.

Begin with the faulting address, instruction and thread stack. Then inspect all threads and the ownership of the object involved. A worker can free a buffer while another thread still uses it; the later crash can appear in a library allocator or string function. The useful question is which path transferred or ended ownership too early.

Optimized builds complicate source-level views. Variables can be removed, merged or moved, and one source line can cover several machine instructions. An “optimized out” variable is not a debugger malfunction. Preserve an optimized build for reproducing timing-sensitive behavior and a suitable debug build for controlled experiments.

## A concrete missing-file investigation

Suppose an executable appears in the target directory, but starting it reports that it cannot be found. Check the file's format before editing PATH. A script may name a missing interpreter in its shebang. An ELF file may name a missing loader in `PT_INTERP`.

The inspected BSP Bash binary requests `/lib/ld-linux-aarch64.so.1`. If a reduced image omits that file, copying Bash alone cannot work. If the loader is present but `libtinfo.so.5` is missing, the error comes from a later stage. Following this chain prevents wasting time on file permissions when the real issue is packaging.

System-call tracing can show which pathname lookup fails, while ELF inspection shows the expected interpreter and libraries without running the binary. Use the least intrusive evidence that answers the current question.

## Memory tools have different coverage

Address sanitizers instrument selected memory accesses and can detect out-of-bounds and use-after-free errors in instrumented code. Thread sanitizers target data races. Undefined-behavior checks cover selected language rules. These tools change memory layout, execution cost and timing, so their results complement normal-build testing.

Valgrind uses another execution model and can be much slower. Architecture and instruction support must match the target. A clean result from one workload does not prove that all error paths are safe, and tools cannot fully model arbitrary DMA writes from PL hardware.

For a DMA-backed application, the kernel and device lifetime rules remain critical. Userspace instrumentation may see a valid mapped address while the buffer's device ownership is wrong. Log request identifiers and buffer transitions so application and driver traces can be correlated.

## Core files and sensitive state

A core dump can preserve process mappings and thread state after a crash. Its usefulness depends on dump policy, available storage and retained matching symbols. A missing core may reflect configured limits or the service manager's handling rather than a failure of the crashing program to signal.

Core files can contain application data and secrets. Store them through the product's normal diagnostic access policy. For an embedded target, also budget disk space and ensure repeated crashes cannot fill the persistent volume.

> [!NOTE]
> **Not run on the reference setup:** a new remote-debugging session, sanitizer run or target core capture. The diagnostic paths are engineering procedures; no successful target output is invented.

## References

- Inspected BSP ELF loader/library metadata in `pre-built/linux/images/rootfs.tar.gz`.
- [GNU GDB manual](https://sourceware.org/gdb/current/onlinedocs/gdb.html/Remote-Debugging.html), remote target and symbol separation.
- [systemd v251:systemd.exec.xml](https://github.com/systemd/systemd/blob/v251/man/systemd.exec.xml), execution environment and resource limits.

- GDB manual, remote debugging and separate debug files
- Yocto 4.1.4 SDK and debugging documentation

---

<sub>← [Cross-Compiling Applications](01-cross-compiling-applications.md) · [Chapter index](README.md) · [Profiling and Performance](03-profiling-and-performance.md) →</sub>
