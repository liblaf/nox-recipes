"""Wrappers around `pytest` for common `nox` session layouts."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, cast

import nox

if TYPE_CHECKING:
    from _typeshed import StrPath


def pytest(
    s: nox.Session,
    *,
    cov: bool = True,
    eager_import: bool = True,
    env: Mapping[str, str | None] | None = None,
    suppress_no_test_exit_code: bool = False,
) -> None:
    """Run `pytest` for the current session.

    Args:
        s:
            The active `nox` session.
        cov:
            Whether to pass `--cov` to `pytest`.
        eager_import:
            Whether to set `EAGER_IMPORT=1` for the test command.
        env:
            Extra environment variables merged into the `pytest` process.
        suppress_no_test_exit_code:
            Whether to treat `pytest` exit code `5` ("no tests collected") as a
            successful run.
    """
    options: list[StrPath] = []
    if cov:
        options.append("--cov")
    _pytest(
        s,
        *options,
        eager_import=eager_import,
        env=env,
        suppress_no_test_exit_code=suppress_no_test_exit_code,
    )


def pytest_bench(
    s: nox.Session,
    *,
    eager_import: bool = True,
    env: Mapping[str, str | None] | None = None,
    suppress_no_test_exit_code: bool = False,
) -> None:
    """Run the benchmark subset with CodSpeed-friendly defaults.

    This helper runs `pytest -m benchmark --codspeed`. If `pytest-xdist` is
    installed in the session environment, it also adds `--numprocesses=0` so
    benchmarks stay single-process and deterministic.

    Args:
        s:
            The active `nox` session.
        eager_import:
            Whether to set `EAGER_IMPORT=1` for the test command.
        env:
            Extra environment variables merged into the `pytest` process.
        suppress_no_test_exit_code:
            Whether to treat `pytest` exit code `5` ("no tests collected") as a
            successful run.
    """
    options: list[StrPath] = ["-m", "benchmark", "--codspeed"]
    plugins: dict[str, str] = pytest_plugin_versions(s)
    if "pytest-xdist" in plugins:
        options.append("--numprocesses=0")
    _pytest(
        s,
        *options,
        eager_import=eager_import,
        env=env,
        suppress_no_test_exit_code=suppress_no_test_exit_code,
    )


def pytest_plugin_versions(s: nox.Session) -> dict[str, str]:
    """Return installed `pytest` plugin versions for the session.

    The result is parsed from `pytest --version --version`, which reports each
    discovered plugin on its own line.

    Args:
        s:
            The active `nox` session.

    Returns:
        A mapping of plugin distribution names to their installed versions.
    """
    output: str = cast(
        "str", s.run_always("pytest", "--version", "--version", silent=True)
    )
    plugins: dict[str, str] = {}
    for line in output.splitlines():
        spec, at, _ = line.partition(" at ")
        if not at:
            continue
        plugin_name, _, plugin_version = spec.strip().rpartition("-")
        plugins[plugin_name] = plugin_version
    return plugins


def _pytest(
    s: nox.Session,
    *options: StrPath,
    eager_import: bool = True,
    env: Mapping[str, str | None] | None = None,
    suppress_no_test_exit_code: bool = False,
) -> None:
    """Run `pytest` with shared option and environment handling."""
    cmd_env: dict[str, str | None] = dict(env or {})
    if eager_import:
        cmd_env["EAGER_IMPORT"] = "1"
    success_codes: list[int] = [0]
    if suppress_no_test_exit_code:
        success_codes.append(5)
    s.run("pytest", *options, *s.posargs, env=cmd_env, success_codes=success_codes)
