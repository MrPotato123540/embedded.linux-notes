# Media Controller and Tools: media-ctl, v4l2-ctl, yavta

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## Inspect before streaming

`media-ctl` shows entities, pads and links. `v4l2-ctl` inspects video-node capabilities, formats and controls. `yavta` helps exercise capture, while `v4l2-compliance` checks interface behavior. The inspected PetaLinux v4lutils packagegroup includes v4l-utils and yavta.

## Camera pipeline walkthrough

For a MIPI CSI-2 camera design, trace sensor → receiver → processing blocks → capture DMA. First confirm sensor power, clock and control-bus communication. Then check endpoint wiring, lane configuration and media links.

Set compatible pad formats across the path before requesting capture buffers. Start with a supported low-complexity mode. Verify frame size, sequence numbers and timestamps before adding display or encoding.

Entity names and pad indices come from the actual graph. A command copied from another camera design can configure the wrong pad or fail even when the hardware is healthy.

> [!NOTE]
> **Not run on the reference setup:** a physical MIPI camera session. No invented entity names or successful capture output are supplied.

## References

- Linux 6.6 media-controller userspace API
- Inspected `packagegroup-petalinux-v4lutils.bb`

---

<sub>← [V4L2 Fundamentals](01-v4l2-fundamentals.md) · [Chapter index](README.md) · [GStreamer](03-gstreamer.md) →</sub>
