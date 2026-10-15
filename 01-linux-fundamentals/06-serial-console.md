# Serial Console

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · ZCU10x boards and QEMU

**[01 · Linux Fundamentals](README.md)** · Part I: Foundations

## In short

- The serial console is the one interface that works from the first instruction of the boot to the last. Keep it connected during all development.
- ZynqMP has two PS UARTs, at `0xFF000000` (UART0) and `0xFF010000` (UART1). **Each boot stage chooses its own UART.** In the ZCU106 2024.1 BSP, TF-A prints to UART1 while everything else prints to UART0.
- The Linux console is set up by three things: `stdout-path` and the `serialN` aliases in the device tree, and the `earlycon` and `console=` kernel arguments.
- On the host, `minicom` or `screen` (both on Ubuntu) or `picocom`/`tio` connect to the USB-UART bridge at **115200 baud, 8N1, no flow control**.

## Concepts

### UART basics

A UART sends bytes as a sequence of bits on one wire per direction (TX, RX, plus ground). Both ends must agree on the format:

| Setting | ZynqMP default | Meaning |
| --- | --- | --- |
| Baud rate | 115200 | Bits per second on the wire |
| Data bits, parity, stop bits | 8N1 | 8 data bits, no parity, 1 stop bit |
| Flow control | None | No RTS/CTS or XON/XOFF; disable it in the terminal program, or input will be ignored |

The ZynqMP UART pins use the logic level of their MIO bank (1.8 V to 3.3 V). Never connect them to an RS-232 port, whose levels are up to ±12 V. Evaluation boards and SOMs put a **USB-UART bridge** on the board, so you only need a USB cable. The host sees one `/dev/ttyUSBn` per bridge channel, and a quad bridge gives you four of them.

### Which stage prints where

Every boot stage is a separate program with its own UART driver and its own idea of which UART to use. PetaLinux selects them in `petalinux-config` → *Subsystem Hardware Settings* → *Serial Settings*. The ZCU106 2024.1 BSP sets:

```text
CONFIG_SUBSYSTEM_PMUFW_SERIAL_PSU_UART_0_SELECT=y
CONFIG_SUBSYSTEM_FSBL_SERIAL_PSU_UART_0_SELECT=y
CONFIG_SUBSYSTEM_TF-A_SERIAL_PSU_UART_1_SELECT=y
CONFIG_SUBSYSTEM_SERIAL_PSU_UART_0_SELECT=y
```

| Stage | UART in the ZCU106 BSP | What you see |
| --- | --- | --- |
| PMU firmware | UART0 | `PMU Firmware 2024.1 ...` |
| FSBL | UART0 | `Zynq MP First Stage Boot Loader` and `Release 2024.1 ...` (on hardware) |
| TF-A (BL31) | **UART1** | `NOTICE:  BL31: ...` |
| U-Boot and Linux (`CONFIG_SUBSYSTEM_SERIAL_*`) | UART0 | U-Boot banner, kernel log, login prompt |

The reference setup proves it. Its QEMU writes UART0 to one log file and UART1 to another. UART1 contains only TF-A's lines:

```text
NOTICE:  BL31: Secure code at 0x60000000
NOTICE:  BL31: Non secure code at 0x8000000
NOTICE:  BL31: v2.10.0	(release):v1.1-13187-g4f82b6134
NOTICE:  BL31: Built : 04:45:53, Mar 12 2024
```

So on a ZCU106 with this BSP, a terminal on UART0 shows the PMU firmware banner and then U-Boot, with no TF-A messages in between. This is the most common reason for "missing" boot output: the stage is running fine, but it is printing to a UART nobody is watching.

> [!NOTE]
> The QEMU reference setup loads TF-A and U-Boot directly into memory, so it does not run the FSBL and you will not see an FSBL banner there. [Chapter 06](../06-boot-sequence/01-boot-overview.md) shows the full chain on hardware.

Other reasons for a silent console, in the order worth checking:

1. Wrong `/dev/ttyUSBn` on the host, or wrong baud rate.
2. Flow control enabled in the terminal program (output appears, input does not work).
3. The stage was built without console output, or with a different UART selected (above).
4. The kernel has no `console=` argument, or the device tree's `stdout-path` and aliases point elsewhere (next section).
5. The board is not booting at all: check the boot mode ([chapter 06](../06-boot-sequence/02-boot-modes.md)) and [Boot Troubleshooting](../06-boot-sequence/15-boot-troubleshooting.md).

### How Linux picks its console

Three mechanisms work together. The device tree of the reference image (decompiled `system.dtb`):

