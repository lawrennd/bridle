---
id: "2026-10-20_mail-config-argument-policy"
title: "Mail config and argument-level allowlist policy"
status: "Completed"
priority: "High"
created: "2026-10-20"
last_updated: "2026-10-20"
category: "features"
related_cips: ["0003"]
owner: "Neil D. Lawrence"
dependencies: []
tags:
- backlog
- mail
- policy
- privacy
---

# Task: Mail config and argument-level allowlist policy

> Implements [CIP-0003](../../cip/cip0003.md).

## Description

Extend bridle policy beyond tool-name allowlisting so mail metadata tools
can enforce configured **accounts**, **mailboxes**, optional **sender
globs**, and **max list** caps before any IMAP call. Load allowlist config
from a user file (e.g. `~/.bridle/mail.toml`) and/or `BRIDLE_MAIL_*` env
vars. Deny by default when mail is unconfigured.

## Acceptance Criteria

- [x] Config declares allowlisted account ids and mailboxes (explicit list)
- [x] Optional `allowed_from` globs; missing/empty means any sender within
      an allowlisted mailbox
- [x] `decide` / `require` (or mail-specific helpers) reject unknown
      account, mailbox, or sender before backend access
- [x] Unit tests cover allow and deny cases without network/IMAP
- [x] Unconfigured mail yields a clear structured denial

## Implementation Notes

- Today `policy.py` only checks tool names; add argument-level checks for
  mail without breaking `gh_*`
- Prefer deny-by-default for empty mailbox lists
- Keep secrets (IMAP passwords) out of the action log; config may point at
  keyring / env for credentials in the adapter task

## Related

- CIP: 0003

## Progress Updates

### 2026-10-20

Task created (Ready) after CIP-0003 Accepted (IMAP Option A).

### 2026-10-20 (implemented)

Implemented and covered by unit tests.
