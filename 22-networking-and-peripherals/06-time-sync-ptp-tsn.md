# Time Synchronization: PTP and TSN

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Synchronization, timestamping and scheduling are separate

The **Precision Time Protocol (PTP)** estimates and corrects clock differences across a network. Hardware timestamping records packet events close to the MAC or PHY boundary. **Time-Sensitive Networking (TSN)** includes mechanisms for traffic scheduling and related deterministic-network behavior. A system can support one of these without supporting every part of the others.

A PTP hardware clock (**PHC**) is a clock exposed by a driver through the Linux PTP subsystem. It is distinct from the Linux system clock. Synchronizing a PHC does not automatically synchronize application calls to `CLOCK_REALTIME`, and synchronizing the system clock does not prove that Ethernet hardware timestamps use it.

The 2024.1 Cadence driver contains `macb_ptp.c`, including PHC registration, adjustment and packet timestamp support. Whether the running interface exposes those capabilities depends on hardware, kernel configuration and driver initialization. A source file in the tree is not a runtime capability report.

The saved QEMU boot capture is more specific: it reports `macb ff0e0000.ethernet: GEM doesn't support hardware ptp.` That observation explains why this emulated interface cannot provide the hardware-PTP evidence needed here. It does not describe the capability of a correctly configured physical ZynqMP board.

## Work the two-way timing calculation

For a simplified original PTP example, let the master send at `t1`, the slave receive at `t2`, the slave send a delay request at `t3`, and the master receive it at `t4`. With equal path delay in both directions and the appropriate protocol corrections, the estimated offset is `((t2 - t1) - (t4 - t3)) / 2`.

Suppose the forward difference is 12 microseconds and the reverse difference is 8 microseconds. The estimated slave offset is 2 microseconds and the mean path delay is 10 microseconds. These are illustrative arithmetic values, not measured ZCU106 performance.

If the actual path delays are unequal, the offset estimate includes half their difference. Hardware timestamping reduces software timestamp uncertainty, but it does not remove physical path asymmetry. Cable paths, switches and traffic behavior can still matter. Use this model to explain residual error rather than assuming every remaining offset is a servo bug.

## The timestamp point defines the measurement

A software transmit timestamp can occur before queueing, driver processing and hardware transmission finish. A hardware timestamp occurs at a hardware-defined event. A receive timestamp has its own event point. Comparing different timestamp types without accounting for their locations produces misleading latency numbers.

Linux provides timestamping options through socket APIs. The application must request supported modes and read timestamps from the correct message path, including the error queue for transmit timestamp delivery where applicable. A normal send completion is not the same event as physical transmission.

The driver may support only particular hardware timestamp filters. A request can be adjusted to a supported filter; inspect the accepted configuration. The existence of `/dev/ptpN` also does not prove that a selected packet stream is being hardware-timestamped. [Linux timestamping documentation](https://www.kernel.org/doc/html/v6.6/networking/timestamping.html).

## A clock servo needs one owner

A PTP daemon such as `ptp4l` can discipline the network-facing clock, while another tool such as `phc2sys` can relate the PHC and system clock. Their exact roles depend on whether the host is master or slave and which clock is the reference.

Do not let several independent services adjust the same clock without a designed relationship. A PTP service and an NTP service can fight over the system clock, creating jumps or frequency corrections that neither expects. Clock ownership belongs in the service configuration and boot order.

Time domains and epochs matter too. PTP time and UTC can differ by the announced offset. A numerically stable clock can still be wrong for an application if the time scale is misinterpreted. Record the domain, role, clock identity, time scale and correction policy with the synchronization result.

## TSN requires the complete traffic path

A time-aware schedule opens and closes transmit opportunities for traffic classes. Linux qdiscs such as `taprio` and `etf` participate in scheduling designs, but software scheduling and hardware offload have different timing limits. A command accepted by a qdisc is not proof that the MAC executes the schedule in hardware.

Match the traffic-class map, queue map, clock and gate schedule to the actual device and driver. Switches on the path must also support the intended behavior. Reserving a transmit window on one endpoint does not bound congestion inside an ordinary unmanaged switch.

Consider an original 1-ms cycle with a 100-microsecond critical window. The application must prepare packets early enough, the scheduler must use the intended clock, and other frames must not overrun the protected interval. Frame size, link speed and guard-time policy therefore affect the usable schedule. A nominal window length is not the same as guaranteed payload time.

## Measure error under the intended load

Collect offset and path-delay statistics over time, including startup, link changes and competing traffic. Report maximum observed error and distribution, not only one quiet steady-state sample. State whether the result compares PHCs, system clocks or application events.

For end-to-end deadlines, measure packet preparation, queueing, transmission, network transit and receiver handling. Good PHC alignment can coexist with late application scheduling. Conversely, a low average application latency does not establish a shared time reference for scheduled actions.

The QEMU Ethernet captures elsewhere in this chapter show ordinary packet exchanges. They do not validate physical timestamp accuracy or TSN hardware scheduling. Emulator timing is influenced by host scheduling and the modeled device behavior.

## Diagnose the failing contract

No PHC suggests hardware capability, configuration or registration issues. PHC present but no packet timestamps suggests socket requests or timestamp-filter support. Stable timestamps with a persistent offset suggest domain, time-scale or path-asymmetry questions. Large jumps after service startup suggest conflicting clock owners or an intended step operation.

A schedule that works only at low load calls for queue mapping, guard time and actual offload evidence. Keep synchronization problems separate from traffic-shaping problems so a tuning change has a clear purpose.

> [!NOTE]
> **Not run on the reference setup:** PTP synchronization, physical timestamp accuracy and TSN scheduling. The timing examples are calculations. The pinned GEM PTP source was inspected without claiming runtime hardware support.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/net/ethernet/cadence/macb_ptp.c`, inspected PHC and timestamp paths.
- [Linux PTP hardware-clock API](https://www.kernel.org/doc/html/v6.6/driver-api/ptp.html).
- [linuxptp project documentation](https://www.linuxptp.org/documentation/), daemon roles and configuration.
- [Linux tc-taprio manual](https://man7.org/linux/man-pages/man8/tc-taprio.8.html), userspace qdisc interface; verify hardware offload with the selected driver.

---

<sub>← [I2C, SPI, UART, CAN and GPIO](05-low-speed-buses.md) · [Chapter index](README.md) · Next chapter: [23 · Storage, Updates and Production](../23-storage-updates-and-production/README.md) →</sub>
