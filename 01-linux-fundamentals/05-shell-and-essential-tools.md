# Shell and Essential Tools for Embedded Work

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[01 · Linux Fundamentals](README.md)** · Part I: Foundations

## In short

- The target's tools are a mix of **BusyBox applets** and full programs. Know which one you are calling: BusyBox versions accept fewer options and print less.
- Write target scripts for POSIX `sh` (`#!/bin/sh`) unless you know `bash` is in the image. Some product images ship only BusyBox `ash`.
- A small set of commands answers most bring-up questions: `dmesg`, `journalctl`, `top`, `free`, `df`, `mount`, `lsblk`, and for hardware `devmem`, `i2cdetect`, `gpiodetect`/`gpioinfo`.
- Getting files on and off the target: `scp`/`rsync` over SSH ([section 07](07-ssh.md)), and `tftp` or `wget` when SSH is not available.

## Concepts

### Which shell, which tool?

```console
target$ ls -l /bin/sh /bin/ls /bin/ps /bin/mount /usr/bin/free /usr/bin/top /sbin/init
lrwxrwxrwx    1 root     root            12 Mar  9  2018 /bin/ls -> /bin/busybox
lrwxrwxrwx    1 root     root            21 Mar  9  2018 /bin/mount -> /bin/mount.util-linux
lrwxrwxrwx    1 root     root            12 Mar  9  2018 /bin/ps -> /bin/busybox
lrwxrwxrwx    1 root     root            14 Mar  9  2018 /bin/sh -> /bin/bash.bash
lrwxrwxrwx    1 root     root            22 Mar  9  2018 /sbin/init -> ../lib/systemd/systemd
lrwxrwxrwx    1 root     root            12 Mar  9  2018 /usr/bin/free -> /bin/busybox
lrwxrwxrwx    1 root     root            12 Mar  9  2018 /usr/bin/top -> /bin/busybox
target$ type ls mount cd
ls is hashed (/bin/ls)
mount is /bin/mount
cd is a shell builtin
```

On this image `/bin/sh` is bash, `ls`, `ps`, `top` and `free` are BusyBox, and `mount` comes from util-linux. Yocto picks one provider per command with **update-alternatives**, so the mix depends on the packages in the image. When two packages provide the same command, the one with the higher priority wins.

BusyBox is a single binary with 205 applets on this image:

```console
target$ busybox | head -2
BusyBox v1.35.0 () multi-call binary.
BusyBox is copyrighted by many authors between 1998-2015.
target$ busybox --list | wc -l
205
target$ busybox ls --help 2>&1 | head -4
BusyBox v1.35.0 () multi-call binary.

Usage: ls [-1AaCxdLHRFplinshrSXvctu] [-w WIDTH] [FILE]...
```

`busybox <applet> --help` shows the options **this** build supports, which is the first thing to check when a command from your host fails on the target. The full applet list of the reference image:

<details>
<summary>BusyBox 1.35.0 applets on the ZCU106 2024.1 image</summary>

```text
[ [[ addgroup adduser ascii ash awk base32 basename blkid bunzip2 bzcat bzip2 cat chattr chgrp chmod chown chroot
chvt clear cmp cp cpio crc32 cut date dc dd deallocvt delgroup deluser depmod devmem df diff dirname dmesg
dnsdomainname du dumpkmap dumpleases echo egrep env expr false fbset fdisk fgrep find flock free fsck fstrim ftpd
ftpget ftpput fuser getopt getty grep groups gunzip gzip hd head hexdump hostname httpd hwclock id ifconfig ifdown
ifup inetd insmod install ip kill killall klogd less ln loadfont loadkmap logger login logname logread losetup ls
lsmod lspci lsusb lzcat md5sum mdev mesg microcom mkdir mkfifo mkfs.vfat mknod mkswap mktemp modprobe more mount
mountpoint mv nc netstat nohup nproc nsenter nslookup od openvt passwd patch pgrep pidof ping ping6 pivot_root
printf ps pwd rdate readlink realpath reboot renice reset resize rev rfkill rm rmdir rmmod route run-parts sed seq
setconsole setsid sh sha1sum sha256sum sha512sum shuf sleep sort start-stop-daemon stat strings stty su sulogin
swapoff swapon switch_root sync sysctl syslogd tail tar tee telnet telnetd test tftp tftpd time top touch tr
traceroute true ts tty udhcpc udhcpd umount uname uniq unlink unzip uptime users usleep vi vlock watch watchdog wc
wget which who whoami xargs xzcat yes zcat
```