```dts
aliases {
    ...
    serial0 = "/axi/serial@ff000000";
    serial1 = "/dcc";
    serial2 = "/axi/serial@ff010000";
    ...
};

chosen {
    bootargs = "earlycon console=ttyPS0,115200 root=/dev/ram0 rw init_fatal_sh=1 cma=1000M";
    stdout-path = "serial0:115200n8";
};
```

- **`serialN` aliases** decide the device names. The Cadence UART driver names its devices `ttyPS<N>` after the alias number, so UART0 is `ttyPS0`, and UART1 becomes **`ttyPS2`**, because alias `serial1` is taken by the Arm debug communication channel (`/dcc`).
- **`earlycon`** without arguments tells the kernel to find the early console through `stdout-path`. It uses a minimal polling driver from the first milliseconds of the boot, long before the real UART driver is probed.
- **`console=ttyPS0,115200`** selects the real console once the driver is up.

You can watch the hand-over in the boot log:

```text
[    0.000000] earlycon: cdns0 at MMIO 0x00000000ff000000 (options '115200n8')
[    0.000000] printk: bootconsole [cdns0] enabled
...
[    2.139488] ff000000.serial: ttyPS0 at MMIO 0xff000000 (irq = 22, base_baud = 2169921) is a xuartps
[    2.141591] printk: console [ttyPS0] enabled
[    2.142193] printk: bootconsole [cdns0] disabled
[    2.152202] ff010000.serial: ttyPS2 at MMIO 0xff010000 (irq = 23, base_baud = 2169921) is a xuartps
```

> [!TIP]
> If the kernel hangs before the UART driver loads, `earlycon` is what lets you see why. Keep it in development builds.

### The login prompt

Once user space runs, systemd starts a **getty** on the console. It opens the TTY, sets the line, prints the login prompt and hands over to `login`:

```console
target# systemctl status serial-getty@ttyPS0.service --no-pager | head -8
● serial-getty@ttyPS0.service - Serial Getty on ttyPS0
     Loaded: loaded (/lib/systemd/system/serial-getty@.service; enabled; preset: disabled)
     Active: active (running) since Thu 2026-10-15 12:41:20 UTC; 1min 52s ago
       Docs: man:agetty(8)
             man:systemd-getty-generator(8)
             http://0pointer.de/blog/projects/serial-console.html
   Main PID: 729 (agetty)
      Tasks: 1 (limit: 3507)
target# stty -F /dev/ttyPS0
speed 115200 baud; line = 0;
intr = ^C; quit = ^\; erase = ^?; kill = ^U; eof = ^D; eol = <undef>;
eol2 = <undef>; swtch = <undef>; start = ^Q; stop = ^S; susp = ^Z; rprnt = ^R;
werase = ^W; lnext = ^V; flush = ^O; min = 1; time = 0;
-brkint -icrnl -imaxbel iutf8
-isig -icanon -iexten -echo -echoe -echok -echoctl -echoke
```

Both commands were run over SSH while nobody was logged in on the console. The main process is `agetty`, which has put the line into raw mode (`-icanon -echo`) to read the user name one character at a time. After a successful login, the service's main process becomes `login` and then your shell, and the line is switched back to normal (canonical, echoing) mode.

`systemd-getty-generator` creates `serial-getty@ttyPS0.service` automatically for the kernel console. To get a login prompt on a second UART as well, enable the service for that device, for example `systemctl enable --now serial-getty@ttyPS2.service`.

## Hands-on

### Finding the right port on the host

Plug in the board's USB-UART cable and power the board, then:

```bash
ls -l /dev/serial/by-id/
dmesg | grep -i ttyUSB
```

A quad bridge creates four ports with the same USB serial number and interface numbers `if00` to `if03`. Which interface is wired to which UART is board-specific. Check the board user guide (UG1182 for ZCU102, UG1267 for ZCU104, UG1244 for ZCU106) or try each port at 115200 while the board boots. Use the `/dev/serial/by-id/...` path in scripts, because `ttyUSBn` numbers change with plug order.

Serial ports belong to the `dialout` group. Add yourself once, then log out and in again:

```bash
sudo usermod -aG dialout "$USER"
```

> [!NOTE]
> **Not run on the reference setup:** the reference setup has no physical board, so the commands in this subsection were not executed. The terminal programs below were tested against the QEMU console through a pseudo-terminal.

### Terminal programs

