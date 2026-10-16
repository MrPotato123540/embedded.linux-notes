# Network Configuration on the Target

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## Build connectivity in layers

An operational network needs a link, an address, a route to the destination and an application service. Name resolution adds another dependency when the application uses hostnames. Each layer has separate state and separate failure evidence.

For IPv4 on an Ethernet link, an on-link destination normally needs a neighbor mapping from IP address to MAC address. An off-link destination needs a selected route and next-hop neighbor. A default route does not make an invalid local subnet correct, and a DNS server cannot repair a missing route.

In the reference QEMU setup, `10.0.2.15`, gateway `10.0.2.2` and DNS service `10.0.2.3` belong to the emulated user-network arrangement used in the recorded session. They are not recommended addresses for an arbitrary physical LAN. A real deployment must use its network's allocation and routing policy.

## Identify the component that owns configuration

The existing reference capture shows `systemd-networkd` selecting `/lib/systemd/network/80-wired.network`. Its meaningful settings were:

```ini
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

This is captured file content, not a new configuration applied during this revision. The command-line exclusions matter: an image booted with network-root or IP boot arguments can follow a different configuration path. A working result from one boot mode is not proof that this file always manages the interface.

Avoid running several configuration managers against the same link. DHCP clients, networkd, NetworkManager and legacy scripts can replace one another's addresses or routes. A configuration that appears briefly and disappears can be an ownership conflict rather than a driver fault.

## Persistence and runtime state are different

An `ip` operation changes current kernel state. A configuration file tells a manager what state to create later. Editing a file without reloading or reconfiguring the manager may leave the old state active. Conversely, a manual runtime change can vanish when the manager reapplies policy.

The reference experiment temporarily installed a networkd file named `10-eth0-static.network`, reloaded the manager and reconfigured `eth0`. The captured status then identified that file as the selected network configuration. Its address was `10.0.2.15/24`, with gateway `10.0.2.2` and DNS `10.0.2.3`.

The earlier file name matters because networkd selects the first matching network file in its ordering rules. A more specific file that sorts later may never be selected. Read the selected file path from status rather than assuming a file took effect because it exists. [systemd network-file rules](https://github.com/systemd/systemd/blob/v251/man/systemd.network.xml).

## Read routes as decisions

The recorded static configuration produced these relevant lines:

```text
default via 10.0.2.2 dev eth0 proto static
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15 metric 10
```

The connected route covers addresses in `10.0.2.0/24`. The default route covers destinations without a more specific route. The source address and outgoing interface also matter, especially when a board has Ethernet, USB networking, a bridge or a VPN at the same time.

For an original example, two interfaces can each receive a default route. Metrics help choose between otherwise comparable routes, while more specific prefixes win before that comparison. A service bound to one local address can still send replies through an unexpected path if routing policy is incomplete.

Do not diagnose every failed hostname connection as DNS. First establish whether the destination IP is reachable through the intended path. Then inspect resolver configuration and the actual answer. Finally inspect the application port, listening address and filtering rules.

## A capture proves a bounded exchange

The saved capture contains:

```text
12:48:41.917904 IP 10.0.2.15 > 10.0.2.2: ICMP echo request, id 1069, seq 0, length 64
12:48:41.918815 IP 10.0.2.2 > 10.0.2.15: ICMP echo reply, id 1069, seq 0, length 64
```

A second request/reply pair followed. The report counted four captured packets and no kernel capture drops. This proves that exchange and the capture tool's observation. It does not prove internet reachability, DNS, TCP service availability or long-term loss rate.

The session also tried to use `timeout`, but the target reported that the command was absent. Minimal images do not necessarily include every host utility. Preserve such failures in evidence rather than rewriting the transcript into an idealized successful procedure.

## Verify recovery instead of assuming it

After removing the temporary static file, the capture shows networkd selecting the original `80-wired.network` again. However, the immediately printed first route line was the connected subnet route, not a default route. That record proves file selection changed; it does not prove that DHCP had fully restored gateway and DNS state at that instant.

A complete restoration check would observe the address, default route, resolver state and a representative connection after the manager settles. This distinction is important in automated tests: a successful reload command is not an end-to-end connectivity result.

For production images, install configuration through a tracked recipe or project overlay. Record stable interface matching rules suitable for the board. Interface names and generated MAC addresses can change between emulation and hardware, so matching only `eth0` may be too weak for multi-interface products.

## Diagnose from a concrete symptom

Link down points below IP configuration. An address without a route points to manager or route policy. An incomplete neighbor entry points to the local segment, VLAN or peer availability. IP reachability with hostname failure points to resolution. A reachable host with refused TCP connections points to service state or binding; silent timeouts also require filtering and return-path checks.

When changing remote access settings, preserve an independent console and a rollback path. A configuration can disconnect the session before you can inspect the result. Treat the final persistent configuration and restored access as part of the change's acceptance criteria.

> [!NOTE]
> **Not run on the reference setup during this revision:** new network reconfiguration. The section analyzes existing QEMU captures; physical LAN, multi-interface and reboot-persistence tests remain open.

## References

- Existing `reference-setup/captures/cap-wp01-net.txt` and `cap-wp01-net2.txt`, inspected locally.
- [systemd-networkd documentation](https://github.com/systemd/systemd/blob/v251/man/systemd-networkd.service.xml), configuration ownership; the reference image reports systemd 251.8.
- [iproute2 project](https://git.kernel.org/pub/scm/network/iproute2/iproute2.git/), route and link inspection tools.

---

<sub>← [Ethernet (GEM)](01-ethernet.md) · [Chapter index](README.md) · [USB Host and Gadget](03-usb.md) →</sub>
