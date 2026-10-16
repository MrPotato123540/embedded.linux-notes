# Common Failures and Fixes

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[24 · Debugging and Board Bring-Up](README.md)** · Part XIII: Debugging and Bring-Up

## Find the first boundary that did not complete

A boot failure is easier to understand as a chain of contracts than as a list of error strings. Power and reset permit BootROM execution. BootROM selects and loads early firmware. FSBL initializes the platform and loads later stages. TF-A and U-Boot establish the Linux handoff. Linux probes devices and starts userspace.

For each failure, record the last successful observable event and the next expected event. A final UART line is useful, but buffered output and console changes can make it an incomplete view. Combine serial logs with artifact inspection and, when appropriate, controlled debug observations.

Keep the exact image hashes, board revision and boot mode. "The same image" should mean the same bytes, not the same filename. A working comparison is valuable only when its hardware and configuration differences are known.

## Case 1: the board is silent

Silence can mean no execution, wrong console or output sent before the terminal was ready. First establish power, reset and boot-mode inputs. Then verify the UART wiring, level standard, selected port and baud settings. A swapped serial connection can imitate a completely dead processor.

If JTAG identifies the device, that proves a debug path but not successful boot. If the processor executes code without UART output, inspect the console's clock and pin route. If no expected code runs, inspect boot source and image validity before changing Linux.

Avoid using a debugger initialization script as an invisible fix. If a board boots only after that script, preserve the difference: it may reveal missing cold-boot clock, DDR or reset initialization.

## Case 2: FSBL stops before the next stage

Inspect the BIF and the actual boot image decode together. Processor destination, load address, entry address, exception level and security attributes answer different questions. A payload can be present in the container yet be loaded or handed off incorrectly.

The reference BIF's five inputs do not produce five ordinary image headers: PMU firmware uses special `pmufw_image` handling. Do not diagnose a missing image solely from a naive input-count comparison. Use Bootgen's decoded structure and the specific format rules.

If the failure follows a hardware-export change, confirm that the loaded FSBL contains the matching initialization. A new DTB cannot repair early DDR settings embedded in old firmware. If authentication is enabled, preserve the exact failure stage and key-policy context instead of treating every load failure as a storage error.

## Case 3: U-Boot starts, but Linux does not

First determine whether U-Boot found the intended kernel, initramfs and device tree. A successful file read is not the same as successful image parsing or verification. Check the image format, target architecture and selected boot command.

Next review placement. Compressed image input, decompressed output, initramfs, DTB and bootloader runtime regions must not overlap in unsafe ways. A valid image copied to an unsuitable address can fail before Linux prints anything.

The saved QEMU flow directly loads artifacts and reports JTAG mode. It does not validate a physical SD/QSPI search path. If emulation works and physical boot fails, compare the loading path before assuming that the kernel has a hardware-only bug.

## Case 4: Linux starts, then cannot mount root

Read the actual kernel command line and the first root-device errors. Determine whether the expected root is initramfs, block storage, UBI/UBIFS or network root. Each requires different drivers and setup stages.

A block root needs the controller, media, partition and filesystem available before mounting. If required support is modular, an initramfs must provide and load it. Waiting longer cannot create a missing driver. Conversely, a valid driver can still need time for a slow device to appear.

The reference capture mounts ext4 from `mmcblk0` itself after the initial RAM-root flow. Substituting `mmcblk0p2` from a different tutorial would select a different layout. Compare identifiers with the generated image, not an assumed partition convention.

## Case 5: a device node exists but the device does not work

Registration proves that some driver initialization completed. It does not prove external signals, DMA, interrupts or application semantics. Follow the path from clocks/resets and pin routing through hardware transactions to completion and userspace consumption.

For an original DMA case, a completion timeout can mean the engine never started, the bus transaction failed, the interrupt was lost or the application waited on the wrong request. A readable identity register validates only the register-access path. Inspect progress and interrupt evidence separately.

If a driver probes only after another component appears, dependency deferral may be correct. If it never probes, inspect the missing provider and the first error rather than repeatedly loading the consumer module. Device-tree schema success cannot prove the described hardware exists.

## Case 6: corruption appears only under load

Memory corruption under load can come from out-of-bounds writes, early buffer reuse, stale cache data, DMA-address truncation or physical memory faults. Similar visible symptoms do not imply the same cause.

Track ownership transitions and sequence numbers. Verify that CPU and device accesses use the DMA API and supported synchronization. Compare CPU-only operation with DMA operation and single-client use with shared-buffer use. Change one boundary at a time.

If temperature or memory frequency changes the failure rate, collect hardware margin evidence. If queue depth or callback timing changes it, investigate lifetime and synchronization. Neither pattern is proof by itself, but each chooses a more useful next experiment.

## Case 7: updates work once, then recovery fails

Inspect the selected slot, pending/confirmed state, attempt counter and persistent-data version. A system can boot the new root image successfully yet make rollback impossible by migrating data too early. A watchdog reset can also repeat the same bad slot forever if boot policy does not consume attempts.

Preserve the first failure and metadata before trying another update. Rewriting the inactive slot or clearing the environment can remove the evidence needed to explain the state transition. Recovery actions should be documented separately from diagnosis.

## Write a result that another engineer can use

A useful report contains a reproducible trigger, exact artifacts, last successful boundary, observed failure, controlled comparison and remaining uncertainty. State which explanation the evidence supports and which alternatives remain.

> [!NOTE]
> **Not run on the reference setup:** new fault injection or physical recovery tests. This section combines inspected source/artifact behavior and existing QEMU evidence. The cases are diagnostic examples, not claims of reproduced board defects.

## References

- [Boot image anatomy](../07-boot-images-and-bootgen/03-boot-bin-anatomy.md), decoded fields and PMU handling.
- [QEMU limits and launch path](02-qemu-emulation.md), [DDR test scope](04-ddr-bring-up.md) and [update state machine](../23-storage-updates-and-production/04-software-update-strategies.md).
- Existing `reference-setup/captures/boot-prebuilt3.log` and pinned FSBL/Linux source cited in the linked sections.

---

<sub>← [DDR Bring-Up and Memory Testing](04-ddr-bring-up.md) · [Chapter index](README.md) · Next chapter: [25 · Security Fundamentals and Cryptography](../25-security-fundamentals-and-cryptography/README.md) →</sub>
