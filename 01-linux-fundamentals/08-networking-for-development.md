# Networking for Development

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · Ubuntu 22.04 host

**[01 · Linux Fundamentals](README.md)** · Part I: Foundations

## In short

- A network link between host and target turns slow edit-flash-boot cycles into seconds: **TFTP** loads a new kernel straight into U-Boot, **NFS** serves the root filesystem from the host, and **SSH** deploys applications.
- On the target, PetaLinux 2024.1 configures Ethernet with **systemd-networkd** (DHCP by default, `/lib/systemd/network/80-wired.network`). A static address is one small `.network` file.
- On the reference setup the target sits behind QEMU's user-mode network: it is `10.0.2.15`, the host is `10.0.2.2`, and QEMU also provides DHCP, DNS and a TFTP server.
- The kernel in the reference image already supports an NFS root filesystem (`CONFIG_ROOT_NFS=y`, `CONFIG_IP_PNP_DHCP=y`).

## Concepts

### Lab topologies

| Topology | How | Pros | Cons |
| --- | --- | --- | --- |
| Direct cable host ↔ board | Second host NIC or USB-Ethernet adapter, static IPs on both ends | Isolated, predictable, no IT involvement | No internet for the board unless the host routes it |
| Lab switch with DHCP | Board and host on the same LAN | Simple, board can reach package feeds | Board address may change; shared network |
| QEMU user-mode network | Built into QEMU (`-netdev user`) | Zero setup, NAT to the internet | Target not reachable from outside without port forwards |

The reference setup uses the third. QEMU emulates a small network behind the host:

