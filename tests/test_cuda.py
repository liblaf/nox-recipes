import liblaf.nox_recipes as recipes


def test_cuda_driver_version() -> None:
    version: int | None = recipes.cuda_driver_version()
    assert version is None or isinstance(version, int)


def test_supports_cuda() -> None:
    assert isinstance(recipes.supports_cuda(), bool)
