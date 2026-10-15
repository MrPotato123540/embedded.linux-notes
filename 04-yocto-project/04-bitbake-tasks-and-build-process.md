# BitBake Tasks and the Build Process

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-04](../ROADMAP.md#wp-04). The outline below is the agreed scope and will be replaced by the full text.

**[04 · The Yocto Project](README.md)** · Part III: Build Systems

## Planned content

- The task chain: fetch, unpack, patch, configure, compile, install, package, rootfs, image
- Directory layout of `tmp/work`, recipe sysroots and `deploy`
- Shared state (sstate) cache, `DL_DIR` and hash equivalence
- Everyday commands: `bitbake -c`, `-e`, `-g`, `-k`, `-f`, `cleansstate`, `devshell`, `listtasks`
- Reading `temp/log.do_*` and `run.do_*` to debug failed tasks

---

<sub>← [Recipes and Metadata Syntax](03-recipes-and-metadata-syntax.md) · [Chapter index](README.md) · [Images, Packagegroups and Features](05-images-packagegroups-and-features.md) →</sub>
