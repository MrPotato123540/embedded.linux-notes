# Interrupts and the GIC

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · ZCU106

**[03 · Zynq UltraScale+ MPSoC Architecture](README.md)** · Part II: Zynq UltraScale+ MPSoC Hardware

## In short

- The APU has an Arm **GIC-400** (GICv2) at `0xF901_0000`; the RPU has its own Arm **PL390** GIC at `0xF900_0000`. Both receive the same set of system interrupts.
- GIC interrupt IDs: **SGIs** 0–15 (software-generated, used by Linux for inter-CPU messages), **PPIs** 16–31 (per-CPU, for example the timers), **SPIs** 32 and up (shared peripherals). ZynqMP's peripheral interrupts are IDs 40 to 187.
- UG1085 lists GIC IDs; the device tree lists SPI numbers. **ID = SPI + 32**: UART0 is ID 53 and `<GIC_SPI 21 IRQ_TYPE_LEVEL_HIGH>` in the device tree.
- The PL can raise 16 interrupts: `pl_ps_irq0[7:0]` = IDs 121–128 and `pl_ps_irq1[7:0]` = IDs 136–143.
- Processors signal each other through the **IPI** block (`0xFF30_0000`). It is unrelated to the `IPI0`–`IPI6` lines in `/proc/interrupts`, which are Linux's SGI-based inter-CPU interrupts.

## Concepts

### Two interrupt controllers

| Controller | Arm IP (UG1085 Table 1-3) | Address | Serves |
| --- | --- | --- | --- |
| APU GIC | GIC-400 r0p1 | Distributor `0xF901_0000`, CPU interface `0xF902_0000`, virtual interface control `0xF904_0000`, virtual CPU interface `0xF906_0000` | Four Cortex-A53 cores |
| RPU GIC | PL390 r0p0 | `0xF900_0000` | Two Cortex-R5F cores |

The APU addresses are the four `reg` ranges of the `gic` node in `zynqmp.dtsi`. UG1085 Table 13-1 states that the system interrupts are broadcast "to the GICs, the PMU via the GIC proxy (GICPx_IRQ registers), and to output signals in the PL". The GIC proxy lets the PMU see interrupts while the processors are asleep, so they can be woken.

The GIC-400 supports the GICv2 virtualization extensions, which is what the two upper `reg` ranges are for: a hypervisor at EL2 (Xen, KVM) uses them to inject virtual interrupts into guests.

### Interrupt types and numbering

| Type | ID range | Scope | Examples on ZynqMP |
| --- | --- | --- | --- |
| SGI | 0–15 | Raised by software on one core for another | Linux rescheduling and function-call IPIs |
| PPI | 16–31 | Private to each core | Generic timer: ID 30 (non-secure physical), 27 (virtual), 26 (hypervisor), 29 (secure physical); GIC maintenance ID 25 |
| SPI | 32–187 used | Shared, routed to any core | All peripherals, PL interrupts, IPI channels |

The device tree `interrupts` property for the GIC has three cells:

```text
<type number flags>
type   : GIC_SPI (0) or GIC_PPI (1)
number : SPI number (ID − 32) or PPI number (ID − 16)
flags  : trigger type (IRQ_TYPE_LEVEL_HIGH = 4, IRQ_TYPE_EDGE_RISING = 1, ...),
         for PPIs also a CPU mask in bits [15:8]
```

From `zynqmp.dtsi`, the timer uses PPIs 13, 14, 11 and 10 (IDs 29, 30, 27, 26):

```dts
	timer {
		compatible = "arm,armv8-timer";
		interrupt-parent = <&gic>;
		interrupts = <GIC_PPI 13 (GIC_CPU_MASK_SIMPLE(4) | IRQ_TYPE_LEVEL_LOW)>,
			     <GIC_PPI 14 (GIC_CPU_MASK_SIMPLE(4) | IRQ_TYPE_LEVEL_LOW)>,
			     <GIC_PPI 11 (GIC_CPU_MASK_SIMPLE(4) | IRQ_TYPE_LEVEL_LOW)>,
			     <GIC_PPI 10 (GIC_CPU_MASK_SIMPLE(4) | IRQ_TYPE_LEVEL_LOW)>;
	};
```

