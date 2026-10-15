# SSH in Depth and Hardening

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[27 · Linux and Network Security](README.md)** · Part XIV: Security

## Three SSH checks

SSH first establishes protected transport and verifies the server identity through its host key. It then authenticates the user. Trusting a user key does not replace checking the server's host key.

For OpenSSH, review `PubkeyAuthentication`, `PasswordAuthentication`, `KbdInteractiveAuthentication`, `PermitRootLogin` and any `Match` blocks. Key-only access requires accounting for all enabled authentication paths. Dropbear uses a different configuration interface.

## Safe rollout

Install and test authorized keys before disabling the previous login method. Validate configuration syntax and keep a controlled recovery path. Inspect the effective configuration because includes and conditional blocks can change the result.

SSH certificates can simplify large fleets by trusting a CA, but require principal, expiry and revocation policy. Protect host keys and avoid cloning one private host key into every device.

Rate limiting and network restrictions reduce exposure. They do not compensate for a leaked private key or an unmaintained daemon.

> [!NOTE]
> **Not run on the reference setup:** production SSH policy rollout or fleet certificate management.

## References

- [OpenSSH sshd_config manual](https://man.openbsd.org/sshd_config), checked against the installed version before use
- [Captured SSH basics](../01-linux-fundamentals/07-ssh.md)

---

<sub>← [Linux System Hardening](01-linux-hardening.md) · [Chapter index](README.md) · [Network Security](03-network-security.md) →</sub>
