# Bitstreams: .bit and .bin

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[07 · Boot Images, BIF and Bootgen](README.md)** · Part IV: Boot

## Bitstream formats

A bitstream configures programmable logic. It contains configuration commands and frame data; a `.bit` file also carries a tool-format header. A raw binary output is prepared for a particular loading interface. The suffix `.bit.bin` is a naming convention, not proof that the bytes suit every loader.

Conversion can involve header removal and byte-order handling. Use the supported conversion tool for the selected load path. Renaming `.bit` to `.bin` does not perform a conversion.

## Full and partial configuration

A full bitstream configures the design. A partial bitstream changes a reconfigurable region and must match the static design used to build it. Compression changes storage representation, not the need for a compatible configuration path.

| Loader | When it runs |
| --- | --- |
| FSBL through PCAP | Before the normal Linux boot |
| U-Boot FPGA commands | During bootloader execution |
| Linux FPGA manager | Under Linux control |

PCAP means **Processor Configuration Access Port**. The loader, bitstream format and hardware state must agree. Stop users of a region before reconfiguration; replacing logic while a DMA engine is active can corrupt memory or hang a bus.

> [!NOTE]
> **Not run on the reference setup:** physical full/partial configuration and format conversion validation.

## References

- AMD UG1283 (2024.1), `process_bitstream`
- `embeddedsw@xilinx_v2024.1:lib/sw_services/xilfpga/`
- [FPGA manager](../17-pl-integration-and-dfx/03-fpga-manager.md)

---

<sub>← [BOOT.BIN Anatomy](03-boot-bin-anatomy.md) · [Chapter index](README.md) · [Generating Boot Images With PetaLinux](05-petalinux-package-boot.md) →</sub>