### The ZynqMP system interrupts

UG1085 (v2.5), Table 13-1 "System Interrupts" lists every SPI. A selection, with the device tree SPI number added:

| Source | GIC ID | SPI | Notes |
| --- | --- | --- | --- |
| OCM ECC | 42 | 10 | |
| QSPI | 47 | 15 | |
| GPIO | 48 | 16 | |
| I2C0, I2C1 | 49, 50 | 17, 18 | |
| SPI0, SPI1 | 51, 52 | 19, 20 | |
| UART0, UART1 | 53, 54 | 21, 22 | |
| CAN0, CAN1 | 55, 56 | 23, 24 | |
| RTC alarm, RTC seconds | 58, 59 | 26, 27 | |
| IPI channel 0 (APU) | 67 | 35 | Channels 1, 2 (RPU0/1): 65, 66; 7–10: 61–64 |
| TTC0–TTC3 | 68–79 | 36–47 | Three per timer |
| SD0, SD1 | 80, 81 | 48, 49 | |
| LPD watchdog | 84 | 52 | Edge-triggered |
| GEM0–GEM3 | 89, 91, 93, 95 | 57, 59, 61, 63 | Wake-up interrupts on the odd IDs in between |
| USB0 | 97–101 | 65–69 | |
| LPD DMA channels 0–7 | 109–116 | 77–84 | |
| CSU, CSU DMA | 117, 118 | 85, 86 | |
| **PL to PS group 0** | **121–128** | **89–96** | `pl_ps_irq0[7:0]`, rising edge or high level |
| **PL to PS group 1** | **136–143** | **104–111** | `pl_ps_irq1[7:0]`, rising edge or high level |
| DDR controller | 144 | 112 | |
| FPD watchdog | 145 | 113 | Edge-triggered |
| PCIe MSI, INTx, DMA | 146–150 | 114–118 | |
| DisplayPort, DPDMA | 151, 154 | 119, 122 | |
| FPD DMA channels 0–7 | 156–163 | 124–131 | |
| GPU | 164 | 132 | "OR of all GPU interrupts" |
| SATA | 165 | 133 | |
| APU performance monitors | 175–178 | 143–146 | One per core |
| CCI, SMMU | 186, 187 | 154, 155 | |

IDs 129–135 are reserved. UG1085 notes that the system watchdogs "produce an interrupt pulse" and "the GIC interrupt controllers must be programmed for edge sensitivity", and that a PL interrupt pulse must last at least four GIC clock cycles, about 40 ns at 100 MHz.

### PL interrupts

The 16 PL interrupt inputs are often not enough. The usual solution, used in the ZCU106 design, is to connect a few important sources directly and put an AXI interrupt controller (AXI INTC) in the PL for the rest. From the ZCU106 XSA ([section 02](02-ps-and-pl.md)):

| PL source | PS input | GIC ID | Device tree |
| --- | --- | --- | --- |
| VCU | `pl_ps_irq0[0]` | 121 | `<0x00 0x59 0x04>` (SPI 89) |
| Frame buffer read | `pl_ps_irq0[1]` | 122 | `<0x00 0x5a 0x04>` (SPI 90) |
| Frame buffer write | `pl_ps_irq0[2]` | 123 | `<0x00 0x5b 0x04>` (SPI 91) |
| AXI INTC (32 inputs) | `pl_ps_irq1[0]` | 136 | `<0x00 0x68 0x04>` (SPI 104) |

The AXI INTC is itself an interrupt controller in the device tree (`interrupt-controller`, `#interrupt-cells = <0x02>`). Linux chains it behind SPI 104, and the devices behind it use it as their `interrupt-parent` with its own numbering.

### Inter-processor interrupts (IPI)

The IPI block lets any processor interrupt any other and pass a short message. From UG1085 (v2.5), Table 13-3:

