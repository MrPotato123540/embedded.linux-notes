# Kernel Headers and Building Modules

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[14 · Kernel Modules and Device Drivers](README.md)** · Part VI: Linux Kernel and Drivers

## Headers serve different users

Userspace API headers describe interfaces available to applications. They do not provide the complete internal kernel build environment needed by a driver module. `linux-libc-headers` therefore cannot replace the matching kernel source/build tree.

An external module needs the configured kernel tree, generated headers, build scripts and, when required, matching symbol-version information. `kernel-devsrc` can supply development source in a Yocto environment, but preparation and configuration still matter.

## Kbuild relationship

A module Makefile declares its object through `obj-m`. Kbuild then compiles it using the kernel's rules. Do not compile a `.c` file with the application compiler flags and rename the result `.ko`.

The SDK cross-toolchain must target the same architecture and a compatible kernel build. On-target compilation also needs the full build prerequisites and sufficient storage; it is not inherently more correct than cross-compilation.

## Validation

Inspect module metadata, unresolved symbols and the target kernel release before loading. Preserve the kernel configuration and source revision with the module package. A successful compile does not establish binary compatibility.

> [!NOTE]
> **Not run on the reference setup:** an external module build/load cycle in this continuation.

## A kernel build tree is more than an include directory

Userspace headers describe the system call interface. A kernel module needs the kernel's internal headers and generated build state. That includes the selected configuration, architecture-generated definitions, compiler settings and exported symbol information. Copying `/usr/include/linux` into a project does not provide a module build environment.

An external module enters Kbuild through its external-module directory. Kbuild supplies the kernel flags and architecture rules, then performs the module post-processing step. That step checks exported references and creates metadata. Calling a C compiler directly may produce an ELF file, but it does not reproduce this pipeline.

`Documentation/kbuild/modules.rst` in the pinned tree explains an important limit: the `modules_prepare` target does not build `Module.symvers`, even when symbol versioning is enabled. A full matching kernel build is then needed. Preparing headers and building the kernel are different levels of evidence.

## Read the teaching Makefile

The [PL-ID Makefile](examples/pl-id/Makefile) has one Kbuild declaration: `obj-m` names the module object. Kbuild compiles the matching C file, creates module metadata and links the final `.ko`. For a module with several C files, a separate list of component objects describes the combined module. The public module name need not equal every source filename.

The source itself uses Linux interfaces such as `devm_platform_ioremap_resource()`, `sysfs_emit()` and `module_platform_driver()`. Whether they exist and have the expected types depends on the target tree. A newer host kernel may accept a source file that the older vendor tree rejects. The reverse can also happen when vendor patches add an interface.

The existing host build used Linux 6.8.0-138 headers and an x86-64 compiler. It proves that the teaching source passes that build's compiler and module processing. It does not produce an Arm64 object. There is no valid conversion step that changes an x86-64 `.ko` into an Arm64 `.ko`; rebuild the source for the target.

## Four identities must agree

| Identity | What must be preserved |
| --- | --- |
| Source identity | Vendor tree revision and local patches |
| Build identity | Configuration, generated files, symbol versions and release string |
| Toolchain identity | Target architecture, compiler family and relevant ABI options |
| Deployment identity | Kernel image and the matching `/lib/modules` contents |

The module's version magic is an early compatibility check. It is not a proof of complete binary compatibility. Disabling or forcing past a check removes evidence; it does not fix a changed structure layout or calling convention.

With symbol versioning, exported interfaces carry checksums derived from type information. A module built with stale symbol data can fail even when the kernel release string looks right. Conversely, a configuration change may affect behavior without producing the exact diagnostic you expected. Keep the kernel build artifacts with the module release.

## Follow the PetaLinux recipe's real build inputs

In the supplied BSP, `poky/meta/classes-recipe/module.bbclass` inherits `module-base` and `kernel-module-split`. It passes `KERNEL_SRC` using `STAGING_KERNEL_DIR`, and passes `O` using `STAGING_KERNEL_BUILDDIR`. This separation matters: source and generated build output need not share one directory.

The class also removes ordinary userspace `CFLAGS`, `CPPFLAGS`, `CXXFLAGS` and `LDFLAGS` before invoking the module Makefile. Kernel compilation has its own flags. A custom Makefile that silently uses host `/lib/modules` paths or a fixed `gcc` bypasses that contract.

For inter-module dependencies, the class builds `KBUILD_EXTRA_SYMBOLS` from suitable kernel-module dependencies and their staged `Module.symvers`. This supports symbol checking between separately built modules. Merely placing both source directories next to each other does not establish that dependency.

## Diagnose at the earliest failed stage

A missing generated header means the build environment is incomplete or points at the wrong output tree. An implicit declaration often means the source expects a different API or omitted a required header. A module post-processing unresolved-symbol error means compilation succeeded but the export contract failed. An invalid-module-format error occurs later, when the target loader checks the produced object.

Keep these stages separate in reports. “The module does not work” loses the distinction between a Makefile problem and a target ABI problem. Record the exact failed task, first useful diagnostic and selected kernel source revision.

Build warnings need their own interpretation. The host test's compiler-version warning is recorded because reproducibility matters. Its missing-`vmlinux` warning prevented BPF Type Format generation; that did not mean compilation failed. It also did not verify the target's BTF configuration.

> [!NOTE]
> **Not run on the reference setup:** rebuilding PL-ID through the PetaLinux 2024.1 target kernel and installing its Arm64 module package. The host result is not used as a substitute.

## References

- [linux-xlnx@xilinx-v2024.1:Documentation/kbuild/modules.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/kbuild/modules.rst).
- Inspected BSP classes: `components/yocto/layers/poky/meta/classes-recipe/module.bbclass` and `module-base.bbclass`.

- Linux 6.6 [external modules](https://docs.kernel.org/6.6/kbuild/modules.html)
- Yocto kernel development manual for 4.1.4

---

<sub>← [Kernel Modules](01-kernel-modules.md) · [Chapter index](README.md) · [Adding Modules to a PetaLinux Project](03-modules-in-petalinux.md) →</sub>
