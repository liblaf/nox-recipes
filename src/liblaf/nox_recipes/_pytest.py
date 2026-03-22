from __future__ import annotations

from typing import TYPE_CHECKING, cast

import nox

if TYPE_CHECKING:
    from _typeshed import StrPath


def pytest(
    s: nox.Session, *, cov: bool = True, suppress_no_test_exit_code: bool = False
) -> None:
    args: list[StrPath] = ["pytest"]
    if cov:
        args.extend(["--cov", "--cov-branch"])
    success_codes: list[int] = [0]
    if suppress_no_test_exit_code:
        success_codes.append(5)
    s.run(*args, *s.posargs, success_codes=success_codes)


def pytest_bench(s: nox.Session, *, suppress_no_test_exit_code: bool = False) -> None:
    args: list[StrPath] = ["pytest", "-m", "benchmark"]
    plugins: dict[str, str] = pytest_plugin_versions(s)
    print(plugins)
    if "pytest-xdist" in plugins:
        args.append("--numprocesses=0")
    success_codes: list[int] = [0]
    if suppress_no_test_exit_code:
        success_codes.append(5)
    s.run(*args, *s.posargs, success_codes=success_codes)


def pytest_plugin_versions(s: nox.Session) -> dict[str, str]:
    output: str = cast(
        "str",
        s.run_always(
            "pytest",
            "--version",
            "--version",
            silent=True,
            # stdout=subprocess.PIPE,
            stderr=None,
        ),
    )
    plugins: dict[str, str] = {}
    for line in output.splitlines():
        spec, at, _ = line.partition(" at ")
        if not at:
            continue
        plugin_name, _, plugin_version = spec.strip().rpartition("-")
        plugins[plugin_name] = plugin_version
    return plugins
