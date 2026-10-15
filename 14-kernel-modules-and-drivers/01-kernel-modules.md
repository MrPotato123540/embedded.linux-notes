# Kernel Modules

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[14 · Kernel Modules and Device Drivers](README.md)** · Part VI: Linux Kernel and Drivers

## Two independent classifications

A driver can be in-tree or out-of-tree, and built-in or loadable. In-tree describes where its source is maintained. Built-in (`=y`) means linked into the kernel; loadable (`=m`) means packaged as a module.

| Tool | Role |
| --- | --- |
| `insmod` | Load a specified module file |
| `modprobe` | Resolve module names, dependencies and configuration |
| `lsmod` | List loaded modules |
| `modinfo` | Inspect module metadata |
| `rmmod` | Request module removal |
| `depmod` | Generate dependency metadata |

Modules live under `/lib/modules/<kernel-release>`. Version magic, configuration and symbol-version checks help reject incompatible builds. Matching only the CPU architecture is insufficient.

## Loading policy

Device modaliases can trigger automatic loading through userspace device management. Module parameters configure supported behavior. Blacklisting affects particular automatic-loading paths; it is not a universal security boundary against privileged explicit loading.

Removal must stop new users and finish outstanding work. A busy module cannot safely disappear while callbacks, DMA or open files still depend on it. Taint flags record conditions such as unsupported/proprietary module use and affect diagnosis.

## References

- `linux-xlnx@xilinx-v2024.1:Documentation/kbuild/modules.rst`
- kmod manual pages shipped with the target packages

---

<sub>[Chapter index](README.md) · [Kernel Headers and Building Modules](02-kernel-headers-and-module-builds.md) →</sub>
