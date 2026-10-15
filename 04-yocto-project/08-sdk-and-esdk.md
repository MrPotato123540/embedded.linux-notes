# SDK and Extensible SDK

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Concepts

A **Software Development Kit (SDK)** contains a cross-toolchain and sysroots that match a target software environment. The host sysroot supplies tools that run on the development machine. The target sysroot supplies headers and libraries for the board.

The standard SDK is produced by `populate_sdk`. The extensible SDK, produced by `populate_sdk_ext`, adds tools for recipe-aware development and rebuilding components. A larger SDK is not automatically the right choice: select it according to whether developers need application compilation or build-system integration.

## Using the environment correctly

The SDK's `environment-setup-*` script sets the compiler, sysroot and related flags. Build the application from a shell with that environment loaded. A compiler executable alone is not enough; library search paths, linker settings and package metadata must also match.

For Make, preserve `CC`, `CXX`, `CFLAGS` and `LDFLAGS` from the environment. For CMake, use the SDK's supplied toolchain integration where available. For Meson, use its cross-file support. An IDE must use the same compiler, debugger and target sysroot instead of silently selecting host defaults.

## Keeping the SDK and image together

Publish the SDK with the image build identifier, layer revisions and package manifest. If the image removes or changes a library, an old SDK can still compile an application that no longer runs correctly. Check runtime dependencies and application behavior on the release image.

An SDK does not include every optional development header automatically. Add the required development packages through the SDK configuration and rebuild it. Copying headers from the host can hide an ABI mismatch until runtime.

> [!NOTE]
> **Not run on the reference setup:** generation of a new standard or extensible SDK in this continuation. The earlier [cross-compilation section](../02-embedded-linux-concepts/02-cross-compilation-and-toolchains.md) contains the existing tested compiler examples.

## References

- Local BSP: `poky/meta/classes-recipe/populate_sdk_base.bbclass`, `populate_sdk_ext.bbclass`
- Yocto 4.1.4 [SDK manual](https://docs.yoctoproject.org/4.1.4/sdk-manual/index.html)

---

<sub>← [devtool Workflow](07-devtool-workflow.md) · [Chapter index](README.md) · Next chapter: [05 · PetaLinux 2024.1](../05-petalinux/README.md) →</sub>
