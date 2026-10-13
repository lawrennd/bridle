---
id: "0001"
title: "Localhost privileged MCP control plane"
status: "In Progress"
priority: "High"
created: "2026-10-13"
last_updated: "2026-10-13"
related_tenets: []
stakeholders: ["Neil D. Lawrence"]
tags: ["mcp", "sandbox", "gh", "doagent", "lynguine"]
---

# Requirement: Localhost privileged MCP control plane

## Statement

Cursor agents running under seatbelt sandbox must be able to perform
allowlisted privileged operations (starting with GitHub `gh`) **without**
disabling the sandbox or exposing agent traffic to `api.github.com` through
the sandbox CONNECT proxy.

Those operations run in a user-controlled process on localhost. Every
invocation is policy-checked and recorded for audit.

## Acceptance criteria

- [x] A sandboxed agent can call bridle MCP tools on `127.0.0.1` / localhost
      (verified 2026-10-13 via Cursor MCP `ping`)
- [x] Bridle executes allowlisted `gh` operations using the user's normal
      keyring credentials (outside the sandbox)
      (verified 2026-10-13 via `gh_pr_list` on `lawrennd/mlai`)
- [x] Non-allowlisted or free-form shell is rejected
      (unit-tested `PolicyDenied`; no shell passthrough tools exposed)
- [x] Each tool call leaves an accountable record (inputs, decision, result)
      (verified 2026-10-13 in `~/.bridle/actions.jsonl`, `bridle.action/v0`)
- [ ] Lynguine engagement is via adapter to existing lynguine server mode,
      not by embedding MCP in lynguine core (initial scope)

## Out of scope (initial)

- Arbitrary remote MCP exposure
- Full multi-agent DOAgent topologies beyond recording tool actions
- Shipping MCP inside the `lynguine` package itself
