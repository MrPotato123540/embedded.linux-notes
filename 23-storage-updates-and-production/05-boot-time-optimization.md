# Boot-Time Optimization

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Measure stage boundaries

Define the endpoint: first display, network service or valid control output. Measure firmware, bootloader, kernel and userspace separately. Timestamped serial logs are useful, but printing itself adds delay.

## Optimization order

Remove unnecessary waits and boot targets, reduce unneeded image content, and fix slow service dependencies. Then examine driver initialization, storage reads and decompression. Keep a baseline and change one item at a time.

Skipping U-Boot or directly entering Linux can reduce work, but transfers its responsibilities elsewhere: image selection, device-tree fixups, verification and recovery still need an owner. Deferred initialization must not expose an application before its required hardware is ready.

Test cold and warm boot, normal and failure paths. An optimization that removes the only recovery path is a product behavior change, not just a timing improvement.

> [!NOTE]
> **Not run on the reference setup:** a controlled before/after hardware benchmark.

## References

- Saved `reference-setup/captures/boot-ts.log`
- Linux 6.6 initcall/debug documentation; systemd-analyze manual

---

<sub>← [Software Update Strategies](04-software-update-strategies.md) · [Chapter index](README.md) · [Reliability and Field Diagnostics](06-reliability-and-field-diagnostics.md) →</sub>
