# GStreamer

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## Pipeline model

GStreamer connects elements through pads. **Caps** describe negotiated media formats. A pipeline controls state and timing; its bus reports errors, state changes and end-of-stream events. Applications must process those messages rather than waiting forever after a failure.

A capture-to-network design typically connects capture, conversion if required, encoder, RTP payloader and UDP sink. A display path uses a compatible sink instead. Every link needs compatible formats and memory types.

## Tools and plugins

`gst-inspect-1.0` describes installed elements and properties. `gst-launch-1.0` is useful for experiments. Plugin collections called base, good, bad and ugly describe project groupings; the names are not a complete security or license assessment.

Use `GST_DEBUG` and pipeline graphs to find negotiation and state failures. Add queues deliberately: they can isolate threads but also increase latency and memory use. DMABUF can avoid copies only when adjacent elements support compatible buffers.

`appsrc` and `appsink` connect application data to a pipeline. Handle timestamps, backpressure and buffer lifetime in C or Python.

> [!NOTE]
> **Not run on the reference setup:** hardware capture/encode pipelines and latency measurement.

## References

- GStreamer Application Development Manual, pipeline, caps and bus sections
- Reference PetaLinux GStreamer packagegroups

---

<sub>← [Media Controller and Tools: media-ctl, v4l2-ctl, yavta](02-media-controller-and-tools.md) · [Chapter index](README.md) · [VCU: Video Codec Unit](04-vcu-video-codec-unit.md) →</sub>
