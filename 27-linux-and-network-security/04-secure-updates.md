# Secure Software Updates

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[27 · Linux and Network Security](README.md)** · Part XIV: Security

## Verify before activation

An update bundle needs authenticated metadata and payloads, a target-compatibility check and a controlled installation transaction. Transport encryption protects the download channel; it does not replace a release signature that can be checked offline.

A valid signature does not prove freshness. Define rollback protection and where the accepted version state is stored. If an attacker can replace that state together with the image, the rollback check may have no effect.

## RAUC and SWUpdate integration

Connect the selected updater to the real slot layout and boot-success mechanism. Keep verification keys trusted by the existing image and provide a planned rotation path. Test interrupted download, interrupted write, invalid signature, wrong hardware target and failed first boot.

The recovery image must enforce compatible security policy. An unsigned recovery path can bypass a signed normal path.

> [!NOTE]
> **Not run on the reference setup:** secure updater integration and rollback/power-loss negative tests.

## References

- RAUC security and bootloader-integration documentation
- SWUpdate signed-image documentation
- [Update architecture](../23-storage-updates-and-production/04-software-update-strategies.md)

---

<sub>← [Network Security](03-network-security.md) · [Chapter index](README.md) · [Vulnerability Management](05-vulnerability-management.md) →</sub>
