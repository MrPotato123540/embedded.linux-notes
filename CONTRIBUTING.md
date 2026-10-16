# Contributing and Writing Rules

These rules keep about 180 sections, written over many work packages, consistent with each other. Read them before you write or change anything.

## What every section must do

- Be correct for **PetaLinux 2024.1**, and say so explicitly when other releases behave differently.
- Explain the **mechanism**, not just the steps. A reader should be able to predict what happens when something changes.
- Give a **source** for every hard fact.
- Show only **commands that have been run** and output that came from a real system.

## Required technical depth

A populated outline is not a completed section. Keep the technical depth of the detailed architecture chapters while using B1–B2 English.

- Explain the mechanism and its state transitions, data flow or ownership rules.
- Follow at least one concrete example through the relevant files, functions, artifacts or runtime observations. Explain what each result means.
- Give the exact release-specific source path when discussing implementation behavior. Distinguish a source default from an observed board value.
- Explain failure cases with evidence that separates competing causes, not only a list of possible problems.
- State compatibility limits, memory/resource lifetimes and integration effects when they matter to the topic.
- Separate executed experiments, inspected sources and proposed hardware procedures. Never invent successful output.
- Use tables, diagrams and code where they clarify the mechanism. Extra length and repeated checklists are not substitutes for engineering detail.

The advanced-depth revision is tracked separately from initial draft coverage in [ROADMAP.md](ROADMAP.md). Do not mark the entire guide complete because every file has prose.

## Language and tone

- English (US spelling), present tense, second person ("you"), active voice.
- Write at **B1–B2 English level**. Use familiar words and short, direct sentences. Explain necessary technical terms when they first appear.
- Keep the full technical depth: preserve exact names, mechanisms, limits, source references and verification notes. Simplify the language, not the engineering.
- Keep paragraphs short. One idea per paragraph.
- Spell out each acronym at its first use in a section, and add it to the [glossary](appendices/01-glossary.md).
- Use exact numbers and names, not adjectives. Write "256 KB OCM at `0xFFFC0000`", not "a small on-chip memory".

## Terminology

| Use | Avoid |
| --- | --- |
| **ZynqMP** after a first mention of "Zynq UltraScale+ MPSoC" | ZU+, "MPSoC" on its own |
| **AMD** (write "AMD (formerly Xilinx)" at the first mention in a chapter). Keep "Xilinx" where it is part of a name: repositories, drivers, tools, compatible strings | Mixing AMD and Xilinx for the same thing |
| **TF-A** (Trusted Firmware-A). Mention "ATF" once as the older name | ATF as the main term |
| **PMU firmware** or **PMUFW** | PMU FW, pmufw (except in file and recipe names) |
| **device tree** in prose; `.dts`, `.dtsi`, `.dtb`, `.dtbo` for files | DT on its own in prose |
| **`BOOT.BIN`** for the file, **boot image** for the concept | |
| **PS**, **PL**, **APU**, **RPU**, **CSU**, **OCM**, **TCM**: spelled out once per chapter | |

## Files and naming

- Chapter folders are named `NN-kebab-case/`. Section files are named `NN-kebab-case.md` and numbered in reading order.
- Every chapter folder has a `README.md` index with a section table. Update its status column when a section changes state.
- Put images in an `assets/` folder inside the chapter, for example `06-boot-sequence/assets/boot-flow.svg`. Prefer inline Mermaid, then SVG. Use PNG only for screenshots.
- Before renaming or moving a file, search for every link to it and update them all.

## Section template

When a stub is turned into a full section, use this structure. Drop the headings that do not apply, but keep the order.

````markdown
# <Section title>

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC · <boards, if relevant>

**[NN · Chapter title](README.md)** · Part <X>: <Part name>

## In short

Three to five bullets: what the reader will understand or be able to do afterwards.

## Concepts

The mechanism first: what it is, why it exists, how it works.

## On ZynqMP

Platform specifics: processors, addresses, registers, files.

## Hands-on

Commands with prompts, followed by real (trimmed) output.

## PetaLinux 2024.1 specifics

Where this lives in a project, which recipe or config option controls it, and how to change it.

## Pitfalls

What commonly goes wrong, and how to recognize it.

## Debugging

How to find out what is happening when it does not work.

## References

The sources used, in the citation formats below.

---

<sub>Keep the navigation line from the stub.</sub>
````

