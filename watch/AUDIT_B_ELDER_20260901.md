# AUDIT LANE B — Elder (deterministic organ audit)

Scope: extract what the elder has already ruled; prepare a fresh elder run for the new fleet structure.
Bounded, evidence-only. Every claim cites `path:line`. `UNKNOWN` stays UNKNOWN.
2026-09-01 02:27Z

---

## 1. Last verdict + every receipt

**Last verdict (current audit.json)** — `/mag/memory/runs/elder/audit.json`
- ts `2026-08-31T04:55:13.288811Z`, `ok:true`, schema `elder.audit.v1`
- organ_summary (audit.json, "organ_summary"): DECLARED 27, INSTRUMENTED 26, WIRED 27, STATEFUL 25, VERIFIED 27, LIVE 17, GHOST **0**
- `gap_count: 0` — zero gaps / clean bill of health at last run
- law (audit.json): `"contradictions resolve by evidence and hierarchy, not vote"`

**Receipts (19)** — `/mag/memory/runs/elder/receipts.jsonl`, each `{schema,ts,ok,gap_count,path}`:

| # | ts (2026-08-31Z) | gap_count |
|---|---|---|
| 1 | 02:00:44 | 1 |
| 2 | 02:01:21 | 1 |
| 3 | 02:09:12 | 1 |
| 4 | 02:26:21 | 0 |
| 5 | 04:24:29 | 0 |
| 6 | 04:27:22 | 7 |
| 7 | 04:27:46 | 7 |
| 8 | 04:29:20 | 6 |
| 9 | 04:32:27 | 7 |
| 10 | 04:38:48 | 7 |
| 11 | 04:39:26 | 6 |
| 12 | 04:42:54 | 5 |
| 13 | 04:43:18 | 5 |
| 14 | 04:43:52 | 5 |
| 15 | 04:47:36 | 4 |
| 16 | 04:51:41 | 3 |
| 17 | 04:52:07 | 4 |
| 18 | 04:54:37 | 0 |
| 19 | 04:55:13 | 0 |

Trajectory: gaps spiked to 7 around 04:27 (mid-day churn), then were worked down to 0 by 04:55. Final two receipts clean. Receipts carry gap_count + path only — **no per-organ detail**; the current audit.json itself is the only source of the summary/resolved verdict.

---

## 2. What elder.py actually audits

**Inputs (reads from disk, all via organ_map REGISTRY):**
- `elder.py:26-30` — ROOT=/mag; OUT_DIR=`/mag/memory/runs/elder`; REPORT=`audit.json`; RECEIPTS=`receipts.jsonl`
- `elder.py:32-43` — `audit()` calls `from .organ_map import map_organs` (import at elder.py:33). **elder has NO inputs of its own** — it delegates entirely to `organ_map.map_organs()`.
- `organ_map.py:46` — `REGISTRY: tuple[dict,…]` is a **hardcoded Python registry** of organs. Each entry declares `source`, optionally `module`/`callable`, `wired_by`, `state_paths`, `proof`, `receipt_paths`.
- `organ_map.py:355-358` — `_path()` resolves relative paths against ROOT (=`/mag`, organ_map.py:30-34 pull `config.ROOT` first, else `Path(__file__).parent.parent`).
- Per organ, `map_organs()` (organ_map.py:389+) checks: source file exists → DECLARED; callable imports (`_importable`) → INSTRUMENTED; wired_by paths exist → WIRED; state_paths exist → STATEFUL; proof passes (`_proof`) → VERIFIED; recent+ok receipt → LIVE; else GHOST. Builds `gap_codes` (source_missing / callable_missing / caller_missing / caller_undeclared / state_missing / proof_failed / receipt_missing / receipt_not_successful / receipt_stale).

**Rules (deterministic, no LLM/network — organ_map.py:16-18):**
- `elder.py:33-39` — sorts gaps so structural gaps (source/callable/caller/state) sort first; stale receipts are "useful follow-up" but never hide an orphan.
- `elder.py:40-42` — `next_action(row)` maps each gap code to a concrete recommended repair.
- law in each result (elder.py:50): `"contradictions resolve by evidence and hierarchy, not vote"`.

**Output shape (audit.json, elder.py:44-51):**
- `{ok, schema:"elder.audit.v1", ts, organ_summary:{DECLARED…GHOST}, gaps:[{id,status,codes,next,callable_error}], gap_count, law}`.
- Writes audit.json (elder.py:45-46) and **appends** one line to receipts.jsonl (elder.py:47-49).

**CLI (elder.py:52-58):** `main()` runs `argparse.ArgumentParser(prog="mag.elder").parse_args(argv)` — **takes no positional args, no flags, no subcommands, no scope**. `UNKNOWN`: there is no way to point elder at a board file via CLI.

