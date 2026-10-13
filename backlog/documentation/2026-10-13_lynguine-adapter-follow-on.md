---
id: "2026-10-13_lynguine-adapter-follow-on"
title: "Track lynguine adapter as follow-on CIP"
status: "Proposed"
priority: "Low"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "documentation"
related_cips: ["0001"]
owner: "Neil D. Lawrence"
dependencies:
- "2026-10-13_gh-adapter-policy"
- "2026-10-13_bridle-hardening-tests"
tags:
- backlog
- lynguine
- follow-on
---

# Task: Track lynguine adapter as follow-on CIP

> Placeholder DO item from [CIP-0001](../../cip/cip0001.md) step 5.
> Implementation belongs in a **new CIP** after the `gh` path is boring.

## Description

Do not implement a lynguine MCP adapter under CIP-0001. When `gh` is
stable, open a follow-on CIP for a bridle adapter that talks to lynguine
server mode (`ServerClient` / localhost HTTP), keeping MCP out of lynguine
core for now.

## Acceptance Criteria

- [ ] CIP-0001 remains free of lynguine adapter implementation scope
- [ ] A follow-on CIP is drafted when hardening of the `gh` path is done
- [ ] This task is Completed or Abandoned once that CIP exists

## Implementation Notes

- CIP-0001 decision: lynguine engages as adapter later, not in lynguine core
- Priority Low until `gh` adapter is routine

## Related

- CIP: 0001 (tracking only)
- Future CIP: TBD

## Progress Updates

### 2026-10-13

Task created (Proposed) as a reminder, not as active implementation.
