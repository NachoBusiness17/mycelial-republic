# MICKEY-17 v2.1 — FRONTIER-BURN ENGINE SPEC

Supersedes v2 (2026-09-25) by applying amendments A1–A12 from the spec steal burn (`watch/inbox/SPEC_EDITS_MICKEY17_V2_20260925.md`; 16 lanes, 63 raw edits → 32 clusters → 12 amendments + 7 laws on trial, red-team-read before filing). v2 is preserved untouched beside this file. **Changelog:** A1 lane archive + fold/spec live at estate absolute paths; A2 refire-once + tombstones + casualty header; A3+A4 verifier clause replaced (two-tier, persisted, honestly stated); A5 Law 5 extends to fold content (script writes counts, byte-checks quotes, computes ranking); A6 incremental lane writes; A7 paced admission, in-place retry banned; A8 REVIEW seat added (five phases → six); A9 steer-preserves-sweep clause (spec only; runner change gated on reading the harness steer path); A10 gate_fixes note-field convention + failure-mode item 11 (no new law); A11 scripted URL-liveness pass at fold; A12 script-computed PRISMA / WIDTH-ECONOMICS / OPERATING-ENVELOPE / FIDELITY sections. Laws on trial, applied: Law 6 letter amended (incremental private writes; law kept); Law 7 kept at 50 with all three justifications replaced; COST DOCTRINE scheduling claim replaced (off-peak is a default for unattended fires, voided by explicit operator order); "width N held" is henceforth a journal receipt, never a conclusion line. Saved engine: `.zcode/workflows/mickey17-v2.dwf.ts`; deterministic fold: `tools/mickey17_v2_fold.py`.

---

## 1. PURPOSE

MICKEY-17 v2.1 is the estate's frontier-burn engine: for one topic, it fans out a fixed width of cheap parallel lanes across the live frontier (papers, vendor engineering blogs, OSS repos, operator forums), drags every claim home as a register row bound to a verbatim quote and a URL, rules honestly on contradictions instead of averaging them, folds the register into one master document whose every count is written by script rather than trusted from any agent's self-report, then files itself back into the estate so the next run starts from a spec instead of a memory. Named for the v1 run of 2026-09-20 (`memory/runs/mickey17/`, 2,493 estate files digested in 72 register slices, folded by script). The first outward dogfood (2026-09-24/25, v2) burned 50 lanes in ~65 minutes and returned 246 rows; the spec steal burn (2026-09-25) then turned the engine on itself and produced this version. **All records of a run live in the estate**: `C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/mickey17_v2/lanes/` is the archive of record (A1) — the fold's scripted recount runs against the estate copy, never a workspace mirror.

## 2. INTERFACE

One invocation takes three arguments (unchanged from v2):

```json
{
  "topic": "one-line statement of what this burn is stealing for",
  "targets": [
    { "id": "short-lane-name", "what": "the source or source-family to mine", "start": "https://absolute/start/url" }
  ],
  "width": 50
}
```

- **`topic`** — one line, prefixes every lane prompt. **`targets[]`** — one per lane; `id` becomes the backup filename; `what` mandatory; `start` optional (search-starting lanes allowed). **`width`** — lanes = targets 1:1; extra side truncated.

**On-disk mapping.** Each lane lands at `ESTATE/memory/runs/mickey17_v2/lanes/<id>.json` — absolute path, written by the lane itself (A1). A lane file is a single object with a `rows` array or a bare array (the counting script accepts both). One row:

```json
{ "lane": "...", "source": "https://...", "claim": "...", "quote": "verbatim from source",
  "estate_status": "confirms-ours | owed | we-have-better | new", "steal": "concrete action + landing spot",
  "leverage": "high | medium | low" }
```

Note fields carry provenance: `fetched`/`fetch_method`/`verified_via`, `caveats`, `rubric_gaps`, `negative_results`, `unverified`, `premise_check`, `grep_evidence`, plus **`gate_fixes`** (A10, optional convention): a lane that hits a security-gate block records the block→fix cycle there; the fold script recounts it next to estate_status. **`refire_of`** (A2): set on a re-fired lane, naming the kill reason. Verification verdicts persist as `ESTATE/memory/runs/mickey17_v2/lanes/<id>.checks.json` (A3+A4). A dead lane is a valid lane file of exactly one negative-result row; a twice-dead lane is a tombstone (`status: "tombstoned"`, `receipts: []`, error verbatim — A2).

## 3. PHASE MACHINE

Six steps, strictly ordered (A8). Steps 1–3 fan out; 4–6 are single-seat. While lanes are in flight, an operator message to the parent seat is **steering context only — it must not interrupt, cancel, or re-fire running lanes** (A9, spec clause; the runner-level change stays gated until someone reads the harness steer-interrupt path and files what it does).

