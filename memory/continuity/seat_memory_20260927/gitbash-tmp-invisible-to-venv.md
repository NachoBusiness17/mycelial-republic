---
name: gitbash-tmp-invisible-to-venv
description: Git Bash /tmp is invisible to the Windows venv python — write temp
  files to $TEMP (or repo paths) whenever a Bash command pipes into .venv python
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

On this machine, Bash tool commands run in Git Bash where `/tmp` maps to a MSYS path, but `.venv/Scripts/python.exe` is a Windows interpreter that cannot see `/tmp/...`. Any compound command like `cmd > /tmp/out.json && .venv/Scripts/python.exe -c "open('/tmp/out.json')"` fails with FileNotFoundError. Bit three times on 2026-09-14/15 (Zenodo record fetch, shared_surface validate capture, drift-patrol check 4 first attempt).

**How to apply:** Redirect temp files to `"$TEMP"` (Windows-visible env var in Git Bash) or to repo-relative paths, e.g. `... > "$TEMP/ss.json"` then read `os.environ['TEMP'] + '/ss.json'`. Same rule for any helper script: copy to `$TEMP/fold_host.mjs`, not `/tmp/`. Related: [[drift-patrol-cron-a7c71ad1]].
