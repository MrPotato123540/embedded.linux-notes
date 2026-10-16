# PCIe

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Identify the controller and its role first

**PCI Express (PCIe)** connects a root complex to endpoints through a serial link. A root complex enumerates devices and assigns address resources. An endpoint exposes functions and base-address registers (**BARs**) to that host. These roles require different software and hardware configuration.

On ZynqMP, the processing-system PCIe path and a PCIe block instantiated in programmable logic are different controllers. Do not choose a driver from the word Xilinx alone. Match the hardware design and device-tree compatible string to the exact implementation.

The inspected 2024.1 processing-system host driver is `drivers/pci/controller/pcie-xilinx-nwl.c`, with binding `xlnx,nwl-pcie.yaml`. It provides host initialization, configuration-space access and interrupt support for that controller. Its existence does not prove that the same driver implements endpoint mode or every PL PCIe design.

## Link training comes before enumeration

The two ends need compatible lane configuration, reference clocking, reset timing and electrical connectivity. Link training establishes the negotiated width and speed. Only then can the host reliably access endpoint configuration space.

A trained link is necessary but not sufficient for a usable function. The host still needs bus numbers and address windows. A driver still needs a matching device ID and working resources. Separate these stages in the log: controller probe, link state, device enumeration, BAR assignment, driver probe and application traffic.

A device can enumerate at a lower width or speed than intended. That may be functional but reduce throughput or reveal a marginal lane. Record negotiated values under the actual board, cable/adapter and endpoint arrangement. A capability register showing a maximum is not the current link result.

## There are several address spaces

A CPU virtual address, CPU physical address, PCIe bus address and device DMA address may differ. A host bridge's outbound windows translate CPU accesses toward endpoint BAR space. Inbound DMA from an endpoint follows its own mapping and protection path.

The device tree's `ranges` describes host-bridge address windows. `dma-ranges`, where relevant to the integration, describes DMA address relationships. An Arm SMMU can add another translation and access-control layer. Review the actual controller binding and DMA topology rather than assuming identity mappings.

For an original example, Linux can map a BAR and read a device identity register successfully while DMA still fails. The BAR read exercises CPU-to-endpoint access. DMA exercises endpoint-to-memory access, its address width, mappings and permissions. One successful direction does not validate the other.

## BAR access is not a DMA API

A BAR describes an endpoint resource. The PCI core assigns it within available windows. Drivers request and map that resource through the kernel interfaces, then use the appropriate memory-mapped I/O accessors. Ordinary pointer dereferences do not express all required device-access semantics.

For DMA, the driver establishes a supported DMA mask, allocates or maps buffers through the DMA API and gives the resulting device address to hardware. A CPU pointer or guessed physical address is unsafe and can work accidentally on one system while failing with an SMMU or different memory placement.

The driver must retain the buffer and mapping until the device finishes. Unmapping early can produce corruption after the application thinks the transfer ended. A timeout does not itself prove hardware stopped; reset and quiesce the device through its documented path before releasing resources that it may still access.

## Interrupt delivery is another independent path

Legacy INTx and **Message Signaled Interrupts (MSI)** use different mechanisms. MSI represents an interrupt through a memory-write transaction to a configured address/data pair. Linux allocates vectors and connects them to handlers through the PCI interrupt APIs.

The NWL driver contains MSI allocation and interrupt-domain support. If a device can DMA data but completions never reach its driver, inspect vector allocation, endpoint interrupt enablement and host delivery. Polling a completion register can help distinguish missing interrupt notification from missing device progress, when the device documentation permits that observation.

Do not hard-code Linux IRQ numbers from one boot. The kernel allocates them dynamically. A device's hardware interrupt source and its Linux IRQ number belong to different namespaces, just as PCI bus and CPU addresses do.

## Work a bounded DMA review

Suppose a teaching endpoint transfers 64 buffers of 1 MiB each. Its driver must account for 64 MiB of payload storage, descriptor storage and mapping limits. If the endpoint accepts only a narrower DMA address range, an allocation above that range needs a supported mapping strategy; truncating the address is corruption.

Next define completion semantics. Does the device signal each buffer or a batch? Can completions arrive out of order? What prevents the application from modifying a transmit buffer while the endpoint reads it? These are device-protocol questions that the generic PCI core cannot answer.

Finally define reset behavior. Pending writes, descriptor ownership and interrupt state must converge to a known condition before resources are reused. A link reset may remove a function while an application still holds its file descriptor. The driver must reject new work and clean up the old instance safely.

## Diagnose by boundary

No host bridge suggests driver, clocks, resets, PHY or device-tree problems. No trained link suggests hardware lane/clock/reset issues. A link with no function suggests enumeration/configuration access. A function with unassigned BARs suggests address-window capacity. A bound function with failed DMA suggests mappings, masks, descriptors or endpoint logic.

If transfers work but throughput is low, compare negotiated link rate, payload size, completion behavior and software queue depth. Sequential bulk throughput and small-request latency stress different parts of PCIe. Include both only when the application needs both; one headline bandwidth number does not characterize the device.

> [!NOTE]
> **Not run on the reference setup:** physical PCIe enumeration, BAR access, DMA, MSI and reset tests. No device registers were read or written. The controller and binding paths were inspected in pinned source.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/pci/controller/pcie-xilinx-nwl.c` and `Documentation/devicetree/bindings/pci/xlnx,nwl-pcie.yaml`.
- [Linux PCI driver guide](https://www.kernel.org/doc/html/v6.6/PCI/pci.html).
- [Linux DMA API guide](https://www.kernel.org/doc/html/v6.6/core-api/dma-api-howto.html).

---

<sub>← [USB Host and Gadget](03-usb.md) · [Chapter index](README.md) · [I2C, SPI, UART, CAN and GPIO](05-low-speed-buses.md) →</sub>
