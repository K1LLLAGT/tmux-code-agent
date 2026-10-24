import os
import subprocess
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
UNINSTALL = REPOSITORY / "uninstall.sh"


def run_uninstall(
    home: Path,
    *arguments: str,
) -> subprocess.CompletedProcess[str]:
    environment = {
        **os.environ,
        "HOME": str(home),
    }

    return subprocess.run(
        ["bash", str(UNINSTALL), *arguments],
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_uninstall_removes_link_and_empty_created_parents(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    source = tmp_path / "source"
    app_root = home / ".local" / "share" / "tmux-code-agent"
    target = app_root / "current"

    source.mkdir()
    app_root.mkdir(parents=True)
    target.symlink_to(source, target_is_directory=True)

    completed = run_uninstall(home)

    assert completed.returncode == 0, completed.stderr
    assert not target.exists()
    assert not target.is_symlink()
    assert not app_root.exists()
    assert not (home / ".local" / "share").exists()
    assert not (home / ".local").exists()


def test_uninstall_preserves_nonempty_parent_directories(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    source = tmp_path / "source"
    app_root = home / ".local" / "share" / "tmux-code-agent"
    target = app_root / "current"
    unrelated = home / ".local" / "share" / "other-app" / "keep.txt"

    source.mkdir()
    app_root.mkdir(parents=True)
    target.symlink_to(source, target_is_directory=True)

    unrelated.parent.mkdir(parents=True)
    unrelated.write_text("preserve\n", encoding="utf-8")

    completed = run_uninstall(home)

    assert completed.returncode == 0, completed.stderr
    assert not target.exists()
    assert not target.is_symlink()
    assert not app_root.exists()
    assert unrelated.read_text(encoding="utf-8") == "preserve\n"
    assert (home / ".local" / "share").is_dir()
    assert (home / ".local").is_dir()


def test_uninstall_dry_run_changes_nothing(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    source = tmp_path / "source"
    app_root = home / ".local" / "share" / "tmux-code-agent"
    target = app_root / "current"

    source.mkdir()
    app_root.mkdir(parents=True)
    target.symlink_to(source, target_is_directory=True)

    completed = run_uninstall(home, "--dry-run")

    assert completed.returncode == 0, completed.stderr
    assert target.is_symlink()
    assert app_root.is_dir()


def test_uninstall_refuses_non_symlink_target(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    target = (
        home
        / ".local"
        / "share"
        / "tmux-code-agent"
        / "current"
    )

    target.parent.mkdir(parents=True)
    target.write_text("do not delete\n", encoding="utf-8")

    completed = run_uninstall(home)

    assert completed.returncode != 0
    assert target.read_text(encoding="utf-8") == "do not delete\n"
    assert "refusing to remove non-symlink" in completed.stderr


def test_uninstall_is_idempotent_when_target_is_absent(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    home.mkdir()

    first = run_uninstall(home)
    second = run_uninstall(home)

    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr


def test_uninstall_rejects_unknown_argument(
    tmp_path: Path,
) -> None:
    home = tmp_path / "home"
    home.mkdir()

    completed = run_uninstall(home, "--unknown")

    assert completed.returncode == 2
    assert "Usage:" in completed.stderr
