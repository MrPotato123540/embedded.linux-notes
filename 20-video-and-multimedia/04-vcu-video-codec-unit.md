# VCU: Video Codec Unit

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## VCU responsibilities

The **Video Codec Unit (VCU)** in supported EV devices provides H.264/H.265 encoding and decoding. It is distinct from the Mali GPU and the display controller. Device variant, hardware design and software support must all match.

The AMD stack can include the Allegro driver, codec-control software, OpenMAX IL integration and `gst-omx`. Exact components depend on the release and image. Check installed plugins rather than assuming a generic GStreamer encoder uses the VCU.

## Encoder trade-offs

Rate control balances bitrate and quality. Group-of-pictures structure affects compression, recovery and latency. Buffering and frame reordering can add delay even when the hardware processes frames quickly.

Validate the complete capture → encode → transport → decode/display path. Record format, frame rate, bitrate, dropped frames and end-to-end latency. A codec-only benchmark does not measure the user's viewing delay.

> [!NOTE]
> **Not run on the reference setup:** physical VCU encoding/decoding and supported-mode validation. No universal throughput limit is inferred from the device-family name.

## References

- AMD PG252, VCU product guide matching the hardware IP release
- Reference PetaLinux VCU/OpenMAX recipes

---

<sub>← [GStreamer](03-gstreamer.md) · [Chapter index](README.md) · [Audio (Overview)](05-audio.md) →</sub>
