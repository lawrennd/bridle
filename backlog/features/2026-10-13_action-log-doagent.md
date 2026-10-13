---
id: "2026-10-13_action-log-doagent"
title: "Accountable action log (DOAgent-compatible)"
status: "Completed"
priority: "High"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "features"
related_cips: ["0001"]
owner: "Neil D. Lawrence"
dependencies: ["2026-10-13_mcp-server-skeleton"]
tags:
- backlog
- doagent
- audit
- mcp
---

# Task: Accountable action log (DOAgent-compatible)

> Implements [CIP-0001](../../cip/cip0001.md).

## Description

Record every bridle tool invocation (inputs, policy decision, outcome or
failure) in an append-only action log. Prefer DOAgent sessions if the
dependency is light; otherwise ship a compatible record schema that can
swap to DOAgent without changing the MCP surface.

## Acceptance Criteria

- [x] Each tool call writes a durable record (timestamp, tool, args
      summary, allow/deny, result or error)
- [x] Records are queryable after a run (JSONL file-backed)
- [x] Schema documented as `bridle.action/v0` (DOAgent mapping later)
- [x] Denied policy checks are logged as well as successful executions

## Implementation Notes

- Can land in parallel with the `gh` adapter once the skeleton exists
- Avoid logging secrets (tokens); redact env and auth material
- CIP allows a compatible schema first if DOAgent is heavy for v0

## Related

- CIP: 0001
- Depends on: 2026-10-13_mcp-server-skeleton
- Related: 2026-10-13_gh-adapter-policy

## Progress Updates

### 2026-10-13

Task created (Ready) after CIP-0001 Accepted.

### 2026-10-13 (later)

Implemented `action_log.py` and wired `_invoke` in `server.py` so every
MCP tool path logs allow/deny/result. Marked Completed.
