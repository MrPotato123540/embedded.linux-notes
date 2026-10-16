# V4L2 Fundamentals

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## Follow one frame through the system

**Video4Linux2 (V4L2)** is the Linux interface for capture, output and many video-processing devices. A `/dev/video*` node is an access point to a driver. It is not a complete description of the camera or the programmable logic (PL) pipeline. A sensor, receiver, scaler and memory writer can be separate objects with separate format settings.

Consider an original teaching design: a camera sends pixels through a PL color converter into a memory writer. The camera controls timing. The converter controls pixel meaning. The memory writer controls stride and buffer placement. The application controls how many empty buffers are available. A visible frame needs all four parts to agree.

On ZynqMP, the Xilinx pipeline driver uses the media graph to connect subdevices and video DMA endpoints. In the inspected 2024.1 kernel, `xvip_dma_verify_format()` checks the memory endpoint against the connected subdevice. `xvip_dma_start_streaming()` participates in pipeline startup. The existence of a video node does not mean that this later check will succeed. [Pinned implementation](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/media/platform/xilinx/xilinx-dma.c).

## Negotiate the complete layout

Start with device capabilities and supported formats. A request passed to `VIDIOC_S_FMT` is a request, not a promise. The driver returns the accepted format, which may change dimensions, stride or plane sizes. Allocate and interpret buffers from that returned result.

Keep these values separate:

| Value | What it describes | Common mistake |
| --- | --- | --- |
| Width and height | Visible pixel dimensions | Treating width as bytes per line |
| Pixel format | Component order and storage layout | Reading YUV data as RGB |
| `bytesperline` | Distance between line starts | Ignoring alignment padding |
| `sizeimage` | Required image storage | Allocating only visible bytes |
| `bytesused` | Payload reported for this buffer | Treating capacity as valid payload |
| Color information | Matrix, range and transfer interpretation | Calling a color mismatch corruption |

A multi-planar API buffer contains a `v4l2_plane` array. Its `length` field counts plane entries; in the single-planar API, buffer length is a byte capacity. Multiple color components do not automatically mean multiple memory allocations. For example, contiguous NV12 and multi-planar NV12 variants have different storage contracts. Inspect the negotiated format rather than inferring the API from the image's appearance. [Linux 6.6 buffer API](https://www.kernel.org/doc/html/v6.6/userspace-api/media/v4l/buffer.html).

## Work a memory calculation

Take an illustrative 1920 × 1080 NV12 image with no padding. Its Y plane uses `1920 × 1080 = 2,073,600` bytes. Interleaved chroma uses half that amount, so a frame uses `3,110,400` bytes. At 60 frames/s, one full-frame write is `186,624,000` bytes/s. A later full read adds the same traffic before any extra processing.

These are calculated payload values, not board measurements. If the driver returns a 2048-byte stride for both planes and the same visible height, storage becomes `2048 × 1080 × 1.5 = 3,317,760` bytes. Six such buffers need `19,906,560` bytes, plus alignment and other driver allocations. Always use returned sizes for real allocation; some formats also pad height or use tiled layouts.

This calculation explains two different failures. Allocation can fail because the required memory cannot be supplied. A stream can also allocate correctly but lose frames because total memory traffic exceeds the available service rate. More buffers help absorb a short delay; they do not create sustained bandwidth.

## Buffer ownership is a state machine

The normal capture sequence is format negotiation, buffer allocation/import, queueing empty buffers, stream start, repeated dequeue/process/requeue, and stream stop. `VIDIOC_QBUF` hands a buffer to the driver. Successful `VIDIOC_DQBUF` returns it to the application. A mapped address stays accessible, but that does not give you permission to modify a buffer while the device owns it.

The inspected driver uses the videobuf2 framework. `xvip_dma_buffer_queue()` obtains DMA addresses and submits work; completion reaches `xvip_dma_complete()`, which records completion information and returns the buffer through videobuf2. CPU pointers, DMA addresses and file descriptors are different kinds of identifier.

If your application holds every completed buffer, capture eventually lacks empty buffers. A slow display branch can therefore stop capture even when the camera and DMA work correctly. Count outstanding buffers at each consumer. Returning a buffer before a downstream device finishes is the opposite failure: it allows new capture data to overwrite an image still in use.

MMAP maps driver-managed memory. USERPTR supplies application memory where the driver supports it. DMABUF shares an allocation through a file descriptor between supporting drivers. DMABUF avoids a copy only when both devices accept the same layout and memory constraints. It does not remove synchronization, cache maintenance or lifetime requirements.

## Changes and shutdown need ownership rules

Changing a layout can make existing buffers too small. A conservative reconfiguration stops streaming, releases old buffers, changes formats and controls, allocates buffers again, then restarts. The exact supported sequence comes from the driver's V4L2 contract. Do not reuse a previous `sizeimage` after a resolution or rotation change.

On shutdown, stop producers and wait for users of shared buffers before releasing allocations. A file descriptor close is not a substitute for understanding other processes or drivers that still hold references. For an encoder, draining delayed output is also separate from stopping raw capture.

## Diagnose from the last successful state

A format error at stream start suggests an inconsistent graph or unsupported layout. A successful start with no completions suggests missing upstream timing, DMA progress or interrupts. Completions with sequence gaps suggest lost frames or exhausted queues. Correct sequences with wrong colors suggest layout or color interpretation first.

Record the returned format, queue depth, sequence number, timestamp flags, payload size and error flags together. A timestamp can refer to different frame events and clocks; comparing it directly with wall-clock time can produce false latency results. An error-marked dequeued buffer must not silently become a valid application frame.

> [!NOTE]
> **Not run on the reference setup:** physical video capture, DMABUF exchange and sustained-bandwidth tests. The worked values are calculations. Driver and API paths were inspected; no successful target stream is claimed.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/media/platform/xilinx/xilinx-dma.c`, queue operations and format validation.
- `linux-xlnx@xilinx-v2024.1:Documentation/userspace-api/media/v4l/{buffer,vidioc-reqbufs,vidioc-qbuf}.rst`, inspected locally.
- [Linux 6.6 V4L2 userspace API](https://www.kernel.org/doc/html/v6.6/userspace-api/media/v4l/v4l2.html).

---

<sub>[Chapter index](README.md) · [Media Controller and Tools: media-ctl, v4l2-ctl, yavta](02-media-controller-and-tools.md) →</sub>
