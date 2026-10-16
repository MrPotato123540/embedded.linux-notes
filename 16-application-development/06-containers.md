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

## Containers share the host kernel

A container packages a userspace filesystem and runs processes with selected isolation. It does not boot its own independent Linux kernel in the ordinary container model. The host kernel must provide the system calls, filesystems, namespaces and device drivers the application needs.

An AArch64 userspace image still needs a compatible execution architecture or an explicitly configured emulation layer. A container image does not turn an x86-64 executable into Arm code. It also cannot install a different kernel ABI by placing headers or modules inside its root filesystem.

For an FPGA application, the host owns the PL configuration, kernel driver and DMA/IOMMU path. The container can package the application runtime, but compatibility with those host components remains part of deployment.

## Namespaces and cgroups solve different problems

Namespaces give processes separate views of resources such as process IDs, mounts and networking. Control groups account for and limit resource use. Neither mechanism alone grants a safe device interface or makes a vulnerable kernel driver harmless.

The pinned cgroup-v2 documentation defines a unified hierarchy and controller interfaces. CPU limits and memory limits apply according to the enabled controllers and hierarchy rules. A container runtime's setting is effective only if the host has the required support and the runtime applies it to the intended process group.

A memory limit can make an application fail even when the machine has free RAM outside that cgroup. A CPU quota can create periodic latency even when another core appears idle. Diagnose the actual cgroup state before concluding that the board lacks performance.

## Device access is an explicit trust decision

A device node grants access to the kernel interface behind it. Mapping a node into a container does not reduce the power of its ioctls. A device that allows arbitrary register programming or DMA can affect resources beyond the container's visible filesystem.

Pass only the required interfaces and permissions. Avoid using a fully privileged container as the final fix for a missing group or device rule. A privileged development configuration can hide the exact capabilities the product actually needs.

For XRT, the userspace library and host `zocl` driver must remain compatible. The supplied BSP couples their package versions. Packaging an unrelated runtime in a container does not remove that dependency. Record host kernel/driver, runtime and accelerator artifact versions together.

## A worked update boundary

Imagine a containerized vision service using a fixed host driver and a PL accelerator. Updating the container changes preprocessing and the host runtime library. If the new library expects a newer driver interface, the application can fail even though the container image starts normally.

If the update also changes the model or xclbin, hardware compatibility becomes another boundary. A correct release process validates the container against the selected host platform and accelerator package, then deploys them as a controlled set or through a documented compatibility matrix.

Rollback must restore compatible persistent data too. A new container can migrate a database on a bind-mounted volume; rolling back only the container image may leave old software unable to read the new data format.

## Storage and logging still need a policy

A writable container layer is useful for temporary changes. It is usually a poor implicit location for durable product state because replacement or cleanup can remove it. Use explicit persistent volumes for data that must survive, and define their ownership and migration rules.

Overlay-based storage can add copy-up costs and consume space unexpectedly. Logs can fill either the writable layer or the host's log storage. Limits and retention policy belong to the deployment, not just the application's source code.

A read-only container root improves predictability only if the application has suitable writable runtime and state paths. Otherwise the first startup failure is often a path policy error rather than a container-runtime fault.

## PID 1 and shutdown exist inside the container too

The first process in a PID namespace has init responsibilities for that namespace. A shell wrapper that does not forward signals or reap children can break clean shutdown. Use an execution model that lets the real application receive termination and manage its children correctly.

Container stop timeouts must allow the application to stop new requests and release hardware. Killing the process does not necessarily stop DMA unless the driver implements correct close and cancellation behavior. The kernel driver's lifetime contract remains the final protection.

> [!NOTE]
> **Not run on the reference setup:** installing a container runtime, running privileged containers, or assigning hardware. This section describes deployment boundaries from pinned kernel and BSP integration sources.

## References

- [linux-xlnx@xilinx-v2024.1:Documentation/admin-guide/cgroup-v2.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/admin-guide/cgroup-v2.rst).
- Inspected BSP `meta-virtualization` layer and `meta-xilinx/meta-xilinx-core/recipes-xrt/xrt/xrt_git.bb`, versioned `zocl` runtime dependency.

- `meta-virtualization` shipped with the reference BSP
- Linux 6.6 namespace and cgroup documentation

---

<sub>← [Python and High-Level Frameworks](05-python-and-high-level-frameworks.md) · [Chapter index](README.md) · Next chapter: [17 · PL Integration, FPGA Manager and DFX](../17-pl-integration-and-dfx/README.md) →</sub>
