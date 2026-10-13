---
id: "2026-10-13_gh-adapter-policy"
title: "Allowlisted gh adapter with structured policy"
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
- gh
- mcp
- policy
---

# Task: Allowlisted gh adapter with structured policy

> Implements [CIP-0001](../../cip/cip0001.md).

## Description

Add a `gh` adapter behind bridle MCP tools with an explicit allowlist and
structured arguments (no free-form shell strings). Initial tools:
`gh_pr_create`, `gh_pr_view` / `gh_pr_list`, and a narrow path-allowlisted
`gh_api` if needed. Credentials stay in the user's keyring; execution
happens in the unsandboxed bridle process.

## Acceptance Criteria

- [x] Allowlisted MCP tools invoke `gh` with structured parameters only
- [x] Non-allowlisted operations are rejected with a clear error (`PolicyDenied`)
- [x] Free-form shell / `gh "$@"` passthrough is not exposed
- [x] Unit tests cover `gh_pr_view` / `gh_pr_create` with mocked `gh`
      (Cursor end-to-end after MCP config reload)
- [x] Policy decisions (allow/deny) are available to the action-log task
      via `bridle.policy.decide` / `require`

## Implementation Notes

- Depend on MCP skeleton being runnable
- Keep argv construction explicit (`shell=False`)
- Document which GitHub operations are in v0 scope

## Related

- CIP: 0001
- Depends on: 2026-10-13_mcp-server-skeleton

## Progress Updates

### 2026-10-13

Task created (Ready) after CIP-0001 Accepted.

### 2026-10-13 (later)

Implemented `policy.py`, `gh_adapter.py`, MCP tools `gh_pr_view` /
`gh_pr_list` / `gh_pr_create`, and mocked unit tests. Marked Completed.

### 2026-10-13 (MCP live)

Live `gh_pr_list` on `lawrennd/mlai` from the Cursor agent returned open
PR #1 (Deep GP pinball fix) without opening the seatbelt sandbox.
