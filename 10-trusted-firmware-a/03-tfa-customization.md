# Building and Customizing TF-A

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot

## Configuration points

The ZynqMP build supports options including `ZYNQMP_ATF_MEM_BASE`, `ZYNQMP_ATF_MEM_SIZE`, `ZYNQMP_CONSOLE`, `DEBUG` and `RESET_TO_BL31`. Their exact effect belongs to the platform makefiles and release documentation.

In Yocto, add build settings through the selected TF-A recipe, commonly using `EXTRA_OEMAKE`. Preserve existing settings and verify the generated build command. A successful make invocation does not prove that Bootgen packaged the new ELF.

## Custom services

A custom silicon-provider service needs a unique function identifier, argument validation, a documented return convention and a caller policy. Check buffer sizes and address ranges before accessing caller memory. Do not let a Non-secure caller request unrestricted register access through EL3.

Keep work bounded and consider concurrent callers. A runtime service can interrupt normal system execution, so long waits affect latency beyond the calling process.

## Validation

Check the map and load range, preserve the ELF for symbols, and verify both valid and invalid requests. Confirm console routing before diagnosing silence.

> [!NOTE]
> **Not run on the reference setup:** a custom SMC service or modified TF-A build.

## References

- TF-A v2.10 ZynqMP documentation, build options and custom SiP service support
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/`

---

<sub>← [BL31 on ZynqMP](02-bl31-on-zynqmp.md) · [Chapter index](README.md) · [BL32 and OP-TEE (Overview)](04-op-tee-overview.md) →</sub>
