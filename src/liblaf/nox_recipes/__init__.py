"""Composable helpers for building `nox` sessions.

`liblaf.nox_recipes` packages a small set of focused helpers for common
automation tasks:

- bootstrapping `uv`-managed environments,
- running `pytest` with project-friendly defaults, and
- guarding CUDA-only sessions on machines without NVIDIA drivers.

The package is designed to be imported into a `noxfile.py` and used from
regular `@nox.session` functions.
"""

import lazy_loader as lazy

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
del lazy