---

## 3. Sibling organs (roles, one line each)

- **atlas.py** — `build()` (atlas.py:38) + `operational_graph()` compile the organ inventory + topology into a durable `memory/runs/atlas/atlas.json`; CLI `build --scope` / `status` (atlas.py:70-85). Atlas = the generated **map** artifact.
- **basecamp.py** — `status(goal)` (basecamp.py:32) reads that atlas summary, ranks gaps, and picks ONE bounded next climb step (ghost → gap → observe); CLI takes an optional goal string (basecamp.py:86-93). Basecamp = the **one-step climb** controller.

They are siblings because atlas consumes `map_organs()` (atlas.py:49-50) and basecamp consumes `atlas.build()` (basecamp.py:40-43) — same registry, same ROOT, same hardcoded input source as elder.

---

## 4. Fresh elder run for the NEW fleet structure — command + patch plan

**Constraint:** elder (and atlas/basecamp) audit ONLY what `organ_map.REGISTRY` (organ_map.py:46) declares, resolved against ROOT=`/mag`. The new structure is
- `/board/FLEET_STRUCTURE_20260901.md` (board file, `ls /board` shows it; 2913 bytes, ts 01:54Z)
- `/board/LANE_SLOT_MAP_20260901.md` (board file; 2510 bytes, ts 01:34Z)

**Neither lives under `/mag/` nor appears in REGISTRY → elder currently CANNOT see them.** `UNKNOWN` stands for whether any future registry entry will reference them. To let the elder audit them, they must become organs/evidence in the registry.

**Patch plan (via /patches JSON — apply to `/mag/mag/organ_map.py`):**
Append one or more entries to `REGISTRY` (after organ_map.py:46), e.g. for each lane/slot target, declaring source/state/receipt paths **that must be resolvable under /mag**. Concretely, the board files would need to be mirrored under `/mag` (e.g. `mag/fleet_structure.py` stub + `memory/runs/fleet/lane_slot_map.md`), OR the registry entry must point `<pattern>` — but since `_path` only resolves against `/mag` (organ_map.py:355, 30-34), `/board/...` cannot be referenced directly unless a symlink/hardlink to `/mag/board/...` is created. Recommendation: place copies at `/mag/board/FLEET_STRUCTURE_20260901.md` + `/mag/board/LANE_SLOT_MAP_20260901.md` and add registry entries.

**Ready-to-run host-side command sequence:**
```bash
# SUPERSEDED (FW-11 2026-09-28): one-shot elder-audit staging, executed 2026-09-01, receipt filed. Do not re-run from prose. Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
# 0) Stage new-structure evidence under /mag so elder's ROOT-resolved paths see it
mkdir -p /mag/board
cp /board/FLEET_STRUCTURE_20260901.md /mag/board/
cp /board/LANE_SLOT_MAP_20260901.md /mag/board/

# 1) (patch) add registry entries in /mag/mag/organ_map.py REGISTRY for the two lane/slot
#    docs, e.g. source:"board/FLEET_STRUCTURE_20260901.md", state_paths:[...], receipt_paths:[...]
# 2) regen the map so elder sees the new organs
cd /mag && python -m mag.organ_map snapshot
# 3) fresh elder run (writes audit.json + appends receipt)
cd /mag && python -m mag.elder
# 4) sibling refresh
cd /mag && python -m mag.atlas build --scope operational
cd /mag && python -m mag.basecamp "map the climb"
```
Post-run verify: `cat /mag/memory/runs/elder/audit.json` (check organ_summary now includes new lane organs) and tail of `receipts.jsonl`.

**Important caveat:** elder/adts are NOT a doc-reader — they are registry-evidence auditors. Adding the two board files as new organs makes them auditable, but elder reports on their evidence-files (source/state/receipt availability), **not** on the semantic content of the lane doctrine in LANE_SLOT_MAP. If the goal is to auditor-verify the *structure doctrine itself*, a board-doc review organ (or registry evidence) must be defined explicitly.

---

## Verdict summary
- Elder's last verdict: **0 gaps, clean** at `2026-08-31T04:55:13Z` (27 organs, 0 GHOST, 17 LIVE).
- What it checks: hardcoded REGISTRY organs' source/download/receipt/proof evidence (deterministic, no LLM) → status ladder + gap codes.
- Fresh run to audit `/board/FLEET_STRUCTURE_20260901.md` + `/board/LANE_SLOT_MAP_20260901.md` requires: staging copies under `/mag/board/` **and** adding REGISTRY entries in `organ_map.py`, then `python -m mag.elder` (no CLI args exist to pass a board file).
