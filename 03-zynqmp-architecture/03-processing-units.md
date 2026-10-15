# Processing Units: APU, RPU, PMU, CSU, GPU and VCU

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · ZCU106

**[03 · Zynq UltraScale+ MPSoC Architecture](README.md)** · Part II: Zynq UltraScale+ MPSoC Hardware

## In short

- A ZynqMP device contains six kinds of processing engines. Four are general-purpose processors you can program: the **APU** (Cortex-A53), the **RPU** (Cortex-R5F), the **PMU** (MicroBlaze) and, indirectly, the **CSU** (MicroBlaze, ROM code only). Two are fixed-function accelerators: the **GPU** (Mali-400 MP2) and the **VCU** (H.264/H.265, EV devices only).
- Linux runs on the APU. The RPU runs bare-metal or RTOS code, often through OpenAMP. The PMU runs AMD's PMU firmware, which Linux calls for power, clock and reset services. The CSU runs its BootROM and then serves crypto and PL configuration requests.
- The RPU comes out of reset in **lock-step** mode. Split mode, which gives two independent cores, must be selected before the RPU is released from reset.
- You can see each unit from Linux: `/proc/cpuinfo` and cpufreq for the APU, `remoteproc` for the RPU, the zynqmp-firmware interface for the PMU, the crypto drivers for the CSU, and kernel modules for the GPU and VCU.

## Concepts

### Overview

| Unit | Processor | Architecture | Maximum clock (DS891) | Power domain | Runs |
| --- | --- | --- | --- | --- | --- |
| APU | 2 or 4 × Cortex-A53 | Armv8-A, AArch64 and AArch32 | 1.5 GHz | FPD | FSBL (typically), TF-A, U-Boot, Linux |
| RPU | 2 × Cortex-R5F | Armv7-R | 600 MHz | LPD | Bare-metal, FreeRTOS, OpenAMP remote firmware; optionally the FSBL |
| PMU | Triple-redundant MicroBlaze | MicroBlaze | – | LPD | PMU ROM, then PMU firmware |
| CSU | Triple-redundant MicroBlaze | MicroBlaze | – | LPD | CSU BootROM only (not user programmable) |
| GPU | Mali-400 MP2 | – | 667 MHz | FPD | Graphics jobs from Linux (EG, EV) |
| VCU | Allegro video codec | – | – | PL | Encode and decode jobs from Linux (EV only) |

The maximum clocks depend on the speed grade; DS891 gives the upper end. The ZCU106 reference design runs the APU at 1199.88 MHz, the RPU and GPU at 499.95 MHz each (`PSU__CRF_APB__ACPU_CTRL__ACT_FREQMHZ`, `PSU__CRL_APB__CPU_R5_CTRL__ACT_FREQMHZ`, `PSU__CRF_APB__GPU_REF_CTRL__ACT_FREQMHZ` in the XSA).

### APU: Cortex-A53 MPCore

From UG1085 (v2.5), Chapter 3, and DS891:

- Four (EG, EV) or two (CG) Cortex-A53 cores, revision r0p4 (UG1085 Table 1-3). In-order, 8-stage, dual-issue pipeline.
- AArch64 and AArch32 execution states, with all four exception levels EL0–EL3 ([section 10](10-exception-levels-and-trustzone.md)).
- Advanced SIMD (NEON), floating point and the Armv8 cryptography extensions (AES, SHA-1, SHA-256).
- Per core: 32 KB L1 instruction cache (2-way, parity) and 32 KB L1 data cache (4-way, ECC). Shared: 1 MB L2 cache (16-way, ECC).
- A snoop control unit (SCU) keeps the L1 data caches coherent. An **ACE** master port connects the cluster to the CCI-400, and the **ACP** slave port lets the PL access the caches ([section 06](06-interconnect-coherency-and-smmu.md)).
- A two-stage MMU, so the APU supports hardware virtualization at EL2.
- Interrupts come from a GIC-400 ([section 08](08-interrupts-and-gic.md)). The Arm generic timer, L2 controller and SCU are accessed through system registers, not memory-mapped addresses (UG1085 Table 10-5, note).
- Each core is a separate power island; the PMU can switch off individual cores and the L2 RAM.

