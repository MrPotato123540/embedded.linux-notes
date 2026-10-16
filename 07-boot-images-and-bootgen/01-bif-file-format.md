# The BIF File Format

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[07 · Boot Images, BIF and Bootgen](README.md)** · Part IV: Boot

## BIF structure

A **Boot Image Format (BIF)** file describes the payloads passed to Bootgen. It contains an image name, braces and a list of input files with attributes. It is a build input, not a script executed by the board.

The reference BSP supplies this input order: FSBL, PMU firmware, TF-A, device tree and U-Boot. Its PMU firmware uses the special `pmufw_image` boot-header path; the device tree has `load=0x100000`. TF-A uses `exception_level=el-3` and `trustzone`; U-Boot uses `exception_level=el-2`. The five inputs are not five ordinary image headers.

| Attribute | Meaning |
| --- | --- |
| `bootloader` | Identifies the first-stage loader |
| `pmufw_image` | Selects BootROM handling of PMU firmware |
| `destination_cpu` | Processor receiving the partition |
| `destination_device` | Selects a supported non-CPU destination, such as PL |
| `exception_level`, `trustzone` | Handoff execution attributes |
| `load`, `startup` | Memory placement and execution entry |
| `offset`, `alignment` | Placement inside the output image |
| `partition_owner` | Stage responsible for partition handling |

An ELF supplies segment and entry information; a data file needs suitable placement metadata. Do not confuse `offset` in the output file with `load` in target memory.

## Design variants

Add a bitstream only when the early boot flow should configure the PL. R5 firmware needs the correct RPU mode and memory layout. A data partition must not be handed off as executable code. Multiple images require explicit ownership and startup policy.

## Read the reference BIF one decision at a time

The actual BSP uses the following BIF. This is the supplied file, not a new board recipe:

```text
the_ROM_image:
{
    [bootloader, destination_cpu=a53-0] zynqmp_fsbl.elf
    [pmufw_image] pmufw.elf
    [destination_cpu=a53-0, exception_level=el-3, trustzone] bl31.elf
    [destination_cpu=a53-0, load=0x100000] system.dtb
    [destination_cpu=a53-0, exception_level=el-2] u-boot.elf
}
```

The first input identifies the first-stage loader and its processor. The PMU input uses special initial-image handling. BL31 supplies the Secure EL3 monitor. The DTB is data with an explicit destination address. U-Boot is the Non-secure next-stage executable at EL2 in this arrangement.

There is no bitstream entry. The presence of `system.bit` in the same directory does not change the BIF. There is also no kernel or root filesystem input in this file. Later bootloader policy selects those artifacts separately.

## Attribute groups answer different questions

Destination attributes identify the consumer. Execution attributes describe processor state. Memory attributes describe load or entry locations. File-placement attributes describe layout inside the container. Ownership attributes describe which stage handles the partition. Keep these groups separate when reviewing a BIF change.

For example, changing `offset` moves stored data within the output image. It does not move the program's runtime code to another RAM address. Changing `load` affects destination placement, but moving linked executable code may also require a compatible link address or relocation support. A packaging override cannot make arbitrary code position-independent.

Similarly, `trustzone` is an execution/security attribute. It is not itself a request to sign every partition. Authentication and encryption have their own format and key-policy inputs. Review those separately from the exception level.

## ELF metadata and explicit attributes must agree

An ELF can describe its entry point and loadable content. A raw data file has no equivalent executable metadata, so placement must be supplied through the supported format. The reference DTB uses `load=0x100000` for that reason.

Inspect ELF program headers and sections before overriding addresses. File-backed data, BSS, stacks and translation tables can require different memory accounting. An entry point is one address within a larger runtime footprint.

The reference BL31 ELF enters at `0xFFFEA000`, matching the packaged entry reported by Bootgen. Its broader ELF layout includes additional runtime regions. This is why BIF review should be paired with ELF and memory-map review rather than limited to filenames.

## Ordering includes lifetime assumptions

The first-stage image must be available when the initial boot flow needs it. Later partitions must be loaded before their consumers run. A PL design must exist before software accesses its devices. A remote-processor application needs the correct memory and ownership setup before handoff.

Early handoff or several processors can make this more complex than a single linear list. The FSBL state machine can continue work after an early handoff. Review whether the next running component can access memory or hardware that another stage is still changing.

For a partial-reconfiguration design, a boot BIF is only part of the system. The static design, partial image, overlay and application must remain compatible. Adding a file to the boot container does not define the runtime quiesce and replacement procedure.

## Paths are release inputs

Relative paths are resolved in the packaging context. A BIF copied to another directory can select different files or fail to find them. For a controlled experiment, use an explicit working directory or absolute paths and record the selected input hashes.

The regeneration experiment in the next section used absolute paths to the supplied BSP inputs and produced an image identical to the supplied `BOOT.BIN`. That is evidence for this BIF and these binaries. It does not establish that their source can be rebuilt identically or that the image boots on a physical board.

## Review the generated representation

After generation, decode the output and compare processor, load, entry, exception-level and security fields. Check the number and type of image/partition records. The special PMU firmware entry means that five BIF inputs produce four image headers in the reference image.

Keep the BIF, tool version and hashes with the result. A short, reviewed BIF is a useful release contract because it shows the exact assembly decisions. A directory of plausible firmware names is not equivalent evidence.

## References

- Inspected `xilinx-zcu106-2024.1:pre-built/linux/images/bootgen.bif`
- AMD UG1283 (2024.1), BIF syntax and attribute reference

---

<sub>[Chapter index](README.md) · [Bootgen](02-bootgen.md) →</sub>
