---
id: "0003"
title: "Metadata-first least disclosure for privileged adapters"
status: "Implemented"
priority: "Medium"
created: "2026-10-20"
last_updated: "2026-10-20"
related_tenets: ["thin-wrapper-over-existing-tools"]
stakeholders: ["Neil D. Lawrence"]
tags: ["mcp", "privacy", "metadata", "least-disclosure", "readonly"]
---

# Requirement: Metadata-first least disclosure for privileged adapters

## Statement

When bridle exposes personal, account-bound, or third-party records to a
sandboxed agent, the agent must be able to work from **metadata** (who,
when, where, subject/title, identifiers, routing fields, and similar
envelope information) **without** receiving the underlying **content**
(bodies, file bytes, message text, attachment payloads, or equivalent).

Metadata access is allowlisted, read-oriented, policy-checked, and audited.
It must not imply permission to read content, nor to send, reply, create,
delete, or otherwise mutate those records. Returned metadata is treated as
untrusted third-party data.

Content access, if ever offered, is a separate explicit capability — not
the default and not bundled into metadata tools.

## Acceptance criteria

- [x] For at least one privileged adapter domain, the agent can list and
      inspect **metadata only** for user-allowlisted resources
      (mail headers via CIP-0003; unit-tested)
- [x] Metadata tool responses contain no content payloads (no bodies,
      attachment bytes, or full-text fields for the record)
- [x] Resources outside the configured allowlist are denied by policy
- [x] Metadata tools cannot send, create, reply, forward, delete, move,
      or change state of the underlying records
- [x] Every metadata call is allowlisted by tool name + structured args,
      policy-checked, and recorded; the action log does not store content
      payloads for those calls
- [x] No free-form shell or backend command/query string passthrough from
      the agent

## Illustrative domains (not the requirement itself)

| Domain | Metadata (in scope for least disclosure) | Content (out of scope unless a later requirement) |
|--------|-------------------------------------------|---------------------------------------------------|
| Mail | From, To, Cc, Bcc, Subject, Date, Message-ID, mailbox | Body, attachments |
| Files / docs | Path, size, mtime, owner, MIME type | File bytes / extracted text |
| Calendar | Time, attendees, title, location | Description / notes body |
| Chat / issues | Author, timestamp, title, labels, ids | Comment/body text |

The first validating implementation is mail headers via CIP-0003. Other
rows are examples of the same privacy outcome, not commitments in this
requirement.

## Out of scope (this requirement)

- Mandating content readers for any domain
- Defining a specific mail, file, or calendar backend
- Changing CIP-0001 sandbox / localhost transport model
- Replacing OS privacy grants (e.g. macOS TCC); bridle policy remains the
  product boundary even when the OS grant is coarser

## Why this matters

Agents often need triage and routing context. Full content multiplies
privacy risk and prompt-injection surface. Least disclosure — metadata
first, content only when separately justified — keeps bridle usable
without turning every adapter into a full data dump.

Informed by **thin-wrapper-over-existing-tools**: prefer existing backends
that can fetch envelope/metadata cleanly, wrapped by bridle policy, rather
than reinventing stores or exposing a vendor MCP’s full catalog.

## Progress Updates

### 2026-10-20
Rewrote from mail-headers-specific draft to a cross-adapter privacy
requirement (metadata vs content). Mail remains the first CIP application.

### 2026-10-20 (later)
Status → Ready. CIP-0003 Accepted with IMAP (Option A) as the mail
backend; backlog breakdown follows.

### 2026-10-20 (backlog)
Status → In Progress. CIP-0003 In Progress; five backlog tasks created.

### 2026-10-20 (implemented)
Status → Implemented. Mail metadata tools shipped with mocked tests.
Awaiting live IMAP smoke before Validated / CIP Closed.
