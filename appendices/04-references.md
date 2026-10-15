# References and Sources

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[Appendices](README.md)** · Appendices

## AMD documents

| Document | Use |
| --- | --- |
| UG1085, Device Technical Reference Manual | Hardware mechanisms, boot, processors and controllers |
| UG1087, Register Reference | Register addresses, fields and access behavior |
| UG1137, Software Developer Guide | ZynqMP software stack and platform management |
| UG1144, PetaLinux Tools Reference Guide | Project configuration, builds and packaging |
| UG1283, Bootgen User Guide | Boot-container format, BIF and security |
| UG1400, Vitis Embedded Software Development | Application and debug flows |
| UG909, Dynamic Function eXchange | DFX design and implementation |
| PG252, Video Codec Unit | VCU interfaces and supported configurations |
| DS891, Device Family Overview | Variant capabilities |

Use the 2024.1 software/tool editions. The locally available UG1085 hardware reference is v2.5; hardware-document revision and software-release version are different labels.

## Pinned source families

| Repository | Release reference |
| --- | --- |
| `embeddedsw`, `device-tree-xlnx` | `xilinx_v2024.1` |
| `linux-xlnx`, `u-boot-xlnx`, `arm-trusted-firmware` | `xilinx-v2024.1` |
| `meta-xilinx`, `meta-xilinx-tools`, `meta-petalinux` | `rel-v2024.1`; archive exact commits for reproduction |
| Poky/OE-Core in the BSP | Inspect shipped metadata; reference identifies Yocto 4.1.4 Langdale |

Tags use different separators. Do not silently replace underscores with hyphens when checking out sources.

## Upstream references

- [Linux 6.6 documentation](https://docs.kernel.org/6.6/)
- [Yocto Project 4.1.4 documentation](https://docs.yoctoproject.org/4.1.4/)
- [U-Boot v2024.01 documentation](https://docs.u-boot.org/en/v2024.01/)
- [TF-A v2.10 documentation](https://trustedfirmware-a.readthedocs.io/en/v2.10/)
- [Devicetree specifications](https://www.devicetree.org/specifications/)
- [OpenAMP documentation](https://openamp.readthedocs.io/)
- [XRT 2024.1 documentation](https://xilinx.github.io/XRT/2024.1/html/index.html)

## Evidence and limits

The sibling `reference-setup/captures` directory contains earlier target sessions plus the new Bootgen decode, FIT listing and PetaLinux help captures. These are local reference artifacts, not files shipped inside this guide repository.

New chapters distinguish source-based explanation from executed tests. Notes marked **Not run on the reference setup** remain open validation work. No chapter should be marked fully verified merely because its outline has been replaced by prose.

---

<sub>← [Register Quick Reference](03-register-quick-reference.md) · [Chapter index](README.md)</sub>
