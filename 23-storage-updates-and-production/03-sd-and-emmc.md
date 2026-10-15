# SD and eMMC

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Managed block storage

SD and eMMC expose block devices. Their internal controller handles flash translation, but write endurance and power-loss behavior still matter. Filesystem journaling does not guarantee that the last application record reached durable storage.

A WIC image includes a partition table and filesystem contents. The eMMC user area and hardware boot partitions are different regions; boot configuration selects how the device uses them. Do not assume writing the user area's first sectors updates an eMMC boot partition.

## Product choices

Select storage with suitable endurance, temperature range and power-loss behavior. Limit unnecessary writes, rotate logs and separate persistent product data from replaceable system images.

Measure with the real access pattern. Sequential throughput does not predict small synchronous-write latency. Test full storage, interrupted updates and cold restart.

> [!WARNING]
> Partitioning, disk-image writes and eMMC boot configuration changes can make a device unbootable or destroy data.

> [!NOTE]
> **Not run on the reference setup:** physical SD/eMMC endurance or power-cut tests.

## References

- Linux 6.6 MMC documentation
- AMD UG1144 (2024.1), WIC and SD boot

---

<sub>← [UBI and UBIFS in Practice](02-ubi-and-ubifs.md) · [Chapter index](README.md) · [Software Update Strategies](04-software-update-strategies.md) →</sub>
