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

## Start from a service's real authority

Consider a network-facing measurement service. It needs to read one device, write results to one directory and send reports to one endpoint. It does not need to load kernel modules, change the network setup or read another service's credentials. That difference should appear in the process user, group membership, file access and device policy.

A dedicated user is the first boundary. Linux capabilities split some traditional root privileges into named rights, but a capability can still be broad. Granting a large capability to avoid understanding one permission failure can restore much of the authority you intended to remove.

An already-open file descriptor is also authority. If a privileged launcher opens a device and passes its descriptor to a restricted service, changing the service's UID does not close that descriptor. Review inherited descriptors, supplementary groups and helper processes, not only the account name in a service file.

## Separate mechanisms by what they enforce

| Mechanism | Main decision | Important limit |
| --- | --- | --- |
| User/group permissions | Whether the process may access an object | Broad groups can expose unrelated devices |
| Capabilities | Whether a privileged operation is allowed | Some capabilities cover many operations |
| Namespaces and mount restrictions | Which resources the process can see or modify | They depend on the kernel and service setup |
| Seccomp | Which system calls and scalar arguments are allowed | It is not a full file-path or application-data policy |
| Linux Security Modules | Whether an operation meets the loaded policy | A compiled-in framework needs a deployed, enforced policy |
| Read-only filesystem | Whether storage paths can be changed normally | It does not constrain all memory, devices or network authority |

Seccomp filters cannot safely act as a general parser of pointed-to user memory. Their useful role is to reduce available kernel entry points. A filter for a network daemon must include its startup and error paths, not only the calls observed during a short happy-path trace.

## Apply systemd restrictions as a service design

The inspected rootfs contains systemd 251.8. The matching v251 `systemd.exec` documentation explains controls such as `NoNewPrivileges=`, `CapabilityBoundingSet=`, `ProtectSystem=`, `ReadWritePaths=` and `PrivateDevices=`. Their availability and effect depend on kernel support and how the service is launched.

`NoNewPrivileges=` prevents a process from gaining new privileges through later execution paths such as set-user-ID programs. A capability bounding set limits the available capability set. Filesystem restrictions can make most paths read-only while preserving a specific data directory. These are complementary controls, not interchangeable settings.

Hardware services need special care with private device views. If the service needs a PL character device, hiding all devices may break its function. The useful response is a narrow, documented device-access design. Running the entire service as unrestricted root is not a necessary conclusion from one failed open.

Test readiness after applying restrictions. A service can start successfully and later fail when it rotates a log, reconnects to a server or reopens a device after reset. Include those lifecycle events in validation. Keep the policy in the image build so a factory reset and update reproduce it.

## Compiler flags reduce exploit opportunities

The shipped `poky/meta/conf/distro/include/security_flags.inc` includes stack protection, format-string checks, position-independent code support and linker hardening. It selects `-fstack-protector-strong`, uses `_FORTIFY_SOURCE=2` where the optimization configuration permits it, and includes RELRO/immediate-binding linker flags.

These flags address different failure paths. Stack protection can detect some stack corruption before a function returns. Fortified library calls can add checks where the compiler knows object sizes. RELRO protects relevant relocation data after setup, and immediate binding supports the intended relocation protection. Position-independent executables allow useful address randomization when the runtime supports it.

The same file contains recipe-specific exceptions. Therefore the presence of this include file is not proof that every binary has every property. Inspect the expanded recipe flags and final ELF metadata for the program you are reviewing. A prebuilt vendor binary may have been produced outside this build policy.

Compiler hardening does not repair a use-after-free or an incorrect bounds check. Keep source fixes and negative tests as the main correction. Treat hardening as another barrier with its own compatibility and coverage limits.

## Kernel policy must match the actual image

Review the running kernel's configuration and boot arguments for module enforcement, relevant access restrictions and debugging features. A saved project fragment describes an input, while the merged `.config` describes the build. The binary that booted still needs to match that build record.

An example failure is an unsigned-module test that unexpectedly succeeds. Distinguish a permissive signing policy from loading a different kernel or testing a built-in driver. A built-in driver is not loaded through the module-signature path. [Verified boot beyond U-Boot](../26-zynqmp-hardware-security-and-secure-boot/07-verified-boot-beyond-u-boot.md) explains the surrounding trust chain.

Protect mutable configuration as carefully as executable files. A read-only binary can execute attacker-controlled plugins or read a configuration that grants broad network access. Trace the files the service trusts and define who may change them.

## Diagnose denied access without weakening the whole policy

Record the failing operation, effective user/groups, object permissions and relevant policy log. Compare a permitted operation against the denied one. An application error saying “permission denied” may refer to a device node, a directory, a capability or a security-module rule.

Change the narrowest policy element supported by that evidence, then repeat both the required operation and the forbidden-access test. Preserve negative results in the release test plan. This guide inspected the configuration mechanisms; it did not deploy or validate a production hardening policy on the target.

## References

- `xilinx-zcu106-2024.1:components/yocto/layers/poky/meta/conf/distro/include/security_flags.inc`
- `systemd@v251:man/systemd.exec.xml`
- `linux-xlnx@xilinx-v2024.1:Documentation/userspace-api/seccomp_filter.rst`

- Linux 6.6 security and kernel self-protection documentation
- Yocto 4.1.4 security guidance and the shipped `meta-security` layer

---

<sub>[Chapter index](README.md) · [SSH in Depth and Hardening](02-ssh-in-depth-and-hardening.md) →</sub>
