# TESLA METER SPEC — the instrument that makes the race runnable (2026-09-11)

> **[AUDIT-TYPED]** status: SPEC — design of the run's first organ (ractor
> mandate TESLA, `watch/SALON_BUILD_DIRECTION_20260909.md`: "build the meter
> first... The meter is the first organ built"). Read-only companion to the
> builder drafts: this file modifies NOTHING in
> `BUDGET_MANIFEST_SKELETON_20260911.md` or `TASK_PACK_SKELETON_20260911.md`;
> where the skeletons need change, amendments are PROPOSED here as rows for
> desk adoption (L0 §7: adoption appends; override is void).
> Mirrors: `mag/grounding_wave.py` (hash-chain, append lock, verify-splits-PASS),
> `mag/honest_cache_meter.py` (never-estimate, capture_failures, EXIT_DRIFT),
> `watch/GROUNDING_WAVE.jsonl` (row shape), `watch/USAGE_METER_SELF_STEAL_20260904.md`
> (the wound: a meter existed per-turn and nothing read it — this spec exists so
> the Astra run cannot repeat it).

## 0. THE ONE LAW OF THE METER

Every token the run causes is counted, priced, and classified — **before** any
scoring happens, at attempt granularity, on $0 lanes exactly as on paid lanes.
Discounts are REPORTED SEPARATELY, never subtracted before logging: the meter
always computes list price, then records the discount as its own measured
column. A free lane produces a full token row with a receipted discount, not a
missing row. This is the whole spec in one sentence; everything below is the
schema that enforces it.

## 1. THE METER SCHEMA — per-episode record format

### 1.1 Token classes (six, each counted AND priced separately)

| Class | Definition | Pricing rule |
|---|---|---|
| `input_tok` | Uncached prompt tokens (task packet + message tail) | full input rate |
| `output_tok` | Visible completion tokens (answer spine + tool text) | full output rate |
| `reasoning_tok` | Thinking tokens. 5.x cannot disable thinking (`thinking=low` pinned). Provider-reported only: if the provider does not split reasoning from output, this is `null` AND `reasoning_split:"UNPROVEN"` — never estimated (honest_cache_meter law 1) | reasoning rate if billed separately, else recorded at output rate with the split marked UNPROVEN |
| `prefix_read_tok` | Cache READS on the shared frozen warm prefix (constitution + event layer v2 — the B/C shared interior; ladder: cache-hit logged per tranche) | prefix-read rate (skeleton §2: ~10% of base input — INFERRED, frozen before run) |
| `cached_full_tok` | Tokens that went through cache machinery but were billed AT FULL QUANTITY (cache writes; providers billing cache reads at full price) | full input rate — that is the point of the class |
| `discounted_tok` | Tokens billed at ANY rate ≠ full base rate, each with a `discount` object naming source and factor (`PROMO_SEAT` $0-lane, `CACHE_READ`, `SEAT_QUOTA` absorbed-by-pool) | list price computed; effective cost and discount recorded as separate columns |

Hard rule: `input_tok + prefix_read_tok + cached_full_tok = total prompt
tokens` and the sum is checkable against the raw provider usage blob, which is
stored VERBATIM in every row (`usage_raw`). No row collapses classes.

### 1.2 The attempt row (what the meter logs — every API call)

```json
{"schema_version":"astra-meter-v1",
 "row_type":"attempt",
 "ts":"2026-09-14T13:05:11Z",
 "episode_id":"E07-I3-f2-B-P1-s2",
 "attempt":1,
 "block":7,"task_id":"I3","condition":"B",
 "family_alias":"<lane-alias>","model_pin":"<pinned-config-id>","seat_alias":"<seat-pool-id>",
 "tok":{"input":4120,"output":1180,"reasoning":null,"reasoning_split":"UNPROVEN",
        "prefix_read":2816,"cached_full":0,"discounted":2816},
 "price_usd":{"list":0.00812,"effective":0.00000,"discount":0.00812},
 "discount":{"source":"PROMO_SEAT","factor":0.0,"receipt":"<quota-%-remaining>"},
 "latency_ms":41210,"retries_left":1,
 "outcome":"OK",
 "failure_class":null,
 "desk_work_ms":null,"waiting_ms":null,
 "usage_raw":{...verbatim provider usage blob...},
 "prev":"<sha256-of-previous-row>","hash":"<sha256-of-this-row>"}
```

`episode_id` grammar (PINNED — the meter keys on it, so it is frozen with the
manifest): `E{block:02d}-{I|S}{1..6}-f{1|2}-{A|B|C|D}-P{pop}-s{seed}`. This
extends the skeleton §5 example (`B07-T3-C-A-P1-s2`), which conflates
task/condition ordering and carries no attempt index — amendment A-T1 (§4).

### 1.3 The episode row (rollup of attempts, one per enrolled episode)

