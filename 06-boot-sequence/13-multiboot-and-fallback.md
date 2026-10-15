# Multiboot, Fallback and Golden Images

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Multiboot and fallback

Multiboot changes where the boot logic searches for an image. `CSU_MULTI_BOOT` participates in that selection, but its meaning must be interpreted with the boot medium and documented search rules. It is not a general byte-address register for every storage type.

A **golden image** is a known recovery image kept available when an update fails. An **A/B system** has two software slots and a controlled switch between them. These designs overlap, but neither guarantees recovery without a tested failure path.

## Product design

Keep the recovery image outside the normal update erase range. Record a boot attempt before trusting the new slot, and confirm success only after meaningful application health checks. A kernel reaching userspace can still leave the product unusable.

BootROM fallback, bootloader slot selection and userspace update policy are separate mechanisms. Decide which layer handles corruption, failed authentication and a runtime hang. A watchdog may detect the last case when header checks cannot.

Kria image-selector and recovery flows add platform-specific logic. Use the SOM's documented flash layout and update procedure rather than replacing it with generic ZynqMP offsets.

> [!NOTE]
> **Not run on the reference setup:** multiboot register changes, corrupted-image fallback and power-loss recovery tests on flash.

## References

- UG1085 (v2.5), Chapter 11, multiboot and image search
- [Software update strategies](../23-storage-updates-and-production/04-software-update-strategies.md)

---

<sub>← [Boot Memory Map: Who Loads What, Where](12-boot-address-map.md) · [Chapter index](README.md) · [JTAG Boot](14-jtag-boot.md) →</sub>
