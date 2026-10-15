# Licensing and Compliance

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[23 · Storage, Updates and Production](README.md)** · Part XII: Production

## Build records support compliance

Every shipped component has its own license terms. Distribution obligations can include notices, license text, corresponding source and, for some licenses and product cases, installation information. The exact duties depend on the license and how the software is distributed.

Do not treat a package's short license label as the full analysis. Preserve the actual license text, modifications, build scripts and source revisions. Proprietary applications using Linux system calls have a different relationship from kernel modules or linked libraries.

## Yocto outputs

License manifests describe selected packages. The archiver class can preserve source and related material. SPDX generation can produce a **Software Bill of Materials (SBOM)**. These outputs support review; none alone proves that every legal obligation is satisfied.

The installed PetaLinux build help includes `--archiver`. Archive the resulting material with the exact release and verify that required sources can be rebuilt or supplied according to the applicable terms.

For release-specific legal decisions, have the actual distribution and license set reviewed by qualified counsel.

## References

- Yocto 4.1.4 Development Tasks Manual, license compliance and source archiving
- Executed PetaLinux 2024.1 build help
- [GNU license texts](https://www.gnu.org/licenses/)

---

<sub>← [Reliability and Field Diagnostics](06-reliability-and-field-diagnostics.md) · [Chapter index](README.md) · [CI and Reproducible Builds](08-ci-and-reproducible-builds.md) →</sub>