The A53 identifies itself in `/proc/cpuinfo` with implementer `0x41` (Arm), part `0xd03` (Cortex-A53), variant `0x0` and revision `4`: r0p4.

### RPU: Cortex-R5F pair

From UG1085 (v2.5), Chapter 4:

- Two Cortex-R5F cores implementing Armv7-R, with a VFPv3 single- and double-precision FPU and an MPU (memory protection unit, not an MMU).
- Per core: 32 KB instruction and 32 KB data L1 caches with ECC, and 128 KB of **tightly coupled memory** (TCM) with ECC, split into a 64 KB ATCM and a 64 KB BTCM (two interleaved 32 KB banks).
- A separate interrupt controller: an Arm PL390 GIC, mapped at `0xF900_0000`.
- Two operating modes, selected only while the RPU is held in reset:

| Mode | UG1085 name | What you get |
| --- | --- | --- |
| Lock-step | "Locked mode … Also known as safety mode" | One logical core. The second core runs the same instructions and the outputs are compared to detect random faults. R5_0 sees 256 KB of TCM (128 KB ATCM + 128 KB BTCM) |
| Split | "Split mode … Also known as performance mode" | Two independent cores, each with its own 128 KB of TCM |

The mode is controlled by `RPU_GLBL_CNTL` at `0xFF9A_0000`. UG1085 Chapter 4 lists the reset defaults: `SLSPLIT` "default (0)", `SLCLAMP` "default (1)", `TCM_COMB` "default (1)". The FSBL's `xfsbl_hw.h` defines the masks: `SLSPLIT` is bit 3 (`0x8`), `SLCLAMP` bit 4 (`0x10`) and `TCM_COMB` bit 6 (`0x40`). So the reset value is `0x50`: lock-step with combined TCMs.

The TCMs have two addresses: a local address at `0x0` seen by the R5 core itself, and a global address in the `0xFFE0_0000` region seen by every other master ([section 05](05-on-chip-memories.md)).

### PMU: platform management unit

From UG1085 (v2.5), Chapter 6:

- "The PMU processor is a triple-redundant processor without caches." It is a MicroBlaze with ECC-protected RAM (Table 6-2: 5-stage pipeline, little endian, fault tolerance enabled).
- It has a 32 KB ROM at `0xFFD0_0000` (inside a 256 KB address region) and 128 KB of RAM at `0xFFDC_0000` (UG1085 Tables 6-5 and 10-2). The ROM is visible only to the PMU; the RAM is reachable by other masters through the XPPU.
- It controls the power islands, isolation and resets of the whole PS, receives errors from all over the device, and wakes processors on events.

Two pieces of code run on it:

- **PMU ROM**, fixed in silicon. It runs first after power-on. Its pre-boot tasks, per UG1085 Chapter 6 "PMU ROM": clean the PMU RAM, enable the System Monitor and check the LPD supply, configure the PLLs with initial settings, trigger the scan and BIST clear of the PS, and release the CSU from reset. After boot it powers domains up and down and resets blocks on request.
- **PMU firmware** (PMUFW), loaded into the PMU RAM during boot. It implements AMD's Embedded Energy Management Interface (EEMI): the API through which TF-A, U-Boot and Linux request clocks, resets, power domains, pin configuration, FPGA loading and more. Without it, Linux on ZynqMP does not work as configured by PetaLinux.

[Chapter 09](../09-pmu-firmware/README.md) covers the PMU and its firmware in depth.

### CSU: configuration and security unit

From UG1085 (v2.5), Chapters 11 and 12, the CSU has two parts:

- The **secure processor block** (SPB): a triple-redundant MicroBlaze that is "not user accessible", 128 KB of ROM holding the BootROM (checked with SHA-3 before it runs), 32 KB of private RAM with ECC, and the physically unclonable function (PUF).
- The **crypto interface block** (CIB): AES-GCM-256, SHA-3/384, an RSA accelerator, the CSU DMA, the secure stream switch, key storage (BBRAM and eFUSE), and the processor configuration access port (PCAP) that loads bitstreams into the PL.

