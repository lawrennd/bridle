# Bridle

Local MCP control plane for Cursor agents: allowlisted privileged adapters
(starting with `gh`), DOAgent-backed action records, and optional lynguine
server adapters — without opening the agent seatbelt sandbox to the public
internet.

Design decisions live in [CIP-0001](cip/cip0001.md),
[REQ-0001](requirements/req0001_localhost-privileged-mcp.md), and
mail metadata least-disclosure in [CIP-0003](cip/cip0003.md) /
[REQ-0003](requirements/req0003_metadata-least-disclosure.md).

## Why

Cursor agent shells under seatbelt often cannot reach `api.github.com`
(CONNECT proxy 403). `gh` then misreports that as an invalid token. Bridle
runs as a normal (unsandboxed) MCP process that Cursor launches; the agent
only speaks MCP, while bridle holds the privileged adapters.

## Install (development)

```bash
cd ~/lawrennd/bridle
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Smoke test (no MCP wire protocol):

```bash
pytest -q
bridle  # blocks on stdio — use from Cursor MCP, or see HTTP below
```

## Cursor MCP config

Bridle is wired for Cursor in two places (stdio; Cursor launches the
process outside the agent seatbelt):

| Scope | File |
|-------|------|
| Global (all workspaces) | `~/.cursor/mcp.json` |
| This repo | `.cursor/mcp.json` |

Both point at the project venv’s `bridle` console script. After editing,
reload Cursor (**Developer: Reload Window**) or toggle the server under
**Cursor Settings → Tools & MCP**, then call `ping`.

Equivalent manual config:

```json
{
  "mcpServers": {
    "bridle": {
      "command": "${userHome}/lawrennd/bridle/.venv/bin/bridle",
      "args": [],
      "env": {
        "BRIDLE_TRANSPORT": "stdio"
      }
    }
  }
}
```

Or via module: `"command": "…/.venv/bin/python"`, `"args": ["-m", "bridle"]`.

## Optional: Streamable HTTP on localhost

For probing without Cursor (still bind localhost only):

```bash
BRIDLE_TRANSPORT=streamable-http BRIDLE_HOST=127.0.0.1 BRIDLE_PORT=8766 bridle
```

Default Cursor integration uses **stdio** (leave `BRIDLE_TRANSPORT` unset).

## Allowlisted tools (v0)

| Tool | Purpose |
|------|---------|
| `ping` | Health check |
| `gh_pr_view` | `gh pr view --repo … --json …` |
| `gh_pr_list` | `gh pr list --repo …` |
| `gh_pr_create` | `gh pr create --repo …` (mutating) |
| `mail_account_list` | Allowlisted mail account labels from config |
| `mail_header_list` | Recent **headers only** (IMAP `EXAMINE` + `BODY.PEEK[HEADER]`) |
| `mail_header_view` | One message’s headers by opaque id |

Optional: set `BRIDLE_GH_BIN` to an absolute `gh` path.

Action log (JSONL, schema `bridle.action/v0`) defaults to
`~/.bridle/actions.jsonl`. Override with `BRIDLE_ACTION_LOG`.

### Mail metadata (CIP-0003)

Headers only — no bodies, attachments, or send/mutate tools. Bridle enforces
account/mailbox (and optional sender) allowlists in config; returned fields
are untrusted third-party data.

Config file: `~/.bridle/mail.toml` (or `BRIDLE_MAIL_CONFIG`). Example:

```toml
[[accounts]]
id = "work"
host = "imap.example.com"
port = 993
username = "you@example.com"
password_env = "BRIDLE_MAIL_PASS_WORK"
allowed_mailboxes = ["INBOX"]
allowed_from = ["*@example.com"]   # optional; empty = any sender in mailbox
max_list = 50
```

Set the password via the named env var (never in the TOML). After adding
tools, reload Cursor MCP so schemas refresh.

## Status

- [x] MCP skeleton + `ping` (CIP-0001 backlog)
- [x] Allowlisted `gh` adapter + policy
- [x] Action log / DOAgent-compatible records
- [ ] Hardening (confirm, tests, failure docs)
- [x] Issues + Discussions adapters — [CIP-0002](cip/cip0002.md)
- [x] Mail header metadata (IMAP) — [CIP-0003](cip/cip0003.md) (In Progress)
