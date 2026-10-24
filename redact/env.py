"""Environment allowlisting for immutable invocation context."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Final

from redact.patterns import SECRET_NAME_RE

SAFE_EXACT: Final[frozenset[str]] = frozenset(
    {
        "HOME",
        "PREFIX",
        "SHELL",
        "TERM",
        "LANG",
        "COLORTERM",
        "TMPDIR",
        "PATH",
        "VIRTUAL_ENV",
        "CONDA_PREFIX",
        "NODE_ENV",
        "NVM_BIN",
        "PYTHONPATH",
    }
)
SAFE_PREFIXES: Final[tuple[str, ...]] = ("LC_",)


def is_safe_name(name: str) -> bool:
    if SECRET_NAME_RE.search(name):
        return False
    return name in SAFE_EXACT or name.startswith(SAFE_PREFIXES)


def filter_environment(source: Mapping[str, str]) -> dict[str, str]:
    """Return deterministic allowlisted environment data only."""

    return {
        name: source[name]
        for name in sorted(source)
        if is_safe_name(name) and isinstance(source[name], str)
    }