```json
{"schema_version":"astra-meter-v1",
 "row_type":"episode",
 "episode_id":"E07-I3-f2-B-P1-s2",
 "attempts":2,"captured_attempts":2,"capture_failures":0,
 "tok_totals":{"input":8036,"output":2210,"reasoning":null,"reasoning_split":"UNPROVEN",
               "prefix_read":5632,"cached_full":0,"discounted":5632},
 "price_usd":{"list":0.0161,"effective":0.0,"discount":0.0161},
 "within_allowance":{"input":true,"output":true},
 "wall_clock_ms":93400,"desk_work_ms":null,"waiting_ms":null,
 "outcome":"OK","failure_class":null,
 "duty_violations":0,"useful_output_chars":2144,
 "prev":"...","hash":"..."}
```

New columns the skeletons lack, each with its ractor lineage: `desk_work_ms` /
`waiting_ms` (EDISON — D-arm 240-second cumulative cap, waiting recorded
separately), `failure_class` from Gopher's FIXED vocabulary (`STALL · REFUSAL ·
OVERRUN · TOOL_FAIL · MALFORMED · TRANSPORT` — L0 §5, so meter rows and failure
receipts join on `episode_id`), `useful_output_chars` (the
USAGE_METER_SELF_STEAL output-ratio lesson: burn must be comparable to output,
per condition — the meter emits `useful_output ÷ tok_totals.output` in every
rollup), `within_allowance` (F4 budget-consumption verdict per class).

### 1.4 Rollups (computed, never hand-tallied)

Rollup keys and their expected denominators (from §3 envelope): by
`(condition)` = 480 rows each; by `(family)` = 960; by `(condition, family)` =
240; by `(task, condition)` = 40; by `block` = 96. Every rollup row carries:
per-class token sums, per-class price sums (list / effective / discount), the
B−C episode-level budget delta per block (the F-T4 gate feed), failure-class
counts, `capture_failures`, refusal/truncation counts, and quota receipts per
seat alias. Rollups render to `watch/ASTRA_METER_ROLLUP_{date}.md` — a report
that quotes a meter number must be able to cite a rollup row, not a vibe.

## 2. THE MANIFEST FORMAT (what BUDGET_MANIFEST_SKELETON adopts)

The manifest is the FROZEN instrument; the meter is its live reading. Format:
one frozen document, fields partitioned by freeze class, hash-sealed at HOLD 4.

**FROZEN-BEFORE-RUN (Fen's law — sealed the day it's born, iterate before the
seal, never after):**
- Envelope arithmetic (§3) incl. the per-cell episode counts.
- Per-tier token allowances PER CLASS: `{input, output, reasoning_allowance,
  prefix_read_expectation, cached_full_expectation}` for I1-I6, S1-S6 (skeleton
  §2 table extended with the two cache classes + a frozen `reasoning_allowance`
  — currently missing, which makes the skeleton's 12.3M bound understated;
  amendment A-T2).
- Deadlines per family and per condition (skeleton §6 fields, operator-pinned).
- Rate cards + discount assumptions per family alias (snapshot at seal; the
  meter prices through the snapshot so historical recomputation matches —
  honest_cache_meter law 4).
- The meter schema itself: `schema_version:"astra-meter-v1"`, row grammar,
  `episode_id` grammar.
- Lane/seat fan map (skeleton §4.3: round-robin seats, per-fan receipts).
- Freeze stamp: `manifest_sha256` recorded at seal; every meter row cites it
  (`manifest_sha` field, omitted from examples above for brevity).

**RUNTIME-MEASURED (never frozen, never edited after capture):** all token
counts, prices, latencies, desk/waiting times, failure classes, quota
receipts. These live ONLY in the ledger; the manifest references, never
contains, them.

**Amendment rule (L0 §7, binding):** frozen fields are never rewritten in
place. A change appends `{field, what blocks, minimal change, why, receipt}` to
the manifest's amendment ledger and re-stamps the version. A meter row
captured under manifest vN stays valid under vN+1 because it carries
`manifest_sha`; readers reconcile by version, never by mutation.

## 3. THE 1,920-EPISODE ENVELOPE — arithmetic template (VERIFIED)

**SUPPORTED decomposition (budget skeleton §1, consistent with the ladder
card's "1,920 episodes per Astra's pre-registration" and FOLD3's four locked
conditions):**

```
1,920 = 20 blocks × 12 tasks × 2 families × 4 conditions
      = 4 conditions × 12 instances × 40 episodes        (40 = 20 blocks × 2 families)
