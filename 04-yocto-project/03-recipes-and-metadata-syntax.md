# Recipes and Metadata Syntax

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-04](../ROADMAP.md#wp-04). The outline below is the agreed scope and will be replaced by the full text.

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Planned content

- `.bb`, `.bbappend`, `.bbclass`, `.inc` and `.conf` files
- Assignment operators and override syntax (`:append`, `:prepend`, `:remove`, machine overrides)
- Key variables: `SRC_URI`, `SRCREV`, `LICENSE`, `LIC_FILES_CHKSUM`, `S`, `B`, `D`, `WORKDIR`, `FILESEXTRAPATHS`
- `DEPENDS` vs. `RDEPENDS`, `PROVIDES`, `PREFERRED_PROVIDER` and `virtual/` targets
- Packaging: `PACKAGES`, `FILES:${PN}`, `${PN}-dev`, `${PN}-dbg`
- Recipe patterns for Makefile, CMake, autotools and prebuilt binaries

---

<sub>← [Layers and the Layer Model](02-layers.md) · [Chapter index](README.md) · [BitBake Tasks and the Build Process](04-bitbake-tasks-and-build-process.md) →</sub>
