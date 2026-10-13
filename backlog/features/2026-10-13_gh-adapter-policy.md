---
id: "2026-10-13_gh-adapter-policy"
title: "Allowlisted gh adapter with structured policy"
status: "Ready"
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

- [ ] Allowlisted MCP tools invoke `gh` with structured parameters only
- [ ] Non-allowlisted operations are rejected with a clear error
- [ ] Free-form shell / `gh "$@"` passthrough is not exposed
- [ ] At least one mutating dry-run or real `gh_pr_view` works end-to-end
      via bridle from a Cursor agent session
- [ ] Policy decisions (allow/deny) are available to the action-log task

## Implementation Notes

- Depend on MCP skeleton being runnable
- Keep argv construction explicit (no `shell=True`)
- Document which GitHub operations are in v0 scope

## Related

- CIP: 0001
- Depends on: 2026-10-13_mcp-server-skeleton

## Progress Updates

### 2026-10-13

Task created (Ready) after CIP-0001 Accepted.
