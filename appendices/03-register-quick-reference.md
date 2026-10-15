# Register Quick Reference

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[Appendices](README.md)** · Appendices

## Selected register addresses

These addresses are for the ZynqMP system view. Check processor access, security permissions and register semantics before reading. The table is a navigation aid, not a programming sequence.

| Address | Register | Main use | Source cross-reference |
| --- | --- | --- | --- |
| `0xFF5E0200` | `CRL_APB.BOOT_MODE_USER` | Software-visible boot-mode selection | UG1087, CRL_APB `BOOT_MODE_USER`; FSBL `CRL_APB_BOOT_MODE_USER` |
| `0xFF5E0220` | `CRL_APB.RESET_REASON` | Recorded reset causes | UG1087, CRL_APB `RESET_REASON`; FSBL `CRL_APB_RESET_REASON` |
| `0xFFCA0010` | `CSU.CSU_MULTI_BOOT` | Multiboot selection state | UG1087, CSU `CSU_MULTI_BOOT`; FSBL `CSU_CSU_MULTI_BOOT` |

The addresses were cross-checked against the pinned FSBL header and the existing architecture notes. Register access semantics and complete bit definitions must be checked in UG1087 before a write. The multiboot value is interpreted by the boot flow; it is not a universal byte offset.

Error diagnosis also uses CSU/PMU status registers. Select the documented register for the failing stage instead of treating one generic “error register” as sufficient. Save values before reset or software clears them.

> [!NOTE]
> **Not run on the reference setup:** a new physical read/write validation of this table. Existing QEMU observations do not prove silicon reset behavior.

## References

- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_hw.h`
- UG1087 Zynq UltraScale+ Devices Register Reference, named register pages
- [Memory map](../03-zynqmp-architecture/04-memory-map.md) and [reset behavior](../03-zynqmp-architecture/07-clocks-power-and-reset.md)

---

<sub>← [Command Cheat Sheets](02-command-cheatsheets.md) · [Chapter index](README.md) · [References and Sources](04-references.md) →</sub>
