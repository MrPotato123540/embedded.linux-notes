# System Address Map

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · ZCU106

**[03 · Zynq UltraScale+ MPSoC Architecture](README.md)** · Part II: Zynq UltraScale+ MPSoC Hardware

## In short

- ZynqMP has a **40-bit physical address space** (1 TB). Below 4 GB sit the low 2 GB of DDR, the PL windows, the QSPI linear window, the PCIe low window and all PS registers. Above 4 GB sit the high DDR (from `0x8_0000_0000`), large PL windows and the PCIe high windows.
- A board with 4 GB of DDR therefore has two memory banks: `0x0000_0000 – 0x7FFF_FFFF` and `0x8_0000_0000 – 0x8_7FFF_FFFF`. The top 1 MB of the lower bank is reserved for the PMU firmware.
- The PS registers you will touch most often are `CRL_APB` (`0xFF5E_0000`) and `CRF_APB` (`0xFD1A_0000`) for clocks and resets, `IOU_SLCR` (`0xFF18_0000`) for MIO pins, `CSU` (`0xFFCA_0000`) and `PMU_GLOBAL` (`0xFFD8_0000`).
- The same map appears in four places: UG1085 Table 10-1, the Vivado Address Editor (stored in the XSA), the device tree `reg` properties and, at run time, `/proc/iomem`. Reading them side by side is the fastest way to debug an address problem.
- Reading a register is not always harmless. The block must be powered and clocked, and some registers are secure-only or owned by the PMU firmware.

## Concepts

### The top-level map

From UG1085 (v2.5), Chapter 10, Table 10-1 "Top-Level System Address Map":

| Region | Range (size) |
| --- | --- |
| DDR low | `0x0000_0000 – 0x7FFF_FFFF` (2 GB) |
| `M_AXI_HPM0_LPD` (LPD to PL) | `0x8000_0000 – 0x9FFF_FFFF` (512 MB) |
| VCU | `0xA000_0000 – 0xA3FF_FFFF` (64 MB) |
| `M_AXI_HPM0_FPD` | `0xA400_0000 – 0xAFFF_FFFF` (192 MB) |
| `M_AXI_HPM1_FPD` | `0xB000_0000 – 0xBFFF_FFFF` (256 MB) |
| Quad-SPI linear | `0xC000_0000 – 0xDFFF_FFFF` (512 MB) |
| PCIe low | `0xE000_0000 – 0xEFFF_FFFF` (256 MB) |
| Reserved | `0xF000_0000 – 0xF7FF_FFFF` (128 MB) |
| STM CoreSight | `0xF800_0000 – 0xF8FF_FFFF` (16 MB) |
| GIC | `0xF900_0000 – 0xF90F_FFFF` (1 MB) |
| Reserved | `0xF910_0000 – 0xFCFF_FFFF` (63 MB) |
| FPD slaves | `0xFD00_0000 – 0xFDFF_FFFF` (16 MB) |
| Upper LPD slaves | `0xFE00_0000 – 0xFEFF_FFFF` (16 MB) |
| Lower LPD slaves | `0xFF00_0000 – 0xFFBF_FFFF` (12 MB) |
| CSU, PMU, TCM, OCM | `0xFFC0_0000 – 0xFFFF_FFFF` (4 MB) |
| Reserved | `0x1_0000_0000 – 0x3_FFFF_FFFF` (12 GB) |
| `M_AXI_HPM0_FPD` | `0x4_0000_0000 – 0x4_FFFF_FFFF` (4 GB) |
| `M_AXI_HPM1_FPD` | `0x5_0000_0000 – 0x5_FFFF_FFFF` (4 GB) |
| PCIe high | `0x6_0000_0000 – 0x7_FFFF_FFFF` (8 GB) |
| DDR high | `0x8_0000_0000 – 0xF_FFFF_FFFF` (32 GB) |
| `M_AXI_HPM0_FPD` | `0x10_0000_0000 – 0x47_FFFF_FFFF` (224 GB) |
| `M_AXI_HPM1_FPD` | `0x48_0000_0000 – 0x7F_FFFF_FFFF` (224 GB) |
| PCIe high | `0x80_0000_0000 – 0xBF_FFFF_FFFF` (256 GB) |
| Reserved | `0xC0_0000_0000 – 0xFF_FFFF_FFFF` (256 GB) |

