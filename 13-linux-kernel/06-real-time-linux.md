# Real-Time Linux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers


## A deadline needs a latency budget

A real-time requirement states when a result must be ready. Average CPU utilization and throughput do not establish that requirement. A system can process many requests per second while occasionally delaying one request beyond its deadline.

Break the end-to-end path into event detection, interrupt delivery, handler work, task wakeup, scheduling, application processing and output completion. Add communication and device delays where they apply. The total deadline applies to that full path, not only the time a benchmark thread spends waiting to run.

For example, an illustrative 1-millisecond control deadline might include sensor transfer, wakeup, computation and actuator transfer. A 40-microsecond scheduling measurement leaves most of the path unmeasured. These numbers are a design example, not results from the reference board.

## PREEMPT_RT changes where work can be preempted

**PREEMPT_RT** reduces important sources of non-preemptible execution. It moves much interrupt-related work into schedulable contexts and changes several lock implementations. This can reduce interference for a high-priority task, but it does not make every hardware or firmware operation bounded.

On an RT kernel, `spinlock_t` uses a different implementation with sleeping-lock behavior, while `raw_spinlock_t` remains a strict spinning primitive. Driver code must follow the correct context rules. Replacing locks blindly can break interrupt handling or create a new latency problem.

Priority inheritance helps when a high-priority task waits for a lock owned by a lower-priority task: the owner can temporarily receive a higher priority so it can release the lock. It cannot preempt a region where preemption or interrupts are truly disabled, and it does not remove the work inside the critical section.

These semantics are documented in the Linux 6.6 locking rules and implemented through the relevant RT locking paths. Review driver assumptions as part of adopting RT, especially code that mixes explicit interrupt disabling with ordinary spinlocks.

## The 2024.1 release boundary matters

The reference recipe selects AMD Linux 6.6.10. Do not infer that it has a complete, enabled PREEMPT_RT configuration because a newer Linux release includes more RT work. The Linux RT project publishes separate 6.6 patch series, and a suitable vendor integration needs an exact compatible baseline.

Record the source commit, RT patch/integration revision, final configuration and toolchain. A patch that applies with offsets or manual conflict fixes needs review of the affected semantics, not only a successful build.

This section does not claim that the supplied BSP kernel is an RT kernel. No new PREEMPT_RT image or latency result was produced for the reference setup.

## Scheduling policy and dependency priority must agree

A high-priority application can still wait for a lower-priority interrupt thread, worker or service. Raising only the application's priority can make the system worse if it consumes the CPU needed by its own dependency.

Map the whole chain: device interrupt, driver completion, worker, application and output path. Assign priorities from the deadlines and blocking relationships. Include management and recovery work so that a runaway real-time task does not prevent the system from diagnosing or stopping it.

Avoid unbounded loops in a real-time thread. A task should block or yield according to its design and handle overload explicitly. A priority setting is not a substitute for a bounded algorithm and known input limits.

## Memory behavior belongs in the timing design

Page faults, allocation, reclaim and storage access can add large or variable delays. A critical path should use preallocated memory and a deliberate page-residency plan where appropriate. Touching memory before the measured operation can separate first-use faults from steady-state behavior.

This still does not remove shared-memory-system interference. Other CPUs and DMA engines compete for cache and DDR resources. A CPU-isolated task can experience memory-bandwidth pressure even when no other task runs on its core.

On ZynqMP, firmware calls can also add latency outside the Linux scheduler's direct control. A clock or power operation that enters TF-A and PMU management needs its own timing analysis. PREEMPT_RT cannot schedule around all time spent in higher-privilege firmware.

## Isolation moves work; it does not delete it

CPU affinity, interrupt affinity and housekeeping placement can reduce interference on a selected core. The displaced work must still run somewhere, and overloaded housekeeping CPUs can delay services the isolated task depends on.

Check device queues, interrupt routing, timer behavior and kernel workers together. Also check frequency and idle-state policy under the actual workload. A benchmark at a fixed high frequency does not characterize a product that enters deeper idle states or changes frequency dynamically.

Use an explicit system load model. Include network traffic, storage activity, DMA, thermal conditions and the other processor domains that the product uses. A short idle test misses many shared-resource effects.

## Measure the right quantity

`cyclictest` measures wakeup/scheduling latency under its selected conditions. It is useful for comparing configurations, but its maximum observed delay is not a mathematical guarantee for all future workloads.

Record duration, CPU set, priority, timer interval, memory behavior, background load, firmware versions and temperature/power conditions. Keep the latency distribution and worst observed outliers. When an outlier occurs, correlate scheduler, interrupt and relevant device traces rather than reporting only one summary number.

For the product deadline, measure the physical or application-level input-to-output path as well. A GPIO or hardware timestamp can reveal delays that a userspace wakeup test never sees. Calibrate the measurement overhead and clock relationship.

## Decide when Linux is outside the required fault boundary

If a function must meet its deadline while Linux stalls or reboots, moving that function to an R5 or programmable logic can provide a more suitable execution boundary. The design still needs bounded communication, independent resource ownership and a safe response when Linux disappears.

An R5 that depends on Linux to refresh its shared buffer or maintain its clock is not independent of Linux failure. Specify what continues, what stops and how stale commands are detected. The architecture choice must follow the failure and timing requirement.

> [!NOTE]
> **Not run on the reference setup:** an RT kernel build, physical latency benchmark or loaded end-to-end deadline test. QEMU boot success is not used as timing evidence for the ZCU106 hardware.

## References

- [Linux 6.6 lock types and PREEMPT_RT rules](https://docs.kernel.org/6.6/locking/locktypes.html).
- [Linux RT project's 6.6 series](https://www.kernel.org/pub/linux/kernel/projects/rt/6.6/), baseline-specific patch availability.
- `linux-xlnx@xilinx-v2024.1:kernel/locking/rtmutex.c` and local `linux-xlnx_2024.1.bb`.
- [RPU and AMP concepts](../21-rpu-and-openamp/01-amp-concepts.md).

---

<sub>← [Kernel Debugging](05-kernel-debugging.md) · [Chapter index](README.md) · Next chapter: [14 · Kernel Modules and Device Drivers](../14-kernel-modules-and-drivers/README.md) →</sub>
