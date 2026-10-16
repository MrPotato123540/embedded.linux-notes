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

## Follow a module from file to running code

A `.ko` is an Executable and Linkable Format (ELF) object. It contains code, data, relocation records and module metadata. It is not a separate process. Loading it adds code to the running kernel address space. A module can therefore damage the whole system through a bad pointer or wrong hardware access.

The kernel loader checks the object and resolves its references to exported symbols. It allocates memory, applies relocations and calls the module initialization function. A successful initialization moves the module into its live state. A failure must leave no registered device, timer or allocated resource behind. The loader cannot infer how to reverse arbitrary work inside a failed initialization function.

In the pinned source, follow `load_module()` and `do_init_module()` in `kernel/module/main.c`. The checks include ELF validity, symbol resolution and supported version checks. Signature handling also depends on kernel configuration and policy. A valid signature answers who signed the object; it does not prove that its code is correct or compatible with the actual PL design.

For a platform driver, module initialization normally registers the driver. Device binding is a separate event. The driver can load successfully even when no matching device exists. It may also match a device whose probe later fails. This gives three different observations: object loaded, driver registered, and device bound. Treating them as one event makes debugging much harder.

## Built-in code changes the release boundary

A configuration value of `y` links a driver into the kernel image. A value of `m` builds a loadable object when the symbol supports modules. Built-in drivers do not appear in the list of loaded modules. Their probe can still fail because clocks, regulators, interrupts or hardware are missing.

A driver needed to mount the real root filesystem must be available before that mount. It can be built in or provided by the early userspace environment. Putting the storage controller module only inside the filesystem that controller must open creates a dependency cycle. This is a boot architecture problem, not a missing startup delay.

Loadable modules make development and optional hardware support easier, but their release unit includes the target kernel configuration and exported interfaces. The filename alone is not enough. Two kernels called `6.6` can have different structures, symbol versions and vendor patches.

## Dependencies are a graph

A module may need exported symbols from another module. Userspace module tools use generated dependency information under the kernel release directory to load this graph in the right order. Directly inserting one file does not provide the same dependency resolution as loading a module by its registered name.

Device aliases form another path. The module's device table creates alias metadata; device discovery produces a matching event; userspace can request the relevant module. This explains why a manually loaded driver can work while automatic loading fails. The object and probe may be correct, but alias metadata, dependency files or the userspace event manager may be absent.

The teaching PL-ID example uses `MODULE_DEVICE_TABLE(of, pl_id_match)`. Its compatible string must match the synthetic device tree. Changing the driver's human-readable name does not repair a wrong compatible string.

## Removal is a concurrency problem

A module reference count protects code from normal unload while known users hold references. It does not replace device lifetime design. A queued work item, interrupt handler or userspace mapping can still point at driver-owned data. Before removing that data, the driver must stop new requests, stop hardware activity and wait for in-flight software paths to finish.

For a streaming device, a useful removal order is: stop accepting jobs, mask device interrupts, stop or terminate DMA, synchronize callbacks, cancel work, detach user interfaces, then release buffers and register mappings. The exact order depends on whether shutdown needs registers, clocks or an active interrupt. Write this dependency order before implementing the error paths.

Forced unload bypasses normal protections and is not a recovery design. A reproducible kernel fault after unload often means that an asynchronous user still holds a pointer. Capture the first fault and its stack; later errors may only be damage from the first one.

## Separate the common failure classes

| Evidence | Most direct next investigation |
| --- | --- |
| Module file absent from rootfs | Recipe packaging and image package selection |
| Invalid format or version complaint | Target release, architecture, configuration and symbol versions |
| Unknown exported symbol | Provider module, export policy and dependency metadata |
| Object loads, no device binds | Device tree, alias match and deferred/failed probe |
| Works until close, unload or reconfiguration | References, callbacks and shutdown ordering |

A successful host compile checks C interfaces against those host headers. It does not establish any of these target conditions. The PL-ID compile result documented later in this chapter remains a host-only check.

## References

- Pinned implementation: [linux-xlnx@xilinx-v2024.1:kernel/module/main.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/kernel/module/main.c).
- Pinned build contract: [Documentation/kbuild/modules.rst](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/kbuild/modules.rst).

- `linux-xlnx@xilinx-v2024.1:Documentation/kbuild/modules.rst`
- kmod manual pages shipped with the target packages

---

<sub>[Chapter index](README.md) · [Kernel Headers and Building Modules](02-kernel-headers-and-module-builds.md) →</sub>
