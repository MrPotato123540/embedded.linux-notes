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

## Separate source integration from image integration

A new application recipe makes the source available to the build system. Its tasks must compile and stage the program. Packaging must then assign the files to output packages. Image configuration must select those packages. Finally, the deployed system must provide the runtime environment the application expects.

The creation tool can generate a starting recipe and enable a selection, but it cannot infer every dependency or product policy. Review the generated recipe before building. Identify the source revision, license, build system, installed paths and runtime requirements explicitly.

The installed 2024.1 application help includes an `install` template for content that does not need compilation. This is useful for scripts or data, but such content still needs package ownership, permissions and dependency declarations. A shell script can depend on commands absent from a minimal image even though no compiler is involved.

## Build a library and its consumer correctly

Suppose `sensor-service` calls a library supplied by `libsensor`. The service recipe declares a build dependency on the library recipe. This lets OpenEmbedded prepare the headers and link-time files in the service's recipe sysroot. The compiler should consume those files through the configured sysroot, not through an absolute path in another recipe's work directory.

At runtime, the service needs the appropriate shared-library package. Packaging can discover many ELF library dependencies automatically. Explicit dependencies are still needed for relationships that ELF analysis cannot see, such as a helper executable called by name or a plugin selected from configuration.

Development headers and unversioned linker symlinks usually belong to a development package. The target runtime generally needs the versioned shared object and its runtime links. Inspect the actual package split rather than assuming the recipe name identifies every output package.

For a prebuilt library, check architecture, ABI, dynamic dependencies and license terms. A file named `.so` can be a linker script, a real shared object or a link. Disabling all package quality checks to force it into an image can hide the exact mismatch you need to diagnose.

## Preserve the cross-build environment

Use the class matching the upstream build system where possible. CMake, Autotools and Meson need a clear distinction between tools executed on the build host and programs produced for the target. A configure step that tries to run an Arm executable on the workstation needs proper cross-build handling.

A hand-written Makefile should accept the supplied compiler and flags. It should install into the destination staging directory. Hard-coded host paths and compiler names make builds depend on the workstation and can accidentally produce the wrong architecture.

Generated code adds another dependency. If a generator runs during the build, it must be available in the host/native context even when its output is target source. If the generated header is required before compilation, the task dependencies must express that order.

## Make service startup part of the package contract

A service needs an executable, configuration, a runtime identity and any writable directories. The service manager also needs ordering and restart policy appropriate to the application. “After the network” is not a complete definition of when a remote dependency is reachable; applications still need retry and failure handling.

For a systemd integration, install the unit through the recipe and declare the relevant service/package settings. Check whether the image uses systemd before relying on that class behavior. A unit file present on disk does not prove that it is enabled, that its executable path is correct or that it can access its hardware.

Run the service with the permissions it needs. If it accesses a device node, define device ownership or another supported access path. Avoid making the service root only to hide an unexplained file-permission problem. Some operations do require privilege, but the requirement should be explicit.

## Test failure behavior as well as startup

For a sensor application, test missing hardware, invalid configuration, device removal where supported, process restart and repeated startup. Check how it releases file descriptors and buffers on failure. An application that works once can still leak resources or leave the device in a state that breaks the next run.

Separate an application crash from a service-manager restart loop. Preserve the first failure message and, when available, matching symbols and a core dump. A restart policy can improve recovery, but it can also hide the original error beneath repeated log messages.

## Confirm the delivered image

Inspect the executable architecture and interpreter, package file list, image manifest and deployed file. Then test a clean image containing only declared dependencies. This catches manual target changes that made a development deployment work accidentally.

The application help and supporting classes were inspected locally. No new application was created, built or deployed in this writing pass. The procedure describes the engineering checks required before claiming that integration is complete.

## References

- Executed `petalinux-create apps --help` from PetaLinux 2024.1
- Local layers: `poky/meta/classes-recipe/cmake.bbclass`, `systemd.bbclass`
- AMD UG1144 (2024.1), adding applications and libraries

---

<sub>← [Customizing Through meta-user](07-meta-user-customization.md) · [Chapter index](README.md) · [Hardware Updates and XSA Re-Import](09-hardware-updates.md) →</sub>
