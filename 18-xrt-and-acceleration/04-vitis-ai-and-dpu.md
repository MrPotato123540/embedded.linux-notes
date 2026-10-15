# Vitis AI and the DPU (Overview)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[18 · XRT and Hardware Acceleration](README.md)** · Part VIII: Programmable Logic and Acceleration

## DPU inference flow

A **Deep Learning Processing Unit (DPU)** executes supported neural-network operations in programmable logic. The deployed model must be compiled for the actual DPU architecture and tool/runtime combination.

The flow includes model preparation, quantization where required, compilation, deployment and execution through the supported Vitis AI Runtime (**VART**). Preprocessing and postprocessing often remain on the CPU and can dominate total latency.

## Integration

Include matching DPU hardware, device-tree/runtime support and model artifacts in the platform release. A model compiled for another DPU configuration may be rejected or unsupported. Operators outside the hardware's capability need an explicitly supported alternative path.

Measure end-to-end accuracy and latency using representative input. A kernel execution time alone excludes camera input, conversions, transfers and result handling.

> [!NOTE]
> **Not run on the reference setup:** DPU synthesis, model compilation and hardware inference. Vitis AI compatibility must be checked for the chosen release and DPU; PetaLinux 2024.1 alone does not specify it.

## References

- AMD [Vitis AI documentation](https://xilinx.github.io/Vitis-AI/)
- XRT documentation for the selected runtime

---

<sub>← [Running Accelerated Applications](03-running-accelerated-applications.md) · [Chapter index](README.md) · Next chapter: [19 · Graphics and Display](../19-graphics-and-display/README.md) →</sub>
