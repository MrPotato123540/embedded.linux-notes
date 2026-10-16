# Ethernet (GEM)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Follow a packet through the hardware boundary

The processing system's **Gigabit Ethernet MAC (GEM)** handles Ethernet frame transfer. A **media access controller (MAC)** is distinct from the external physical-layer device, or PHY, that handles the electrical link. Linux also needs clock/reset configuration, the MAC-to-PHY interface description and a working DMA path.

On the reference image, the captured `networkctl` report identifies `platform-ff0e0000.ethernet` with driver `macb`. The 2024.1 implementation is the Cadence MACB/GEM driver in `drivers/net/ethernet/cadence/macb_main.c`. Its shared source supports several hardware variants, so a capability present somewhere in the source is not automatically present in every ZynqMP GEM instance.

For transmit, Linux gives the driver a packet buffer. The driver maps its data for DMA, fills descriptors and hands them to hardware. Completion allows mappings and buffers to be released. For receive, the driver provides empty buffers; hardware fills them and returns descriptor ownership; the driver passes received packets into the networking stack.

## Descriptor ownership is the core data path

A descriptor describes a buffer to hardware. The CPU must finish its descriptor writes before making the descriptor available. On completion, the driver must observe hardware state before reusing the buffer. The DMA API handles address mapping and required cache operations for the platform; a userspace virtual pointer is not a valid DMA address.

The receive path uses polling through the networking **NAPI** mechanism to process work in batches. Interrupts schedule work rather than requiring every received frame to be fully handled in the interrupt handler. This reduces interrupt overhead under load, but also means interrupt counts are not packet counts.

A receive drop can happen before a packet reaches a socket: missing descriptors, DMA errors, ring pressure or networking backlog can each lose data. Application counters alone cannot identify which layer dropped it. Compare hardware/driver statistics with interface and application statistics. [Pinned driver](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/net/ethernet/cadence/macb_main.c).

## Link negotiation does not validate board timing

The PHY uses its management interface to report and configure link state. The MAC driver coordinates PHY and MAC settings through phylink in this release. `macb_phylink_connect()` and the MAC link callbacks show where connection and speed/duplex changes enter the driver.

The device tree must describe the correct PHY connection and `phy-mode`. RGMII delay choices describe where clock/data timing adjustment is expected. Adding delay at both ends or neither end can cause marginal operation. Do not copy `rgmii-id` or another mode from a different board without checking PCB routing and the PHY configuration.

An illuminated link LED proves only part of the path. The PHY may negotiate with the cable partner while the MAC-to-PHY timing is wrong. Such a board can show carrier yet drop frames, fail only at a higher speed or change behavior with temperature.

The pinned `cdns,macb.yaml` binding describes the properties accepted by the Linux driver. The schematic, PHY data sheet and exported hardware configuration determine their correct values for the board.

## Read the available evidence precisely

An existing QEMU capture recorded:

```text
Path: platform-ff0e0000.ethernet
Driver: macb
MTU: 1500 (min: 68, max: 10222)
QDisc: mq
```

This is trimmed from `reference-setup/captures/cap-wp01-net.txt`, outside the repository. It establishes the emulated image's driver binding and reported interface limits. It does not validate an actual PHY, RGMII timing or physical jumbo-frame support.

The same capture contains an `ethtool` capability report. Capability lists describe what the driver/PHY reports; the negotiated speed and duplex are separate observations. A list including 1000-Mbit/s modes is not a measured throughput result.

The captured U-Boot log also warns that it selected a random MAC address. Production identity needs a stable, unique assignment from the board or provisioning design. A changing MAC can alter DHCP leases and network policy even when the driver and IP configuration are unchanged.

A later packet capture recorded two ICMP requests and two replies between `10.0.2.15` and `10.0.2.2`. That proves a short IP exchange through the QEMU network path at that time. It does not establish sustained throughput, packet-loss behavior or real cable operation.

## Calculate packet rate as well as byte rate

For an illustrative 1-Gbit/s link, dividing by eight gives a raw bit-rate ceiling of 125 MB/s before framing and protocol overhead. Small packets stress descriptors, interrupts and per-packet work more than large packets with the same payload byte rate.

A workload carrying 100 bytes per application message at 100,000 messages/s has only 10 MB/s of application payload, yet it needs 100,000 message-processing events plus protocol work. A large sequential transfer with similar byte rate can be much easier. Report packet size, protocol, direction and number of flows with every performance result.

Offloads change where checksums or segmentation happen. A packet capture on the transmitting host can show a checksum before hardware fills it. Do not call that wire corruption without a capture point that observes the completed transmitted frame.

## Separate physical, driver and network causes

No netdev suggests probe, clocks, reset, device-tree or kernel configuration problems. A netdev without carrier suggests PHY discovery, cable, link configuration or board timing. Carrier with no local IP exchange suggests addresses, routes, neighbor discovery, VLANs or filtering, while receive error counters can still expose a lower-layer problem.

Failures only under load call for ring statistics, CPU load, packet rate and memory pressure. Failures after suspend or reset call for restoration of clocks, PHY state and descriptors. Changing ring size can absorb a burst but cannot fix a permanently overloaded consumer.

For a custom board, retain the actual PHY identifier, PHY address, link mode, device-tree node and board revision. Those facts distinguish a software regression from a change in strapping, routing or component population.

> [!NOTE]
> **Not run on the reference setup:** physical Ethernet, signal-integrity, sustained-throughput and hardware timestamp tests. Existing QEMU captures were read; their scope is limited to the emulated network path.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/net/ethernet/cadence/macb_main.c` and `Documentation/devicetree/bindings/net/cdns,macb.yaml`, inspected locally.
- [Linux 6.6 phylink documentation](https://www.kernel.org/doc/html/v6.6/networking/sfp-phylink.html).
- Existing `xilinx-zcu106-2024.1` QEMU captures `cap-wp01-net.txt` and `cap-wp01-net2.txt`.

---

<sub>[Chapter index](README.md) · [Network Configuration on the Target](02-network-configuration.md) →</sub>