UG1085 note 1 to the table: the VCU range is where the design tools place the VCU by default; without a VCU, `M_AXI_HPM0_FPD` gets the full 256 MB from `0xA000_0000`.

Three design consequences:

- **DDR is split.** The low 2 GB must stay below 4 GB for 32-bit masters and for software that cannot use 64-bit addresses. Everything above 2 GB is placed at `0x8_0000_0000`. A 4 GB board has 2 GB in each window; there is no DDR at `0x8000_0000`.
- **The PL has small 32-bit windows and large 64-bit windows.** A 32-bit PL master, or a 32-bit RPU, can only use the windows below 4 GB ([section 02](02-ps-and-pl.md)).
- **All PS registers live in the top 256 MB of the 4 GB space** (`0xF000_0000` upward), so every processor, including the 32-bit RPU and PMU, can reach them.

### The last 4 MB

The region `0xFFC0_0000 – 0xFFFF_FFFF` holds the on-chip memories and the boot-related units. From UG1085 (v2.5), Table 10-2, in ascending order:

| Slave | Range (size) |
| --- | --- |
| CSU ROM | `0xFFC0_0000 – 0xFFC1_FFFF` (128 KB) |
| CSU RAM | `0xFFC4_0000 – 0xFFC4_7FFF` (32 KB) |
| eFUSE | `0xFFCC_0000 – 0xFFCC_FFFF` (64 KB) |
| PMU ROM | `0xFFD0_0000 – 0xFFD3_FFFF` (256 KB) |
| PMU RAM | `0xFFDC_0000 – 0xFFDD_FFFF` (128 KB) |
| RPU TCMs and caches | `0xFFE0_0000 – 0xFFEF_FFFF` (layout in [section 05](05-on-chip-memories.md)) |
| OCM | `0xFFFC_0000 – 0xFFFF_FFFF` (256 KB) |

The OCM ends exactly at the top of the 32-bit space. It therefore contains `0xFFFF_0000`, the Cortex-R5F high-vector address, and it is where the BootROM loads the FSBL.

### The reserved megabyte below 2 GB

The device tree of a PetaLinux project does not describe the full 2 GB of DDR low:

```dts
	memory@0 {
		device_type = "memory";
		reg = <0x00 0x00 0x00 0x7ff00000 0x08 0x00 0x00 0x80000000>;
	};
```

The upstream `zynqmp-zcu106-revA.dts` in `linux-xlnx` describes `0x80000000`; the device tree generator (DTG) writes `0x7ff00000`. The DTG takes the size from the XSA, where the A53's DDR range `psu_ddr_0` ends at `0x7FEF_FFFF` (see [Hands-on](#from-the-xsa-with-xsct)). PG201 (v3.5), "DDR Software Self-Refresh", explains why: the PS configuration "reserves the lower DDR (0x7ff00000 to 0x7fffffff when lower 2GB DDR is enabled) for AMD's use only (This memory is used for APU restart and it is always required to be enabled for the PMU by default)."

If you write a device tree by hand, keep that megabyte out of Linux's memory, either by shrinking `memory@0` as the DTG does or with a `reserved-memory` node marked `no-map`.

### Register blocks you will touch

From UG1085 (v2.5), Table 10-4 "System-level Register Sets", with the addresses of a few registers from the generated `psu_init.h`:

