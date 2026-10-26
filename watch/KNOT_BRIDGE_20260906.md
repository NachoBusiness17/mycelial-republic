# KNOT_BRIDGE_20260906 — BATCH5 / S3 (s3-knots)

Scope: find the sanctioned backfill machinery, prove the gap vs the zcode CLI db, dry-run it bounded, file the verdict. NO live chain writes (chain verified 7291 knots before/after — untouched).

## ITEM 1 — The sanctioned tool (exists)

- `python main.py backfill-sessions [--all] [--dry-run] [--llm]` → `mag/records.py:backfill_sessions()` (main.py:442 def, :2590 handler).
- Reads (stream): union of `memory/biography/` artifacts + `~/.grok/sessions/**/chat_history.jsonl` + residual registry (`mag/records.py:list_known_session_ids`, resolver `mag/chat_source.py` — sources `grok` | `mag_agent` ONLY).
- Writes (chain): `summarize_session` → `write_session_pack` → `append_verkle_knot` (mag/session_dossier.py:542, mag/verkle_knot.py:606, file lock + one-leaf-per-session consolidation).
- Sanctioned by lore: docs/DNA.md:100/134 ("OS daily backfill-sessions for crashed sessions"), docs/ref/MAG_LOOP_DISCIPLINE.md:28 ("integrity gaps are batch jobs"), blackboard pin seq 34 (orphan t2fdf11eacc = a routine `[verkle] backfill-sessions --all` run).

## ITEM 2 — Gap analysis (CLI-db coverage)

- Does backfill read the zcode CLI db (`~/.zcode/cli/db/db.sqlite`, 317MB, 354 `sess_*` rows, epoch-ms)? **No — SUPPORTED: coverage missing.** No code path in records.py/chat_source.py touches sqlite or `sess_` ids.
- Dry-run evidence (ran, bounded by mode): **116 holes**, ALL uuid-shaped grok-stream ids (`019fe6f9-…`), ZERO `sess_` ids → resolves W1's "linkage Disputed": the knotter does NOT index the CLI db; it indexes a third stream (grok home + host spore; W1's last-knot id `01a07384` ≈ `active_session.json` `01a073c5`).
- Adapter, not rewrite: `summarize_session()` is already seat-agnostic — accepts `chat_path=` + `source=` for any transcript. Cheapest bridge: export CLI-db sessions into the EXISTING `mag_agent` format (`memory/agent_sessions/<sid>.json`, `{"session_id", "messages":[...]}`) and `list_known_session_ids()` picks them up with zero knotter changes.

### Adapter spec (the build, ~60-100 lines, 1-2h, $0 heuristic mode)

1. `mag/zcode_export.py::export_sessions(db_path, ids|since_ms, out_dir=memory/agent_sessions) -> list[sid]`
   - Open sqlite READ-ONLY (`file:...db.sqlite?mode=ro` — never write the CLI db).
   - Per session row → `{"session_id": id, "title": title, "time_created": epoch_ms, "time_updated": epoch_ms, "messages": [json.loads(m.data) for m in message WHERE session_id=? ORDER BY sequence]}`.
   - Skip already-exported (mtime/`time_updated` guard, same anti-bloat rule as biography.py:415).
2. Field mapping session→knot: `session_id`=sessions.id (keep `sess_` prefix verbatim), start=`time_created` (epoch-ms→ISO), end=`time_updated`, dominant theme=`sessions.title` (`title_source=first_input` — free, no LLM), provider="zcode-cli".
3. First batch = W1's 51 orphans (ended >2h, knotless): top named windows first — `sess_cac6dbfa` (879 msgs), `sess_36090652` (235), `sess_a0843589` (231), `sess_6d789a4e` (192), then batch by prefix `sess_subagent_agent_` older than 2h. Ledger: memory/runs/batch5_20260906/ORPHAN_LEDGER_20260906.md.

## ITEM 3 — Dry-run proof

`python main.py backfill-sessions --dry-run` → `{"ok": true, "n_targets": 116, …}` all missing `[residual, card, content_commit, chain_leaf]`. No knots written: dry-run path `continue`s before `summarize_session` (records.py:192-200); chain verified 7291 lines / tip `08a223a5c7f7` after run — identical to W1's 01:30Z audit. Disclosure: the tool appends one metrics row to `logs/kpi.jsonl` even in dry-run (sanctioned tool behavior; not a chain write).

## ITEM 4 — Verdicts (tri-state)

| Claim | Verdict |
|---|---|
| A sanctioned backfill bridge exists | **Supported** — `backfill-sessions --all`, dry-run + docs + blackboard pin seq 34 |
| It covers the zcode CLI db today | **Disputed→Disproven** — zero `sess_` ids in 116 dry-run targets; grok/mag_agent sources only |
| Closing it is a flag | **Disputed** — it is a small ADAPTER (export CLI db → mag_agent jsonl), not a flag; seams already exist (`chat_path`/`source` params) |
| Effort | ~60-100 lines, 1-2h, $0 (heuristic summary, no LLM); backfill of 51 sessions then rides the existing batch op |

## THE GAP-CLOSER

**BUILD REQUIRED** (small): adapter per spec above, then one command closes everything, forward and backfill:

```
# SUPERSEDED (FW-11 2026-09-28): one-shot 2026-09-06 backfill; mag/zcode_export.py since deleted - do not re-run. Do not re-run from prose. Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
python mag/zcode_export.py --since 24h && python main.py backfill-sessions
```

(For night shift TODAY, the grok-stream half is already closable with `python main.py backfill-sessions` — 116 holes in the stream it does index. The `sess_` half waits on the adapter. Both are OPERATOR-gated live-chain writes; S3 ran dry-run only.)

Receipt: BATCH5|s3|RECEIPT: backfill tool=found backfill-sessions (mag/records.py, main.py:2590), CLI-db coverage=missing (adapter required), dry-run=ran (116 holes, 0 chain writes, tip 08a223a5c7f7/7291 verified), card watch/KNOT_BRIDGE_20260906.md
