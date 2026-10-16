# Profiling and Performance

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Measure the bottleneck

Define the workload and output metric before tuning. Throughput, response latency, CPU use and energy are different measurements. Record input size, CPU frequency policy, temperature and concurrent activity.

`top` and `/proc` show broad resource use. `vmstat` helps identify memory and scheduling pressure. `perf` can attribute execution cost when the kernel configuration and permissions support the required events.

## ZynqMP considerations

CPU frequency scaling changes timing. Cache misses and DDR contention can limit a task even when the CPU is not fully busy. PL DMA, display and video traffic can compete with application memory access.

Compare one change at a time and include a correctness check. Faster processing that drops frames or returns stale DMA data is not a valid improvement.

> [!NOTE]
> **Not run on the reference setup:** hardware performance measurements. No QEMU result is presented as Cortex-A53 throughput or DDR bandwidth.

## Define the measured result before collecting counters

Throughput measures completed work per time. Latency measures the time for one unit of work. CPU utilization measures how much processor time is busy. They answer different questions. A design can improve throughput by batching while making individual requests wait longer.

Choose a representative input and a correctness check. For a data pipeline, record bytes or frames accepted and completed, not merely loop iterations. A benchmark that drops work can look faster than a correct implementation. A benchmark that measures only submission time can miss a queue growing behind it.

Separate warm-up from steady state. First use can include page faults, library loading, cache population and accelerator setup. Those costs matter for cold-start latency, but mixing them unpredictably into steady-state samples makes comparison difficult.

## Follow one request through a pipeline

Consider an illustrative request with 2 ms of input preparation, 1 ms of transfer, 1 ms of compute and 2 ms of output processing. Its serial latency is 6 ms. Making compute four times faster reduces that to 5.25 ms, a speedup of only about 1.14 times.

This arithmetic is an example, not a board measurement. It shows why improving the most visible kernel can have little application effect. Measure the full path and optimize the stage that limits the required metric. If stages overlap, use a timeline rather than adding all durations as if they were serial.

Queue depth can hide transfer latency and increase throughput. It also retains more buffers and increases the worst-case wait. Report queue depth with performance results; otherwise two measurements may describe different service quality.

## CPU time and elapsed time separate waiting from work

If elapsed time is high but CPU time is low, investigate blocking I/O, synchronization, scheduling and device waits. If both are high, inspect computation, memory behavior and contention. High CPU utilization alone does not prove useful work: spinning on a status register can keep a core busy while doing little.

Sampling profiles estimate where execution spends time. They do not directly explain every blocked interval. Combine CPU samples with scheduling and I/O evidence when latency is the concern. A hot lock routine can indicate contention elsewhere in the ownership design.

Hardware counters add information about events such as cycles and cache behavior, but event availability and interpretation are processor-specific. Multiplexing too many events can reduce precision. Record the selected events and scaling rather than comparing an unlabeled counter total.

## Measurement changes the workload

Tracing, debug logging and profiling consume CPU time and memory bandwidth. A high-frequency log inside an interrupt or frame loop can become the bottleneck it is trying to observe. Use bounded captures and compare with an uninstrumented correctness-preserving baseline.

CPU frequency policy, thermal limits and background services also affect results. An affinity setting can reduce migration noise but can also create unrealistic contention if all work is pinned to one core. Record the configuration that matters to the performance claim.

The pinned kernel's perf-security documentation explains why access to performance events is controlled. A permission failure is not proof that the PMU is absent. Check policy and required privilege separately from kernel support and event availability.

## Memory traffic often dominates embedded pipelines

An image operation may read an input buffer, write an intermediate buffer, read it again and write output. Even simple arithmetic can therefore generate several times the image size in memory traffic. Removing one copy can help more than reducing a few instructions.

For an illustrative 1920×1080 four-byte pixel image, one full buffer is 8,294,400 bytes before any extra stride padding. Reading and writing it once transfers at least twice that amount at the application-data level. The memory system can carry additional traffic from cache behavior, descriptors and other clients.

Compare this demand with simultaneous display, video and PL DMA activity. A standalone microbenchmark may hide the contention that appears in the product. Shared-memory accelerators compete for the same memory controllers even when compute happens outside the CPU.

## Report distributions and limits

An average can hide rare long delays. Record useful percentiles or a histogram when latency matters, along with sample count and workload. Keep errors and timeouts in the report instead of discarding them as inconvenient outliers.

For throughput, state whether the result includes setup, synchronization, transfers and validation. For power or thermal behavior, use a measurement method appropriate to the board; software CPU utilization is not a power measurement.

> [!NOTE]
> **Not run on the reference setup:** target profiling or throughput measurements. Numerical examples are calculated workload models and must not be quoted as ZCU106 performance results.

## References

- [linux-xlnx@xilinx-v2024.1:Documentation/admin-guide/perf-security.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/admin-guide/perf-security.rst).
- [DMA ownership and allocation](../14-kernel-modules-and-drivers/06-dma-and-memory-management.md) for memory-path limits.

- Linux 6.6 perf, cpufreq and `/proc` documentation
- [Interconnect and coherency](../03-zynqmp-architecture/06-interconnect-coherency-and-smmu.md)

---

<sub>← [Debugging Applications](02-debugging-applications.md) · [Chapter index](README.md) · [System Services and Logging](04-system-services-and-logging.md) →</sub>
