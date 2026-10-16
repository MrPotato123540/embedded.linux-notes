# Building the FSBL

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[08 · First Stage Boot Loader (FSBL)](README.md)** · Part IV: Boot


## The build has four inputs, not just one source tree

A First Stage Boot Loader (FSBL) build combines application source, a standalone board support package, generated hardware initialization and a linker layout. The compiler and build options are also part of its identity. Two ELFs built from the same `xfsbl_main.c` can behave differently because the hardware export or generated `psu_init` code differs.

The hardware export describes the processing-system configuration. Generated headers and initialization code turn that description into software constants and register sequences. The standalone libraries provide low-level services. The FSBL application uses them to load and hand off later images.

This dependency chain matters when maintaining patches. A source patch belongs in your project layer or another tracked source input. A generated work directory is an output. Editing it can appear to work once, then disappear when BitBake rebuilds the task or creates a fresh workspace.

## What the local 2024.1 recipes actually select

The BSP contains a base recipe in `meta-xilinx/meta-xilinx-standalone/recipes-bsp/embeddedsw/fsbl-firmware_2024.1.bb`. Its include selects `zynqmp_fsbl` for ZynqMP and points the build at `lib/sw_apps/zynqmp_fsbl/src`.

However, that file is not the whole PetaLinux flow. `meta-xilinx-tools/recipes-bsp/embeddedsw/fsbl-firmware_2024.1.bbappend` replaces important behavior. It inherits `xsctapp` and `xsctyaml`, selects the `Zynq MP FSBL` application, uses the XSCT-generated project directory and deploys its `executable.elf` under the FSBL artifact name.

The append also sets `XSCTH_COMPILER_DEBUG_FLAGS` to include `-DFSBL_DEBUG_INFO`. This is an important difference from the upstream header's quiet debug defaults. Reading only `xfsbl_config.h` would give an incomplete answer about the recipe-built image's intended logging.

These facts come from reading the local BSP layers. A project can add another append or override. To establish the final value in a specific build, inspect its effective BitBake metadata and task logs. Layer file contents establish candidate settings; the resolved build establishes which settings won.

## An artifact inspection that was run

The following host command was executed on the supplied BSP ELF:

```console
$ readelf -h /home/anado/Downloads/xilinx-zcu106-2024.1/pre-built/linux/images/zynqmp_fsbl.elf
```

The relevant fields report `ELF64`, little-endian data, `AArch64`, and entry address `0xfffc0000`. A second executed inspection used `readelf -l` on the same path. It showed the main loadable segment plus `.handoff_params` and `.bitstream_buffer` allocations.

Why inspect an ELF that already boots? It gives you a baseline before customization. The machine type catches an accidental R5 or wrong-architecture artifact. The entry address catches a linker-placement change. Program headers reveal memory requirements that file size alone misses.

A successful compilation proves that source and libraries passed the build. It does not prove that their hardware description matches the board, that Bootgen packaged this ELF, or that the resulting image was selected at reset.

## Budget OCM from the linker map

The tagged `lscript.ld` gives its main FSBL region origin as `0xFFFC0000` and length as `0x29E00`. It places handoff data in a separate `0x200`-byte region at `0xFFFE9E00`, and has a separate bitstream-buffer region at `0xFFFF0040`.

The reference main segment needs `0x25368` bytes in memory. Relative to the tagged main region limit, that leaves `0x4A98` bytes before considering whether a custom generated script has changed the layout. This is a useful baseline calculation, not a guarantee that all additional code can use that whole difference. Alignment, new sections and stack requirements can change the result.

The source linker defaults include a `0x2000` stack and a 1024-byte heap unless overridden. Large local arrays consume stack; large static arrays consume data or BSS. Neither becomes safe merely because the code section still fits. Review the largest call path as well as the linker totals.

## Feature removal is a boot-policy decision

`xfsbl_config.h` uses exclusion switches such as `FSBL_QSPI_EXCLUDE_VAL`, `FSBL_SD_EXCLUDE_VAL`, `FSBL_BS_EXCLUDE_VAL` and `FSBL_SECURE_EXCLUDE_VAL`. Their names are negative: enabling an exclusion removes functionality. Keep this meaning clear when discussing a “disabled” option.

Removing an unused boot-device driver can recover space. Removing authentication support changes what secure flows the binary can process. Removing bitstream support changes whether the boot image can configure programmable logic. Decide from the full supported boot and recovery set, not only the fastest happy path.

The base recipe uses size and link-time optimization options. Link-time optimization can remove unused code, but it does not remove required memory ownership or make a large stack frame safe. A debug build can change both size and timing, so compare its map and its runtime behavior separately.

## Build, deploy and package are separate boundaries

A reproducible change records the hardware export, application revision, local patches, effective flags, tool versions and linker map. The deployed ELF should have a recorded hash. The packaging input should point to that artifact, and the produced `BOOT.BIN` should be inspected afterward.

Suppose a custom hook is present in source and visible in the new ELF, but the boot log still shows the old behavior. First compare the packaged FSBL with the new deployment output. Then confirm which boot medium and image offset the board selected. Repeatedly cleaning the compiler output cannot correct a stale file on the SD card.

> [!NOTE]
> **Not run on the reference setup:** a new FSBL compilation from the modified hardware export and its physical-board boot. The recipe analysis and supplied-ELF inspections were performed; they are not a substitute for that build and boot pair.

## References

- Local BSP: `components/yocto/layers/meta-xilinx/meta-xilinx-standalone/recipes-bsp/embeddedsw/{fsbl-firmware_2024.1.bb,fsbl-firmware.inc}`.
- Local BSP: `components/yocto/layers/meta-xilinx-tools/recipes-bsp/embeddedsw/fsbl-firmware_2024.1.bbappend`.
- [2024.1 FSBL configuration](https://github.com/Xilinx/embeddedsw/blob/xilinx_v2024.1/lib/sw_apps/zynqmp_fsbl/src/xfsbl_config.h) and adjacent `lscript.ld`.

---

<sub>← [FSBL Source Walkthrough](02-fsbl-source-walkthrough.md) · [Chapter index](README.md) · [Customizing the FSBL](04-fsbl-customization.md) →</sub>
