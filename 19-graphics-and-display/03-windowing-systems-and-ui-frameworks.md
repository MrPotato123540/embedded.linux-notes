# Windowing Systems and UI Frameworks

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[19 · Graphics and Display](README.md)** · Part IX: Graphics and Multimedia

## Choose the display model

| Stack | Typical fit |
| --- | --- |
| Wayland with Weston or another compositor | Multiple clients and controlled composition |
| X11 | Applications depending on the X ecosystem |
| Direct KMS/EGL path | A controlled single-application display |

Qt chooses its platform integration through plugins. The selected plugin, EGL implementation and kernel display driver must agree. A Qt application can run without hardware acceleration, so verify the renderer rather than assuming acceleration from smooth startup.

## Product considerations

Decide how the display handles application crashes, input devices, rotation, multiple screens and remote maintenance. Test startup without a connected display and reconnection later. Keep font, input and graphics dependencies in the image recipe.

A smaller stack can reduce startup and maintenance cost, but may need more application-side work for window management or recovery.

> [!NOTE]
> **Not run on the reference setup:** compositor and Qt platform-plugin validation on hardware.

## References

- Qt platform abstraction and embedded Linux documentation for the selected Qt release
- Reference `meta-qt5` and PetaLinux display packagegroups

---

<sub>← [Arm Mali-400 MP2 GPU](02-mali-gpu.md) · [Chapter index](README.md) · Next chapter: [20 · Video and Multimedia](../20-video-and-multimedia/README.md) →</sub>
