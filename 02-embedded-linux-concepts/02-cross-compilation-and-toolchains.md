# Cross-Compilation and Toolchains

> **Applies to:** PetaLinux 2024.1 · Vitis 2024.1 · Zynq UltraScale+ MPSoC

**[02 · Embedded Linux Concepts](README.md)** · Part I: Foundations

## In short

- A **cross compiler** runs on the x86-64 host and produces code for the target's CPU. Its name carries a **target triplet** such as `aarch64-xilinx-linux` (Linux on Arm64) or `aarch64-xilinx-elf` (bare metal).
- A toolchain is more than `gcc`: binutils, a **C library**, **kernel headers** and a debugger, all built for the same target.
- Every cross compiler links against a **sysroot**: a copy of the target's headers and libraries. Its C library must match the target's, or programs fail with symbol-version errors at runtime.
- A ZynqMP project uses up to four toolchains at once: Linux on the A53, bare metal on the A53 (FSBL), bare metal on the R5 and on the PMU's MicroBlaze.

## Concepts

### Build, host and target

GNU tools distinguish three machines:

| Term | Meaning | For a cross compiler on the reference setup |
| --- | --- | --- |
| build | Where the compiler itself was compiled | x86-64 |
| host | Where the compiler runs | x86-64 (your development PC) |
| target | What the generated code runs on | aarch64 (the Cortex-A53) |

A **native** compiler has host = target. A **cross** compiler has host ≠ target. When you configure a program with autotools for the board, `--host=aarch64-xilinx-linux` means "the program will run on aarch64", which is a frequent source of confusion: from the program's point of view, the board is its host.

### Target triplets

The prefix of each tool name says what it produces: `<arch>-<vendor>-<os>[-<abi>]`. All of these exist on the reference host:

| Triplet | Produces code for | Typical use on ZynqMP |
| --- | --- | --- |
| `aarch64-xilinx-linux` | Linux user space and kernel on Arm64, glibc | Applications, kernel, U-Boot |
| `aarch64-linux-gnu` | Same, Debian/Ubuntu naming | Distribution cross compilers |
| `aarch64-xilinx-elf` (`aarch64-none-elf`) | Arm64 bare metal, no OS, newlib C library | FSBL, bare-metal A53 code |
| `arm-xilinx-eabi` (`armr5-none-eabi`) | 32-bit Arm bare metal, embedded ABI | Cortex-R5F firmware, FreeRTOS |
| `microblaze-xilinx-elf` | MicroBlaze bare metal | PMU firmware |

Vitis 2024.1 ships all of them. Asking each compiler what it targets:

```console
$ G=/tools/Xilinx2024.1/Vitis/2024.1/gnu
$ $G/aarch64/lin/aarch64-none/bin/aarch64-none-elf-gcc --version | head -1; $G/aarch64/lin/aarch64-none/bin/aarch64-none-elf-gcc -dumpmachine
aarch64-xilinx-elf-gcc.real (GCC) 12.2.0
aarch64-xilinx-elf
$ $G/armr5/lin/gcc-arm-none-eabi/bin/armr5-none-eabi-gcc --version | head -1; $G/armr5/lin/gcc-arm-none-eabi/bin/armr5-none-eabi-gcc -dumpmachine
arm-xilinx-eabi-gcc.real (GCC) 12.2.0
arm-xilinx-eabi
$ $G/microblaze/lin/bin/microblaze-xilinx-elf-gcc --version | head -1; $G/microblaze/lin/bin/microblaze-xilinx-elf-gcc -dumpmachine
microblaze-xilinx-elf-gcc.real (GCC) 12.2.0
microblaze-xilinx-elf
```

The file names follow the generic `-none-` convention, but `-dumpmachine` reveals that they are AMD builds (`-xilinx-`), all GCC 12.2.0. The `.real` suffix shows that the visible command is a wrapper script around the actual compiler, which is how Yocto-built toolchains are packaged.

### What is in a toolchain

| Component | Role |
| --- | --- |
| Compiler (`gcc`, `g++`) | C/C++ to assembly |
| binutils (`as`, `ld`, `objdump`, `readelf`, `strip`, `objcopy`) | Assemble, link, inspect and convert binaries |
| C library | `printf`, `malloc`, system call wrappers. **glibc** for Linux on ZynqMP; **newlib** for bare metal; musl in some small distributions |
| Kernel headers (UAPI) | Definitions of system calls, `ioctl`s and structures that user space shares with the kernel |
| Debugger (`gdb`) | Runs on the host and talks to `gdbserver` on the target, or to a JTAG probe |

### The sysroot

A cross compiler must not use the host's headers and libraries in `/usr/include` and `/usr/lib`: they are x86-64 code for Ubuntu's glibc. Instead it uses a **sysroot**, a directory that looks like the target's root filesystem but contains only what is needed to build: headers, libraries and their symbolic links.

