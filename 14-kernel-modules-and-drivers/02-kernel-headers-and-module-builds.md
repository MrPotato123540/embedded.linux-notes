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

## References

- Linux 6.6 [external modules](https://docs.kernel.org/6.6/kbuild/modules.html)
- Yocto kernel development manual for 4.1.4

---

<sub>← [Kernel Modules](01-kernel-modules.md) · [Chapter index](README.md) · [Adding Modules to a PetaLinux Project](03-modules-in-petalinux.md) →</sub>
