import json
from pathlib import Path

from bridle import action_log
from bridle.server import ping


def test_record_writes_jsonl(tmp_path: Path) -> None:
    path = tmp_path / "actions.jsonl"
    entry = action_log.record(
        tool="ping",
        allowed=True,
        args={},
        result={"ok": True},
        reason="allowlisted",
        path=path,
    )
    assert entry["schema"] == "bridle.action/v0"
    lines = path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    loaded = json.loads(lines[0])
    assert loaded["tool"] == "ping"
    assert loaded["allowed"] is True


def test_redacts_token_fields(tmp_path: Path) -> None:
    path = tmp_path / "actions.jsonl"
    action_log.record(
        tool="ping",
        allowed=True,
        args={"api_token": "secret-value", "repo": "a/b"},
        path=path,
    )
    loaded = json.loads(path.read_text(encoding="utf-8").strip())
    assert loaded["args"]["api_token"] == "***"
    assert loaded["args"]["repo"] == "a/b"


def test_ping_logs_when_env_set(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "actions.jsonl"
    monkeypatch.setenv("BRIDLE_ACTION_LOG", str(path))
    result = ping()
    assert result["ok"] is True
    loaded = json.loads(path.read_text(encoding="utf-8").strip())
    assert loaded["tool"] == "ping"
    assert loaded["allowed"] is True
