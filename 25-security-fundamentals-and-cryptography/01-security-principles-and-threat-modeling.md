# Security Principles and Threat Modeling

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[25 · Security Fundamentals and Cryptography](README.md)** · Part XIV: Security

## Start with assets and trust boundaries

Security protects specific assets against specific threats. List firmware, device identity, user data, control outputs and service availability. Then identify who can reach network ports, storage, update interfaces, debug connectors and physical devices.

| Property | Question |
| --- | --- |
| Confidentiality | Who can read the data? |
| Integrity | Who can change it without detection? |
| Availability | Can the required service continue? |
| Authenticity | Can the source or identity be verified? |
| Accountability | Can an action be traced reliably? |

A signature can support accountability, but technical signing alone does not settle legal non-repudiation.

## Threat modeling

STRIDE groups threats as spoofing, tampering, repudiation, information disclosure, denial of service and elevation of privilege. Apply it at each boundary: network-to-service, application-to-driver and updater-to-bootloader.

Use several controls with different failure modes. Secure boot checks software origin; least privilege limits runtime damage; signed updates support maintenance. None replaces the others.

Document assumptions and test negative cases, such as a modified image, expired credential or full storage. Defaults should be safe before an operator changes configuration.

## References

- Microsoft STRIDE threat-modeling documentation
- NIST SP 800-160, systems security engineering

---

<sub>[Chapter index](README.md) · [Cryptography Primer](02-cryptography-primer.md) →</sub>