</details>

### Shell scripting for targets

A script that runs on any target shell sticks to POSIX `sh`: no arrays, no `[[ ]]`, no `function` keyword, no `${var,,}`. A small but complete example that summarizes the running system:

```sh
#!/bin/sh
# sysinfo.sh - print a short summary of the running system
set -eu

kernel=$(uname -r)
model=$(tr -d '\0' < /proc/device-tree/model)
cpus=$(grep -c '^processor' /proc/cpuinfo)
mem_mb=$(awk '/^MemTotal:/ {printf "%d", $2 / 1024}' /proc/meminfo)
rootdev=$(awk '$2 == "/" {print $1; exit}' /proc/mounts)

echo "Board : ${model}"
echo "Kernel: ${kernel}"
echo "CPUs  : ${cpus}"
echo "RAM   : ${mem_mb} MiB"
echo "Root  : ${rootdev}"
for dev in /sys/class/net/*; do
    name=${dev##*/}
    [ "$name" = lo ] && continue
    echo "Net   : ${name} $(cat "$dev/operstate")"
done
```

```console
target$ chmod +x sysinfo.sh && ./sysinfo.sh
Board : ZynqMP ZCU106 RevA
Kernel: 6.6.10-xilinx-v2024.1-g3af4295e00ef
CPUs  : 4
RAM   : 3930 MiB
Root  : /dev/mmcblk0
Net   : can0 down
Net   : eth0 up
Net   : sit0 down
```

Points worth copying:

- `set -eu` stops at the first failing command and at the first unset variable.
- The device tree `model` string ends in a NUL byte. `tr -d '\0'` removes it before printing.
- Everything comes from `/proc` and `/sys`, so the script needs no extra tools and works with BusyBox alone.
- Quote every variable expansion (`"$dev/operstate"`). Unquoted variables break on spaces and empty values.

> [!TIP]
> Check scripts on the host with `shellcheck --shell=sh script.sh` before copying them to the target. It catches most portability problems and quoting bugs.

## Hands-on

### Inspecting the system

| Question | Command |
| --- | --- |
| What did the kernel say during boot? | `dmesg` (ring buffer), `journalctl -k -b` (kernel messages of this boot) |
| What do the services say? | `journalctl -b -u <unit>`, `journalctl -b -p err` |
| What is running and using CPU? | `top`, `ps` |
| How much memory is free? | `free -h`, `/proc/meminfo` |
| Which filesystems, how full? | `mount`, `df -h`, `lsblk` |
| How long since boot, how loaded? | `uptime`, `/proc/loadavg` |
| Which USB and PCI devices? | `lsusb`, `lspci` |

Kernel messages are kept in a ring buffer. `dmesg` reads it:

```console
target# dmesg | head -5
[    0.000000] Booting Linux on physical CPU 0x0000000000 [0x410fd034]
[    0.000000] Linux version 6.6.10-xilinx-v2024.1-g3af4295e00ef (oe-user@oe-host) (aarch64-xilinx-linux-gcc (GCC) 12.2.0, GNU ld (GNU Binutils) 2.39.0.20220819) #1 SMP Sat Apr 27 05:22:24 UTC 2024
[    0.000000] KASLR disabled due to lack of seed
[    0.000000] Machine model: ZynqMP ZCU106 RevA
[    0.000000] earlycon: cdns0 at MMIO 0x00000000ff000000 (options '115200n8')
```

The systemd journal collects kernel messages **and** service output. A normal user only sees their own messages:

```console
target$ journalctl -b -p err --no-pager | head -5
Hint: You are currently not seeing messages from other users and the system.
      Users in groups 'adm', 'systemd-journal', 'wheel' can see all messages.
      Pass -q to turn off this notice.
No journal files were opened due to insufficient permissions.
target# journalctl -b -p err --no-pager | head -6
Oct 15 12:13:07 xilinx-zcu106-20241 kernel: xilinx-ams ffa50000.ams: error -ETIMEDOUT: failed to initialize AMS
Oct 15 12:13:07 xilinx-zcu106-20241 kernel: macb ff0e0000.ethernet: GEM doesn't support hardware ptp.
Oct 15 12:13:07 xilinx-zcu106-20241 kernel: max20751 4-0072: Failed to identify chip capabilities
Oct 15 12:13:07 xilinx-zcu106-20241 kernel: max20751 4-0073: Failed to identify chip capabilities
Oct 15 12:13:07 xilinx-zcu106-20241 kernel: macb ff0e0000.ethernet: GEM doesn't support hardware ptp.
Oct 15 12:13:11 xilinx-zcu106-20241 kernel[550]: [    1.424990] xilinx-ams ffa50000.ams: error -ETIMEDOUT: failed to initialize AMS
target# journalctl --disk-usage
Archived and active journals take up 8.0M in the file system.
```

