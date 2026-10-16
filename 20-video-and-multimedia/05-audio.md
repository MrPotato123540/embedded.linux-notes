# Audio (Overview)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[20 · Video and Multimedia](README.md)** · Part IX: Graphics and Multimedia

## Follow samples from the application to the wire

Linux audio usually uses the **Advanced Linux Sound Architecture (ALSA)**. For embedded boards, **ALSA System on Chip (ASoC)** connects a CPU-side audio interface, a codec-side interface and board-specific routing. The board description must explain which ports connect, which clocks they use and which side supplies those clocks.

An audio codec here is a hardware converter or audio-interface device, not an H.264 video codec. It can convert digital samples to an analog output or convert microphone input to digital samples. HDMI or DisplayPort audio may instead remain digital through the external connection.

The application writes or reads **pulse-code modulation (PCM)** samples through an ALSA stream. The driver moves samples through a ring buffer, often using direct memory access (DMA). The interface serializes samples according to a format such as I2S. A working PCM device only proves registration; it does not prove an external clock, correct wiring or an audible route.

## Three clocks answer different questions

The sample clock sets frames per second. The bit clock shifts the bits of each frame. A master clock may feed codec internals and must follow that device's clocking rules. The CPU interface or external codec can supply the serial clocks depending on the design.

For an original stereo example, 48,000 frames/s with two 32-bit slots requires a `48,000 × 2 × 32 = 3,072,000 Hz` bit clock. The samples might contain only 24 valid bits within each 32-bit slot. A 24-bit sample representation and a 24-bit physical slot are not automatically the same setting.

Both ends must agree on frame polarity, bit-clock edge, slot count, slot width and data alignment. If one end expects I2S timing and the other expects left-justified timing, the stream can shift sample bits even though clocks are present. If both ends wait for the other to generate clocks, DMA may never make expected progress. [ASoC clocking documentation](https://www.kernel.org/doc/html/v6.6/sound/soc/clocking.html).

## Frames, samples, periods and buffers

An ALSA frame contains one sample for each channel. With two channels stored as 32-bit words, a frame uses eight bytes. A 256-frame period therefore represents `256 / 48000 = 5.333 ms` and uses 2048 bytes. Four periods form a 1024-frame buffer, about 21.333 ms and 8192 bytes.

These are calculated values, not measured latency. A driver can impose different alignment or minimum period constraints. Application scheduling, plugin conversion, codec filtering and output hardware add delay. The buffer size only describes one part of the path.

A period is a useful notification unit. Smaller periods can reduce the time before software handles progress, but they increase wakeup rate and scheduling overhead. A larger buffer tolerates a longer scheduling delay but can retain more audio. Choose both from the deadline and available CPU time.

In playback, an **underrun** means the device runs out of prepared samples. In capture, an **overrun** means incoming samples overwrite data the application has not consumed. ALSA reports these as XRUN conditions. Recovery restarts a stream state; it cannot reconstruct the audio that was lost. Count XRUNs and retain the workload conditions.

## The software route can hide conversion

A direct hardware PCM interface exposes the device's accepted parameters. An ALSA plugin route can add rate conversion, channel conversion or sample-format conversion. This is useful, but it changes CPU use and latency. Record the PCM name and accepted hardware parameters when comparing performance.

For example, an application requesting 44.1 kHz may work through a software-converting route even when the hardware runs at 48 kHz. That success does not prove a 44.1-kHz hardware clock configuration. Compare the application format with the actual device format before diagnosing clock drift.

The same distinction applies to sample size. A 24-bit payload may be packed into three bytes or stored in a four-byte word. Buffer calculations must use the selected ALSA sample format, not only a marketing statement about converter resolution.

## ASoC separates reusable and board-specific work

The CPU digital audio interface driver handles its peripheral. The codec driver handles the external audio device. The machine description connects them and supplies board-specific routing and clock relationships. Dynamic Audio Power Management, or **DAPM**, tracks routes and powers relevant parts as needed.

A silent output can therefore have several layers: the PCM stream runs, but a mixer control mutes the path; the route does not reach an output widget; a codec supply is absent; or the serial interface timing is wrong. Adjusting application volume cannot fix a missing clock or supply.

In PetaLinux 2024.1, inspect the chosen kernel ASoC drivers, the generated device-tree audio nodes and the selected ALSA userspace packages separately. Avoid copying an audio card node from a different evaluation design. The PL interface, external codec and wiring may differ even on the same SoC family. [ASoC overview](https://www.kernel.org/doc/html/v6.6/sound/soc/overview.html).

## Diagnose time and content independently

First prove that stream positions advance at the expected rate. Then prove that data contains the expected samples. Finally prove that the intended physical output or input carries them. A running DMA counter does not prove correct channel order or an unmuted analog path.

For repeated clicks, compare XRUN counters with scheduling and storage/network activity. For a constant pitch error, compare requested and actual clock rates. For swapped channels or noisy low bits, inspect slot mapping and sample alignment. For slowly increasing audio/video drift, examine whether the streams use independent clocks and how timestamps are related.

A loopback test should record whether it is digital, analog or application-only. Each exercises a different set of components. An application-only loopback cannot validate codec pins, analog routing or board noise.

> [!NOTE]
> **Not run on the reference setup:** physical audio playback/capture, clock measurements, loopback and XRUN stress tests. The timing and buffer examples are calculations; no audio hardware success is claimed.

## References

- [Linux 6.6 ALSA documentation](https://www.kernel.org/doc/html/v6.6/sound/), PCM and ASoC architecture.
- [ALSA PCM interface](https://www.alsa-project.org/alsa-doc/alsa-lib/pcm.html), frame units, parameters, stream states and error recovery.
- `linux-xlnx@xilinx-v2024.1:sound/soc/`, release-specific CPU, codec and machine-driver implementation; select the drivers matching the actual hardware design.

---

<sub>← [VCU: Video Codec Unit](04-vcu-video-codec-unit.md) · [Chapter index](README.md) · Next chapter: [21 · RPU and OpenAMP](../21-rpu-and-openamp/README.md) →</sub>
