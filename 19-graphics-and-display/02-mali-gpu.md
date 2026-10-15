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

## References

- DS891 device-family feature tables
- `meta-xilinx@rel-v2024.1`, Mali recipes
- [Mesa Lima documentation](https://docs.mesa3d.org/drivers/lima.html)

---

<sub>← [Display Subsystem and DRM/KMS](01-display-subsystem-and-drm-kms.md) · [Chapter index](README.md) · [Windowing Systems and UI Frameworks](03-windowing-systems-and-ui-frameworks.md) →</sub>