`-p err` shows only messages of priority "error" and worse, which makes it the fastest way to spot driver problems after a boot. On QEMU these particular errors are expected: QEMU does not model the AMS sysmon block or the board's PMBus voltage regulators. On real hardware, every one of them would deserve a look.

> [!NOTE]
> The journal lives under `/var/log/journal` or `/run/log/journal`. On this image both are in RAM ([section 04](04-filesystem-hierarchy-and-processes.md)), so the journal of the previous boot is gone after a reboot.

A one-shot process overview (BusyBox `top` in batch mode):

```console
target# top -b -n 1 | head -8
Mem: 329120K used, 3695940K free, 11140K shrd, 28528K buff, 115516K cached
CPU:  2.1% usr  2.1% sys  0.0% nic 95.6% idle  0.0% io  0.0% irq  0.0% sirq
Load average: 0.29 0.17 0.19 1/155 972
  PID  PPID USER     STAT   VSZ %VSZ CPU %CPU COMMAND
  971   953 root     R     2012  0.0   1  4.3 top -b -n 1
  756   732 root     S     226m  5.7   3  0.0 /usr/libexec/at-spi-bus-launcher --launch-immediately
  781   732 root     S     187m  4.7   3  0.0 matchbox-desktop
  782   732 root     S     187m  4.7   2  0.0 matchbox-panel --start-applets showdesktop,windowselector --end-applets clock,,systray,startup-notify,notify
```

The ZCU106 BSP image starts an X11 desktop (Xorg, matchbox) for the DisplayPort output, even when nothing is connected. A product image would not.

Memory, storage and devices:

```console
target$ free -h
              total        used        free      shared  buff/cache   available
Mem:           3.8G      120.4M        3.6G       10.1M      115.5M        3.6G
Swap:             0           0           0
target$ df -h
Filesystem                Size      Used Available Use% Mounted on
devtmpfs                  1.4G      4.0K      1.4G   0% /dev
/dev/mmcblk0              1.2G    880.6M    233.2M  79% /
tmpfs                     1.9G         0      1.9G   0% /dev/shm
tmpfs                   786.1M      9.8M    776.3M   1% /run
tmpfs                     4.0M         0      4.0M   0% /sys/fs/cgroup
tmpfs                     1.9G      8.0K      1.9G   0% /tmp
tmpfs                     1.9G     32.0K      1.9G   0% /var/volatile
tmpfs                   393.1M         0    393.1M   0% /run/user/1000
target$ lsblk
NAME      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
mtdblock0  31:0    0   30M  0 disk 
mtdblock1  31:1    0  256K  0 disk 
mtdblock2  31:2    0   60M  0 disk 
mmcblk0   179:0    0    2G  0 disk /
target$ lsusb
Bus 001 Device 001: ID 1d6b:0002
Bus 002 Device 001: ID 1d6b:0003
```

- `available` in `free` is what new programs can actually get. `free` alone ignores the page cache, which the kernel gives back when needed.
- `mtdblock0` to `mtdblock2` are the QSPI flash partitions that `/proc/mtd` lists as `qspi-boot`, `qspi-bootenv` and `qspi-kernel` ([chapter 23](../23-storage-updates-and-production/01-mtd-and-flash.md)).
- `lsusb` shows only the two root hubs (`1d6b` is the Linux Foundation vendor ID): USB 2.0 and USB 3.0 of the DWC3 controller. BusyBox `lsusb` prints IDs without names.

### Poking hardware

> [!WARNING]
> These commands talk to hardware directly. A wrong address or a write to the wrong I2C device can hang the system or, on real boards, change power-supply settings. Read before you write, and know what is at the address.

