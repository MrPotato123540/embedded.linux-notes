# Peripherals, MIO and EMIO

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · ZCU106

**[03 · Zynq UltraScale+ MPSoC Architecture](README.md)** · Part II: Zynq UltraScale+ MPSoC Hardware

## In short

- The PS peripherals reach the outside world through **78 MIO pins** in three banks of 26, or through **EMIO** signals into the PL, from where they can use PL pins or PL logic.
- Each MIO pin has a four-level multiplexer, controlled by `IOU_SLCR.MIO_PIN_n` at `0xFF18_0000 + 4·n`. The Vivado PS configuration chooses the routing; `psu_init` in the FSBL programs it.
- On PetaLinux, Linux can program the pins again: device tree `pinctrl` nodes, applied through the PMU firmware. The FSBL's settings and the device tree must therefore agree.
- The four **PS-GTR** lanes are shared by PCIe Gen2, SATA, USB 3.0, DisplayPort and SGMII. The lane assignment is fixed in the hardware design and appears in the device tree as `phys` properties.
- Every PS peripheral has an upstream Linux driver. The table in this section maps controller, compatible string and driver.

## Concepts

### MIO banks

From UG1085 (v2.5), Chapter 28: "The 78 MIO signals are divided into three banks, and each bank includes 26 device pins. Each bank (500, 501, and 502) has its own power pins, VCCO_PSIO{0:2}". The voltage, 1.8 V or 3.3 V, is set by the board. A fourth PS bank, 503 (`VCCO_PSIO3`), carries the boot mode, configuration, PS JTAG, error, reset and POR pins (UG1085 Chapter 2).

| Bank | MIO pins | GPIO bank in Linux | ZCU106 I/O standard (XSA) |
| --- | --- | --- | --- |
| 500 | 0–25 | Bank 0, lines 0–25 | `PSU_BANK_0_IO_STANDARD=LVCMOS18` |
| 501 | 26–51 | Bank 1, lines 26–51 | `PSU_BANK_1_IO_STANDARD=LVCMOS18` |
| 502 | 52–77 | Bank 2, lines 52–77 | `PSU_BANK_2_IO_STANDARD=LVCMOS18` |
| 503 | Dedicated pins | – | `PSU_BANK_3_IO_STANDARD=LVCMOS33` |

The boot device pins are fixed (UG1085 Table 11-1): QSPI on MIO 0–12, for example. That constrains everything else, because the BootROM uses those pins before any software runs.

### The MIO multiplexer

Each pin's register has four select fields. From the generated `psu_init.c`, for MIO 18:

```c
    * Register : MIO_PIN_18 @ 0XFF180048

    * Level 0 Mux Select 0= Level 1 Mux Output 1= Not Used
    *  PSU_IOU_SLCR_MIO_PIN_18_L0_SEL                              0
...
    * Level 3 Mux Select 0= gpio0, Input, gpio_0_pin_in[18]- (GPIO bank 0) 0=
    * gpio0, Output, gpio_0_pin_out[18]- (GPIO bank 0) 1= can0, Input, can0_ph
    * y_rx- (Can RX signal) 2= i2c0, Input, i2c0_scl_input- (SCL signal) 2= i2
    * c0, Output, i2c0_scl_out- (SCL signal) 3= swdt0, Input, swdt0_clk_in- (W
    * atch Dog Timer Input clock) 4= spi1, Input, spi1_mi- (MISO signal) 4= sp
    * i1, Output, spi1_so- (MISO signal) 5= ttc2, Input, ttc2_clk_in- (TTC Clo
    * ck) 6= ua0, Input, ua0_rxd- (UART receiver serial input) 7= Not Used
    *  PSU_IOU_SLCR_MIO_PIN_18_L3_SEL                              6

    * Configures MIO Pin 18 peripheral interface mapping
    * (OFFSET, MASK, VALUE)      (0XFF180048, 0x000000FEU ,0x000000C0U)
```

