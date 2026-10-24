import re

import pytest

from core.errors import StateError
from core.ids import (
    DISPLAY_ID_LENGTH,
    SESSION_ID_LENGTH,
    display_session_id,
    is_session_id,
    new_session_id,
    validate_session_id,
)


def test_new_session_id_is_canonical_and_random() -> None:
    values = {new_session_id() for _ in range(100)}
    assert len(values) == 100
    assert all(len(value) == SESSION_ID_LENGTH for value in values)
    assert all(re.fullmatch(r"[0-9a-f]{32}", value) for value in values)


@pytest.mark.parametrize(
    "value",
    [None, 12, "", "a" * 31, "a" * 33, "A" * 32, "g" * 32, "../" + "a" * 29],
)
def test_invalid_session_ids_are_rejected(value: object) -> None:
    assert not is_session_id(value)
    with pytest.raises(StateError) as caught:
        validate_session_id(value)
    assert caught.value.code == "ERR_INVALID_SESSION_ID"


def test_validate_and_display_session_id() -> None:
    value = "0123456789abcdef0123456789abcdef"
    assert validate_session_id(value) == value
    assert display_session_id(value) == value[:DISPLAY_ID_LENGTH]
