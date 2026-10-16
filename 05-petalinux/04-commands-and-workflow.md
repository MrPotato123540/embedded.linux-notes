# Commands and Workflow

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Workflow

A complete build flow has five stages: create, import hardware, configure, build and package. Boot testing comes after packaging. Record the input hardware revision before starting.

The installed 2024.1 help uses **subcommands** for creation and packaging. For example, project creation is `petalinux-create project`; boot packaging is `petalinux-package boot`. Older guides often show `-t project` or `--boot`. Use the installed release help as the authority for accepted syntax.

| Operation | Relevant interface |
| --- | --- |
| Create from BSP | `project` subcommand with `--source` |
| Create for ZynqMP | `project` subcommand with `--template zynqMP` |
| Import hardware | `petalinux-config --get-hw-description` |
| Configure a component | `petalinux-config -c` |
| Build one component | `petalinux-build -c` |
| Select a BitBake task | `petalinux-build -x` |
| Build an SDK | `petalinux-build --sdk` |
| Build an extensible SDK | `petalinux-build --esdk` |

These interfaces were checked through local help. They are not a transcript of a newly completed image build.

## Iterating safely

After a recipe change, rebuild the component and then the image that includes its package. After a boot-firmware change, regenerate the boot image. A successful component build does not update an SD card automatically.

Packaging has separate boot, WIC disk-image, BSP and prebuilt purposes. QEMU and JTAG also have different boot inputs. Select the flow first, then check its subcommand help.

Cleaning removes evidence and may require large rebuilds. Preserve patches and logs before using clean tasks. Treat a release upgrade as a controlled migration: rebuild from pinned inputs and test hardware behavior again.

## Treat the workflow as a sequence of state changes

Creating a project establishes its initial metadata. Importing hardware changes the platform inputs. Configuration translates project choices into build settings. Building produces component and image artifacts. Packaging arranges selected artifacts for a boot or distribution flow. Boot testing exercises those artifacts through a particular loader path.

Each stage has an input and an observable output. Record both. If a board runs an old kernel after a successful build, the failure may be in packaging, copying or boot selection. Repeating the build cannot identify which later stage selected the old file.

## Read installed help before copying release-specific syntax

The installed 2024.1 interface uses creation subcommands such as `project`, `apps` and `modules`. Boot packaging uses the `boot` subcommand. Some older examples use a different command structure. The exact accepted options should come from the installed tool and the release-specific documentation.

The captured `petalinux-create project --help` describes `--source` for BSP input and `--template` for a template project. It lists `zynqMP` with that capitalization. Its examples also show the project-name option. Help for the parent command and help for the selected subcommand can describe different parts of the same invocation, so inspect both when an option appears to be missing.

The application help distinguishes a C application template, C++, autoconf and install-only content. It also lists hardware-acceleration templates. Choosing a template selects a starting recipe layout; it does not verify a device binding or register map.

## Choose the smallest useful rebuild boundary

A source edit to an application normally starts with rebuilding that component. You then need image integration if the result is delivered as part of the root filesystem. A kernel change needs the kernel result and any matching module packages. A boot-firmware change needs the updated firmware and a regenerated boot image that includes it.

| Changed input | Inspect after building | Additional delivery step |
| --- | --- | --- |
| Application source | Executable and package contents | Rebuild image or use a recorded development deployment |
| Kernel fragment | Final kernel configuration and image | Keep modules and booted kernel together |
| Device-tree include | Compiled DTB contents | Confirm loader selects that DTB or updated FIT |
| FSBL or PMUFW source | Firmware ELF identity | Repackage `BOOT.BIN` |
| Bitstream | Hardware revision and bitstream identity | Update early-boot package or late-load firmware set |
| Image package selection | Manifest and root filesystem | Deploy the new root filesystem |

This table is a dependency guide. The exact recipe names and packaging inputs depend on the selected project. Inspect those values instead of assuming a generic filename identifies the active provider.

## Diagnose wrapper failures at the underlying task

A wrapper often reports only that a component failed. Preserve that message, then locate the first failing BitBake task. The task log shows the actual compiler, fetcher, patch or package-manager failure. The generated task script shows the expanded environment that produced it.

A fetch failure should lead to the source URL, revision and mirror policy. A patch failure should lead to the selected source and patch order. A compile failure should lead to compiler flags, generated headers and sysroot dependencies. A root filesystem failure should lead to package names, conflicts and installation scripts. These failures require different changes even when the top-level command is the same.

Use clean tasks deliberately. Before cleaning, preserve local source edits and the useful logs. A clean rebuild can confirm that a fix is durable, but it should follow a hypothesis. If the fix is only “remove every cache,” the cause remains unexplained.

## Packaging is a separate validation step

The boot packager consumes concrete files. Review the generated BIF and confirm which FSBL, PMUFW, TF-A, U-Boot and optional PL data it names. Inspect the completed boot image with the matching Bootgen release. A successful package command proves format processing, not that every input belongs to the same hardware revision.

A WIC image adds partition layout and filesystem content. A BSP package preserves a reusable project. Prebuilt packaging prepares files for a selected launch flow. These outputs serve different consumers, so their success criteria differ.

## Finish with a recorded boot path

For QEMU, record the launch mode and files loaded. For JTAG, record initialization and downloaded ELF files. For SD or flash, record the boot-mode selection, partition or offset layout, and deployed file checksums. Then capture the serial log from reset through the application milestone you care about.

Test one known change that identifies the new build, such as a controlled version string, and compare it with the release manifest. Do not rely only on file modification times. A bootloader environment or script can select a different medium than the one you just updated.

The command interfaces above were checked through local help. The deeper rebuild and deployment sequence is a procedure, not a claim that a fresh full image build or physical-board boot occurred during this writing pass.

## References

- Executed help from `/opt/pkg/petalinux24.1`: create, config, build, package and boot tools
- AMD UG1144 (2024.1), command-line reference

---

<sub>← [Project Structure: A Real 2024.1 Project Dissected](03-project-structure.md) · [Chapter index](README.md) · [The Configuration System](05-configuration-system.md) →</sub>
