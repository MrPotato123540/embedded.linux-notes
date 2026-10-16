# Building and Customizing TF-A

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot


## A build option can change the memory contract

A Trusted Firmware-A (TF-A) customization can add logging, change the console, relocate BL31 or add a Secure payload dispatcher. These are not all local code changes. Some alter the memory that must remain reserved, the boot metadata, or the services visible to Linux.

The ZynqMP platform files are `platform.mk`, `include/platform_def.h` and `bl31_zynqmp_setup.c` under `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp`. Read them together with the PetaLinux recipe so that source defaults and build overrides stay separate.

The local recipe pins the AMD 2.10 branch to commit `4f82b6134e7b43722616c855e5016d42a3ea26d2`. Its build invokes the BL31 target for `PLAT=zynqmp` with `RESET_TO_BL31=1`. The platform makefile also enforces this entry arrangement.

## Follow the actual 2024.1 placement condition

Without an explicit `ZYNQMP_ATF_MEM_BASE`, the tagged header selects the OCM base `0xFFFEA000` only when `!DEBUG`, `SPD_none` and `!SDEI_SUPPORT` are all true. Otherwise, its default base is `0x1000` with limit `0x80000` in DDR.

This is more precise than saying “release builds use OCM and debug builds use DDR.” Adding a Secure payload dispatcher or changing another supported feature can also change the selected branch. Review the preprocessor condition for the exact build.

If you provide `ZYNQMP_ATF_MEM_BASE`, the build also needs `ZYNQMP_ATF_MEM_SIZE`. The region covers runtime storage, not only the initialized binary. A smaller file after optimization does not justify shrinking the reservation below stacks, BSS and translation tables.

## Work through a relocation decision

Assume a product moves BL31 into a dedicated DDR region to support a larger build. This is an integration example, not an executed relocation.

First, select a range that exists on the board and does not overlap the FSBL's temporary buffers, loaded images, decompression areas, device tree, initramfs or other resident firmware. Next, configure BL31's base and size and inspect the linked sections and program headers.

Then make the boot package load the resulting image correctly. Finally, keep that region unavailable to Linux and other later allocators for the firmware's full lifetime. A correct BL31 link address without a matching reservation can boot and fail only after Linux reuses the memory.

TF-A can prepare a device tree when the relevant DTB address and placement support are configured. Do not assume that this happens automatically for every relocated image. Confirm the actual tree handed to Linux and its reserved ranges. Hardware protection remains a separate requirement from allocator reservation.

## The R5 first-stage view adds another constraint

If the FSBL runs on an R5, its view of low addresses includes tightly coupled memory. The TF-A ZynqMP documentation specifically warns about placing a DDR BL31 within the first 256 KB for that flow. A physical-address plan that works for the A53 loader can therefore be wrong for an R5 loader.

Resolve addresses from every participating processor's view. The bootloader that copies the image must reach the intended DDR, and BL31 must execute from the same intended storage afterward. A single flat address table can hide this difference.

## PetaLinux recipe variables and their effects

The local `arm-trusted-firmware.inc` maps `ATF_CONSOLE` into `ZYNQMP_CONSOLE`, maps `ATF_MEM_BASE` and `ATF_MEM_SIZE` into the platform placement options, and uses `DEBUG_ATF` to select debug output and the debug build directory.

The platform accepts the named Cadence console choices and DCC according to `platform.mk`. A console change also needs the appropriate physical routing and access path. Selecting a UART whose pins or clock are unavailable produces a valid build with no useful output.

Store overrides in tracked project metadata and inspect the resolved compile command. An environment variable in one terminal is weaker provenance than a recipe append that another developer can rebuild.

## Custom services need a narrow ABI

An **application binary interface (ABI)** defines the service identifier, argument sizes, allowed callers, result codes and lifetime rules. A custom EL3 service should perform a narrow platform operation with bounded work. Large application logic in the monitor increases the amount of privileged code that must be reviewed.

Validate every caller-supplied address, length and arithmetic operation before use. A valid start address with an overflowing length can describe an invalid range. A Non-secure shared buffer can change while the service runs. The service must not trust a prior check as proof that the data remains unchanged.

Also define concurrency across CPUs. A register sequence that is safe from one core can fail when two cores call simultaneously. Use suitable locking and avoid waiting while holding a lock for work that needs the same service to progress.

## Packaging and evidence

Keep the new ELF, map, configuration and recipe revision with the boot package. Inspect BL31 entry and runtime sections, then inspect the packaged partition. The supplied reference ELF has code at `0xFFFEA000`, but that observation does not validate a newly relocated build.

Test boot and at least one relevant runtime call. For a CPU-service change, include the affected CPU transition. For a custom shared-memory call, include invalid input and concurrent requests. For a console-only change, confirm both early and runtime output behavior where supported.

> [!NOTE]
> **Not run on the reference setup:** TF-A rebuilding, DDR relocation, custom SMC services and their runtime tests. The exact placement condition and recipe mappings were verified from 2024.1 source and local layers.

## References

- [2024.1 ZynqMP platform definitions](https://github.com/Xilinx/arm-trusted-firmware/blob/xilinx-v2024.1/plat/xilinx/zynqmp/include/platform_def.h) and adjacent `platform.mk`.
- Local BSP: `meta-xilinx-core/recipes-bsp/arm-trusted-firmware/{arm-trusted-firmware_2024.1.bb,arm-trusted-firmware.inc}`.
- [TF-A 2.10 ZynqMP platform documentation](https://trustedfirmware-a.readthedocs.io/en/v2.10/plat/xilinx-zynqmp.html), DDR placement and RPU loader restrictions.

---

<sub>← [BL31 on ZynqMP](02-bl31-on-zynqmp.md) · [Chapter index](README.md) · [BL32 and OP-TEE (Overview)](04-op-tee-overview.md) →</sub>
