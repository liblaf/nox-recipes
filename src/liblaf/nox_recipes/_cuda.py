import pynvml


def supports_cuda(version: int | None = None) -> bool:
    try:
        pynvml.nvmlInit()
        cuda_version: int = pynvml.nvmlSystemGetCudaDriverVersion_v2()
        pynvml.nvmlShutdown()
    except pynvml.NVMLError:
        return False
    else:
        if version is None:
            return True
        return cuda_version >= version