```console
$ export PATH=/tools/Xilinx2024.1/Vitis/2024.1/gnu/aarch64/lin/aarch64-linux/bin:$PATH
$ aarch64-linux-gnu-gcc -dumpmachine
aarch64-xilinx-linux
$ aarch64-linux-gnu-gcc -print-sysroot
<Xilinx>/Vitis/2024.1/gnu/aarch64/lin/aarch64-linux/bin/../aarch64-xilinx-linux
$ strings $(aarch64-linux-gnu-gcc -print-sysroot)/lib/libc.so.6 | grep -m1 "GNU C Library"
GNU C Library (GNU libc) stable release version 2.36.
```

Vitis's Linux cross compiler is a Yocto-built toolchain whose sysroot carries glibc 2.36, the same version as the PetaLinux 2024.1 target ([section 01.01](../01-linux-fundamentals/01-what-is-linux.md)). That match is what makes its binaries run on the board.

> [!IMPORTANT]
> glibc is backward compatible but not forward compatible. A program linked against glibc 2.36 runs on 2.36 or newer, but not on 2.35. The loader then refuses to start it with a message of the form `version 'GLIBC_2.36' not found (required by ./app)`. Always build against a sysroot whose C library is no newer than the target's. (The message format is shown for illustration; it was not captured on the reference setup.)

## Hands-on

### Cross-compiling and inspecting a program

`hello.c`:

```c
#include <stdio.h>
#include <sys/utsname.h>

int main(void)
{
    struct utsname u;

    uname(&u);
    printf("Hello from %s, kernel %s\n", u.machine, u.release);
    return 0;
}
```

Build it and look at the result:

```console
$ aarch64-linux-gnu-gcc -O2 -o hello hello.c
$ file hello
hello: ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-aarch64.so.1, BuildID[sha1]=502cbc8972454873e46e2fafea66f363caf2f998, for GNU/Linux 3.14.0, with debug_info, not stripped
$ readelf -h hello | grep -E 'Class|Machine'
  Class:                             ELF64
  Machine:                           AArch64
$ readelf -l hello | grep interpreter
      [Requesting program interpreter: /lib/ld-linux-aarch64.so.1]
$ readelf -d hello | grep NEEDED
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
```

Three facts decide whether this binary runs somewhere:

1. **Machine `AArch64`.** It needs an Arm64 CPU.
2. **Interpreter `/lib/ld-linux-aarch64.so.1`.** The kernel starts this dynamic loader first, which then loads the libraries.
3. **`NEEDED libc.so.6`.** The loader must find a compatible glibc.

### Running it in the wrong place, and in the right one

Copy it to the target and run it, together with a native x86-64 build of the same source:

```console
$ gcc -O2 -o hello-x86 hello.c && ./hello-x86
Hello from x86_64, kernel 6.8.0-138-generic
$ scp hello hello-x86 zcu106-qemu:/tmp/
target$ /tmp/hello
Hello from aarch64, kernel 6.6.10-xilinx-v2024.1-g3af4295e00ef
target$ /tmp/hello-x86
sh: line 1: /tmp/hello-x86: cannot execute binary file: Exec format error
```

`Exec format error` is the kernel saying "this is not code for my CPU".

The reverse direction is more subtle on this host, because Ubuntu's `qemu-user-static` package has registered a **binfmt** handler (`/usr/libexec/qemu-binfmt/aarch64-binfmt-P`): the kernel automatically runs foreign Arm64 binaries in the QEMU user-mode emulator.

```console
$ ls /proc/sys/fs/binfmt_misc/ | grep -i aarch64
qemu-aarch64
$ ./hello
aarch64-binfmt-P: Could not open '/lib/ld-linux-aarch64.so.1': No such file or directory
$ qemu-aarch64 -L $(aarch64-linux-gnu-gcc -print-sysroot) ./hello
Hello from aarch64, kernel 6.8.0-138-generic
```

The emulator starts, but the binary asks for an Arm64 dynamic loader that the host does not have. Pointing QEMU at the toolchain's sysroot with `-L` supplies loader and libraries, and the program runs. This is the sysroot idea in one command: the binary is only half of the program, the other half is the target's libraries.

### Static linking

```console
$ aarch64-linux-gnu-gcc -O2 -static -o hello-static hello.c
$ ./hello-static
Hello from aarch64, kernel 6.8.0-138-generic
$ stat -c "%s %n" hello hello-static hello-x86
75520 hello
708224 hello-static
16064 hello-x86
```

A static binary contains its C library, needs no loader and runs anywhere the CPU and kernel fit, here even through binfmt without `-L`. The price is size (708 KB instead of 75 KB), no shared security updates of the library, and license obligations: statically linking glibc (LGPL) requires you to let users relink your program. Static linking is useful for rescue tools and tiny initramfs utilities, not as a default.

Why is the dynamic Arm64 binary 75 KB when the x86-64 one is 16 KB? Not because of the code, which is tiny in both. The Arm64 linker aligns loadable segments to 64 KiB, the x86-64 one to 4 KiB, and the gap is padding in the file:

