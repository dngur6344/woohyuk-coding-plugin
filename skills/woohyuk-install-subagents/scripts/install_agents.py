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
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        tomllib = None


REQUIRED_FIELDS = {"name", "description", "developer_instructions"}
SCALAR_FIELDS = {
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "sandbox_mode",
}
ALLOWED_FIELDS = SCALAR_FIELDS | {"developer_instructions"}
SCALAR_ASSIGNMENT = re.compile(
    r'^([a-z_][a-z0-9_]*)[ \t]*=[ \t]*"([^"\\\r\n]*)"[ \t]*$'
)
DEVELOPER_START = re.compile(
    r'^[ \t]*developer_instructions[ \t]*=[ \t]*"""[ \t]*$'
)
DEVELOPER_END = re.compile(r'^[ \t]*"""[ \t]*$')


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


def parse_restricted_toml(path: Path) -> dict[str, object]:
    """Parse only the top-level TOML subset used by bundled role files."""
    text = path.read_bytes().decode("utf-8")
    for offset, character in enumerate(text):
        codepoint = ord(character)
        if character in {"\n", "\t"}:
            continue
        if (
            character == "\r"
            and offset + 1 < len(text)
            and text[offset + 1] == "\n"
        ):
            continue
        if codepoint < 0x20 or 0x7F <= codepoint <= 0x9F:
            line_number = text.count("\n", 0, offset) + 1
            raise ValueError(
                f"{path}:{line_number}: disallowed control character U+{codepoint:04X}"
            )

    lines = text.splitlines()
    payload: dict[str, object] = {}
    index = 0

    while index < len(lines):
        line = lines[index]
        line_number = index + 1
        if not line.strip():
            index += 1
            continue

        if DEVELOPER_START.fullmatch(line):
            field = "developer_instructions"
            if field in payload:
                raise ValueError(f"{path}:{line_number}: duplicate field {field!r}")

            index += 1
            instructions = []
            while index < len(lines):
                instruction_line = lines[index]
                if DEVELOPER_END.fullmatch(instruction_line):
                    break
                if '"""' in instruction_line:
                    raise ValueError(
                        f"{path}:{index + 1}: embedded triple-quote delimiter"
                    )
                if "\\" in instruction_line:
                    raise ValueError(
                        f"{path}:{index + 1}: backslashes are unsupported "
                        "in developer_instructions"
                    )
                instructions.append(instruction_line)
                index += 1
            if index == len(lines):
                raise ValueError(
                    f"{path}:{line_number}: unterminated developer_instructions"
                )
            payload[field] = "\n".join(instructions)
            index += 1
            continue

        assignment = SCALAR_ASSIGNMENT.fullmatch(line)
        if assignment:
            field, value = assignment.groups()
            if field not in SCALAR_FIELDS:
                raise ValueError(f"{path}:{line_number}: unknown field {field!r}")
            if field in payload:
                raise ValueError(f"{path}:{line_number}: duplicate field {field!r}")
            payload[field] = value
            index += 1
            continue

        raise ValueError(
            f"{path}:{line_number}: invalid or unsupported TOML syntax"
        )

    return payload


def load_and_validate(path: Path) -> dict[str, object]:
    if tomllib is None:
        payload = parse_restricted_toml(path)
    else:
        try:
            with path.open("rb") as source:
                payload = tomllib.load(source)
        except tomllib.TOMLDecodeError as error:
            raise ValueError(f"{path}: invalid TOML: {error}") from error

    unknown = set(payload).difference(ALLOWED_FIELDS)
    if unknown:
        fields = ", ".join(sorted(unknown))
        raise ValueError(f"{path}: unknown fields: {fields}")

    non_strings = [
        field for field, value in payload.items() if not isinstance(value, str)
    ]
    if non_strings:
        fields = ", ".join(sorted(non_strings))
        raise ValueError(f"{path}: fields must be quoted strings: {fields}")

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
