# JTAG, XSDB and XSCT

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## Debug connection

`hw_server` provides hardware access; XSDB connects to it and exposes processor targets. XSCT adds scripting and software-development operations. Select the intended processor explicitly before loading code or changing memory.

Read-only inspection should come before writes. Register access can still have side effects, so use the register specification. The debugger's address view depends on its target and access path.

## ELF and control flow

Load the ELF built for the selected processor and use its symbols for breakpoints and stepping. Preserve the source revision and compiler settings. A raw binary lacks the same symbol and segment information.

Tcl scripts should check target presence and command failures. Avoid hard-coded target numbers that change after reconnecting. A script should leave the system in a known state after an error.

> [!NOTE]
> **Not run on the reference setup:** physical JTAG operations. Earlier QEMU GDB-stub experiments do not validate physical register access through a probe.

## References

- AMD UG1400 (2024.1), XSDB/XSCT and debugging
- [JTAG boot](../06-boot-sequence/14-jtag-boot.md)

---

<sub>[Chapter index](README.md) · [QEMU Emulation](02-qemu-emulation.md) →</sub>
