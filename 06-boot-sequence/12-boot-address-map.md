# Boot Memory Map: Who Loads What, Where

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[06 · Boot Sequence](README.md)** · Part IV: Boot

## Addresses belong to a boot flow

A storage offset, load address and entry address are different values. Storage tells the loader where bytes are stored. The load address tells it where to place them. The entry address tells the processor where execution starts.

Bootgen 2024.1 decoded these addresses from the reference `BOOT.BIN`:

| Partition | Load address | Entry address |
| --- | --- | --- |
| FSBL | `0xFFFC0000` | `0xFFFC0000` |
| TF-A BL31 | `0xFFFEA000` | `0xFFFEA000` |
| Device tree | `0x00100000` | Not executable |
| U-Boot | `0x08000000` | `0x08000000` |

The saved U-Boot network session separately loads `Image` at `0x00200000` and `system.dtb` at `0x00100000`. Those are later-stage choices. They do not relocate the earlier firmware automatically.

## Overlap checks

For every live object, record the start address and full size. Include decompressed kernel size, ramdisk, DTB growth space, U-Boot relocation, stacks and resident firmware. Two files can have different starting addresses and still overlap.

Use half-open ranges `[start, start + size)` when calculating collisions. Also check which addresses are reachable by the loader and the destination processor. An address valid for an A53 view may mean something else to an R5.

Do not invent one universal table for script, FIT and ramdisk addresses: read the environment and script shipped with the chosen image.

## Add size, lifetime and owner to every address

A useful boot memory map records at least the address range, owner, purpose and lifetime of each object. Two objects may legally reuse memory at different times. Two objects with different starting addresses may still overlap while both are live.

For ranges `[A, A + L)` and `[B, B + M)`, overlap exists when `A < B + M` and `B < A + L`. Use arithmetic wide enough for the address space and check overflow. This test is necessary but not sufficient: the region must also be valid memory with the correct access and security attributes.

A runtime firmware region, a temporary loading buffer and an OS payload have different lifetimes. Reusing a finished temporary buffer can be valid. Reusing TF-A's runtime data because its initial banner has already printed is not valid.

## ELF memory size differs from stored file size

The reference FSBL ELF's first load segment has file size `0x1F448` and memory size `0x25368`, starting at `0xFFFC0000`. Its file-backed bytes do not include every runtime allocation. Additional ELF regions include handoff parameters and a bitstream buffer.

The reference BL31 ELF enters at `0xFFFEA000`. Its section layout includes stacks, BSS, translation tables and coherent memory beyond its initialized data. Section inspection reaches an end address of `0xFFFFE000` for the coherent-memory section. A map based only on the packaged initialized bytes would miss these runtime requirements.

There can also be reuse between early-stage regions according to the firmware's loading and handoff design. Do not declare every ELF segment intersection a defect without examining lifetime and loading behavior. Conversely, do not assume an overlap is safe merely because a reference boot once succeeded. Read the linker scripts and loader sequence for the exact builds involved.

## Container addresses and payload addresses differ

A FIT can be loaded into a staging area and then supply a kernel, DTB and initramfs to different final locations. The container's address is not the kernel's entry address. A compressed kernel has a stored range and a decompressed destination range, and both may be needed during loading.

The reference generated configuration stages the FIT at `0x10000000`, while its FIT metadata gives the kernel load and entry as `0x00200000`. The stored kernel payload is gzip-compressed. Check the expanded kernel size and loader behavior before deciding whether those regions can safely coexist with other data.

For a raw-image path, the Arm64 header gives placement and size requirements. Do not replace those requirements with a load address copied from another project's script. The loader must also preserve the final DTB and initramfs through kernel entry.

## U-Boot can relocate data before handoff

The saved boot log starts with the DTB at `0x00100000` and the ramdisk image at `0x04000000`. It later reports moving the DTB to `0x776A0000` and the ramdisk data to `0x776B1000`, with the ramdisk ending at `0x77BE7393`.

These are observations from the recorded run, not fixed addresses promised for every boot. They demonstrate that initial load addresses and final Linux input addresses can differ. Inspect the final loader messages and tree when diagnosing a collision.

Leave room for device-tree modifications. A loader can add properties such as boot arguments or initramfs bounds. The original DTB file length may not equal the working buffer capacity needed by those edits.

## Firmware and Linux must agree on reserved memory

Linux uses the described usable memory and honors the reservation mechanisms provided to it. Memory owned by firmware, remote processors or fixed shared buffers must be represented consistently. A buffer known only to an R5 linker script can still be allocated by Linux if Linux was never told to reserve it.

Reservation also does not establish cache coherency or access permissions by itself. A shared-memory design needs address agreement, ownership, cache policy and synchronization. Those requirements continue after the boot map has been validated.

## Build the map from evidence

Inspect the actual firmware ELFs, decoded boot image, boot script/environment, FIT contents and final DTB. Record whether each value is a storage offset, a RAM address or an entry point. Then assign sizes and lifetimes from the relevant format and source implementation.

The numerical observations in this section were checked with `readelf`, Bootgen and the saved logs. A complete collision proof for a changed image still needs its own artifact set, including decompressed sizes and runtime reservations. No new universal address layout is proposed here.

## References

- `reference-setup/captures/bootgen-2024.1-read.txt`
- Saved `cap-wp01-uboot.txt`
- [System address map](../03-zynqmp-architecture/04-memory-map.md)

---

<sub>← [User-Space Startup](11-user-space-startup.md) · [Chapter index](README.md) · [Multiboot, Fallback and Golden Images](13-multiboot-and-fallback.md) →</sub>