| Block | Base | Secure access | Controls | Examples |
| --- | --- | --- | --- | --- |
| `CRF_APB` | `0xFD1A_0000` | XMPU | FPD clocks and resets | `APLL_CTRL` `0xFD1A0020`, `ACPU_CTRL` `0xFD1A0060`, `RST_FPD_TOP` `0xFD1A0100` |
| `APU` | `0xFD5C_0000` | XMPU | APU control | |
| `FPD_SLCR` | `0xFD61_0000` | XMPU | FPD system-level control | `AFI_FS` `0xFD615000` |
| `FPD_SLCR_SECURE` | `0xFD69_0000` | Yes | FPD TrustZone settings | |
| `IOU_SLCR` | `0xFF18_0000` | XPPU | MIO pin configuration | `MIO_PIN_18` `0xFF180048`, `BANK0_CTRL4` `0xFF180144` |
| `IOU_SECURE_SLCR` | `0xFF24_0000` | Yes | IOU AXI protection | |
| `IOU_SCNTRS` | `0xFF26_0000` | Yes | System timestamp counter | |
| `LPD_SLCR` | `0xFF41_0000` | XPPU | LPD system-level control | `AFI_FS` `0xFF419000` |
| `LPD_SLCR_SECURE` | `0xFF4B_0000` | Yes | LPD TrustZone settings | |
| `CRL_APB` | `0xFF5E_0000` | XPPU | LPD clocks and resets | `IOPLL_CTRL` `0xFF5E0020`, `UART0_REF_CTRL` `0xFF5E0074`, `PL0_REF_CTRL` `0xFF5E00C0`, `BOOT_MODE_USER` `0xFF5E0200`, `RST_LPD_TOP` `0xFF5E023C` |
| `RPU` | `0xFF9A_0000` | XPPU | RPU control | `RPU_GLBL_CNTL` `0xFF9A0000` |

Other blocks that come up in later chapters:

| Block | Base | Source |
| --- | --- | --- |
| `IPI` (inter-processor interrupts) | `0xFF30_0000` | UG1085 Table 10-8 |
| `CSU` (`IDCODE` at `+0x40`, `VERSION` at `+0x44`) | `0xFFCA_0000` | UG1085 Table 10-8, [section 01](01-device-family-overview.md) |
| `PMU_GLOBAL` | `0xFFD8_0000` | UG1085 Table 6-5 |
| `CSU_DMA` | `0xFFC8_0000` | UG1085 Table 10-8 |
| `BBRAM` | `0xFFCD_0000` | UG1085 Table 10-8 |
| DDR controller, DDR PHY | `0xFD07_0000`, `0xFD08_0000` | UG1085 Table 10-9 |
| SMMU registers | `0xFD80_0000` | UG1085 Table 10-9 |

The I/O peripherals sit at 64 KB steps in the LPD (UART0 `0xFF00_0000`, UART1 `0xFF01_0000`, I2C `0xFF02_0000`/`0xFF03_0000`, GEM0–3 `0xFF0B_0000`–`0xFF0E_0000`, QSPI `0xFF0F_0000`, SD0/SD1 `0xFF16_0000`/`0xFF17_0000`, USB0/USB1 `0xFF9D_0000`/`0xFF9E_0000`) and in the FPD (SATA `0xFD0C_0000`, PCIe `0xFD0E_0000`, PS-GTR `0xFD40_0000`, DisplayPort `0xFD4A_0000`, GPU `0xFD4B_0000`, DPDMA `0xFD4C_0000`). The full lists are UG1085 Tables 10-6 to 10-9; the bit fields of every register are in UG1087 (the register reference).

UG1085 Table 10-1 calls the 1 MB region at `0xF900_0000` "APU GIC", and Table 10-5 lists a GIC distributor at `0xF900_0000`. Inside that region, the XSA places the RPU's GIC (`psu_rcpu_gic`) at `0xF900_0000` and the APU's GIC-400 (`psu_acpu_gic`) at `0xF901_0000`, where the Linux device tree also has it ([section 08](08-interrupts-and-gic.md)).

## On ZynqMP

### Where the boot software lives

The address map also tells you where each stage of the boot chain runs. From the ELF headers of the ZCU106 2024.1 prebuilt images and the BSP's `boot.scr`:

