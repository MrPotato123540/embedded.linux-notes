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

## A framebuffer object is not the pixel allocation

A DRM framebuffer describes how pixel data is stored: dimensions, format, per-plane pitches and offsets, and associated memory objects. The underlying allocation has its own lifetime. Creating a framebuffer does not necessarily allocate new pixel storage, and removing its userspace handle does not mean every hardware or kernel reference has finished.

A plane selects a framebuffer and describes source/destination rectangles. A CRTC provides display timing and combines the relevant scanout state. An encoder and connector connect that timing stream to an output. These software objects model the display pipeline; they are not interchangeable with a GPU rendering context.

A pixel format identifier describes channel layout. A format modifier can describe tiling or compression where supported. Two devices may support the same logical color format but not the same memory layout. Successful buffer sharing therefore needs agreement on both storage and synchronization.

## Follow one frame from producer to display

The producer first obtains a buffer and writes pixels, either through the CPU or a rendering device. The display controller must not read it before production completes and the relevant synchronization is satisfied. Userspace then requests scanout of that framebuffer through the supported KMS interface.

The old buffer cannot be reused while display hardware still scans it. A completion event or fence, under the selected interface's contract, tells the application when the transition makes reuse safe. Merely returning from a nonblocking submission is not enough.

Double buffering separates the buffer being displayed from the one being prepared. A third buffer can improve scheduling flexibility but adds memory use and can increase queueing latency. Buffer count should follow the application's latency policy rather than a generic “more is faster” rule.

## Atomic state is a capability, not an assumption

The DRM atomic model lets userspace propose a related set of object changes and validate them together. A test-only request can check constraints without applying the state when the driver and interface support it. Real resources still impose limits: scaling, formats, bandwidth and available planes.

The existence of generic atomic helpers in Linux documentation does not prove that every vendor pipeline exposes the same userspace capabilities. Inspect the actual driver and advertised interface. The pinned AMD tree includes both framework-specific pipeline code and display helpers; avoid applying instructions written for a different upstream revision without review.

Object IDs are discovered at runtime. Do not hard-code a connector or CRTC number from one boot log. Hotplug and different driver composition can change the available topology.

## The 2024.1 ZynqMP source has two ordering rules

In `zynqmp_dpsub_probe()`, the DisplayPort subdriver is probed before the display subdriver so that output-format information is available. Later, `zynqmp_dpsub_bind()` binds the display component before the DisplayPort component so the encoder can find its CRTC.

These are different lifecycle stages with different dependency order. A log that says the subsystem probed does not by itself prove that every component bound and a usable DRM pipeline appeared. The driver also populates sound child devices and handles an external-CRTC arrangement separately.

Removal reverses the relevant relationships, depopulates child devices, releases reserved-memory association and disables runtime power-management integration. This source walkthrough shows why a display subsystem cannot be understood as one register block with one enable bit.

## Stride and bandwidth make a concrete constraint

For an illustrative 1920×1080 buffer with four bytes per pixel and no additional row padding, each frame occupies 8,294,400 bytes. At 60 frames/s, one full scanout reads 497,664,000 bytes/s of pixel data before additional traffic and protocol effects. This is a calculated lower-level payload model, not a measured ZCU106 limit.

Actual pitch can exceed width times bytes-per-pixel because of alignment. Multiplanar formats have separate offsets and strides. A CPU producer that advances by the visible width instead of the actual pitch can create diagonal corruption or repeated rows even though the KMS mode is correct.

Rendering, video capture and PL DMA add memory traffic. A display underflow can result from shared bandwidth pressure, not only an invalid display clock. Keep the complete pipeline active during product performance tests.

## DMA-BUF shares memory, not automatic correctness

DMA-BUF lets drivers share buffer objects through file descriptors. Each importing device still needs a supported mapping and layout. A shared file descriptor does not imply that both devices can use every modifier or address range.

Synchronization tells readers when the producer finished. CPU access also needs the exporter's supported cache-access protocol. Do not treat a CPU mmap of a shared buffer as permission to modify it while a GPU or display controller uses it.

Releasing the application's file descriptor drops one reference. Attachments, mappings, queued work and framebuffer objects can hold others. A leak investigation should follow those references rather than only count application allocations.

## Diagnose from output connection to pixels

A disconnected connector points first to cable, hotplug and physical link detection. A connected connector with no usable mode points to mode discovery and link constraints. A valid mode with a blank frame points to plane state, buffer content or format. Tearing or occasional corruption points to synchronization, buffer reuse or bandwidth.

A CPU-filled test pattern validates a useful scanout path without proving GPU rendering. A rendered offscreen image validates rendering without proving DisplayPort output. Use those independent tests to isolate the failing boundary.

> [!NOTE]
> **Not run on the reference setup:** physical modesetting, hotplug, DMA-BUF interchange or bandwidth tests. Driver/source inspection and calculated memory examples are the evidence here.

## References

- [linux-xlnx@xilinx-v2024.1:drivers/gpu/drm/xlnx/zynqmp_dpsub.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/gpu/drm/xlnx/zynqmp_dpsub.c) and [zynqmp_disp.c](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/gpu/drm/xlnx/zynqmp_disp.c).
- Pinned [DRM memory management](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/gpu/drm-mm.rst) and [DMA-BUF documentation](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/Documentation/driver-api/dma-buf.rst).

- Linux 6.6 [DRM/KMS](https://docs.kernel.org/6.6/gpu/drm-kms.html)
- `linux-xlnx@xilinx-v2024.1:drivers/gpu/drm/xlnx/`

---

<sub>[Chapter index](README.md) · [Arm Mali-400 MP2 GPU](02-mali-gpu.md) →</sub>
