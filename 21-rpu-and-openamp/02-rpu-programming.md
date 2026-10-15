# Programming the RPU

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Split and lockstep

In split mode, the R5 cores can run separate software. In lockstep mode, they work together for fault detection rather than providing two independent application instances. Firmware, memory layout and platform configuration must match the selected mode.

**Tightly Coupled Memory (TCM)** provides predictable local access. DDR offers larger capacity but shares the system path. Link addresses and processor-visible addresses must agree with the chosen memory view.

## Build and boot

Vitis can build bare-metal or FreeRTOS applications for the selected RPU platform. Preserve the linker script, hardware export and libraries with the firmware.

The FSBL can load RPU firmware during boot, or Linux remoteproc can manage a supported runtime lifecycle. Do not combine both ownership models without a documented attach/recovery design. Loading the same processor again can destroy a running control task.

> [!NOTE]
> **Not run on the reference setup:** RPU split/lockstep hardware execution and timing tests.

## References

- UG1085 (v2.5), RPU configuration and TCM
- AMD UG1400 (2024.1), standalone and FreeRTOS application flows

---

<sub>← [AMP vs. SMP Concepts](01-amp-concepts.md) · [Chapter index](README.md) · [remoteproc and RPMsg](03-remoteproc-and-rpmsg.md) →</sub>
