# OpenAMP in PetaLinux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Build one agreement across four artifacts

A working OpenAMP system needs matching Linux configuration, device tree, R5 firmware and application protocol. Installing the OpenAMP library is only one part of this agreement. Linux normally uses its kernel remoteproc/RPMsg infrastructure, while the remote software uses the corresponding remote-side libraries and platform support.

Keep a release record that joins the kernel image, DTB, remote ELF, remote linker map, message protocol version and relevant package revisions. A mismatch can still boot both operating environments while leaving communication broken.

The installed 2024.1 BSP includes `meta-openamp` and AMD-specific additions. It also contains several recipe versions. The existence of a recipe does not prove that BitBake selected it for your image. Review preferred versions, provider choices, append files and the resolved build configuration.

## Read the actual recipe inputs

The local `meta-openamp/recipes-openamp/open-amp/open-amp_v2023.10.bb` pins OpenAMP to `1904dee18da85400e72b8f55c5c99e872a486573`. The RPMsg example include selects the system-reference revision `2c5d2064e45faf7e3a542d1232593beec40ff940` by default. AMD vendor append files can alter the selected recipe inputs, so these are inspected recipe defaults, not a claim about a completed image.

The AMD remoteproc kernel fragment contains `CONFIG_ZYNQMP_R5_REMOTEPROC=m`. That means the fragment requests a module. It does not prove the final kernel configuration uses a module or that the resulting module is present in the root filesystem. Other fragments, dependencies and image packaging still matter.

Separate library development packages from runtime applications and kernel modules. A root filesystem with headers is not proof that the intended service starts. A remote firmware recipe must also install the ELF where the selected Linux firmware-loading path can find it.

## Device-tree structure is release-specific

The pinned binding uses `compatible = "xlnx,zynqmp-r5fss"` for the cluster and `"xlnx,zynqmp-r5f"` for its processor children. It describes `xlnx,cluster-mode`, power domains, mailbox channels and reserved memory references. Do not copy a newer binding's node structure or properties without checking this release's schema and driver.

The binding lists split mode 0, lockstep 1 and single-CPU mode 2. The inspected implementation supports only the first two. It also expects two available R5 child nodes for split mode. This is a concrete example of why source review must follow schema review.

The reserved-memory entries distinguish the firmware region, transport buffer pool and two vrings. Their addresses and sizes must agree with the remote ELF and resource table. Reserve the complete runtime footprint, including data that is absent from the file but exists in memory.

## Node names can affect behavior in this driver

In `add_mem_regions_carveout()`, the 2024.1 driver treats a reserved-memory node named `vdev0buffer` specially. It calls `rproc_of_resm_mem_entry_init()` for that node; other memory entries use the ordinary carveout initialization path. The comparison uses the node name, not its source label.

That distinction matters during cleanup of a device-tree example. Renaming a label can preserve references, while changing the actual node name can change how this driver registers memory. Follow the release's working structure and inspect the compiled tree. A visually clearer name is not necessarily a behavior-preserving edit here. [Pinned carveout implementation](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/remoteproc/xlnx_r5_remoteproc.c).

Avoid publishing a universal physical address for these regions. DDR capacity, bootloader allocations, CMA, other remote processors and PL DMA can all consume memory. Start from the complete board memory map, then choose non-overlapping regions with required alignment.

## Work a static consistency review

For an original review example, suppose firmware uses one DDR code region, two vrings and a message pool. Create a table with each region's physical base, remote device address, size, owner and cache policy. Match every ELF load segment to a region. Match each resource-table vring to the corresponding reservation.

Next compare the selected RPU mode with TCM placement. Confirm the mailbox transmit and receive channels refer to the intended processor pair. Confirm that the Linux device tree does not enable a competing driver for an R5-owned peripheral. Finally compare application service names and message layouts.

This review can catch address overlap and version mismatch without starting a processor. It cannot prove interrupts, hardware permissions or cache maintenance work at runtime. Keep those as separate acceptance tests rather than presenting static consistency as a successful board test.

## Package for repeatable startup and recovery

A startup service should wait for the required kernel and firmware resources, select the intended image and observe readiness through a defined protocol. A fixed delay is weak evidence: slower storage or probe deferral can make the same delay too short on another boot.

The service also needs a shutdown and restart policy. Stop application traffic before removing endpoints or stopping remoteproc. Handle a remote crash as a new session with new transport state. If an independent boot stage already started the R5, use a flow explicitly designed for that ownership model; do not assume ordinary load-and-start operations safely attach to arbitrary running firmware.

Keep firmware outside mutable, untracked application directories when reproducibility matters. A service that loads whichever file happens to share a familiar filename defeats the image manifest. Record the content hash and remote-reported build identity with diagnostics.

## Debug configuration before timing

If the module does not bind, inspect compatible strings, available child nodes and power-domain dependencies. If firmware loading fails, inspect packaging and ELF/carveout compatibility. If transport appears but the service does not, inspect resource-table features, channel names and driver matching.

If a previous release's example suddenly fails, compare device-tree binding, firmware resource table, kernel RPMsg configuration and recipe revisions as one set. Copying only the old ELF into a new image is not a controlled migration test.

> [!NOTE]
> **Not run on the reference setup:** a complete OpenAMP image build and APU/RPU runtime test. Recipe defaults, kernel fragment, binding and implementation were inspected locally; resolved-image package selection remains a build-specific check.

## References

- Inspected `xilinx-zcu106-2024.1:components/yocto/layers/meta-openamp/recipes-openamp/` and `vendor/xilinx/recipes-kernel/linux/openamp-xilinx-kmeta/cfg/remoteproc-zynqmp.cfg`.
- [2024.1 R5 binding](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/devicetree/bindings/remoteproc/xlnx,zynqmp-r5fss.yaml).
- [Programming the RPU](02-rpu-programming.md), address translation and executable placement.

---

<sub>← [remoteproc and RPMsg](03-remoteproc-and-rpmsg.md) · [Chapter index](README.md) · [IPI and Shared Memory Patterns](05-ipi-and-shared-memory.md) →</sub>