The mask `0xFE` covers `L0_SEL` (bit 1), `L1_SEL` (bit 2), `L2_SEL` (bits [4:3]) and `L3_SEL` (bits [7:5]). Level 0 carries the fastest interfaces and level 3 the slow ones. In the ZCU106 `psu_init.c`, QSPI on MIO 0 and GEM3 on MIO 64 use level 0 (`0x02`), USB0 ULPI on MIO 52 level 1 (`0x04`), SD1 on MIO 39 level 2 (`0x10`), and UART0 on MIO 18 level 3 (`0xC0`); the MIO 18 description above also lists NAND on level 1 and SD0 on level 2. UG1085 explains the order: "a priority structure based on maximum toggle rates must be implemented to place high-speed signal interfaces (such as gigabit Ethernet RGMII or USB ULPI) closer to the pin". Value `0xC0` selects level 3, option 6: UART0 RXD.

Other registers in `IOU_SLCR` set the electrical properties per pin, such as drive strength, Schmitt trigger, pull-up/down and slew rate: `BANKn_CTRL0`, `CTRL1` and `CTRL3` to `CTRL6` for each bank (all written by `psu_init.c`; `BANK0_CTRL4` is at `0xFF180144`). UG1085 Table 28-2 lists, for each MIO pin, which signal of which peripheral it can carry; low-speed controllers such as CAN, I2C and UART can be placed on almost any pin pair.

### EMIO

EMIO connects PS peripheral signals to the PL instead of to MIO pins. It is used to:

- reach more pins, using PL I/O banks,
- connect a PS controller to PL logic (for example GEM in GMII mode to a PL PHY interface, or a UART to a PL-side protocol bridge),
- get GPIOs between PS software and PL logic: up to 96 EMIO GPIOs in GPIO banks 3–5 ([section 02](02-ps-and-pl.md)).

Each controller chapter in UG1085 lists which of its signals have an EMIO path (for example the `emio_sdio0_*` signals in the SD chapter). EMIO pins only work once the PL is configured.

### Who programs the MIO

UG1085 (v2.5), Chapter 28: "Some MIO pins are programmed by the PMU ROM pre-boot. Some might also be programmed by the PMU user firmware, the CSU for the boot device, the FSBL, or other low-level code." On a PetaLinux system, the full list is:

1. The **CSU BootROM** configures the boot device pins.
2. The **FSBL** runs `psu_mio_init_data()` from `psu_init.c`, programming every pin the Vivado design uses.
3. **Linux** applies the `pinctrl` settings from the device tree, through the PMU firmware's pin-control API.

Step 3 is optional and depends on the device tree. The ZCU106 BSP has it: the machine configuration selects the board file with `YAML_DT_BOARD_FLAGS ?= "{BOARD zcu106-reva}"`, and the generated `zcu106-reva.dtsi` contains pin groups such as:

```dts
	pinctrl_uart0_default: uart0-default {
		mux {
			groups = "uart0_4_grp";
			function = "uart0";
		};

		conf {
			groups = "uart0_4_grp";
			slew-rate = <SLEW_RATE_SLOW>;
			power-source = <IO_STANDARD_LVCMOS18>;
		};
```

and binds them to the devices:

```dts
&uart0 {
	pinctrl-names = "default";
	pinctrl-0 = <&pinctrl_uart0_default>;
};
```

A custom board without a board file has no `pinctrl` nodes. Linux then leaves the MIO as the FSBL configured it.

### Peripheral catalogue

The PS peripherals, their counts (DS891), compatible strings (`zynqmp.dtsi`) and the Linux drivers bound on the reference image (`/sys/bus/platform/devices/*/driver`):

