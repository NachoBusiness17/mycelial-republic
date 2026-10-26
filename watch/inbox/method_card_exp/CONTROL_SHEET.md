# CONTROL SHEET — estate facts, local_sovereign_agent

Twelve reference facts for the estate at `C:/Users/foste/Documents/projects/local_sovereign_agent`.
Every number below was read from an estate file or counted with a command run in-session
on 2026-09-24. Each fact ends with the exact way to re-verify it.

---

**1. The binding constitution is a pointer, not a local file.**
`CONSTITUTION.md:3-5` says the real constitution lives at
`../mycelial-republic/docs/CONSTITUTION.md`, and lines 7-13 name five laws this
instrument must obey: fork equality (no rank/token); data tiers T0-T3 (T0/T1 never
to free remote train-on-input APIs); Handoff.v1 contracts for escalation;
append-only router audit log; mining proposals never auto-merge. If that file is
missing, the rule is: stop and restore it before any public claims. (Note the
fifth law in action at `state/CURRENT.md:12-13`: a commit was blocked by the
Mimosa gate and the operator had to rule it "code-as-law" before it landed.)
Re-verify: `sed -n '1,15p' CONSTITUTION.md`

**2. CURRENT has a built-in freshness meter (48h self-expiry).**
`state/CURRENT.md:3-6` — if the `updated:` date is more than 48h old when read at
boot, the file "is lying" and must be refreshed from the memory index before
trusting anything in it. The current `updated:` stamp is 2026-09-24
(`state/CURRENT.md:8`), so it is live today. The 09-24 status it records
(`state/CURRENT.md:9-17`): the daily KeyAudit had been failing every morning by
construction (CLI seats counted as missing keys; orphan scan was dead code);
fixed to 32/32 keys declared, audit green, landed as commit **3ee362d04**;
Discord+Hermes (Mag bot) verified live with Adam (ItsCommodore) actively
using it, session running since 09-21.
Re-verify: `sed -n '1,10p' state/CURRENT.md`

**3. The memory index is the state of record, with a fixed boot order.**
`state/CURRENT.md:18-20` declares the memory index as canonical state; on disk
that is `memory/MEMORY.md` (491 lines, newest-first). The map for any "where is X"
question (`state/CURRENT.md:26-30`): memory/MEMORY.md (what things mean) →
`watch/ESTATE_ATLAS/ATLAS.md` (what exists) → grep
`watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` (the exact file). "No luck involved."
Re-verify: `wc -l memory/MEMORY.md`

**4. The estate index is ~1.2 million rows — CURRENT's "1.7M" claim is stale.**
`wc -l watch/ESTATE_INDEX/ESTATE_INDEX.jsonl` → **1,207,962 rows** (ran this
session). `state/CURRENT.md:30` still advertises "the exact file, 1.7M rows";
trust the counted number, not the prose.
Re-verify: `wc -l watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`

**5. 94% of the estate is frozen sediment.**
`watch/ESTATE_ATLAS/ATLAS.md` (generated 2026-09-23T11:52:37Z) counts
1,199,877 files / 65.37 GB under Documents/projects. Of those, **1,132,147 files
(94%) are COLD+FROZEN sediment**; the live organ total is 114,243 files; the
HOT+WARM working set is 67,730 files. Largest live organs: memory/runs/ 46,436
files (1.13 GB) and memory/biography/ 44,172 files (0.37 GB). Other organ rows
in the same table: watch/ 16,279 files (5.76 GB), dashboard/ 581 (3.63 GB),
state/ 2,698 (0.04 GB), mag/ 2,178 (0.03 GB), docs/ 528, tests/ 285,
scripts/ 219, tools/ 132, queue/ 735.
Re-verify: `sed -n '1,40p' watch/ESTATE_ATLAS/ATLAS.md`

**6. The biggest append-only sink is Mimosa hook-state.**
Per the ATLAS.md sink table: `.mimosa/hook-state/` holds **522,324 files /
7.23 GB** — bigger than `mine/raw/` (103,033 files / 5.73 GB) and
`memory/biography_backup/` (33,530 files). Sinks are "capped by rule, never
hand-weeded"; the hook-state owner is the Mimosa lane.
Re-verify: `grep -n "mimosa" watch/ESTATE_ATLAS/ATLAS.md`

