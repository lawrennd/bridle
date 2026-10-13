---
id: "2026-10-13_bridle-hardening-tests"
title: "Bridle hardening: confirm, tests, failure docs"
status: "Ready"
priority: "Medium"
created: "2026-10-13"
last_updated: "2026-10-13"
category: "features"
related_cips: ["0001"]
owner: "Neil D. Lawrence"
dependencies:
- "2026-10-13_gh-adapter-policy"
- "2026-10-13_action-log-doagent"
tags:
- backlog
- testing
- hardening
- documentation
---

# Task: Bridle hardening — confirm, tests, failure docs

> Implements [CIP-0001](../../cip/cip0001.md).

## Description

Harden the v0 bridle path: optional confirmation for mutating operations,
unit tests with mocked `gh`, and documentation of failure modes (bridle not
running vs policy deny vs the Cursor seatbelt CONNECT 403 red herring).

## Acceptance Criteria

- [ ] Optional confirm path for mutating tools (config or per-call flag)
- [ ] Unit tests cover policy allow/deny and argument validation
- [ ] Mocked-`gh` tests cover adapter success and failure paths
- [ ] README (or CIP compression later) documents: bridle down, policy
      deny, and sandbox proxy 403 misreported as invalid token

## Implementation Notes

- Depends on `gh` adapter and action log existing
- Keep confirm UX simple for v0 (config file or env flag is enough)

## Related

- CIP: 0001
- Depends on: 2026-10-13_gh-adapter-policy, 2026-10-13_action-log-doagent

## Progress Updates

### 2026-10-13

Task created (Ready) after CIP-0001 Accepted.
