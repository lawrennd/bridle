"""MCP server entry points for bridle.

Default transport is stdio (Cursor launches bridle as a subprocess). Optional
Streamable HTTP on 127.0.0.1 is available for local probing without Cursor.
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from bridle import __version__

mcp = FastMCP(
    "bridle",
    instructions=(
        "Bridle is a local privileged MCP control plane. "
        "Call ping to verify the server is reachable. "
        "Allowlisted adapters (gh, …) register additional tools."
    ),
)


@mcp.tool()
def ping() -> dict[str, Any]:
    """Health check: confirm the bridle MCP server is reachable."""
    return {
        "ok": True,
        "service": "bridle",
        "version": __version__,
    }


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
