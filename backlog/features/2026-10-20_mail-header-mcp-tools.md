---
id: "2026-10-20_mail-header-mcp-tools"
title: "MCP tools mail_account_list / mail_header_list / mail_header_view"
status: "Completed"
priority: "High"
created: "2026-10-20"
last_updated: "2026-10-20"
category: "features"
related_cips: ["0003"]
owner: "Neil D. Lawrence"
dependencies: ["2026-10-20_mail-imap-header-adapter"]
tags:
- backlog
- mail
- mcp
---

# Task: MCP tools for mail header metadata

> Implements [CIP-0003](../../cip/cip0003.md).

## Description

Expose three allowlisted MCP tools on the FastMCP server, wired through
`_invoke` like `gh_*`:

| Tool | Purpose |
|------|---------|
| `mail_account_list` | Labels from config only |
| `mail_header_list` | Recent headers (`account`, optional `mailbox`, `limit`, `from_glob`) |
| `mail_header_view` | One message headers by opaque id |

Update `ALLOWED_TOOLS` and server `instructions` (headers only; metadata is
untrusted data). Extend `_invoke` to catch the mail adapter error type.

## Acceptance Criteria

- [x] Three tools registered; no body/send/mutate mail tools
- [x] Policy deny and adapter errors return `{ok: false, error: …}`
- [x] `instructions` state metadata-only / untrusted content
- [x] Unit or smoke tests cover tool wiring with mocked adapter

## Implementation Notes

- Mirror `gh_pr_*` wrapper style in `server.py`
- Do not expose free-form IMAP or script parameters

## Related

- CIP: 0003
- Depends on: 2026-10-20_mail-imap-header-adapter

## Progress Updates

### 2026-10-20

Task created (Ready) after CIP-0003 Accepted.

### 2026-10-20 (implemented)

Implemented and covered by unit tests.
