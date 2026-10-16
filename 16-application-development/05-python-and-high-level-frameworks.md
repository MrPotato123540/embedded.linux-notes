# Python and High-Level Frameworks

> **Applies to:** PetaLinux 2024.1 · Zynq UltraScale+ MPSoC

**[16 · Application Development](README.md)** · Part VII: Root Filesystem and User Space

## Package high-level software deliberately

Python, Qt and OpenCV can run on embedded Linux, but their dependencies affect storage, memory and startup time. Select needed modules through recipes and package manifests rather than copying a development machine's whole environment.

A target-side `pip` install changes the deployed system outside the image build. If used for development, record it and convert the required packages into a reproducible release input. Native Python extensions need the target architecture and compatible libraries.

## Framework boundaries

Qt needs the selected display/windowing stack. OpenCV acceleration depends on the enabled backend and hardware support. Installing a package with a familiar name does not prove that it uses the GPU or PL.

PYNQ and Jupyter provide a higher-level development environment on supported platforms. Their board images, overlays and runtime versions form a coordinated stack; they are not automatic features of every PetaLinux image.

## Separate Python code from native dependencies

A pure Python module mainly depends on the interpreter and other Python packages. A native extension also depends on the target machine ABI, Python extension ABI, C/C++ runtime and linked libraries. A package that imports correctly on the host can therefore fail on the board before its Python code runs.

Wheel tags encode compatibility information, but selecting a wheel still requires the correct target environment. A host-built extension cannot be made into an AArch64 extension by copying it into the target's site-packages directory. The extension must be built with a suitable cross-build process or provided as a compatible target artifact.

The supplied Poky layer includes `python3_3.10.6.bb` and build classes for setuptools and PEP517 workflows. This identifies available release integration, not a guarantee that every optional Python package is installed in the supplied rootfs.

## Follow an import through its dependencies

Suppose an application imports a Python package that wraps a numerical C library. The interpreter first resolves the Python module path. Loading the extension then invokes the dynamic linker for its shared-object dependencies. Initialization can finally fail because of an incompatible Python API or library behavior.

A `ModuleNotFoundError` points first to package installation and module search paths. An “undefined symbol” or shared-library error points to the native load stage. A crash during import can come from native initialization. Treating every import failure as a reason to reinstall the top-level Python package loses these distinctions.

A virtual environment changes Python package isolation and interpreter paths. It does not provide a different kernel or automatically replace every native system library. Its directory can also contain absolute paths that make careless relocation fail.

## Use the image build for deployed dependencies

Recipes make source versions, build dependencies and package contents reviewable. The release's Python build classes manage host tools and target installation conventions. A recipe for a native extension must separate build-time generators from target code and declare the needed target libraries.

Installing packages interactively on a writable development board is useful for exploration. It does not update the immutable image recipe or guarantee that a later board receives the same dependency versions. Convert the tested dependency set into controlled build inputs before release.

Avoid network resolution during normal service startup. A package index outage should not prevent a device from booting a previously validated application. Keep the application and its dependencies available as part of a known release artifact.

## Performance depends on where work runs

Python-level loops, native numerical kernels and device-backed operations have different costs. Moving work into a vectorized library can reduce interpreter overhead while increasing temporary-buffer use. Passing data to an accelerator can reduce compute time while adding conversion, synchronization and transfer costs.

Measure the whole request. A fast inference call does not include image decoding, resizing, color conversion and output interpretation unless the measurement explicitly covers them. An application can spend most of its time preparing data for a fast native backend.

For CPython versions in this release family, the Global Interpreter Lock affects execution of ordinary Python bytecode in threads. Native libraries may release it while doing work, and processes have a different memory/communication cost. Do not select threads or processes from a generic “Python is slow” assumption; measure the actual path and library behavior.

## Array ownership crosses language boundaries

A numerical array has a data pointer, shape, element type and strides. A slice can be a view over another allocation rather than an independent contiguous copy. A native library or hardware interface that expects contiguous data cannot infer that requirement from the logical shape alone.

When passing a buffer to asynchronous work, keep the owning Python object alive until completion. A temporary array can otherwise be released while native code retains its pointer. A read-only Python view also does not necessarily stop another owner from modifying the same underlying storage.

For DMA buffers, Python's memory safety does not replace the kernel/runtime ownership protocol. The application must still synchronize CPU/device access and avoid reusing a buffer while the device owns it. A Python wrapper that hides every buffer transition makes this harder to review.

## Framework size and startup are product costs

Large frameworks can bring many shared libraries, models and plugins. Their installed size, peak RAM and first-use latency may dominate a small embedded system. Keep only the required components where the framework supports that split, and preserve the matching plugin/model versions.

A service should validate critical imports and model files before reporting readiness. Report the selected backend and version so silent fallback to a CPU implementation does not become a misleading acceleration claim.

> [!NOTE]
> **Not run on the reference setup:** installing new Python frameworks or measuring their target performance. The build classes and release recipe were inspected; package compatibility still needs target tests.

## References

- Inspected BSP `poky/meta/recipes-devtools/python/python3_3.10.6.bb`, `classes-recipe/setuptools3.bbclass` and `python_pep517.bbclass`.
- [Python 3.10 C API initialization/thread state](https://docs.python.org/3.10/c-api/init.html), interpreter lock and native extension execution.

- Inspected `meta-petalinux@rel-v2024.1` Python, Qt, OpenCV and Jupyter packagegroups
- Yocto 4.1.4 recipe and Python packaging documentation

---

<sub>← [System Services and Logging](04-system-services-and-logging.md) · [Chapter index](README.md) · [Containers on ZynqMP](06-containers.md) →</sub>
