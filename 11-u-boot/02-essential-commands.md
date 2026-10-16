# Essential U-Boot Commands

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot


## Treat commands as observations and state changes

U-Boot commands operate on a live bootloader. Some only report state; others change RAM, hardware or persistent storage. Their availability depends on the build configuration. Use the target's own help and configuration as the final authority for supported syntax.

A reliable session records the current environment, device selection and memory plan before changing state. This is especially useful when a command succeeds but its result is not the artifact later booted. A later load can overwrite an earlier buffer, and a later command can change a variable used by the next step.

The table groups command families by their role. It is an interface map, not a transcript claiming that every command was executed on this reference image.

| Purpose | Typical commands | What the result establishes |
| --- | --- | --- |
| Identify the build | `version`, `help` | Banner/toolchain or compiled command support |
| Inspect runtime state | `bdinfo`, `coninfo`, `dm tree` | Memory/console/device-model observations |
| Inspect boot policy | `printenv`, `run` | Stored values or execution of a variable's commands |
| Inspect filesystems | `fatls`, `ext4ls` | Files visible on the selected device and partition |
| Load bytes | `fatload`, `ext4load`, `tftpboot` | A transfer into RAM, subject to its return status |
| Inspect an image | `iminfo`, `fdt` | Container or device-tree data at the selected address |
| Enter an OS | `booti`, `bootm`, `bootefi` | A format-specific handoff path |

## Read the saved network example carefully

The following commands and outputs are from the saved reference QEMU capture, not a new physical-board test:

```console
ZynqMP> version
U-Boot 2024.01 (May 14 2024 - 03:31:48 +0000)

aarch64-xilinx-linux-gcc (GCC) 12.2.0
GNU ld (GNU Binutils) 2.39.0.20220819
```

The later DHCP command obtains an address, then attempts a default boot filename and reports `TFTP error: 'File not found' (1)`. That error is at the file-service boundary. It does not mean the preceding address assignment failed.

The explicit transfer then succeeds:

```console
ZynqMP> setenv serverip 10.0.2.2
ZynqMP> tftpboot 0x200000 Image
...
Bytes transferred = 24269312 (1725200 hex)
ZynqMP> tftpboot 0x100000 system.dtb
...
Bytes transferred = 54985 (d6c9 hex)
```

The capture also shows that `printenv ipaddr serverip` did not find those variables immediately after the failed automatic transfer. Do not replace the actual output with the assumption that every successful DHCP exchange leaves the same environment state in every build.

## Convert transfer sizes into memory ranges

For the recorded raw kernel load, `0x200000 + 0x1725200 = 0x1925200`. Thus, the transferred file occupies `[0x200000, 0x1925200)` before any later move or additional runtime allocation. The DTB occupies `[0x100000, 0x10D6C9)` at that point.

These two recorded buffers do not overlap. That calculation still does not prove the complete boot layout is safe. The kernel header can require more runtime space than the file contains, a compressed image needs decompression space, and U-Boot may relocate the DTB or initramfs.

Use end-exclusive ranges consistently: the end is the first byte outside the object. This makes overlap checks easier and avoids subtracting one from every size calculation.

## Device selection is part of every storage command

A storage command identifies an interface, device and often a partition. A visible file on one card or partition does not prove the boot script selected that same location. Device numbering can also differ from Linux's names.

If a load reports “file not found,” first confirm the selected device, partition and filesystem. If filesystem listing works but the transfer fails, inspect the file size and read path. If the controller cannot initialize, investigate clocks, reset, pins and the device itself before changing the filename.

The same separation applies to network boot: link readiness, address configuration, route/server reachability, server path and file transfer are separate conditions. A successful ping proves an ICMP exchange; it does not prove that the TFTP root contains the desired kernel.

## Environment commands have different lifetimes

`printenv` reports values, `setenv` changes the current environment, and `run` executes commands stored in a variable. Persistence requires an enabled backend and a successful save operation. Do not assume a temporary change survives reset.

After a successful load, many loading paths update variables such as `filesize`. A later transfer can replace that value. A script that needs the kernel size after loading the DTB must preserve the kernel's result explicitly rather than assuming `filesize` still describes the first file.

A failed load can also leave old bytes in RAM. Gate the boot command on the current load's success. Otherwise, a script can accidentally boot a previous image and make a broken update look successful.

## Memory and hardware commands need an ownership map

Memory display commands can be useful for ordinary RAM buffers, but memory-mapped device reads can have side effects. Some status registers clear on read or require a specific access width. Use the peripheral specification before treating all physical addresses as passive bytes.

> [!WARNING]
> Memory writes, memory tests, flash erase/write operations and writable USB mass-storage export can destroy live software or persistent data. Establish the exact target range and recovery method before using them.

In particular, a broad memory test can overwrite U-Boot's relocated code, stack, heap, loaded images or resident firmware. A test range that excludes only the original ELF load address is not sufficient after relocation.

## Build a useful failure record

Record the command, complete error, selected device, relevant environment values, destination address and transferred size. For an image problem, add the format inspection. For a handoff problem, add the last message and the kernel/DTB identities.

This evidence separates command syntax errors from transport failures and separates valid transfers from invalid boot contracts. Repeating the same load with a different address is useful only when the new address addresses an identified overlap or placement constraint.

## References

- Saved `reference-setup/captures/cap-wp01-uboot.txt`.
- [U-Boot 2024.01 command documentation](https://docs.u-boot.org/en/v2024.01/usage/index.html), command-specific behavior and build dependencies.
- `u-boot-xlnx@xilinx-v2024.1:cmd/booti.c`, `arch/arm/lib/bootm.c` and `env/env.c`.

---

<sub>← [U-Boot Overview](01-u-boot-overview.md) · [Chapter index](README.md) · [Environment, boot.scr and uEnv.txt](03-environment-and-boot-scripts.md) →</sub>
