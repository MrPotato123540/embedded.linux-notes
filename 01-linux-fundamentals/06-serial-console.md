# Serial Console

> [!NOTE]
> 🚧 **Planned.** This section is written in work package [WP-01](../ROADMAP.md#wp-01). The outline below is the agreed scope and will be replaced by the full text.

**[01 · Linux Fundamentals](README.md)** · Part I: Foundations

## Planned content

- UART basics: baud rate, 8N1, flow control, USB-UART bridges on AMD boards
- Host tools: `picocom`, `minicom`, `screen`, `tio`; the `dialout` group
- Which UART each boot stage prints to (FSBL, PMUFW, TF-A, U-Boot, Linux) and why output can be missing
- Linux console: `console=` boot argument, `earlycon`, `serial-getty@` service
- Capturing boot logs with timestamps

---

<sub>← [Shell and Essential Tools for Embedded Work](05-shell-and-essential-tools.md) · [Chapter index](README.md) · [SSH: Secure Shell](07-ssh.md) →</sub>
