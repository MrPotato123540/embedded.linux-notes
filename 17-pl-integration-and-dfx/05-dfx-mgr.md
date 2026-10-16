# dfx-mgr and Accelerator Packages

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Package management for PL applications

`dfx-mgrd` manages supported accelerator packages; `dfx-mgr-client` requests operations. Packages can contain the bitstream, overlay and metadata describing the shell or accelerator. Typical AMD layouts use `/lib/firmware/xilinx` with files such as `shell.json`, `accel.json`, `.bit.bin` and `.dtbo`.

The metadata must match the actual static design and load flow. Copying files into the directory does not prove that the daemon can validate or activate them.

## PetaLinux 2024.1 integration

The inspected application-template help lists separate full, static and partial DFX templates for supported device families. Select the ZynqMP template matching the design. A partial application can depend on the static package; keep that dependency in the build and deployment record.

Kria's `xmutil` adds a platform application-management interface. Use the matching platform's package conventions and firmware version.

> [!NOTE]
> **Not run on the reference setup:** package listing, activation and removal on a physical DFX platform.

## The manager coordinates packages and active hardware

`dfx-mgr` provides a daemon, client interface and library for accelerator management. It adds package discovery, shell/slot information and loading policy above lower-level programming mechanisms. It is not a replacement for a compatible static design, correct drivers or application shutdown.

The supplied 2024.1 recipe pins source commit `ec70363a2a878737057995f922a9460d18aafa26` on `xlnx_rel_v2024.1`. It depends on components including `libdfx`, `zocl`, `libdrm` and systemd. This concrete pin is a better release identity than examples taken from the repository's current default branch.

The recipe installs `dfx-mgrd`, `dfx-mgr-client`, configuration under `/etc/dfx-mgrd`, and firmware-package storage under `/lib/firmware/xilinx`. The supplied service uses notification-based startup and runs a firmware-detection helper before the daemon.

## Read the package structure as a compatibility graph

At the pinned revision, a base shell directory contains `shell.json` and its hardware artifacts. DFX accelerator subdirectories contain slot-specific entries and `accel.json`. A partial image for slot 0 is not automatically valid for slot 1, even when both implement the same algorithm.

The README defines shell types such as `PL_FLAT`, `PL_DFX` and `XRT_FLAT`. Flat and partial-reconfiguration packages have different requirements. Do not copy a DFX metadata example into a flat design merely because both include a bitstream.

The manager can report relationships between the base unique identifier and a partial image's parent identifier. A match is useful compatibility evidence. A missing identifier is weaker evidence, not a positive match. It does not prove that an image is safe simply because no mismatch was detected.

## Configuration controls discovery

The daemon configuration names firmware locations to monitor and can identify a default accelerator selection. The pinned README states that configuration changes require restarting the daemon. Editing the file while leaving the old process active does not establish that the new policy is in use.

Package discovery uses filesystem notifications. The documented limitations include unreliable notification behavior for network-filesystem use in this arrangement. An NFS development root can therefore behave differently from local storage even when files appear in a shell listing.

Installing a package should be an atomic, controlled operation from the manager's point of view. A directory that becomes visible before its bitstream and metadata finish copying can look like a broken package. Stage and publish complete compatible artifacts through the supported deployment process.

## The client socket is a control interface

The pinned README identifies `/var/run/dfx-mgrd.socket` as the client connection point. Exposing that socket to another process or container gives it access to the manager's control interface according to the daemon's policy. That is broader than reading a firmware directory.

A containerized application may use a host daemon, but the host still owns FPGA programming and drivers. Review which clients may request loads/removals and how competing requests are serialized. Two applications must not independently assume exclusive ownership of the same slot.

An application lease or equivalent management policy should connect use of an accelerator with its lifetime. A successful load request alone does not tell the manager when all users have released buffers and stopped hardware work.

## Follow one package from disk to service

For an illustrative DFX package, first validate the base-shell identity and available slot-specific partial image. Then check metadata syntax and the presence of the matching overlay and runtime artifacts. Next establish that the current shell and selected slot are suitable.

The manager requests the hardware transition through its integration layers. Driver creation and runtime discovery follow. The application finally opens the new accelerator and validates its own interface. Keep these stages in logs so “package found” cannot be mistaken for “application ready.”

If a load fails, distinguish package discovery, metadata parsing, compatibility checks, programming and device probe. A missing firmware file and a failed hardware isolation operation need different recovery. Repeatedly reinstalling the package cannot fix every stage.

## Removal still depends on driver correctness

Before asking the manager to remove an active accelerator, stop application submissions and finish or cancel in-flight work. The manager cannot infer that an application has kept a mapped buffer pointer in another thread. Driver cleanup must also stop bus masters before freeing their memory.

If replacement fails, keep the service unavailable until the actual hardware state is known. The daemon's remembered active package and the device's current functional state can diverge after a fault. Reconcile them explicitly during recovery.

The package can also contain policy that changes runtime configuration. For example, the pinned README describes XRT-flat handling that updates the active xclbin path used by VART. A read-only-root design must account for such writes rather than assuming firmware management is read-only outside the bitstream itself.

> [!NOTE]
> **Not run on the reference setup:** starting or controlling dfx-mgr, installing accelerator packages or changing slot state. Recipe, service and pinned upstream metadata documentation were inspected only.

## References

- Inspected BSP `meta-xilinx/meta-xilinx-core/recipes-bsp/dfx-mgr/dfx-mgr_2024.1.bb`.
- [dfx-mgr@ec70363 README](https://github.com/Xilinx/dfx-mgr/blob/ec70363a2a878737057995f922a9460d18aafa26/README.md), package schema and limitations.
- [Pinned service](https://github.com/Xilinx/dfx-mgr/blob/ec70363a2a878737057995f922a9460d18aafa26/src/dfx-mgr.service) and [client interface](https://github.com/Xilinx/dfx-mgr/blob/ec70363a2a878737057995f922a9460d18aafa26/src/dfxmgr_client.h).

- Executed PetaLinux 2024.1 `petalinux-create apps --help`
- AMD [dfx-mgr source](https://github.com/Xilinx/dfx-mgr)

---

<sub>← [DFX: Dynamic Function eXchange](04-dfx-dynamic-function-exchange.md) · [Chapter index](README.md) · [DMA Between PS and PL](06-dma-between-ps-and-pl.md) →</sub>
