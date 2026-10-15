# I2C, SPI, UART, CAN and GPIO

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Bus-specific checks

| Bus | Check before userspace testing |
| --- | --- |
| I2C | Address, pull-ups, voltage, clock rate and driver ownership |
| SPI | Chip select, mode, clock rate, word width and full-duplex behavior |
| UART | Pin route, voltage, baud and flow control |
| CAN | Transceiver, termination, bitrate and controller mode |
| GPIO | Line offset, direction, active polarity and consumer ownership |

I2C probing can have side effects on some devices. Do not scan or force-access a bus used by a live driver without understanding the target device. `spidev_test` requires a compatible device binding and meaningful wiring.

SocketCAN exposes CAN controllers as network interfaces. `candump` can observe frames, but CAN error states and physical termination still need inspection. A local loopback result does not prove an external bus works.

Use libgpiod for supported GPIO character-device access rather than relying on deprecated sysfs examples.

> [!NOTE]
> **Not run on the reference setup:** physical low-speed bus tests.

## References

- Linux 6.6 I2C, SPI, GPIO and [SocketCAN](https://docs.kernel.org/6.6/networking/can.html) documentation

---

<sub>← [PCIe](04-pcie.md) · [Chapter index](README.md) · [Time Synchronization: PTP and TSN](06-time-sync-ptp-tsn.md) →</sub>
