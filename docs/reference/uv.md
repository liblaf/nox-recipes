# uv Helpers

These helpers wrap the `uv pip` commands most often used in `nox` session
bootstrap. They are designed to compose cleanly: start with
`setup_uv()` for the common case, then drop to the lower-level helpers when you
need more control over how requirement files are compiled or installed.

::: liblaf.nox_recipes.Resolution

::: liblaf.nox_recipes.setup_uv

::: liblaf.nox_recipes.uv_pip_compile

::: liblaf.nox_recipes.uv_pip_sync

::: liblaf.nox_recipes.uv_pip_install
