# V4L2 Fundamentals

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## V4L2 objects

**Video4Linux2 (V4L2)** provides interfaces for video capture, output and related devices. A video node exposes a stream interface. Subdevices describe components such as sensors and processing blocks. Pads and links describe how those components connect.

A format includes more than width and height. Pixel encoding, planes, stride, field order and color information must agree across the pipeline. A buffer with the right byte count can still have the wrong layout.

## Buffer ownership

MMAP lets applications map driver-managed buffers. USERPTR supplies userspace memory where supported. DMABUF exchanges buffer handles between participating drivers. Support is device-specific; these modes are not interchangeable guarantees of zero-copy.

Queue a buffer, let the device own it during capture/output, then dequeue before reading or reusing it. Respect returned sizes, timestamps and error flags.

The Xilinx video pipeline integrates PL video components through its media graph and bindings. Check the actual topology and IP configuration before choosing a userspace format.

## References

- Linux 6.6 V4L2 userspace API and media-controller documentation
- `linux-xlnx@xilinx-v2024.1:drivers/media/platform/xilinx/`

---

<sub>[Chapter index](README.md) · [Media Controller and Tools: media-ctl, v4l2-ctl, yavta](02-media-controller-and-tools.md) →</sub>