| Channel | Default owner | Registers | Message buffer |
| --- | --- | --- | --- |
| 0 | APU | `0xFF30_0000` | `0xFF99_0400` |
| 1 | RPU0 | `0xFF31_0000` | `0xFF99_0000` |
| 2 | RPU1 | `0xFF32_0000` | `0xFF99_0200` |
| 3–6 | PMU (hard-wired) | `0xFF33_0000` – `0xFF33_3000` | `0xFF99_0E00` |
| 7–10 | PL 0–3 | `0xFF34_0000` – `0xFF37_0000` | `0xFF99_0600` – `0xFF99_0C00` |

"The software might reassign the interrupt channels and message buffers except for the PMU interrupts." The ZCU106 design does: it assigns channels 7 and 8 to the APU (`PSU__GEN_IPI_7__MASTER=APU`, `PSU__GEN_IPI_8__MASTER=APU`).

IPIs carry two kinds of traffic on a running system:

- **EEMI calls to the PMU firmware.** TF-A forwards each Linux firmware call from channel 0 (APU) to channel 3 (PMU_0), with the message in the buffers at `0xFF99_0400` and `0xFF99_0E00`: `IPI_LOCAL_ID` is `IPI_ID_APU` and `IPI_REMOTE_ID` is `IPI_ID_PMU0` in TF-A's `plat/xilinx/zynqmp/include/plat_ipi.h` ([section 07](07-clocks-power-and-reset.md)).
- **OpenAMP.** The `zynqmp-ipi-mailbox` driver gives `remoteproc` and RPMsg a mailbox to the RPU ([chapter 21](../21-rpu-and-openamp/README.md)).

## On ZynqMP

### What the reference image shows

```console
target$ cat /proc/interrupts
           CPU0       CPU1       CPU2       CPU3       
 11:       8246      12322       8514       9824     GICv2  30 Level     arch_timer
 14:          0          0          0          0     GICv2  67 Level     zynqmp-ipi
 15:          0          0          0          0     GICv2  58 Level     ffa60000.rtc
 16:          0          0          0          0     GICv2  59 Level     ffa60000.rtc
...
 22:        229          0          0          0     GICv2  53 Level     xuartps
...
 44:        175          0          0          0     GICv2  95 Level     eth0, eth0
...
 49:          0          0          0          0     GICv2  84 Edge      ff150000.watchdog
...
 55:          0          0          0          0     GICv2 164 Level     Mali_GP_MMU, Mali_GP, Mali_PP0_MMU, Mali_PP0, Mali_PP1_MMU, Mali_PP1
 57:          0          0          0          0     GICv2 122 Level     xilinx_framebuffer
 58:          0          0          0          0     GICv2 123 Level     xilinx_framebuffer
IPI0:       202        186        149        148       Rescheduling interrupts
IPI1:      3182       3818       3856       4681       Function call interrupts
...
```

How to read a line:

- The first column (`22`) is the Linux virtual IRQ number. It is assigned at boot and has no meaning outside Linux.
- `GICv2 53` is the controller and the hardware interrupt ID, the number in UG1085 Table 13-1. UART0 is 53 = SPI 21.
- `Level`/`Edge` is the trigger type from the device tree. The LPD watchdog at 84 is `Edge`, as UG1085 requires.
- The timer is PPI 14 = ID 30, the non-secure physical timer: Linux runs in the non-secure world.
- `zynqmp-ipi` on ID 67 is the APU's IPI channel 0. `IPI0`–`IPI6` at the bottom are Linux's own SGIs between the four cores.

The kernel log shows a ZynqMP-specific detail of the GIC-400 integration:

```text
[    0.000000] GIC: Adjusting CPU interface base to 0x00000000f902f000
[    0.000000] Root IRQ handler: gic_handle_irq
[    0.000000] GIC: Using split EOI/Deactivate mode
```

The device tree gives the CPU interface a 128 KB window at `0xF902_0000`. The GIC driver detects that the first 4 KB page is aliased over 64 KB and, in its own words, moves "the base up by 60kB, so that we have a 8kB contiguous region, which allows us to use GICC_DIR at its normal offset" (`drivers/irqchip/irq-gic.c`). That enables the split EOI/deactivate mode, which the driver uses when the kernel was started at EL2, as here, so that KVM can hand interrupts to guests.

