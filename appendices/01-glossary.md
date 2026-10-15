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

---

<sub>[Chapter index](README.md) · [Command Cheat Sheets](02-command-cheatsheets.md) →</sub>
