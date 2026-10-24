"""Shared exception types for tmux-code-agent.

M1 establishes a small, dependency-free error vocabulary.  Exceptions carry a
stable machine-readable code, a human-readable message, and an optional exit
status suitable for the CLI layer.  Rendering and logging belong outside the
exception classes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

DEFAULT_EXIT_CODE: Final[int] = 1
CONFIG_EXIT_CODE: Final[int] = 2


@dataclass(frozen=True, slots=True)
class ErrorInfo:
    """Serializable, non-secret description of a TCA failure."""

    code: str
    message: str
    exit_code: int = DEFAULT_EXIT_CODE

    def __post_init__(self) -> None:
        if not self.code or not self.code.strip():
            raise ValueError("error code must not be empty")
        if not self.message or not self.message.strip():
            raise ValueError("error message must not be empty")
        if self.exit_code < 1 or self.exit_code > 255:
            raise ValueError("exit_code must be in range 1..255")

    def as_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "message": self.message,
            "exit_code": self.exit_code,
        }


class TCAError(Exception):
    """Base class for expected, user-presentable TCA failures."""

    default_code: Final[str] = "ERR_TCA"
    default_exit_code: Final[int] = DEFAULT_EXIT_CODE

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        exit_code: int | None = None,
    ) -> None:
        selected_code = code or self.default_code
        selected_exit = (
            self.default_exit_code if exit_code is None else exit_code
        )
        self.info = ErrorInfo(selected_code, message, selected_exit)
        super().__init__(message)

    @property
    def code(self) -> str:
        return self.info.code

    @property
    def exit_code(self) -> int:
        return self.info.exit_code

    def as_dict(self) -> dict[str, object]:
        return self.info.as_dict()


class UsageError(TCAError):
    """Invalid CLI invocation or launch request."""

    default_code: Final[str] = "ERR_USAGE"
    default_exit_code: Final[int] = CONFIG_EXIT_CODE


class ConfigError(TCAError):
    """Invalid or unreadable TCA configuration."""

    default_code: Final[str] = "ERR_CONFIG"
    default_exit_code: Final[int] = CONFIG_EXIT_CODE


class ContextError(TCAError):
    """Invocation-context capture failed or was unsafe."""

    default_code: Final[str] = "ERR_CONTEXT"


class PathSafetyError(TCAError):
    """A path violates a TCA safety or isolation invariant."""

    default_code: Final[str] = "ERR_PATH_SAFETY"


class StateError(TCAError):
    """Session state is invalid, corrupt, or inconsistent."""

    default_code: Final[str] = "ERR_STATE"
