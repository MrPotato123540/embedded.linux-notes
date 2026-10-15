# DMA Between PS and PL

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Transfer path

A PS–PL DMA design includes the DMA engine, AXI connections, memory mapping, interrupts and software ownership. AXI DMA, VDMA and MCDMA serve different stream patterns. Choose a driver matching the configured IP, including scatter-gather and channel capabilities.

The port and transaction attributes determine whether the transfer participates in cache coherency. Adding `dma-coherent` to the device tree cannot create a coherent hardware path. For non-coherent paths, follow the DMA API's synchronization rules.

## Userspace access

DMA-proxy and u-dma-buf patterns expose different interfaces and ownership models. Review their source version and limitations before adopting one. A mapped buffer still needs synchronization, bounds checking and cleanup when the process exits.

## Measurement

Separate setup cost, transfer time and application processing. Verify data patterns under concurrent CPU and peripheral load. A high throughput figure with stale cache data is invalid.

> [!NOTE]
> **Not run on the reference setup:** hardware DMA correctness and throughput measurements.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/dma/xilinx/`
- [DMA API and memory management](../14-kernel-modules-and-drivers/06-dma-and-memory-management.md)

---

<sub>← [dfx-mgr and Accelerator Packages](05-dfx-mgr.md) · [Chapter index](README.md) · Next chapter: [18 · XRT and Hardware Acceleration](../18-xrt-and-acceleration/README.md) →</sub>
