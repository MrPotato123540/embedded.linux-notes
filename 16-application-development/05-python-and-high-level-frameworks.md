# Python and High-Level Frameworks

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Package high-level software deliberately

Python, Qt and OpenCV can run on embedded Linux, but their dependencies affect storage, memory and startup time. Select needed modules through recipes and package manifests rather than copying a development machine's whole environment.

A target-side `pip` install changes the deployed system outside the image build. If used for development, record it and convert the required packages into a reproducible release input. Native Python extensions need the target architecture and compatible libraries.

## Framework boundaries

Qt needs the selected display/windowing stack. OpenCV acceleration depends on the enabled backend and hardware support. Installing a package with a familiar name does not prove that it uses the GPU or PL.

PYNQ and Jupyter provide a higher-level development environment on supported platforms. Their board images, overlays and runtime versions form a coordinated stack; they are not automatic features of every PetaLinux image.

## References

- Inspected `meta-petalinux@rel-v2024.1` Python, Qt, OpenCV and Jupyter packagegroups
- Yocto 4.1.4 recipe and Python packaging documentation

---

<sub>← [System Services and Logging](04-system-services-and-logging.md) · [Chapter index](README.md) · [Containers on ZynqMP](06-containers.md) →</sub>
