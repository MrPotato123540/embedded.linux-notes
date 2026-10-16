# devtool Workflow

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Concepts

`devtool` connects source development with the recipe that builds it. Its workspace layer temporarily changes where the build gets source. This avoids editing files that BitBake may replace during the next unpack or clean operation.

The normal sequence is:

1. Use `add` for a new component, or `modify` to work on an existing recipe.
2. Edit the extracted source and commit logical changes in its Git repository.
3. Use `build` to test the recipe in the build environment.
4. Use `deploy-target` only for development testing on a reachable target.
5. Use `finish` to put the recipe changes or patches into a maintained layer.

Deployment is not image integration. A target changed by `deploy-target` may contain files that a fresh product image does not have. Finish the recipe change, rebuild the image and test that image before claiming the feature is integrated.

## Kernel and U-Boot changes

Start from the provider selected by the current machine. Keep a patch limited to one behavior, and record the source revision on which it was developed. A patch applying cleanly does not prove that a changed driver still matches the hardware.

The `externalsrc` class can point a recipe at an external source tree. This helps development, but that tree must not become an undocumented requirement for release builds. Check that the final recipe fetches committed source without the workspace override.

## Debugging

If a change disappears, check whether the build still uses the workspace source. If a clean build behaves differently, check for uncommitted files and generated files that were never added to the recipe. Review the resulting patch, not only the development directory.

> [!NOTE]
> **Not run on the reference setup:** the full modify/build/deploy/finish cycle in this continuation. Use this as a workflow description, not a recorded successful session.

## What the workspace changes

Normally, a recipe fetches and prepares source inside the build's work area. That directory belongs to the build system. Unpack and clean operations can replace it. A development workspace moves source editing into a location intended for human changes and makes metadata point at that location.

This creates two states that you must track: the source repository where you edit code, and the recipe metadata that selects that source. A correct patch in an unused source tree changes nothing. A workspace override can also make a local build succeed even though the maintained recipe still points at old source.

The `externalsrc` mechanism is part of this connection. It changes how tasks obtain source and build directories. This is useful during development because rebuilding need not discard your edits. It is also why a release test must remove the workspace dependency and rebuild from the maintained recipe.

## Develop one change with a clear baseline

Before modifying a component, record its selected provider and source revision. Read its existing patches. Decide whether your change belongs upstream, in a product patch or in configuration. A configuration change should not become a source patch just because the source file is easy to edit.

For an existing component, `modify` prepares a development source tree and workspace metadata. For a new component, `add` helps create the recipe relationship. Generated metadata is a starting point: review licensing, source location, dependency declarations and installation behavior before treating it as a product recipe.

Commit source changes in small logical steps. One commit might fix an error path; another might add a board-specific option. This makes the eventual patch series easier to review and easier to rebase when the vendor source changes. Keep generated build output out of the source patch unless the upstream project intentionally versions it.

The bundled implementation makes these boundaries visible. `scripts/lib/devtool/standard.py` contains `add`, `modify`, `update_recipe`, `reset` and `finish`. The build and deployment operations live in separate modules. The tool is coordinating recipe metadata, source control and deployment; it is not a second compiler.

## Build and deployment answer different questions

A workspace build tests the recipe using the development source. This can reveal compile failures and packaging problems. It does not prove that the maintained layer contains everything required to reproduce the build.

Deploying to a target is a fast development step. It can place changed files on an already running image. That image may contain old dependencies, manual configuration and files from earlier experiments. A successful deployed test is useful evidence about behavior, but it is weaker evidence about image completeness.

For example, a new daemon may work after deployment because a developer manually installed a helper package yesterday. The final image recipe still lacks that dependency. A fresh image test catches this because it starts from declared metadata instead of accumulated target state.

Deployment can also leave old files behind when an application's file layout changes. A renamed plugin may coexist with its previous version and alter discovery order. Inspect the resulting file set and use the tool's supported cleanup workflow before drawing conclusions from another deployment.

## Finish the change into a maintained layer

Finishing transfers the development change into metadata that the build can use without the workspace. Depending on the workflow, this can involve patches, recipe changes or an append in the destination layer. Review the output rather than assuming every local file was captured.

Check the generated patch series for unrelated formatting, temporary debug prints, embedded absolute paths and untracked files. Check the recipe for correct source revisions, patch order and file search paths. A patch that applies cleanly still needs a behavior test; it may alter the wrong configuration branch or a driver that the target never binds.

Then run a build without the workspace override. This is the critical integration boundary. If it fails while the workspace build succeeds, compare source content, generated files and dependency declarations. Do not immediately restore the workspace and call the discrepancy resolved.

## Kernel and bootloader work need extra evidence

For a kernel change, verify the selected kernel provider, resulting configuration and deployed image identity. If the change is in a module, ensure the module installed on the target belongs to that kernel build. A successful compiler run does not prove the board loaded the new module.

For U-Boot, inspect the ELF or binary used by the boot-image packaging step. It is possible to rebuild U-Boot and then package an older file from another directory. The same applies to FSBL and PMU firmware. Keep the build result and packaging input tied to one release record.

A driver change also needs hardware evidence: matching device-tree data, resource ownership, interrupts and failure handling. The source-development workflow cannot provide those checks on its own.

## A reproducible completion record

Record the original source revision, the final patches, the destination layer revision, the configuration used, and the identity of the tested artifact. Note whether testing used temporary deployment or a rebuilt image. This lets another engineer understand exactly what the result establishes.

The full workflow remains unexecuted in this writing pass. The source paths and responsibilities were checked in the local BSP. The sequence above is a development procedure, with its integration checkpoints stated explicitly.

## References

- Local BSP: `poky/scripts/lib/devtool/`, `poky/meta/classes/externalsrc.bbclass`
- Yocto 4.1.4 [devtool quick reference](https://docs.yoctoproject.org/4.1.4/ref-manual/devtool-reference.html)

---

<sub>← [Machine and Distro Configuration](06-machine-and-distro-configuration.md) · [Chapter index](README.md) · [SDK and Extensible SDK](08-sdk-and-esdk.md) →</sub>
