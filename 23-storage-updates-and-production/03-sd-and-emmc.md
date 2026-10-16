# SD and eMMC

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Managed flash exposes logical blocks

SD cards and eMMC contain a controller that maps logical block addresses to flash storage. The host normally sees block I/O rather than raw eraseblocks and bad-block markers. Wear leveling, internal caching and garbage collection occur inside the device and can affect latency and durability.

The Linux MMC subsystem manages the card protocol. ZynqMP's host integration uses the SDHCI framework and the Arasan driver path in `drivers/mmc/host/sdhci-of-arasan.c`. Bus width, voltage support, clocks, card-detect wiring and timing modes must match the board and device.

A controller supporting a fast mode does not prove the board can use it. Signal routing, pull-ups, power rails and card/device capabilities constrain negotiation. A stable lower-speed mode and an unstable higher-speed mode are different evidence from a total failure to enumerate.

## Separate media layout from controller setup

An ordinary SD image may contain a partition table, a boot filesystem and a root filesystem. It can also contain a filesystem directly on the whole block device. The image-generation method determines the layout; the device name alone does not.

The saved reference QEMU log reports:

```text
mmc0: SDHCI controller on ff170000.mmc [ff170000.mmc] using ADMA 64-bit
mmc0: new high speed SD card at address 4567
mmcblk0: mmc0:4567 QEMU! 2.00 GiB
```

Later, ext4 is mounted from `mmcblk0` itself. This captured emulation layout does not use a shown `mmcblk0p2` root partition. Copying a familiar `/dev/mmcblk0p2` root argument would therefore be wrong for that artifact. It also does not prove the layout or timing of a physical SD card.

Use a filesystem UUID or partition identifier when suitable for the boot design, but understand what it identifies. A filesystem UUID belongs to filesystem content; a partition UUID belongs to partition metadata. Cloning an image can duplicate these values across devices, so production identity policy matters.

## eMMC has several hardware areas

An eMMC device can expose a user area, boot areas and a Replay Protected Memory Block (**RPMB**) area. These are not ordinary partitions inside one GPT. Linux represents special areas through interfaces appropriate to their semantics.

Boot-area selection and boot-bus configuration are device settings with effects beyond the current Linux mount. RPMB uses an authenticated protocol and key provisioning; it is not a normal writable filesystem partition. Do not treat a device node that resembles the user area as interchangeable with it.

Some device configuration operations can be permanent or have restricted change rules. This guide does not perform them. A production flow must identify the exact eMMC part and follow its specifications and the relevant standard, with a recoverable plan for ordinary settings and explicit control of irreversible provisioning.

## Durability crosses several caches

An application write can enter the Linux page cache. Filesystem writeback sends block requests. The host controller transfers them. The storage device can still have internal work before data is durable. Completion at one boundary does not automatically describe all lower boundaries.

`fsync()` and related interfaces request durability through the filesystem and block stack, but the result depends on correctly implemented device flush and ordering behavior. A storage part's power-loss behavior must be tested under the application's real update pattern. A benchmark that only writes and rereads while power stays on does not test crash durability.

Ext4's journal protects filesystem metadata consistency according to its mode and options. It does not turn a multi-file application update into an atomic transaction. The recorded reference mount uses ordered data mode; that is a captured mount property, not a universal setting for every PetaLinux image. [Ext4 journal documentation](https://www.kernel.org/doc/html/v6.6/filesystems/ext4/journal.html).

## Work a configuration update example

Suppose an original application replaces a settings file. It writes a new file in the same directory, checks errors, synchronizes the file as needed, renames it over the old name and synchronizes the directory when required for persistence. This pattern separates data preparation from name replacement.

The exact guarantees depend on the filesystem and storage stack. If settings span several files, a single rename does not make all of them one transaction. A versioned directory or application journal may be needed. The recovery path must decide which complete version to use after interruption.

Do not update a file in place merely because it is small. A partial sector or multi-block update can leave a mixed old/new record. Add format version, length and integrity checks so startup can reject incomplete content and select a retained valid copy.

## Performance depends on latency distribution

Large sequential writes show only one workload. Small synchronous writes, database commits and nearly full media can behave very differently. Internal garbage collection can create long latency spikes that matter to watchdogs, logging and control applications.

For an original workload producing 2 MB/s of logs, a one-second storage stall requires at least 2 MB of buffering before other queued work is counted. A nominal 20-MB/s benchmark does not eliminate that stall requirement. Measure sustained rate and worst observed pause under realistic fill level and temperature.

Reduce unnecessary write amplification by batching suitable updates, limiting logs and separating immutable root content from mutable state. Do not disable required synchronization solely to improve a throughput number; that changes the durability contract.

## Diagnose negotiation, I/O and filesystem errors separately

No card detection suggests power, reset, card-detect or pin configuration. Enumeration followed by errors at a fast mode suggests timing/voltage issues. Repeated I/O errors across filesystems suggest the lower storage path. Filesystem recovery after an abrupt reset requires application and durability analysis as well as media health checks.

Preserve kernel errors, card identity, negotiated mode, image hash and board revision. Device health indicators can help with trends but do not predict every failure. Keep a recovery image and a method that does not depend on the damaged writable root filesystem.

> [!NOTE]
> **Not run on the reference setup:** physical SD/eMMC programming, boot-area changes, endurance and power-cut tests. Existing emulated MMC/ext4 logs and the pinned host driver were inspected read-only.

## References

- `linux-xlnx@xilinx-v2024.1:drivers/mmc/host/sdhci-of-arasan.c`, inspected host integration.
- [Linux MMC tools documentation](https://www.kernel.org/doc/html/v6.6/driver-api/mmc/mmc-tools.html), device-information and management scope.
- Existing `reference-setup/captures/boot-prebuilt3.log`, emulated card identity and ext4 mount evidence.

---

<sub>← [UBI and UBIFS in Practice](02-ubi-and-ubifs.md) · [Chapter index](README.md) · [Software Update Strategies](04-software-update-strategies.md) →</sub>
