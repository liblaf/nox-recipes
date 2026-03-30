"""Helpers for bootstrapping `uv`-managed environments in `nox`."""

from __future__ import annotations

import enum
import tempfile
from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

import nox

if TYPE_CHECKING:
    from _typeshed import StrPath


class Resolution(enum.StrEnum):
    """Dependency resolution strategies supported by `uv pip`.

    Attributes:
        HIGHEST:
            Prefer the newest compatible versions.
        LOWEST:
            Prefer the oldest compatible versions across the graph.
        LOWEST_DIRECT:
            Prefer the oldest compatible versions for direct dependencies while
            still allowing newer transitive requirements when needed.
    """

    HIGHEST = "highest"
    LOWEST = "lowest"
    LOWEST_DIRECT = "lowest-direct"


def setup_uv(
    s: nox.Session,
    *,
    extras: Iterable[str] = (),
    all_extras: bool = False,
    groups: Iterable[str] = (),
    resolution: Resolution | None = None,
    quiet: bool = True,
) -> None:
    """Create and sync a session environment from `pyproject.toml`.

    `setup_uv()` is the high-level helper for most projects. It compiles a
    constraints file, compiles the requested requirements against those
    constraints, syncs the session environment, and finally installs the current
    project in editable mode.

    Args:
        s:
            The active `nox` session.
        extras:
            Project extras to include while compiling and installing.
        all_extras:
            Whether to include every defined extra.
        groups:
            Dependency groups to include when compiling the session
            requirements.
        resolution:
            Optional dependency resolution strategy for the initial constraints
            compile.
        quiet:
            Whether to ask `uv` for quieter output.
    """
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir: Path = Path(tmpdir_str)
        constraints: Path = tmpdir / "constraints.txt"
        requirements: Path = tmpdir / "requirements.txt"
        uv_pip_compile(
            s,
            extras=extras,
            all_extras=all_extras,
            output_file=constraints,
            resolution=resolution,
            quiet=quiet,
        )
        uv_pip_compile(
            s,
            constraints=[constraints],
            extras=extras,
            all_extras=all_extras,
            groups=groups,
            output_file=requirements,
            quiet=quiet,
        )
        uv_pip_sync(s, requirements, quiet=quiet)
    uv_pip_install(s, editables=["."], no_deps=True, quiet=quiet)


def uv_pip_compile(
    s: nox.Session,
    *options: StrPath,
    constraints: Iterable[StrPath] = (),
    extras: Iterable[str] = (),
    all_extras: bool = False,
    groups: Iterable[str] = (),
    output_file: StrPath | None = None,
    resolution: Resolution | None = None,
    quiet: bool = True,
) -> None:
    """Run `uv pip compile` against the current project's `pyproject.toml`.

    Args:
        s:
            The active `nox` session.
        *options:
            Additional command-line options appended before `pyproject.toml`.
        constraints:
            Compiled requirement files passed with `--constraints`.
        extras:
            Project extras enabled during compilation.
        all_extras:
            Whether to enable every defined extra.
        groups:
            Dependency groups enabled during compilation.
        output_file:
            Optional destination file passed with `--output-file`.
        resolution:
            Optional dependency resolution strategy for `uv`.
        quiet:
            Whether to ask `uv` for quieter output.
    """
    args: list[StrPath] = ["uv", "pip", "compile"]
    for constraint in constraints:
        args.extend(("--constraints", constraint))
    for extra in extras:
        args.extend(("--extra", extra))
    if all_extras:
        args.append("--all-extras")
    for group in groups:
        args.extend(("--group", group))
    if output_file:
        args.extend(("--output-file", output_file))
    args.extend(("--generate-hashes", "--emit-index-url", "--emit-index-annotation"))
    if resolution:
        args.extend(("--resolution", resolution))
    if isinstance(s.python, str):
        args.extend(("--python-version", s.python))
    if quiet:
        args.append("--quiet")
    args.extend(options)
    args.append("pyproject.toml")
    s.run_install(*args, external=True)


def uv_pip_sync(s: nox.Session, *src_files: StrPath, quiet: bool = True) -> None:
    """Run `uv pip sync` for one or more compiled requirement files.

    Args:
        s:
            The active `nox` session.
        *src_files:
            Requirement files consumed by `uv pip sync`.
        quiet:
            Whether to ask `uv` for quieter output.
    """
    args: list[StrPath] = ["uv", "pip", "sync"]
    if isinstance(s.python, str):
        args.extend(("--python-version", s.python))
    args.append("--strict")
    if quiet:
        args.append("--quiet")
    args.extend(src_files)
    s.run_install(*args, external=True)


def uv_pip_install(
    s: nox.Session,
    *options: StrPath,
    constraints: Iterable[StrPath] = (),
    editables: Iterable[str] = (),
    extras: Iterable[str] = (),
    all_extras: bool = False,
    groups: Iterable[str] = (),
    no_deps: bool = False,
    resolution: Resolution | None = None,
    quiet: bool = True,
) -> None:
    """Run `uv pip install` with session-oriented defaults.

    Args:
        s:
            The active `nox` session.
        *options:
            Additional command-line options forwarded to `uv pip install`.
        constraints:
            Compiled requirement files passed with `--constraints`.
        editables:
            Editable paths installed with `--editable`.
        extras:
            Project extras enabled during installation.
        all_extras:
            Whether to enable every defined extra.
        groups:
            Dependency groups enabled during installation.
        no_deps:
            Whether to pass `--no-deps`.
        resolution:
            Optional dependency resolution strategy for `uv`.
        quiet:
            Whether to ask `uv` for quieter output.
    """
    args: list[StrPath] = ["uv", "pip", "install"]
    for constraint in constraints:
        args.extend(("--constraints", constraint))
    for extra in extras:
        args.extend(("--extra", extra))
    if all_extras:
        args.append("--all-extras")
    if no_deps:
        args.append("--no-deps")
    if resolution:
        args.extend(("--resolution", resolution))
    if quiet:
        args.append("--quiet")
    for editable in editables:
        args.extend(("--editable", editable))
    for group in groups:
        args.extend(("--group", group))
    args.extend(options)
    s.run_install(*args, external=True)
