---
id: "thin-wrapper-over-existing-tools"
title: "Thin wrapper over existing tools"
status: "Active"
created: "2026-10-20"
last_reviewed: "2026-10-20"
review_frequency: "Annual"
conflicts_with: []
tags:
- tenet
- adapters
- reuse
---

# Thin wrapper over existing tools

## Tenet

**Description**: Bridle is a control plane, not a reimplementation of every
host capability. Prefer wrapping tools the user already trusts and maintains
(`gh`, system `osascript` only when unavoidable, established IMAP/OAuth
clients, existing CLI or library adapters) behind allowlisted MCP tools,
policy, and the action log. Invent new protocol clients or duplicate mature
MCP servers only when no suitable tool exists, or when wrapping would break
the privacy and audit constraints that justify bridle.

**Quote**: *"Bridge, do not rebuild."*

**Examples**:
- GitHub access goes through the user's `gh` CLI and keyring, not a bespoke
  REST client inside bridle.
- Mail headers, if exposed, should prefer an existing read-only mail stack
  (IMAP `EXAMINE` / `BODY.PEEK`, or a focused library) wrapped by bridle
  policy — not a ground-up mail store.
- Fixed GraphQL documents inside bridle for Discussions still *call* `gh`;
  the agent never authors queries.

**Counter-examples**:
- Reimplementing GitHub's API surface in Python "because MCP needs it."
- Shipping a full Mail.app clone or free-form AppleScript interpreter.
- Bundling an unrelated third-party email MCP wholesale without a policy
  and audit boundary (bridle would stop being the control plane).

**Conflicts**:
- Completeness vs reuse: an existing tool may expose bodies, send, or
  mutation we must not offer.
  Resolution: wrap narrowly (subset of capabilities) or choose a different
  backend; do not widen bridle's MCP surface to match the upstream tool.
- Offline Mail.app convenience vs coarse macOS Automation grants.
  Resolution: document the TCC trade-off in the CIP; prefer backends with
  finer auth when privacy requirements demand it.
