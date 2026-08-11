#!/usr/bin/env python3
"""Install bundled Woohyuk custom-agent definitions for Codex."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import shutil
import sys

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 and earlier
    tomllib = None


REQUIRED_FIELDS = {"name", "description", "developer_instructions"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install Woohyuk custom Codex subagent roles."
    )
    parser.add_argument(
        "--scope",
        choices=("user", "project"),
        default="user",
        help="Install under CODEX_HOME (default) or a project's .codex directory.",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        help="Project root for --scope project; defaults to the current directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace installed role files that differ from the bundled versions.",
    )
    return parser.parse_args()


def destination_dir(args: argparse.Namespace) -> Path:
    if args.scope == "user":
        codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
        return codex_home / "agents"

    project_root = (args.project_root or Path.cwd()).expanduser().resolve()
    return project_root / ".codex" / "agents"


def load_and_validate(path: Path) -> dict[str, object]:
    if tomllib is not None:
        try:
            with path.open("rb") as source:
                payload = tomllib.load(source)
        except tomllib.TOMLDecodeError as error:
            raise ValueError(f"{path}: invalid TOML: {error}") from error
    else:
        text = path.read_text(encoding="utf-8")
        payload = {}
        for field in ("name", "description"):
            match = re.search(
                rf'^\s*{field}\s*=\s*"([^"\n]+)"\s*$', text, re.MULTILINE
            )
            if match:
                payload[field] = match.group(1)
        if re.search(
            r'^\s*developer_instructions\s*=\s*"""[\s\S]+"""\s*$',
            text,
            re.MULTILINE,
        ):
            payload["developer_instructions"] = True

    missing = REQUIRED_FIELDS.difference(payload)
    if missing:
        fields = ", ".join(sorted(missing))
        raise ValueError(f"{path}: missing required fields: {fields}")

    if payload["name"] != path.stem:
        raise ValueError(
            f"{path}: name must match filename stem {path.stem!r}"
        )

    return payload


def main() -> int:
    args = parse_args()
    source_dir = Path(__file__).resolve().parent.parent / "assets" / "agents"
    sources = sorted(source_dir.glob("*.toml"))
    if not sources:
        print(f"No bundled agent files found in {source_dir}", file=sys.stderr)
        return 1

    try:
        for source in sources:
            load_and_validate(source)
    except (OSError, UnicodeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1

    destination = destination_dir(args)
    conflicts = [
        destination / source.name
        for source in sources
        if (destination / source.name).exists()
        and (destination / source.name).read_bytes() != source.read_bytes()
    ]
    if conflicts and not args.force:
        print("Refusing to overwrite customized agent files:", file=sys.stderr)
        for conflict in conflicts:
            print(f"- {conflict}", file=sys.stderr)
        print("Rerun with --force only after approving replacement.", file=sys.stderr)
        return 2

    destination.mkdir(parents=True, exist_ok=True)
    installed = 0
    unchanged = 0
    for source in sources:
        target = destination / source.name
        if target.exists() and target.read_bytes() == source.read_bytes():
            unchanged += 1
            print(f"unchanged: {target}")
            continue
        shutil.copy2(source, target)
        installed += 1
        print(f"installed: {target}")

    print(
        f"complete: {installed} installed, {unchanged} unchanged; "
        "start a new Codex session"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
