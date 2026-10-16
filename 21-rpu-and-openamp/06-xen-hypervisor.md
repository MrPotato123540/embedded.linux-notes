# Xen Hypervisor (Overview)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Xen partitions the APU execution environment

**Xen** is a hypervisor that runs below guest operating systems. On Arm systems, it uses the virtualization support associated with exception level EL2. Guests normally run their kernel code at EL1. This differs from AMP between Cortex-A53 and Cortex-R5: Xen virtualizes or partitions the APU environment; it does not turn an R5 application into an AArch64 guest.

A Xen system can also use the RPU, but that creates another ownership problem. Decide which component manages R5 firmware, shared memory and interrupts. A Linux guest cannot assume it owns every physical device that an ordinary bare-metal Linux installation would own.

The PetaLinux 2024.1 layers contain AMD Xen recipes and integration. The inspected `xen-xilinx_4.18.inc` pins revision `c4ff3360900b7428ca31de2425763acfe7ad9c21` on `xlnx_rebase_4.18`. Other Xen recipes also exist in the tree. This is an inspected recipe input, not evidence that the reference image boots Xen.

## Follow the boot and management roles

Firmware and the bootloader prepare the machine and start Xen with its required image and device-tree information. Xen establishes its own memory and interrupt control, then starts domains. **Domain 0 (Dom0)** is the privileged management domain in a conventional setup. Other guests are often called DomU domains.

Dom0 can provide device backends and management tools, but that does not mean every guest reaches hardware through ordinary Linux drivers in the same way. A virtual device may use a frontend driver in the guest and a backend service in another domain. A passed-through device gives a guest more direct hardware access under the platform's assignment rules.

Boot artifacts must therefore match the selected Xen flow. Reusing a normal Linux boot command with an extra filename is not enough. The bootloader must supply the expected Xen image, guest modules, memory information and command lines in the supported form. [Xen Arm boot protocol](https://xenbits.xen.org/docs/4.18-testing/misc/arm/booting.txt).

## CPU isolation and memory isolation are different

A virtual CPU (**vCPU**) is a guest's execution context. Pinning vCPUs to physical CPUs can reduce scheduling interference, but it does not remove shared-cache, memory-controller or interrupt contention. A latency claim needs the full workload, not only a CPU-affinity setting.

Guest memory is translated under hypervisor control. A guest physical address is not automatically a machine physical address. Passing a number between a guest and a PL DMA engine requires a supported mapping path; an address meaningful inside the guest may not be meaningful to the device.

Memory reserved for Xen, Dom0, other guests, RPU firmware and device buffers must fit the complete machine map. A guest's free-memory report excludes resources outside that guest, so it cannot prove that the global allocation plan is safe.

## Device assignment includes DMA and reset

Passing through a device means assigning its registers, interrupts and DMA access appropriately. An input/output memory management unit such as the Arm SMMU can help restrict DMA, but support depends on the device path and Xen/platform integration. A device visible in a guest does not by itself prove DMA isolation.

Review shared reset and clock relationships. If two devices share a reset domain, resetting one guest's device may affect another domain. If a device's bus master can reach unrestricted memory, register isolation alone is insufficient. The ownership boundary must follow the hardware, not just device-tree node boundaries.

For a PL peripheral, include its bitstream lifecycle. Reconfiguring PL can remove hardware while a guest still holds mapped registers or queued DMA work. A safe management flow must stop users, quiesce bus masters and invalidate stale resources before replacing the design.

## Work a two-guest example

Consider an original design with a Linux networking guest and a control guest. Give each a memory budget and a vCPU policy. Decide whether Ethernet is a virtual device served by a backend or directly assigned to one guest. Define how the other guest exchanges control data.

If Ethernet is virtualized through a backend, networking latency includes the frontend, shared rings, backend scheduling and physical driver. If it is directly assigned, the owning guest needs the device resources and DMA protections. The second design may reduce one software path but complicates sharing and recovery.

Now add an R5 sensor service. Choose one manager for remoteproc and the shared-memory region. If both guests can reset the R5 or rewrite its buffers, neither guest has a stable communication contract. A dedicated service can mediate access, but its protocol and failure behavior become part of the system.

## Shared communication still needs validation

Xen grant tables and event channels support controlled sharing and notification between domains. They are not interchangeable with arbitrary physical-address exchange. A frontend/backend protocol defines which pages are shared, who owns ring entries and how notifications work.

A malicious or faulty guest can submit invalid lengths or indices. Backend code must validate them and bound resource use. Even in a trusted product, version mismatch can create malformed requests. Keep the frontend/backend ABI and package versions with the release record.

Guest restart also needs cleanup of grants, event channels and outstanding device work. A new guest instance must not inherit a stale interpretation of old shared pages. This resembles the generation problem in OpenAMP, but uses Xen's own resource-management interfaces.

## Debug one layer at a time

If Xen itself does not start, inspect the firmware handoff, image placement and boot description. If Xen starts but Dom0 does not, inspect the Dom0 image, console and memory assignment. If a guest starts but lacks a device, inspect assignment and frontend/backend availability before debugging the ordinary peripheral driver.

For latency changes, compare hypervisor scheduling, backend CPU use and shared memory traffic. A guest's CPU trace shows only part of the path. For device faults, preserve both guest logs and the hypervisor/management-domain view so address and interrupt translations can be related.

> [!NOTE]
> **Not run on the reference setup:** Xen builds, guest boot, passthrough, SMMU isolation and timing tests. The Xen 4.18 recipe revision was inspected locally. The two-guest system is an original design example.

## References

- Inspected `xilinx-zcu106-2024.1:components/yocto/layers/meta-xilinx/meta-xilinx-virtualization/recipes-extended/xen/xen-xilinx_4.18.inc`.
- [Xen 4.18 documentation](https://xenbits.xen.org/docs/4.18-testing/), Arm boot, domain configuration and interfaces.
- [AMD Xen recipe revision](https://github.com/Xilinx/xen/tree/c4ff3360900b7428ca31de2425763acfe7ad9c21), platform implementation corresponding to the inspected recipe.

---

<sub>← [IPI and Shared Memory Patterns](05-ipi-and-shared-memory.md) · [Chapter index](README.md) · Next chapter: [22 · Networking and Peripherals](../22-networking-and-peripherals/README.md) →</sub>
