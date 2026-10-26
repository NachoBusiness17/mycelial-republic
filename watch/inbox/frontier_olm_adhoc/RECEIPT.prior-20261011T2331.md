source-fetched: adhoc

# FRONTIER OLM ADHOC MINE: FOLD RECEIPT (wave-3 edition, 2026-10-11 late window)

Why a third edition: this fold folds the mine's second confirmation batch and second steal round (a later wave of the same adhoc run). The wave-2 mints of the four outputs are preserved byte-identical beside this edition (copies made this fold, before overwriting): `DIGEST.prior-20261011T0504.md`, `register.prior-20261011T0448.jsonl`, `percolator_candidates.prior-20261011T2040.jsonl`, `RECEIPT.prior-20261011T0659.md`. The two registers' URL sets are disjoint (verified by script this fold: 0 shared URLs; wave 2 held 23 rows - its own provenance is in `RECEIPT.prior-20261011T0659.md`).

Fold moment: 2026-10-11, this session (seat: folder, the fold gopher). Run directory: `watch/inbox/frontier_olm_adhoc/` inside repo root `C:/Users/foste/Documents/projects/local_sovereign_agent`.

Gate: `tools/fold_gate.py acquire --holder "olm-mine:adhoc" --wait 900` exited 0 ("HELD C:\Users\foste\Documents\projects\local_sovereign_agent\memory\runs\fold_locks\workflow-fold.lock holder=olm-mine:adhoc") before this ask's writes; released after the writes (Instruments item 6).

## Instruments run this ask (exact commands and outputs)

