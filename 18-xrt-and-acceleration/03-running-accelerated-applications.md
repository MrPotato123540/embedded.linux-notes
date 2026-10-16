# Running Accelerated Applications

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[18 · XRT and Hardware Acceleration](README.md)** · Part VIII: Programmable Logic and Acceleration

## Execution lifecycle

Open the device, load a compatible xclbin, select the kernel, allocate buffer objects for the correct memory groups, populate inputs, synchronize as required, start a run and wait for completion. Synchronize output before the CPU reads it.

A mapped buffer pointer does not guarantee automatic visibility across every device path. Follow the runtime's buffer ownership rules. “Zero-copy” describes avoided copies, not the absence of synchronization.

## Debugging

Use the installed runtime utilities, such as the supported `xbutil` commands, to inspect device and runtime status. `xrt.ini` can enable release-specific diagnostics. Preserve the exact configuration because tracing can change performance.

Validate output against a software reference before measuring speed. Check transfer sizes, kernel arguments, completion status and timeouts. Separate data-movement overhead from compute time.

> [!NOTE]
> **Not run on the reference setup:** an XRT accelerator run or profile.

## Use a buffer-ownership timeline

The CPU fills an input buffer while it owns that data. A synchronization toward the device makes the intended contents available through the runtime's platform-specific mechanism. The run then owns the data for its execution interval. After confirmed successful completion, output synchronization makes device-produced data available to the CPU.

The following is **illustrative C++**, written to show API relationships. It is not a complete application, has not been compiled here, and assumes a compatible three-argument kernel `(input, output, count)` plus already validated device and kernel objects:

```cpp
const std::size_t bytes = count * sizeof(std::uint32_t);
// Production code must check count and multiplication overflow first.
xrt::bo input(device, bytes, kernel.group_id(0));
xrt::bo output(device, bytes, kernel.group_id(1));
auto* in = input.map<std::uint32_t*>();
auto* out = output.map<std::uint32_t*>();
fill_input(in, count);  // Application-defined function.
input.sync(XCL_BO_SYNC_BO_TO_DEVICE, bytes, 0);
auto run = kernel(input, output, count);
run.wait();
if (run.state() != ERT_CMD_STATE_COMPLETED)
    throw std::runtime_error("accelerator did not complete successfully");
output.sync(XCL_BO_SYNC_BO_FROM_DEVICE, bytes, 0);
check_output(out, count);  // Application-defined software reference.
```

The example deliberately uses the argument's memory group for each buffer. The output pointer is created early but not read until completion and synchronization. The element count and byte count are separate values; passing bytes to a kernel that expects elements can overrun the buffer.

## `map`, `write` and `sync` do different work

The pinned `xrt_bo.h` describes `map()` as exposing the host-side buffer mapping. `write()` copies application data into the buffer's host backing storage. `sync()` synchronizes the chosen direction and byte range with the device side.

A direct write through the mapped pointer can avoid an application-to-buffer copy. It does not remove the synchronization requirement. On an embedded shared-memory platform, synchronization may mainly perform cache maintenance rather than move data over PCIe, but the application must still follow the API contract.

Partial synchronization needs correct bounds. The offset is within the buffer object and the size is in bytes. A range for one tensor row must account for stride and element size. Synchronizing only the logical width while the kernel reads padded data can leave part of the input stale.

## Completion is not necessarily success

The pinned `xrt_kernel.h` explicitly distinguishes returning from a wait from successful completion. Inspect the run state. Errors, aborts and timeouts must not be treated as valid output. An application should carry request identity through submission, state checks and validation.

The same 2024.1 header documents an important limitation: a timeout in `run::wait()` can be masked when other runs keep completing within the timeout interval. Therefore, that wait is not a reliable hard wall-clock deadline in every concurrent workload.

A product needing a hard deadline requires an independent supervision/recovery design validated against the selected runtime. A timeout also does not establish that hardware stopped using its buffers. Keep the objects alive until the supported abort/reset/completion path makes reuse safe.

## Reuse requires a state transition

A run handle can be reused under its documented contract, but a buffer cannot be refilled while a previous run still reads it. For pipelining, keep a pool with explicit states and associate each run with its input/output pair.

For an illustrative double-buffered pipeline, the CPU can prepare pair B while the device runs pair A. After A completes and its output is consumed, A becomes available again. If the consumer is slow, the pool fills and the producer needs backpressure or a defined dropping policy.

Do not use one global mapped pointer and a “current job” variable when several jobs overlap. Store per-job lengths, buffers, timestamps and completion state. This makes both correctness and diagnosis easier.

## Validate data before comparing speed

Use a software reference that checks output size, ordering and values. Include edge cases such as zero/short work where supported, maximum valid count and lengths that cross alignment boundaries. For floating-point results, define a justified error tolerance rather than accepting any nonzero output.

A deterministic test pattern can reveal stale buffers and argument-order errors. Repeating the same all-zero input can hide both problems. Keep failures in the performance record instead of discarding them from average throughput.

Separate allocation, input preparation, synchronization, scheduling, kernel execution, output synchronization and postprocessing. The fastest kernel time may contribute little to total latency if conversions dominate.

## Diagnosis by last completed stage

Device-open failure points to runtime/driver discovery and permission. Kernel-construction failure points to xclbin identity and kernel name. Group lookup or allocation failure points to connectivity and memory resources. Execution failure points to argument layout, hardware protocol and completion. Correct completion with wrong values points to data layout, synchronization or algorithm behavior.

Tracing options in `xrt.ini` can add evidence but also overhead. Record the installed runtime version and active tracing settings with each capture. No target XRT execution or trace was produced for this revision.

## References

- [XRT@a75e984:xrt_bo.h](https://github.com/Xilinx/XRT/blob/a75e9843c875bac0f52d34a1763e39e16fb3c9a7/src/runtime_src/core/include/xrt/xrt_bo.h), mapping/copy/synchronization interfaces.
- [XRT@a75e984:xrt_kernel.h](https://github.com/Xilinx/XRT/blob/a75e9843c875bac0f52d34a1763e39e16fb3c9a7/src/runtime_src/core/include/xrt/xrt_kernel.h), group lookup, run state and documented wait-timeout limitation.

- XRT 2024.1 native API, buffer synchronization and runtime configuration documentation

---

<sub>← [Embedded Platforms for Acceleration](02-embedded-platforms-for-acceleration.md) · [Chapter index](README.md) · [Vitis AI and the DPU (Overview)](04-vitis-ai-and-dpu.md) →</sub>
