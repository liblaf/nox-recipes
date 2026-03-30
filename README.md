<div align="center" markdown>

![nox-recipes](https://socialify.git.ci/liblaf/nox-recipes/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Transparent&pulls=1&stargazers=1&theme=Auto)

**[Explore the docs »](https://liblaf.github.io/nox-recipes/)**

[![PyPI - Version](https://img.shields.io/pypi/v/liblaf-nox-recipes?logo=PyPI)](https://pypi.org/project/liblaf-nox-recipes/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/liblaf-nox-recipes?logo=python)](https://pypi.org/project/liblaf-nox-recipes/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/liblaf-nox-recipes?logo=PyPI)](https://pypi.org/project/liblaf-nox-recipes/)
[![Python / Docs](https://github.com/liblaf/nox-recipes/actions/workflows/python-docs.yaml/badge.svg)](https://github.com/liblaf/nox-recipes/actions/workflows/python-docs.yaml)
[![Python / Test](https://github.com/liblaf/nox-recipes/actions/workflows/python-test.yaml/badge.svg)](https://github.com/liblaf/nox-recipes/actions/workflows/python-test.yaml)
[![Python / Bench](https://github.com/liblaf/nox-recipes/actions/workflows/python-bench.yaml/badge.svg)](https://github.com/liblaf/nox-recipes/actions/workflows/python-bench.yaml)
[![MegaLinter](https://github.com/liblaf/nox-recipes/actions/workflows/shared-mega-linter.yaml/badge.svg)](https://github.com/liblaf/nox-recipes/actions/workflows/shared-mega-linter.yaml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

[Documentation](https://liblaf.github.io/nox-recipes/) · [API Reference](https://liblaf.github.io/nox-recipes/reference/) · [Changelog](https://github.com/liblaf/nox-recipes/blob/main/CHANGELOG.md) · [Report Bug](https://github.com/liblaf/nox-recipes/issues) · [Request Feature](https://github.com/liblaf/nox-recipes/issues)

![Rule](https://cdn.jsdelivr.net/gh/andreasbm/readme/assets/lines/rainbow.png)

</div>

## ✨ Features

- **`uv`-first session bootstrap**: compile constraints, sync environments, and install your project in editable mode with a couple of lines in `noxfile.py`.
- **Thin `pytest` wrappers**: run regular test sessions with coverage or benchmark sessions with CodSpeed-friendly defaults.
- **Dependency resolution coverage**: exercise `highest`, `lowest`, or `lowest-direct` dependency sets without duplicating session logic.
- **CUDA-aware skips**: keep GPU-only jobs polite on machines without an NVIDIA driver.

## 📦 Installation

> [!NOTE]
> Install `liblaf-nox-recipes`, then import it as `liblaf.nox_recipes`.

`nox-recipes` supports Python 3.12, 3.13, and 3.14.

```bash
uv add --dev liblaf-nox-recipes
```

If you use `setup_uv()`, make sure the `uv` CLI is available anywhere `nox` runs.

## 🚀 Quick Start

```python
from typing import Any

import nox

from liblaf import nox_recipes as recipes
from liblaf.nox_recipes import Resolution

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True

PYPROJECT: dict[str, Any] = nox.project.load_toml("pyproject.toml")
PYTHON_VERSIONS: list[str] = nox.project.python_versions(PYPROJECT)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True, tags=["test"])
@nox.parametrize(
    "resolution",
    [
        nox.param(Resolution.HIGHEST, id="highest"),
        nox.param(Resolution.LOWEST_DIRECT, id="lowest-direct"),
    ],
)
def test(s: nox.Session, resolution: Resolution | None) -> None:
    recipes.setup_uv(s, groups=["test"], resolution=resolution)
    recipes.pytest(s, suppress_no_test_exit_code=True)
```

This gives each session a reproducible `uv`-managed environment, installs your project in editable mode, and runs `pytest` with sensible defaults. `Resolution` lets you probe different parts of your dependency graph without copying setup code into multiple sessions.

## 🧰 Included Recipes

| Helper | Purpose |
| --- | --- |
| `setup_uv()` | Compile constraints, compile requirements, sync the session environment, and install `.` in editable mode. |
| `uv_pip_compile()` | Wrap `uv pip compile` for extras, groups, constraints, and resolution strategies. |
| `uv_pip_sync()` | Sync an environment from one or more compiled requirement files with `--strict`. |
| `uv_pip_install()` | Install editables, extras, groups, or constrained dependencies with `uv pip install`. |
| `pytest()` | Run `pytest` with optional coverage and optional suppression for the "no tests collected" exit code. |
| `pytest_bench()` | Run `pytest -m benchmark --codspeed`, adjusting for `pytest-xdist` when present. |
| `pytest_plugin_versions()` | Inspect installed `pytest` plugin versions inside a session. |
| `supports_cuda()` / `cuda_driver_version()` | Detect whether CUDA-backed sessions should run. |

## 🖥️ GPU-Only Sessions

```python
@nox.session(tags=["gpu"])
def smoke_cuda(s: nox.Session) -> None:
    if not recipes.supports_cuda():
        s.skip("CUDA driver not available")

    recipes.setup_uv(s, groups=["test"])
    s.run("python", "-c", "print('CUDA is available')")
```

This is useful when the same repository needs CPU-safe local runs and optional GPU jobs on dedicated runners.

## ⌨️ Local Development

```bash
git clone https://github.com/liblaf/nox-recipes.git
cd nox-recipes
uv sync --all-packages
nox
```

The documentation site includes this root README, so improving examples here also improves the published docs.

## 🤝 Contributing

Issues and pull requests are welcome. The most helpful contributions are usually small, focused improvements to the recipe surface area, docs, or real-world `noxfile.py` examples.

## 📄 License

Copyright © 2026 [liblaf](https://github.com/liblaf).

This project is [MIT](https://github.com/liblaf/nox-recipes/blob/main/LICENSE) licensed.
