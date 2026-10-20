"""Allowlist policy for bridle adapters (no free-form shell)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class PolicyDenied(PermissionError):
    """Raised when a tool or operation is not on the allowlist."""


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    tool: str
    reason: str
    details: dict[str, Any] | None = None


# Tools registered on the MCP server that may invoke privileged adapters.
ALLOWED_TOOLS = frozenset(
    {
        "ping",
        "gh_pr_view",
        "gh_pr_list",
        "gh_pr_create",
        "mail_account_list",
        "mail_header_list",
        "mail_header_view",
    }
)


def decide(tool: str, **details: Any) -> PolicyDecision:
    """Return an allow/deny decision for a tool invocation."""
    if tool not in ALLOWED_TOOLS:
        return PolicyDecision(
            allowed=False,
            tool=tool,
            reason=f"tool {tool!r} is not on the bridle allowlist",
            details=dict(details) or None,
        )
    return PolicyDecision(
        allowed=True,
        tool=tool,
        reason="allowlisted",
        details=dict(details) or None,
    )


def require(tool: str, **details: Any) -> PolicyDecision:
    """Allowlist check that raises PolicyDenied on reject."""
    decision = decide(tool, **details)
    if not decision.allowed:
        raise PolicyDenied(decision.reason)
    return decision
