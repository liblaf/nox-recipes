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
    uv_pip_sync(
        s, extras=extras, all_extras=all_extras, resolution=resolution, quiet=quiet
    )
    # intentionally not following resolution for dependency groups, since they
    # are usually for development and we want to install the latest versions of
    # them
    uv_pip_install(s, groups=groups, quiet=quiet)
    uv_pip_install(s, editables=["."], no_deps=True, quiet=quiet)


def uv_pip_sync(
    s: nox.Session,
    *options: StrPath,
    extras: Iterable[str] = (),
    all_extras: bool = False,
    groups: Iterable[str] = (),
    resolution: Resolution | None = None,
    quiet: bool = True,
) -> None:
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir: Path = Path(tmpdir_str)
        lockfile: Path = tmpdir / "pylock.toml"

        args: list[StrPath] = ["uv", "pip", "compile"]
        for extra in extras:
            args.extend(["--extra", extra])
        if all_extras:
            args.append("--all-extras")
        for group in groups:
            args.extend(["--group", group])
        args.extend(("--output-file", lockfile))
        if resolution:
            args.extend(["--resolution", resolution])
        if isinstance(s.python, str):
            args.extend(["--python-version", s.python])
        if quiet:
            args.append("--quiet")
        args.extend(options)
        args.append("pyproject.toml")
        s.run_install(*args, external=True)

        args: list[StrPath] = ["uv", "pip", "sync"]
        if isinstance(s.python, str):
            args.extend(["--python-version", s.python])
        args.append("--strict")
        if quiet:
            args.append("--quiet")
        args.append(lockfile)
        s.run_install(*args, external=True)


def uv_pip_install(
    s: nox.Session,
    *options: StrPath,
    editables: Iterable[str] = (),
    extras: Iterable[str] = (),
    all_extras: bool = False,
    groups: Iterable[str] = (),
    no_deps: bool = False,
    resolution: Resolution | None = None,
    quiet: bool = True,
) -> None:
    args: list[StrPath] = ["uv", "pip", "install"]
    for extra in extras:
        args.extend(["--extra", extra])
    if all_extras:
        args.append("--all-extras")
    if no_deps:
        args.append("--no-deps")
    if resolution:
        args.extend(["--resolution", resolution])
    if quiet:
        args.append("--quiet")
    for editable in editables:
        args.extend(["--editable", editable])
    for group in groups:
        args.extend(["--group", group])
    args.extend(options)
    s.run_install(*args, external=True)
