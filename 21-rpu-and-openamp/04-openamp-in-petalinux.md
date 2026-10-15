# OpenAMP in PetaLinux

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[21 · RPU and OpenAMP](README.md)** · Part X: Heterogeneous Multiprocessing

## Package and hardware configuration

OpenAMP integration needs compatible Linux support, remote firmware, reserved memory, mailbox wiring and userspace software. Enabling a packagegroup alone cannot establish those hardware relationships.

The inspected packagegroup includes libmetal, OpenAMP and echo, matrix-multiply and RPC demo groups. Some remote-firmware dependencies are machine-specific. Read the final dependency expansion for the selected machine rather than assuming every board gets the same firmware.

## From demo to product

First test a small echo exchange with matching example firmware. Then add a protocol with versioning, bounded lengths, sequence identifiers, timeouts and recovery. Do not send raw pointers between processors; their address views and ownership differ.

Test remote reset, Linux application restart and a full Linux reboot. Confirm that pending messages and stale buffers cannot be mistaken for new work.

> [!NOTE]
> **Not run on the reference setup:** OpenAMP demos or a custom protocol on physical RPU hardware.

## References

- Inspected `meta-petalinux@rel-v2024.1:recipes-core/packagegroups/packagegroup-petalinux-openamp.bb`
- [OpenAMP documentation](https://openamp.readthedocs.io/)

---

<sub>← [remoteproc and RPMsg](03-remoteproc-and-rpmsg.md) · [Chapter index](README.md) · [IPI and Shared Memory Patterns](05-ipi-and-shared-memory.md) →</sub>
