# User Guide

`liblaf.nox_recipes` is a small collection of helpers for writing tidy,
repeatable `nox` sessions. The package stays close to the tools it wraps:
`uv` still resolves and installs dependencies, `pytest` still runs your test
suite, and `pynvml` still decides whether CUDA is available. The helpers exist
to keep that wiring in one place instead of repeating it across every project.

This design is close to the style used by `attrs`: lead with regular Python,
keep the surface area small, and let the documentation explain how the pieces
fit together.

## Start With `setup_uv()`

For most projects, `setup_uv()` is the only environment bootstrap helper you
need. See the [uv helper reference](../reference/uv.md) for the full API. It
does four things:

1. Compiles a constraints file from `pyproject.toml`.
2. Compiles the requested dependency groups against those constraints.
3. Syncs the session environment from the compiled requirements file.
4. Installs the current project in editable mode.

```python
from typing import Any

import nox

from liblaf import nox_recipes as recipes
from liblaf.nox_recipes import Resolution

PYPROJECT: dict[str, Any] = nox.project.load_toml("pyproject.toml")
PYTHON_VERSIONS: list[str] = nox.project.python_versions(PYPROJECT)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
@nox.parametrize(
    "resolution",
    [
        nox.param(Resolution.HIGHEST, id="highest"),
        nox.param(Resolution.LOWEST_DIRECT, id="lowest-direct"),
    ],
)
def test(s: nox.Session, resolution: Resolution) -> None:
    recipes.setup_uv(s, groups=["test"], resolution=resolution)
    recipes.pytest(s, suppress_no_test_exit_code=True)
```

If you need more control, drop down to the lower-level helpers:
`uv_pip_compile()`, `uv_pip_sync()`, and `uv_pip_install()`.

## Resolution Strategies

`Resolution` exposes the resolution modes supported by `uv`. The
[uv helper reference](../reference/uv.md) documents each option in detail:

| Value | Meaning |
| --- | --- |
| `Resolution.HIGHEST` | Prefer the newest compatible versions. |
| `Resolution.LOWEST` | Prefer the oldest compatible versions across the graph. |
| `Resolution.LOWEST_DIRECT` | Prefer the oldest direct requirements while keeping transitive resolution practical. |

`highest` is a good default for everyday development. The lower-bound strategies
are useful when you want CI coverage across older supported dependency ranges.

## Running Tests

Use `pytest()` for normal test runs and `pytest_bench()` for benchmark
sessions. The [pytest helper reference](../reference/pytest.md) covers the
individual parameters.

```python
@nox.session(reuse_venv=True)
def test(s: nox.Session) -> None:
    recipes.setup_uv(s, groups=["test"])
    recipes.pytest(s, suppress_no_test_exit_code=True)


@nox.session(reuse_venv=True)
def bench(s: nox.Session) -> None:
    recipes.setup_uv(s, groups=["test"])
    recipes.pytest_bench(s)
```

Both helpers forward `s.posargs` so `nox -s test -- -k smoke` still behaves as
you expect. They also accept an `env` mapping for per-session environment
variables.

## Optional CUDA Sessions

GPU-only sessions should be easy to skip on laptops and required on GPU
runners. `supports_cuda()` is the small guard for that. The
[CUDA helper reference](../reference/cuda.md) covers the underlying detection
helpers.

```python
@nox.session(tags=["gpu"])
def smoke_cuda(s: nox.Session) -> None:
    if not recipes.supports_cuda():
        s.skip("CUDA driver not available")

    recipes.setup_uv(s, groups=["test"])
    s.run("python", "-c", "print('CUDA is available')")
```

If you need to compare against a minimum driver requirement, pass the version
integer returned by `cuda_driver_version()`.

## Which Helper Should I Reach For?

- Start with `setup_uv()` unless you know you need finer-grained control.
- Use `pytest()` for regular test sessions.
- Use `pytest_bench()` for CodSpeed-style benchmark runs.
- Use `pytest_plugin_versions()` when session behavior depends on which pytest plugins are installed.
- Use `supports_cuda()` to gate optional GPU jobs.
