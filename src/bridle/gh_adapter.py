"""Allowlisted GitHub CLI adapter (structured args only)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any

from bridle.policy import require


class GhError(RuntimeError):
    """Raised when a gh invocation fails."""


def _gh_bin() -> str:
    configured = os.environ.get("BRIDLE_GH_BIN", "").strip()
    if configured:
        return configured
    found = shutil.which("gh")
    if not found:
        raise GhError("gh executable not found on PATH (set BRIDLE_GH_BIN)")
    return found


def run_gh(args: list[str], *, timeout: float = 120.0) -> dict[str, Any]:
    """Run ``gh`` with an explicit argv list (never a shell string)."""
    if not args:
        raise GhError("empty gh argv")
    if any(not isinstance(a, str) for a in args):
        raise GhError("gh argv must be a list of strings")

    cmd = [_gh_bin(), *args]
    try:
        completed = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise GhError(f"gh timed out after {timeout}s: {' '.join(cmd)}") from exc

    result: dict[str, Any] = {
        "argv": cmd,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    if completed.returncode != 0:
        raise GhError(
            f"gh exited {completed.returncode}: {completed.stderr.strip() or completed.stdout.strip()}"
        )
    return result


def gh_pr_view(
    repo: str,
    number: int,
    *,
    json_fields: str = "number,title,url,state,body",
) -> dict[str, Any]:
    """View a pull request (allowlisted)."""
    require("gh_pr_view", repo=repo, number=number)
    if not isinstance(number, int) or number <= 0:
        raise GhError("number must be a positive integer")
    if not repo or "/" not in repo:
        raise GhError("repo must look like owner/name")

    raw = run_gh(
        [
            "pr",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            json_fields,
        ]
    )
    payload = json.loads(raw["stdout"] or "{}")
    return {"ok": True, "pr": payload}


def gh_pr_list(
    repo: str,
    *,
    state: str = "open",
    limit: int = 10,
    json_fields: str = "number,title,url,state",
) -> dict[str, Any]:
    """List pull requests (allowlisted)."""
    require("gh_pr_list", repo=repo, state=state, limit=limit)
    if state not in {"open", "closed", "merged", "all"}:
        raise GhError("state must be one of open|closed|merged|all")
    if not isinstance(limit, int) or not 1 <= limit <= 100:
        raise GhError("limit must be an int in 1..100")
    if not repo or "/" not in repo:
        raise GhError("repo must look like owner/name")

    raw = run_gh(
        [
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            state,
            "--limit",
            str(limit),
            "--json",
            json_fields,
        ]
    )
    payload = json.loads(raw["stdout"] or "[]")
    return {"ok": True, "pull_requests": payload}


def gh_pr_create(
    repo: str,
    *,
    title: str,
    body: str,
    base: str,
    head: str,
    draft: bool = False,
) -> dict[str, Any]:
    """Create a pull request (allowlisted mutating operation)."""
    require(
        "gh_pr_create",
        repo=repo,
        title=title,
        base=base,
        head=head,
        draft=draft,
    )
    if not repo or "/" not in repo:
        raise GhError("repo must look like owner/name")
    if not title.strip():
        raise GhError("title must be non-empty")
    if not base.strip() or not head.strip():
        raise GhError("base and head must be non-empty")

    args = [
        "pr",
        "create",
        "--repo",
        repo,
        "--title",
        title,
        "--body",
        body,
        "--base",
        base,
        "--head",
        head,
    ]
    if draft:
        args.append("--draft")

    raw = run_gh(args)
    # gh prints the PR URL on stdout for successful create
    url = (raw["stdout"] or "").strip().splitlines()[-1] if raw["stdout"] else ""
    return {"ok": True, "url": url, "stdout": raw["stdout"], "stderr": raw["stderr"]}
