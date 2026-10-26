# LANE 19 SEAL-HOOK TEST (2026-09-22)

One-shot probe from mining lane 19 [record-health]: this file exists only to
prove that a Write landing under `watch/` triggers the ZCode hook channel
(`C:/Users/foste/.zcode/cli/config.json` → `hooks.events`) and appends exactly
one `op=autoseal` line to `watch/inbox/index_events.jsonl`.

Expected: exactly one line with `"op": "autoseal"`, this path, a sha256
(file < 256 KB), and purpose `autoseal (rib.md.record.v1)`.

This file is disposable; the lane's doc update lives in
`MD_RECORD_STEAL_MAP_20260921.md`.
