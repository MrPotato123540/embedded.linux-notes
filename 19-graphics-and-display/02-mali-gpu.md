# Arm Mali-400 MP2 GPU

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[19 · Graphics and Display](README.md)** · Part IX: Graphics and Multimedia

## Mali-400 stack

Supported ZynqMP variants include a Mali-400 MP2 GPU. It is a rendering engine, not a DisplayPort controller. Its graphics API generation differs from modern desktop GPUs; do not assume Vulkan, desktop OpenGL or general compute support.

The AMD proprietary path combines a compatible `mali` kernel module with matching `libmali-xlnx` userspace. Window-system backends must match the selected X11, Wayland or other supported display path. Mixing libraries from a different stack can fail during EGL initialization.

Mesa's Lima driver is an open-source alternative for supported Mali-400 hardware. Selecting it is a stack change, not simply replacing one shared library while keeping all proprietary components.

## Validation

Check the actual renderer and API support, then test the intended surface format and compositor. Tools such as `es2gears` or `glmark2` are useful when built for the selected backend. A software-rendered benchmark does not establish GPU acceleration.

> [!NOTE]
> **Not run on the reference setup:** GPU rendering and backend comparison.

## Rendering and presentation are separate pipelines

The Mali-400 MP2 processes graphics work and writes rendered results into memory. A display controller later reads pixels for a physical output. An application can therefore have a working GPU and no working monitor output, or working display scanout with CPU rendering only.

The hardware belongs to the Mali Utgard generation. Its expected embedded graphics baseline includes OpenGL ES 1.1/2.0 with suitable software. Do not select an application that requires a modern desktop graphics feature set without checking every required API and extension against the actual driver.

The graphics stack also needs a window-system integration layer. EGL connects rendering contexts and surfaces to the selected native platform. A library built for one backend can load successfully but fail when asked to create a surface for another backend.

## Inspect the supplied proprietary stack

The BSP's `kernel-module-mali.bb` selects Arm's `r9p0-01rel0` kernel driver source and applies release patches. It inherits the module build class, so its binary depends on the selected kernel build. The recipe requires the machine feature `mali400`.

The matching `libmali-xlnx.bb` selects userspace binaries at the same driver generation and declares a dependency on `kernel-module-mali`. It provides virtual EGL, GLES and GBM capabilities to the build. Provider selection is therefore a build-system decision as well as a runtime library decision.

The rootfs manifest reports `libmali-xlnx` as `r9p0+01rel0`; package-version formatting differs from the recipe's source-generation spelling. Keep both identities clear when comparing logs with metadata. The archive evidence does not establish that the driver loaded or rendered a frame.

## Backends are packaged alternatives

The local recipe installs a common library set plus backend variants for supported X11, fbdev, Wayland and headless paths. `MALI_BACKEND_DEFAULT` defaults in the recipe to X11, while distribution features and overrides determine what is actually built and selected.

Alternatives select the visible monolithic `libMali` library path. The recipe contains target-side alternative handling because ordinary library-cache processing can disturb the intended symlinks during image creation. This is a concrete first-boot concern for read-only rootfs designs.

A wrong backend can produce EGL initialization or surface-creation failure even when the kernel module is correct. Inspect the selected library and native platform together. Adding random library search paths can load a second incompatible provider and make the failure less predictable.

## Follow a rendering request

The application creates an EGL display connection, chooses a compatible configuration, creates a context and a surface, then submits graphics commands. The userspace driver builds device work and communicates with the kernel driver. Completion makes the result available for later consumers under the stack's synchronization rules.

A context owns rendering state and references objects such as textures and buffers. A surface represents a rendering/presentation target. Their lifetime must cover queued work. Destroying a high-level widget does not necessarily mean its GPU work has finished at the same instant.

Shader compilation, texture upload and buffer allocation can create first-use delays. Measure them separately from steady-state drawing when startup and animation performance have different requirements.

## A concrete Weston compatibility trap

The BSP's `weston_10.0.2.bbappend` explicitly skips that Weston recipe when the relevant ZynqMP/Mali-400/libmali conditions apply. Its reason is missing GLES 3 interfaces in this libmali arrangement, and it directs the build toward Weston 9.

This is stronger evidence than assuming the newest recipe present in the layer must be suitable. A packagegroup selects a capability; provider/version policy still decides the concrete implementation. Review the effective recipe selection for the intended image.

Do not fix this by merely renaming a library or bypassing the recipe check. The missing API is a runtime interface constraint. Either use the supported stack combination or validate a deliberate alternative stack.

## Lima is an alternative stack with its own contract

Mesa's Lima driver supports Mali-400 rendering through the open-source kernel/userspace stack. It uses a different interface arrangement from the proprietary Mali module and libraries. Mesa also needs display sharing integration because the GPU itself does not control scanout. [Mesa Lima documentation](https://docs.mesa3d.org/drivers/lima.html).

Switching requires coordinated kernel configuration, Mesa providers, EGL/GBM selection and compositor integration. It is not a one-file replacement for `libMali.so`. The current Mesa page describes project capabilities; it does not certify the exact Mesa version and vendor kernel shipped in this 2024.1 BSP.

Choose the stack using application requirements and measured behavior on the intended image. Keep a known-good image for comparison so a provider switch does not mix old and new libraries.

## Separate API support from renderer selection

A program can report successful OpenGL initialization while using a software renderer. Check the actual renderer and supported extensions. A successful EGL display connection alone does not prove that GPU work occurred.

If context creation fails, inspect API version and backend/configuration compatibility. If shaders fail, preserve compiler diagnostics and required language features. If output is correct but slow, inspect software fallback, uploads, overdraw and synchronization stalls before raising the GPU clock.

If corruption appears only during resize or shutdown, inspect object lifetime and synchronization. If the GPU works offscreen but presentation fails, move the investigation to buffer sharing and KMS rather than changing shader code.

> [!NOTE]
> **Not run on the reference setup:** proprietary or Lima rendering, stack switching and compositor compatibility tests. The release recipes and supplied package manifest were inspected directly.

## References

- Inspected BSP `meta-xilinx/meta-xilinx-core/recipes-graphics/mali/kernel-module-mali.bb`, `recipes-graphics/libgles/libmali-xlnx.bb` and `recipes-graphics/wayland/weston_10.0.2.bbappend`.
- [AMD UG1085, GPU chapter](https://docs.amd.com/api/khub/documents/xzMsp_c5sG9J6A3u7NkJYQ/content), Mali-400 architecture/API generation.
- [Mesa Lima documentation](https://docs.mesa3d.org/drivers/lima.html), alternative stack and rendering/display separation.

- DS891 device-family feature tables
- `meta-xilinx@rel-v2024.1`, Mali recipes
- [Mesa Lima documentation](https://docs.mesa3d.org/drivers/lima.html)

---

<sub>← [Display Subsystem and DRM/KMS](01-display-subsystem-and-drm-kms.md) · [Chapter index](README.md) · [Windowing Systems and UI Frameworks](03-windowing-systems-and-ui-frameworks.md) →</sub>
