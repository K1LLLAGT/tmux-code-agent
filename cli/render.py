"""CLI rendering kept separate from capture and persistence."""

from __future__ import annotations

import json
from typing import Any


def render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def render_dry_run(payload: dict[str, Any]) -> str:
    return "\n".join(
        (
            "TMUX CODE AGENT - DRY RUN",
            f"Session:   {payload['session_id'][:8]}",
            f"Workspace: {payload['manifest']['workspace']}",
            f"State:     {payload['paths']['state_dir']}",
            f"Runtime:   {payload['paths']['runtime_dir']}",
            "Status:    CREATED",
        )
    )
