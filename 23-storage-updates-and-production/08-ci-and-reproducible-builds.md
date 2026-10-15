# CI and Reproducible Builds

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Rebuild from maintained inputs

A continuous integration pipeline should capture tool versions, layer commits, XSA revision, configuration, source checksums and build outputs. Build application and BSP changes through the same controlled process used for release.

Separate stages for metadata validation, build, packaging, artifact inspection and target testing. A compile-only job cannot detect an invalid boot layout or a peripheral timing problem.

## Caches and reproducibility

Share download and sstate caches with controlled permissions. Periodically rebuild without relying on a warm cache to expose missing inputs. Containers help stabilize host tools but do not fix moving source branches or unrecorded hardware exports.

Compare package manifests and image hashes. If binary outputs differ, investigate timestamps, paths, source revisions and build configuration. Reproducibility is a measured result, not a property gained by using a container.

> [!NOTE]
> **Not run on the reference setup:** a second clean build and complete CI hardware pipeline.

## References

- Yocto 4.1.4 reproducible-build and buildhistory documentation
- [BSP packaging](../05-petalinux/10-bsp-packaging-and-reproducible-builds.md)

---

<sub>← [Licensing and Compliance](07-licensing-and-compliance.md) · [Chapter index](README.md) · Next chapter: [24 · Debugging and Board Bring-Up](../24-debugging-and-bring-up/README.md) →</sub>