| Stage | Location | Address | Source |
| --- | --- | --- | --- |
| PMU firmware | PMU RAM | `0xFFDC_0000` (entry `0xFFDD12A0`) | `pmufw.elf` program headers |
| FSBL | OCM | `0xFFFC_0000` | `zynqmp_fsbl.elf` entry point |
| TF-A BL31 | Top of OCM | `0xFFFE_A000` | `bl31.elf` entry point; `BL31_BASE` in TF-A `platform_def.h` |
| U-Boot | DDR | `0x0800_0000` | `u-boot.elf` entry point; `PLAT_ARM_NS_IMAGE_BASE` in TF-A; `CONFIG_SUBSYSTEM_MEMORY_PSU_DDR_0_BANKLESS_U__BOOT_TEXTBASE_OFFSET=0x8000000` |
| Device tree | DDR | `0x0010_0000` | `boot.scr`: `fatload ... 0x00100000 system.dtb` |
| Kernel `Image` | DDR | `0x0020_0000` | `boot.scr`: `booti 0x00200000 0x04000000 0x00100000` |
| Initial RAM disk | DDR | `0x0400_0000` | Same `booti` line |

TF-A also prints `BL31: Secure code at 0x60000000`, its default `BL32_BASE`, although this BSP has no BL32 (secure OS). [Chapter 06](../06-boot-sequence/README.md) follows the boot chain through these addresses.

## Hands-on

### From the XSA with xsct

The Vivado Address Editor is the source of all PL addresses. Its result is stored in the XSA, and the HSI commands in `xsct` (part of Vitis) can print it without opening Vivado. This script lists every memory range the first A53 core can see:

```tcl
hsi::open_hw_design system.xsa
set cpu [hsi::get_cells -hier psu_cortexa53_0]
foreach r [hsi::get_mem_ranges -of_objects $cpu] {
    puts [format "%-36s %-16s %-16s %s" $r [common::get_property BASE_VALUE $r] [common::get_property HIGH_VALUE $r] [common::get_property SLAVE_INTERFACE $r]]
}
hsi::close_hw_design [hsi::current_hw_design]
```

Run it next to a copy of the XSA. It prints 112 ranges for the ZCU106 design; here filtered to a few:

```console
$ source /tools/Xilinx2024.1/Vitis/2024.1/settings64.sh
$ xsct memmap.tcl | grep -E '^(psu_ddr_[01]|psu_ocm_ram_0|psu_qspi_linear_0|psu_r5_tcm_ram_global|psu_acpu_gic|psu_rcpu_gic|psu_uart_0|psu_crl_apb|mpsoc_ss_axi_intc_0|vcu_0|vcu_ddr4_controller_0) '
mpsoc_ss_axi_intc_0                  0x80000000       0x8000FFFF       s_axi
vcu_0                                0xA0100000       0xA01FFFFF       S_AXI_LITE
vcu_ddr4_controller_0                0x4800000000     0x487FFFFFFF     S_AXI_PORT3
psu_acpu_gic                         0xF9010000       0xF907FFFF
psu_crl_apb                          0xFF5E0000       0xFF85FFFF
psu_ddr_0                            0x0              0x7FEFFFFF
psu_ddr_1                            0x800000000      0x87FFFFFFF
psu_ocm_ram_0                        0xFFFC0000       0xFFFFFFFF
psu_qspi_linear_0                    0xC0000000       0xDFFFFFFF
psu_r5_tcm_ram_global                0xFFE00000       0xFFE3FFFF
psu_rcpu_gic                         0xF9000000       0xF900FFFF
psu_uart_0                           0xFF000000       0xFF00FFFF
```

PL slaves come first (they carry the slave interface name), then the PS ranges in alphabetical order. `psu_ddr_1` shows the 2 GB of upper DDR on this board, and `psu_ddr_0` the reserved megabyte.

Replace `psu_cortexa53_0` with `psu_cortexr5_0` and the same script shows the RPU's view (108 ranges). It differs in three ways: the TCMs appear at the R5's local addresses (`psu_r5_0_atcm` `0x0 – 0xFFFF`, `psu_r5_0_btcm` `0x20000 – 0x2FFFF`), the DDR starts at 1 MB (`psu_r5_ddr_0` `0x100000 – 0x7FEFFFFF`) because the R5's low addresses belong to the TCMs, and there is no upper DDR. HSI still lists the PL DDR4 at `0x48_0000_0000`, which a 32-bit R5 cannot address.

### From U-Boot

`bdinfo` prints the memory banks U-Boot took from the device tree:

