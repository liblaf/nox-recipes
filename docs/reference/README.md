# API Reference

The public API is intentionally small and centered on a few building blocks:

- `setup_uv()` and the `uv_pip_*()` helpers for environment bootstrap.
- `pytest()` and `pytest_bench()` for test execution.
- `supports_cuda()` and `cuda_driver_version()` for GPU-aware session guards.

Use the pages in this section when you need exact signatures or parameter
behavior. The [user guide](../guide/README.md) is the better place to start if
you want examples first.

::: liblaf.nox_recipes
    options:
      members: false
