# BL32 and OP-TEE (Overview)

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[10 · Trusted Firmware-A (BL31)](README.md)** · Part IV: Boot


## Add a trusted OS only when the design needs one

**OP-TEE (Open Portable Trusted Execution Environment)** is a trusted operating system that can run as BL32. On the AArch64 arrangement discussed here, its core runs at Secure EL1 and trusted applications run at Secure EL0. Trusted Firmware-A remains the EL3 monitor that switches between Secure and Non-secure execution.

Linux applications do not become Secure by opening a TEE device. They remain Non-secure clients. The trusted application exposes a defined operation, checks its inputs and returns a result. The useful boundary is the service contract and protected state, not a general promise that all application behavior becomes trusted.

OP-TEE is optional. The reference BIF contains no BL32 payload. The saved TF-A message `Secure code at 0x60000000` comes from prepared BL32 entry information and does not establish that a trusted OS was loaded.

## Follow a client request through the layers

A client application uses the client API to open a session and invoke a command. Linux's TEE subsystem and OP-TEE driver turn that request into the supported Secure-call ABI. TF-A dispatches the call to the trusted OS, which selects the trusted application and command.

The response can contain both a transport-level result and a trusted-application result. A successful kernel ioctl does not necessarily mean the requested trusted operation succeeded. Preserve the result and origin information supplied by the client interface so that failures can be located at the correct layer.

The pinned Linux implementation is in `drivers/tee/optee/call.c` and `smc_abi.c`. It manages call state and shared-memory objects rather than passing an arbitrary userspace pointer directly to Secure code.

## One invocation can cross the boundary several times

The function `optee_smc_do_call_with_arg()` performs an SMC invocation and handles possible **remote procedure calls (RPCs)** back from the Secure side. Its companion `optee_handle_rpc()` handles cases such as shared-memory allocation/free, foreign-interrupt handling and command RPCs.

This means one client operation is not necessarily one uninterrupted period of Secure execution. The trusted OS can need a normal-world service and later resume. Linux scheduling and the userspace supplicant can therefore affect service availability and response time.

A trusted operation that needs normal-world storage must tolerate storage errors and unavailable support. Protecting data confidentiality or integrity does not force the normal world to provide timely service. Availability remains a separate design issue.

## Separate private memory from shared memory

Secure code, private data and trusted stacks need memory that the Non-secure world cannot read or modify under the intended hardware policy. Shared memory is deliberately accessible across the boundary and carries untrusted parameters or results.

A Linux `reserved-memory` node prevents normal allocation of a region when used correctly. It does not, by itself, program every memory-protection unit or block every DMA master. Review hardware protection and all bus masters that can reach the region.

A shared buffer needs a defined physical layout, size and cache/coherency model. The Linux driver tracks shared-memory objects and obtains physical addresses through the TEE memory APIs. Treating a userspace virtual address as a firmware physical address is not a valid shortcut.

## A worked command-design example

Assume a trusted application verifies a signed product configuration and returns a parsed, bounded result. This is an illustrative service design, not an implemented application in the reference image.

The command accepts a shared input buffer and an output buffer capacity. It checks parameter types, input length and allowed maximum size. It copies or safely processes the input under a design that accounts for concurrent Non-secure modification. It verifies the signature against its intended trust anchor, then parses the authenticated data.

The order matters. Parsing complex unauthenticated data before validation increases the exposed parser surface. Checking a shared buffer once and later rereading changed contents can also break the link between validation and use. The design must keep the verified bytes and the interpreted bytes consistent.

On a short output buffer, the command reports the required size through its defined interface rather than writing past the limit. On invalid input, it returns a stable error without exposing private state. Repeated calls and concurrent sessions must not corrupt shared trusted state.

## Integrate all boot and runtime components

A working setup needs a compatible OP-TEE image, the corresponding TF-A Secure payload dispatcher, correct boot-image metadata and valid memory placement. Linux needs the TEE driver and an accurate device-tree description. Userspace needs the matching client components and any required supplicant service.

The TF-A placement can change when a dispatcher is enabled. In the pinned ZynqMP header, the compact OCM default requires `SPD_none` as well as other conditions. Adding BL32 can therefore require reviewing BL31's own placement and reservation, not only allocating BL32 memory.

Keep versions and configuration together. A driver probe can fail if the firmware does not answer the expected discovery calls. A trusted OS banner can appear while session opening fails because the trusted application is missing or incompatible. An opened session can still fail on a command with unsupported parameter types.

## Diagnose by the last working interface

If Linux has no TEE device, inspect configuration, device-tree matching and firmware discovery. If the device exists but session opening fails, inspect application identity, loading and trusted-side error origin. If a call blocks, inspect pending RPC work and the supplicant as well as the Secure call path.

For memory faults, inspect the whole range and its attributes, not only the first address. For concurrency faults, record session identity and buffer ownership. For security claims, test invalid lengths, unsupported commands and modified shared data, not only a successful demonstration command.

> [!NOTE]
> **Not run on the reference setup:** OP-TEE boot integration, trusted-application execution, RPC service tests and hardware isolation. The Linux call/RPC path was inspected in the 2024.1 source. OP-TEE architecture documentation is used for the model, not as proof of a BSP-installed OP-TEE version.

## References

- [OP-TEE 4.1 architecture](https://optee.readthedocs.io/en/4.1.0/architecture/core.html), execution and world-switch model.
- [2024.1 Linux OP-TEE SMC implementation](https://github.com/Xilinx/linux-xlnx/blob/xilinx-v2024.1/drivers/tee/optee/smc_abi.c) and adjacent `call.c`.
- `arm-trusted-firmware@xilinx-v2024.1:plat/xilinx/zynqmp/{bl31_zynqmp_setup.c,include/platform_def.h}`.
- [TrustZone and OP-TEE integration](../26-zynqmp-hardware-security-and-secure-boot/08-trustzone-and-op-tee.md).

---

<sub>← [Building and Customizing TF-A](03-tfa-customization.md) · [Chapter index](README.md) · Next chapter: [11 · U-Boot](../11-u-boot/README.md) →</sub>
