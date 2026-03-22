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
    env: dict[str, str | None] = {}
    if eager_import:
        env["EAGER_IMPORT"] = "1"
    if env is not None:
        env.update(env)
    success_codes: list[int] = [0]
    if suppress_no_test_exit_code:
        success_codes.append(5)
    s.run("pytest", *options, *s.posargs, env=env, success_codes=success_codes)
