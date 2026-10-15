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

## References

- Local BSP: `poky/bitbake/doc/bitbake-user-manual/bitbake-user-manual-metadata.rst`
- Local BSP: `poky/meta/conf/bitbake.conf`, `poky/meta/classes-recipe/cmake.bbclass`
- Yocto 4.1.4 [variable glossary](https://docs.yoctoproject.org/4.1.4/ref-manual/variables.html)

---

<sub>← [Layers and the Layer Model](02-layers.md) · [Chapter index](README.md) · [BitBake Tasks and the Build Process](04-bitbake-tasks-and-build-process.md) →</sub>
