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

## Follow the connection in order

An SSH connection has several stages: reach the daemon, negotiate protected transport, authenticate the server, authenticate the user, authorize the requested session and start its program. A failure at one stage should not be “fixed” by weakening another stage.

For example, a changed host-key warning concerns server identity. Adding a user public key to `authorized_keys` does not resolve it. Verify whether the board was reprovisioned, whether its address changed to another device, or whether an unexpected endpoint is answering. Update the trusted host identity only after establishing which case occurred.

After server identity succeeds, user authentication proves possession of an allowed credential. Session authorization then controls shell access, commands and forwarding. A key accepted for authentication should not automatically receive every SSH feature if it is intended only for an automated maintenance job.

## Inspect the release actually shipped

The reference `rootfs.manifest` lists `openssh`, `openssh-sshd` and related packages at version 9.0p1. Its build metadata is `poky/meta/recipes-connectivity/openssh/openssh_9.0p1.bb`. This is an inventory observation, not a claim that the unmodified 2024.1 image meets a current production security baseline.

The inspected recipe input `openssh/sshd_config` contains an early include for `/etc/ssh/sshd_config.d/*.conf`, an explicit `.ssh/authorized_keys` path and `KbdInteractiveAuthentication no`. Many other lines are commented examples. A commented line is not an active assignment, and a recipe input is not proof of the final runtime file.

OpenSSH generally uses the first obtained value for a keyword, with conditional processing affecting connection-specific settings. Do not assume that appending a later line overrides an earlier include. Inspect the effective result for the intended user and source address, especially when `Match` blocks are present.

## Define a key-only policy precisely

Public-key authentication, password authentication and keyboard-interactive authentication are separate paths. PAM can participate in account/session handling as well as authentication, depending on the build and configuration. Disabling one password-looking option does not prove that every password-based path is gone.

Write the intended result first: which accounts may log in, which authentication methods they may use and whether root may log in directly. Then map that policy to the installed OpenSSH version. Dropbear has a different interface, so do not copy OpenSSH directives into a Dropbear service.

For automation, limit what the accepted key can do. A forced command or certificate/key restrictions can reduce session authority, but the called program still needs input validation. A restricted command that passes untrusted arguments to a shell can undo the restriction.

## Host identity must be unique and persistent

A shared rootfs image should not distribute one private host key to every device. Generate or provision each unit's host identity through a controlled process, then preserve it across normal updates. Otherwise one compromised unit can impersonate another, or every upgrade causes host-key warnings that users learn to ignore.

First boot also needs entropy and writable storage at the time keys are created. A service-ordering mistake can start SSH before key generation finishes. A read-only-root design needs an explicit persistent location and permissions for host identity.

Factory reset policy must say whether host identity is retained or replaced. If it is replaced, the management system needs an authenticated way to learn the new identity. A fleet cannot safely treat every changed fingerprint as expected merely because devices sometimes reset.

## Certificates reduce distribution work, not policy work

SSH certificates let a CA authorize user or host keys with principals and validity limits. They use OpenSSH's certificate format, which is different from X.509 certificates used by TLS. A TLS certificate file is not directly an SSH user certificate.

For a fleet, define principals that correspond to intended users or device identities. A broadly trusted CA with unrestricted principals can grant much wider access than a per-device key list. Protect the CA signing operation and keep issuance records with the certificate's purpose and lifetime.

Expiry depends on a meaningful clock. Revocation also needs a distribution path to disconnected devices. A short certificate lifetime helps only if devices have trustworthy time and the maintenance workflow can renew credentials. Test those conditions during network loss and recovery.

## Roll out without losing the only maintenance path

Install the intended public keys and verify a new independent connection before removing the old method. A session already open may survive even though no future session can authenticate. Test a fresh connection as the exact maintenance user from the intended network.

Validate the candidate configuration with the installed daemon, inspect its connection-specific effective policy and then perform a controlled reload. The host used for this revision has no `sshd` binary, so no syntax-check or effective-policy output is claimed here. The earlier [SSH chapter](../01-linux-fundamentals/07-ssh.md) contains the actual captured reference connection.

Keep an approved serial or service recovery path during rollout. Its authority must match the product threat model. After the new policy works, test denied passwords, denied accounts, unintended forwarding and a wrong host identity as separate cases.

## Read failures at the correct layer

“Connection refused” usually places the problem before SSH authentication: no matching listener or an active rejection. A transport timeout may involve routing or filtering. A host-key mismatch occurs after reaching an SSH server. “Permission denied” during authentication needs server-side method and account evidence.

Correlate client diagnostics with server logs using time and source address. Do not print private keys or dump full credential stores into a support bundle. The goal is to identify the failed decision while preserving the secrecy of the credentials used to reach it.

## References

- [OpenSSH 9.0p1 sshd_config manual source](https://github.com/openssh/openssh-portable/blob/V_9_0_P1/sshd_config.5)
- `xilinx-zcu106-2024.1:components/yocto/layers/poky/meta/recipes-connectivity/openssh/openssh/sshd_config` and `pre-built/linux/images/rootfs.manifest`
- [Captured SSH basics](../01-linux-fundamentals/07-ssh.md)

---

<sub>← [Linux System Hardening](01-linux-hardening.md) · [Chapter index](README.md) · [Network Security](03-network-security.md) →</sub>
