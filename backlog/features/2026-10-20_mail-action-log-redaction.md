---
id: "2026-10-20_mail-action-log-redaction"
title: "Action-log truncation and redaction for mail metadata"
status: "Ready"
priority: "Medium"
created: "2026-10-20"
last_updated: "2026-10-20"
category: "features"
related_cips: ["0003"]
owner: "Neil D. Lawrence"
dependencies: ["2026-10-20_mail-header-mcp-tools"]
tags:
- backlog
- mail
- audit
- privacy
---

# Task: Action-log truncation and redaction for mail metadata

> Implements [CIP-0003](../../cip/cip0003.md).

## Description

Ensure `bridle.action/v0` JSONL records for mail tools never retain message
bodies (none should be returned) and truncate oversized header fields in
logged `args` / `result`. Extend redaction for credential-like keys in mail
errors (password, token, authorization already covered — verify IMAP auth
failures do not leak secrets).

## Acceptance Criteria

- [ ] Logged mail results omit any accidental body-sized payloads
- [ ] Oversized header strings in the log are truncated with a marker
- [ ] Unit tests assert redaction/truncation on sample header results
- [ ] Existing `gh_*` logging behaviour unchanged

## Implementation Notes

- Touch `action_log.py` carefully; keep schema version unless a bump is
  required
- Prefer truncating at log time rather than stripping fields the agent
  already received (agent still gets full headers within adapter caps)

## Related

- CIP: 0003
- Depends on: 2026-10-20_mail-header-mcp-tools

## Progress Updates

### 2026-10-20

Task created (Ready) after CIP-0003 Accepted.
