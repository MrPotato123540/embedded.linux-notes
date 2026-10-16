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

## Three addresses describe one buffer

The CPU uses a virtual address to access a kernel allocation. The pages have physical addresses. The device uses a DMA address produced for that particular device. These values may happen to match in a simple system, but that is not the API contract. An IOMMU or bounce buffer can make the device address different.

Keep DMA addresses in `dma_addr_t`. Do not truncate them to a 32-bit register field without proving that the device's address mask and allocation meet that limit. A driver declares supported addressing with the DMA mask API and checks the result. The mask describes what the engine can reach, not how much RAM Linux currently uses.

The mapping must use the `struct device` representing the DMA master. Mapping with an unrelated device can choose different translation, coherency or bounce-buffer behavior. This matters when a platform driver submits work to a separate DMAengine provider.

## Streaming mappings transfer ownership

A streaming mapping is suitable for a payload used for a transfer. For CPU-produced transmit data, the CPU prepares the bytes before mapping or synchronizing for the device. While the device owns the mapping, the CPU must not modify it. Completion returns control through unmapping or the appropriate synchronization call.

For received data, the CPU must wait for completion and synchronize for CPU access before reading. A retained mapping can alternate ownership using the matching synchronization APIs. It must keep the same direction and correct range throughout that protocol. `DMA_TO_DEVICE` and `DMA_FROM_DEVICE` describe data movement relative to main memory and the device, not the caller's informal idea of upload or download.

Mapping can fail. The driver checks `dma_mapping_error()` and does not program an engine with an unchecked result. If a later setup step fails, it unmaps only the mappings that succeeded, with their original size and direction.

## Coherent memory still needs ordering

Coherent allocation removes explicit cache maintenance for the supported CPU/device path. It does not stop the compiler or CPU from publishing fields in an unsafe order. Consider a descriptor with an address, length and an ownership bit. The device must not see the ownership bit before the address and length are ready.

The following is an **illustrative ordering model**, not a complete descriptor format or a tested hardware program:

```text
CPU owns descriptor
    write DMA address and length
    apply the required DMA write barrier
    publish the device-ownership field
    ring the device doorbell using its MMIO protocol
Device owns descriptor
    device completes data movement
    device publishes completion
CPU observes completion
    apply the required DMA read ordering
    consume completion fields and payload under the mapping rules
```

The exact barrier and accessor requirements depend on the shared-memory and MMIO contract. `dma_wmb()` orders suitable shared-memory writes; it does not flush an arbitrary non-coherent streaming mapping. Cache maintenance and ordering solve different problems. A coherent descriptor ring can also refer to non-coherent streaming payloads, so one queue may need both mechanisms.

## Scatter-gather has two counts

A scatter-gather list describes several memory segments. Mapping can merge entries or change their DMA representation. The number of DMA segments returned by `dma_map_sg()` is the number the hardware-facing loop uses. The original number of input entries is used when unmapping the list. Confusing these values can leak mappings or program invalid descriptors.

A hardware engine also has its own segment limits: maximum descriptor length, alignment, boundary restrictions and address width. Successful DMA mapping does not prove that one hardware descriptor can describe the whole returned segment. The driver must obey both the DMA API and the engine's format.

Never map a stack buffer for asynchronous DMA. Its lifetime can end before completion, and stack memory does not meet the normal streaming-buffer assumptions. An arbitrary `vmalloc()` pointer is not a single physically contiguous buffer either. Select an allocation and mapping strategy that matches the transfer.

## CMA solves a specific allocation problem

The Contiguous Memory Allocator (CMA) reserves regions that can support large physically contiguous allocations. Other movable allocations may use the region until a contiguous request needs it. A large amount of total free RAM therefore does not guarantee a suitable contiguous allocation at the required moment.

CMA is not an instruction to skip the DMA API. It does not make a path coherent or give userspace permission to program a bus address. An IOMMU may allow a contiguous device-address view over noncontiguous physical pages, but that capability depends on the device and backend. Do not assume all FPGA or graphics allocations use the same strategy.

Budget memory using simultaneous ownership. For example, four illustrative 8 MiB input buffers plus four 8 MiB output buffers already retain 64 MiB before descriptors, display buffers and kernel use. Doubling queue depth can increase throughput while making contiguous allocation fail during startup.

## Completion, cancellation and removal

A timeout means software has not observed completion. It does not prove that the device stopped accessing memory. Before unmapping or freeing a timed-out buffer, the driver must terminate or reset the engine through a documented sequence and wait until access is impossible. Otherwise the next allocation can receive a late DMA write.

For DMAengine clients, distinguish asynchronous termination from synchronization of callbacks. The pinned client guide documents the relevant APIs and context restrictions. Do not wait for a callback while holding the same lock the callback needs.

Diagnose stale data with known patterns and explicit ownership records. Diagnose address faults with the device-visible address and IOMMU evidence. Diagnose allocation failure with size, mask and contiguous-memory pressure. A slower transfer that returns correct data is a better baseline than a high throughput result with silent corruption.

## References

- [linux-xlnx@xilinx-v2024.1:Documentation/core-api/dma-api-howto.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/core-api/dma-api-howto.rst).
- [DMA API details](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/core-api/dma-api.rst) and [DMAengine client guide](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/dmaengine/client.rst), same pinned tag.

- Linux 6.6 [DMA mapping guide](https://docs.kernel.org/6.6/core-api/dma-api-howto.html)
- `linux-xlnx@xilinx-v2024.1:drivers/dma/xilinx/`

---

<sub>← [Accessing Hardware From User Space](05-user-space-hardware-access.md) · [Chapter index](README.md) · Next chapter: [15 · Root Filesystem and Init](../15-root-filesystem-and-init/README.md) →</sub>
