# Media Controller and Tools: media-ctl, v4l2-ctl, yavta

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## A video node is only one part of a graph

The **media controller** interface describes the devices and connections that form a media pipeline. An entity represents a functional block. A pad is an input or output connection point. A link joins pads. A video node is usually where a stream enters or leaves memory; a subdevice exposes controls and pad formats for a component along the route.

The graph has two kinds of information. Topology says which connections exist. Configuration says which links are active and which format each pad carries. A route can exist in the device tree yet be unusable because one component did not probe. It can also be fully registered but have incompatible active formats.

The 2024.1 Xilinx video pipeline implementation lives in `xilinx-vipp.c`. It parses the graph and uses asynchronous subdevice matching before completing the pipeline. This is why a missing sensor clock or an unresolved endpoint can appear as a missing media route rather than a clear video-stream error. [Pinned pipeline source](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/media/platform/xilinx/xilinx-vipp.c).

## Give each tool a clear job

| Tool | Main question | What it cannot prove alone |
| --- | --- | --- |
| `media-ctl` | Which entities, pads, links and pad formats exist? | That pixels reach memory |
| `v4l2-ctl` | What does a video node support and return? | That all upstream blocks are correctly routed |
| `yavta` | How does a low-level capture queue behave? | That a complete display or codec application is correct |
| GStreamer | Can negotiated buffers move through an application graph? | That the underlying hardware graph was configured correctly |

Select tools that the image actually includes. These programs are separate packages, not commands provided by the Linux kernel. Confirm the selected recipes and image manifest in PetaLinux rather than assuming a full desktop multimedia installation.

Do not identify a camera only as `/dev/video0`. Enumeration order can change when a driver loads earlier or an additional capture device is present. Match the media entity, driver and bus path, then resolve its device node. Save that mapping with the test report.

## Configure an illustrative pipeline in dependency order

Consider this original topology:

```text
sensor source -> receiver sink/source -> scaler sink/source -> DMA sink -> video node
```

First identify physical input timing and the sensor's supported format. Next set the receiver input to that bus format. Set the scaler's input format to match its upstream output, then choose the scaler output size. Finally negotiate the memory format at the DMA video node.

The format name on an internal media bus and the memory pixel format are different namespaces. A bus code describes samples crossing a hardware connection. A V4L2 FourCC describes how image data is stored for userspace. You cannot copy a numeric value between them and expect a valid conversion.

For a hypothetical 1920 × 1080 sensor scaled to 1280 × 720, the receiver and scaler sink can stay at the sensor size while the scaler source and memory endpoint use the smaller size. Setting every pad to 1280 × 720 can be wrong because the sensor still sends 1920 × 1080. Read back each accepted format after configuration.

Some links are immutable because hardware wiring fixes them. Others can be enabled or disabled through the media API. A userspace link operation cannot add a missing PL wire or change a hardware block's compiled data width. The FPGA design and Linux graph must describe the same system.

## ACTIVE and TRY have different purposes

Subdevice format operations distinguish active configuration from a trial configuration. Trial operations allow negotiation without changing a running device's active state. This supports applications that need to explore a valid combination before committing it.

Do not assume that changing a sink format leaves all other pads unchanged. Drivers may propagate format restrictions across a block. A scaler, converter or receiver can adjust another pad or reject a combination. Read back the entire affected route, including crop and compose rectangles where those interfaces exist.

Keep frame rate and selection rectangles with dimensions. A correct width and height do not prove the expected frame interval. A crop changes the sampled area; scaling changes its output size. Confusing those operations can produce a valid image that covers the wrong part of a scene. [Subdevice userspace API](https://www.kernel.org/doc/html/v6.6/userspace-api/media/v4l/dev-subdev.html).

## Separate discovery from stream tests

A useful test record has four layers. First, record registered entities and links. Second, record accepted pad and memory formats. Third, record a short capture with buffer count, sequence numbers and payload sizes. Fourth, inspect the content using a known layout and color interpretation.

For the third layer, choose a bounded capture that can return every queued buffer. A viewer that blocks on a missing display can hide a healthy capture device. For the fourth, a raw file has no automatic knowledge of stride, range or matrix. Store this metadata beside the file or use a container that records the needed information.

Repeated starts and stops matter. A first stream can succeed while a second fails because the previous application left a downstream consumer active or the driver did not fully unwind an error path. Test reconfiguration separately from initial startup. Both must preserve buffer ownership and graph locking.

## Find the first inconsistent boundary

If a media entity is absent, begin with probe dependencies, clocks, resets, device-tree endpoints and the driver binding. If all entities exist but link validation fails, compare the two pads on each active link. If streaming begins but no buffers finish, inspect source activity and the DMA endpoint. This order avoids changing several unrelated layers at once.

The DMA implementation's `xvip_dma_verify_format()` is an exact place to understand which endpoint comparison fails in this release. Read the returned error together with the connected subdevice's active format. Avoid turning a format check off merely to force stream startup; a mismatch can mean the memory writer will interpret line boundaries incorrectly.

If a route works at a lower rate, distinguish memory-bandwidth pressure from pixel-clock or line-timing limits. The first affects queueing and completion under load. The second may break framing before the first valid image. A reduced workload is evidence only when you record what changed.

> [!NOTE]
> **Not run on the reference setup:** `media-ctl`, `v4l2-ctl` and `yavta` against a physical PL video pipeline. No board-specific entity name or successful capture output is invented here.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/media/platform/xilinx/{xilinx-vipp,xilinx-dma}.c`, inspected registration and validation paths.
- [Linux 6.6 media controller API](https://www.kernel.org/doc/html/v6.6/userspace-api/media/mediactl/media-controller.html).
- [v4l-utils upstream source](https://git.linuxtv.org/v4l-utils.git/), source of `media-ctl` and `v4l2-ctl`; use the version selected by the image recipe.

---

<sub>← [V4L2 Fundamentals](01-v4l2-fundamentals.md) · [Chapter index](README.md) · [GStreamer](03-gstreamer.md) →</sub>
