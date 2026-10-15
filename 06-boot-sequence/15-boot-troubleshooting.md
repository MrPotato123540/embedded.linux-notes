# Boot Troubleshooting

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Find the last confirmed stage

| Symptom | First checks |
| --- | --- |
| No output | Power, reset, mode straps, UART selection and baud rate |
| FSBL error | Stage/error code, hardware export, storage and DDR initialization |
| FSBL finishes, no U-Boot | BL31 and U-Boot addresses, handoff state, console routing |
| U-Boot cannot load files | Selected device, partition, filesystem and filename |
| Stops at `Starting kernel ...` | Arm64 entry state, DTB and early console |
| Root-mount panic | Root argument, driver availability and filesystem format |
| Login works, application fails | Services, permissions, libraries and application logs |

## Evidence to keep

Save the complete serial log, tool versions, image checksums, boot mode and reset type. Record whether the test used prebuilt files or a new local build. “Same filename” is not enough to identify an image.

Read hardware error registers only through a documented access path and before a reset changes the evidence. Decode FSBL errors against the exact source release. A numeric code from another release may have a different meaning.

## Reduce the problem

Change one input at a time. Start with the reference BSP on the reference board when possible. Then add the new hardware export, firmware change or custom driver separately. Repeatedly cleaning the build cannot repair an electrical clock or reset problem.

For a stuck processor, JTAG can show the program counter and stack, but use the matching symbols. QEMU is useful for software sequencing; it cannot prove DDR margins or physical peripheral timing.

## References

- UG1085 (v2.5), boot error status and reset sections
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_error.h`
- Saved reference boot and U-Boot captures

---

<sub>← [JTAG Boot](14-jtag-boot.md) · [Chapter index](README.md) · Next chapter: [07 · Boot Images, BIF and Bootgen](../07-boot-images-and-bootgen/README.md) →</sub>
