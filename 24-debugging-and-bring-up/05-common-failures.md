# Common Failures and Fixes

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## Failure classification

| Stage | Evidence to collect |
| --- | --- |
| Build parsing | Recipe/layer revision and first parse error |
| Fetch/build | Task log, source URL/revision and generated command |
| Boot firmware | Boot mode, reset reason, serial log and ELF hashes |
| Kernel probe | Live device tree, configuration and first driver error |
| Root filesystem | Root arguments, detected devices and image format |
| Application | Exact executable, libraries, configuration and logs |

A useful report explains expected behavior, actual behavior, minimal reproduction and the last known working version. Include board revision and whether the test used QEMU or hardware.

Search the exact error and affected component in AMD answer records, upstream mailing lists and source history. Confirm that a proposed fix applies to the same release and hardware. A similar symptom is not enough.

Change one variable at a time and keep the failing artifact until the cause is understood.

## References

- [Boot troubleshooting](../06-boot-sequence/15-boot-troubleshooting.md)
- Linux kernel reporting-issues documentation

---

<sub>← [DDR Bring-Up and Memory Testing](04-ddr-bring-up.md) · [Chapter index](README.md) · Next chapter: [25 · Security Fundamentals and Cryptography](../25-security-fundamentals-and-cryptography/README.md) →</sub>