At boot, the CSU BootROM reads the boot header, loads the FSBL into the OCM and the PMU firmware into the PMU RAM, optionally after authenticating and decrypting them. After boot, software uses the CIB through the PMU firmware: the Linux `zynqmp-aes` and `zynqmp-rsa` drivers, and the FPGA manager for PCAP. The boot side is in [chapter 06](../06-boot-sequence/README.md), the security side in [chapter 26](../26-zynqmp-hardware-security-and-secure-boot/README.md).

### GPU: Mali-400 MP2

From DS891 and UG1085 (v2.5), Chapter 5: one geometry processor, two pixel processors (each its own power island in the FPD), a 64 KB L2 cache, OpenGL ES 1.1 and 2.0, OpenVG 1.1. The registers are at `0xFD4B_0000` and all GPU interrupts share GIC ID 164. The GPU renders into memory; displaying the result is the job of the DisplayPort controller or a display pipeline in the PL ([chapter 19](../19-graphics-and-display/README.md)).

### VCU: video codec unit

EV devices add a hard H.264/H.265 encoder and decoder that can encode and decode at the same time (DS891). DS891 lists it with the PL features: it is instantiated in the Vivado design, configured with the PL, and reached through the PL AXI ports. In the ZCU106 design, its registers sit in the `M_AXI_HPM0_FPD` window at `0xA010_0000`, and it reads and writes frames in DDR through HPC0 and HP1–HP3 ([section 02](02-ps-and-pl.md)). The Linux drivers are AMD's `al5e`/`al5d` (Allegro DVT) encoder and decoder drivers; GStreamer accesses them through OpenMAX IL ([chapter 20](../20-video-and-multimedia/README.md)).

### DisplayPort controller

Not a processor, but often grouped with the GPU: a DisplayPort 1.2a source (transmit only) with up to two lanes at up to 5.4 Gb/s over the PS-GTR transceivers, its own DMA engine (DPDMA), a blender for two video planes and an audio path. On the ZCU106 it uses GT lanes 1 and 0 (`PSU__DISPLAYPORT__LANE0__IO=GT Lane1`, `PSU__DISPLAYPORT__LANE1__IO=GT Lane0` in the XSA).

## On ZynqMP

### Who runs what on the reference system

| Unit | Code | Evidence on the reference setup |
| --- | --- | --- |
| PMU | PMU ROM, then PMU firmware 2024.1 | Boot log: `PMU Firmware 2024.1` (built May 19 2024). In QEMU the PMU ROM is replaced by the BSP's `pmu_rom_qemu_sha3.elf` |
| CSU | BootROM (on hardware) | QEMU's `petalinux-boot` flow loads the boot files directly and does not run the BootROM |
| APU | TF-A (EL3), U-Boot, then Linux 6.6 (EL2/EL1) | `U-Boot 2024.01`, `CPU: All CPU(s) started at EL2` |
| RPU | Nothing: held in reset in lock-step mode | `/sys/class/remoteproc` is empty because the BSP's `openamp.dtbo` is not applied by default |
| GPU | Mali kernel module `mali` (r9p0) and `libmali-xlnx` | `lsmod`, `/proc/interrupts` (`Mali_GP`, `Mali_PP0`, `Mali_PP1` on ID 164) |
| VCU | `al5e`/`al5d` drivers, `kernel-module-vcu`, `libvcu-xlnx` | Packages in `rootfs.manifest`. QEMU does not model the VCU |

## Hands-on

### APU

```console
target$ grep -m4 -E "CPU implementer|CPU part|CPU variant|CPU revision" /proc/cpuinfo
CPU implementer	: 0x41
CPU variant	: 0x0
CPU part	: 0xd03
CPU revision	: 4
target$ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
299999 399999 599999 1199999 
target$ cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver
cpufreq-dt
```

The frequency list comes from the `opp-table-cpu` node that the device tree generator derives from the APU clock in the XSA: 1.2 GHz divided by 1, 2, 3 and 4. `cpufreq-dt` changes the rate by asking the PMU firmware to change the `ACPU` clock divider ([section 07](07-clocks-power-and-reset.md)).

### RPU mode

```console
target# devmem 0xFF9A0000 32
0x00000050
```

