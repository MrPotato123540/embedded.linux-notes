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

## An SDK is a compatibility boundary

Application compilation depends on more than the processor instruction set. It also depends on the C library, exported headers, library ABI, dynamic loader and selected library features. A toolchain that produces valid AArch64 instructions can still produce an application that does not run on the target image.

The SDK packages these assumptions into a development environment. Its host-side tools run on the developer's computer. Its target sysroot contains the headers and libraries used to compile and link target programs. These two trees must not be mixed. A host executable may inspect target files, but that does not make a target library suitable for linking the host tool itself.

The environment setup script sets compiler variables and related paths so build tools use the intended context. Some compiler variables contain both an executable and arguments. Treating the entire value as a single filesystem path can break a custom build wrapper. Let the supported build system consume the environment in its documented form.

## Follow a dynamically linked application

During compilation, headers describe types, functions and constants. During linking, libraries resolve symbols and contribute ABI requirements. On the target, the ELF interpreter loads the program and its shared-library dependencies. Each stage can fail independently.

Suppose a program builds successfully but the target says the file cannot be found even though it exists. One possible cause is that the ELF interpreter named in the program is absent. This is different from an ordinary missing application file. Inspect the executable format and interpreter before changing permissions or copying more libraries at random.

Suppose the loader finds all libraries but reports an unavailable symbol version. The SDK and image may have different library versions. A successful link against the SDK proves only that the SDK satisfies the program. It does not prove the release image supplies the same ABI.

Suppose the application starts but a feature fails. A library may have been built without an optional backend, or runtime data and plugins may be missing. Compare build features and runtime package content as well as library filenames.

## Make, CMake and package discovery

A Makefile should accept the compiler and flags supplied by the SDK. Hard-coding `gcc` can select the host compiler. Replacing `CFLAGS` or `LDFLAGS` can drop architecture, sysroot, hardening or reproducibility settings. A project that needs additional flags should add them in a way that preserves the environment's requirements.

CMake separates the system running the build from the system receiving the program through its toolchain configuration. The SDK's integration describes the compiler and search behavior. Without it, a successful host build can be mistaken for a target build. Inspect the compiler and discovered library paths in the generated build configuration.

`pkg-config` is another common boundary. The executable runs on the host, but its search must find target `.pc` files. If it discovers workstation metadata, it may supply host include or library paths. Fix the package search context rather than copying those paths into the project.

An IDE adds another layer of cached settings. After changing SDKs, verify the selected compiler, debugger, sysroot and configuration cache. The terminal and IDE can build the same source with different toolchains even when both display the same project name.

## Standard SDK and extensible SDK

A standard SDK is suitable when developers primarily compile applications against an agreed image environment. The image team owns changes to the supplied libraries and SDK package set. Developers consume that environment and deliver applications with known runtime requirements.

An extensible SDK adds recipe-aware development facilities and a controlled way to build or update components. It is useful when application work also requires modifying dependencies or integrating recipes. It needs its own maintenance policy: the available components, updates and source access must match the product workflow.

The difference is not simply installer size. Ask who is allowed to change dependencies, how changes return to the product layer, and how a release build reproduces them. An eSDK workspace that never returns its changes to maintained metadata has the same integration problem as an ordinary untracked source tree.

## Construct the SDK from image requirements

The SDK must contain development material for the target APIs used by applications. A runtime package can provide a shared object without providing the headers or linker symlinks needed by developers. Conversely, a development package in the SDK does not imply that all runtime packages are installed in the image.

When a header is missing, identify the package that owns it and update SDK configuration. Do not fill the gap with workstation headers. They may describe a different library version or architecture. For generated headers, ensure the SDK contains the target configuration's result rather than an upstream template.

Publish the SDK with an image identifier, package manifests, layer revisions and relevant configuration. Keep the installer checksum so the exact SDK can be identified later. When the image changes its ABI or optional features, rebuild and retest the SDK relationship.

## Validation that reaches the target

A useful SDK acceptance test compiles a representative application, inspects its architecture and dynamic dependencies, installs it into a clean release image and exercises the APIs it uses. Include a program that touches the libraries most important to the product, rather than only a program that prints a line.

Cross-debugging also needs matching symbols and source. Keep unstripped debug information associated with the deployed executable. A debugger connected successfully to the target can still show misleading stack frames if its symbols belong to another build.

**Source trail:** local `poky/meta/classes-recipe/populate_sdk_base.bbclass`, `populate_sdk_ext.bbclass`, `toolchain-scripts.bbclass`, and `poky/scripts/lib/devtool/sdk.py`. The earlier cross-compilation chapter contains executed examples. A newly generated SDK and target acceptance run are still required for this expanded procedure.

## References

- Local BSP: `poky/meta/classes-recipe/populate_sdk_base.bbclass`, `populate_sdk_ext.bbclass`
- Yocto 4.1.4 [SDK manual](https://docs.yoctoproject.org/4.1.4/sdk-manual/index.html)

---

<sub>← [devtool Workflow](07-devtool-workflow.md) · [Chapter index](README.md) · Next chapter: [05 · PetaLinux 2024.1](../05-petalinux/README.md) →</sub>
