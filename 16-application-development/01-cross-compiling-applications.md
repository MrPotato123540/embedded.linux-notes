# Cross-Compiling Applications

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Use the image's development environment

Load the matching SDK environment before building. It selects the cross-compiler, target sysroot and flags. Preserve these settings in Make or use the supplied CMake toolchain integration. `pkg-config` must search target metadata, not the host's libraries.

A successful link can still produce an unusable program if the loader or shared-library versions differ on the target. Inspect the executable architecture and required libraries, then run it on the release image.

## Recipe integration

For repeatable deployment, build the application through a recipe and include its package in the image. Keep compiler options, source revisions and configuration under version control. Direct copying is useful for an experiment but does not update the image manifest.

The earlier cross-compilation chapter includes captured tests. Reuse that setup before adding large frameworks or hardware access.

## References

- [Cross-compilation and toolchains](../02-embedded-linux-concepts/02-cross-compilation-and-toolchains.md)
- Yocto 4.1.4 SDK manual

---

<sub>[Chapter index](README.md) · [Debugging Applications](02-debugging-applications.md) →</sub>
