---
id: "2026-10-20_mail-headers-readme"
title: "Document mail header tools, config, and privacy boundary"
status: "Ready"
priority: "Medium"
created: "2026-10-20"
last_updated: "2026-10-20"
category: "documentation"
related_cips: ["0003"]
owner: "Neil D. Lawrence"
dependencies: ["2026-10-20_mail-header-mcp-tools"]
tags:
- backlog
- mail
- documentation
- privacy
---

# Task: Document mail header tools, config, and privacy boundary

> Implements [CIP-0003](../../cip/cip0003.md).

## Description

Update the project README (and any MCP config notes) with the new allowlisted
tools, example `~/.bridle/mail.toml` / env vars, IMAP credential setup, and
an explicit privacy note: bridle enforces metadata-only and account
allowlists; this does not replace OS grants if a future backend needs them
(IMAP Option A avoids Mail.app Automation).

## Acceptance Criteria

- [ ] README allowlist table includes the three `mail_*` tools
- [ ] Config and credential setup documented briefly
- [ ] Privacy / least-disclosure note links REQ-0003 / CIP-0003
- [ ] Cursor MCP reload note for new tool schemas

## Implementation Notes

- User content: root `README.md` only; do not treat VibeSafe system docs as
  the home for this

## Related

- CIP: 0003
- Depends on: 2026-10-20_mail-header-mcp-tools

## Progress Updates

### 2026-10-20

Task created (Ready) after CIP-0003 Accepted.
