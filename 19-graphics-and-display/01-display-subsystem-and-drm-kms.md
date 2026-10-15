# Display Subsystem and DRM/KMS

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[19 · Graphics and Display](README.md)** · Part IX: Graphics and Multimedia

## Rendering and scanout

The display controller sends pixels to an output; a GPU renders pixels. These are separate jobs. ZynqMP's DisplayPort subsystem can use memory-backed and supported live-video paths, depending on the hardware design and driver configuration.

**Direct Rendering Manager / Kernel Mode Setting (DRM/KMS)** models display resources:

| Object | Role |
| --- | --- |
| Framebuffer | Pixel storage description |
| Plane | Image layer feeding display composition |
| CRTC | Display timing and scanout pipeline |
| Encoder | Output encoding path |
| Connector | Physical/logical display connection |

The `zynqmp_dpsub` driver connects the PS display hardware to this framework. PL video mixers and HDMI/SDI pipelines need their own compatible drivers and graph description.

## Diagnosis

Check connector status, advertised modes, pixel format, stride and buffer layout. `modetest` can inspect KMS resources; `kmscube` additionally exercises rendering integration. A working test pattern does not prove that every GPU path works.

> [!NOTE]
> **Not run on the reference setup:** physical display output or hotplug testing.

## References

- Linux 6.6 [DRM/KMS](https://docs.kernel.org/6.6/gpu/drm-kms.html)
- `linux-xlnx@xilinx-v2024.1:drivers/gpu/drm/xlnx/`

---

<sub>[Chapter index](README.md) · [Arm Mali-400 MP2 GPU](02-mali-gpu.md) →</sub>
