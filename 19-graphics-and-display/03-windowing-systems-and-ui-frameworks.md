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

## The compositor owns presentation policy

A window system coordinates application surfaces, input and display output. In a Wayland arrangement, clients submit buffers and the compositor decides how to combine or present them. The compositor normally owns the relevant display-control path for its session.

X11 uses a different client/server protocol and integration model. Xwayland can allow X11 applications inside a Wayland session, adding another component to the dependency chain. An application linked for X11 does not become a native Wayland client merely because Weston is running.

A direct fullscreen application can use a platform integration such as Qt EGLFS without a conventional desktop compositor. It still needs suitable device ownership, EGL support and input integration. Running it alongside another owner of the same display can fail even when each works alone.

## Follow one Wayland buffer

The client prepares a buffer and attaches it to a surface. A surface commit publishes pending state according to the protocol. The compositor can read the buffer, combine it with other surfaces or use it for a direct scanout path when constraints allow.

The client must not overwrite a buffer while the compositor uses it. The core `wl_buffer.release` event provides the relevant reuse notification for that buffer object. Frame callbacks serve a different purpose: they help pace production and do not replace buffer-release tracking. [Wayland protocol specification](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_buffer).

GPU-backed buffers add device synchronization. A released protocol object and a completed GPU job belong to related but distinct layers. Use the synchronization model supported by the actual protocol extensions, compositor and driver combination; do not assume explicit-fence support from a newer desktop stack.

## Composition can add memory traffic

Direct scanout can avoid composing a full intermediate image when one suitable surface can feed a plane. It depends on format, size, modifier, transform, visibility and driver constraints. A cursor, overlay or rotation can change the selected path.

GPU composition reads client buffers and writes a final output buffer. CPU composition uses a different processing path but still moves pixels. A benchmark with one fullscreen window can therefore perform differently from the product UI with translucent panels and video.

Frame rate alone does not reveal latency. A compositor can queue several frames and keep a smooth rate while user input appears late. Measure input-to-visible-result behavior where interaction matters, and record buffer count and presentation policy.

## The 2024.1 BSP constrains Weston selection

The PetaLinux Weston packagegroup requires the Wayland distribution feature and pulls in Weston, its startup integration, examples and Wayland protocol packages. It adds Xwayland when the X11 feature is selected.

The AMD `weston_10.0.2.bbappend` rejects the Mali-400/libmali combination because the required GLES 3 interfaces are unavailable and points to Weston 9. The same layer supplies a Weston 9 recipe. Therefore, “Weston exists in the layer” is not enough to select a compatible version.

The proprietary Mali recipe also chooses a window-system backend. A Wayland compositor needs the matching library/backend arrangement, not an X11 default selected elsewhere. Inspect effective provider/version/backend values as one configuration.

## A Qt application has several load stages

A Qt executable first needs its normal loader and shared libraries. It then selects a Qt Platform Abstraction plugin, which connects Qt to the native window system. Rendering modules may further load EGL/GLES and other plugins. A successful ELF startup can therefore be followed by a platform-plugin failure.

For an illustrative kiosk, decide whether Qt runs as a Wayland client or owns a direct fullscreen backend. Package the corresponding plugin and its runtime libraries. Keep the application's environment consistent with that choice and the selected GPU provider.

A plugin file can exist but fail to load because one of its dependent libraries is missing or incompatible. Inspect the complete dependency chain before copying more plugins into the directory. A broad plugin path containing several Qt versions can select an incompatible binary.

The pinned Qt 5.15.2 QPA documentation explicitly gives no source or binary compatibility guarantee for QPA classes. A custom platform plugin therefore needs its own compatibility review against the selected Qt build. Do not apply public Qt application-API compatibility assumptions to those internal platform interfaces.

## Session, input and permissions are dependencies

A compositor needs access to the appropriate display and input devices under the image's session policy. A service launched before those permissions and runtime directories exist can fail even though the same binary works from a login session.

Input-device discovery and touchscreen calibration are separate from rendering. A visible UI with no input should be diagnosed through input events, seat assignment and permissions rather than the graphics shader path. A rotated display may also need a matching input-coordinate transform.

Define who restarts the compositor and clients after failure. If the compositor exits, client connections and presentation objects become invalid. A robust kiosk reconnects or restarts through an explicit service dependency rather than retaining stale surface state.

## Diagnose in layers

First establish KMS output with a supported simple path. Then establish the GPU/EGL backend. Then start the intended compositor and inspect its selected renderer and outputs. Finally test the application and its platform plugin.

If the compositor starts but one client fails, inspect that client's protocol/plugin and libraries. If all clients show black content, inspect compositor rendering and buffer import. If content is correct until resize or hotplug, inspect object recreation and buffer lifetime. If only one desktop layout is slow, inspect composition and memory traffic.

> [!NOTE]
> **Not run on the reference setup:** Weston, X11/Xwayland, Qt UI, input and hotplug execution. The protocol rules and local 2024.1 packaging constraints were reviewed; no desktop performance result is claimed.

## References

- Inspected BSP `meta-petalinux/recipes-core/packagegroups/packagegroup-petalinux-weston.bb` and AMD `recipes-graphics/wayland/weston_10.0.2.bbappend`.
- [Wayland core protocol](https://wayland.freedesktop.org/docs/html/apa.html), surface commit, frame callbacks and buffer release.
- [Qt qtdoc@v5.15.2:QPA source documentation](https://github.com/qt/qtdoc/blob/v5.15.2/doc/src/platforms/qpa.qdoc), platform-plugin architecture; match the image's selected Qt provider.

- Qt platform abstraction and embedded Linux documentation for the selected Qt release
- Reference `meta-qt5` and PetaLinux display packagegroups

---

<sub>← [Arm Mali-400 MP2 GPU](02-mali-gpu.md) · [Chapter index](README.md) · Next chapter: [20 · Video and Multimedia](../20-video-and-multimedia/README.md) →</sub>
