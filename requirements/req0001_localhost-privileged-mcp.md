---
id: "0001"
title: "Localhost privileged MCP control plane"
status: "Ready"
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

- [ ] A sandboxed agent can call bridle MCP tools on `127.0.0.1` / localhost
- [ ] Bridle executes allowlisted `gh` operations using the user's normal
      keyring credentials (outside the sandbox)
- [ ] Non-allowlisted or free-form shell is rejected
- [ ] Each tool call leaves an accountable record (inputs, decision, result)
- [ ] Lynguine engagement is via adapter to existing lynguine server mode,
      not by embedding MCP in lynguine core (initial scope)

## Out of scope (initial)

- Arbitrary remote MCP exposure
- Full multi-agent DOAgent topologies beyond recording tool actions
- Shipping MCP inside the `lynguine` package itself
