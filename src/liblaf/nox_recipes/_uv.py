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