| Address | Role |
| --- | --- |
| `10.0.2.15` | The target (assigned by QEMU's DHCP server) |
| `10.0.2.2` | The host. Connections to it reach the host's own `127.0.0.1` |
| `10.0.2.3` | DNS server, forwarding to the host's resolver |

The QEMU command line adds `hostfwd=tcp:127.0.0.1:2222-:22` so that the host can reach the target's SSH server ([section 07](07-ssh.md)), and `tftp=<dir>` so that QEMU serves that directory over TFTP at `10.0.2.2`.

### How the target configures its network

```console
target$ ip -br addr
lo               UNKNOWN        127.0.0.1/8 ::1/128
sit0@NONE        DOWN
can0             DOWN
eth0             UP             10.0.2.15/24 metric 10 fec0::ccd4:d3ff:fe02:615f/64 fe80::ccd4:d3ff:fe02:615f/64
target$ ip route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 10
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 metric 10
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 10
10.0.2.3 dev eth0 proto dhcp scope link src 10.0.2.15 metric 10
target$ networkctl list --no-pager
IDX LINK TYPE     OPERATIONAL SETUP
  1 lo   loopback carrier     unmanaged
  2 sit0 sit      off         unmanaged
  3 can0 can      off         unmanaged
  5 eth0 ether    routable    configured

4 links listed.
target$ systemctl is-active systemd-networkd NetworkManager networking 2>&1
active
inactive
inactive
```

systemd-networkd manages `eth0`. The image also contains `/etc/network/interfaces` (ifupdown) with `iface eth0 inet dhcp`, but the `networking` service that would read it is not active. When you look for "the network configuration" on a PetaLinux target, look at networkd first.

The default configuration comes from systemd itself:

```console
target# cat /lib/systemd/network/80-wired.network | grep -v '^#' | grep -v '^$'
[Match]
Type=ether
Name=!veth*
KernelCommandLine=!nfsroot
KernelCommandLine=!ip
[Network]
DHCP=yes
[DHCP]
UseMTU=yes
RouteMetric=10
ClientIdentifier=mac
```

It matches every Ethernet interface and runs DHCP, **except** when the kernel command line contains `nfsroot` or `ip`. In that case the kernel has already configured the interface to mount its root filesystem, and networkd must not touch it ([NFS root](#nfs-root) below).

`networkctl status eth0` shows which file was applied and the details of the lease (trimmed):

```console
target# networkctl status eth0 --no-pager | head -12
* 5: eth0
                     Link File: /lib/systemd/network/99-default.link
                  Network File: /lib/systemd/network/80-wired.network
                          Type: ether
                          Kind: n/a
                         State: routable (configured)
                  Online state: online
                          Path: platform-ff0e0000.ethernet
                        Driver: macb
              Hardware Address: f2:3e:3c:7b:26:0a
                           MTU: 1500 (min: 68, max: 10222)
                         QDisc: mq
```

`ff0e0000.ethernet` is GEM3, the PS Ethernet controller used on ZCU10x boards, driven by the `macb` driver ([chapter 22](../22-networking-and-peripherals/01-ethernet.md)).

## Hands-on

### A static IP address on the target

Files in `/etc/systemd/network/` take precedence over those in `/lib/systemd/network/`, and the first matching file in lexical order wins. A static configuration for `eth0`:

```console
target# cat /etc/systemd/network/10-eth0-static.network
[Match]
Name=eth0

[Network]
Address=10.0.2.15/24
Gateway=10.0.2.2
DNS=10.0.2.3
target# networkctl reload && networkctl reconfigure eth0 && sleep 3 && networkctl status eth0 --no-pager | head -12
* 5: eth0
                     Link File: /lib/systemd/network/99-default.link
                  Network File: /etc/systemd/network/10-eth0-static.network
...
target# ip -br addr show eth0; ip route
eth0             UP             10.0.2.15/24 metric 10 fec0::f03e:3cff:fe7b:260a/64 fe80::f03e:3cff:fe7b:260a/64
default via 10.0.2.2 dev eth0 proto static
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 metric 10
```

The default route now says `proto static`. On a real board, use addresses from your lab network, and put the file into the image so that it survives reflashing ([chapter 05](../05-petalinux/07-meta-user-customization.md)).

> [!WARNING]
> Going back to DHCP on the reference target by deleting the file and running `networkctl reload && networkctl reconfigure eth0` left the target **without a default route**: the DHCP address came back, the static route went away, and no DHCP route replaced it. `networkctl renew eth0` did not help; `systemctl restart systemd-networkd` did. If you change network configuration over SSH, keep the serial console open.

On the host side, give the NIC used for a direct cable a fixed address, for example with NetworkManager:

```bash
nmcli connection add type ethernet ifname enx001122334455 con-name board-link \
    ipv4.method manual ipv4.addresses 192.168.10.1/24 ipv6.method disabled
nmcli connection up board-link
```

> [!NOTE]
> **Not run on the reference setup:** the `nmcli` commands change the host's network configuration and need a second NIC.

### TFTP: loading a kernel from the host

TFTP is a tiny UDP file-transfer protocol without authentication. U-Boot implements it, which makes it the standard way to boot a freshly built kernel without touching the SD card.

**The server on the host.** Ubuntu's `tftpd-hpa` serves one directory. On the reference host it is installed and active:

```console
$ systemctl is-active tftpd-hpa
active
$ cat /etc/default/tftpd-hpa
# /etc/default/tftpd-hpa

TFTP_USERNAME="tftp"
TFTP_DIRECTORY="/srv/tftp"
TFTP_ADDRESS=":69"
TFTP_OPTIONS="--secure"
$ tftp 127.0.0.1 -c get BOOT.BIN && stat -c '%s %n' BOOT.BIN
21153024 BOOT.BIN
```

`--secure` confines the server to `/srv/tftp`, so clients request plain file names (`Image`, not `/srv/tftp/Image`). Copy the files to boot into that directory:

```bash
sudo apt install tftpd-hpa        # if it is not installed yet
sudo cp images/linux/Image images/linux/system.dtb /srv/tftp/
```

> [!NOTE]
> **Not run on the reference setup:** the `sudo` commands above. On the reference setup, QEMU's built-in TFTP server (the `tftp=` option) played the role of `tftpd-hpa`.

**The client in U-Boot.** Stop autoboot by pressing a key during `Hit any key to stop autoboot`, then:

```console
ZynqMP> setenv autoload no
ZynqMP> dhcp
BOOTP broadcast 1
DHCP client bound to address 10.0.2.16 (0 ms)
ZynqMP> setenv serverip 10.0.2.2
ZynqMP> tftpboot 0x200000 Image
Using ethernet@ff0e0000 device
TFTP from server 10.0.2.2; our IP address is 10.0.2.16
Filename 'Image'.
Load address: 0x200000
Loading: *#################################################################
	 ...
	 98.5 MiB/s
done
Bytes transferred = 24269312 (1725200 hex)
ZynqMP> tftpboot 0x100000 system.dtb
Using ethernet@ff0e0000 device
TFTP from server 10.0.2.2; our IP address is 10.0.2.16
Filename 'system.dtb'.
Load address: 0x100000
Loading: *####
done
Bytes transferred = 54985 (d6c9 hex)
ZynqMP> setenv bootargs earlycon console=ttyPS0,115200 root=/dev/mmcblk0 rw rootwait cma=1000M
ZynqMP> booti 0x200000 - 0x100000
## Flattened Device Tree blob at 00100000
   Booting using the fdt blob at 0x100000
Working FDT set to 100000
   Loading Device Tree to 0000000077bd3000, end 0000000077be36c8 ... OK
Working FDT set to 77bd3000
Starting kernel ...
```

The kernel then mounted the ext4 root filesystem from the SD card and booted to the login prompt:

```text
[    0.000000] Kernel command line: earlycon console=ttyPS0,115200 root=/dev/mmcblk0 rw rootwait cma=1000M
[    3.805761] EXT4-fs (mmcblk0): mounted filesystem 3b837610-55ee-494c-a360-3ca957829a7a r/w with ordered data mode. Quota mode: none.
[    3.806520] VFS: Mounted root (ext4 filesystem) on device 179:0.
[    3.893272] Run /sbin/init as init process
```

What each step does:

| Step | Purpose |
| --- | --- |
| `setenv autoload no` | Without it, `dhcp` immediately tries to TFTP a boot file named after the IP address. The reference run without it printed `*** Warning: no boot file name; using '0A000210.img'` and failed with `TFTP error: 'File not found'` |
| `dhcp` | Gets an IP address. Alternatively set `ipaddr` by hand |
| `setenv serverip` | Address of the TFTP server. Without it U-Boot does not know where to ask |
| `tftpboot <addr> <file>` | Downloads the file to the given RAM address |
| `setenv bootargs ...` | Kernel command line. Here: use the SD card as root instead of the prebuilt image's RAM disk |
| `booti <kernel> - <dtb>` | Boots an arm64 `Image`. The `-` means "no initrd" |

Add `saveenv` to make `serverip` and friends permanent on a board whose environment is stored in flash. The load addresses `0x200000` (kernel) and `0x100000` (DTB) are the ones PetaLinux uses; [chapter 06](../06-boot-sequence/12-boot-address-map.md) explains where they come from, and [chapter 11](../11-u-boot/03-environment-and-boot-scripts.md) shows how to automate all of this in a boot script.

### NFS root

With an NFS root filesystem, the target mounts its `/` from a directory on the host. Changes on the host (a rebuilt application, an edited config file) are visible on the target immediately, without copying or reflashing.

The kernel needs NFS client support, root-over-NFS and IP auto-configuration built in. The reference kernel has all of them:

```console
target$ zcat /proc/config.gz 2>/dev/null | grep -E '^CONFIG_(ROOT_NFS|IP_PNP|IP_PNP_DHCP|NFS_FS|NFS_V3|NFS_V4)='
CONFIG_IP_PNP=y
CONFIG_IP_PNP_DHCP=y
CONFIG_NFS_FS=y
CONFIG_NFS_V3=y
CONFIG_NFS_V4=y
CONFIG_ROOT_NFS=y
```

On the host, export a directory containing the unpacked root filesystem:

```bash
sudo apt install nfs-kernel-server
sudo mkdir -p /srv/nfs/zcu106
sudo tar -xpf images/linux/rootfs.tar.gz -C /srv/nfs/zcu106
echo '/srv/nfs/zcu106 192.168.10.0/24(rw,no_root_squash,no_subtree_check)' | sudo tee -a /etc/exports
sudo exportfs -ra
```

`no_root_squash` lets the target's root user act as root on the export, which a root filesystem needs. Restrict the export to the lab subnet.

In U-Boot, point the kernel at the export:

```text
setenv bootargs earlycon console=ttyPS0,115200 root=/dev/nfs nfsroot=192.168.10.1:/srv/nfs/zcu106,v3,tcp ip=dhcp rw
```

| Argument | Meaning |
| --- | --- |
| `root=/dev/nfs` | Mount the root filesystem over NFS |
| `nfsroot=<server>:<path>,<options>` | Server and exported path; `v3,tcp` avoids NFSv4 setup issues |
| `ip=dhcp` | Let the kernel configure the interface before user space starts (needs `CONFIG_IP_PNP_DHCP`) |

Because `nfsroot` and `ip` appear on the command line, `80-wired.network` does not match, and networkd leaves the interface alone. That is intentional: re-running DHCP on the interface that carries the root filesystem can hang the system. PetaLinux can build an image for this setup directly (`petalinux-config` → *Image Packaging Configuration* → *Root filesystem type* → *NFS*, [chapter 15](../15-root-filesystem-and-init/04-rootfs-boot-options.md)).

> [!NOTE]
> **Not run on the reference setup:** the reference host has no NFS server installed, and the NFS steps above were not executed. The kernel configuration check was.

### Diagnostics

| Tool | Where | Use |
| --- | --- | --- |
| `ping` | Host, target, U-Boot | Basic reachability |
| `ip addr`, `ip route`, `networkctl` | Target | Addresses, routes, which config was applied |
| `ss -ltn`, `netstat -tln` | Host, target | Listening ports |
| `ethtool <if>` | Target (install it) | Link speed, duplex, auto-negotiation, driver statistics |
| `tcpdump` | Host, target (install it) | See the actual packets |
| `iperf3` | Both ends | Throughput |

`ethtool` and `tcpdump` are not in the reference image, but the package feed has them ([section 03](03-package-management.md)):

```console
target# ethtool eth0 | head -8
Settings for eth0:
	Supported ports: [ TP	 MII ]
	Supported link modes:   10baseT/Half 10baseT/Full
	                        100baseT/Half 100baseT/Full
	                        1000baseT/Half 1000baseT/Full
	                        1000baseX/Full
	Supported pause frame use: Transmit-only
	Supports auto-negotiation: Yes
target# (sleep 2; ping -c 2 10.0.2.2 >/dev/null) & tcpdump -n -i eth0 -c 4 icmp 2>&1
[1] 1066
...
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
12:48:41.917904 IP 10.0.2.15 > 10.0.2.2: ICMP echo request, id 1069, seq 0, length 64
12:48:41.918815 IP 10.0.2.2 > 10.0.2.15: ICMP echo reply, id 1069, seq 0, length 64
12:48:42.919237 IP 10.0.2.15 > 10.0.2.2: ICMP echo request, id 1069, seq 1, length 64
12:48:42.919454 IP 10.0.2.2 > 10.0.2.15: ICMP echo reply, id 1069, seq 1, length 64
4 packets captured
4 packets received by filter
0 packets dropped by kernel
```

When `tcpdump` runs on the serial console, kernel messages about promiscuous mode appear in between (trimmed here). Run it over SSH to avoid them, and exclude your own SSH traffic with a filter such as `not port 22`.

> [!TIP]
> BusyBox on this image has no `timeout` applet. Use `-c <count>` with tcpdump and ping to make them stop on their own.

## Pitfalls

- **Forgetting `setenv autoload no` before `dhcp` in U-Boot.** You get a confusing TFTP error for a file you never asked for.
- **Running NFS root with networkd reconfiguring the interface.** Make sure the kernel command line contains `ip=` or `nfsroot=` so that the default `80-wired.network` does not match.
- **TFTP through firewalls.** TFTP uses UDP port 69 and then random ports. A host firewall (`ufw`) must allow it, or transfers time out after the first packet.
- **Board and lab network on the same subnet as the host's main NIC.** Two interfaces in one subnet confuse routing on the host. Use a separate subnet for the board link.
- **Changing the network configuration over SSH.** One typo and the session is gone. Keep the serial console connected.

## References

- `systemd.network(5)`, `networkctl(1)`, `systemd-networkd(8)`
- QEMU documentation: user-mode networking (`-netdev user`, `hostfwd`, `tftp`)
- `linux-xlnx@xilinx-v2024.1:Documentation/admin-guide/nfs/nfsroot.rst` (`root=/dev/nfs`, `nfsroot=`, `ip=`)
- U-Boot documentation: `tftpboot`, `dhcp`, `booti`, environment variables `autoload`, `serverip`
- `tftpd-hpa` and `exports(5)` man pages
- `xilinx-zcu106-2024.1:project-spec/configs/configs/Kconfig.imagepkgconfigurations` (*Root filesystem type* → *NFS*)
- Captured on the reference setup: target `ip`, `networkctl`, `ethtool`, `tcpdump`, static networkd configuration; U-Boot TFTP session and boot with SD root; host `tftpd-hpa` status and transfer

---

<sub>← [SSH: Secure Shell](07-ssh.md) · [Chapter index](README.md) · Next chapter: [02 · Embedded Linux Concepts](../02-embedded-linux-concepts/README.md) →</sub>
