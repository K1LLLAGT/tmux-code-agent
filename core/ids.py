"""Session identifiers for tmux-code-agent."""

from __future__ import annotations

import re
import secrets
from typing import Final

from core.errors import StateError

SESSION_ID_BYTES: Final[int] = 16
SESSION_ID_LENGTH: Final[int] = SESSION_ID_BYTES * 2
DISPLAY_ID_LENGTH: Final[int] = 8
_SESSION_ID_RE: Final[re.Pattern[str]] = re.compile(
    rf"^[0-9a-f]{{{SESSION_ID_LENGTH}}}$"
)


def new_session_id() -> str:
    """Return a lowercase 128-bit hexadecimal session identifier."""

    return secrets.token_hex(SESSION_ID_BYTES)


def is_session_id(value: object) -> bool:
    """Return whether *value* is a canonical session identifier."""

    return isinstance(value, str) and _SESSION_ID_RE.fullmatch(value) is not None


def validate_session_id(value: object) -> str:
    """Return a canonical ID or raise a stable TCA state error."""

    if not is_session_id(value):
        raise StateError(
            "session ID must be 32 lowercase hexadecimal characters",
            code="ERR_INVALID_SESSION_ID",
        )
    return value


def display_session_id(value: object) -> str:
    """Return the short UI/log label for a validated session ID."""

    return validate_session_id(value)[:DISPLAY_ID_LENGTH]