**7. The canon manifest verified green this morning.**
`CORPUS_CATALOG.md:5` — run at 2026-09-24T13:15:09: **"CANON MANIFEST: VERIFIED
(205 hashes match)"**. The canon shelf holds 208 files / 20.5 MB
(`CORPUS_CATALOG.md:11`), spanning 2026-09-05 to 2026-09-23.
Re-verify: `sed -n '1,12p' CORPUS_CATALOG.md`

**8. Corpus bulk: oral history + library dwarf everything else.**
`CORPUS_CATALOG.md:15` — oral_history shelf: **15,747 files / 1,423.9 MB**.
`CORPUS_CATALOG.md:18` — library shelf: **45,794 files / 5,445.5 MB**. The
catalog ledgers are append-only: `state/library/catalog.jsonl` +
`catalog_runs.jsonl` — "The Librarian records; it never cleans"
(`CORPUS_CATALOG.md:32`).
Re-verify: `sed -n '9,32p' CORPUS_CATALOG.md`

**9. The meters: readings file + five meter programs.**
`watch/meter_readings.jsonl` has exactly **16 rows** (wc -l, this session); its
last `daily_rollup` is ts 2026-09-01T11:05:27Z, grading "MEASURED", with
cron_fleet = 1 standing job (m0_meter_daily), 0 errors, 0 down. Its own note
line names the 24h cost driver: "deepseek off-peak cache-mine (est $0.017...
~87 probes @100% hit-rate). No active subagents this window; $0 lane holds."
Meter code
lives at `tools/meters_nightly.py`, `tools/thrash_meter.py` (11,933 bytes),
`mag/divergence_meter.py`, `mag/honest_cache_meter.py`,
`mag/vertical_meter.py`, `scripts/usage_meter_sweep.py`.
Re-verify: `wc -l watch/meter_readings.jsonl && tail -2 watch/meter_readings.jsonl`

**10. Hard rails are deterministic — evaluated with NO LLM.**
`configs/constitutional_rails.json` (as_of 2026-08-03) is enforced at preflight
by `agent_cli._preflight_tool` (see `mag/rails.py`, per the file's own note,
line 4). Two rules: `no_live_secret_values` — a regex blocks sk-… key values and
api_key assignments written into any artifact (line 9); `no_residual_dna` —
blocks writes to `.env`, `verkle_tip.json`, `verkle_chain.jsonl`, `/knots/`,
`quota_state.json` (line 17).
Re-verify: `cat configs/constitutional_rails.json`

**11. The fleet runs 8 containers, all bound to localhost.**
`docker-compose.yml` defines 8 `container_name` entries: mag-sovereign (ports
`127.0.0.1:8765` + `127.0.0.1:8000`), mag-redis (:6379), mag-ollama (:11434),
mag-browser (:9222 CDP), mag-openclaw-tailscale, mag-openclaw,
mag-openclaw-cloudflared, mag-worker (lines 15, 67, 91, 121, 155, 194, 237,
263). Every published port maps to 127.0.0.1.
Re-verify: `grep -n "container_name\|127.0.0.1" docker-compose.yml`

**12. Codebase shape: one 5.4K-line main, a 1,005-file fleet organ, 278 test files.**
`main.py` = **5,371 lines** / 233,762 bytes (wc -l). `mag/` holds **1,005 .py
files** (ls | wc). `tests/` has 278 entries; `pytest.ini` sets
`testpaths = tests` and `addopts = -ra -p no:cacheprovider`. `requirements.txt`
pins 14 deps (langgraph, langchain-ollama, fastapi, faster-whisper, textarena,
chess, ...). Git HEAD: c63a4df74 "plan: cooker hourly row + claritas faces
section" (git log -1, this session). The next commit down, 86628c678, wires the
cooker burner: "hourly fire --due catches every pool refill... never auto-rearm".
One more recent trunk fact from `git log`: d972d0308 — "DeepSeek-V3 retired...
serverless endpoint now zombie-503s (not 404; masquerades as transient); lanes
repointed to DeepSeek-V4-Flash-0731 (live-tested 849ms)".
Re-verify: `wc -l main.py && ls mag/*.py | wc -l && ls tests | wc -l && git log --oneline -1`

---

*Sheet written by the control-builder run of 2026-09-24. Facts 4, 9, 12 counted
live; all others read verbatim from the cited paths.*
