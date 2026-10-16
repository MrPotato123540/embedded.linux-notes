# Glossary

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[Appendices](README.md)** · Appendices

## Hardware and boot

| Term | Meaning |
| --- | --- |
| APU | Application Processing Unit; Cortex-A53 processor cluster |
| RPU | Real-Time Processing Unit; Cortex-R5 subsystem |
| PMU / PMUFW | Platform Management Unit / its runtime firmware |
| CSU | Configuration Security Unit |
| PS / PL | Processing System / Programmable Logic |
| OCM / TCM | On-Chip Memory / Tightly Coupled Memory |
| DDR | Double Data Rate memory |
| MIO / EMIO | Multiplexed I/O / Extended Multiplexed I/O |
| GIC | Generic Interrupt Controller |
| EL | Exception level; processor privilege level |
| FSBL | First Stage Boot Loader |
| TF-A / BL31 | Trusted Firmware-A / its EL3 runtime stage |
| BIF | Boot Image Format description supplied to Bootgen |
| XSA | Xilinx Support Archive; exported hardware information |
| PCAP | Processor Configuration Access Port |
| PSCI | Power State Coordination Interface |
| SMC / HVC | Secure Monitor Call / Hypervisor Call |
| SMCCC | SMC Calling Convention |
| EEMI | Embedded Energy Management Interface |
| IPI | Inter-Processor Interrupt |
| ZynqMP | Short name for Zynq UltraScale+ MPSoC |

## Build and Linux

| Term | Meaning |
| --- | --- |
| BSP | Board Support Package |
| SDK / eSDK | Software Development Kit / extensible SDK |
| ABI | Application Binary Interface |
| sysroot | Root directory containing target headers and libraries for a toolchain |
| sstate | Shared-state cache of reusable build-task results |
| DTS / DTSI / DTB | Device-tree source / include / binary |
| DTC / DTG / SDT | Device Tree Compiler / Generator / System Device Tree |
| DMA / CMA | Direct Memory Access / Contiguous Memory Allocator |
| IOMMU / SMMU | I/O Memory Management Unit / Arm System MMU |
| UAPI | Userspace API exposed by the kernel |
| UIO | Userspace I/O framework |
| MTD / UBI / UBIFS | Memory Technology Device / Unsorted Block Images / UBI File System |
| PID | Process identifier |
| RTOS | Real-Time Operating System |
| AMP | Asymmetric Multiprocessing |
| RPMsg | Remote Processor Messaging |

## Acceleration and multimedia

| Term | Meaning |
| --- | --- |
| DFX | Dynamic Function eXchange; partial reconfiguration flow |
| XRT | Xilinx Runtime |
| DPU / VART | Deep Learning Processing Unit / Vitis AI Runtime |
| VCU | Video Codec Unit |
| DRM / KMS | Direct Rendering Manager / Kernel Mode Setting |
| V4L2 | Video4Linux2 |
| ALSA | Advanced Linux Sound Architecture |
| PTP / TSN | Precision Time Protocol / Time-Sensitive Networking |

## Security and production

| Term | Meaning |
| --- | --- |
| TEE / OP-TEE | Trusted Execution Environment / Open Portable TEE |
| XMPU / XPPU | Xilinx Memory / Peripheral Protection Unit |
| PPK / SPK | Primary / Secondary Public Key |
| BBRAM / PUF | Battery-backed RAM / Physical Unclonable Function |
| CA / CSR | Certificate Authority / Certificate Signing Request |
| HSM | Hardware Security Module |
| MAC / HMAC | Message Authentication Code / hash-based MAC; MAC also means Media Access Control in networking |
| SBOM / SPDX | Software Bill of Materials / Software Package Data Exchange |
| CVE | Common Vulnerabilities and Exposures identifier |
| IMA / EVM | Integrity Measurement Architecture / Extended Verification Module |
| A/B update | Two-slot update scheme with controlled boot selection |

## Common interfaces and formats

