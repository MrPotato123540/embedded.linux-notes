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

## Why host support is an engineering input

The build runs many host programs before it produces a target executable. Shell tools unpack source, Python evaluates metadata, native tools generate code, and host utilities construct filesystem images. Differences in these programs can cause failures that have nothing to do with Arm or the board.

Use the release's supported host environment as a baseline. A container or virtual machine can help preserve userspace tools, but it still depends on storage, permissions, memory and the host kernel. Record the environment you actually use rather than assuming a container name is a complete build description.

Install and build with a normal user. A root-owned file created by an earlier privileged build can later block an ordinary task. Broadly changing permissions hides the cause and can make shared caches unsafe. Identify the directory and operation that failed, then correct ownership or the build location deliberately.

## Keep one release environment per shell

Sourcing `settings.sh` changes the current shell's environment. Launching the script as a child process would not preserve those changes in the parent shell. This distinction explains why a tool may remain unavailable after a user believes they have loaded the environment.

Do not stack multiple tool releases in one terminal. Earlier paths and environment variables may remain active. Use a new shell, load the intended release, and inspect which executable is selected. This matters for tools such as Bootgen that can also be installed independently: the host's default Bootgen can differ from the one supplied with Vivado 2024.1.

The reference work already found this distinction. The default host Bootgen was older, so the final boot-image inspection used the explicit Vivado 2024.1 executable. A filename such as `bootgen` is not enough evidence of tool version. Record the selected path and the version banner with diagnostic output.

## Plan storage around four different data sets

| Data set | Main purpose | Recovery requirement |
| --- | --- | --- |
| Maintained project inputs | Configuration, recipes, patches and hardware identity | Must be backed up and versioned |
| Downloads | Source archives and repository fetches | Must be available from a controlled source or mirror |
| Shared state | Reusable task results | Can accelerate a correct rebuild |
| Temporary work | Unpacked source, task scripts and build objects | Regeneratable, but valuable during diagnosis |

These sets grow differently. Several projects can share downloads and shared state, while their temporary work must remain isolated. A full disk can fail a task during archive extraction, linking, package creation or image generation. The final error may appear in a different tool from the one that consumed most of the space.

Filesystem behavior also matters. The installed `petalinux-create project --help` explicitly discusses a local `TMPDIR` when a project is on NFS. Build work involves large numbers of small files, permissions, links and locking. A network share that stores documents successfully is not automatically a suitable temporary build filesystem.

## Proxy, mirrors and offline claims

The source download cache and shared-state cache are different. A shared-state hit can make a build succeed without compiling a component. It does not prove that the component's source is still retrievable. A release process needs a way to recover both source and build configuration even when caches are empty.

An offline test should use controlled source availability and disable network fetching. Start with a fresh temporary build area so old work does not hide missing inputs. Include submodules, archive checksums, license text and vendor assets in the review. A Git branch name alone is not a durable source identity.

If the network is unreliable, identify the failing fetcher and URL before changing mirrors. A TLS failure, missing revision and proxy authentication failure require different fixes. Preserve the original fetch log. Do not disable certificate checking as a general build-system solution.

## Host failures versus target failures

A host compile failure occurs before an image reaches the board. A target dynamic-loader error occurs after deployment. A TFTP failure concerns the network boot path. Keeping these categories separate prevents unnecessary changes to the hardware design or kernel configuration.

For example, a successful image build followed by a failed NFS root mount should lead you to inspect network connectivity, server exports, permissions, kernel support and boot arguments. Reinstalling PetaLinux does not address those runtime boundaries. Similarly, a missing host utility during image generation should not be treated as a target package-selection problem.

## A useful environment record

Keep the tool release, installer identity, host distribution, relevant environment setup, project location and cache locations with the release record. Record any supported host workaround and why it is needed. This lets another engineer distinguish a project defect from a host-specific condition.

This section does not claim a new installation, package installation or complete offline build. It explains the preparation and diagnostic boundaries using the existing host, installed help and earlier tool-version evidence. A new supported-host setup must still be tested before it becomes a team baseline.

## References

- AMD UG1144 (2024.1), installation requirements and troubleshooting
- Locally executed `petalinux-create project --help`, including local `TMPDIR` requirements

---

<sub>← [What Is PetaLinux?](01-what-is-petalinux.md) · [Chapter index](README.md) · [Project Structure: A Real 2024.1 Project Dissected](03-project-structure.md) →</sub>
