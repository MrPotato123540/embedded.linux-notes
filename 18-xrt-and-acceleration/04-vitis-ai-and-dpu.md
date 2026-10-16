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

## Use the documented 2024.1 compatibility combination

Vitis AI release numbers do not directly match PetaLinux release numbers. AMD's Vitis AI 4.0 release notes identify Vitis AI 3.5 tools together with the DPU IP supplied on the 4.0 branch as compatible with Vivado, Vitis and PetaLinux 2024.1. The same notes say the runtime and library were updated around XRT 2024.1. Use that stated combination as a starting point and retain the exact artifacts. [Vitis AI 4.0 release notes](https://github.com/Xilinx/Vitis-AI/releases/tag/v4.0).

This does not mean an arbitrary 3.5 prebuilt board image or model is compatible with every 2024.1 custom platform. The notes also distinguish which IP, reference designs and prebuilt images changed. Hardware configuration and target architecture remain required checks.

## Quantization changes the numerical contract

A trained floating-point model describes operations and weights. Quantization maps selected values into a smaller numeric representation suitable for the chosen execution path. Calibration uses representative data to estimate useful ranges. Poor calibration can preserve compilation success while reducing application accuracy.

Preprocessing is part of this contract. Color order, resize method, normalization, tensor layout and element type must match the model preparation. A correct DPU can produce consistently wrong classifications when the application supplies BGR data where training expected RGB.

Keep a known input and its expected intermediate representation. Comparing only the final label makes it hard to distinguish preprocessing error from quantization error. Compare the floating-point baseline, quantized model and deployed result at meaningful boundaries.

## Compilation targets a particular DPU configuration

The compiler maps supported graph regions to the target DPU's operations and resources. The target architecture/fingerprint must match the deployed hardware. A model filename containing a board name is weaker evidence than the compiler target and actual hardware identity.

Operator support depends on both operations and graph structure. AMD's model-development guide explains that ordering and fusion patterns can affect whether a graph maps well. An unsupported region needs an explicit supported CPU/custom-operator path; it should not be assumed to disappear automatically. [Model development workflow](https://xilinx.github.io/Vitis-AI/3.5/html/docs/workflow-model-development.html).

For a custom ZynqMP design, DPU resource configuration, clocking, memory path and interrupt/runtime integration belong to the hardware/software platform. A successful model compile does not validate those board-level details. [DPU system integration](https://xilinx.github.io/Vitis-AI/3.5/html/docs/workflow-system-integration.html).

## Follow tensors through the runtime

VART exposes runner interfaces for selected graph execution. Tensor metadata describes shape, element type and layout. The application must allocate and populate buffers that follow that metadata, submit work through the selected runner and observe its completion/status contract.

The 3.5 C++ runner interface separates execution submission from waiting by job identity. Do not generalize that behavior to every language binding or runner backend; inspect the exact API in use. Input and output buffer lifetime must cover the work that uses them. [VART3.5 C++ Runner](https://xilinx.github.io/Vitis-AI/3.5/html/doxygen/api/class/classvart_1_1_runner.html).

An array's logical dimensions do not guarantee contiguous storage. A sliced image can have a row stride larger than its visible width. A conversion step may be required before the tensor buffer is valid, and that cost belongs in end-to-end measurements.

## A worked inference investigation

Consider a classifier that runs without an error but returns the wrong class for a known image. First compare decoded pixels and color order. Next compare resizing/cropping and normalization. Then verify tensor shape, quantization parameters and buffer size. Only after these match should you attribute the mismatch to DPU execution.

If the same prepared tensor gives the expected result in the supported quantized reference but fails on hardware, compare compiled-model target identity, runtime versions and buffer handling. If the quantized reference already differs badly from the floating-point baseline, investigate quantization and model support before changing the driver.

This sequence keeps each comparison meaningful. Recompiling every layer at once can change several inputs and hide the original cause.

## Throughput is a pipeline property

The DPU handles supported inference operations. Input capture, decoding, resize, color conversion, CPU graph regions and postprocessing can remain substantial costs. Batching can improve utilization while increasing latency and memory use.

For an illustrative pipeline, a fast DPU stage cannot exceed a slower serial preprocessing stage's sustained input rate. Add overlap only after buffer ownership is clear. Each in-flight inference needs its own valid input/output state, and a slow consumer must not allow completed output buffers to be overwritten.

Measure accuracy on representative data as well as latency and throughput. A faster preprocessing approximation can change the model input distribution. Performance acceptance should include the required accuracy bound, not merely a frame counter.

## Deployment is a matched set

Retain the model, compiler target description, preprocessing specification, DPU hardware, runtime/library versions and application build together. A model update can require a new runtime or hardware configuration even when the application API appears unchanged.

On failure, report the exact model and hardware identities before generic “DPU not working” conclusions. No model compilation or inference was performed for this revision; the release compatibility and runtime contracts were checked against primary documentation.

## References

- [Vitis AI 4.0 release notes](https://github.com/Xilinx/Vitis-AI/releases/tag/v4.0), explicit 2024.1 compatibility statement.
- [Vitis AI 3.5 model development](https://xilinx.github.io/Vitis-AI/3.5/html/docs/workflow-model-development.html), [system integration](https://xilinx.github.io/Vitis-AI/3.5/html/docs/workflow-system-integration.html), and [Runner API](https://xilinx.github.io/Vitis-AI/3.5/html/doxygen/api/class/classvart_1_1_runner.html).

- AMD [Vitis AI documentation](https://xilinx.github.io/Vitis-AI/)
- XRT documentation for the selected runtime

---

<sub>← [Running Accelerated Applications](03-running-accelerated-applications.md) · [Chapter index](README.md) · Next chapter: [19 · Graphics and Display](../19-graphics-and-display/README.md) →</sub>
