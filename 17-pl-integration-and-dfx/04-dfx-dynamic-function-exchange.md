# DFX: Dynamic Function eXchange

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[17 · PL Integration, FPGA Manager and DFX](README.md)** · Part VIII: Programmable Logic and Acceleration

## Static and reconfigurable logic

**Dynamic Function eXchange (DFX)** changes a reconfigurable region while a compatible static design remains loaded. A reconfigurable module must match the partition interface and implementation constraints of that static design.

The software sequence must prevent transactions crossing an unstable boundary. Stop clients, drain transfers, isolate or decouple the region, apply required resets and load the matching partial bitstream. Restore communication only after the hardware and software state are ready.

## Design outputs

Vivado's DFX flow produces related static and partial artifacts. Package their compatibility information with overlays and application metadata. Two partial bitstreams for different static builds are not interchangeable even if they use the same region name.

## Failure testing

Test load failure, interrupted application shutdown and repeated module changes. Recovery must leave the system in a known state rather than exposing half-configured devices. Review clocks and reset behavior across each transition.

> [!NOTE]
> **Not run on the reference setup:** physical partial reconfiguration and interruption tests.

## References

- AMD UG909, Dynamic Function eXchange, release matching Vivado 2024.1
- Linux FPGA-region/bridge documentation

---

<sub>← [Linux FPGA Manager](03-fpga-manager.md) · [Chapter index](README.md) · [dfx-mgr and Accelerator Packages](05-dfx-mgr.md) →</sub>