**Registers with `devmem`.** `devmem <address> [width [value]]` reads or writes physical memory through `/dev/mem` (root only). As an example, read the boot mode register, which [chapter 06](../06-boot-sequence/02-boot-modes.md) covers in detail:

```console
target# devmem 0xFF5E0200 32
0x00000000
```

`0xFF5E0200` is `boot_mode` in the `CRL_APB` register block (base `0xFF5E0000`, offset `0x200`), and boot mode `0` is JTAG. That matches what U-Boot printed during this boot (`Bootmode: JTAG_MODE`), because the QEMU reference setup loads its images directly into memory, the way a JTAG debugger would.

**I2C with i2c-tools.** The reference image does not include i2c-tools; install them as shown in [section 03](03-package-management.md):

```console
target# i2cdetect -l
i2c-0	i2c       	Cadence I2C at ff020000         	I2C adapter
i2c-1	i2c       	Cadence I2C at ff030000         	I2C adapter
i2c-2	i2c       	i2c-0-mux (chan_id 0)           	I2C adapter
i2c-3	i2c       	i2c-0-mux (chan_id 1)           	I2C adapter
...
i2c-21	i2c       	i2c-1-mux (chan_id 7)           	I2C adapter
i2c-22	i2c       	ZynqMP DP AUX                   	I2C adapter
```

The two PS I2C controllers (`ff020000`, `ff030000`) feed I2C multiplexers on the ZCU106, and the kernel creates one adapter per mux channel. The DisplayPort AUX channel is also an I2C adapter (for monitor EDID). Then `i2cdetect -y <bus>` scans a bus, and `i2cget`/`i2cset` read and write registers of one device.

**GPIO with libgpiod.** The old `/sys/class/gpio` interface is deprecated. Use the character-device tools from `libgpiod-tools`:

```console
target# gpiodetect
gpiochip0 [firmware:zynqmp-firmware:gpio] (4 lines)
gpiochip1 [zynqmp_gpio] (174 lines)
gpiochip2 [0-0020] (16 lines)
gpiochip3 [0-0021] (16 lines)
target# gpioinfo gpiochip0
gpiochip0 - 4 lines:
	line   0:      unnamed       unused   input  active-high 
	line   1:      unnamed      "reset"  output   active-low [used]
	line   2:      unnamed       unused   input  active-high 
	line   3:      unnamed       unused   input  active-high 
```

- `zynqmp_gpio` is the PS GPIO controller with its MIO and EMIO pins ([chapter 03](../03-zynqmp-architecture/09-peripherals-mio-emio.md)).
- `0-0020` and `0-0021` are I2C GPIO expanders on bus 0, addresses `0x20` and `0x21`.
- The 4-line chip is the device's four boot-mode pins, which the PS can drive as outputs after boot through the platform firmware (`compatible = "xlnx,zynqmp-gpio-modepin"`). Line 1 shows as `"reset"` because the ZCU106 device tree uses it as the reset of the USB 3.0 controller: `usb@ff9d0000` has `reset-gpios = <&modepin_gpio 1 GPIO_ACTIVE_LOW>`.

`gpioset` and `gpioget` drive and read single lines.

**SPI.** `spidev_test` comes from the kernel source tree (`tools/spi/`) and is not part of the reference image. It needs a `/dev/spidevB.C` node, which only exists when the device tree binds a device to the `spidev` driver ([chapter 22](../22-networking-and-peripherals/05-low-speed-buses.md)).

### Files and text

`grep`, `find`, `sed`, `awk`, `hexdump` and `dd` cover most needs. A few target-flavored examples:

```console
target$ awk -F: '$3 >= 1000 {print $1, $6, $7}' /etc/passwd
petalinux /home/petalinux /bin/sh
nobody /nonexistent /sbin/nologin
target$ find /etc -name '*.service' 2>/dev/null | head -3
/etc/systemd/system/dbus-org.freedesktop.resolve1.service
/etc/systemd/system/network-online.target.wants/systemd-networkd-wait-online.service
/etc/systemd/system/modutils.service
target$ hexdump -C /proc/device-tree/model
00000000  5a 79 6e 71 4d 50 20 5a  43 55 31 30 36 20 52 65  |ZynqMP ZCU106 Re|
00000010  76 41 00                                          |vA.|
00000013
```

`dd` reads raw bytes from devices and files. The ext4 superblock starts 1024 bytes into the partition, and its magic number `0xEF53` sits at offset `0x38`, stored little-endian as `53 ef`:

