# remoteproc and RPMsg

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Lifecycle and messages

**remoteproc** manages a remote processor's supported firmware lifecycle. **RPMsg** carries messages over a shared-memory transport, commonly using virtio queues. Starting a processor and exchanging messages are related but separate operations.

A firmware resource table can describe requested resources and virtio devices. Carveouts reserve memory; vrings describe queues; mailboxes/IPI provide notifications. The firmware linker map, resource table and Linux device tree must agree.

## ZynqMP integration

Use the R5 driver and binding from the pinned vendor kernel. Older and newer driver implementations can expect different node layouts. The reference image includes `openamp.dtb`, but selecting that file is a boot-flow choice, not an automatic consequence of installing packages.

Userspace access depends on the RPMsg driver/interface enabled in the image. Validate endpoint identity and message sizes. A remote firmware bug may still access shared hardware or memory outside a high-level messaging abstraction.

> [!NOTE]
> **Not run on the reference setup:** loading R5 firmware and exchanging RPMsg traffic.

## References

- Linux 6.6 remoteproc and RPMsg documentation
- Inspected 2024.1 ZynqMP R5 remoteproc source
- Reference `openamp.dtb`

---

<sub>← [Programming the RPU](02-rpu-programming.md) · [Chapter index](README.md) · [OpenAMP in PetaLinux](04-openamp-in-petalinux.md) →</sub>
