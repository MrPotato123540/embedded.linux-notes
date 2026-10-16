# Embedded Platforms for Acceleration

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[18 · XRT and Hardware Acceleration](README.md)** · Part VIII: Programmable Logic and Acceleration

## Platform agreement

A Vitis embedded platform combines hardware and software components. The hardware defines accelerator interfaces, clocks, memory and interrupts. The software image supplies the kernel driver, runtime libraries, firmware and application dependencies.

For PetaLinux, include the matching XRT and `zocl` support and verify the generated device-tree requirements. Enabling a packagegroup alone does not prove that the driver is bound or that memory resources are correct.

## Compatibility record

Record the hardware platform identifier, tool release, XRT version, kernel build and xclbin build. Test the platform with a known small accelerator before integrating a complex application.

Do not mix PCIe-card instructions with the embedded ZynqMP flow. Their drivers and device discovery differ even when the application-level API looks similar.

> [!NOTE]
> **Not run on the reference setup:** a Vitis platform build and accelerator deployment.

## A platform is the fixed part of an execution contract

An embedded acceleration platform joins hardware interfaces with boot software, Linux, runtime support and development metadata. The accelerator build uses the platform's exposed clocks, interrupts and memory connections. The resulting application artifact is valid only for the supported contract.

The processing-system configuration, static PL design and software image must agree. A memory port exposed to an accelerator must reach the intended memory through a valid address/coherency path. A control interface must be accessible to the runtime driver. An interrupt must reach the handler that reports completion.

A general-purpose ZCU106 BSP can supply useful boot and software components without being the exact extensible platform required by a particular accelerator. The board name alone does not identify the platform interface.

## Follow the build artifacts

The hardware export describes the fixed design and its interfaces. The platform package adds the metadata needed by the acceleration build flow. Kernel objects produced by high-level synthesis or other supported compilation are linked against those interfaces. The resulting xclbin describes the linked accelerator and its runtime-visible layout.

The host application is a separate AArch64 executable. It links against the target runtime libraries and uses the xclbin's kernel names, argument order and memory groups. Building the xclbin successfully does not prove that the host binary's loader or libraries exist in the rootfs.

Boot artifacts then bring up the processing system, firmware and Linux. Depending on the platform flow, programmable content may be established during boot or through later runtime management. Do not load a second conflicting design simply because the host application has an xclbin path.

## Memory topology determines valid buffers

A platform can expose several memory resources or several connections to shared memory. The runtime metadata records which kernel argument can use which group. This is a hardware connectivity constraint, not merely an allocator preference.

For an illustrative kernel with separate input and output ports, input may connect to one memory group and output to another. Reusing the input's group for both because it worked in a simpler design can break after relinking. Query or validate each argument's group against the actual xclbin.

Memory capacity must cover simultaneous ownership: active input/output buffers, queued work, runtime state and other clients such as display. A platform that passes a single-buffer test can fail under a production queue depth because allocation and bandwidth demands changed.

## Clocks affect correctness and measurement

The accelerator's clock must satisfy its implemented timing and platform configuration. A faster requested clock is not evidence that timing closed or that the board runs at that rate. Keep the implemented clock configuration with performance results.

Control and data paths can use different clocks. Reset release and clock-domain crossings must be valid before the runtime accesses the kernel. A control register that responds while the data path is held in reset can lead to an accepted start with no useful work.

Interrupt completion also depends on the selected design and runtime integration. A busy-wait workaround may hide a missing interrupt while changing CPU usage and latency. Diagnose the route before accepting the workaround as the product architecture.

## PetaLinux supplies software components through recipes

The BSP acceleration packagegroup selects XRT and `zocl` for ZynqMP. The XRT recipe enables libdfx integration for this machine family. The runtime and driver share the release source pin and package version.

These recipe facts identify software support available to the platform. Device-tree nodes, reserved-memory choices, clocks and the actual hardware design still require matching integration. Enabling one packagegroup does not synthesize an accelerator or reserve every buffer it may need.

Build the SDK from the intended image configuration so the application sees the same runtime headers and libraries as the target. A host-side development package from another XRT release can compile APIs the deployed runtime does not provide.

## A compatibility record makes failures explainable

Record platform identity, hardware export hash, static/partial artifact identity, runtime version, driver/kernel build and host executable build ID. Also record the xclbin's kernel names and argument contract used by the application.

When an upgrade fails, compare those identities before changing code. A wrong platform artifact can look like a buffer error; a wrong userspace library can look like a driver failure. A controlled compatibility record narrows the first investigation.

For rollback, restore a set known to work together. If persistent configuration names a newly introduced kernel, reverting only the runtime library may not restore operation. Treat application configuration and programmable artifacts as part of the release.

## Validation order

First validate boot and runtime device availability. Then validate a small known-correct accelerator on the platform, followed by the intended workload and queue depth. Finally test restart, cancellation and replacement under the product's lifecycle policy.

Each stage should preserve output correctness, not only report that a command returned. No complete custom platform build or board validation was performed for this revision; this is a source-backed integration walkthrough.

## References

- Inspected BSP `meta-petalinux/recipes-core/packagegroups/packagegroup-petalinux-vitis-acceleration.bb` and XRT 2024.1 recipes.
- [XRT 2024.1 native API](https://xilinx.github.io/XRT/2024.1/html/xrt_native_apis.html).
- [Hardware handoff contract](../17-pl-integration-and-dfx/01-hardware-handoff.md) and [DFX lifecycle](../17-pl-integration-and-dfx/04-dfx-dynamic-function-exchange.md).

- XRT 2024.1 embedded platform documentation
- Inspected `meta-petalinux@rel-v2024.1` Vitis acceleration packagegroup

---

<sub>← [XRT Overview](01-xrt-overview.md) · [Chapter index](README.md) · [Running Accelerated Applications](03-running-accelerated-applications.md) →</sub>
