#!/usr/bin/env python3
"""Resolve the model selected for the active Codex session."""

from __future__ import annotations

import json
import os
from pathlib import Path
import re


SESSION_ID = re.compile(r"^[0-9a-fA-F-]{32,36}$")


def emit(status: str, model: str | None = None, effort: str | None = None) -> None:
    print(
        json.dumps(
            {
                "status": status,
                "model": model,
                "reasoning_effort": effort,
            },
            separators=(",", ":"),
        )
    )


def main() -> int:
    session_id = os.environ.get("CODEX_SESSION_ID") or os.environ.get(
        "CODEX_THREAD_ID"
    )
    if not session_id or not SESSION_ID.fullmatch(session_id):
        emit("unknown")
        return 0

    codex_home = Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser()
    sessions_root = codex_home / "sessions"
    candidates = sorted(
        sessions_root.rglob(f"*{session_id}*.jsonl"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    for candidate in candidates:
        latest_model = None
        latest_effort = None
        try:
            with candidate.open(encoding="utf-8") as session:
                for line in session:
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if item.get("type") != "turn_context":
                        continue
                    payload = item.get("payload")
                    if not isinstance(payload, dict):
                        continue
                    model = payload.get("model")
                    if isinstance(model, str) and model:
                        latest_model = model
                        effort = payload.get("effort")
                        latest_effort = effort if isinstance(effort, str) else None
        except OSError:
            continue

        if latest_model:
            emit("detected", latest_model, latest_effort)
            return 0

    emit("unknown")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
