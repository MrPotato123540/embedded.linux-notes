# dfx-mgr and Accelerator Packages

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Package management for PL applications

`dfx-mgrd` manages supported accelerator packages; `dfx-mgr-client` requests operations. Packages can contain the bitstream, overlay and metadata describing the shell or accelerator. Typical AMD layouts use `/lib/firmware/xilinx` with files such as `shell.json`, `accel.json`, `.bit.bin` and `.dtbo`.

The metadata must match the actual static design and load flow. Copying files into the directory does not prove that the daemon can validate or activate them.

## PetaLinux 2024.1 integration

The inspected application-template help lists separate full, static and partial DFX templates for supported device families. Select the ZynqMP template matching the design. A partial application can depend on the static package; keep that dependency in the build and deployment record.

Kria's `xmutil` adds a platform application-management interface. Use the matching platform's package conventions and firmware version.

> [!NOTE]
> **Not run on the reference setup:** package listing, activation and removal on a physical DFX platform.

## References

- Executed PetaLinux 2024.1 `petalinux-create apps --help`
- AMD [dfx-mgr source](https://github.com/Xilinx/dfx-mgr)

---

<sub>← [DFX: Dynamic Function eXchange](04-dfx-dynamic-function-exchange.md) · [Chapter index](README.md) · [DMA Between PS and PL](06-dma-between-ps-and-pl.md) →</sub>
