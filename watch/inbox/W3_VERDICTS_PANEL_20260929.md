# W3 VERDICTS PANEL (2026-09-29)

Mickey17 Wave 3 lane. Pays return 23 of `watch/inbox/MICKEY17_WAVE_LEDGER_20260929.md`: the new estate (gwap/gps/mountain) had no dashboard face (zero grep hits); now every organ joins by appending one source line.

## Files

- `dashboard/server.py` (additive): one door `GET /api/v1/verdicts` + module helpers. The gps sqlite (`tools/gps_mcp/gps_ledger.db3`, the `CapabilityLedger` schema in `tools/gps_mcp/ledger.py`) is opened READ-ONLY via `sqlite3.connect("file:...?mode=ro", uri=True)` and queried `SELECT model_id, task_shape, pass_rate, sample_size, updated_at FROM capability ORDER BY updated_at DESC LIMIT 50`. gwap/mountain are `os.listdir` filename tails (mtime desc, tail 10, no content ever read): `memory/runs/gwap` (the `SessionLedger` STORE) and `watch/inbox/mountain_climb_ractor_20260929`. Missing db/dir degrades to empty, never errors.
- `dashboard/static/verdicts.html` (new): cloned from `links.html` zero-fetch shape (same palette/esc()/bar/err pattern; no CDN, no libraries). gps rows render as a table (model / task shape / pass-rate bar / n / updated) with a filter box; gwap + mountain render filename lists; each panel carries its source line from the door payload. Manual refresh only, no polling (ractor-fossil lesson). Served at `/static/verdicts.html` via the existing static route; the running dashboard process needs a restart to serve the new door.

## Door verification (route function called directly, no server spin-up)

Fixture sqlite built through the organ's own writer (`tools.gps_mcp.ledger.CapabilityLedger.record_verdict`), fixture gwap/mountain dirs with mtimes. `_verdicts_payload(db_path=..., gwap_dir=..., mountain_dir=...)` returned valid JSON (single line, `json.dumps` round-trip clean):

```
FIXTURE_JSON_ONE_LINE={"schema":"verdicts.v1","organs":{"gps":{"source":"tools/gps_mcp/gps_ledger.db3 · capability · sqlite read-only","rows":[{"model_id":"glm-5.3-prime","task_shape":"repo-dig","pass_rate":0.6666666666666666,"sample_size":3,"updated_at":"2026-09-30T00:25:09+00:00"},{"model_id":"qwen3.8-max-prime","task_shape":"judgment","pass_rate":1.0,"sample_size":1,"updated_at":"2026-09-30T00:25:09+00:00"}]},"gwap":{"source":"memory/runs/gwap · newest session ledgers (filenames only)","files":["NEWEST_session.jsonl","mud-demo-20260929.jsonl","b3-demo-clean-20260929.jsonl"]},"mountain":{"source":"watch/inbox/mountain_climb_ractor_20260929 · newest receipts (filenames only)","files":["SYNTHESIS.md","GRADED.md","RECEIPT.md"]}}}
```

Running mean check: 2 pass + 1 fail -> 0.6667 at n=3 matches `record_verdict` math; newest-mtime file heads the gwap tail. Live-estate call: gps rows 0 (`gps_ledger.db3` not yet seeded on disk), gwap 3 session ledgers, mountain 9 receipts listed. `py_compile` clean. Em-dash count in both touched-file additions: 0. No git commit (lane law). Tests not required for a static page (lane spec).
