# Users, Passwords and Login

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[15 · Root Filesystem and Init](README.md)** · Part VII: Root Filesystem and User Space

## Build-time identity

Users, groups and login policy are part of the image. Yocto's `useradd` support suits package-owned service users; `extrausers` can apply image-wide account changes. Use stable ownership rules when persistent files survive upgrades.

The reference captures use the `petalinux` account, and the local QEMU scripts set a laboratory password. That password is a test fixture, not a production default or a recommendation. Check the release's first-login behavior on an unmodified image before documenting a factory procedure.

## Product policy

Create unique credentials or provision authorized keys through a controlled process. Keep service users separate from interactive administrators. Development autologin and empty-password settings should be explicit build variants, with a check preventing them from entering the release image.

A read-only root affects password updates and host-key storage. Provide a defined persistent location or provisioning mechanism, and test factory reset behavior.

> [!NOTE]
> **Not run on the reference setup:** pristine-image first-login policy and production credential provisioning in this continuation.

## Separate identity, authentication and authorization

A user ID identifies a process owner. Authentication proves an identity through a password, key or another mechanism. Authorization decides what that identity may access. These are separate layers: a valid login does not automatically grant access to a device, and a process can run under a service account without an interactive login.

The kernel normally evaluates numeric user and group IDs. Names in account databases are a userspace mapping. Copying a writable data partition between images with different numeric assignments can therefore give the files to the wrong service even if familiar names appear in the new image.

Choose stable IDs for persistent service data when the product's image policy requires them. Record ownership migrations with software updates. Do not solve mismatches by making an entire persistent volume writable by every user.

## Build accounts as release inputs

Yocto account-handling classes let recipes or image metadata declare users, groups and account changes. Keep those declarations in version control. A manual target-side account change is lost when the rootfs is replaced unless it belongs to an explicitly persistent account store.

A service account usually needs no interactive shell or password login. Its files, supplementary groups and runtime directories should reflect the service's actual needs. Granting a whole application root privileges because one device node has restrictive permissions hides the real integration problem.

A development image may enable convenience features that a product image must revisit. Inspect the effective image configuration and packaged files. Do not infer that the shipped BSP's login policy is suitable for an internet-connected product.

## SSH has client and server identity

A client public key can authorize a user login. A server host key identifies the machine to the client. These serve different purposes. Copying one host private key into every device makes them share server identity, even if each device has a different login password.

Generate or provision device identity according to a documented first-boot or manufacturing policy. A read-only rootfs needs a writable or protected location for persistent identity. Recreating host keys at every boot causes trust changes; cloning the same keys across devices hides device changes. Both behaviors can confuse operators and automated clients.

A key placed in an authorized-keys file also needs correct ownership and permission policy. The server may reject unsafe files even when the key text is correct. Diagnosis should distinguish network reachability, SSH negotiation, server identity validation and user authentication.

## A worked service-access boundary

Consider a telemetry service that reads a sensor and writes one database. Give it its own account, a writable state directory and group access to the sensor node. It does not need permission to update the rootfs, program FPGA images or read unrelated private keys.

If a helper performs a privileged operation, define a narrow request interface and validate inputs. A general shell command passed through a privileged helper is much harder to constrain. File capabilities can grant selected kernel privileges, but each capability still has a specific scope and must be reviewed against the executable's behavior.

Service-manager restrictions can reduce accessible paths and capabilities further. They complement Unix ownership rather than replacing it. Test the actual service under those restrictions; a program that only works when launched manually as root has not passed the intended deployment contract.

## Password storage and image handling

Passwords should not be stored as plain text in the account database. Build configuration may still expose secrets if passwords or private keys are embedded directly in recipes, logs or source history. Treat credential provisioning as a separate controlled input and avoid publishing real credentials in examples.

A password hash is also sensitive because it can be attacked offline. A common hash in every shipped device is not per-device identity. Product policy should define initial access, credential rotation, recovery and what happens after factory reset.

This guide does not invent a default password or recommend enabling remote root login. The supplied archive inspection focused on package and executable structure and did not print credential files.

## Distinguish denial from process failure

A login denial can come from authentication policy, a locked account, missing home files or a disallowed shell. A service access denial can come from file ownership, supplementary groups, a device rule or a sandbox restriction. An application that exits before touching a file may instead have a missing dynamic library.

Collect the identity and effective groups of the failing process, the path's ownership, and the service's applied restrictions. Compare those with the intended policy. Avoid using a broad permission change as the final fix merely because it makes the symptom disappear.

> [!NOTE]
> **Not run on the reference setup:** account provisioning, key rotation and remote login policy changes. Those operations were not needed for the read-only documentation verification.

## References

- Inspected BSP Poky account classes under `components/yocto/layers/poky/meta/classes/` and `meta/classes-recipe/` (`useradd`, `extrausers` integration).
- [systemd v251:systemd.exec.xml](https://github.com/systemd/systemd/blob/v251/man/systemd.exec.xml), service users, groups and execution restrictions.

- Local BSP: `poky/meta/classes/extrausers.bbclass`, useradd classes
- AMD UG1144 (2024.1), rootfs user configuration
- Reference QEMU setup notes

---

<sub>← [Device Management: devtmpfs, udev and mdev](08-device-management-and-udev.md) · [Chapter index](README.md) · Next chapter: [16 · Application Development](../16-application-development/README.md) →</sub>
