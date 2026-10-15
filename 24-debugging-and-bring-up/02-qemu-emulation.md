# QEMU Emulation

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## What the emulator covers

AMD QEMU can model the application processors and PMU using a coordinated multi-architecture launch. PetaLinux supplies a release-specific QEMU boot flow and machine-description files.

The reference setup uses copies of the prebuilt images, serial sockets and host SSH forwarding. The writable rootfs copy changes during use; it should not be confused with the original BSP artifact.

## Useful tests and limits

QEMU is useful for userspace, boot sequencing and supported virtual peripherals. It does not establish physical DDR margins, PL timing, cache-coherent DMA correctness or real device throughput.

Keep the launch arguments, image hashes and logs. A QEMU-specific device tree can differ from the physical board tree. Success under one launch configuration does not prove that the same files boot from SD or QSPI.

The reference notes warn that resetting through the monitor can hang this multi-architecture setup. Use the established guest reboot procedure for that environment.

## References

- `reference-setup/README.txt` and scripts
- Saved QEMU serial captures
- AMD UG1144 (2024.1), QEMU boot

---

<sub>← [JTAG, XSDB and XSCT](01-jtag-xsdb-and-xsct.md) · [Chapter index](README.md) · [Custom Board Bring-Up](03-custom-board-bring-up.md) →</sub>
