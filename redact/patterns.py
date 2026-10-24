"""Secret-name and value patterns used by M1 capture/redaction."""

from __future__ import annotations

import re
from typing import Final

SECRET_NAME_RE: Final[re.Pattern[str]] = re.compile(
    r"(?:^|_)(?:TOKEN|SECRET|PASSWORD|PASSWD|API_KEY|PRIVATE_KEY|ACCESS_KEY|AUTH|COOKIE)(?:$|_)",
    re.IGNORECASE,
)

VALUE_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9._~+/=-]+"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
)

REDACTED: Final[str] = "[REDACTED]"