| Controller | Count | Compatible | Linux driver |
| --- | --- | --- | --- |
| UART | 2 | `xlnx,zynqmp-uart`, `cdns,uart-r1p12` | `xuartps` |
| I2C | 2 | `cdns,i2c-r1p14` | `cdns-i2c` |
| SPI | 2 | `cdns,spi-r1p6` | `cdns-spi` |
| CAN | 2 | `xlnx,zynq-can-1.0` | `xilinx_can` |
| GPIO | 1 (78 MIO + 96 EMIO lines) | `xlnx,zynqmp-gpio-1.0` | `zynq-gpio` |
| Quad-SPI | 1 (single or dual flash) | `xlnx,zynqmp-qspi-1.0` | `zynqmp-qspi` |
| NAND (ONFI 3.1) | 1 | `xlnx,zynqmp-nand-controller`, `arasan,nfc-v3p10` | Arasan NAND driver |
| SD/SDIO/eMMC | 2 | `xlnx,zynqmp-8.9a`, `arasan,sdhci-8.9a` | `sdhci-arasan` |
| Gigabit Ethernet (GEM) | 4 | `xlnx,zynqmp-gem`, `cdns,gem` | `macb` |
| USB 3.0/2.0 | 2 | `xlnx,zynqmp-dwc3` with a `snps,dwc3` child | `dwc3-xilinx`, `dwc3` |
| SATA | 1 (2 ports) | `ceva,ahci-1v84` | `ahci-ceva` |
| PCIe Gen2 | 1 (x1, x2, x4) | `xlnx,nwl-pcie-2.11` | NWL PCIe host driver |
| DisplayPort | 1 (2 TX lanes) | `xlnx,zynqmp-dpsub-1.7` | `zynqmp-display` |
| PS-GTR | 4 lanes | `xlnx,zynqmp-psgtr-v1.1` | `xilinx-psgtr` |
| LPD and FPD DMA | 2 × 8 channels | `xlnx,zynqmp-dma-1.0` | `xilinx-zynqmp-dma` |
| Watchdog | 3 (LPD, FPD, CSU) | `cdns,wdt-r1p2` | `cdns-wdt` |
| Triple-timer counter | 4 | `cdns,ttc` | Timer driver, registers `ttc_clocksource` and `ttc_clockevent` |
| RTC | 1 | `xlnx,zynqmp-rtc` | `rtc_zynqmp` |
| System monitor (AMS) | 1 | `xlnx,zynqmp-ams` | `xilinx-ams` (IIO) |

As the compatible strings show, much of the peripheral IP comes from IP vendors: Cadence (`cdns`: UART, I2C, SPI, GEM, TTC, watchdog), Arasan (SD, NAND), Synopsys (`snps`: USB), CEVA (SATA) and Northwest Logic (`nwl`: PCIe). The same Linux drivers therefore serve other SoCs with the same IP.

### PS-GTR transceivers

The four PS-GTR lanes are shared. From UG1085 (v2.5), Table 29-1 "Interconnect Matrix":

| Controller | Lane 0 | Lane 1 | Lane 2 | Lane 3 |
| --- | --- | --- | --- | --- |
| PCIe | PCIe.0 | PCIe.1 | PCIe.2 | PCIe.3 |
| SATA | SATA.0 | SATA.1 | SATA.0 | SATA.1 |
| USB0 3.0 | USB0 | USB0 | USB0 | – |
| USB1 3.0 | – | – | – | USB1 |
| DisplayPort | DP.1 | DP.0 | DP.1 | DP.0 |
| GEM0–GEM3 (SGMII) | GEM0 | GEM1 | GEM2 | GEM3 |

One lane carries one protocol. The ZCU106 design uses all four (`PSU__*__IO` parameters in the XSA): DisplayPort on lanes 1 and 0, USB0 on lane 2, SATA port 1 on lane 3. PCIe and SGMII are therefore not available on the PS side of this board without a different design. The reference clock for each lane comes from one of the four `PS_MGTREFCLK` inputs, and "should be stable before releasing the PS_POR_B, just like PS_REF_CLK" (UG1085 Chapter 29).

## On ZynqMP

