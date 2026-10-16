# CI and Reproducible Builds

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Reproducibility needs a defined output

A reproducible build produces the same intended output from the same declared inputs under a controlled process. State what you compare: a compiler output, root filesystem, boot container or complete storage image. Byte-identical `BOOT.BIN` packaging does not prove that the firmware binaries inside it were reproducibly compiled.

Continuous integration (**CI**) should preserve the inputs and evidence needed to explain a result. A green job without its configuration, source revisions and artifact identity is weak release evidence. A build that succeeds only because an old workspace contains an undeclared file is not repeatable from its manifest.

For PetaLinux 2024.1, include the tool release, host environment, hardware export, layer revisions, project configuration, local recipes/patches and external source revisions. Include bitstream and firmware provenance even when they are produced in a separate pipeline.

## Pin inputs at the level that can change

A branch name can move. A download URL can serve different content. An unversioned hardware export can change peripheral addresses while keeping the same filename. Pin immutable revisions or hashes and retain the actual input when the upstream retention policy is insufficient.

BitBake `SRCREV` pins a source revision when used as intended. Avoid `${AUTOREV}` in a release recipe because it asks the build to follow moving source state. Download checksums protect fetched archives, but local files and generated inputs also need tracking.

The installed VCU and OpenAMP recipes provide concrete examples of pinned revisions. Their resolved values can still be changed by append files and overrides. Archive the effective configuration, not only the base recipe that appears to contain the version.

## Cache correctness is different from clean rebuilds

Yocto shared state, or **sstate**, reuses task outputs identified through task signatures. It saves time when inputs and dependency tracking are correct. It is not evidence that a task ran from scratch during a particular job.

Use routine cached builds for fast feedback, then selected independent clean builds for reproducibility and missing-dependency checks. Deleting caches on every job makes builds slower without automatically improving source control or determinism. Conversely, reusing one workspace forever can hide undeclared dependencies.

Record whether an artifact was rebuilt or restored from cache when interpreting a test. A successful fetch-free build also requires a prepared source mirror and declared inputs; it should not accidentally use network access to fill missing dependencies.

## Sources of byte differences

Timestamps, build paths, random seeds, file ordering, archive metadata and generated identifiers can change output. `SOURCE_DATE_EPOCH` is a common mechanism for giving tools a stable time input, but each tool must honor it correctly.

Filesystem images can include UUIDs, creation times and allocation order. Boot containers can include security metadata or other generated content. A signed or encrypted image may legitimately differ depending on the selected scheme and metadata policy. Define which artifacts are expected to be identical and which require a structured comparison.

Do not remove security properties merely to force a matching hash. Compare deterministic unsigned inputs separately when appropriate, and preserve the signing operation's public verification data and audit record. Private keys must remain outside ordinary build artifacts and logs.

## Use the existing packaging experiment correctly

A previous reference experiment regenerated the supplied boot image using Bootgen 2024.1 and the supplied BIF inputs. Both files were 1,838,720 bytes with SHA-256:

```text
97363bab9a28ecda6713840aa55986b98b09fd51b016b030224064f04af612ff
```

The record is `reference-setup/captures/bootgen-regeneration-2026-10-16.txt`. It proves identical packaging for those supplied binaries and that tool invocation. It does not prove source-level reproducibility of FSBL, PMU firmware, TF-A or U-Boot, nor that the image boots on physical hardware.

This bounded result is still useful. If a later packaging run differs while all input hashes are unchanged, inspect tool version, BIF attributes and generated metadata. If an input hash changed, investigate its producing build before blaming Bootgen.

## Structure CI around different failure classes

A useful pipeline can first validate tracked configuration and local links, then build changed components, then assemble images, inspect artifact structure and run supported emulation tests. Hardware tests follow on the appropriate board and storage medium.

Static checks can catch a missing device-tree label, overlapping planned memory regions or mismatched manifest hashes. QEMU can test selected boot and userspace behavior. Neither validates physical DDR timing, flash power-loss behavior, PL throughput or secure provisioning. Label test scope so one green stage is not read as proof of all layers.

For a changed device driver, a host syntax/build check is weaker than a build against the exact target kernel configuration. For a documentation-only change, a full image build may add no relevant evidence. Select checks from the changed contract and retain their limitations.

## Publish a release set with traceable relationships

An original release bundle can contain a signed manifest, boot artifacts, root image, package list, SBOM, corresponding-source materials, configuration snapshots and test results. Each artifact should have a content hash and a clear relation to the manifest.

Include the hardware export and PL build identity where permitted and needed. A Linux image and bitstream from different builds can each be individually valid yet incompatible together. Record the supported board revisions and migration requirements for persistent data.

Separate build from deployment. Producing a release candidate does not change a board. Deployment should select one reviewed manifest and verify the received content before writing the intended inactive target. CI credentials and production signing authority need roles appropriate to those operations.

## Investigate mismatches from the outside inward

Compare whole-artifact hashes first to detect differences. Then compare container metadata, file lists, per-file hashes and relevant binary sections to locate them. A different filesystem image hash can come from metadata while all application binaries match; a matching image filename proves nothing.

Rebuild in a separate directory or clean worker to expose path and environment dependence. Keep both outputs and the comparison report. Fix the undeclared input or nondeterministic step, then repeat the comparison that failed. Do not claim reproducibility from two runs that simply reused the same cached artifact.

> [!NOTE]
> **Not run on the reference setup:** complete independent PetaLinux rebuilds and a production CI deployment. The existing Bootgen experiment provides packaging evidence only. Local recipe and class inputs were inspected for the proposed workflow.

## References

- [Yocto reproducible-build documentation](https://docs.yoctoproject.org/4.1.4/test-manual/reproducible-builds.html).
- [SOURCE_DATE_EPOCH specification](https://reproducible-builds.org/docs/source-date-epoch/).
- [Recorded Bootgen regeneration](../07-boot-images-and-bootgen/02-bootgen.md), input/output scope and hash.
- [Licensing artifacts](07-licensing-and-compliance.md), source archives and SBOM boundaries.

---

<sub>← [Licensing and Compliance](07-licensing-and-compliance.md) · [Chapter index](README.md) · Next chapter: [24 · Debugging and Board Bring-Up](../24-debugging-and-bring-up/README.md) →</sub>
