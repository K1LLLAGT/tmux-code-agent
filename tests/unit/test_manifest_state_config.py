import json
import os
import stat
import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

from core.config import Config, load_config
from core.context import GitFacts, InvocationContext
from core.errors import ConfigError, StateError
from core.ids import new_session_id
from core.manifest import build_manifest, write_manifest
from core.paths import build_session_paths, create_session_dirs
from core.state import initial_state, write_state_atomic


@pytest.fixture
def short_prefix() -> Iterator[Path]:
    """Provide a short Termux-like prefix for socket-path tests."""

    temp_root = os.environ.get(
        "TMPDIR",
        "/tmp",
    )

    with tempfile.TemporaryDirectory(
        prefix="m1-p-",
        dir=temp_root,
    ) as directory:
        prefix = Path(directory) / "usr"
        prefix.mkdir()
        yield prefix


def fake_context(
    home: Path,
    prefix: Path,
    workspace: Path,
) -> InvocationContext:
    return InvocationContext(
        logical_pwd=str(workspace),
        physical_pwd=str(workspace),
        workspace=str(workspace),
        home=str(home),
        prefix=str(prefix),
        shell="/bin/sh",
        term="xterm",
        locale={},
        environment={
            "HOME": str(home),
            "PREFIX": str(prefix),
        },
        python_executable="python",
        python_version="3",
        virtual_env=None,
        node_env=None,
        git=GitFacts(is_repo=False),
    )


def test_manifest_is_exclusive_and_mode_0400(
    tmp_path: Path,
    short_prefix: Path,
) -> None:
    home = tmp_path / "h"
    workspace = home / "w"

    workspace.mkdir(parents=True)

    paths = build_session_paths(
        new_session_id(),
        home=home,
        prefix=short_prefix,
    )

    create_session_dirs(paths)

    manifest = build_manifest(
        fake_context(
            home,
            short_prefix,
            workspace,
        ),
        paths,
    )

    write_manifest(
        paths.manifest,
        manifest,
    )

    assert (
        stat.S_IMODE(paths.manifest.stat().st_mode)
        == 0o400
    )

    with pytest.raises(StateError) as caught:
        write_manifest(
            paths.manifest,
            manifest,
        )

    assert caught.value.code == "ERR_MANIFEST_EXISTS"


def test_state_write_is_atomic_shape_and_mode(
    tmp_path: Path,
) -> None:
    path = tmp_path / "state.json"
    state = initial_state("a" * 32)

    write_state_atomic(
        path,
        state,
    )

    assert json.loads(
        path.read_text()
    )["status"] == "CREATED"

    assert (
        stat.S_IMODE(path.stat().st_mode)
        == 0o600
    )

    assert not list(
        tmp_path.glob(".state-*.tmp")
    )


def test_config_defaults_and_file(
    tmp_path: Path,
) -> None:
    assert load_config() == Config()

    path = tmp_path / "config.toml"

    path.write_text(
        '[launch]\n'
        'allow_home_workspace=true\n'
        '[paths]\n'
        'state_root="/s"\n'
    )

    config = load_config(path)

    assert config.allow_home_workspace is True
    assert config.state_root == "/s"

    path.write_text("[launch\n")

    with pytest.raises(ConfigError) as caught:
        load_config(path)

    assert caught.value.code == "ERR_CONFIG_PARSE"

