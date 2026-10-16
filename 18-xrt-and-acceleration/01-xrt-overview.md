# XRT Overview

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[18 · XRT and Hardware Acceleration](README.md)** · Part VIII: Programmable Logic and Acceleration

## XRT components

**Xilinx Runtime (XRT)** connects a host application with supported programmable-logic accelerators. On embedded platforms, userspace libraries cooperate with the `zocl` kernel driver and platform firmware.

An `xclbin` contains accelerator configuration and metadata. The metadata describes information needed to load and use the compiled design. It must match the platform; a runtime library cannot make an incompatible hardware design work.

## Programming models

The native XRT API exposes devices, kernels, runs and buffer objects. OpenCL provides another programming model where supported by the selected release. Keep application API use consistent with the installed runtime and build tools.

The runtime is not the accelerator itself. Compute behavior still comes from the hardware kernel and its interface contract. Check argument order, widths, memory groups and synchronization.

## XRT spans userspace and the kernel

Xilinx Runtime (XRT) provides APIs and tools for accelerator execution. On an embedded ZynqMP platform, the application uses runtime libraries that communicate with the `zocl` kernel driver and the platform's programmable hardware. This differs from a PCIe accelerator card's host-driver arrangement.

The runtime coordinates buffer objects, kernel arguments, execution requests and completion. It does not make arbitrary PL logic into a supported accelerator. The hardware must expose the control, memory and interrupt interfaces expected by the selected platform flow.

The xclbin is a runtime artifact containing hardware/runtime metadata and, for relevant flows, programmable content. Its metadata describes kernel interfaces and memory connectivity. It is not simply an ELF executable for the A53, and it is not interchangeable with every raw bitstream file.

## The supplied recipe pins a specific implementation

The BSP's `recipes-xrt/xrt/xrt.inc` sets branch `2024.1`, source commit `a75e9843c875bac0f52d34a1763e39e16fb3c9a7` and package version `202410.2.17.0`. Both userspace XRT and `zocl` use this shared source definition.

The `xrt_git.bb` recipe declares a runtime dependency on `zocl` at the same package version. The `zocl_git.bb` recipe builds its source through the kernel module class. These choices connect runtime compatibility with the target kernel build, rather than treating the driver as an unrelated binary.

The supplied rootfs manifest contains both packages at that version. This proves packaging in that artifact. It does not prove a successful device probe, a loaded xclbin or a completed accelerator request.

## Objects express ownership

A device object identifies a runtime device. A loaded xclbin has an identity used to select matching kernels. A kernel object describes an accelerator function and its arguments. A buffer object owns or refers to memory managed through the runtime. A run object tracks one execution request.

These are separate lifetimes. An application must keep required buffers and execution state valid until hardware no longer uses them. Destroying a convenient C++ wrapper is not a substitute for a defined completion or cancellation path when an operation is still active.

A mapped buffer pointer gives CPU access to the buffer's host-side view. It does not prove that the device sees the CPU's latest writes. The `sync()` API expresses the required direction and range. Its implementation may involve cache maintenance or movement depending on the platform and allocation type.

## Memory connectivity is part of the kernel interface

A kernel pointer argument is connected to particular memory resources by the hardware platform and link process. Allocating a buffer in an arbitrary memory group can make the argument invalid even if allocation succeeds.

The pinned C++ header provides `kernel.group_id(argno)` to obtain the memory group for an argument. Its documented behavior includes throwing when the group is ambiguous. A program should not silently replace that failure with group zero. Resolve the intended compute unit/connectivity or use the documented platform arrangement.

The argument number follows the kernel's declared interface, not a guessed buffer order in the host application. Scalar arguments and multiple memory ports make that distinction important.

## Native API and OpenCL are different programming layers

XRT offers native interfaces and supports relevant OpenCL integration. They expose related hardware through different object and command models. Select one model deliberately and use its synchronization rules; do not mix an OpenCL queue assumption with a native run object's lifetime.

The native API can make an embedded control path direct: select the device, load or identify the compatible xclbin, construct the kernel, allocate buffers, synchronize, run and wait. The simplicity of that sequence does not remove error handling or multi-thread ownership.

A framework such as VART can sit above these layers for a particular workload. Its model graph and tensor semantics add another contract. Debug from the highest failing layer down while preserving evidence from lower layers that already succeeded.

## Distinguish discovery, loading and execution failures

No runtime device suggests kernel driver, device-tree or permission integration. A device that opens but rejects an xclbin suggests artifact/platform compatibility or load policy. Successful loading with buffer-allocation failure suggests memory resources and limits. A run that never completes suggests arguments, scheduling, interrupts or hardware protocol.

A runtime utility version string does not validate all those boundaries. Keep the actual library version, driver version, kernel release and xclbin identity in a support record. Container packaging must preserve compatibility with the host driver too.

## Release limits

Do not use current-master examples as proof of 2024.1 API behavior. The pinned header already contains a timeout limitation that matters for robust applications, discussed in section 18.03. Newer overloads and supported flags can differ.

> [!NOTE]
> **Not run on the reference setup:** runtime device discovery, xclbin loading and accelerator execution. Recipe, manifest and pinned API-header inspection are the evidence for this section.

## References

- Inspected BSP `meta-xilinx/meta-xilinx-core/recipes-xrt/xrt/xrt.inc`, `xrt_git.bb` and `recipes-xrt/zocl/zocl_git.bb`.
- [XRT@a75e984:xrt_bo.h](https://github.com/Xilinx/XRT/blob/a75e9843c875bac0f52d34a1763e39e16fb3c9a7/src/runtime_src/core/include/xrt/xrt_bo.h) and [xrt_kernel.h](https://github.com/Xilinx/XRT/blob/a75e9843c875bac0f52d34a1763e39e16fb3c9a7/src/runtime_src/core/include/xrt/xrt_kernel.h).

- [XRT 2024.1 documentation](https://xilinx.github.io/XRT/2024.1/html/index.html)
- AMD XRT source and embedded `zocl` driver

---

<sub>[Chapter index](README.md) · [Embedded Platforms for Acceleration](02-embedded-platforms-for-acceleration.md) →</sub>
