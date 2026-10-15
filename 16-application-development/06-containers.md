# Containers on ZynqMP

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Containers share the kernel

A container packages userspace and isolates selected resources using kernel facilities. It does not provide its own kernel driver for a host device. Docker or Podman support requires the appropriate recipes, kernel configuration and runtime policy.

`meta-virtualization` supplies build integration, but enabling the layer does not install every runtime. Select packages and verify storage, networking and cgroup behavior on the image.

## Hardware access

Pass only required device nodes and permissions. A container using an accelerator still depends on the host driver, loaded bitstream and compatible userspace runtime. Broad privileged mode can remove much of the intended isolation.

Kria application containers belong to a platform-specific deployment flow. Keep the application, firmware package and platform version compatible.

## Validation

Test restart, resource limits, persistent data and device removal. Record the container digest and host image version together.

> [!NOTE]
> **Not run on the reference setup:** container deployment with physical accelerators.

## References

- `meta-virtualization` shipped with the reference BSP
- Linux 6.6 namespace and cgroup documentation

---

<sub>← [Python and High-Level Frameworks](05-python-and-high-level-frameworks.md) · [Chapter index](README.md) · Next chapter: [17 · PL Integration, FPGA Manager and DFX](../17-pl-integration-and-dfx/README.md) →</sub>
