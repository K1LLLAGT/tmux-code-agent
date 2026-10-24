"""tmux-code-agent command-line entry point."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cli.launch import dry_run_start, live_start
from cli.render import render_dry_run, render_json
from core.config import load_config
from core.errors import TCAError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tmux-code-agent")
    sub = parser.add_subparsers(dest="command", required=True)
    start = sub.add_parser("start")
    start.add_argument("--dry-run", action="store_true")
    start.add_argument("--json", action="store_true")
    start.add_argument("--workspace")
    start.add_argument("--config", type=Path)
    start.add_argument("--allow-home", action="store_true")
    start.add_argument("--allow-root", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_config(args.config)
        if args.allow_home or args.allow_root:
            from dataclasses import replace
            config = replace(
                config,
                allow_home_workspace=config.allow_home_workspace or args.allow_home,
                allow_root_workspace=config.allow_root_workspace or args.allow_root,
            )
        if args.command == "start":
            if args.dry_run:
                payload = dry_run_start(workspace=args.workspace, config=config)
                print(render_json(payload) if args.json else render_dry_run(payload))
                return 0
            payload = live_start(workspace=args.workspace, config=config)
            if args.json:
                print(render_json(payload))
            else:
                print(f"Session:   {payload['session_id'][:8]}")
                print(f"Status:    {payload['status']}")
                print(f"URL:       {payload['url']}")
                print(f"Runtime:   {payload['paths']['runtime_dir']}")
            return 0
    except TCAError as exc:
        print(render_json({"error": exc.as_dict()}), file=sys.stderr)
        return exc.exit_code
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