1. Gate acquire: `C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe C:/Users/foste/Documents/projects/local_sovereign_agent/tools/fold_gate.py acquire --holder "olm-mine:adhoc" --wait 900` -> "HELD ... holder=olm-mine:adhoc", exit 0.
2. Directory survey (ls + python os.walk): pre-write state 647 files / 51,557,053 bytes; `steal/` 14 files listed with sizes below; `sweep/` and `lens/` aggregates measured post-write (below).
3. Registry scans: `wc -l memory/workflows/REGISTRY.jsonl` -> 177 lines; `grep -n -i "adhoc\|olm"` -> olm-mine family rows at lines 31-40, 64, 93-95, 102-104, 124; `grep -c "adhoc"` -> 0.
4. Builder script `C:/Users/foste/AppData/Local/Temp/fold_adhoc_wave3.py` run under the acquired gate; it: copied the four prior mints (shutil.copy2), wrote `register.jsonl` (21 rows) and `percolator_candidates.jsonl` (5 rows) via per-line json.dumps (ensure_ascii=False), wrote `DIGEST.md`, then validated: json.loads per line (21/21 and 5/5 parse, 0 errors), URL disjointness vs `register.prior-20261011T0448.jsonl` (0 shared URLs), area/source counters, em/en-dash audit (0 and 0 in all three files), non-ASCII audit (only the ASTRO row's Polish quote characters in register.jsonl, disclosed below).
5. Post-write measurements: python os.path.getsize / os.walk (table below); this file's own row is solved to a fixed point by a finisher pass and re-verified with os.path.getsize.
6. Gate release (after all writes): `C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe C:/Users/foste/Documents/projects/local_sovereign_agent/tools/fold_gate.py release --holder "olm-mine:adhoc"`.

## Counts

Confirmed finds this wave: 21 (register.jsonl rows, json-validated this ask).
- By area: finetuning-adaptation 5, kv-cache-context-engineering 6, agent-memory-continuity via x 2, evals-self-improvement via x 3, inference-efficiency 5.
- By source door (door = discovery channel, not URL host; source fields normalized to door families - the two via-x sweeps' longer door strings live verbatim in their sweep bank note fields): hn 5, reddit 6, x 10.

Unconfirmed (excluded from register): 3 (DIGEST.md section 5, each with its confirmation evidence).

Steal cards -> percolator_candidates.jsonl: 5 rows (agent-memory-continuity via x; evals-self-improvement via x; finetuning-adaptation; inference-efficiency; kv-cache-context-engineering).

Sweep payloads folded: 32, items 219 (hand-tallied from this ask's per-sweep items arrays; per area: swarm-orchestration 30, kv-cache-context-engineering 29, evals-self-improvement 29, open-local-models 28, inference-efficiency 28, agent-memory-continuity 27, quantization-compression 25, finetuning-adaptation 23; counts item-slots, not distinct artifacts - DIGEST.md honest gap 4). Of the 219, 24 reached the confirmation pass (21 confirmed + 3 failed).

Prior wave (preserved): 23 confirmed rows, URL-disjoint (0 shared). Combined run total across both waves: 44 confirmed finds.

## Workflow gate row pointer

`memory/workflows/REGISTRY.jsonl` - NO row names this adhoc run (grep -c "adhoc" = 0 over 177 lines, run this ask). Nearest verifiable pointers, read this ask:
- `memory/workflows/REGISTRY.jsonl:102-104` - olm-mine.dwf.ts, digest c7c95efcd512, verdict PASS, ts 2026-10-06T00:52:51Z (the family's latest PASS rows; checks G1-G8).
- `memory/workflows/REGISTRY.jsonl:124` - olm-mine.dwf.ts STATUS-Row, status active, latest_registry_row_ts 2026-10-06T00:52:51Z, ts 2026-10-06T18:53:21Z.
- `memory/workflows/REGISTRY.jsonl:175-177` - the newest rows in the file (mcp-landscape-wide-dig.dwf.ts, PASS, ts 2026-10-11T02:07:34Z), named so the pointer includes the file's true tail.

The prior mint (`RECEIPT.prior-20261011T0659.md`) classified the missing row as an incident, not registered debt; the evals steal card's mapping-keyed coverage-census probe is the designed detector; this fold did not register a row (DIGEST.md honest gap 8).

## File inventory (bytes measured this ask)

Interpretation, stated: every file this fold wrote or preserved is listed individually; `sweep/` (621 files of raw captures and banks) and `lens/` are listed as measured aggregates because a full listing would bury the fold outputs - the tree is on disk and re-measurable with Instruments item 5.

Fold outputs written this wave:
```
DIGEST.md	39698
register.jsonl	20461
percolator_candidates.jsonl	19239
RECEIPT.md	10604 bytes (fixed point)
```
(DIGEST.md size is post-repair: the cold-reader repair pass in the same session grew it from the 28,592-byte mint to 39,698 bytes fixing 17 issues, repair record below; RECEIPT.md row self-size re-solved to fixed point after the repair.)

Prior mints preserved this fold (shutil.copy2, byte-identical):
```
DIGEST.prior-20261011T0504.md	36715
register.prior-20261011T0448.jsonl	22556
percolator_candidates.prior-20261011T2040.jsonl	26969
RECEIPT.prior-20261011T0659.md	19768
```

steal/ (14 files, 213,444 bytes):
```
agent-memory-continuity via x.json	4809
agent-memory-continuity via x.md	12610
evals-self-improvement via x.json	6016
evals-self-improvement via x.md	19312
finetuning-adaptation.md	35340
inference-efficiency.json	6215
inference-efficiency.md	20837
kv-cache-context-engineering.json	4723
kv-cache-context-engineering.md	45012
kv-cache-context-engineering.reddit2.json	7894
open-local-language-models.json	8256
open-local-language-models.md	20542
swarm-orchestration.json	6241
swarm-orchestration.md	15637
```

Aggregates and total (os.walk, measured after the writes): `sweep/` 621 files / 51,146,649 bytes; `steal/` 14 files / 213,444 bytes; `lens/` 8 files / 90,952 bytes; run-directory total post-write 651 files / 51647055 bytes (pre-write this ask: 647 files / 51,557,053 bytes; the delta is the four .prior preserves plus the four output rewrites, arithmetically checked).

## Cold-reader repair record (same session, after the mint)

The cold reader reported 17 issues against the minted DIGEST.md; all 17 were fixed in place this repair ask, under a fresh gate acquire (exit 0). Instruments run by the repair pass, exactly:
1. Gate re-acquire: same command as Instruments item 1 -> "HELD ... holder=olm-mine:adhoc", exit 0.
2. Sweep-bank census input: `ls watch/inbox/frontier_olm_adhoc/sweep/ | grep -i "\.md$"` -> 74 .md files: 36 live area-door banks (32 current-generation incl. 4 `open-local-models-*`, PLUS 4 prior-generation `open-local-language-models-*` - the name drift DIGEST gap 2 now states), 9 preserved prior mints, remainder scratch reads.
3. Live spot-check A (register row 12, agentmemory v0.9.30): WebFetch of https://github.com/rohitg00/agentmemory/releases/tag/v0.9.30 -> answer YES, the register quote appears verbatim ("Durable capture: event ids, a persistent capture inbox, retries, dead letters, and an offline hook spool" continuing "while the server is down"), release tag v0.9.30.
4. Live spot-check B (register row 18, MemSkill): WebFetch of https://arxiv.org/abs/2602.02474 -> answer NO for byte-verbatim: the live abstract reads "a \emph{designer} that periodically reviews hard cases where selected skills yield incorrect or incomplete memories..." (literal LaTeX \emph markup inside the sentence where the register quote has plain "designer"); title and authors match (MemSkill; Zhang, Long, Bao, Feng, Zhang, Yue, Wang). Substantively present, not byte-verbatim; recorded as such in DIGEST section 1.
5. Post-edit audit over DIGEST.md: all 17 fix-marker strings present (script check, 0 missing); em/en-dash counts 0/0; door-column rows 21/21; 131 lines, 39,698 bytes.
6. This receipt's inventory row for DIGEST.md updated 28592 -> 39698 and totals re-solved to fixed point.
Not run by the repair pass: any further web fetches beyond the two spot-checks, pytest, estate instruments, the per-bank item census (deliberately deferred - DIGEST gap 6 states why).

## Honest notes

- Supersedes lineage: the four live outputs were the wave-2 mints until this fold; preserved before overwriting (names above). Nothing else in the run directory was touched by this fold.
- Quote dash-normalization: em/en dashes appear in no output (audit 0/0 per file); arrows in quoted material render as -> and en-dashes as - (e.g. the SupersocksIntel and CryptoBandit rows); the ASTRO register row carries the Polish README quote verbatim in UTF-8 with its English gloss inside the why field.
- Source normalization: register source fields are door families (hn/reddit/x); the fold input's longer per-sweep door strings live in the sweep banks.
- The 1wom3fe finding: the kv steal card's rev-2 addendum uses 1wom3fe numbers sourced to the sweep's raw capture; this wave's confirmation pass found the claimed quote absent from the live page, so the percolator row and DIGEST.md flag it (section 5.1). Its ~3.2 GB figure and eviction counters are NOT register-grade.
- Not run by this fold: pytest, estate instruments, any probe, any web fetch (the fold consumed the ask's payload; every web-verification claim inside it is attributed to the confirmation pass quoted in DIGEST.md section 5).
- Counting caveat: the 219 per-area sweep counts are hand-tallied from the ask's 32 items arrays; the wave-2 input tallied 241 for the same banks (DIGEST.prior-20261011T0504.md section 1) - both numbers are true of their inputs; neither was re-derived from the sweep files by this fold.
