# USB Host and Gadget

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Host and gadget are different roles

A USB host controls bus enumeration and schedules transfers. A USB device, called a **gadget** in Linux's device-side framework, responds to the host and exposes functions such as serial, network or storage. The same controller hardware can support different roles, but connector wiring, PHYs, power control and software must support the selected role.

ZynqMP uses the Synopsys DWC3 controller with AMD platform integration. In the inspected 2024.1 source, `dwc3-xilinx.c` handles platform clocks, resets, PHY setup and power-management details before the child controller operates. `dwc3_xlnx_probe()` reads `dr_mode` from the child node. A parent-only edit can therefore miss the property the implementation actually reads.

A device tree setting is not permission to source power through an unsupported connector. The board's VBUS switch, ID/role signals and USB2/USB3 wiring determine which roles can work safely. Review the schematic before changing role configuration.

## Enumeration is a sequence of observable stages

In host mode, connection detection is followed by reset, descriptor reads, address assignment and configuration selection. Class or device drivers then bind to interfaces. A device may enumerate successfully but lack a Linux function driver. Conversely, a timeout before descriptor reads suggests a lower-level connection, power, reset or PHY problem.

USB3 and USB2 use different signaling paths. A device falling back to a lower speed may still transfer correctly while exposing a problem in the higher-speed path. Record the actual negotiated speed and topology, not only the controller's maximum capability.

A hub introduces another power and scheduling boundary. A device that works directly but fails behind a hub can have power demand, reset timing or topology-specific issues. Compare one variable at a time and retain the cable, hub and power arrangement with the result.

## Transfers have a lifetime

Host drivers submit **USB request blocks (URBs)**. The USB core and host controller own submitted work until completion or cancellation. A driver must not free an URB's buffer while hardware can still access it. Disconnect can race with in-flight work, so cleanup must stop submissions and wait for the supported cancellation path.

Control transfers configure devices. Bulk transfers prioritize correctness and use available bandwidth. Interrupt transfers provide scheduled polling for suitable endpoints. Isochronous transfers reserve timing opportunities but do not provide ordinary retransmission of lost data. Choose a transfer type from the device protocol; userspace cannot turn a bulk endpoint into an isochronous one by increasing buffer size.

For streaming, a larger queue can hide short software delays, but it also increases outstanding memory and possibly latency. If production rate exceeds sustained transfer capacity, buffers eventually fill. Count actual completed bytes and failures rather than submitted bytes alone. [Linux USB driver API](https://www.kernel.org/doc/html/v6.6/driver-api/usb/usb.html).

## A gadget needs descriptors, functions and a controller binding

The Linux composite-gadget framework can assemble functions through configfs when the required kernel support and function drivers exist. A gadget description includes identity strings, configurations and function instances. Binding it to a USB Device Controller (**UDC**) makes it available to the external host.

The sequence matters. Build a coherent configuration first, then bind it. On teardown, disconnect/unbind before destroying resources that an active host can still access. Editing a live function tree without regard to connection state can produce host-visible failures or stale assumptions.

For an original network-gadget example, the USB function exposes a network link, but IP addresses, routes and services still need configuration on both sides. Successful USB enumeration does not prove an SSH service is reachable. It establishes the lower transport boundary only.

Use identifiers appropriate for the product and its authorization. Do not copy another vendor's product identity into a production image merely because a tutorial uses it. The identity is part of how hosts choose drivers and distinguish devices.

## Storage gadgets have a strict ownership problem

A mass-storage gadget exports a backing file or device to another host. The remote host can cache filesystem metadata and data. Linux on the gadget side must not independently mount and modify the same filesystem while it is exported for ordinary block access.

For example, exporting a partition while a local service writes logs into it creates two unsynchronized filesystem owners. Each can make valid changes based on stale metadata and corrupt the other. A file-based transfer service has a different sharing model and can be a better fit when both sides need live access.

Disconnect and host removal also affect durability. The host may still have pending writes. A completed application write on the host is not a universal proof that all storage layers made it persistent. Define safe removal and recovery behavior for the actual product.

## Power management changes the failure pattern

Runtime suspend and resume can expose clock, reset or PHY sequencing bugs that do not appear during initial enumeration. The pinned AMD glue driver has explicit runtime and system power-management paths. If a device works after boot but fails after idle, compare those paths and wakeup settings before replacing application code.

Repeated connect/disconnect tests also exercise cleanup. A memory leak or stale request can remain hidden in a single successful transfer. Track device instances and outstanding requests across cycles, and distinguish host-side failure from gadget-side failure with logs from both ends.

## Diagnose the last completed stage

No physical detection points to connector, power, role and PHY setup. Descriptor errors point to low-level signaling, reset timing or device firmware. A configured interface without a driver points to class support or matching. A bound network function without IP connectivity points to network configuration.

Failures only under throughput load need transfer-size, queue-depth, CPU and memory-bandwidth evidence. Failures only on USB3 need the actual negotiated speed and link error context. A working USB2 fallback narrows the problem but does not validate the USB3 hardware path.

> [!NOTE]
> **Not run on the reference setup:** physical host enumeration, gadget binding, USB power changes and storage export. No backing storage was written or exported. Platform source was inspected for the 2024.1 integration.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/usb/dwc3/dwc3-xilinx.c`, inspected role, PHY, reset and power-management paths.
- [Linux USB gadget configfs documentation](https://www.kernel.org/doc/html/v6.6/usb/gadget_configfs.html).
- [Linux mass-storage gadget documentation](https://www.kernel.org/doc/html/v6.6/usb/mass-storage.html).

---

<sub>← [Network Configuration on the Target](02-network-configuration.md) · [Chapter index](README.md) · [PCIe](04-pcie.md) →</sub>