| Program | Open a port | Quit | Log to a file | Package (Ubuntu) |
| --- | --- | --- | --- | --- |
| `minicom` | `minicom -D /dev/ttyUSB1 -b 115200` | Ctrl-A, X, Enter | Ctrl-A, L | `minicom` |
| `screen` | `screen /dev/ttyUSB1 115200` | Ctrl-A, k, y | `screen -L ...` | `screen` |
| `picocom` | `picocom -b 115200 /dev/ttyUSB1` | Ctrl-A, Ctrl-X | `--logfile boot.log` | `picocom` |
| `tio` | `tio -b 115200 /dev/ttyUSB1` | Ctrl-T, Q | `--log --log-file boot.log` | `tio` |

minicom remembers settings in `~/.minirc.dfl`. Run `minicom -s` once and set *Hardware Flow Control* to *No*. `minicom -o` skips the modem initialization strings, which only add garbage on a board console.

The reference setup exposes the QEMU console as a Unix socket. `socat` turns it into a pseudo-terminal, so that the same programs can be used:

```bash
socat pty,raw,echo=0,link=./vtty unix-connect:ttyPS0.sock &
minicom -D ./vtty -b 115200 -o
```

### Capturing a boot log with timestamps

Timestamps on the host side tell you how long each stage takes, including the stages that print no timestamps themselves. The following pipeline needs nothing beyond `socat` and bash. On the reference setup the input is the QEMU socket:

```bash
socat -u UNIX-CONNECT:ttyPS0.sock - \
  | while IFS= read -r line; do printf '[%s] %s\n' "$(date +%T.%3N)" "${line%$'\r'}"; done \
  > boot-ts.log
```

On a board, replace the input with the serial device: `socat -u /dev/ttyUSB1,b115200,raw,echo=0 -`.

Key lines from a cold boot of the reference target:

```text
[15:40:49.466] PMU Firmware 2024.1	May 19 2024   02:40:12
[15:40:49.879] U-Boot 2024.01 (May 14 2024 - 03:31:48 +0000)
[15:40:52.942] Hit any key to stop autoboot:  2  1  0
[15:40:53.109] Starting kernel ...
[15:40:53.134] [    0.000000] earlycon: cdns0 at MMIO 0x00000000ff000000 (options '115200n8')
[15:41:20.812] [  OK  ] Reached target Multi-User System.
[15:41:24.417] xilinx-zcu106-20241 login:
```

U-Boot appears 0.4 s after the PMU firmware, and 2 of the following 3.2 s are U-Boot's autoboot countdown. User space then takes most of the remaining 31 s. QEMU timing is not hardware timing, but the method is the same; [chapter 23](../23-storage-updates-and-production/05-boot-time-optimization.md) uses it to optimize boot time.

## Pitfalls

- **Hardware flow control left on.** You see output but cannot type. Turn it off in the terminal program.
- **Two programs on one port.** A second terminal (or a forgotten `screen` session) steals characters from the first. The same happens with the QEMU socket of the reference setup, which accepts one client at a time.
- **Looking for TF-A messages on UART0.** In the ZCU106 2024.1 BSP they are on UART1.
- **Hard-coding `/dev/ttyPS1` for UART1.** The name follows the device tree alias; on this BSP it is `ttyPS2`.
- **Pasting long commands into a 115200-baud console.** Characters can be dropped. Use SSH for anything longer than a line.

## References

- `xilinx-zcu106-2024.1:project-spec/configs/config` (`CONFIG_SUBSYSTEM_*_SERIAL_*`)
- `xilinx-zcu106-2024.1:pre-built/linux/images/system.dtb`, decompiled with `dtc` (`aliases`, `chosen`)
- `linux-xlnx@xilinx-v2024.1:Documentation/admin-guide/kernel-parameters.txt` (`earlycon`, `console`)
- `linux-xlnx@xilinx-v2024.1:drivers/tty/serial/xilinx_uartps.c` (`CDNS_UART_TTY_NAME "ttyPS"`, line number from `of_alias_get_id(..., "serial")`)
- `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c` (FSBL banner)
- `xilinx-zcu106-2024.1:project-spec/configs/configs/Kconfig.syshw` (*Serial Settings* menu)
- Board user guides: UG1182 (ZCU102), UG1267 (ZCU104), UG1244 (ZCU106)
- Man pages: `agetty(8)`, `systemd-getty-generator(8)`, `minicom(1)`, `screen(1)`, `socat(1)`
- Captured on the reference setup: UART0 and UART1 logs of the QEMU target, timestamped cold-boot log, `systemctl`, `stty`

---

<sub>← [Shell and Essential Tools for Embedded Work](05-shell-and-essential-tools.md) · [Chapter index](README.md) · [SSH: Secure Shell](07-ssh.md) →</sub>
