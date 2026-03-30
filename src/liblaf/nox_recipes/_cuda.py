"""Helpers for detecting CUDA availability inside `nox` sessions."""

import pynvml


def cuda_driver_version() -> int | None:
    """Return the CUDA driver version reported by NVIDIA's NVML library.

    Returns:
        The integer version returned by
        `pynvml.nvmlSystemGetCudaDriverVersion_v2()`, or `None` when NVML
        cannot be initialized or no supported NVIDIA driver is available.
    """
    initialized = False
    try:
        pynvml.nvmlInit()
        initialized = True
        version: int = pynvml.nvmlSystemGetCudaDriverVersion_v2()
    except pynvml.NVMLError:
        return None
    finally:
        if initialized:
            pynvml.nvmlShutdown()
    return version


def supports_cuda(version: int | None = None) -> bool:
    """Return whether the current machine satisfies a CUDA requirement.

    Args:
        version:
            Optional minimum CUDA driver version. When omitted, the function
            only checks whether any CUDA driver is available.

    Returns:
        `True` if a CUDA driver is present and meets the requested minimum
        version, otherwise `False`.
    """
    cuda_version: int | None = cuda_driver_version()
    if cuda_version is None:
        return False
    if version is None:
        return True
    return cuda_version >= version
