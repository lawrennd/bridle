"""MCP server entry points for bridle.

Default transport is stdio (Cursor launches bridle as a subprocess). Optional
Streamable HTTP on 127.0.0.1 is available for local probing without Cursor.
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from bridle import __version__
from bridle import action_log, gh_adapter
from bridle.policy import PolicyDenied, decide, require

mcp = FastMCP(
    "bridle",
    instructions=(
        "Bridle is a local privileged MCP control plane. "
        "Call ping to verify the server is reachable. "
        "Allowlisted gh tools: gh_pr_view, gh_pr_list, gh_pr_create. "
        "No free-form shell is exposed."
    ),
)


def _invoke(tool: str, args: dict[str, Any], fn) -> dict[str, Any]:
    """Run an allowlisted tool, always writing an action-log record."""
    decision = decide(tool, **args)
    if not decision.allowed:
        action_log.record(
            tool=tool,
            allowed=False,
            args=args,
            reason=decision.reason,
            error=decision.reason,
        )
        return {"ok": False, "error": decision.reason}
    try:
        result = fn()
        action_log.record(
            tool=tool,
            allowed=True,
            args=args,
            reason=decision.reason,
            result=result if isinstance(result, dict) else {"value": result},
        )
        return result
    except (PolicyDenied, gh_adapter.GhError) as exc:
        action_log.record(
            tool=tool,
            allowed=True,
            args=args,
            reason=decision.reason,
            error=str(exc),
        )
        return {"ok": False, "error": str(exc)}


@mcp.tool()
def ping() -> dict[str, Any]:
    """Health check: confirm the bridle MCP server is reachable."""

    def _run() -> dict[str, Any]:
        require("ping")
        return {
            "ok": True,
            "service": "bridle",
            "version": __version__,
        }

    return _invoke("ping", {}, _run)


@mcp.tool()
def gh_pr_view(repo: str, number: int) -> dict[str, Any]:
    """View a GitHub pull request via allowlisted ``gh pr view``."""
    args = {"repo": repo, "number": number}
    return _invoke("gh_pr_view", args, lambda: gh_adapter.gh_pr_view(repo, number))


@mcp.tool()
def gh_pr_list(
    repo: str,
    state: str = "open",
    limit: int = 10,
) -> dict[str, Any]:
    """List GitHub pull requests via allowlisted ``gh pr list``."""
    args = {"repo": repo, "state": state, "limit": limit}
    return _invoke(
        "gh_pr_list",
        args,
        lambda: gh_adapter.gh_pr_list(repo, state=state, limit=limit),
    )


@mcp.tool()
def gh_pr_create(
    repo: str,
    title: str,
    body: str,
    base: str,
    head: str,
    draft: bool = False,
) -> dict[str, Any]:
    """Create a GitHub pull request via allowlisted ``gh pr create``."""
    args = {
        "repo": repo,
        "title": title,
        "body": body,
        "base": base,
        "head": head,
        "draft": draft,
    }
    return _invoke(
        "gh_pr_create",
        args,
        lambda: gh_adapter.gh_pr_create(
            repo,
            title=title,
            body=body,
            base=base,
            head=head,
            draft=draft,
        ),
    )


def run() -> None:
    """Run the MCP server.

    Environment:
      BRIDLE_TRANSPORT: ``stdio`` (default) or ``streamable-http``
      BRIDLE_HOST: bind host for HTTP (default ``127.0.0.1``)
      BRIDLE_PORT: bind port for HTTP (default ``8766``)
    """
    transport = os.environ.get("BRIDLE_TRANSPORT", "stdio").strip().lower()
    if transport in {"stdio", ""}:
        mcp.run(transport="stdio")
        return
    if transport in {"streamable-http", "http"}:
        host = os.environ.get("BRIDLE_HOST", "127.0.0.1")
        port = int(os.environ.get("BRIDLE_PORT", "8766"))
        mcp.run(transport="streamable-http", host=host, port=port)
        return
    raise SystemExit(
        f"Unknown BRIDLE_TRANSPORT={transport!r}; use stdio or streamable-http"
    )