1. **SWEEP.** Launch under a **paced admission ramp** (A7): the first wave admits 8 lanes; remaining lanes admit as slots drain. Each lane runs on the cheapest flash-tier model, reads its sources, and **writes only its own file, incrementally** (A6): append/rewrite `lanes/<id>.json` as rows confirm; on any restart read its own file first and mine only the gap; rows carry an idempotency key (source URL + verbatim-quote hash). A crashed or killed lane is **re-fired exactly once** (A2) — same target id, `refire_of` note, prompt rewritten to name the kill reason and offer an alternate start; a twice-dead lane becomes a tombstone. In-place retry against a usage window is banned: on a usage-limit error, parse the reset timestamp and **reroute to the next model/key or park until reset**, filing the casualty as a negative row.
2. **SUPPORTS-CHECK (tier 1, every row).** A flash-tier binary judgment per row — `supports: yes|no` + one-line reason, checked against the fetched source. A byte-perfect quote that does not entail its claim demotes the row (binding ≠ supporting). All verdicts append to `lanes/<id>.checks.json` before phase 4 opens (A3+A4).
3. **DEEP-VERIFY (tier 2, fold-load-bearing rows only).** The selection is **mechanical, not lane-authored and not array-order**: the fold script's top-K candidates plus every tier-1 `supports: no` row go to an independent verifier on a different model family or mechanical-only method. Verdicts: `verified | unconfirmed | crashed | same-chain-verified` — crashed confirmers count in their own bucket, never merged with substantive unconfirmations (A3+A4).
4. **FOLD.** One seat whose **first act is the counting script** (`tools/mickey17_v2_fold.py`) over the estate lane archive. The script writes into the fold: the **casualty header** (fired N / landed M / landed-empty E / missing N−M, transient-vs-hard, cause named — A2), the scoreboard, the verifier table from persisted verdicts, and the four pipeline sections (A12): **PRISMA flow** (identified / screened / excluded-with-one-mutually-exclusive-reason-code / included, invariant asserted before the fold may be written), **WIDTH-ECONOMICS** (rows-per-lane distribution, top-10 share, cross-lane duplicate-quote count), **OPERATING ENVELOPE** (rate-limited retries, peak/min, grind ratio, hook failures × mean duration), **FIDELITY** (rows passing byte-check / total; verifier-confirmed / verifier-passed). A scripted HEAD/GET pass stamps every rendered row `url_checked_at`; URLs dead at fold time move to negative results with their HTTP status (A11). The seat writes prose around script-written numbers only; any number taken from a summary instead of recomputed is tagged `carried` (A5). Fold contents: scoreboard, top steals (ranking computed by script; a lane-claimed top steal outside the script's top-K files as DISPUTED), DISPUTED tier with conditional rulings, negative results as a counted reasons table, go list sized one-seat-one-sitting. Every steal/ruling sentence carries lane id + row index.
5. **REVIEW.** A fresh-reader seat that has seen nothing else judges fold-as-text: a fixed five-point form (row-binding spot-check, DISPUTED ruled conditionally, negatives itemized, scoreboard matches the script recount, go list one-sitting-sized), at most 5 bullets, returning **ACCEPT or REVISE-once** (A8). SPEC may not start, and FILE may not run, without a recorded review verdict.
6. **SPEC + FILE-INTO-ESTATE.** One seat formalizes/updates this engine document from the run's own evidence (quotes byte-checked against lane rows — A5b). Then everything files: fold, spec, **and the lane archive already in place** — spec citations land as absolute `path:line` (A1). A run that does not file itself did not happen.

## 4. THE RUBRIC

Six checks (unchanged from v2 — the trial kept them; "under-scoped, not overpriced": 2 of the first run's 10 recorded failure modes were invisible to all six by construction, and the repair is the tier-1 supports-check, not a seventh standing check). A lane that cannot pass one records why in a note field. **1. Primary source fetched** (method + raw-bytes cross-check where possible). **2. Verbatim quote bound** — a paraphrase is not a quote; a quote with silently dropped words is a failed row; no quote, no row. **3. URL recorded** (estate-internal absolute path counts). **4. Estate grep ≥ 2 dirs** of `corpus/steal`, `memory/research_polished`, `watch/inbox`; a zero-hit grep is a recorded finding. **5. Concrete steal action** — one seat, one sitting, landing spot named. **6. Negative results first-class** — dead sources, walls, empty greps, premise drift, unconfirmations filed with evidence.

## 5. LAWS

Seven laws (A10 explicitly adds no eighth).

1. **CITATION-BINDING.** No quote, no row. The field's measured baseline is ~47% verbatim fidelity; the quote is the unit of storage so the check stays mechanical. Binding is not supporting — entailment is tier 1's job.
2. **NEGATIVE-FIRST-CLASS.** A dead source is a result. Tombstones are filed casualties (transient gets one bounded idempotent refill; hard is subtracted from owed, cause named). Nothing silently dropped, nothing substituted unlabeled.
3. **CONTRADICTION-TIER.** Never average, rule with conditions — or name the claim that is false. A merged "both are kind of right" sentence is a fold defect.
4. **ABSOLUTE-PATHS.** Every prompt, citation, and file reference is absolute; estate citations land as `path:line`. The law applies to the engine's own receipts — v2 broke it for its own lane archive and A1 is the repair. A run may write "width N held" only if its journal shows N concurrent subagents; otherwise "N lanes fired in W waves (T minutes)" — measured, never asserted.
5. **FOLD-BY-SCRIPT, EXTENDED (A5).** Counts recounted from files, never self-reports — and the script **writes** the scoreboard, verifier table, and pipeline sections into the markdown; seats write prose around script-written numbers only. Phase byte-compares every fold and spec quote against the cited lane row; mismatch blocks filing. The top-K ranking is computed by the script.
6. **WRITES-SERIAL.** Reads fan out; shared-state writes are single-seat, serial, after lanes land. The letter is amended (A6): "one file of their own" never meant one write — lane-private incremental writes are parallel and expected; the law was always about shared state.
7. **WIDTH-LADDER, justifications replaced (trial verdict).** 14 = day minimum, 50 = standard burn, more only behind an economics gate. What the evidence actually supports: median 5 rows/lane (flat), top-10 lanes 20.7% of rows, 0.4% duplicate quotes — no concentration, so 50 stands. What died: the night window is **not** the cheap window (00Z Sunday produced 16,522 rate-limited events vs 726 mid-morning — off-peak moves token price, only **pacing** moves the 429 budget); higher rungs are not "the same shape" (the estate's own 240-lane rung shared one prompt prefix — correlated width; above 50 requires the previous fold's WIDTH-ECONOMICS to show duplicate-quote share < 10% and top-10 share < 50%); within-lane "more" has a measured negative regime (fact-check accuracy falls ~42% from 2 to 150 tool calls).

## 6. COST DOCTRINE

Cheap flash lanes; verification spend aimed mechanically. Tier-1 supports-checks on every row (~hundreds of flash judgments, negligible); the expensive deep pass only on fold-load-bearing rows the script selects. Disputed-pair rulings and fold/spec quote byte-checks are the other premium spends. **Scheduling (replaced):** off-peak windows are the default for *unattended standing fires* — and are **voided by any explicit operator order**: waiting for a window after being told "go" is a fold-reportable defect. Off-peak moves token price only; admission pacing moves the 429 budget. On usage-window errors: reroute to the next key/model or park until reset — never in-place retry.

## 7. FAILURE MODES (standing list, reason codes for the PRISMA flow)

1 phantom-source · 2 premise-drift · 3 url-owner-rot · 4 walled-source · 5 barren-start · 6 fabricated-name-or-rumor · 7 quote-drift (incl. quote-real-claim-unsupported) · 8 unit-error · 9 verifier-unconfirmed (and crashed confirmers, own bucket) · 10 empty-estate-grep · **11 scanner-under-coverage (A10): inconclusive gate scans filed with count and rate — first dogfood of the guard trace: 2,032 of 10,491 PreToolUse scans (19.4%) inconclusive; ENOBUFS cause unconfirmed in the audited log.** These codes are the mutually-exclusive exclusion reasons in the fold's PRISMA flow; every instance cites its lane or fold section.

## 8. PORTS

1. **Reusable workflow** — `.zcode/workflows/mickey17-v2.dwf.ts`, args `{topic, targets, width}`; implements the ramp, refire-once, incremental writes, both verification tiers, the review seat, and the estate-side archive. Re-firing passes a new topic/targets — nothing topic-specific inside. **Resume:** existing lane files are accepted as completed; only missing lanes fan out; re-runs dedupe on (source URL + quote hash).
2. **Task-wall chore family** — `burn(<topic>, width=N) -> fold -> chores[]`; the daily 14-wide minimum, the 50-wide weekly standard; every fold's go list converts one-to-one into wall chores. (Update 2026-09-26: strip-write-tools-at-fan-out is DISCHARGED RUNNER-SIDE, `watch/inbox/WRITE_STRIP_FANOUT_20260926.md`: estate spawns (`mag/orchestrator.py spawn_task`) now compile child tool schemas read-only by default. The ZCode-harness `agent()` schema-restriction change stays SPEC-ONLY in that receipt, still open. A10's non-discharge applies to that harness leg only.)
3. **Corpus/steal entry** — the standing registration in `corpus/steal` pointing at this spec, the current fold, and v1 as the inward ancestor.

---

*Provenance: v2.1 text applies amendments A1–A12 exactly as evidenced in `watch/inbox/SPEC_EDITS_MICKEY17_V2_20260925.md` (every amendment carries verbatim evidence, cost, and the law it touches; the trial section's 7 reversals are folded into Laws 4/6/7 and §6 above). The v2 text is preserved unmodified in `MICKEY17_V2_ENGINE_SPEC_20260924.md`. Counts in the trial came from script recounts over the 50-lane archive and the session store read read-only.*
