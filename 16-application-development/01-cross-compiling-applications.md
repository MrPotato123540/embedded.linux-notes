# Cross-Compiling Applications

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Use the image's development environment

Load the matching SDK environment before building. It selects the cross-compiler, target sysroot and flags. Preserve these settings in Make or use the supplied CMake toolchain integration. `pkg-config` must search target metadata, not the host's libraries.

A successful link can still produce an unusable program if the loader or shared-library versions differ on the target. Inspect the executable architecture and required libraries, then run it on the release image.

## Recipe integration

For repeatable deployment, build the application through a recipe and include its package in the image. Keep compiler options, source revisions and configuration under version control. Direct copying is useful for an experiment but does not update the image manifest.

The earlier cross-compilation chapter includes captured tests. Reuse that setup before adding large frameworks or hardware access.

## The target ABI is a chain of agreements

The Application Binary Interface (ABI) defines details such as register use, data layout, symbol naming and executable loading. For a Linux application, the contract includes the instruction set, word size, libc, dynamic loader and every linked library. Choosing an Arm compiler is only the first step.

An SDK sysroot is a controlled view of target headers and libraries. The compiler searches it when building and linking. It is not the target's live filesystem, and changes installed manually on a board do not automatically appear in it. Rebuild or update the SDK when the supported development contract changes.

The build machine also runs tools during compilation. A code generator must execute on the host, while the generated application executes on the target. Confusing these roles can make a build try to run an AArch64 helper on an x86-64 host. Yocto's native and target recipe variants express this separation.

## Follow one executable to `main()`

The source is compiled into target object files. The linker resolves symbols against target libraries and writes ELF metadata. For a dynamic executable, `PT_INTERP` names the loader. On execution, the kernel maps the executable and interpreter; the interpreter loads shared objects, performs relocations and transfers control through runtime startup to the application's `main()`.

The supplied BSP gives a concrete example. Its `/bin/bash.bash` is AArch64 ELF64 and requests `/lib/ld-linux-aarch64.so.1`. Its recorded library requirements include `libtinfo.so.5` and `libc.so.6`. The artifact was inspected with `readelf` on the host without executing it.

If that loader is missing, the kernel can report a missing-file error even though `bash.bash` is present. If the loader exists but `libtinfo.so.5` is absent, failure happens during shared-library loading. If the library has the right filename but lacks a required symbol version, the ABI still fails. These are three different points in the chain.

## Build systems must preserve the SDK environment

A Makefile that assigns a fixed host compiler can override the SDK's target compiler. A CMake project that ignores its toolchain configuration can discover host headers or libraries. A `pkg-config` lookup can return host metadata unless the environment correctly selects target paths and sysroot handling.

The local Yocto `cmake.bbclass` describes the generated cross-build settings. Application recipes should use the build class rather than reconstructing toolchain paths inside source code. This lets the same source follow the selected machine and SDK.

Check the actual compiler invocation when diagnosis is needed. The environment's intended setting is weaker evidence than the command the build system ran. A host include directory in that invocation can produce a subtle ABI mismatch even if compilation succeeds.

## A small application still has release inputs

Consider an illustrative sensor application that uses a JSON library and a device ioctl. The recipe needs the JSON development files to compile. The target package needs the runtime library when dynamically linked. The ioctl structure must match the kernel driver's userspace interface, using fixed-width fields and documented alignment.

A header copied from a newer driver can compile successfully while the older deployed driver rejects or misinterprets the request. Version the userspace interface and define how unsupported operations fail. A shared source repository does not guarantee that the kernel and application deployed together came from the same revision.

Install the binary, configuration and service unit through recipes. Include the package in the image and keep the image manifest. Copying a test binary to `/tmp` is useful for an experiment, but it does not create a reproducible deployment path.

## Static linking changes dependencies, not architecture

A static executable can avoid normal dynamic-loader and shared-library lookup at startup. It still depends on the kernel ABI and may use runtime data files, plugins or name-service behavior. Static linking is therefore not a universal promise that one binary works on every Linux image.

The supplied BusyBox executable has no interpreter or dynamic library requirements in the inspected ELF metadata, while systemd and Bash do. This difference explains why a recovery utility may survive a broken shared-library installation. It does not make the static utility independent of drivers or device permissions.

Link-time optimization, architecture tuning and floating-point/vector choices also affect deployment. Select options supported by the actual target CPU and required runtime, not by the fastest development workstation.

## Validate one boundary at a time

First inspect architecture and ELF metadata. Then verify that required runtime packages exist in the intended image. Then execute a functional test under the intended account and service environment. Only after correctness is established should you compare performance builds.

Preserve an unstripped binary or separate debug information with the release build ID. The shipped executable can be stripped for size while the host retains symbols for debugging. Rebuilding later from the same source may still produce a different binary if toolchain or dependency inputs changed.

> [!NOTE]
> **Not run on the reference setup:** a new application build and deployment for this revision. Existing cross-compilation captures remain in chapter 02; this section adds source and artifact analysis.

## References

- Inspected BSP `rootfs.tar.gz` ELF artifacts and `poky/meta/classes-recipe/cmake.bbclass`.
- [linux-xlnx@xilinx-v2024.1:fs/binfmt_elf.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/fs/binfmt_elf.c).

- [Cross-compilation and toolchains](../02-embedded-linux-concepts/02-cross-compilation-and-toolchains.md)
- Yocto 4.1.4 SDK manual

---

<sub>[Chapter index](README.md) · [Debugging Applications](02-debugging-applications.md) →</sub>
