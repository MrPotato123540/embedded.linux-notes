# VCU: Video Codec Unit

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## The VCU is one stage in a larger system

The **Video Codec Unit (VCU)** provides hardware video encoding and decoding on suitable Zynq UltraScale+ MPSoC EV devices. The ZCU106's device supports this subsystem, but a usable video design still needs the right hardware configuration, clocks, memory path, driver, firmware and userspace libraries. A board name is not a complete video-system configuration.

Encoding consumes raw pictures and produces a compressed bitstream. Decoding consumes a compressed bitstream and produces pictures. Capture, scaling, color conversion, display and network transport are separate jobs. A VCU pipeline can therefore fail outside the codec even when the encoder itself works.

The installed PetaLinux 2024.1 recipes provide a useful map of the actual stack. They explicitly require the `vcu` machine feature. Selecting a package name alone does not satisfy that requirement or supply the matching hardware design.

## Follow the release's dependency chain

| 2024.1 recipe | Role | Inspected dependency or input |
| --- | --- | --- |
| `kernel-module-vcu_2024.1.bb` | Out-of-tree kernel modules | `vcu-modules`, pinned `SRCREV`; depends at runtime on firmware |
| `vcu-firmware_2024.1.bb` | Codec firmware binaries | Installs `al5d*.fw` and `al5e*.fw` under `/lib/firmware` |
| `libvcu-xlnx_2024.1.bb` | Codec control software | Depends at runtime on VCU kernel modules |
| `libomxil-xlnx_2024.1.bb` | OpenMAX integration libraries | Build dependency on `libvcu-xlnx` |

These files were inspected under `meta-xilinx/meta-xilinx-core/recipes-multimedia/vcu/`. The module recipe pins `91d19a16308a438596138d30d8174e148fc45584`; the firmware recipe pins `6ee1998c53817ab0c137b8b99089337d5caba62c`. Record the resolved recipes and overrides for an actual build; the directory also contains older release recipes.

This matters when debugging an application that cannot open an encoder. Begin with the device and kernel module, then firmware load, then the control library, then the media plugin. Replacing only a plugin can leave an incompatible lower stack unchanged. A source package version is not proof that the running root filesystem contains that package.

## Raw bandwidth and encoded bandwidth are different budgets

For an illustrative 3840 × 2160, 60-frame/s, 8-bit NV12 source without padding, one frame contains `3840 × 2160 × 1.5 = 12,441,600` bytes. One memory pass is `746,496,000` bytes/s. A capture write plus an encoder read already accounts for roughly 1.49 GB/s of payload traffic.

That calculation excludes reference pictures, reconstructed pictures, alignment, display access and other masters. It is not a VCU performance guarantee. A 20-Mbit/s encoded output, for example, would be only 2.5 MB/s before transport overhead, yet the raw-memory traffic would remain large. Compressing the output does not remove the input bandwidth requirement.

Ten-bit formats need their actual packing rule. Do not replace 8 by 10 in a byte count unless the selected layout truly packs samples that way. Some formats store samples in wider words; others use a specialized packed or tiled layout. Use the software stack's accepted stride and buffer-size requirements.

## Codec settings change both quality and system behavior

A **group of pictures (GOP)** defines a pattern of intra and predicted pictures. Reference pictures stay alive because later pictures need them. Bidirectional prediction can require reordering. These choices change memory use and delay, not only compression ratio.

A rate-control target is also not a maximum for every individual frame. An intra picture may be much larger than an average predicted picture. Transport queues and storage must tolerate this variation. A link sized only for average bitrate can lose data during a burst even when long-term bandwidth looks sufficient.

Low latency requires a complete configuration: acquisition buffering, codec reference/reordering policy, look-ahead where used, transport queues and receiver buffering. Disabling one codec feature cannot remove time already stored in a capture queue. Evaluate picture quality and bitrate stability together with delay.

Codec profile, level, chroma format, bit depth and resolution must be accepted by both encoder and decoder. A valid H.264 or H.265 stream can still be unsuitable for a specific receiver. Preserve the encoded stream's headers and the receiver's supported mode when analyzing compatibility.

## Treat each buffer class separately

Raw input pictures, internal reference pictures and compressed output buffers have different lifetimes. An input picture may be returned after the codec finishes reading it, while internal reconstruction data must remain for later frames. Output capacity must account for variable-size compressed data.

A frame counter at input is not a complete output check. Compare presentation timestamps, output picture order, codec errors and decoded content. When stopping, drain delayed pictures through the supported API. Closing the application immediately after the last raw submission may discard valid encoded data still in flight.

Shared buffers also require matching memory contracts. A capture DMABUF is useful only if the codec stack accepts its alignment, addressability and layout. A successful import can still involve additional internal buffers. Describe the observed copy path precisely rather than labeling the whole application zero-copy.

## Separate hardware, firmware and stream failures

A missing device suggests hardware description, module loading or probe dependencies. A firmware request error points to firmware packaging or path/version problems. Allocation errors suggest a memory requirement or mapping limit. Failures only on a specific encoded stream suggest unsupported stream parameters or damaged data.

If performance falls only when display and capture run together, compare total memory traffic and concurrent workload. If failures occur after repeated starts, inspect resource release and outstanding buffers. If images decode with wrong colors, inspect raw layout and color metadata before changing codec rate control.

Keep the hardware export, bitstream, kernel/modules, firmware, control libraries and plugin versions as one release record. The module recipe is an out-of-tree build tied to the selected kernel build, so a kernel update also needs a module compatibility review.

> [!NOTE]
> **Not run on the reference setup:** VCU hardware encode/decode, throughput, quality and power measurements. Recipe dependencies and source revisions were inspected locally. The bandwidth numbers are original calculations.

## References

- Inspected `xilinx-zcu106-2024.1:components/yocto/layers/meta-xilinx/meta-xilinx-core/recipes-multimedia/vcu/*_2024.1.bb`.
- [AMD VCU modules, 2024.1 recipe revision](https://github.com/Xilinx/vcu-modules/tree/91d19a16308a438596138d30d8174e148fc45584).
- [AMD VCU control software, 2024.1 recipe revision](https://github.com/Xilinx/vcu-ctrl-sw/tree/940f9fa933402de6f959911c236f36add5dd3a40).
- AMD PG252, *H.264/H.265 Video Codec Unit*, configuration and interface description; use the document revision matching the exported IP.

---

<sub>← [GStreamer](03-gstreamer.md) · [Chapter index](README.md) · [Audio (Overview)](05-audio.md) →</sub>
