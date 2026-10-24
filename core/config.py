"""M1 configuration loading with strict, small defaults."""

from __future__ import annotations

import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from core.errors import ConfigError


@dataclass(frozen=True, slots=True)
class Config:
    allow_home_workspace: bool = False
    allow_root_workspace: bool = False
    state_root: str | None = None
    runtime_root: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_config(path: Path | None = None) -> Config:
    if path is None or not path.exists():
        return Config()
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigError("configuration cannot be read", code="ERR_CONFIG_PARSE") from exc
    launch = data.get("launch", {})
    paths = data.get("paths", {})
    if not isinstance(launch, dict) or not isinstance(paths, dict):
        raise ConfigError("configuration sections must be tables", code="ERR_CONFIG_SCHEMA")
    for key in ("allow_home_workspace", "allow_root_workspace"):
        if key in launch and not isinstance(launch[key], bool):
            raise ConfigError(f"launch.{key} must be boolean", code="ERR_CONFIG_SCHEMA")
    for key in ("state_root", "runtime_root"):
        if key in paths and not isinstance(paths[key], str):
            raise ConfigError(f"paths.{key} must be string", code="ERR_CONFIG_SCHEMA")
    return Config(
        allow_home_workspace=launch.get("allow_home_workspace", False),
        allow_root_workspace=launch.get("allow_root_workspace", False),
        state_root=paths.get("state_root"),
        runtime_root=paths.get("runtime_root"),
    )
