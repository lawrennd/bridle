# Bridle

Local MCP control plane for Cursor agents: allowlisted privileged adapters
(starting with `gh`), DOAgent-backed action records, and optional lynguine
server adapters — without opening the agent seatbelt sandbox to the public
internet.

Design decisions live in [CIP-0001](cip/cip0001.md) and
[REQ-0001](requirements/req0001_localhost-privileged-mcp.md).

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

Add to Cursor MCP settings (user or project). Prefer an absolute path and
the project venv so the server runs outside the agent seatbelt with your
normal credentials available to child processes:

```json
{
  "mcpServers": {
    "bridle": {
      "command": "/Users/neil/lawrennd/bridle/.venv/bin/bridle",
      "args": []
    }
  }
}
```

Or via module:

```json
{
  "mcpServers": {
    "bridle": {
      "command": "/Users/neil/lawrennd/bridle/.venv/bin/python",
      "args": ["-m", "bridle"]
    }
  }
}
```

After reload, the agent should see a `ping` tool. Call it to confirm bridle
is reachable (`ok: true`, `service: bridle`).

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

Optional: set `BRIDLE_GH_BIN` to an absolute `gh` path.

Action log (JSONL, schema `bridle.action/v0`) defaults to
`~/.bridle/actions.jsonl`. Override with `BRIDLE_ACTION_LOG`.

## Status

- [x] MCP skeleton + `ping` (CIP-0001 backlog)
- [x] Allowlisted `gh` adapter + policy
- [x] Action log / DOAgent-compatible records
- [ ] Hardening (confirm, tests, failure docs)
