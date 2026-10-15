# Network Configuration on the Target

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[22 · Networking and Peripherals](README.md)** · Part XI: Networking and Peripherals

## One owner per interface

Use a deliberate network manager: ifupdown, systemd-networkd or NetworkManager. Competing managers can overwrite addresses, routes and DNS settings and make behavior appear random.

A static setup needs an address and prefix, routes and DNS where required. DHCP supplies selected settings dynamically, but does not guarantee that a file server or remote application is available. The hostname is separate from both address assignment and name resolution.

## Diagnosis

Inspect link state, local addresses, routing and resolver configuration in that order. Test a local peer by address before blaming DNS. For a direct development cable, avoid conflicting subnets with other host interfaces.

Keep product configuration in the image or a defined persistent data store. A manual change after boot may disappear on reboot or be replaced by the network manager.

## References

- [Development networking](../01-linux-fundamentals/08-networking-for-development.md)
- Manuals for the network manager selected by the image

---

<sub>← [Ethernet (GEM)](01-ethernet.md) · [Chapter index](README.md) · [USB Host and Gadget](03-usb.md) →</sub>