| Term | Meaning |
| --- | --- |
| API / ABI | Application Programming Interface / Application Binary Interface |
| CPU / GPU / FPGA | Central Processing Unit / Graphics Processing Unit / Field-Programmable Gate Array |
| AXI | Advanced eXtensible Interface; an Arm interconnect protocol family |
| MMIO / MMU | Memory-Mapped I/O / Memory Management Unit |
| IRQ | Interrupt request |
| ELF / FIT | Executable and Linkable Format / Flattened Image Tree |
| DTBO | Compiled device-tree overlay |
| ROM / RAM | Read-Only Memory / Random-Access Memory |
| FPD / LPD | Full-Power Domain / Low-Power Domain |
| PHY / MDIO | Physical-layer device / Management Data Input/Output |
| RGMII / SGMII | Reduced Gigabit Media Independent Interface / Serial Gigabit Media Independent Interface |
| UART / SPI / I2C | Universal Asynchronous Receiver/Transmitter / Serial Peripheral Interface / Inter-Integrated Circuit |
| CAN / USB | Controller Area Network / Universal Serial Bus |
| PCIe / QSPI | Peripheral Component Interconnect Express / Quad Serial Peripheral Interface |
| SD / eMMC | Secure Digital / embedded MultiMediaCard |
| NFS / TFTP | Network File System / Trivial File Transfer Protocol |
| DHCP / DNS | Dynamic Host Configuration Protocol / Domain Name System |
| TCP / UDP / RTP | Transmission Control Protocol / User Datagram Protocol / Real-time Transport Protocol |
| SSH / TLS / VPN | Secure Shell / Transport Layer Security / Virtual Private Network |
| AES / RSA | Advanced Encryption Standard / Rivest–Shamir–Adleman algorithm family |
| SHA | Secure Hash Algorithm |
| CBC / CTR / GCM | Cipher Block Chaining / Counter mode / Galois/Counter Mode |
| ECC | Elliptic-Curve Cryptography in security; Error-Correcting Code in memory/storage |
| ECDSA / ECDH | Elliptic Curve Digital Signature Algorithm / Elliptic Curve Diffie–Hellman |
| IV | Initialization vector; requirements depend on the algorithm/mode |
| CI | Continuous Integration |
| GPL / LGPL | GNU General Public License / GNU Lesser General Public License |
| SPDX identifier | Standard short identifier for a license expression |

