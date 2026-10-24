"""Best-effort output scrubber for already-selected text values."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from redact.patterns import REDACTED, VALUE_PATTERNS


def scrub_text(text: str, *, secret_values: Iterable[str] = ()) -> str:
    result = text
    for value in sorted({v for v in secret_values if v}, key=len, reverse=True):
        result = result.replace(value, REDACTED)
    for pattern in VALUE_PATTERNS:
        result = pattern.sub(REDACTED, result)
    return result


def collect_secret_values(source: Mapping[str, str]) -> tuple[str, ...]:
    from redact.patterns import SECRET_NAME_RE

    return tuple(
        value
        for name, value in source.items()
        if SECRET_NAME_RE.search(name) and value
    )
