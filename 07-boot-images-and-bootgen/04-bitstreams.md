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

## Format conversion is part of the loading contract

A bitstream contains configuration information for the programmable logic. Tool-generated wrappers can add metadata around that information, and different consumers expect different representations. The correct conversion depends on the loader and platform, not only on the filename suffix.

Renaming a file changes no bytes. A `.bit` file renamed to `.bin` can still carry a header that the selected loader does not expect. Conversely, removing bytes manually can destroy required configuration data. Use the documented tool path and inspect the result for the intended consumer.

Byte-order handling is another reason to avoid generic conversion recipes. A loader may expect a representation already prepared for its access path. Applying a second swap or conversion can corrupt an otherwise valid payload. Keep the conversion command and source bitstream identity in the release record.

## The bitstream and software describe the same hardware interface

A Linux driver expects a particular register map, interrupt behavior, clock/reset arrangement and possibly DMA interface. The bitstream implements that contract. The device tree describes how software reaches it. These files must be versioned as one compatible set.

A successful configuration operation proves that the configuration path accepted and processed data according to its checks. It does not prove that a driver is using the right register offsets or that external board connections match the design. A safe identification register, if the IP defines one, can help confirm the loaded hardware interface.

The supplied BSP contains a `system.bit` file of 10,545,840 bytes, but its reference boot BIF does not include that file. This concrete observation separates “available artifact” from “configured during early boot.” Inspect the chosen early or late loading flow before assuming PL devices exist.

## Full configuration and partial configuration have different compatibility rules

A full design establishes the overall PL configuration. A partial design changes a reconfigurable region within a particular static design. The partial image must match that static implementation and its interface constraints. A similar block diagram or identical application name is not enough.

The static design provides routing and interfaces around the region. A partial image generated against another static implementation can be incompatible even if its register map appears unchanged. Preserve the build relationship and design identifiers required by the DFX flow.

Software compatibility is an additional requirement. Replacing one accelerator with another may change devices, buffers and application protocol. The overlay and userspace configuration must follow the loaded function, and old drivers must stop using removed resources.

## Quiesce users before changing hardware

Before reconfiguration, stop application submissions and wait for or cancel active work through the supported driver interface. Disable or isolate the relevant data path as required by the design. Ensure that DMA cannot continue writing memory while the region is absent or changing.

After configuration, restore clocks/resets and device descriptions in the supported order, bind the intended drivers and verify readiness before allowing new work. If configuration fails, keep the region unavailable and follow a defined recovery path. A failed operation must not leave applications treating stale device handles as healthy hardware.

This sequence is a lifetime problem, not only a file-loading problem. Buffer ownership, interrupts and driver removal need to be correct under both normal operation and failure.

## Early and late loading change probe timing

With early loading, the boot firmware configures PL before Linux starts. The base tree can describe devices expected at initial probe. Packaging must include the correct PL input, and early firmware must perform the required initialization.

With late loading, Linux's FPGA framework and the platform firmware cooperate to configure the design. Device creation may use overlays or another supported management path. The driver must not access its register window before the hardware is available.

Moving a design between these policies can require changes to the base tree, overlay, firmware package and application startup. It is not enough to copy the bitstream into another directory.

## Validate the selected path

Record the source bitstream, conversion tool/version, converted output, static/partial relationship and loader. Check configuration status, then test the actual peripheral function and repeated load/unload behavior where supported. Include failure recovery and active-work rejection.

Physical full/partial configuration and conversion acceptance were not tested on the reference setup. The file-size and BIF observations were checked locally. The expanded procedure states the additional hardware evidence needed before accepting a loading design.

## References

- AMD UG1283 (2024.1), `process_bitstream`
- `embeddedsw@xilinx_v2024.1:lib/sw_services/xilfpga/`
- [FPGA manager](../17-pl-integration-and-dfx/03-fpga-manager.md)

---

<sub>← [BOOT.BIN Anatomy](03-boot-bin-anatomy.md) · [Chapter index](README.md) · [Generating Boot Images With PetaLinux](05-petalinux-package-boot.md) →</sub>
