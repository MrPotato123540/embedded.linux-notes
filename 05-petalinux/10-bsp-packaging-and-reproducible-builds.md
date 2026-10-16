# BSP Packaging and Reproducible Builds

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[05 · PetaLinux 2024.1](README.md)** · Part III: Build Systems

## What a BSP preserves

A **Board Support Package (BSP)** packages a project for reuse. It can include configuration, hardware assets and selected prebuilt files. It is useful for sharing a starting point, but it does not automatically capture every remote source or host dependency.

A reproducible release needs the tool version, hardware revision, layer revisions, source revisions, patches, configuration and package manifest. Record checksums for published images. Pin moving Git branches to commits in release records.

## Cache and CI policy

A continuous integration build should start from maintained inputs. Shared downloads and shared state can reduce time, but a cache-only success can hide missing sources. Periodically test a clean build against controlled mirrors.

A container can fix many host tools, but it does not remove all host dependencies. Filesystem behavior, user permissions, available memory and kernel features still matter. Keep build output owned by the intended user, and do not run the normal build as root.

## Release test

Recreate the project in a separate directory, build it, compare manifests and boot the output. Explain any binary differences before calling the build reproducible. Timestamps, build paths and uncontrolled source revisions can all affect output.

> [!NOTE]
> **Not run on the reference setup:** BSP export/reimport and a second clean build. Packaging a BSP alone is not evidence of reproducibility.

## Reusability and reproducibility are different claims

A BSP can make a project easy to share. A reproducible build claim is stronger: defined inputs and a defined environment should produce an explainable result. An archive that contains configuration but refers to moving source branches may be reusable today and impossible to rebuild later.

Distinguish functional reproduction from bit-for-bit reproduction. Two images may boot and pass the same tests while differing in timestamps, filesystem metadata or embedded paths. Conversely, identical package names do not prove identical source or binaries. State which property was tested and keep the evidence that supports it.

The release record should connect hardware, firmware, Linux and userspace. A source manifest for only the application is not enough when the boot firmware and device tree are built from another hardware export.

## Build an input manifest before packaging

| Input | Identity to preserve | Why the filename is insufficient |
| --- | --- | --- |
| PetaLinux tools | Release and installer/checksum record | Several installations can expose the same command name |
| Hardware export | Hardware revision and XSA checksum | An export can be overwritten in place |
| Layers | Repository URL, commit and local patch record | Branch tips move |
| Component source | Resolved revisions or verified archives | Recipe version strings can remain unchanged |
| Configuration | Maintained project inputs and layer policy | Generated files can hide local edits |
| Release artifacts | Checksums and package manifests | Files can be copied from another build |

Also preserve the relationship between the files. A manifest containing two XSA files and two firmware builds must say which combination was released. An unordered collection of checksums cannot express that contract by itself.

## Check what the BSP actually contains

Use the release-specific packaging interface and inspect the archive contents after export. Verify that maintained recipes, patches, configuration and required hardware assets are present. If prebuilt files are included, identify them as prebuilt output and record their origin separately from project inputs.

A project may reference external source directories, private mirrors or files outside its tree. Those references can survive packaging while the actual content does not. Recreating the BSP on the same workstation may accidentally find those external files and hide the omission.

A stronger test uses a separate workspace with only the documented dependencies available. This is why export success alone is weak evidence. The archive must be consumed by a fresh project before its portability claim is meaningful.

## Caches are accelerators, not the source archive

Shared state can restore output without rerunning a component's full build. That is useful for everyday development and continuous integration. It also means a cached build may pass while a required source server is unavailable or a recipe contains an undeclared assumption.

Keep controlled source mirrors and verify source recovery independently. Then test a build with fresh temporary state. An offline test should explicitly prevent network fetching so an unexpected external dependency becomes visible rather than silently succeeding.

Avoid treating a cache deletion as a substitute for dependency review. If a recipe reads an untracked workstation file, a clean build on that workstation may still succeed. Isolation and an input manifest are needed to expose that hidden dependency.

## Explain binary differences systematically

Start by confirming that both builds used the same resolved inputs. Compare package manifests, configuration and source revisions. If those match, compare the differing artifacts by format. An ELF file, an archive and a filesystem image contain different kinds of metadata.

For an ELF difference, inspect sections, symbols and build identifiers. For an archive, inspect member names, order, timestamps and permissions. For a filesystem image, distinguish file content from filesystem metadata and free-space layout. A raw whole-file checksum identifies a difference but does not explain it.

Do not remove useful version information merely to make checksums match. The goal is a controlled and understandable build. A deliberate build identifier may differ by policy; an uncontrolled absolute workstation path is a different kind of defect.

## CI should validate the final package set

A useful CI pipeline validates metadata, builds the selected artifacts, records manifests, packages a coherent release and runs available boot/application tests. Keep the symbols and logs needed to diagnose that release. A pipeline that stops after compiling one application cannot certify the boot firmware or root filesystem.

Separate fast development checks from periodic recovery tests. The fast path can use caches. The recovery path tests whether maintained inputs and mirrors are sufficient. Both need stable artifact identities so their results are attributable to a specific build.

The export/reimport and second clean-build experiments remain open. The earlier source and artifact inspections support the manifest design, but they do not establish a completed reproducibility test.

## References

- AMD UG1144 (2024.1), BSP packaging and build mirrors
- Yocto 4.1.4 [reproducible builds](https://docs.yoctoproject.org/4.1.4/test-manual/reproducible-builds.html)

---

<sub>← [Hardware Updates and XSA Re-Import](09-hardware-updates.md) · [Chapter index](README.md) · [Yocto Without PetaLinux](11-yocto-without-petalinux.md) →</sub>
