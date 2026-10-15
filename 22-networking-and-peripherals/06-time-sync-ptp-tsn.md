# Time Synchronization: PTP and TSN

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Two clocks to consider

**Precision Time Protocol (PTP)** synchronizes clocks using network messages and timestamps. A supported Ethernet device can provide a PTP hardware clock. `ptp4l` manages PTP operation; `phc2sys` can synchronize between a hardware clock and the system clock in a chosen direction.

Choose the PTP profile, domain, transport and timestamping mode consistently across the network. Hardware timestamps reduce some software timing noise, but do not eliminate cable asymmetry or incorrect network configuration.

## TSN scope

**Time-Sensitive Networking (TSN)** includes several Ethernet mechanisms. Time synchronization alone does not provide traffic scheduling or bounded latency. The MAC, switches, drivers and configuration must support the required mechanisms end to end.

The reference BSP includes `meta-xilinx-tsn`, but that does not make every GEM/PL interface a fully configured TSN endpoint.

> [!NOTE]
> **Not run on the reference setup:** hardware timestamping, clock-offset measurement or TSN latency tests.

## References

- [linuxptp ptp4l manual](https://www.linuxptp.org/documentation/ptp4l/)
- `meta-xilinx-tsn` shipped with the reference BSP

---

<sub>← [I2C, SPI, UART, CAN and GPIO](05-low-speed-buses.md) · [Chapter index](README.md) · Next chapter: [23 · Storage, Updates and Production](../23-storage-updates-and-production/README.md) →</sub>