### Lane assignment in the device tree

The device tree describes each controller's lane in its `phys` property. From `zynqmp-zcu106-revA.dts` in `linux-xlnx`:

```dts
	phys = <&psgtr 3 PHY_TYPE_SATA 1 1>;
...
	phys = <&psgtr 2 PHY_TYPE_USB3 0 2>;
...
	phys = <&psgtr 1 PHY_TYPE_DP 0 3>,
	       <&psgtr 0 PHY_TYPE_DP 1 3>;
```

The four cells are, per the binding `xlnx,zynqmp-psgtr.yaml`: the GTR lane, the PHY type, the PHY instance (which controller port) and the reference clock number. The decompiled prebuilt `system.dtb` has the same values in numeric form, for example `phys = <0x23 0x03 0x01 0x01 0x01>` for SATA (`PHY_TYPE_SATA` = 1).

### The pins Linux claims

The pinctrl debugfs shows which MIO pins are claimed by which driver. Excerpt from the reference setup:

```console
target# cat /sys/kernel/debug/pinctrl/firmware:zynqmp-firmware:pinctrl-zynqmp_pinctrl/pinmux-pins
Pinmux settings per pin
Format: pin (name): mux_owner gpio_owner hog?
pin 0 (MIO0): (MUX UNCLAIMED) (GPIO UNCLAIMED)
...
pin 13 (MIO13): ff0a0000.gpio (GPIO UNCLAIMED) function gpio0 group gpio0_13_grp
pin 14 (MIO14): ff020000.i2c (GPIO UNCLAIMED) function i2c0 group i2c0_3_grp
pin 15 (MIO15): ff020000.i2c (GPIO UNCLAIMED) function i2c0 group i2c0_3_grp
pin 16 (MIO16): ff030000.i2c (GPIO UNCLAIMED) function i2c1 group i2c1_4_grp
pin 17 (MIO17): ff030000.i2c (GPIO UNCLAIMED) function i2c1 group i2c1_4_grp
pin 18 (MIO18): ff000000.serial (GPIO UNCLAIMED) function uart0 group uart0_4_grp
pin 19 (MIO19): ff000000.serial (GPIO UNCLAIMED) function uart0 group uart0_4_grp
pin 20 (MIO20): ff010000.serial (GPIO UNCLAIMED) function uart1 group uart1_5_grp
pin 21 (MIO21): ff010000.serial (GPIO UNCLAIMED) function uart1 group uart1_5_grp
...
pin 64 (MIO64): ff0e0000.ethernet (GPIO UNCLAIMED) function ethernet3 group ethernet3_0_grp
...
pin 76 (MIO76): ff0e0000.ethernet (GPIO UNCLAIMED) function mdio3 group mdio3_0_grp
pin 77 (MIO77): ff0e0000.ethernet (GPIO UNCLAIMED) function mdio3 group mdio3_0_grp
```

This matches the MIO routing in the XSA (`PSU_MIO_TREE_PERIPHERALS`): QSPI on 0–12, I2C0 on 14–15, I2C1 on 16–17, UART0 on 18–19, UART1 on 20–21, CAN1 on 24–25, DisplayPort AUX on 27–30, SD1 on 39–51, USB0 on 52–63, GEM3 on 64–75, MDIO3 on 76–77. MIO 0–12 are unclaimed because the QSPI node has no `pinctrl-0` in the device tree.

## Hands-on

### See Linux programming the pins

On the reference setup, no FSBL ran, so no `psu_init` programmed the MIO. Compare a pin that Linux claims with one it does not:

```console
target# devmem 0xFF180048 32
0x000000C0
target# devmem 0xFF180000 32
0x00000000
```

MIO 18 (`0xFF180048`) holds `0xC0`, the UART0 RXD selection that `psu_init.c` would have written. Linux's pinctrl driver set it through the PMU firmware when the UART driver probed. MIO 0 (`0xFF180000`) is the QSPI clock pin: `psu_init.c` would write `0x00000002` (`L0_SEL` = 1, QSPI), but no Linux driver claims it, so it stays at reset value 0. On hardware both values would be set, because the FSBL ran first.

