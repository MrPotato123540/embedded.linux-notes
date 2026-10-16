# Configuring and Building the Kernel

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[13 · The Linux Kernel](README.md)** · Part VI: Linux Kernel and Drivers


## Configuration is a resolved dependency graph

Kconfig describes kernel features and their dependencies. A baseline defconfig and configuration fragments request choices; the final `.config` records the resolved result. A symbol requested as `y` or `m` can be changed or unavailable when its dependencies are not satisfied.

The distinction matters for driver work. Adding a fragment line is not proof that the driver was built. Inspect the final symbol and its required subsystem choices after configuration. For a module, also verify that the module artifact was produced and installed into the intended root filesystem.

A configuration is part of the software identity. Two kernels from the same commit can have different memory behavior, driver support and debugging facilities. Archive the full `.config` with the deployed image.

## The PetaLinux interfaces and local layer inputs

PetaLinux 2024.1 exposes kernel configuration through `petalinux-config -c kernel` and component building through `petalinux-build -c kernel`. Their interfaces were checked in installed help during the reference work. This section does not claim that a fresh full kernel build was executed.

The local user layer contains `project-spec/meta-user/recipes-kernel/linux/linux-xlnx_%.bbappend`. It adds `bsp.cfg` to `SRC_URI` and `KERNEL_FEATURES`. The supplied fragment is empty in the inspected project, so the existence of that append does not establish any extra symbol settings.

This is a useful lesson: inspect the content and resolved configuration, not only the filename. A build system can correctly include an empty fragment and still leave all requested custom behavior absent.

## Keep source changes and configuration changes explicit

A source fix belongs in a tracked patch or selected source revision. A feature choice belongs in maintained configuration input. The recipe append connects those inputs to the selected kernel provider.

Do not use an edited generated work directory as the only record. BitBake can recreate it, reuse cached task output or build a new machine variant elsewhere. A source change must be represented in the recipe inputs so task signatures and rebuilds reflect it.

After applying a patch, inspect the patched source and task log. After merging configuration, inspect the final `.config`. These checks catch different mistakes: a patch can be absent while a symbol is enabled, or the source can be correct while the needed configuration is disabled.

## Worked design: a driver needed for root storage

Assume a custom board boots from a storage controller that requires a kernel driver and a clock provider. This is a configuration example, not a new reference-board build.

If the driver is built in, it can participate before mounting the persistent root filesystem. If it is a module, the initramfs must contain that module and its dependencies and load them before root mount. Storing the only copy on the root filesystem creates a circular dependency.

The device tree must describe the controller and its providers, and firmware must permit required resource operations. Enabling the controller symbol alone cannot repair a missing clock node or a denied power-domain request.

Review the final artifact set: kernel, module tree, initramfs, DTB and boot arguments. A successful link of `Image` is only one boundary in that chain.

## Direct builds need an equally complete input set

An out-of-Yocto build requires the correct architecture, cross-toolchain, source revision, configuration and output directory. Keeping build output separate from source helps avoid mixing artifacts from different configurations.

The compiler prefix is not proof of the intended ABI or version. Record the toolchain identity and inspect the produced image/module architecture. A host x86 module build cannot validate an ARM64 module's target behavior, even when it catches useful C errors.

For external modules, use the prepared build artifacts of the exact target kernel. `Module.symvers`, generated headers and configuration affect compatibility. A plain source checkout with the same version number is not a complete module-build environment.

## Defconfig and full configuration have different uses

A reduced defconfig records choices relative to defaults. It is convenient for maintenance, but defaults can change when the source changes. The full `.config` records what the specific build resolved.

For an upgrade, compare both requested intent and resolved output. A symbol can be renamed, removed or gain dependencies. A fragment that worked in one release can be ignored or resolve differently in another without expressing the intended product behavior.

Keep warnings from configuration checks. Silencing an unknown-symbol warning can leave a critical feature disabled while the build still succeeds.

## Deployment must include matching modules and metadata

A kernel component build can produce a new Image without rebuilding or deploying every root filesystem artifact. Confirm the selected root filesystem has the matching module directory and dependency metadata.

The running release string determines the normal module lookup path, but equal strings do not prove equal binary interfaces. Local changes can alter structures or symbols without a deliberate version change. Use a product build identity that distinguishes incompatible artifacts.

If a DTB is embedded in FIT, regenerate and inspect that container. Copying a new standalone DTB beside an old FIT does not update the embedded tree selected by the boot command.

## Verify the change at its intended boundary

For a configuration-only driver enablement, verify the resolved symbol, built artifact, probe and device function. For a core patch, run the affected subsystem tests and a representative workload. For an image-format change, inspect the header and bootloader compatibility.

Avoid repeating a full build merely to create confidence after the relevant checks already pass. Broaden testing when the change affects shared behavior, exposes a new failure or leaves a concrete uncertainty.

> [!NOTE]
> **Not run on the reference setup:** a fresh PetaLinux kernel build, new target module deployment and the illustrative root-storage configuration. The local recipe inputs and installed command interfaces were inspected.

## References

- `linux-xlnx@xilinx-v2024.1:Documentation/kbuild/kconfig.rst` and the kernel build system.
- Local BSP: `project-spec/meta-user/recipes-kernel/linux/{linux-xlnx_%.bbappend,linux-xlnx/bsp.cfg}`.
- [AMD UG1144, 2024.1](https://docs.amd.com/r/2024.1-English/ug1144-petalinux-tools-reference-guide), kernel configuration and build workflow.

---

<sub>← [Kernel Image Formats](03-kernel-image-formats.md) · [Chapter index](README.md) · [Kernel Debugging](05-kernel-debugging.md) →</sub>