per condition: 480      per family: 960      per task: 160
per (condition, family) cell: 240      per (condition, task) cell: 40
irreducible I1-I6: 960  ·  sham S1-S6: 960
```

Both factorizations are the SAME envelope; the canonical on-disk form is the
block form (matches the skeleton and the D-arm tension), the cell form (40 per
condition×task) is the meter's rollup denominator — use either, never a third.

**Token envelope template (per class, so the bound is auditable):**

```
envelope_tokens[class] = Σ_cells  episodes(cell) × allowance[class](cell tier)
envelope_tokens[list_usd] = Σ_rows  tok[class] × rate[class](family)
```

Worked worst case (skeleton §2 allowances, input+output only): 960 × 9,536 +
960 × 3,268 ≈ **12.29M tokens** — REPRODUCED by the template. Two honest
caveats, tri-stated: (a) it omits `reasoning_tok`, which 5.x cannot disable
(thinking=low still bills) — the bound is UNDERSTATED until a frozen
`reasoning_allowance` per tier exists (A-T2); (b) it prices all prefix reads at
full rate — `prefix_read` economics (~10%, INFERRED) is what makes effective
volume "materially lower," and the meter proves that instead of asserting it,
because the D-arm tension (480 desk episodes × 4 min = exactly the 32-hour
budget — skeleton §1 DISPUTED) is ALSO visible in meter columns (`desk_work_ms`
vs the cap). The envelope is what makes the manifest checkable; the meter is
what makes it true.

## 4. WHERE THE METER LOGS (proposed organ contract)

- **Organ:** `mag/astra_meter.py` (built AFTER this spec, BEFORE HOLD 3 — the
  meter is the first organ built, per the mandate; rehearsal F-H3 is its
  acceptance test).
- **Ledger file:** `watch/ASTRA_METER_20260911.jsonl` — append-only JSONL,
  hash-chained `prev`/`hash` per row, append LOCK during writes, GENESIS
  `"0"×64` — mirroring `mag/grounding_wave.py` exactly. Corrections are new
  rows citing the old hash (delete-as-append); captured rows are never edited.
- **Constant names (frozen with the schema):** `ASTRA_METER_LEDGER`,
  `ASTRA_METER_LOCK`, `SCHEMA_VERSION = "astra-meter-v1"`, exits
  `EXIT_OK=0 / EXIT_PARSE=1 / EXIT_DRIFT=2 / EXIT_SWALLOW=3` — the exit family
  mirrors `mag/honest_cache_meter.py`, plus the new swallow alarm (§5).
- **Verify law (grounding_wave v3, carried):** `verify()` reports
  LINKAGE-PASS (hash chain intact) SEPARATELY from CAPTURE-PASS (rows fired =
  rows captured) and DENOMINATOR-PASS (captured episodes = envelope cells
  fired). No reader may quote bare "PASS" again.
- **Ledgers mirrored (pattern provenance):** `watch/GROUNDING_WAVE.jsonl`
  (append-only chained rows), `mag/honest_cache_meter.py` (verbatim usage_raw,
  capture_failures, dedupe on provider response id with duplicates COUNTED not
  dropped, nightly invoice reconciliation), `watch/USAGE_METER_SELF_STEAL_20260904.md`
  (output-ratio + the meter-nobody-reads wound), skeleton §4's per-seat quota
  receipts (the promo accounting unit).
- **Render:** nightly `watch/ASTRA_METER_ROLLUP_{date}.md` + the final run
  report's budget section is the seal-time rollup, cited by `manifest_sha`.

## 5. THE FALSIFIER — the meter alarms, never swallows

The fleet's wound is the `except: pass` that makes a row vanish and the run
look healthy. Gopher's law applied to instrumentation: **nothing vanishes into
a retry, and nothing vanishes into a log line either.**

- **F-T1 (no-swallow, new teeth):** every generation attempt the harness
  observes is either CAPTURED or counted in `capture_failures` — a `try/except`
  anywhere in the capture path that neither captures nor counts is a build
  defect; the meter exits `EXIT_SWALLOW` and the run HALTS at the next block
  boundary. Alarms, not absences.
- **F-T2 (denominator lock):** at every pause/seal point,
  `captured episode rows == episodes fired per the envelope ledger`. Missing
  rows block the run; the denominator is EPISODES FIRED, not episodes
  succeeded (Gopher: stalls stay in the denominator — so do uncounted rows).
- **F-T3 (drift):** nightly reconciliation of meter sums vs provider-side
  truth (seat quota receipts per fan; invoice lines on any paid overflow)
  within a frozen tolerance; drift beyond it exits `EXIT_DRIFT` and pages the
  desk — mirrors honest_cache_meter's nightly job.
- **F-T4 (compute-match gate feed):** the meter computes the B−C episode-level
  token-budget delta per block. Non-zero delta = skeleton F-B1 fires: halt
  before any scored episode and fix the manifest, not the results. The meter is
  the instrument that DETECTS the gate-void; without it F-B1 is a promise, not
  a check.
- **F-T5 (class completeness):** any family whose rows exceed 20%
  `reasoning_split:"UNPROVEN"` is flagged METER-INCOMPLETE in the rollup and
  the affected gate's confidence is DOWNGRADED and reported — measured
  ignorance, never assumed symmetry.
- **F-T6 (rehearsal acceptance):** HOLD 3's 16 rehearsal episodes must show
  16/16 captured with all six classes populated (or honestly nulled per F-T5)
  before any real episode fires. Instrumentation miss = ladder F-H3: fix the
  harness, not the hypothesis. This is the meter's own falsifier — if the
  meter cannot pass its rehearsal, the race does not start.

---
*Frozen-field law per Fen; denominator law per Gopher; time-capture per Edison;
visibility per Mengxi. The meter is first because every other mandate is
unverifiable without it. Spec read-only vs builders' drafts; amendments A-T1
(episode_id grammar), A-T2 (reasoning allowance + cache-class split) are
PROPOSED rows for desk adoption into BUDGET_MANIFEST_SKELETON_20260911.md.*