```console
ZynqMP> bdinfo
boot_params = 0x0000000000000000
DRAM bank   = 0x0000000000000000
-> start    = 0x0000000000000000
-> size     = 0x000000007ff00000
DRAM bank   = 0x0000000000000001
-> start    = 0x0000000800000000
-> size     = 0x0000000080000000
...
relocaddr   = 0x000000007fc7a000
...
```

U-Boot relocates itself near the top of the lower bank (`relocaddr`), below the reserved megabyte. `md` reads registers directly; here the CSU `IDCODE` and `VERSION` registers and `CRL_APB.BOOT_MODE_USER`:

```console
ZynqMP> md.l 0xffca0040 2
ffca0040: 04600093 00003003                    ..`..0..
ZynqMP> md.l 0xff5e0200 1
ff5e0200: 00000000                             ....
```

`BOOT_MODE_USER` reads 0, the JTAG boot mode. That is the QEMU model's default: the reference setup loads the boot files directly instead of booting from a device ([chapter 06](../06-boot-sequence/README.md)).

### From Linux

`/proc/iomem` shows what the kernel knows: memory banks and every device with a `reg` property that a driver has claimed. Run it as root; for other users the addresses read as zero.

```console
target# cat /proc/iomem
00000000-7fefffff : System RAM
  00000000-00000013 : ZOCL_ERT_INTC_STATUS
  00210000-0155ffff : Kernel code
  01560000-0181ffff : reserved
  01820000-0199ffff : Kernel data
  38e00000-775fffff : reserved
...
a00f0000-a00fffff : a00f0000.v_frmbuf_rd v_frmbuf_rd@a00f0000
a0200000-a020ffff : a0200000.v_frmbuf_wr v_frmbuf_wr@a0200000
fd0b0000-fd0bffff : fd0b0000.perf-monitor perf-monitor@fd0b0000
fd0c0000-fd0c1fff : fd0c0000.ahci ahci@fd0c0000
...
ff000000-ff000fff : xuartps
ff010000-ff010fff : xuartps
...
800000000-87fffffff : System RAM
...
```

Things to notice:

- `System RAM` ends at `0x7FEF_FFFF` and continues at `0x8_0000_0000`, as in the device tree.
- The kernel was loaded at `0x0020_0000` (`booti 0x00200000 ...`); the `Kernel code` region starts 64 KB higher, at `0x0021_0000`.
- The large `reserved` region from `0x38E0_0000` is the 1000 MB CMA area requested with `cma=1000M` on the kernel command line (`cma: Reserved 1000 MiB at 0x0000000038e00000` in `dmesg`).
- The PL frame buffers appear only because `dfx-mgr` loaded the PL overlay at boot.

Individual registers can be read with BusyBox `devmem`:

```console
target# devmem 0xFFCA0040 32
0x04600093
```

The reference kernel has `CONFIG_DEVMEM=y` and does not set `CONFIG_STRICT_DEVMEM`, so `/dev/mem` gives access to every physical address, including RAM. That is convenient in the lab and a reason to change it in production ([chapter 27](../27-linux-and-network-security/README.md)).

### From XSDB

On hardware, XSDB reads physical addresses through the JTAG debug access port, independent of what the CPUs are doing:

```text
xsdb% connect
xsdb% targets -set -nocase -filter {name =~ "*PSU*"}
xsdb% mrd 0xFFCA0040 2
```

> [!NOTE]
> **Not run on the reference setup:** XSDB needs a JTAG connection through `hw_server`. XSDB can attach to QEMU's GDB stub (`gdbremote connect`), but that path only reads through the CPU's current virtual address map, so `mrd` of a physical register address fails with `Memory read error`.

## Reading and writing registers safely

| Risk | What happens | How to avoid it |
| --- | --- | --- |
| Block powered down, clock gated or held in reset | The access gets an error response or never completes; Linux reports an SError or the system hangs | Check the power domain and clock first ([section 07](07-clocks-power-and-reset.md)); let the driver enable the block |
| Secure-only register (Table 10-4 "Yes"), or a block the XPPU/XMPU protects | A non-secure access from Linux at EL1 is rejected | Access it from TF-A or the PMU firmware, or change the protection configuration ([section 06](06-interconnect-coherency-and-smmu.md)) |
| Register owned by firmware (PLLs, clock dividers, resets, MIO) | Writing it behind the owner's back desynchronizes the clock and reset frameworks in Linux and the PMU firmware | Use the Linux API (clock, reset, pinctrl frameworks), which goes through the PMU firmware |
| PL address | Hangs if the PL is not configured ([section 02](02-ps-and-pl.md)) | Check `/sys/class/fpga_manager/fpga0/state` first |
| Wrong access width | Some blocks only accept 32-bit accesses | Use 32-bit accesses (`devmem <addr> 32`, `md.l`) unless the register is documented otherwise |

## PetaLinux 2024.1 specifics

The memory layout is configured in `petalinux-config` → Subsystem Hardware Settings → Memory Settings. The ZCU106 project uses:

```text
CONFIG_SUBSYSTEM_MEMORY_PSU_DDR_0_BANKLESS_SELECT=y
CONFIG_SUBSYSTEM_MEMORY_PSU_DDR_0_BANKLESS_BASEADDR=0x0
CONFIG_SUBSYSTEM_MEMORY_PSU_DDR_0_BANKLESS_SIZE=0x80000000
CONFIG_SUBSYSTEM_MEMORY_PSU_DDR_0_BANKLESS_U__BOOT_TEXTBASE_OFFSET=0x8000000
CONFIG_SUBSYSTEM_MEMORY_IP_NAME="PSU_DDR_0"
```

The generated device tree (`components/plnx_workspace/device-tree/device-tree/system-top.dts`) still contains both banks with the reserved megabyte removed:

```dts
	memory@0 {
		device_type = "memory";
		reg = <0x0 0x0 0x0 0x7ff00000>, <0x00000008 0x00000000 0x0 0x80000000>;
	};
