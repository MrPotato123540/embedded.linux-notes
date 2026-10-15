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

## References

- Local BSP: `poky/meta/classes/extrausers.bbclass`, useradd classes
- AMD UG1144 (2024.1), rootfs user configuration
- Reference QEMU setup notes

---

<sub>← [Device Management: devtmpfs, udev and mdev](08-device-management-and-udev.md) · [Chapter index](README.md) · Next chapter: [16 · Application Development](../16-application-development/README.md) →</sub>
