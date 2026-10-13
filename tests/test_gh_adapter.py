import json
from unittest.mock import MagicMock, patch

import pytest

from bridle import gh_adapter
from bridle.policy import PolicyDenied


def test_run_gh_rejects_non_string_argv() -> None:
    with pytest.raises(gh_adapter.GhError, match="list of strings"):
        gh_adapter.run_gh(["pr", "view", 1])  # type: ignore[list-item]


@patch("bridle.gh_adapter.shutil.which", return_value="/usr/bin/gh")
@patch("bridle.gh_adapter.subprocess.run")
def test_gh_pr_view_ok(mock_run: MagicMock, _which: MagicMock) -> None:
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout=json.dumps(
            {"number": 1, "title": "Fix", "url": "https://example/pr/1", "state": "OPEN"}
        ),
        stderr="",
    )
    result = gh_adapter.gh_pr_view("lawrennd/bridle", 1)
    assert result["ok"] is True
    assert result["pr"]["number"] == 1
    argv = mock_run.call_args.args[0]
    assert argv[:4] == ["/usr/bin/gh", "pr", "view", "1"]
    assert mock_run.call_args.kwargs["shell"] is False


@patch("bridle.gh_adapter.shutil.which", return_value="/usr/bin/gh")
@patch("bridle.gh_adapter.subprocess.run")
def test_gh_pr_create_ok(mock_run: MagicMock, _which: MagicMock) -> None:
    mock_run.return_value = MagicMock(
        returncode=0,
        stdout="https://github.com/lawrennd/bridle/pull/2\n",
        stderr="",
    )
    result = gh_adapter.gh_pr_create(
        "lawrennd/bridle",
        title="Add thing",
        body="body",
        base="main",
        head="feature",
    )
    assert result["ok"] is True
    assert result["url"].endswith("/pull/2")


def test_unknown_tool_not_callable_via_require() -> None:
    with pytest.raises(PolicyDenied):
        from bridle.policy import require

        require("gh_shell")