```console
target# dd if=/dev/mmcblk0 bs=1024 skip=1 count=1 2>/dev/null | hexdump -C | head -6
00000000  d0 21 05 00 90 21 05 00  ad 41 00 00 28 12 01 00  |.!...!...A..(...|
00000010  30 96 04 00 00 00 00 00  02 00 00 00 02 00 00 00  |0...............|
00000020  00 80 00 00 00 80 00 00  70 77 00 00 4f c3 d0 6a  |........pw..O..j|
00000030  4f c3 d0 6a 04 00 ff ff  53 ef 01 00 01 00 00 00  |O..j....S.......|
00000040  5e 0b 4f 66 00 00 00 00  00 00 00 00 01 00 00 00  |^.Of............|
00000050  00 00 00 00 0b 00 00 00  00 01 00 00 3c 00 00 00  |............<...|
```

The same technique identifies boot images, bitstreams and partitions in later chapters ([chapter 07](../07-boot-images-and-bootgen/03-boot-bin-anatomy.md)).

> [!CAUTION]
> `dd` writes as happily as it reads. `dd of=/dev/mmcblk0` overwrites the card without asking. Double-check `if=` and `of=` every time.

### Moving files

With SSH available, use `scp` and `rsync` ([section 07](07-ssh.md)). Without it, the BusyBox `tftp` and `wget` clients work against any TFTP or HTTP server. On the reference setup the host is reachable from the target as `10.0.2.2`:

```console
target$ cd /tmp && tftp -g -r system.dtb 10.0.2.2 && ls -l system.dtb; cd
-rw-r--r--    1 petalinu petalinu     54985 Oct 15 12:29 system.dtb
target$ wget -O /tmp/Image http://10.0.2.2:18000/Image
Connecting to 10.0.2.2:18000 (10.0.2.2:18000)
saving to '/tmp/Image'
...
'/tmp/Image' saved
target$ md5sum /tmp/Image /tmp/system.dtb
c17c70580356615fc3f626b01a40147c  /tmp/Image
c3529b3be8a941e7a2f3e60c80db1ac7  /tmp/system.dtb
```

On the host, the HTTP server was a one-liner, and the checksums match:

```console
$ python3 -m http.server 18000 --bind 127.0.0.1 --directory ./tftpboot
$ md5sum tftpboot/Image tftpboot/system.dtb
c17c70580356615fc3f626b01a40147c  tftpboot/Image
c3529b3be8a941e7a2f3e60c80db1ac7  tftpboot/system.dtb
```

Always compare checksums after copying something you are about to boot or flash. [Section 08](08-networking-for-development.md) explains the TFTP server side and the `10.0.2.2` address.

## Pitfalls

- **Host command, target syntax.** `ps aux`, `ls --color=auto`, `grep -P` and many GNU options do not exist in BusyBox. Check with `busybox <applet> --help`.
- **bash-only scripts on an ash target.** A script tested on a host with bash fails on a target whose `/bin/sh` is BusyBox `ash`. Test with the target's shell.
- **Reading the journal as a normal user.** You get "insufficient permissions" and nothing else. Use `sudo journalctl`, or add the user to the `systemd-journal` group.
- **Trusting `free`'s `free` column.** Look at `available`.

## References

- BusyBox documentation: `busybox <applet> --help` on the target, [busybox.net](https://busybox.net/)
- `xilinx-zcu106-2024.1:pre-built/linux/images/system.dtb`, decompiled with `dtc` (`xlnx,zynqmp-gpio-modepin`, `usb@ff9d0000` `reset-gpios`)
- `u-boot-xlnx@xilinx-v2024.1:arch/arm/mach-zynqmp/include/mach/hardware.h` (`ZYNQMP_CRL_APB_BASEADDR`, `boot_mode` at `0x200`, `JTAG_MODE`, `BOOT_MODES_MASK`)
- libgpiod: `linux-xlnx@xilinx-v2024.1:Documentation/userspace-api/gpio/` and the libgpiod README
- Man pages: `journalctl(1)`, `dmesg(1)`, `dd(1)`, `hexdump(1)`
- Captured on the reference setup: all target and host output above

---

<sub>← [Filesystem Hierarchy, Processes and Permissions](04-filesystem-hierarchy-and-processes.md) · [Chapter index](README.md) · [Serial Console](06-serial-console.md) →</sub>
