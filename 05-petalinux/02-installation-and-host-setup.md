# Installation and Host Setup

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## Host preparation

Use a host distribution supported by the exact PetaLinux release. The reference host uses Ubuntu 22.04 LTS. Host package names, minimum memory and disk requirements belong to the release's installation requirements; do not copy a package list from another year without checking it.

Install as a normal user into a location that user can maintain. Build directories need space for downloaded source, temporary objects, packages and shared state. Several builds can share caches, but their temporary work directories should remain separate.

The installed environment script is `/opt/pkg/petalinux24.1/settings.sh` on this host. Loading it selects the tools for this release. Avoid mixing different PetaLinux environments in one terminal.

## Caches and offline operation

`DL_DIR` stores downloaded sources. Shared state stores reusable task output. A source mirror and an sstate mirror solve different problems: a cache hit may avoid compilation, but missing source can still break a clean rebuild.

Before promising an offline build, test it with network fetching disabled and a fresh temporary build directory. Include Git repositories, source archives, license files and any separately downloaded vendor assets. Record checksums and source revisions.

## Common host failures

| Symptom | Check |
| --- | --- |
| Tool not found | Correct release environment loaded |
| Permission failures | Ownership of project and cache directories |
| Build fails only on a network share | Local temporary directory and filesystem behavior |
| Text or Python encoding errors | Supported UTF-8 locale |
| Network boot fails after a successful build | TFTP/NFS service, firewall and file permissions |

> [!NOTE]
> **Not run on the reference setup:** a fresh installer run, host package installation and a complete offline build. The existing 2024.1 installation was used for help inspection.

## References

- AMD UG1144 (2024.1), installation requirements and troubleshooting
- Locally executed `petalinux-create project --help`, including local `TMPDIR` requirements

---

<sub>← [What Is PetaLinux?](01-what-is-petalinux.md) · [Chapter index](README.md) · [Project Structure: A Real 2024.1 Project Dissected](03-project-structure.md) →</sub>
