# Audio (Overview)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## Audio stack

**Advanced Linux Sound Architecture (ALSA)** provides audio device and control interfaces. A working PCM device needs compatible sample format, rate, channel count and clocking. Mixer routing can mute a valid stream even when data transfer succeeds.

DisplayPort audio and PL I2S paths use different hardware routes. For an I2S design, check clock master/slave roles, bit clock, frame clock and codec configuration. Device-tree audio links must describe the actual wiring.

## Integration

The inspected audio packagegroup includes ALSA libraries and tools, SoX, and conditional PulseAudio support. Installing userspace tools does not create a missing kernel sound device.

GStreamer audio pipelines add format negotiation and clock selection. When combining audio and video, choose a clear timing source and measure drift over a long run.

> [!NOTE]
> **Not run on the reference setup:** physical audio playback, capture or audio/video synchronization.

## References

- Inspected `meta-petalinux@rel-v2024.1:recipes-core/packagegroups/packagegroup-petalinux-audio.bb`
- Linux 6.6 ALSA/ASoC documentation

---

<sub>← [VCU: Video Codec Unit](04-vcu-video-codec-unit.md) · [Chapter index](README.md) · Next chapter: [21 · RPU and OpenAMP](../21-rpu-and-openamp/README.md) →</sub>
