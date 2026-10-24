import os
import time
from pathlib import Path

from tmuxctl.panes import registry
from tmuxctl.server import (
    kill_server,
    run,
    start_private_server,
)


def test_registry_authoritative_and_process_exit(
    tmp_path: Path,
) -> None:
    socket = (
        Path(os.environ["PREFIX"])
        / "tmp"
        / f"tca-m3-reg-{os.getpid()}.sock"
    )
    workspace = tmp_path / "w"
    workspace.mkdir()

    try:
        start_private_server(
            socket,
            workspace,
        )

        before = registry(socket)

        assert len(before) == 3

        pane_id = next(iter(before))

        assert before[pane_id]["dead"] is False

        run(
            socket,
            "respawn-pane",
            "-k",
            "-t",
            pane_id,
            "sh",
            "-c",
            "exit 7",
        )

        deadline = time.monotonic() + 2.0
        after = {}

        while time.monotonic() < deadline:
            after = registry(socket)

            if (
                pane_id in after
                and after[pane_id]["dead"] is True
            ):
                break

            time.sleep(0.05)

        assert pane_id in after
        assert after[pane_id]["dead"] is True

    finally:
        kill_server(socket)
        socket.unlink(missing_ok=True)

