# CUDA Helpers

These helpers use NVIDIA's NVML bindings to decide whether a GPU-specific
session should run. They are intentionally conservative: if the driver cannot be
queried, they report that CUDA is unavailable.

::: liblaf.nox_recipes.cuda_driver_version

::: liblaf.nox_recipes.supports_cuda
