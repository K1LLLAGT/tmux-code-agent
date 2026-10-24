import pytest

from core.errors import (
    CONFIG_EXIT_CODE,
    ConfigError,
    ContextError,
    ErrorInfo,
    PathSafetyError,
    StateError,
    TCAError,
    UsageError,
)


def test_error_info_serializes_stable_fields() -> None:
    info = ErrorInfo("ERR_EXAMPLE", "example failure", 7)
    assert info.as_dict() == {
        "code": "ERR_EXAMPLE",
        "message": "example failure",
        "exit_code": 7,
    }


@pytest.mark.parametrize(
    ("code", "message", "exit_code"),
    [
        ("", "message", 1),
        ("   ", "message", 1),
        ("ERR_X", "", 1),
        ("ERR_X", "   ", 1),
        ("ERR_X", "message", 0),
        ("ERR_X", "message", 256),
    ],
)
def test_error_info_rejects_invalid_values(
    code: str,
    message: str,
    exit_code: int,
) -> None:
    with pytest.raises(ValueError):
        ErrorInfo(code, message, exit_code)


def test_tca_error_is_exception_and_machine_readable() -> None:
    error = TCAError("boom")
    assert isinstance(error, Exception)
    assert str(error) == "boom"
    assert error.code == "ERR_TCA"
    assert error.exit_code == 1
    assert error.as_dict()["message"] == "boom"


def test_tca_error_allows_explicit_code_and_exit_status() -> None:
    error = TCAError("boom", code="ERR_BOOM", exit_code=17)
    assert error.as_dict() == {
        "code": "ERR_BOOM",
        "message": "boom",
        "exit_code": 17,
    }


@pytest.mark.parametrize(
    ("error_type", "expected_code", "expected_exit"),
    [
        (UsageError, "ERR_USAGE", CONFIG_EXIT_CODE),
        (ConfigError, "ERR_CONFIG", CONFIG_EXIT_CODE),
        (ContextError, "ERR_CONTEXT", 1),
        (PathSafetyError, "ERR_PATH_SAFETY", 1),
        (StateError, "ERR_STATE", 1),
    ],
)
def test_specialized_errors_have_stable_defaults(
    error_type: type[TCAError],
    expected_code: str,
    expected_exit: int,
) -> None:
    error = error_type("failure")
    assert error.code == expected_code
    assert error.exit_code == expected_exit
