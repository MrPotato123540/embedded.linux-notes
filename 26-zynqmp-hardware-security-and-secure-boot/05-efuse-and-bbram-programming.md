# eFUSE and BBRAM Programming

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[26 · ZynqMP Hardware Security and Secure Boot](README.md)** · Part XIV: Security

## Provisioning is a manufacturing operation

Security provisioning changes the device's future boot and debug behavior. Use the supported `xilskey`/device security programming flow for the exact device and tool release. A generic register-write script is not an adequate replacement.

> [!CAUTION]
> eFUSE programming is irreversible. Wrong key hashes, revocation settings or access controls can permanently prevent intended boot or recovery. BBRAM key loss can also make encrypted images unusable until a supported reprovisioning path is available.

## Required record

Prepare the device identity, intended policy, public-key hashes, programming tool version, operator authorization and expected verification results. Keep private keys out of the device log. Verify the input calculations independently before programming.

Test the whole plan on a development device: valid boot, invalid boot, power-cycle, key retention and recovery. Only then freeze a production procedure with explicit pass/fail criteria.

> [!NOTE]
> **Not run on the reference setup:** any eFUSE or BBRAM write. This guide does not present untested irreversible commands as a recipe.

## References

- AMD UG1283 (2024.1), key sources and authentication
- `embeddedsw@xilinx_v2024.1:lib/sw_services/xilskey/`

---

<sub>← [Boot Image Encryption (AES-GCM)](04-encryption.md) · [Chapter index](README.md) · [Secure Boot With PetaLinux](06-secure-boot-in-petalinux.md) →</sub>
