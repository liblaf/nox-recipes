import liblaf.nox_recipes as recipes


def test_supports_cuda() -> None:
    assert isinstance(recipes.supports_cuda(), bool)
