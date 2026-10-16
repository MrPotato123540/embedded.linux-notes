# Recipes and Metadata Syntax

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Concepts

Recipes are configuration programs, not shell scripts. BitBake expands their variables and combines the recipe with classes, includes and append files before tasks run.

| Suffix | Purpose |
| --- | --- |
| `.bb` | Recipe |
| `.bbappend` | Changes to a matching recipe |
| `.bbclass` | Shared behavior selected with `inherit` |
| `.inc` | Metadata included by another file |
| `.conf` | Build, machine or distribution configuration |

`=` stores a value for later expansion. `:=` expands immediately. `?=` assigns only if no value exists at that point. `+=` adds a separating space. `:append` adds text without adding a space automatically; write the space explicitly when extending a list. `:remove` removes matching items. Machine and package overrides select where a value applies.

## Following a recipe

| Variable | Question it answers |
| --- | --- |
| `SRC_URI`, `SRCREV` | Where is the source, and which revision is used? |
| `LICENSE`, `LIC_FILES_CHKSUM` | What license applies, and which text is checked? |
| `WORKDIR` | Where does this recipe perform its work? |
| `S`, `B` | Where are source and build files? |
| `D` | Where does installation stage target files? |
| `PACKAGES`, `FILES:${PN}` | Which output packages receive those files? |
| `FILESEXTRAPATHS` | Where can append files supply patches or local files? |

`DEPENDS` names build dependencies, usually recipes whose output enters the recipe sysroot. `RDEPENDS:${PN}` names runtime packages required by the output package. These are not interchangeable. `PROVIDES` offers alternative recipe names; `PREFERRED_PROVIDER` chooses a provider when several recipes offer the same interface, such as `virtual/kernel`.

## Build-system patterns

Use the matching `cmake` or `autotools` class when the upstream project supports it. A Makefile project needs correct compiler variables and an installation step into `${D}`. Prebuilt binaries still need architecture, runtime-library and license checks. Never hide an architecture mismatch by disabling every packaging check.

Development headers usually belong in `${PN}-dev`; debug symbols belong in `${PN}-dbg`. A file installed into `${D}` can still be absent from the image if no package owns it or the package is not selected.

## Expansion time changes the result

BitBake has a parse stage and an expansion stage. With ordinary `=`, a variable reference is expanded when the value is needed. With `:=`, it is expanded at the assignment. This difference matters when a later file changes a referenced variable.

Consider this original metadata example:

```bitbake
LABEL = "first"
DEFERRED = "${LABEL}"
IMMEDIATE := "${LABEL}"
LABEL = "second"
```

After these assignments, expanding `DEFERRED` uses the later value of `LABEL`. `IMMEDIATE` retains the value seen at its own assignment. This example describes the parser semantics documented in the bundled BitBake manual; it is not a console transcript.

The distinction explains a common append pattern: `FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"`. Immediate expansion captures the append file's directory while that file is being parsed. The final colon separates this entry from the existing search path. Without the separator, two intended directories can become one invalid path. Without the right expansion timing, `THISDIR` may no longer identify the file you intended.

Overrides add a second dimension. A machine override limits an assignment to a machine context. A package override limits it to a package context. `RDEPENDS:${PN}` describes dependencies of one output package; assigning plain `RDEPENDS` does not express that same package boundary. When debugging, identify both the value and the context in which BitBake expands it.

## Build dependencies and runtime dependencies

A build dependency supplies inputs to a recipe task. A runtime dependency supplies packages to the target installation. For a C application using a shared library, the headers and link-time files are build inputs. The shared object needed by the dynamic loader is a runtime input. They often come from the same upstream project, but they are handled by different mechanisms.

OpenEmbedded can discover many shared-library dependencies during packaging. It cannot infer every dependency from an executable's dynamic section. A shell script that calls another program, a Python application importing an optional module, or a service opening a data file may need an explicit runtime dependency. The absence of a linker error does not prove these dependencies are complete.

Use package names in runtime dependencies. A recipe can produce several differently named packages. For example, requesting the recipe's development package may add headers and unversioned linker symlinks that are unnecessary on a production target. Inspect the package split before deciding which package the image needs.

## Trace a real recipe instead of reading variables alone

The BSP includes `poky/meta/recipes-extended/which/which_2.21.bb`. Its source is a release archive with checksums and a local patch. It inherits `autotools`, `texinfo` and `update-alternatives`. It also sets `DEPENDS = "cwautomacros-native"` and changes the configure preparation with a prepended task fragment.

Read this in causal order. The archive provides the upstream source. The patch adjusts that source. The native dependency provides macros used on the host. The class supplies the standard configure, compile and installation procedure. The recipe's task fragment changes a project-specific input before the inherited configure work runs. The alternatives metadata handles a command name that can have more than one implementation.

The recipe also has `BBCLASSEXTEND = "nativesdk"`. This requests another recipe context for an SDK-host build. It does not mean the target executable can run on the workstation. Architecture and sysroot selection still depend on the active recipe context.

## Installation, package ownership and image selection

Three directories are easy to confuse. `${S}` contains the source. `${B}` contains build results and may be separate from `${S}`. `${D}` is the target installation staging tree. A recipe that writes files directly into the host's `/usr` violates the staging model and can damage the host. Use the class's installation support and the destination variables supplied by OpenEmbedded.

After installation, packaging assigns staged paths to `PACKAGES` entries according to their `FILES` expressions. Ordering matters when patterns overlap. The package quality checks can identify files left unassigned. Suppressing that check does not put those files in the image; correct the package ownership instead.

The final image then selects packages. If an executable exists in `${D}` but not in the image, inspect package contents before changing compilation. If it is in a package but absent from the image manifest, inspect image selection. If it is in the root filesystem but cannot start, inspect runtime dependencies, permissions and the executable interpreter.

## Preserve flags supplied by the build system

Cross builds need more than a compiler binary name. Compiler, linker and preprocessor flags carry sysroot paths, architecture tuning, hardening and reproducibility settings. A hand-written Makefile can accidentally replace these values with its own defaults. Prefer the appropriate class and pass the build system's variables through to the upstream build.

Do not solve a host-header leak by adding another absolute workstation path. The recipe should declare the missing dependency and consume it through its sysroot. Absolute paths can make one workstation succeed while the next one fails, and can leave host-specific paths inside generated output.

**Source trail:** local `poky/bitbake/doc/bitbake-user-manual/bitbake-user-manual-metadata.rst`, `poky/meta/conf/bitbake.conf`, and `which_2.21.bb`. The teaching assignment example was written for this guide; the `which` settings were inspected in the real BSP.

## References

- Local BSP: `poky/bitbake/doc/bitbake-user-manual/bitbake-user-manual-metadata.rst`
- Local BSP: `poky/meta/conf/bitbake.conf`, `poky/meta/classes-recipe/cmake.bbclass`
- Yocto 4.1.4 [variable glossary](https://docs.yoctoproject.org/4.1.4/ref-manual/variables.html)

---

<sub>← [Layers and the Layer Model](02-layers.md) · [Chapter index](README.md) · [BitBake Tasks and the Build Process](04-bitbake-tasks-and-build-process.md) →</sub>
