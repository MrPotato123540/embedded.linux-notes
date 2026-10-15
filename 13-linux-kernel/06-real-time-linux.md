# Real-Time Linux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers

## Latency rather than average speed

Real-time work has a deadline. Average CPU use or throughput does not show the worst delay before a task can run. Interrupt handling, non-preemptible sections, memory pressure, drivers and firmware can all add latency.

For a Linux 6.6-based system, verify the exact PREEMPT_RT patch/configuration combination. Do not assume that later mainline real-time support is present in the pinned 2024.1 vendor tree.

## Measuring and tuning

`cyclictest` measures scheduling latency under its test conditions. Run representative CPU, storage, network and DMA load and record the maximum as well as the distribution. A short idle run cannot establish a product deadline guarantee.

CPU isolation, IRQ affinity and threaded interrupts can reduce interference, but move work elsewhere rather than making it disappear. Also check frequency scaling, memory bandwidth and priority inversion.

If the deadline must survive Linux stalls or reboot, place the function on the RPU or in programmable logic with a suitable communication boundary. The complete system still needs timing analysis.

> [!NOTE]
> **Not run on the reference setup:** PREEMPT_RT build and latency benchmark under hardware load.

## References

- Linux 6.6 real-time and scheduler documentation
- [RPU and AMP concepts](../21-rpu-and-openamp/01-amp-concepts.md)

---

<sub>← [Kernel Debugging](05-kernel-debugging.md) · [Chapter index](README.md) · Next chapter: [14 · Kernel Modules and Device Drivers](../14-kernel-modules-and-drivers/README.md) →</sub>
