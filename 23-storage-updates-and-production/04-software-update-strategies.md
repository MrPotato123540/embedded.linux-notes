# Software Update Strategies

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Update architecture

An A/B design writes an inactive slot and changes boot selection after verification. A recovery design boots a separate environment to replace the main system. Both need a tested path through interrupted writes and failed startup.

| Framework | General integration model |
| --- | --- |
| RAUC | Signed bundles, slots and bootloader integration |
| SWUpdate | Configurable handlers for image and component updates |
| Mender | Device update client with deployment-management integration |

These are architecture descriptions, not a claim that current framework releases run unchanged on Langdale. Pin and test the version integrated into the product.

## Boot success

Mark a new slot successful only after meaningful health checks. Keep kernel, modules, firmware and rootfs compatibility together. Multiboot can help select boot images, but does not implement the whole update transaction or data migration.

> [!NOTE]
> **Not run on the reference setup:** an updater integration or power-cut campaign.

## References

- [RAUC basics](https://rauc.readthedocs.io/en/latest/basic.html)
- [SWUpdate overview](https://sbabic.github.io/swupdate/overview.html)
- [Mender documentation](https://docs.mender.io/)

---

<sub>← [SD and eMMC](03-sd-and-emmc.md) · [Chapter index](README.md) · [Boot-Time Optimization](05-boot-time-optimization.md) →</sub>
