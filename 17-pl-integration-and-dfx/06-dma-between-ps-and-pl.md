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

## The stream and memory sides have different contracts

An AXI DMA engine connects a memory interface with a streaming interface. The memory side uses addresses and lengths. The stream side uses handshakes and packet/frame conventions. Correct memory allocation does not guarantee that the stream producer supplies the expected end-of-packet signal or that the consumer accepts data.

AXI VDMA and MCDMA add different frame/channel models. The compatible string and generated properties must describe the configured IP. Driver support for a family does not mean every mode, address width or channel arrangement is enabled in one hardware instance.

The pinned `drivers/dma/xilinx/xilinx_dma.c` reads hardware-description properties including `xlnx,addrwidth`. That input affects the supported addressing model. A stale device-tree value can make large-memory configurations fail even when small buffers appeared to work during initial tests.

## Follow a DMAengine client request

A client requests the intended channel through the DMAengine interface. It allocates or obtains a payload buffer, maps it for the channel's DMA device and prepares a transaction using the supported channel API. Submission returns a cookie that identifies the queued transaction. Issuing pending work starts eligible queued activity.

The completion callback signals software that the transaction reached its completion path. The client still follows the DMA ownership protocol before the CPU reads received data or rewrites transmitted data. A callback is not permission to ignore cache synchronization for a retained streaming mapping.

Preparation, submission and issue-pending are separate stages. A prepared descriptor that is never issued cannot produce a completion. A submitted cookie also does not prove that the hardware started if the channel is halted or another transfer is blocking progress.

## Read the provider's interrupt path

`xilinx_dma_irq_handler()` reads channel status, rejects interrupts with no relevant status, and acknowledges the asserted interrupt classes. On errors, it distinguishes recoverable conditions under the configured behavior from errors that mark the channel faulty. Its diagnostic includes status and descriptor-pointer information.

On completion-related status, the handler updates descriptor state under the channel lock and starts eligible pending work. It then schedules deferred processing through a tasklet. This explains why a raw interrupt count and an application callback count need not be identical at every instant.

The driver's internal synchronization protects its queue. It does not protect an application's separate buffer queue. The client must still ensure that the same payload is not handed to a producer while the DMA engine owns it.

## Cache coherency is an end-to-end property

A coherent path requires the correct PS–PL connection and transaction attributes, along with matching software description. The `dma-coherent` property tells Linux about that hardware property. It cannot create it.

For a non-coherent receive buffer, device writes may not be visible through an old CPU cache line until the DMA API returns ownership to the CPU. For a transmit buffer, dirty CPU data may not yet be visible to the device. Incorrect behavior can depend on load and cache state, making a simple one-transfer test misleading.

Do not infer coherency because a control register read works or because CPU and device use the same physical DDR. MMIO control and cached payload memory have different rules. Also separate descriptor ordering from payload cache maintenance, as described in chapter 14.

## A worked buffer-ring model

Consider four illustrative receive buffers. Each buffer has one state: available to the device, active in DMA, completed for CPU processing, or held by the consumer. A buffer returns to the device only after the consumer releases it and the required synchronization completes.

If the consumer is slower than the source, the ring fills. The design needs backpressure, bounded dropping or another explicit policy. Reusing the oldest buffer while the consumer still reads it produces torn data, not additional throughput.

Attach a sequence number and expected pattern to test data. Check length, ordering and content for every completed buffer. Run with enough variation to exercise ring wrap and concurrent CPU traffic. These are proposed hardware tests, not results from this revision.

## Cancellation must stop access before reuse

The pinned provider's termination path attempts to stop the channel, resets it and frees queued descriptor state. It also has a synchronization callback for deferred work. The client must use the DMAengine termination/synchronization APIs under their documented context rules.

A timeout alone does not authorize unmapping or freeing the payload. Hardware may still write after software stops waiting. A failed stop/reset operation requires a stronger recovery state that prevents memory reuse while access remains possible.

Do not hold a client lock while waiting for a callback that requires the same lock. This common shutdown deadlock appears only under load or process exit and is easy to miss in a successful single-transfer example.

## Separate throughput from correctness

Measure setup, transfer, callback latency and CPU processing separately, then report end-to-end results. Include direction, buffer size, queue depth, stream behavior and concurrent traffic. A transfer counter increasing does not prove the payload is correct.

If interrupts arrive but data is stale, investigate synchronization and buffer reuse. If no interrupt arrives and status reports an error, inspect addresses, descriptors and stream protocol. If the engine waits with no error, investigate backpressure and missing packet completion before blaming interrupt routing.

## References

- [linux-xlnx@xilinx-v2024.1:drivers/dma/xilinx/xilinx_dma.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/dma/xilinx/xilinx_dma.c), probe, interrupt, submission and termination paths.
- [Pinned DMAengine client guide](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/dmaengine/client.rst).

- `linux-xlnx@xilinx-v2024.1:drivers/dma/xilinx/`
- [DMA API and memory management](../14-kernel-modules-and-drivers/06-dma-and-memory-management.md)

---

<sub>← [dfx-mgr and Accelerator Packages](05-dfx-mgr.md) · [Chapter index](README.md) · Next chapter: [18 · XRT and Hardware Acceleration](../18-xrt-and-acceleration/README.md) →</sub>