### Find the GPIO line of a MIO or EMIO pin

The `zynqmp_gpio` chip numbers its 174 lines as MIO 0–77, then EMIO 0–95:

| Pin | GPIO line |
| --- | --- |
| MIO n | n |
| EMIO n | 78 + n |
| `pl_resetn0` (EMIO 95) | 173 |

```console
target# gpiodetect
gpiochip0 [firmware:zynqmp-firmware:gpio] (4 lines)
gpiochip1 [zynqmp_gpio] (174 lines)
gpiochip2 [0-0020] (16 lines)
```

The frame buffer write IP's `reset-gpios = <... 0x50 ...>` in [section 02](02-ps-and-pl.md) is line 80, EMIO 2.

## PetaLinux 2024.1 specifics

- Pin routing comes from the Vivado PS configuration only. PetaLinux cannot change it; a new routing needs a new XSA and a new FSBL.
- The board file that adds `pinctrl` nodes is chosen by the machine configuration (`YAML_DT_BOARD_FLAGS`). For a custom board, either leave it out, so Linux keeps the FSBL's pin setup, or write `pinctrl` nodes that match the hardware design exactly ([chapter 12](../12-device-tree/README.md)).

## Pitfalls

- **Device tree pinctrl that disagrees with the XSA.** Linux re-programs the pins when the driver probes. A copied evaluation-board `pinctrl` node on a custom board can silently move a peripheral to the wrong pins.
- **Wrong bank voltage.** The I/O standard is a property of the board's `VCCO_PSIO` supply. A 3.3 V device on a 1.8 V bank does not work, or worse.
- **Planning PCIe, SATA, USB 3.0 and DisplayPort at the same time.** There are four PS-GTR lanes, and Table 29-1 limits which controller may use which lane.
- **Expecting EMIO peripherals before the PL is loaded.** Their signals go nowhere until the bitstream is configured.
- **Confusing MIO numbers, GPIO line numbers and pin names.** MIO 18 is GPIO line 18, but EMIO 2 is GPIO line 80.

## References

- DS891 Zynq UltraScale+ MPSoC Data Sheet: Overview (v1.11.1), peripheral feature lists
- UG1085 Zynq UltraScale+ Device TRM (v2.5): Chapter 2 (`VCCO_PSIO` banks), Chapter 11 (Table 11-1), Chapter 27 (GPIO banks), Chapter 28 ("Overview of the Blocks Function", Tables 28-2, 28-3), Chapter 29 (Table 29-1)
- `xilinx-zcu106-2024.1:project-spec/hw-description/system.xsa` (`psu_init.c` `psu_mio_init_data()`, `PSU_MIO_TREE_PERIPHERALS`, `PSU_BANK_*_IO_STANDARD`, GT lane parameters), `components/plnx_workspace/device-tree/device-tree/zcu106-reva.dtsi`
- `meta-xilinx@rel-v2024.1:meta-xilinx-bsp/conf/machine/zcu106-zynqmp.conf` (`YAML_DT_BOARD_FLAGS`)
- `linux-xlnx@xilinx-v2024.1:arch/arm64/boot/dts/xilinx/zynqmp.dtsi`, `zynqmp-zcu106-revA.dts`, `Documentation/devicetree/bindings/phy/xlnx,zynqmp-psgtr.yaml`, `include/dt-bindings/phy/phy.h`
- Captured on the reference setup: pinctrl debugfs, `devmem`, `gpiodetect`, `/sys/bus/platform/devices`

---

<sub>← [Interrupts and the GIC](08-interrupts-and-gic.md) · [Chapter index](README.md) · [Exception Levels and TrustZone](10-exception-levels-and-trustzone.md) →</sub>
