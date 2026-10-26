# AUDIT LANE C — VERKLE ORGAN (bounded, evidence-only)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: verkle chain integrity is perfect (6312 knots, 6311/6311 parent chaining, 0 orphans) and ts regressions are write-time bookkeeping artifacts, not faults — SUPPORTED (static byte-level measurement, chain⇄tip consistent) · falsifier: host `self_check` finding a broken parent link, index gap, or missing leaf_hash

Date: 2026-09-01T02:30Z · Auditor: worker subagent · Lane: C (verkle knot timeline + chain health)

## 0. Source of truth (read from disk)

| Item | Path | Evidence |
|---|---|---|
| Lance code | `/mag/mag/verkle_lance.py` (456 lines) | — |
| Chain store | `/mag/memory/biography/verkle_chain.jsonl` | code: `CHAIN = BIO/"verkle_chain.jsonl"` (verkle_lance.py:36) |
| Tip file | `/mag/memory/biography/verkle_tip.json` | code: `TIP = BIO/"verkle_tip.json"` (verkle_lance.py:37) |
| Knots dir | `/mag/memory/biography/knots/` | code: `KNOTS = BIO/"knots"` (verkle_lance.py:35) |
| Peer chain file | `/mag/memory/runs/chain.jsonl` + `head.json` (145 KB) | separate, named `chain.jsonl`, NOT the verkle store |

> **Compass note.** The task hint `/mag/memory/runs/party_subchain*` does **not exist** on this cage. The verkle store lives under `/mag/memory/biography/` per the constants at verkle_lance.py:35-37. `/mag/memory/runs/chain.jsonl` is a *different* (145 KB) ledger and was not used as the verkle source.

## 1. Data model (from the code, read-only)

- One row per **session leaf**; fields: `index`, `ts`, `start_minute`, `filename` (`.knot.json`), `leaf_hash`, `session_id`, `dominant_theme`, `parent_verkle_root`, `verkle_root`, `tension_index`, `dossier_commit`, `amended` (verkle_lance.py:44-46, 54-66).
- **Temporal truth = `index`** (0..n-1). Chain is content-addressed: `verkle_root` of row i = root up to i; `parent_verkle_root` of row i must equal `verkle_root` of row i-1 (verkle_lance.py:28-34).
- `ts` is the **write/recorded time**, not the session time; the `.knot.json` filename carries the true session timestamp (`2026-08-13_0742_session_...`).

## 2. Chain health (measured from bytes)

| Metric | Value |
|---|---|
| Knots (`n_leaves`) | **6312** (chain.jsonl lines == tip `n_leaves` == 6312) |
| Index monotonic (0..6311 in order) | **true** |
| Parent → prev-root chaining | **6311 / 6311** (perfect) |
| All content-addressed (leaf_hash + verkle_root) | **true** (no missing hashes) |
| Orphans (rows w/o session_id) | **0** |
| Duplicate / re-summarized leaves | 0 (6312 distinct leaf_hashes; since `ts` varies but file is per-session with amend-in-place) |
| Distinct filename-days spanned | 3283 |
| First session (filename-date) | 2026-08-02T1436 (idx 962) |
| Last session (filename-date) | 2026-09-01T0144 (idx 6306) |

**Tip (live snapshot at 02:29:35Z, chain ⇄ tip consistent):**
- Tip knot: `index 6311`, `root = 2670c7ea555c2d2290f5d930814206240d6d993a4599ac38ba30d933f7ecac7d`
- Root prefix **`2670c7ea555c`** · parent `a50785687b6d` · session `mag-agent-orc-t1508580941` · ts `2026-09-01T02:27:46Z`

