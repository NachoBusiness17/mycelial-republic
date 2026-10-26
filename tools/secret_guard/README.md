# secret_guard (2026-10-23)

Code-level layer for the standing rule "just don't touch secrets". Policy: `configs/secrets_policy.yaml`.
Audit: `state/secret_guard/audit.jsonl` (append-only, sha256[:8] only, never values).

* `tools.secret_guard.load_secret(path, name)`: the only sanctioned way for repo code to load a secret. The value stays in-process.
* `export_secret`: always refuses. The CLI has no `get` or `export` subcommand on purpose.
* `request_transfer`: needs a real TTY on stdin and stdout, no agent env marker, and a fresh 6-hex nonce typed back. Anything else is denied.
* `tools/safe_ssh.py`: wraps ssh/scp/sftp/rsync/adb. It scans argv, stdin and local source files against in-memory secret values and blocks on a hit.
* Hook: with `MAG_SECRET_GUARD=1`, `install_hook()` blocks open()/os.open of policy paths and the launch of egress commands outside safe_ssh.
  The repo's own `tools/bob_bridge.py` and `tools/gstd_drain.py` call `ssh` directly, so under the hook they get blocked until they are ported to `safe_ssh.run`.

## PowerShell note (profile-agnostic)
Set the guard per session so it does not depend on any profile:
`$env:MAG_SECRET_GUARD = "1"`. Python only honours it after the hook is loaded, either from an entrypoint
that calls `install_hook()` or from the proposed venv sitecustomize (`sitecustomize_snippet.py`, NOT installed).
PowerShell itself (`Get-Content .env`, `ssh`) is not covered. See the limits below.

## What this cannot stop
Any agent with a raw shell, any other interpreter, or `python -I`/`-S` bypasses an in-repo guard. Real enforcement has to happen at the OS level (see the decisions in the incident report).
