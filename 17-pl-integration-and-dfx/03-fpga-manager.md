# Linux FPGA Manager

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Framework and platform driver

The Linux FPGA-manager framework separates common programming control from device-specific loading. On ZynqMP, the platform driver uses the supported firmware path to configure the PL. Manager state describes the programming operation; it does not verify the application behavior of the loaded design.

A firmware file must have the format expected by the loader. Use supported bitstream conversion, full/partial flags and a matching device-tree description. Do not infer readiness from the filename.

## Runtime sequence

Stop users of the affected hardware, complete or cancel DMA, isolate the region as required, load the bitstream, then activate matching devices and applications. `fpgautil` and vendor packaging can coordinate supported operations, but their command syntax and available interfaces depend on the release.

A generic writable sysfs loading interface is not guaranteed by the upstream manager API. Check the actual vendor implementation before copying a sysfs command.

> [!NOTE]
> **Not run on the reference setup:** full bitstream loading through Linux on hardware.

## Manager, region and bridge have different jobs

The FPGA Manager framework provides a common programming interface. A manager driver performs the device-specific loading operation. An FPGA region connects that manager with the programmable region and any bridges that must be isolated during programming.

A bridge represents a path that must be disabled while logic is unsafe. The framework can coordinate registered bridges, but it cannot invent missing isolation hardware or discover every active application. The system designer must describe the relevant paths and stop consumers before replacement.

Device-tree overlays can connect programming with device enumeration. The region layer can program the selected image and then allow the new device description to become active. Applying an ordinary peripheral node without the corresponding programming/lifecycle arrangement can probe hardware before it exists.

## Follow the ZynqMP driver into firmware

In `drivers/fpga/zynqmp-fpga.c`, the manager's `write_init` callback stores image flags and checks requested features against the firmware-supported feature list. These flags distinguish full/partial and supported security-related modes. A rejected feature is a policy/capability failure before the main load.

The write callback allocates a DMA-coherent staging buffer, copies the image into it and accounts for alignment. For the user-key path, it also allocates space for the key material required by that interface. The code issues a write barrier before invoking `zynqmp_pm_fpga_load()`.

That sequence is a concrete example of coherent memory still needing ordering: firmware must not begin consuming the buffer before the CPU's writes are visible in the required order. The callback frees the staging buffer after the firmware call returns. Its lifetime therefore depends on the firmware API's completion contract.

The operation goes through platform firmware rather than treating the PL configuration path as an arbitrary userspace MMIO device. Linux configuration, firmware capability and the image format must all agree.

## Programming completion is not application readiness

A successful load means the programming operation reached its success condition. The new logic may still need reset release, clock setup, driver probe and application-level initialization. A device can also program successfully and implement the wrong register contract.

Use separate states for image available, programming accepted, programming complete, driver bound and service ready. A management interface that reports only one “loaded” Boolean hides the boundary needed for diagnosis.

For a safe identity check, use a register whose behavior and availability are defined by the hardware design. Do not start an application merely because the manager's state is operational if its dependent driver has not successfully probed.

## Firmware filenames are lookup inputs

The firmware loader obtains an image by its requested name from the configured firmware mechanism. Package the expected payload format and location through a recipe. A `.bit` container, a converted binary bitstream and a different-family programming image are not interchangeable just because they describe programmable logic.

The supplied BSP includes a `fpga-manager-script` recipe whose actual source is `fpgautil.c`. Despite the package name, review the installed utility and release implementation before using command options copied from another release. This section does not issue a programming command against unknown hardware.

An overlay's firmware name must resolve to the same artifact whose compatibility was reviewed. A stale file at the expected path can make a deployment appear correct while loading an older design.

## Failure paths must retain a safe state

If programming fails after isolation, do not automatically resume old clients. The old hardware may already be partly replaced, and the new hardware may not be functional. Keep access blocked until a known compatible image is loaded or the system follows its recovery policy.

If driver probe fails after programming succeeds, the manager may be healthy while the device description or dependency chain is wrong. Preserve firmware load status and probe error separately. Repeating programming can erase useful evidence without fixing the missing clock or wrong compatible string.

An interrupted management process does not by itself define what happens to the hardware. The supervisor should track the transaction and reconcile actual state on restart rather than assuming its last saved message is current.

## Ownership before removal

Before replacing an active region, stop new requests, drain or cancel existing jobs, stop bus masters and remove dependent software interfaces in the required order. Bridge isolation prevents selected transactions but does not necessarily flush an engine's internal state or complete userspace callbacks.

The old device tree and driver state must not survive as valid handles to a new hardware instance. Review overlay removal constraints and every callback that retains device-tree data. The pinned overlay documentation warns that retained pointers into removed overlay storage become invalid.

> [!NOTE]
> **Not run on the reference setup:** FPGA programming, bridge isolation and recovery after a failed load. The pinned driver and region framework were inspected; no firmware programming call was issued.

## References

- [linux-xlnx@xilinx-v2024.1:drivers/fpga/zynqmp-fpga.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/fpga/zynqmp-fpga.c).
- [FPGA region API](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/fpga/fpga-region.rst) and [manager API](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/fpga/fpga-mgr.rst), same pinned tag.
- Inspected BSP `meta-xilinx/meta-xilinx-core/recipes-bsp/fpga-manager-script/files/fpgautil.c`.

- Linux 6.6 [FPGA manager](https://docs.kernel.org/6.6/driver-api/fpga/fpga-mgr.html)
- `linux-xlnx@xilinx-v2024.1:drivers/fpga/zynqmp-fpga.c`

---

<sub>← [Accessing PL Peripherals From Linux](02-accessing-pl-peripherals.md) · [Chapter index](README.md) · [DFX: Dynamic Function eXchange](04-dfx-dynamic-function-exchange.md) →</sub>
