# Project Structure: A Real 2024.1 Project Dissected

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Project map

| Directory | What it contains | Maintenance rule |
| --- | --- | --- |
| `project-spec/configs` | Project and rootfs selections | Keep intentional configuration changes |
| `project-spec/hw-description` | Imported hardware description and generated inputs | Tie to the hardware export revision |
| `project-spec/meta-user` | Product recipes, patches and configuration | Treat as maintained source |
| `components/yocto` | Build-system layers and SDK support | Record origins; avoid untracked edits |
| `components/plnx_workspace` | Generated component workspace | Do not use as the only copy of a change |
| `build` | Build configuration, tasks and temporary output | Regeneratable build state |
| `images/linux` | Newly built deployable files | Publish with checksums and a manifest |
| `pre-built/linux` | Prebuilt BSP artifacts | Not proof of a successful local build |
| `hardware` | BSP hardware assets | Preserve provenance |
| `.petalinux` | Tool metadata | Follow the project's ignore rules |

The hardware directory can contain the XSA, bitstream and processor initialization files. Their exact placement depends on how the project was created and imported. Inspect the project rather than assuming every generated file exists before configuration.

## What belongs in Git

The inspected BSP ignores `build/`, `images/linux/`, `pre-built/linux/`, `components/plnx_workspace` and `components/yocto`. It preserves `.petalinux/metadata` while ignoring most other `.petalinux` content.

Keep recipes, patches, configuration and a reference to the exact hardware export. Large release images can live in artifact storage. An ignored directory may still contain valuable uncommitted debugging work; move that work into a maintained recipe before cleaning it.

## Debugging

When a change vanishes, identify whether you edited source policy or generated output. Trace from `project-spec` through the generated build configuration to the final artifact. Never use file modification time alone as proof that the board booted the intended image.

## Trace ownership from input to output

A PetaLinux project contains maintained inputs, generated metadata, temporary build state and deployable artifacts. These categories can sit close together in the directory tree, but they have different ownership rules. The most useful question is not “which directory contains this file?” but “which input will recreate it?”

Start with `project-spec/configs/config` and `rootfs_config`. They record project and root filesystem selections. Hardware import contributes data under `project-spec/hw-description`. The user layer under `project-spec/meta-user` supplies persistent additions. The tool combines these inputs with its layer set to produce the build configuration and component workspaces.

During a build, recipes prepare source, create task scripts and stage output in the build area. Deploy tasks then publish component artifacts. Packaging can combine those artifacts into boot or disk images. Editing a late-stage file may be useful for a diagnosis, but it does not define a repeatable change unless you also update its maintained source.

## The real user-layer device-tree chain

The reference BSP has `project-spec/meta-user/recipes-bsp/device-tree/device-tree.bbappend`. It extends the file search path and adds `system-user.dtsi` to `SRC_URI`. The corresponding file in `files/` includes `system-conf.dtsi` and has an empty root-node extension in this inspected project.

These two files have different jobs. The append makes the include file available to the recipe. The DTS include supplies hardware-description changes. Merely creating a `.dtsi` in an arbitrary directory does not connect it to the build. Conversely, adding it to `SRC_URI` does not mean every node you describe is correct for the board.

The append also contains a conditional `require` controlled by `SYSTEM_DTFILE`. This is a reminder that one source file can support more than one generation path. Read the condition and the selected configuration before concluding which path the current project uses. A conditional reference is not evidence that the referenced branch executed.

## Generated configuration is valuable evidence

`build/conf/plnxtool.conf` translates project choices into BitBake settings. In the inspected project it assigns `MACHINE = "xilinx-zcu106"`, places temporary work under the project build directory, and defines ZynqMP image output formats. It also supplies an image-specific package selection.

This file is useful when a menu setting does not appear to work. Compare the maintained project configuration with the generated value. If generation is wrong, investigate the project setting or generation path. If generation is correct but the final recipe value differs, investigate metadata precedence. If both are correct, inspect the relevant task and deployed output.

Do not treat this diagnostic value as a reason to maintain product policy only in `build/conf`. Regeneration can overwrite it. The durable fix belongs in the supported project input or user layer.

## Prebuilt files and locally built files

`pre-built/linux/images` contains vendor-provided artifacts in the reference BSP. They are useful for a baseline boot and for inspecting a real boot image. They do not record the result of your current recipe changes. `images/linux` belongs to the local output flow, but you must still confirm which build and packaging step produced each file.

Copying an artifact into another directory breaks any simple relationship between its path and its origin. Keep checksums and a release manifest. If the board boots through a script, inspect the filenames and addresses that script actually selects. A new `Image` beside an old `image.ub` does not prove the new kernel is used.

## What the supplied ignore rules teach

The BSP's `.gitignore` excludes `build/`, `images/linux/`, `pre-built/linux/`, `components/plnx_workspace` and `components/yocto`. It ignores most `.petalinux` files while keeping `.petalinux/metadata`. This expresses a distinction between project identity and large or regeneratable state.

An ignored path is not necessarily disposable. A developer may have edited source inside a workspace or left the only useful failure log under `build`. Before cleaning, inspect those locations and move intentional changes into maintained recipes or patches. Git cannot recover a file it never tracked.

Large hardware exports and release binaries need a deliberate storage policy. Keeping them outside Git is reasonable if the project records an immutable identifier, checksum and retrieval location. A note saying “use the latest XSA” is not enough to recreate an older release.

## Diagnose a disappearing change

Suppose a device-tree node appears during one test and vanishes after reconfiguration. First identify where it was edited. If it was edited in generated output, find the maintained include that should own the change. If the include is already maintained, inspect recipe discovery and the final include chain. If the compiled DTB contains the node, inspect boot selection and the live tree.

The same sequence applies to kernel options and application files: persistent input, generated metadata, task result, deployed artifact, runtime consumer. Stopping at an earlier stage can produce a false diagnosis. For example, a correct compiled DTB does not explain a board that loaded another DTB from a different partition.

**Source trail:** the inspected BSP's `.gitignore`, `project-spec/configs/`, `project-spec/meta-user/recipes-bsp/device-tree/`, and `build/conf/plnxtool.conf`. These paths were inspected directly; they are not a fabricated project layout.

## References

- Inspected `xilinx-zcu106-2024.1:.gitignore` and project directory tree
- AMD UG1144 (2024.1), project structure

---

<sub>← [Installation and Host Setup](02-installation-and-host-setup.md) · [Chapter index](README.md) · [Commands and Workflow](04-commands-and-workflow.md) →</sub>
