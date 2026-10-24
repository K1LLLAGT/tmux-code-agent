import os
import stat
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

from core.errors import PathSafetyError
from core.ids import new_session_id
from core.paths import (
    PRIVATE_DIR_MODE,
    assert_unix_path,
    build_session_paths,
    create_session_dirs,
    ensure_private_dir,
    validate_workspace,
)


def mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


@pytest.fixture
def short_prefix() -> Iterator[Path]:
    """Provide a short Termux-like prefix for socket-path tests."""

    temp_root = os.environ.get(
        "TMPDIR",
        "/tmp",
    )

    with tempfile.TemporaryDirectory(
        prefix="tca-p-",
        dir=temp_root,
    ) as directory:
        prefix = Path(directory) / "usr"
        prefix.mkdir()
        yield prefix


def test_build_session_paths_uses_full_state_id_and_short_runtime_id(
    tmp_path: Path,
    short_prefix: Path,
) -> None:
    session_id = "0123456789abcdef0123456789abcdef"

    paths = build_session_paths(
        session_id,
        home=tmp_path / "home",
        prefix=short_prefix,
    )

    assert paths.state_dir.name == session_id
    assert paths.runtime_dir.name == "tca-01234567"
    assert paths.tmux_socket.name == "tmux.sock"
    assert paths.control_socket.name == "ctl.sock"


def test_create_session_dirs_enforces_private_permissions(
    tmp_path: Path,
    short_prefix: Path,
) -> None:
    paths = build_session_paths(
        new_session_id(),
        home=tmp_path / "home",
        prefix=short_prefix,
    )

    create_session_dirs(paths)

    for path in (
        paths.state_root,
        paths.state_dir,
        paths.runtime_dir,
    ):
        assert path.is_dir()
        assert mode(path) == PRIVATE_DIR_MODE

    assert paths.runtime_root.is_dir()


def test_ensure_private_dir_repairs_permissions(
    tmp_path: Path,
) -> None:
    path = tmp_path / "private"
    path.mkdir(mode=0o755)
    os.chmod(path, 0o755)

    assert ensure_private_dir(path) == path
    assert mode(path) == PRIVATE_DIR_MODE


def test_ensure_private_dir_rejects_regular_file(
    tmp_path: Path,
) -> None:
    path = tmp_path / "not-a-dir"
    path.write_text("x")

    with pytest.raises(PathSafetyError):
        ensure_private_dir(path)


def test_assert_unix_path_checks_encoded_length(
    tmp_path: Path,
) -> None:
    short = tmp_path / "sock"
    encoded_length = len(os.fsencode(short))

    assert assert_unix_path(
        short,
        limit=encoded_length,
    ) == short

    with pytest.raises(PathSafetyError) as caught:
        assert_unix_path(
            short,
            limit=encoded_length - 1,
        )

    assert caught.value.code == "ERR_UNIX_PATH_TOO_LONG"


def test_validate_workspace_accepts_project_dir(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    workspace = home / "projects" / "x"
    workspace.mkdir(parents=True)

    assert validate_workspace(
        workspace,
        home=home,
    ) == workspace.resolve()


def test_validate_workspace_rejects_home_by_default(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    home.mkdir()

    with pytest.raises(PathSafetyError) as caught:
        validate_workspace(
            home,
            home=home,
        )

    assert caught.value.code == "ERR_WORKSPACE_HOME"

    assert validate_workspace(
        home,
        home=home,
        allow_home=True,
    ) == home.resolve()


def test_validate_workspace_rejects_root_by_default() -> None:
    with pytest.raises(PathSafetyError) as caught:
        validate_workspace(
            "/",
            home="/",
        )

    assert caught.value.code == "ERR_WORKSPACE_ROOT"

    assert validate_workspace(
        "/",
        home="/",
        allow_root=True,
        allow_home=True,
    ) == Path("/")


def test_validate_workspace_rejects_missing_path(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    home.mkdir()

    with pytest.raises(PathSafetyError) as caught:
        validate_workspace(
            tmp_path / "missing",
            home=home,
        )

    assert caught.value.code == "ERR_WORKSPACE_RESOLVE"
