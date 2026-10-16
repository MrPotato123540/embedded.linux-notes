# Environment, boot.scr and uEnv.txt

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot


## The environment is a program input

U-Boot's environment contains plain values and command lists. `bootcmd` selects automatic boot behavior, `bootargs` supplies kernel arguments, and other variables can hold load addresses, filenames or nested commands. A readable environment is therefore also executable policy.

The active environment can come from compiled defaults or an enabled persistent backend. If persistent data is invalid or unavailable, the build can use defaults. A saved environment can also retain old values after replacing the U-Boot binary. This explains why two boards with the same executable can take different boot paths.

`setenv` changes the current in-memory value. Saving requires backend support and a successful persistent write. A script that relies on persistence must account for write failure and power loss, rather than assuming the command's presence guarantees durable storage.

## Follow nested control flow

Suppose `bootcmd` runs a scan variable, which loads `boot.scr`, which changes `bootargs` and invokes another environment variable. Reading only the first string misses most of the behavior. Trace the executed commands and the point at which each value is expanded.

A later command can overwrite a value that appeared correct earlier. This is common with `bootargs`, selected device variables and `filesize`. Preserve important results when they are produced and check the final values immediately before the handoff boundary.

A failed load does not automatically clear its destination buffer. If the script ignores the failure, a later `booti` or `bootm` can use stale bytes. Gate every dependent action on the operation that produced its input.

## boot.scr has a source and a generated wrapper

The local PetaLinux 2024.1 recipe is `meta-xilinx-core/recipes-bsp/u-boot/u-boot-xlnx-scr.bb`. It reads a `boot.cmd` template, replaces recipe placeholders and wraps the result with `mkimage` as a script image. The generated `boot.scr` should be treated as an artifact.

Maintain the source template or recipe override in version control. Editing the binary wrapper is not a reproducible source change, and regenerating the project can replace it. Also, inspect the deployed script actually copied to the boot medium; a correct build output does not update an older card automatically.

The recipe uses `-A arm -T script -C none` when wrapping the command text. The `arm` field here is script-container metadata; it does not turn the AArch64 kernel into a 32-bit kernel. The script's later boot command and loaded image determine the kernel handoff path.

## The 2024.1 recipe's address choices

The inspected recipe defines these ZynqMP defaults before project overrides:

| Artifact role | Recipe default offset |
| --- | --- |
| Raw kernel | `0x200000` |
| Device tree | `0x100000` |
| Ramdisk | `0x4000000` |
| FIT container | `0x10000000` |

The recipe can add the DDR base unless configured to skip that behavior. A string already expressed through a U-Boot variable follows a different substitution path. Read the generated command text to see the final values rather than manually combining defaults twice.

These addresses are not universal safe zones. A larger kernel, new reserved firmware range or different DDR map can require a changed layout. Review actual sizes and lifetimes, including decompression and relocation, before adopting the defaults in a custom product.

## uEnv.txt is opt-in behavior

A text file named `uEnv.txt` does nothing merely because it exists on a filesystem. The active boot flow must load it and import or interpret it with the intended command. The local script recipe exposes its name and load-address settings, but the selected template determines how it is used.

Import formats and allowed variable names deserve review. A writable text environment can change boot policy if the script imports sensitive values without restriction. In a verified-boot design, decide which policy inputs are authenticated and which are only operational preferences.

Do not assume that distro boot and standard boot are both active in every configuration. They are framework choices with their own scanning and policy behavior. Inspect the compiled configuration and actual environment for this image.

## A worked fallback design

Assume a product has primary and recovery images. This is a design example, not a supplied production script. The primary path loads the selected image, validates its format and required authentication, then starts it. If any required step fails, the script records the failure reason and tries a defined recovery path.

The recovery path should load its own known files and should not reuse an address as proof that a previous load succeeded. It also needs a compatible device tree and root filesystem. Combining a recovery kernel with a primary DTB can produce a partially booting system with incorrect hardware behavior.

A boot attempt should become successful only after the intended system reaches its health criterion. Reaching the U-Boot handoff is too early to prove root filesystem mount or application startup. If a boot-count mechanism is used, specify who confirms success and which persistent state survives reset.

## Environment storage is part of the flash layout

A persistent environment backend uses an assigned storage area and format. Its offset and size must match the board's storage map. Moving partitions or changing environment geometry without migration can make U-Boot read unrelated bytes or overwrite another artifact when saving.

Redundant environments can improve recovery from interrupted writes, but their exact behavior depends on the backend and configuration. They do not replace a tested power-loss plan for the complete update process. Keep boot image, environment and OS-slot ownership explicit.

> [!NOTE]
> **Not run on the reference setup:** persistent environment writes, redundant-environment power-loss tests and the illustrative two-image fallback. The recipe transformation and defaults were inspected locally; the saved session only demonstrates temporary environment changes.

## References

- Local BSP: `meta-xilinx/meta-xilinx-core/recipes-bsp/u-boot/u-boot-xlnx-scr.bb` and its `boot.cmd` templates.
- [2024.1 environment implementation](https://github.com/Xilinx/u-boot-xlnx/blob/xilinx-v2024.1/env/env.c).
- Saved `cap-wp01-uboot.txt` and [FIT image selection](04-fit-images.md).

---

<sub>← [Essential U-Boot Commands](02-essential-commands.md) · [Chapter index](README.md) · [FIT Images and image.ub](04-fit-images.md) →</sub>
