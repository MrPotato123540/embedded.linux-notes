# Environment, boot.scr and uEnv.txt

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[11 · U-Boot](README.md)** · Part IV: Boot

## Environment lifetime

U-Boot starts from compiled defaults or a supported persistent environment. `setenv` changes the current environment; persistence depends on the backend and a successful save. A build may deliberately have no persistent environment.

`bootcmd` defines automatic boot behavior. `bootargs` supplies Linux arguments. `run` executes a variable as a command list. Inspect nested variables when the apparent boot command does not explain the final behavior.

## Scripts

`boot.scr` is a script wrapped in a U-Boot image header, normally produced with `mkimage`. Its source should be maintained, not recovered by editing the binary. PetaLinux's boot-script recipe supplies release-specific defaults.

`uEnv.txt` is plain text only when the boot flow explicitly loads and imports it. Its presence on a card does not make U-Boot read it automatically. Distro boot and standard boot behavior also depend on configuration; do not assume both are active.

## Robust fallback

Check each load result before executing an image. Keep fallback targets explicit and avoid silently booting an old file after a failed update. Record the selected slot and boot reason so userspace can confirm the right image.

## References

- `meta-xilinx@rel-v2024.1`, `u-boot-xlnx-scr` recipe
- `u-boot-xlnx@xilinx-v2024.1`, environment and boot-script code

---

<sub>← [Essential U-Boot Commands](02-essential-commands.md) · [Chapter index](README.md) · [FIT Images and image.ub](04-fit-images.md) →</sub>
