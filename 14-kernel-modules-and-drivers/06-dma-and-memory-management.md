# DMA, CMA and Memory Management

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[14 · Kernel Modules and Device Drivers](README.md)** · Part VI: Linux Kernel and Drivers

## DMA address and ownership

**Direct Memory Access (DMA)** lets a device transfer data without the CPU copying every byte. A DMA address is the address returned for that device by the DMA API. It need not equal a CPU virtual or physical address, especially with an IOMMU.

Coherent allocations simplify cache visibility but still need correct ordering. Streaming mappings require ownership transitions and the proper direction. Check mapping failures and synchronize before the CPU or device reuses a buffer. Do not use `virt_to_phys` as a general DMA mapping API.

## Buffer mechanisms

| Mechanism | Purpose |
| --- | --- |
| DMAengine | Common client interface for supported DMA controllers |
| CMA | Contiguous Memory Allocator for suitable large allocations |
| Reserved memory | Keep ranges for defined users |
| dma-buf | Share buffers between participating drivers |

AXI DMA, VDMA, MCDMA and ZynqMP DMA have different capabilities and driver bindings. A descriptor format or transfer constraint from one does not apply to all.

Zero-copy means avoiding a particular copy, not eliminating ownership, synchronization or lifetime rules. Before exposing a buffer to userspace, define who may access it during a transfer and what happens when the process exits.

> [!NOTE]
> **Not run on the reference setup:** physical DMA and cache-coherency stress tests.

## References

- Linux 6.6 [DMA mapping guide](https://docs.kernel.org/6.6/core-api/dma-api-howto.html)
- `linux-xlnx@xilinx-v2024.1:drivers/dma/xilinx/`

---

<sub>← [Accessing Hardware From User Space](05-user-space-hardware-access.md) · [Chapter index](README.md) · Next chapter: [15 · Root Filesystem and Init](../15-root-filesystem-and-init/README.md) →</sub>
