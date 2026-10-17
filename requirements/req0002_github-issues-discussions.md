---
id: "0002"
title: "Allowlisted GitHub issues and Discussions via bridle"
status: "Proposed"
priority: "High"
created: "2026-10-17"
last_updated: "2026-10-17"
related_tenets: []
stakeholders: ["Neil D. Lawrence"]
tags: ["mcp", "gh", "issues", "discussions", "graphql"]
---

# Requirement: Allowlisted GitHub issues and Discussions via bridle

## Statement

A sandboxed Cursor agent using bridle must be able to **read, comment on,
close/reopen, and (for Q&A) mark answers on** GitHub **Issues** and
**Discussions** for repositories the user can access — without free-form shell
and without seatbelt CONNECT access to `api.github.com`.

Pull-request tools already exist (`gh_pr_*`). Issues and Discussions are
required for maintainer workflows (e.g. SheffieldML/GPy CIP-0007 trackers and
usage Discussions) that today fall back to unsandboxed `gh api graphql`.

## Acceptance criteria

- [ ] Agent can list and view issues (open/closed) for a given `owner/repo`
- [ ] Agent can comment on an issue; close or reopen with a reason where
      GitHub supports it
- [ ] Agent can list and view Discussions (including category, body, comment
      count, answered state for Q&A)
- [ ] Agent can add a Discussion comment; close a Discussion; optionally mark
      a Q&A comment as the answer
- [ ] Every call is allowlisted by tool name + structured args, policy-checked,
      and recorded in the bridle action log
- [ ] No free-form `gh` / GraphQL string passthrough from the agent

## Out of scope (this requirement)

- Creating new Discussions or Issues (can be a follow-on slice)
- GitHub Projects, Discussions polls admin, or org-level moderation APIs
- Changing CIP-0001 sandbox / localhost transport model
