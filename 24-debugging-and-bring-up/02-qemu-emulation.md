# QEMU Emulation

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## Emulation models selected hardware behavior

QEMU can run firmware and Linux against modeled processors and devices. It is valuable for boot-flow, userspace and integration tests that the model supports. It does not reproduce physical signal timing, DDR training margins, analog behavior or arbitrary PL logic.

For this guide, the saved reference setup uses AMD's PetaLinux 2024.1 QEMU binaries and the ZCU106 BSP prebuilt artifacts. It includes a PMU-side MicroBlaze instance and an A53-side AArch64 instance. They cooperate through the selected machine description and shared machine path.

A generic distribution QEMU executable with a similar name is not automatically equivalent. AMD-specific machine options and hardware description support belong to a particular build. Record the executable and version with every emulation result.

## There are two different device-tree roles

The inspected launch script supplies hardware-description DTBs to QEMU through `-hw-dtb`: `zynqmp-qemu-multiarch-pmu.dtb` and `zynqmp-qemu-multiarch-arm.dtb`. These describe the modeled machine for the emulator's flow.

It separately loads `system.dtb` into guest memory for the firmware/Linux boot path. The guest device tree describes devices to software running inside the emulation. Changing the guest DTB does not create a corresponding hardware model in QEMU.

This distinction is especially important for PL devices. A new guest node can make Linux attempt to probe an address, but if no model implements that device, the driver cannot validate real register behavior. A successful device-tree compilation is therefore much weaker than a successful hardware-driver test.

## Read the actual launch artifacts

The saved `reference-setup/scripts/qemu_start.sh` loads these A53-side artifacts:

| Artifact | Inspected placement or role |
| --- | --- |
| `system.dtb` | Raw load at `0x00100000` |
| `Image` | Raw load at `0x00200000` |
| `ramdisk.cpio.gz.u-boot` | Raw load at `0x04000000` |
| `boot.scr` | Raw load at `0x20000000` |
| `u-boot.elf`, `bl31.elf` | ELF-aware loader inputs |
| `rootfs.ext4` | Raw SD backing image |

These are script inputs for the recorded flow, not universal load addresses. ELF loading and raw loading use different metadata. A raw file needs explicit placement; an ELF carries load/entry information. Review overlap using actual sizes, including decompression and runtime requirements.

The PMU instance loads a QEMU-specific ROM image and PMU firmware. Starting only the A53 command while omitting its expected PMU counterpart can fail in firmware-service paths even when the Linux image itself is unchanged.

## Distinguish direct loading from BootROM boot

The launch script places several artifacts directly into guest memory. This bypasses parts of a physical storage/BootROM loading path. The saved U-Boot log reports `Bootmode: JTAG_MODE`, consistent with that scripted flow.

A successful emulated boot therefore does not prove that an SD card's partition layout, QSPI offsets or secure BootROM policy are correct. The same payloads can work when directly loaded but fail when the real first-stage loader reads a malformed container or storage location.

Use emulation to answer the question it actually exercises: whether those loaded artifacts cooperate through the modeled handoff and Linux/userspace path. Use Bootgen inspection and physical boot tests for the other boundaries.

## Console and network paths need explicit endpoints

The inspected script maps `ttyPS0` to a Unix-domain socket and logs it, while another serial output goes to a separate file. Looking at the wrong console can create a false hang diagnosis. TF-A, U-Boot and Linux can use different UART choices depending on configuration.

Its user-network setup forwards host `127.0.0.1:2222` to guest port 22. This is a host-local forwarding rule, not a bridge that makes the guest a normal peer on the physical LAN. Host-to-guest access, guest outbound access and physical-network reachability have different paths.

The captured interface used `10.0.2.15` in the QEMU network. Do not copy this address into a physical deployment as if it were a board default. Port conflicts and an old emulator process can also make a new test connect to the wrong guest; identify the process and artifact set behind a session.

## Writable images can contaminate later tests

The inspected script attaches `rootfs.ext4` directly as a raw backing file. A running guest can modify that file. If the next run reuses it, package installations and configuration edits from earlier tests remain, so the next result is not necessarily a clean BSP baseline.

Use a disposable copy or a supported snapshot/overlay strategy for repeatable tests. Record the base image hash and whether the run preserved changes. Do not run the existing helper blindly against an important image: it also recreates its run directory. This revision inspected the script without launching it.

A test that passes only after a previous guest installed a package has an undeclared image dependency. Repeating it from a clean backing image is the appropriate check, rather than treating the modified guest as proof that the original image includes the package.

## Interpret captured boot evidence

The saved log identifies Linux `6.6.10-xilinx-v2024.1-g3af4295e00ef`, the ZCU106 model and the `root=/dev/ram0` initial command line. Later it identifies a QEMU SD device and mounts ext4 from `mmcblk0`. These observations describe the specific prebuilt flow.

They do not show physical DDR training, VCU operation, RPU real-time behavior or flash endurance. Host scheduling and emulator implementation also affect elapsed time, so a QEMU boot-duration result is not a silicon performance benchmark.

## Debug from process to guest

If no output appears, inspect emulator startup errors and console selection first. If firmware starts but Linux does not, inspect loaded artifacts, addresses and boot script. If Linux starts but root setup fails, inspect the backing image and actual root arguments. If SSH fails while the console works, inspect guest service state and host forwarding.

Keep both emulator stderr and guest serial logs. An unimplemented device access may be visible only outside the guest. A guest kernel panic may be visible only on its console. Combining the two provides the boundary needed to distinguish model limitations from guest software errors.

> [!NOTE]
> **Not run on the reference setup during this revision:** a fresh QEMU boot. Existing scripts and boot/network captures were inspected. Physical-hardware conclusions and a clean-image rerun remain separate tests.

## References

- Inspected `reference-setup/scripts/{qemu_start.sh,boot_capture.py}` and existing `captures/boot-prebuilt3.log`, outside the repository.
- AMD UG1144 (2024.1), QEMU boot flow; installed `petalinux-boot qemu` interface.
- [AMD QEMU source](https://github.com/Xilinx/qemu), use the revision selected by the 2024.1 tool release rather than assuming upstream equivalence.

---

<sub>← [JTAG, XSDB and XSCT](01-jtag-xsdb-and-xsct.md) · [Chapter index](README.md) · [Custom Board Bring-Up](03-custom-board-bring-up.md) →</sub>
