# GStreamer

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## Data, negotiation and control use the same graph

**GStreamer** connects elements through pads. Buffers carry data. Caps describe the format and its constraints. Events carry stream information such as segment boundaries and end of stream. Queries ask downstream elements about capabilities, allocation and other requirements. The application bus reports messages such as errors and state changes.

A pipeline can be syntactically valid yet fail during negotiation. It can negotiate successfully yet fail when a hardware element allocates memory or starts a device. Separate these stages when you read an error: element creation, linking, caps negotiation, allocation, device startup and steady streaming.

On ZynqMP, GStreamer sits above the kernel media graph and the installed codec stack. A `v4l2src` element does not replace the need to configure PL subdevice routes. A codec plugin cannot create VCU hardware on a device that does not contain it. The selected plugins must match the image's libraries and drivers.

## A caps filter does not perform a conversion

In an original teaching flow, a camera produces NV12 frames while an application asks for RGB. A caps filter can restrict acceptable formats, but it cannot transform NV12 pixels into RGB pixels. An element with a real conversion implementation must do that work. If every element advertises only incompatible formats, negotiation should fail.

Caps describe more than a media type. Width, height, frame rate, color information and memory features can all matter. Two pads may both say `video/x-raw` but still disagree about layout or memory type. Caps features such as DMABUF memory require compatible support on both sides; a compatible pixel name alone is insufficient.

Read pad templates to learn possible formats, then inspect negotiated caps to learn the chosen format. The first is a capability set; the second is a runtime decision. A plugin installed from a different release can change either. [GStreamer negotiation design](https://gstreamer.freedesktop.org/documentation/additional/design/negotiation.html).

## Allocation can break a supposed zero-copy path

A buffer pool decides where reusable buffers come from. An allocator controls the memory object. Buffer metadata can describe plane offsets and strides. A downstream hardware element may need alignment, contiguous addressing or a particular memory feature. Allocation negotiation has to satisfy those requirements in addition to caps negotiation.

Consider a camera buffer passed to an encoder and display. If the encoder accepts the camera's allocation but the display needs a different tiled format, at least one branch needs conversion or a new allocation. Passing a file descriptor along the graph does not prove that every stage uses the same physical storage.

Track the allocation owner and final release. The source can reuse a buffer only after every downstream reference is released. A branch that stores old samples can retain the capture pool and stall the entire pipeline. This may look like a camera timeout even though the real issue is application lifetime management. [GStreamer allocation design](https://gstreamer.freedesktop.org/documentation/additional/design/bufferpool.html).

## Queues trade memory and latency for scheduling freedom

A queue provides a thread boundary and a finite place to hold data. It allows upstream and downstream work to overlap, but a full queue applies back pressure unless its policy drops data. A queue does not fix a consumer that is permanently slower than the source.

For an illustrative 60-frame/s stream, a branch that keeps four complete frames can add about `4 / 60 = 66.7 ms` of queued time. This is a queueing estimate, not an end-to-end latency measurement. Acquisition, codec reordering, display scheduling and network buffering add their own delay.

For live preview, dropping old frames may be better than showing an increasingly old scene. For evidence recording, silent loss may be unacceptable. Choose queue limits and drop policy from the application's meaning, then count drops. Do not use an unbounded application list as an accidental queue.

After a `tee`, each branch usually needs scheduling independence. Otherwise a blocking sink on one branch can hold the thread that should feed the other. Even with separate queues, shared capture buffers remain a common resource. Thread separation and buffer-lifetime separation are different concerns.

## Time and state transitions explain many surprises

A pipeline moves through NULL, READY, PAUSED and PLAYING. Some resources appear only during state changes. Non-live sources commonly preroll before playback; live sources cannot provide normal paused data in the same way. An application must handle asynchronous state transitions and bus errors rather than assume every state request completes immediately.

Timestamps are interpreted against a segment and pipeline clock. A raw source timestamp, encoded presentation timestamp and physical display time are different observations. Measure end-to-end latency with a common event or a controlled clock relationship. The number shown by one sink is not automatically total camera-to-display latency.

For an encoded recording, send and wait for end of stream when the application requires a clean container close. An immediate process kill can leave delayed codec data or container metadata unwritten. Stopping capture, draining an encoder and finalizing a file are separate operations. [GStreamer states](https://gstreamer.freedesktop.org/documentation/additional/design/states.html).

## Build the pipeline in testable stages

First prove source negotiation and bounded capture without encoding or display. Next prove the encoder using known input. Then join the two while watching allocation and queue pressure. Add the network or container sink last. This preserves a working comparison when the combined graph fails.

Keep the exact plugin names, versions, negotiated caps, element properties and selected device nodes with the result. The installed recipe family matters in PetaLinux 2024.1: AMD's VCU stack includes vendor control and OpenMAX libraries, so a generic upstream V4L2 codec example may describe a different integration.

A `not-negotiated` error calls for caps and pad investigation. An allocation failure calls for pool sizes, memory features and device constraints. A steady stream with growing delay calls for queue and timestamp inspection. High CPU use calls for identifying software conversion or copies before changing the kernel.

> [!NOTE]
> **Not run on the reference setup:** hardware GStreamer pipelines and latency measurements. The frame-delay calculation and pipeline descriptions are explanatory examples, not captured target results.

## References

- [GStreamer application manual](https://gstreamer.freedesktop.org/documentation/application-development/), bus handling, pads and application state control.
- Inspected `xilinx-zcu106-2024.1:components/yocto/layers/meta-xilinx/meta-xilinx-core/recipes-multimedia/vcu/` and the adjacent `gstreamer/` recipe directory.
- [VCU software integration](04-vcu-video-codec-unit.md) and [V4L2 buffer ownership](01-v4l2-fundamentals.md).

---

<sub>← [Media Controller and Tools: media-ctl, v4l2-ctl, yavta](02-media-controller-and-tools.md) · [Chapter index](README.md) · [VCU: Video Codec Unit](04-vcu-video-codec-unit.md) →</sub>
