<div align="center" markdown>

![Nox Recipes](https://socialify.git.ci/liblaf/nox-recipes/image?description=1&forks=1&issues=1&language=1&name=1&owner=1&pattern=Transparent&pulls=1&stargazers=1&theme=Auto)

**[Explore the docs »](https://liblaf-nox-recipes.readthedocs.io/en/stable/)**

[![PyPI - Version](https://img.shields.io/pypi/v/liblaf-nox-recipes?logo=PyPI)](https://pypi.org/project/liblaf-nox-recipes/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/liblaf-nox-recipes?logo=Python)](https://pypi.org/project/liblaf-nox-recipes/)
[![Docs](https://github.com/liblaf/nox-recipes/actions/workflows/python-docs.yaml/badge.svg)](https://liblaf-nox-recipes.readthedocs.io/en/stable/)
[![Test](https://github.com/liblaf/nox-recipes/actions/workflows/python-test.yaml/badge.svg)](https://github.com/liblaf/nox-recipes/actions/workflows/python-test.yaml)
[![Codecov](https://codecov.io/gh/liblaf/nox-recipes/graph/badge.svg)](https://codecov.io/gh/liblaf/nox-recipes)
[![License](https://img.shields.io/github/license/liblaf/nox-recipes)](https://github.com/liblaf/nox-recipes/blob/main/LICENSE)

[Changelog](https://github.com/liblaf/nox-recipes/blob/main/CHANGELOG.md) · [Releases](https://github.com/liblaf/nox-recipes/releases) · [Report Bug](https://github.com/liblaf/nox-recipes/issues) · [Request Feature](https://github.com/liblaf/nox-recipes/issues)

![Rule](https://cdn.jsdelivr.net/gh/andreasbm/readme/assets/lines/rainbow.png)

</div>

`liblaf-nox-recipes` keeps `noxfile.py` sessions small by packaging the `uv`, `pytest`, and CUDA glue you would otherwise repeat across repositories.

## ✨ Features

- 💨 **Bootstrap `uv`-managed environments in one call:** `setup_uv()` compiles constraints from `pyproject.toml`, resolves the dependency groups you ask for, syncs the session environment, and installs the current project in editable mode.
- 📉 **Exercise multiple dependency strategies:** `Resolution` exposes `highest`, `lowest`, and `lowest-direct` modes so you can cover both everyday development and lower-bound compatibility in CI.
- 🧪 **Keep test sessions short without hiding `pytest`:** `pytest()` forwards `s.posargs`, supports per-session environment variables, and keeps shared flags out of each `@nox.session`.
- ⚡ **Run CodSpeed-friendly benchmarks:** `pytest_bench()` adds the benchmark marker, `--codspeed`, and single-process defaults when helpers like `pytest-xdist` are installed.
- 🖥️ **Skip GPU-only jobs safely:** `supports_cuda()` and `cuda_driver_version()` use NVML to decide whether CUDA-specific sessions should run.

## 📦 Installation

> [!NOTE]
> `liblaf-nox-recipes` requires Python 3.12+ and expects `uv` to be available anywhere your `nox` sessions run.

```bash
uv add --dev liblaf-nox-recipes
```

If you also want `uv` to create and manage the virtual environments that `nox` uses, install `nox-uv` and set `nox.options.default_venv_backend = "uv"` in your `noxfile.py`.

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
def test(s: nox.Session, resolution: Resolution) -> None:
    recipes.setup_uv(s, groups=["test"], resolution=resolution)
    recipes.pytest(s, suppress_no_test_exit_code=True)
```

Start with `setup_uv()` for the common case. When you need finer control, drop down to `uv_pip_compile()`, `uv_pip_sync()`, and `uv_pip_install()` directly. For GPU-only jobs, guard the session with `supports_cuda()` before doing any CUDA-dependent work.

## ⌨️ Local Development

```bash
git clone https://github.com/liblaf/nox-recipes.git
cd nox-recipes
mise run install
nox
mise run docs:serve
```

`nox` executes the test-tagged matrix from `noxfile.py`, and `mise run docs:serve` rebuilds the docs site that also embeds this README.

## 🤝 Contributing

Focused issues and pull requests are welcome. Please run `nox` before opening a PR, and rebuild the docs with `mise run docs:serve` when you change documentation or public APIs.

[![PR WELCOME](https://img.shields.io/badge/%F0%9F%A4%AF%20PR%20WELCOME-%E2%86%92-ffcb47?labelColor=black&style=for-the-badge)](https://github.com/liblaf/nox-recipes/pulls)

[![Contributors](https://gh-contributors-gamma.vercel.app/api?repo=liblaf/nox-recipes)](https://github.com/liblaf/nox-recipes/graphs/contributors)

---

#### 📝 License

Copyright © 2026 [liblaf](https://github.com/liblaf). <br />
This project is [MIT](https://github.com/liblaf/nox-recipes/blob/main/LICENSE) licensed.
