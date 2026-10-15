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

## References

- Linux 6.6 perf, cpufreq and `/proc` documentation
- [Interconnect and coherency](../03-zynqmp-architecture/06-interconnect-coherency-and-smmu.md)

---

<sub>← [Debugging Applications](02-debugging-applications.md) · [Chapter index](README.md) · [System Services and Logging](04-system-services-and-logging.md) →</sub>
