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

## References

- Local BSP: `poky/scripts/lib/devtool/`, `poky/meta/classes/externalsrc.bbclass`
- Yocto 4.1.4 [devtool quick reference](https://docs.yoctoproject.org/4.1.4/ref-manual/devtool-reference.html)

---

<sub>← [Machine and Distro Configuration](06-machine-and-distro-configuration.md) · [Chapter index](README.md) · [SDK and Extensible SDK](08-sdk-and-esdk.md) →</sub>