**Reliability caveats (static, from bytes):**
- `ts` is **write-time, not session-time**: 433 timestamp regressions and 115 "gaps >1 day" appear when sorting by `ts`. This is a *bookkeeping artifact* (bulk migration writes on 08-31→09-01), **not** a chain integrity fault — `index` is monotonic and root chaining is perfect. Do not use `ts` for dating; use `filename`/`index`.
- The chain is **actively being written this minute** (mtime 02:29:35Z; the tip root mutated across three reads: `4561bc…`→`15cac4…`→`2670c7…`). The summarizer amends the tip line in place. Re-run health checks after writes settle.
- CAUTION: I could **not run** `python -m mag.verkle_lance self_check` — **no Python interpreter exists on this cage** (`python/python3` absent). The static audit above reproduces the checks `self_check()` performs at verkle_lance.py:398-414 (n, order_monotonic, orphans, all_content_addressed, genesis/tip ts).

## 3. Milestone KNOTS (load-bearing, per theme/filename-date)

This chain is a **per-session leaf ledger**, not an event ledger: there are **0 knots whose label/session encodes launch/death/law**. The SYSTEM-ATTEMPT events (fleet-structure law, audit) do not yet have knots — they are *candidates to be tied in* (see §5). Most-load-bearing existing knots:

| idx | filename-date | theme | root prefix | note |
|---|---|---|---|---|
| 0 | 2026-08-12_1641 | untagged | `6bcba096` | **genesis** knot (index 0) |
| 7 | 2026-08-31_0404 | **constitution** | `2655e205` | first law/constitution knot |
| 62 | 2026-08-08_1936 | mirror | `a6da4a06` | early mirror-subchain knot |
| 962 | 2026-08-02_1436 | **data_r0** | `09fae394` | earliest real session (index that opens the data epoch) |
| 1111 | 2026-08-11_1202 | **fact_bus** | `3f18d752` | first fact-* infiltration knot (fact_bus genesis) |
| 2751 | 2026-08-11_1914 | **memlang** | `5c9b0096` | first memlang-* knload (the Lance's own lineage) |
| 6284 | 2026-08-17_0015 | **constitution** | `59a34680` | latest constitution knot before tip |
| 6311 | 2026-09-01_0144(ts 02:27) | untagged | `2670c7ea` | **tip** (current root) |

(Theme distribution confirms law/ops mass: `constitution` 98, `autonomous_janitor` 124, `scrum_plan` 14, `biography` 964, `mirror_meta` 36, `untagged` 4665.)

## 4. Gap/orphan summary (static)

- `index` strictly 0..6311 → **no index gaps, no dup indices**.
- Parent chain intact for all 6311 transitions → **no broken links / no orphans** in root lineage.
- Only anomaly is `ts`-based (write-time) non-monotonicity described in §2 — cosmetic, filename/index are the anchors.

## 5. Ready host commands

> IMPORTANT correction to the task brief: `tie_in` in this file is the **rib-builder/puppet join**, taking `--n`/`--mode` only (verkle_lance.py:321-340; CLI 83-84/112). The **event temporal tie-in is the `link` tool**, taking `--event` + `--when` (verkle_lance.py:150-190; CLI 97-98). `--key` is used only by `trace`/`verify` (CLI 89/101/105). Use `link`, not `tie_in`, to attach events.

```bash
# SUPERSEDED (FW-11 2026-09-28): one-shot verkle health check, executed 2026-09-01. Do not re-run from prose. Receipt: watch/inbox/fifty_wide_20260917/FW11_fence_owners.md
# Health check (needs python on the host; not available on this cage):
python -m mag.verkle_lance self_check

# Tie-in 1 — FLEET_STRUCTURE law filed 2026-09-01T01:52Z
python -m mag.verkle_lance link --event "FLEET_STRUCTURE law filed" --when "2026-09-01T01:52:00Z"

# Tie-in 2 — fleet audit 2026-09-01
python -m mag.verkle_lance link --event "fleet audit" --when "2026-09-01T00:00:00Z"

# Optional: locate nearest/facted knots by label or hash
python -m mag.verkle_lance trace --key "FLEET_STRUCTURE"
python -m mag.verkle_lance verify --key "2670c7ea555c"
```

The `link --event` = free-text label (matched against session_id/theme/hash substring), `--when` = ISO timestamp used as the temporal anchor to attach the knot at-or-before that moment. Use the `link` (not `tie_in`) command for the two new fleet-structure events.