Definitions are explained with context and sources in the linked chapters from the [guide contents](../README.md#contents).
## Memory and ownership vocabulary

| Term | Meaning and engineering consequence |
| --- | --- |
| Virtual address | Address interpreted through a CPU's current translation context; not automatically valid for another process or a device |
| Physical address | Address in a particular physical system view; remote processors can have a different local view |
| DMA address / IOVA | Address returned for device access by the DMA mapping layer; it may differ from the CPU physical address |
| Coherent memory | Memory whose relevant CPU/device views have the required coherence; ordering and ownership rules still apply |
| Streaming DMA mapping | Mapping with a defined transfer direction and explicit CPU/device ownership transitions |
| Memory barrier | Operation that constrains ordering; it is not a general replacement for cache synchronization |
| MMIO accessor | Kernel interface for device-register access, with architecture-specific I/O semantics |
| Lifetime | Interval during which an object, mapping, buffer or permission remains valid |
| Use-after-free | Access after an object's lifetime ends; a stale pointer can refer to reused memory |
| TOCTOU | Time of check to time of use; checked data changes before the operation that relies on it |
| W1C | Write one to clear; writing a set bit acknowledges/clears a corresponding status bit where the register defines this behavior |
| RMW | Read-modify-write; safe only when the register's read and write semantics permit it |
| SG | Scatter-gather; a transfer described by multiple memory segments |
| dma-buf | Kernel framework for sharing buffers between drivers; shared storage still needs format, lifetime and synchronization agreement |
| Fence | Completion/synchronization object used to coordinate access to shared work or buffers |

See [DMA and memory management](../14-kernel-modules-and-drivers/06-dma-and-memory-management.md). “Contiguous” must say which address space is contiguous. A buffer can be contiguous for a device through an IOMMU mapping without having contiguous CPU physical pages. A file's byte offset is neither kind of memory address.

## Boot, execution and update vocabulary

| Term | Meaning and engineering consequence |
| --- | --- |
| Entry point | Address where execution starts; it can differ from the lowest loadable address |
| `PT_LOAD` | ELF program-header type describing a loadable segment |
| `p_filesz` / `p_memsz` | Stored segment size / runtime memory size; zero-initialized memory can make the latter larger |
| BSS | Zero-initialized static storage; normally occupies memory without equivalent initialized file bytes |
| BL32 / BL33 | TF-A names for the optional Secure payload / Non-secure next-stage payload |
| Control FDT | Flattened device tree used by U-Boot itself; distinct from the tree handed to Linux |
| Root of trust | Starting mechanism and trust material on which later verification relies |
| TCB | Trusted Computing Base; components whose failure can break the selected security property |
| Verified boot | Boot flow that enforces acceptance checks before trusting later content |
| Measured boot | Recording selected measurements for assessment; measurement alone does not imply rejection |
| Rollback protection | Policy that rejects previously valid but no longer allowed versions |
| Trial boot | Temporary selection of a candidate release pending a defined health confirmation |
| Atomic operation | Operation observed as all-or-nothing at its stated boundary; not a general promise about the whole update |
| Durable state | State that survives the specified failure, such as power loss, after the required storage operations |

See [ELF and boot memory](../06-boot-sequence/06-fsbl-stage.md), [chain of trust](../26-zynqmp-hardware-security-and-secure-boot/02-chain-of-trust.md) and [secure updates](../27-linux-and-network-security/04-secure-updates.md). Always name the boundary of an atomicity or durability claim. A successful userspace write is not automatically a durable multi-file transaction.

## Security and service vocabulary

| Term | Meaning and engineering consequence |
| --- | --- |
| AEAD | Authenticated Encryption with Associated Data; authenticates visible context as well as protected ciphertext |
| KDF | Key Derivation Function; derives keys from suitable input and a defined context |
| Nonce | Protocol-specific value whose uniqueness/freshness requirements must be maintained across the key lifetime |
| Salt | Usually public derivation/hash input used to separate instances or precomputation domains |
| EKU | Extended Key Usage; X.509 constraints on the intended purpose of a certificate |
| SAN | Subject Alternative Name; X.509 identity field used in relevant peer-name checks |
| CRL / OCSP | Certificate Revocation List / Online Certificate Status Protocol |
| PSK / SSK | Primary Secret Key / Secondary Secret Key in the Bootgen signing hierarchy; PSK can mean pre-shared key in other protocols |
| RPMB | Replay Protected Memory Block; storage feature used by supported secure-storage designs |
| LSM | Linux Security Module; framework for additional security enforcement hooks and policy |
| DAC / MAC | Discretionary / Mandatory Access Control; “MAC” here does not mean a network address or message authentication code |
| PAM | Pluggable Authentication Modules; account, authentication and session functions depend on the deployed stack |
| PIE / RELRO | Position-Independent Executable / Relocation Read-Only; build properties used by exploit mitigations |
| Seccomp | Secure computing system-call filtering; reduces permitted kernel entry points |
| RPC | Remote Procedure Call; a request/reply interface across a process or execution boundary |

## Additional system terms

The later system chapters also use these domain-specific terms:

| Term | Meaning and engineering consequence |
| --- | --- |
| SMP | Symmetric Multiprocessing; one OS schedules work across cooperating processors |
| vCPU | Virtual CPU presented to a guest; its execution depends on hypervisor scheduling |
| Dom0 / DomU | Xen control domain / guest domain; device ownership and guest permissions still need explicit configuration |
| ASoC | ALSA System on Chip; framework joining audio CPU interfaces, codecs and board links |
| DAPM | Dynamic Audio Power Management; tracks audio routes and related power needs |
| PCM | Pulse-Code Modulation; sampled audio data with an agreed format, channel count and rate |
| PHC | PTP Hardware Clock; hardware time source exposed through the relevant Linux clock interface |
| PEB / LEB | Physical / Logical Eraseblock; UBI maps logical eraseblocks onto physical flash storage |
| URB | USB Request Block; a submitted transfer has a lifetime through completion or cancellation |
| UDC | USB Device Controller; hardware/driver side of a Linux USB gadget |
| GOP | Group of Pictures; video coding structure that affects dependencies, seeking and latency |
| NAPI | Linux network-driver polling mechanism that coordinates receive work with interrupts |
| BAR | Base Address Register; PCI/PCIe resource description, distinct from a device's DMA address |
| MSI / MSI-X | Message Signaled Interrupts / extended form; interrupt messages replace a dedicated interrupt line where supported |
| OPP | Operating Performance Point; a supported operating combination such as frequency and voltage |
| RCU | Read-Copy Update; synchronization model whose grace periods matter before old data is freed |
| DAP / TAP | Debug Access Port / Test Access Port; distinct parts of processor debug and test access |
| JTAG | Joint Test Action Group; common name for the standardized test-access interface used by supported debug flows |
| SDEI | Software Delegated Exception Interface; firmware-to-OS event mechanism with build and runtime requirements |
| PPI / SPI in GIC context | Private / Shared Peripheral Interrupt; SPI has a different meaning in the serial-bus chapter |

## Similar words that must stay separate

“Signed,” “encrypted” and “trusted” are not synonyms. A signature needs a trusted verification key. Encryption needs a correct key and protocol, and does not alone define who approved the content. Trust is the system's acceptance policy based on these mechanisms.

“Built,” “packaged” and “booted” are also different observations. Compiling firmware produces an executable. Packaging combines existing artifacts into a container. Booting executes a path on a named target. Recreating a byte-identical `BOOT.BIN` from supplied inputs establishes packaging reproducibility, not a fresh source build.

“Supported” must name the layer. A binding schema may describe a value that a particular driver release rejects. A userspace header may declare an API that the loaded firmware cannot serve. Follow the complete path before claiming product support.

Use IEC units when binary size matters: KiB is 1,024 bytes and MiB is 1,048,576 bytes. A 32-bit word is four bytes in the boot-image fields discussed here. Convert word offsets before comparing them with file sizes or memory addresses, and state whether an interval includes its final address.


---

<sub>[Chapter index](README.md) · [Command Cheat Sheets](02-command-cheatsheets.md) →</sub>
