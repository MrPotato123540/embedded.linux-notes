# Network Security

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[27 · Linux and Network Security](README.md)** · Part XIV: Security

## Control network entry points

Inventory listeners and their owners. `ss` shows local sockets; an authorized external scan can show what is reachable from a particular network. A local listener list does not account for firewall, routing or address-family exposure.

Use nftables or the selected iptables backend consistently. Define allowed traffic and test both IPv4 and IPv6 where enabled. Preserve remote maintenance access while deploying a new policy, with an explicit recovery method.

## Identity and encryption

TLS requires certificate-chain and peer-identity validation, not just encryption. Mutual TLS adds client authentication and a device-credential lifecycle. Keep time synchronization and expiry handling in the design.

A VPN such as WireGuard can protect a management path, but services inside it still need authentication and least privilege. Lost device keys must be revocable without replacing the whole fleet's credentials.

> [!NOTE]
> **Not run on the reference setup:** firewall rollout, mutual TLS or VPN deployment.

## Trace a packet to the service

A packet reaches the board through an interface, routing decision, filtering path and socket. A listening socket is only one point in that path. A daemon bound to loopback is different from one bound to every address, and an IPv6 listener can create exposure that an IPv4-only review misses.

Draw the intended network roles first. A measurement device may have a control interface, a data interface and an outbound update connection. Each role needs explicit peers and protocols. Using a port number as the whole policy ignores which interface received the packet and which service actually owns the socket.

For Netfilter, packets delivered to the local host use the input path; routed packets use the forward path; locally generated packets use output. A board acting as a router or container host may use more than one. Filtering only input does not define the policy for traffic it forwards.

## Rules need hooks, order and address-family coverage

nftables organizes rules in tables and chains. A base chain attaches to a packet-processing hook. A regular chain needs a path that calls it. A carefully written chain that is never reached does not enforce anything.

The `inet` family can cover IPv4 and IPv6 rules, while protocol-specific details still need appropriate handling. Decide how loopback, established traffic, management access and required control traffic fit the policy. Do not copy an allow list without checking the system's address assignment and routing needs.

These mechanics follow the Netfilter project documentation. The reference image's manifest does not establish an installed nftables policy, and no firewall deployment was performed here. Use the selected userspace and kernel versions when validating actual syntax and feature support.

## Connection state affects policy changes

A stateful policy tracks connections so replies can be allowed without opening arbitrary inbound sessions. The state table has its own lifetime and resource cost. A test that keeps an old SSH session open may continue to work even when new SSH connections are blocked.

When changing maintenance rules, test both a fresh allowed connection and a fresh denied connection. Also test after reboot, when connection state has gone away and rule loading order may differ. A policy that becomes active only after a network service starts can leave an early exposure window.

Resource exhaustion is another concern. Limits on new connections, request size and application work serve different purposes. A packet filter can reduce unwanted traffic, but an accepted authenticated client can still request expensive operations. Apply workload limits at the application boundary too.

## IPv6 and control traffic need deliberate treatment

IPv6 neighbor discovery and path-MTU behavior depend on control messages. Blocking all ICMPv6 can break normal communication in ways that look like random connection failures. Similarly, blocking every ICMP message in IPv4 can hide useful path errors.

The correct policy depends on whether the board is a host, router or bridge and on its address-assignment method. Document that role before selecting control-message rules. Do not treat an interface with no global IPv6 address as proof that it has no IPv6 reachability.

For failure diagnosis, compare local addresses, routes, listener bindings and packet observations from the intended peer network. A successful loopback connection says little about the external path. An external scan from one subnet also says little about another interface behind different routing or filtering.

## TLS joins transport with identity

TLS protects a connection after the peers establish the required trust. The client must validate the certificate chain and the expected server identity. A certificate issued by a trusted CA for another name should fail. The host certificate lab in [PKI](../25-security-fundamentals-and-cryptography/03-pki-and-certificates.md) records exactly that distinction.

Mutual TLS adds client certificate authentication. The server still needs authorization: which device may submit data, receive updates or request an administrative action? Accepting any certificate from a fleet CA as an administrator would give every device too much authority.

Keep device identity separate from server trust anchors. One identifies the client; the other decides which servers the client trusts. They have different rotation and compromise responses. A server-CA update should not silently replace the device's private identity key.

Bootstrap time is a practical dependency. A device without valid time may reject a valid certificate or accept a time state that weakens expiry checks. Design how it obtains a trustworthy starting time and how it behaves while offline. Disabling certificate checks to make first boot work removes the property the channel was meant to provide.

## A VPN changes reachability, not service authority

A management VPN can place administration traffic on a restricted path. The endpoint still needs an allowed peer-key set, routes and firewall policy. A tunnel does not automatically restrict which services its peers may reach after packets are decrypted.

Treat a lost device or operator key as a lifecycle event. Remove its authority without replacing every unrelated identity. Keep a record connecting a VPN peer to the intended device or operator, but do not use an IP address as the only identity record.

Check the underlying transport too. The tunnel's outer packets need routing and any required firewall permission. A working tunnel handshake with failed application traffic often points to inner routing, MTU or service policy rather than failed cryptography.

## Build a useful network acceptance matrix

Test each service from an allowed management peer, a disallowed peer and the relevant address families. Repeat before and after reboot, interface reconnection and update. For TLS, include wrong identity, unknown CA and expired/not-yet-valid credentials under controlled test time.

Record which layer rejected each case. A firewall drop does not prove that the application rejects a bad certificate, because the handshake never reached it. Conversely, a TLS rejection does not prove that other unauthenticated listeners are closed. Keep the tests focused enough that their results support the exact claim being made.

## References

- [Netfilter nftables manual](https://netfilter.org/projects/nftables/manpage.html), packet-path concepts; verify syntax against the selected installed version
- [RFC 8446: TLS 1.3](https://www.rfc-editor.org/rfc/rfc8446)
- [Certificate validation](../25-security-fundamentals-and-cryptography/03-pki-and-certificates.md)

---

<sub>← [SSH in Depth and Hardening](02-ssh-in-depth-and-hardening.md) · [Chapter index](README.md) · [Secure Software Updates](04-secure-updates.md) →</sub>
