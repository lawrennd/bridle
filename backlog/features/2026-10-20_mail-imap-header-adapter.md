---
id: "2026-10-20_mail-imap-header-adapter"
title: "IMAP adapter for header-only mail metadata"
status: "Completed"
priority: "High"
created: "2026-10-20"
last_updated: "2026-10-20"
category: "features"
related_cips: ["0003"]
owner: "Neil D. Lawrence"
dependencies: ["2026-10-20_mail-config-argument-policy"]
tags:
- backlog
- mail
- imap
- metadata
---

# Task: IMAP adapter for header-only mail metadata

> Implements [CIP-0003](../../cip/cip0003.md). Backend: Option A (IMAP).

## Description

Add `mail_adapter.py` (or equivalent) that opens allowlisted accounts via
IMAP using read-only folder semantics (`EXAMINE`) and fetches **headers
only** (`BODY.PEEK[HEADER]` or equivalent). No body, no attachments, no
mutations. Return a stable opaque message id plus From/To/Cc/Bcc/Subject/
Date/Message-ID/mailbox fields. Map failures to a structured error type
(parallel to `GhError`).

## Acceptance Criteria

- [x] Adapter calls `require` / mail policy before any IMAP I/O
- [x] Folder opened read-only; fetch path requests headers only
- [x] Response schema has no `body`, attachment bytes, or full-text keys
- [x] Unit tests with mocked IMAP assert argv/commands and schema
- [x] Credentials via env/keyring path documented; never returned to agent

## Implementation Notes

- Prefer stdlib `imaplib` (thin wrapper tenet) unless a tiny helper is
  clearly safer
- No agent-supplied IMAP command strings
- Cap header value length before return

## Related

- CIP: 0003
- Depends on: 2026-10-20_mail-config-argument-policy

## Progress Updates

### 2026-10-20

Task created (Ready) after CIP-0003 Accepted.

### 2026-10-20 (implemented)

Implemented and covered by unit tests.
