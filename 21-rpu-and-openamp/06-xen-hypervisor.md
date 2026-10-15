# Xen Hypervisor (Overview)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Virtualization boundary

Xen runs at the hypervisor level and partitions processor, memory and device resources between domains. Linux guests can share a managed platform while a specialized domain runs another workload.

Virtualization is useful when software isolation and lifecycle separation justify its complexity. It does not automatically make a guest real-time or safely isolate every DMA-capable device. Device assignment needs interrupt, memory and IOMMU consideration.

## Firmware access

A guest may use a hypervisor-mediated firmware interface instead of issuing direct SMC requests. Its device tree and call method must match the hypervisor's implementation. Copying the bare-metal Linux tree into a guest can expose resources the guest does not own.

Test domain startup, shutdown, device reset and failure recovery. Keep a record of which domain owns each peripheral and which services are shared.

> [!NOTE]
> **Not run on the reference setup:** Xen domains or passthrough on ZynqMP hardware.

## References

- Xen Arm documentation for the selected release
- Reference `meta-virtualization` and `packagegroup-petalinux-xen` recipes

---

<sub>← [IPI and Shared Memory Patterns](05-ipi-and-shared-memory.md) · [Chapter index](README.md) · Next chapter: [22 · Networking and Peripherals](../22-networking-and-peripherals/README.md) →</sub>
