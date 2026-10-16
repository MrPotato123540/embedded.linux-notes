# I2C, SPI, UART, CAN and GPIO

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Start with ownership and electrical behavior

I2C, SPI, UART, CAN and GPIO have different bus rules, but they share one integration problem: the hardware export, pin routing, Linux driver and board circuit must describe the same signals. A controller can probe successfully while its external pins are unconnected or routed through an unavailable PL design.

**Multiplexed I/O (MIO)** routes processing-system signals directly to device pins. **Extended MIO (EMIO)** routes them through programmable logic. Selecting EMIO creates a dependency on the PL implementation and its configuration lifetime. A Linux controller driver cannot create the missing PL connection.

The pinned 2024.1 drivers include `i2c-cadence.c`, `spi-cadence.c`, `xilinx_uartps.c`, `xilinx_can.c` and `gpio-zynq.c`. They serve different Linux subsystems, with different userspace interfaces and locking rules. Avoid replacing those interfaces with raw register access while the kernel owns the device.

## I2C transactions are not arbitrary byte streams

**Inter-Integrated Circuit (I2C)** uses addressed transactions on shared clock and data wires. Devices commonly use a register-address write followed by a read. Some require a repeated START between these parts; two separate transfers with a STOP between them may change the operation.

Linux's I2C transfer API can express combined messages. SMBus helper operations are related but do not cover every possible I2C device protocol. Select the operation from the device data sheet, including address width, register width and byte order.

For an original sensor example, a two-byte big-endian register value must be assembled in the documented order. A little-endian CPU does not change the wire order. A plausible but reversed value can be more dangerous than an obvious bus error.

A NACK can mean no device at the address, an unpowered device, an unsupported operation or a device that is temporarily busy. A stuck-low line suggests another class of problem, including a device stopped mid-transaction or an electrical fault. Do not use an indiscriminate bus scan on a live production bus: probe operations can have side effects on some devices. [Linux I2C protocol](https://www.kernel.org/doc/html/v6.6/i2c/i2c-protocol.html).

## SPI needs mode, framing and chip-select agreement

**Serial Peripheral Interface (SPI)** has no universal discovery or addressing protocol. The device tree describes which device is attached to each chip select. Clock polarity and phase, bits per word, maximum clock rate and chip-select timing must match the peripheral.

A protocol can require several transfers while chip select remains asserted. Linux represents related transfers in a message. Splitting that sequence into unrelated userspace operations can insert a chip-select gap and reset the peripheral's command parser.

Reading all zeros or all ones does not uniquely identify a software bug. Check power, chip select, pin routing, mode and return-data activity. A logic analyzer is useful because it shows whether the wire transaction matches the intended command. Increasing delays can hide timing faults without explaining them.

Use a proper kernel device binding for known hardware. `spidev` is a userspace SPI access interface, not a generic production-compatible identity for every chip. Its use and device binding must follow the selected kernel's rules. [Linux SPI userspace API](https://www.kernel.org/doc/html/v6.6/spi/spidev.html).

## UART has framing and flow-control state

A **Universal Asynchronous Receiver/Transmitter (UART)** sends framed characters at an agreed baud rate. Data bits, parity and stop bits must match at both ends. A wrong reference clock can make an apparently correct divisor produce the wrong physical baud rate.

Hardware flow control adds another dependency. If a transmitter waits for a CTS signal that is absent or incorrectly routed, application writes can block or stop progressing. Disabling flow control may be a useful controlled test, but the final configuration must match the wiring and expected traffic.

The Linux tty layer also has line-discipline settings. Canonical processing, echo and character translations are useful for terminals but can corrupt a binary protocol. A serial console and an application should not independently own the same port. Kernel logs mixed into a device protocol can look like random input corruption.

## CAN has arbitration and error state

**Controller Area Network (CAN)** provides message arbitration and error detection on a shared bus. The controller needs a suitable external transceiver, correct termination and a bit-timing configuration derived from the actual controller clock.

Linux SocketCAN represents CAN through the networking stack. An application uses CAN frames and interface state rather than a private serial byte stream. Classical CAN and CAN FD are distinct capabilities; the selected controller instance and driver support determine which are available.

A transmitted frame needs another active node to acknowledge it. A lone node can accumulate transmit errors even when its local transmitter works. Bus-off is a defined error state, not simply a lost application socket. Recovery policy must consider why errors occurred, not only restart the interface repeatedly. [Linux SocketCAN documentation](https://www.kernel.org/doc/html/v6.6/networking/can.html).

## GPIO is a leased line, not a fixed global number

**General-purpose I/O (GPIO)** lines have direction, polarity and ownership. The modern character-device interface identifies a chip and line offset and holds a request while the user owns it. Global numeric GPIO identifiers from older interfaces are not stable board identities.

Active-low describes logical meaning, not necessarily the raw electrical level shown by a meter. Open-drain behavior and external pulls also matter. Releasing a line request can return control to another owner or default state, so define safe output behavior across process exit and reboot.

Do not request a line already used for a regulator, reset, chip select or interrupt. A pin visible in a schematic may belong to a kernel-managed function. Changing it can reset a peripheral while its driver has work in flight.

## Build a diagnosis from wire to application

For every bus, record the controller, pin route, external component, clock, protocol settings and owner. Compare a known transaction with the wire trace and driver result. If the trace is wrong, inspect configuration and scheduling. If the trace is correct but the reply is wrong, inspect device state, timing and interpretation.

> [!NOTE]
> **Not run on the reference setup:** physical bus transfers, scans, GPIO changes and electrical measurements. No live peripheral was probed. The examples explain protocol boundaries and pinned driver locations.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/i2c/busses/i2c-cadence.c`, `drivers/spi/spi-cadence.c`, `drivers/tty/serial/xilinx_uartps.c`, `drivers/net/can/xilinx_can.c`, `drivers/gpio/gpio-zynq.c`, inspected locally.
- [Linux GPIO character-device API](https://www.kernel.org/doc/html/v6.6/driver-api/gpio/using-gpio.html).

---

<sub>← [PCIe](04-pcie.md) · [Chapter index](README.md) · [Time Synchronization: PTP and TSN](06-time-sync-ptp-tsn.md) →</sub>
