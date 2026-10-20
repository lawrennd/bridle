"""Append-only action log (DOAgent-compatible schema for v0)."""

from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any

_lock = threading.Lock()


def default_log_path() -> Path:
    configured = os.environ.get("BRIDLE_ACTION_LOG", "").strip()
    if configured:
        return Path(configured).expanduser()
    return Path.home() / ".bridle" / "actions.jsonl"


_LOG_STRING_CAP = 512
# Keys that must never appear in the action log (content under REQ-0003).
_CONTENT_KEYS = frozenset({"body", "text", "html", "attachment", "attachments", "payload"})


def _truncate_str(value: str) -> str:
    if len(value) <= _LOG_STRING_CAP:
        return value
    return value[:_LOG_STRING_CAP] + "…[truncated]"


def _redact(value: Any) -> Any:
    """Redact secrets, drop content keys, and truncate long strings for the log."""
    if isinstance(value, dict):
        out: dict[str, Any] = {}
        for key, item in value.items():
            lk = str(key).lower()
            if lk in _CONTENT_KEYS or any(
                s in lk for s in ("token", "password", "secret", "authorization")
            ):
                out[key] = "***"
            else:
                out[key] = _redact(item)
        return out
    if isinstance(value, list):
        return [_redact(v) for v in value]
    if isinstance(value, str):
        return _truncate_str(value)
    return value


def record(
    *,
    tool: str,
    allowed: bool,
    args: dict[str, Any] | None = None,
    result: dict[str, Any] | None = None,
    error: str | None = None,
    reason: str | None = None,
    path: Path | None = None,
) -> dict[str, Any]:
    """Append one JSONL action record. Returns the record written."""
    entry = {
        "ts": time.time(),
        "tool": tool,
        "allowed": allowed,
        "reason": reason,
        "args": _redact(args or {}),
        "result": _redact(result) if result is not None else None,
        "error": error,
        "schema": "bridle.action/v0",
    }
    target = path or default_log_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(entry, ensure_ascii=False, sort_keys=True)
    with _lock:
        with target.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    return entry