```

[Chapter 05](../05-petalinux/README.md) covers the Memory Settings menu, and [chapter 12](../12-device-tree/README.md) how the DTG builds the memory node.

## Pitfalls

- **Expecting DDR at `0x8000_0000`.** That address belongs to `M_AXI_HPM0_LPD`. DDR above 2 GB is at `0x8_0000_0000`.
- **Using the upstream device tree's memory node unchanged.** It includes the PMU firmware's reserved megabyte. Linux may then allocate it and break APU restart and other PMU firmware functions.
- **Mixing up the two GICs.** `0xF900_0000` is the RPU GIC; the APU GIC-400 distributor is at `0xF901_0000`.
- **Copying addresses from Zynq-7000 code.** The SLCR, peripheral and OCM addresses are all different on ZynqMP.
- **Reading `/proc/iomem` as a normal user** and believing every address is zero.

## References

- UG1085 Zynq UltraScale+ Device TRM (v2.5), Chapter 10, Tables 10-1 to 10-9; Chapter 6, Table 6-5
- UG1087 Zynq UltraScale+ Devices Register Reference (register bit fields)
- PG201 Zynq UltraScale+ MPSoC Processing System LogiCORE IP Product Guide (v3.5), "DDR Software Self-Refresh"
- `xilinx-zcu106-2024.1:project-spec/hw-description/system.xsa` (`psu_init.h`, address map via HSI), `project-spec/configs/config`, `components/plnx_workspace/device-tree/device-tree/system-top.dts`, `pre-built/linux/images/` (`boot.scr`, ELF headers)
- `linux-xlnx@xilinx-v2024.1:arch/arm64/boot/dts/xilinx/zynqmp-zcu106-revA.dts`
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/include/platform_def.h` (`BL31_BASE`, `BL32_BASE`, `PLAT_ARM_NS_IMAGE_BASE`)
- `device-tree-xlnx@xilinx_v2024.1:ddrps/data/ddrps.tcl` (memory node generation)
- Captured on the reference setup: U-Boot `bdinfo` and `md`, `/proc/iomem`, `devmem`, kernel configuration

---

<sub>← [Processing Units: APU, RPU, PMU, CSU, GPU and VCU](03-processing-units.md) · [Chapter index](README.md) · [On-Chip Memories: OCM, TCM and Friends](05-on-chip-memories.md) →</sub>
