# Running Accelerated Applications

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[18 · XRT and Hardware Acceleration](README.md)** · Part VIII: Programmable Logic and Acceleration

## Execution lifecycle

Open the device, load a compatible xclbin, select the kernel, allocate buffer objects for the correct memory groups, populate inputs, synchronize as required, start a run and wait for completion. Synchronize output before the CPU reads it.

A mapped buffer pointer does not guarantee automatic visibility across every device path. Follow the runtime's buffer ownership rules. “Zero-copy” describes avoided copies, not the absence of synchronization.

## Debugging

Use the installed runtime utilities, such as the supported `xbutil` commands, to inspect device and runtime status. `xrt.ini` can enable release-specific diagnostics. Preserve the exact configuration because tracing can change performance.

Validate output against a software reference before measuring speed. Check transfer sizes, kernel arguments, completion status and timeouts. Separate data-movement overhead from compute time.

> [!NOTE]
> **Not run on the reference setup:** an XRT accelerator run or profile.

## References

- XRT 2024.1 native API, buffer synchronization and runtime configuration documentation

---

<sub>← [Embedded Platforms for Acceleration](02-embedded-platforms-for-acceleration.md) · [Chapter index](README.md) · [Vitis AI and the DPU (Overview)](04-vitis-ai-and-dpu.md) →</sub>
