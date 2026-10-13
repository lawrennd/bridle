"""Smoke tests for the bridle ping tool (no live MCP transport)."""

from bridle import __version__
from bridle.server import ping


def test_ping_ok() -> None:
    result = ping()
    assert result["ok"] is True
    assert result["service"] == "bridle"
    assert result["version"] == __version__
