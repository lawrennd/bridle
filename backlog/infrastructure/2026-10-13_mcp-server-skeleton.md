---
id: "2026-10-13_mcp-server-skeleton"
title: "MCP server skeleton on localhost"
status: "Completed"
priority: "High"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "infrastructure"
related_cips: ["0001"]
owner: "Neil D. Lawrence"
dependencies: []
tags:
- backlog
- mcp
- infrastructure
---

# Task: MCP server skeleton on localhost

> Backlog tasks are DOING the work defined in CIPs (HOW).  
> Implements [CIP-0001](../../cip/cip0001.md).

## Description

Stand up a Python MCP server bound to localhost that Cursor agents can call
without opening the seatbelt sandbox to the public internet. Include a
health/ping tool and document how to register the server in Cursor MCP
config.

## Acceptance Criteria

- [x] MCP server starts from the bridle repo in an unsandboxed terminal
- [x] Server listens on localhost only (127.0.0.1) for optional HTTP;
      Cursor uses stdio by default
- [x] Health/ping tool implemented and unit-tested (`pytest`); wire it in
      Cursor via MCP config in README
- [x] README includes a Cursor MCP config snippet and start instructions
- [x] Package/layout is ready for adapters to register tools
      (`src/bridle/server.py` FastMCP instance)

## Implementation Notes

- Prefer a small, dependency-light MCP Python stack consistent with the
  rest of the `lawrennd` tooling
- Keep tool handlers thin; policy and adapters come in follow-on tasks
- Do not require sandbox disable in Cursor for the agent side

## Related

- CIP: 0001
- Requirement: REQ-0001

## Progress Updates

### 2026-10-13

Task created (Ready) after CIP-0001 Accepted.

### 2026-10-13 (later)

Implemented `src/bridle` with FastMCP `ping`, `pyproject.toml`, stdio
default + optional `BRIDLE_TRANSPORT=streamable-http` on 127.0.0.1:8766,
README Cursor MCP snippet, and unit test. Marked Completed.