`0x50` sets `SLCLAMP` (bit 4) and `TCM_COMB` (bit 6) and clears `SLSPLIT` (bit 3): lock-step, the reset default. On hardware, the value changes when the FSBL loads an RPU application in split mode, or when Linux `remoteproc` configures the RPU ([chapter 21](../21-rpu-and-openamp/README.md)).

### PMU firmware

```console
target# echo pm_get_api_version > /sys/kernel/debug/zynqmp-firmware/pm
target# cat /sys/kernel/debug/zynqmp-firmware/pm
PM-API Version = 1.1
```

The kernel logs the same version at boot (`zynqmp_firmware_probe Platform Management API v1.1`). The firmware itself prints its banner on the PMU's UART during boot (`PMU Firmware 2024.1`).

### GPU

```console
target$ lsmod | grep -i mali
mali                  225280  0
```

The Mali kernel driver is an out-of-tree module, packaged as `kernel-module-mali` (version `r9p0+01rel0` in `rootfs.manifest`), built only when the machine has the `mali400` feature ([section 01](01-device-family-overview.md#petalinux-20241-specifics)).

## PetaLinux 2024.1 specifics

Every unit has a matching software component, and most of them are in the boot image:

| Unit | Component | Where it comes from in PetaLinux |
| --- | --- | --- |
| APU | FSBL (`zynqmp_fsbl.elf`), TF-A (`bl31.elf`), U-Boot, kernel | `BOOT.BIN`, `Image` ([chapter 07](../07-boot-images-and-bootgen/README.md)) |
| PMU | `pmufw.elf` | `BOOT.BIN`, loaded by the CSU BootROM |
| RPU | OpenAMP firmware (`openamp-fw-echo-testd`, `openamp-fw-mat-muld`, `openamp-fw-rpc-demo` in this BSP) | Root filesystem, loaded by `remoteproc` |
| GPU | `kernel-module-mali`, `libmali-xlnx` | `MACHINE_FEATURES` `mali400` |
| VCU | `kernel-module-vcu`, `libvcu-xlnx`, `libomxil-xlnx`, `gstreamer1.0-omx` | `MACHINE_FEATURES` `vcu` |

## Pitfalls

- **Expecting two RPU cores by default.** Out of reset, the RPU is in lock-step mode. Code built for R5_1 never runs unless something switches to split mode first.
- **Treating the PMU firmware as optional.** UG1085 Chapter 11: "The PMU FW must be present in most systems for the AMD-based FSBL and system software." Linux clock, reset, power and pin control all go through it.
- **Assuming the GPU is a display controller.** The Mali GPU only renders. Output needs the DisplayPort controller or a PL display pipeline, plus a driver for it.
- **Looking for the VCU in the PS address map.** It lives behind the PL ports, at whatever address the Vivado design gives it, and only works after the PL is configured.

## References

- DS891 Zynq UltraScale+ MPSoC Data Sheet: Overview (v1.11.1), feature lists and Tables 1, 3, 5, 7
- UG1085 Zynq UltraScale+ Device TRM (v2.5): Chapter 1 (Table 1-3), Chapter 3 ("Cortex-A53 MPCore Processor Features"), Chapter 4 ("Real-time Processing Unit Features", "RPU CPU Configuration", "Tightly Coupled Memory Functional Description"), Chapter 5, Chapter 6 ("PMU Processor", "PMU ROM", Tables 6-2 and 6-5), Chapter 10 (Tables 10-2, 10-5), Chapter 11 ("Introduction"), Chapter 12 ("Configuration Security Unit (CSU) Introduction")
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_hw.h` (`RPU_RPU_GLBL_CNTL_*_MASK`)
- `xilinx-zcu106-2024.1:project-spec/hw-description/system.xsa`, `pre-built/linux/images/rootfs.manifest`, `pre-built/linux/images/system.dtb` (`opp-table-cpu`)
- Captured on the reference setup: `/proc/cpuinfo`, cpufreq, `devmem`, zynqmp-firmware debugfs, `lsmod`, timestamped boot log

---

<sub>← [Processing System (PS) and Programmable Logic (PL)](02-ps-and-pl.md) · [Chapter index](README.md) · [System Address Map](04-memory-map.md) →</sub>