## Hands-on

### Move an interrupt to another CPU

A GICv2 delivers each SPI to one CPU. The affinity mask allows several, but the effective target is one of them:

```console
target# grep eth0 /proc/interrupts
 44:        895          9          0          0     GICv2  95 Level     eth0, eth0
target# cat /proc/irq/44/smp_affinity_list /proc/irq/44/effective_affinity_list
0-3
0
target# echo 1 > /proc/irq/44/smp_affinity_list
target# ping -c 5 -q 10.0.2.2 > /dev/null
target# grep eth0 /proc/interrupts
 44:        898         15          0          0     GICv2  95 Level     eth0, eth0
target# echo 0-3 > /proc/irq/44/smp_affinity_list
```

After the change, the Ethernet interrupts arrive on CPU1. Moving busy interrupts away from a core that runs a latency-sensitive task is a common tuning step; `irqbalance` automates it on larger systems. The Linux IRQ number (44 here) can differ between boots, so look it up first.

### Find the interrupt of a PL device

Take the GIC ID from the Vivado design (the bit of `pl_ps_irq0/1` it is wired to), convert it to an SPI number and compare with the device tree:

```text
pl_ps_irq0[2]  →  ID 121 + 2 = 123  →  SPI 123 − 32 = 91 = 0x5b  →  interrupts = <0x00 0x5b 0x04>
```

That is the frame buffer write IP in the ZCU106 overlay, and `GICv2 123` in `/proc/interrupts`.

## PetaLinux 2024.1 specifics

- The device tree generator computes PL `interrupts` properties from the XSA, including the offset of each `pl_ps_irq` input. When you add PL IP by hand in `system-user.dtsi` or an overlay, you have to do the arithmetic above yourself.
- The `interrupts` encoding in decompiled `.dtb`/`.dtbo` files is numeric: `<0x00 0x5b 0x04>` means `<GIC_SPI 91 IRQ_TYPE_LEVEL_HIGH>`.

## Pitfalls

- **Writing the GIC ID into the device tree.** `<GIC_SPI 121 ...>` points at ID 153 (FPD ATB error), not at `pl_ps_irq0[0]`.
- **Edge interrupts declared as level, or the reverse.** A PL signal that pulses for a few cycles must be declared edge-triggered; a level interrupt from IP that holds the line until serviced must be declared level. Check the IP's documentation.
- **PL interrupt pulses shorter than four GIC clocks.** They can be missed.
- **Confusing Linux IPIs with ZynqMP IPIs.** The `IPI` rows in `/proc/interrupts` are SGIs; the IPI hardware block appears as `zynqmp-ipi` on ID 67.
- **Using the APU GIC address in RPU code** (or the reverse). The R5 must program its PL390 at `0xF900_0000`.

## References

- UG1085 Zynq UltraScale+ Device TRM (v2.5), Chapter 13 ("GIC Proxy Interrupts", Table 13-1 "System Interrupts", Table 13-3 "IPI Channel and Message Buffer Default Associations"), Table 1-3
- Arm CoreLink GIC-400 Generic Interrupt Controller Technical Reference Manual; Arm Generic Interrupt Controller Architecture Specification (GICv2)
- `linux-xlnx@xilinx-v2024.1:arch/arm64/boot/dts/xilinx/zynqmp.dtsi` (`gic`, `timer`, `zynqmp_ipi`), `drivers/irqchip/irq-gic.c`
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/include/plat_ipi.h`, `plat/xilinx/zynqmp/zynqmp_ipi.c`
- `xilinx-zcu106-2024.1:project-spec/hw-description/system.xsa` (`PSU__GEN_IPI_*`, PL interrupt wiring), `zcu106-2.0.dtbo`
- Captured on the reference setup: `/proc/interrupts`, `/proc/irq/*/`, `dmesg`

---

<sub>← [Clocks, Power Domains and Reset](07-clocks-power-and-reset.md) · [Chapter index](README.md) · [Peripherals, MIO and EMIO](09-peripherals-mio-emio.md) →</sub>
