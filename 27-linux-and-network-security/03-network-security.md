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

## References

- nftables documentation; OpenSSL and mbedTLS documentation for selected versions
- [Certificate validation](../25-security-fundamentals-and-cryptography/03-pki-and-certificates.md)

---

<sub>← [SSH in Depth and Hardening](02-ssh-in-depth-and-hardening.md) · [Chapter index](README.md) · [Secure Software Updates](04-secure-updates.md) →</sub>
