# Linux System Hardening

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[27 · Linux and Network Security](README.md)** · Part XIV: Security

## Reduce authority and exposure

Run services under dedicated users and grant only required capabilities. Remove unused services and writable paths. A small image helps review, but required updates, diagnostics and recovery still need support.

Mandatory access control systems such as SELinux, AppArmor and SMACK enforce additional policy. The selected kernel, userspace and policy must work together. Adding `meta-security` alone does not create an enforced product policy.

## Kernel and filesystem policy

Review address randomization, stack protection, module policy and relevant sysctls against the actual kernel configuration. Test restrictions with the product workload so developers do not later disable them broadly to fix one permission error.

A read-only root limits persistent system changes. It does not prevent a privileged process from accessing every exposed device or network service. Protect mutable configuration and secrets separately.

## Acceptance tests

Verify that the service can perform its required work and cannot access unrelated files/devices. Repeat after an upgrade and factory reset. Keep the selected policy in version control.

## References

- Linux 6.6 security and kernel self-protection documentation
- Yocto 4.1.4 security guidance and the shipped `meta-security` layer

---

<sub>[Chapter index](README.md) · [SSH in Depth and Hardening](02-ssh-in-depth-and-hardening.md) →</sub>