```console
$ aarch64-linux-gnu-readelf -lW hello | grep LOAD
  LOAD           0x000000 0x0000000000000000 0x0000000000000000 0x000944 0x000944 R E 0x10000
  LOAD           0x00fdc8 0x000000000001fdc8 0x000000000001fdc8 0x000278 0x000280 RW  0x10000
$ readelf -lW hello-x86 | grep LOAD
  LOAD           0x000000 0x0000000000000000 0x0000000000000000 0x0006e0 0x0006e0 R   0x1000
  LOAD           0x001000 0x0000000000001000 0x0000000000001000 0x000209 0x000209 R E 0x1000
  LOAD           0x002000 0x0000000000002000 0x0000000000002000 0x000100 0x000100 R   0x1000
  LOAD           0x002da8 0x0000000000003da8 0x0000000000003da8 0x000268 0x000270 RW  0x1000
```

The 64 KiB alignment lets the same binary run on kernels configured for 4 KiB, 16 KiB or 64 KiB pages. The remaining difference is debug information from glibc's startup files (`crti.S`, `crtn.S`, `init.c`, `abi-note.c`), which is what `with debug_info` in the `file` output refers to. Stripping it (`aarch64-linux-gnu-strip`) brings `hello` from 75520 to 67592 bytes.

### The Yocto/PetaLinux SDK

For real applications, use the SDK that belongs to **your** image ([chapter 04](../04-yocto-project/08-sdk-and-esdk.md)). PetaLinux generates it with `petalinux-build --sdk`. Its `environment-setup-*` script sets `CC`, `CFLAGS` and friends so that every build uses the right sysroot and CPU options. In the ZCU106 project, that script contains:

```text
export CC="aarch64-xilinx-linux-gcc  -mcpu=cortex-a72.cortex-a53 -march=armv8-a+crc -fstack-protector-strong  -O2 -D_FORTIFY_SOURCE=2 -Wformat -Wformat-security -Werror=format-security --sysroot=$SDKTARGETSYSROOT"
```

- `-mcpu=cortex-a72.cortex-a53` tunes for a combination of Cortex-A72 and Cortex-A53. meta-xilinx sets the same default tune, `DEFAULTTUNE ?= "cortexa72-cortexa53"`, for both ZynqMP (A53) and Versal (A72), in `soc-zynqmp.inc` and `soc-versal.inc`. It is also why the target's packages have the architecture `cortexa72_cortexa53`.
- `--sysroot=$SDKTARGETSYSROOT` points at the image's own sysroot, with exactly the libraries the image contains, including the ones you added (OpenSSL, GStreamer, ...).
- The hardening flags (`-fstack-protector-strong`, `-D_FORTIFY_SOURCE=2`) match how the rest of the image was compiled.

Calling `aarch64-xilinx-linux-gcc` directly loses all of that. Always use `$CC` after sourcing the script, and let Make, CMake or Meson pick it up ([chapter 16](../16-application-development/01-cross-compiling-applications.md)).

### Toolchains you will meet

| Toolchain | Where it comes from | Use it for |
| --- | --- | --- |
| PetaLinux/Yocto SDK | `petalinux-build --sdk` (your image) | Applications and libraries for your image. The default choice |
| Vitis Linux toolchain | `<Vitis>/gnu/aarch64/lin/aarch64-linux/` | Quick experiments, Vitis application projects |
| Vitis bare-metal toolchains | `<Vitis>/gnu/aarch64/`, `armr5/`, `microblaze/` | FSBL, R5 firmware, PMU firmware |
| Distribution cross compilers | `apt install gcc-aarch64-linux-gnu` | Building the kernel or U-Boot outside Yocto. Not for user space, because the host distribution's glibc rarely matches the target's |

## Pitfalls

- **Mixing sysroots.** Headers from one sysroot and libraries from another compile fine and crash later.
- **Using `-I/usr/include` or `-L/usr/lib` in a cross build.** Those are host paths. pkg-config must be pointed at the sysroot too (`PKG_CONFIG_SYSROOT_DIR`), which the SDK environment script does.
- **Building against a newer glibc than the target has.** The program refuses to start on the target.
- **Forgetting that binfmt can hide architecture mistakes.** On a host with `qemu-user-static`, a wrongly built Arm64 test binary may "run" on your PC in emulation. Check with `file` before deploying.

## References

- GCC manual: `-dumpmachine`, `-print-sysroot`, `--sysroot`, `-mcpu`
- `meta-xilinx@rel-v2024.1:meta-xilinx-core/conf/machine/include/soc-zynqmp.inc` and `soc-versal.inc` (`DEFAULTTUNE`)
- `xilinx-zcu106-2024.1:components/yocto/environment-setup-cortexa72-cortexa53-xilinx-linux` (`CC`)
- Linux man pages: `ld.so(8)`, `elf(5)`, `binfmt_misc` (`Documentation/admin-guide/binfmt-misc.rst`)
- Captured on the reference setup: Vitis 2024.1 toolchains, cross build and inspection of `hello`, runs on host and QEMU target

---

<sub>← [Anatomy of an Embedded Linux System](01-anatomy-of-an-embedded-linux-system.md) · [Chapter index](README.md) · [Build Systems Landscape](03-build-systems-landscape.md) →</sub>
