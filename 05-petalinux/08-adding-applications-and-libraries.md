# Adding Applications and Libraries

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Application integration

A project application needs both a recipe and image selection. Creating a recipe makes software buildable; selecting its output package makes it part of the root filesystem.

The installed 2024.1 `petalinux-create apps --help` lists C, C++, autoconf and install templates. It also lists several DFX-specific templates. The older generic `fpgamanager` name is not the template list shown by this installation; use the actual release help.

## Recipe responsibilities

A compiled application needs source inputs, a license, build dependencies, a build step and installation into `${D}`. A CMake project should use the CMake class and honor the cross-toolchain. An install-only recipe still needs file ownership and permissions.

Libraries need correct runtime packaging and development headers. A consuming recipe names the library recipe in `DEPENDS`, so its headers and link libraries enter the consumer's sysroot. Runtime dependencies are handled separately.

For a systemd service, install the unit and use the systemd class with the correct package and service settings. Installing a unit file does not by itself prove that the service is enabled or starts successfully.

## Validation

Check four results: the binary architecture, package contents, image manifest and target behavior. Test missing configuration and service restart as well as normal startup. If using `devtool` to deploy quickly, finish by rebuilding and booting the real image.

> [!NOTE]
> **Not run on the reference setup:** creation and deployment of a new application in this continuation. Template names were checked against installed help.

## References

- Executed `petalinux-create apps --help` from PetaLinux 2024.1
- Local layers: `poky/meta/classes-recipe/cmake.bbclass`, `systemd.bbclass`
- AMD UG1144 (2024.1), adding applications and libraries

---

<sub>← [Customizing Through meta-user](07-meta-user-customization.md) · [Chapter index](README.md) · [Hardware Updates and XSA Re-Import](09-hardware-updates.md) →</sub>
