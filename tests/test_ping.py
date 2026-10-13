"""Smoke tests for the bridle ping tool (no live MCP transport)."""

from pathlib import Path

from bridle import __version__
from bridle.server import ping


def test_ping_ok(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("BRIDLE_ACTION_LOG", str(tmp_path / "actions.jsonl"))
    result = ping()
    assert result["ok"] is True
    assert result["service"] == "bridle"
    assert result["version"] == __version__
