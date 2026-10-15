# BSP Packaging and Reproducible Builds

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## What a BSP preserves

A **Board Support Package (BSP)** packages a project for reuse. It can include configuration, hardware assets and selected prebuilt files. It is useful for sharing a starting point, but it does not automatically capture every remote source or host dependency.

A reproducible release needs the tool version, hardware revision, layer revisions, source revisions, patches, configuration and package manifest. Record checksums for published images. Pin moving Git branches to commits in release records.

## Cache and CI policy

A continuous integration build should start from maintained inputs. Shared downloads and shared state can reduce time, but a cache-only success can hide missing sources. Periodically test a clean build against controlled mirrors.

A container can fix many host tools, but it does not remove all host dependencies. Filesystem behavior, user permissions, available memory and kernel features still matter. Keep build output owned by the intended user, and do not run the normal build as root.

## Release test

Recreate the project in a separate directory, build it, compare manifests and boot the output. Explain any binary differences before calling the build reproducible. Timestamps, build paths and uncontrolled source revisions can all affect output.

> [!NOTE]
> **Not run on the reference setup:** BSP export/reimport and a second clean build. Packaging a BSP alone is not evidence of reproducibility.

## References

- AMD UG1144 (2024.1), BSP packaging and build mirrors
- Yocto 4.1.4 [reproducible builds](https://docs.yoctoproject.org/4.1.4/test-manual/reproducible-builds.html)

---

<sub>← [Hardware Updates and XSA Re-Import](09-hardware-updates.md) · [Chapter index](README.md) · [Yocto Without PetaLinux](11-yocto-without-petalinux.md) →</sub>
