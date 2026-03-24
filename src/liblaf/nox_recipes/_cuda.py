import pynvml


def cuda_driver_version() -> int | None:
    try:
        pynvml.nvmlInit()
        version: int = pynvml.nvmlSystemGetCudaDriverVersion_v2()
        pynvml.nvmlShutdown()
    except pynvml.NVMLError:
        return None
    else:
        return version


def supports_cuda(version: int | None = None) -> bool:
    cuda_version: int | None = cuda_driver_version()
    if cuda_version is None:
        return False
    if version is None:
        return True
    return cuda_version >= version