## Commands and code blocks

- Always tag the language of a code block:

  | Tag | Use for |
  | --- | --- |
  | `console` | Interactive sessions, with prompts and output |
  | `bash` / `sh` | Scripts that can be copied as a whole |
  | `text` | Logs, boot output, tool output without commands |
  | `c`, `dts`, `make`, `python`, `tcl` | Source code, device tree, Makefiles, scripts, XSDB |

- Use the prompts from the [README conventions](README.md#conventions): `$` (host), `target$` (target, normal user), `target#` (target, root), `ZynqMP>` (U-Boot), `xsdb%` (XSDB).
- Trim long output with `...`, but never invent output. If an example was not captured from a real system, say so.
- You may anonymize host-specific details in output (user names, host names, home directories) as long as nothing else changes.
- Put a `[!WARNING]` or `[!CAUTION]` in front of anything destructive (`dd`, `flash_erase`, `sf erase`, eFUSE programming).

## Reference setup

Unless a section says otherwise, examples were captured on this setup:

| Role | What it is |
| --- | --- |
| Host | Ubuntu 22.04 LTS, PetaLinux 2024.1 installed in `/opt/pkg/petalinux24.1`, Vivado/Vitis 2024.1 |
| Target | The prebuilt image of the `xilinx-zcu106-2024.1` BSP running in AMD's QEMU (the same images `petalinux-boot qemu --prebuilt 3` uses), with the serial console on a socket and SSH forwarded to host port 2222 |

Some commands need real hardware (a USB-UART cable, a JTAG probe, an SD card) or root on the host (installing packages, exporting NFS shares). When such a command could not be run on the reference setup, mark it like this, and keep the mark until someone has run it:

```markdown
> [!NOTE]
> **Not run on the reference setup:** <what, and why>.
```

## Facts, sources and verification

Every address, register (name, offset, bit field), default value, size, magic number, command option and configuration symbol needs a source. Use one of these formats:

| Source type | Format | Example |
| --- | --- | --- |
| AMD document | `<doc> (<version>), <chapter/section>, <table/figure>` | UG1085 (vX.Y), Chapter N, Table N-M |
| Source code | `repo@tag:path` (add `#Lnn` for a line) | `embeddedsw@xilinx_v2024.1:lib/sw_apps/zynqmp_fsbl/src/xfsbl_main.c` |
| Real project | `<bsp>:path` | `xilinx-zcu106-2024.1:pre-built/linux/images/bootgen.bif` |

For register tables and default values, prefer a short quote from the source over a paraphrase.

Mark facts that have not been verified yet. A work package cannot be closed while its chapter still contains one of these:

```markdown
> [!WARNING]
> **Unverified:** <claim>. To check: <where>.
```

Mark differences between releases like this:

```markdown
> [!NOTE]
> **Release difference:** <behaviour in older or newer releases>.
```

Clone source repositories **outside** this repository, for example into `~/xlnx-src/2024.1/`, and always check out the pinned tag.

## Callouts

The guide uses GitHub alert syntax:

| Alert | Use for |
| --- | --- |
| `> [!NOTE]` | Background information and release differences |
| `> [!TIP]` | Shortcuts and productivity hints |
| `> [!IMPORTANT]` | Facts that are required for a correct result |
| `> [!WARNING]` | A risk of breaking the board or losing data, and unverified content |
| `> [!CAUTION]` | Irreversible operations: eFUSE programming, key loss, permanent lock-down |

## Diagrams and tables

- Use Mermaid for flows, sequences and state machines. GitHub renders it directly.
- Use Markdown tables for memory maps and register layouts. Sort addresses in ascending order and write ranges as `start – end (size)`.
- Do not copy figures from AMD documents. Redraw them and cite the original.

## Quoted material

- Quote only short excerpts from AMD documents and source files, and always say where they come from.
- Code excerpts keep the license of their origin. Include the `SPDX-License-Identifier` when you quote more than a few lines.

## Workflow

1. Work on one work package at a time, directly on `main`, as requested by the repository owner. Do not create work-package branches.
2. Use commit messages of the form `WP-06: add boot modes section`.
3. When a section is finished, replace its stub, update the status in the chapter `README.md` and update [ROADMAP.md](ROADMAP.md).
4. Before closing a work package, run a link checker (for example `lychee` or `markdown-link-check`) and resolve every *Unverified* warning.
