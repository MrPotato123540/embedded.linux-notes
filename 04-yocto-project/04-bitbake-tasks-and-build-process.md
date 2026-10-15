# BitBake Tasks and the Build Process

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Concepts

BitBake builds a dependency graph. A task runs only when its required inputs are ready. The common source-build path is fetch → unpack → patch → configure → compile → install → package. Image tasks then install selected packages into a root filesystem and create output formats.

`do_install` writes into `${D}`. It does not install software on your host or target. Packaging splits that staged tree into packages. Image assembly uses package dependencies, so a successful compile alone does not prove that a file reaches the image.

## Files worth knowing

| Location | Use |
| --- | --- |
| Recipe `temp/log.do_*` | Task output, including the compiler error |
| Recipe `temp/run.do_*` | Expanded task script and environment |
| `recipe-sysroot` | Target dependencies available to that recipe |
| `recipe-sysroot-native` | Build-host tools available to that recipe |
| `tmp/deploy` | Deployable images, packages and SDK output |
| `DL_DIR` | Download cache |
| `SSTATE_DIR` | Shared-state cache of reusable task results |

A task signature describes its relevant inputs. Shared state can restore a result when the signature matches. Hash equivalence can also identify tasks with equivalent output. Neither cache should replace source control or a record of build configuration.

## Debugging sequence

Read the first failing task's log before cleaning anything. Check its generated script, compiler invocation and sysroot. Then inspect the final recipe environment and dependency graph. BitBake supports `-e` for the environment, `-g` for graphs, `-c` for selecting a task and `-k` to continue independent work after an error.

`listtasks` lists tasks; `devshell` opens the recipe's development environment. `-f` forces a task and changes normal reuse behavior. `cleansstate` removes reusable state for a recipe and can make diagnosis slower by destroying useful evidence. Avoid broad cleaning as the first response to a configuration mistake.

> [!NOTE]
> **Not run on the reference setup:** a fresh full BitBake build and shared-state recovery test during this writing pass. No build-success output is implied here.

## References

- Local BSP: `poky/meta/classes-global/base.bbclass`, `poky/meta/classes-global/sstate.bbclass`
- Yocto 4.1.4 [task reference](https://docs.yoctoproject.org/4.1.4/ref-manual/tasks.html)
- BitBake manual shipped in `poky/bitbake/doc/`

---

<sub>← [Recipes and Metadata Syntax](03-recipes-and-metadata-syntax.md) · [Chapter index](README.md) · [Images, Packagegroups and Features](05-images-packagegroups-and-features.md) →</sub>
