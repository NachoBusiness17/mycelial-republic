# MC6 - OPUS BRIEF SKELETON (the paid ask's structure, 2026-09-30)

Fence owner: MC6 lane. Files owned: this skeleton + `tools/lensing_ask.py` (the
carrier; DO NOT FIRE). Parent plan: `watch/inbox/THE_MOUNTAIN_CLIMB_PLAN.md`
Phase 2. Gates carried down: fires ONLY on operator GO (the AA1 law); nothing
enters the brief unsourced; every number below names its byte source.

This file is the SPEC, not the brief. MC1-MC4 lanes paste their dossiers into
the slots below; MC5 (route v1) fires later and takes its slot; the evidence
pack is REGENERATED FROM BYTES at assembly time, never from memory.

## 1. THE SKELETON - sections and byte budgets

Prompt envelope: hard ceiling 40,960 bytes (40 KiB), enforced by the carrier's
size guard (`tools/lensing_ask.py --dry` fails closed over it). Working target
37,000 so assembly has 3,960 bytes of slack for glue and last receipts.

| # | Section | Filled from | Budget (bytes) | Content law |
|---|---------|-------------|----------------|-------------|
| 0 | ENVELOPE | this skeleton (fixed text) | 1,000 | Who we are in 3 sentences; the output contract; the laws (UNPROVEN marks, no praise, path cites, no em-dash bytes, one shot no follow-up) |
| 1 | THE SHERPA | MC1 dossier | 4,500 | The carrier architecture, every organ, each with the receipt that proves it exists and works. Organs, not history |
| 2 | THE SUMMIT | MC2 dossier | 3,000 | The compass arc + operator canon in the operator's own words with pointers (sovereign platform, GWAP-as-backend, Roblox-without-predators, portability, continuity) |
| 3 | WHERE WE STAND | MC3 gap dossier | 4,500 | System-by-system rows: system, status, maturity, missing piece, source. The audit's FAIL rows live here as gap inputs |
| 4 | THE ROUTE v1 | MC5 (fires later) | 6,000 | The climb's pitches: what to build, why this order, how each pitch is verified (a falsifier per pitch). Slot stays EMPTY until MC5 lands |
| 5 | THE BIBLIOGRAPHY | MC4 dossier | 2,500 | Curated per-domain sources only (server design, netcode, procgen, verifiable/anti-cheat, RL-as-content, engine, distribution). No annotations beyond one line each |
| 6 | THE EVIDENCE PACK | regenerated at assembly (section 2 below) | 12,000 | Instrument outputs only. No prose claims the pack does not carry |
| 7 | THE ASK | section 3 below (fixed text) | 3,000 | The lensing questions, verbatim from this skeleton |
| - | Assembly glue (headers, dividers) | - | 500 | Section dividers only, no new content |
| | TOTAL | | 37,000 target / 40,960 ceiling | |

Budget law: a section over budget is CUT, not padded around; if MC5 lands over
6,000 the route gets compressed by its own lane before assembly, never by the
assembler silently. The carrier's `--dry` reports the per-section share (split
on `## ` boundaries) so drift is visible before any spend.

## 2. THE EVIDENCE PACK - what proves our state better than prose

Seven instruments, 12,000 bytes. Each row: what it proves, the byte source, the
assembly rule. Assembly rule is universal: READ THE NAMED BYTES at assembly
time, re-run the named instrument where it is a live command, paste output with
timestamp. A number that cannot be re-derived the same day does not ship.

### 2.1 GPS ledger capability table (1,800 B) - the meter exists

- Proves: routing by measurement not label; receipts per decision step; truth
  separated from price.
- Byte source: `watch/inbox/game_platform_basecamp_20260929/GPS_MCP_V0_20260929.md`
  (28 tests in 2.94s; smoke: design_judgment to frontier-opus $0.12 conf 0.97;
  cascade local 0.75 to mid 0.92 total $0.0042; record_verdict 0.96 -> 0.9608
  at n=53 running mean; 3 receipt rows for 3 decision steps).
- Live re-derive at assembly: `.venv\Scripts\python.exe -m pytest tools/gps_mcp/test_gps_mcp.py -q`
  and a `report_capability` dump of the seeded ledger (`tools/gps_mcp/`).
- Shape: the capability table (model x task_shape x pass_rate x n x cost)
  followed by the three confessed birth defects (one-bit escalation, unverified
  evidence_hash, fixed 0.85 gate with no decay) verbatim from the receipt's
  "what the Opus spec-review should critique first".

### 2.2 The duel tier table, W8 + V1 + AH10 (2,200 B) - the meter measures quality-per-dollar

- Proves: blind-judged cross-family duels with metered costs produce a stable
  tier split, not vibes.
- Byte sources (all in `watch/inbox/last_mile_20260930/`):
  - `W8_MULTIFAMILY.md` - 12 duels, 4 families, 3 shapes; two-tier split identical
    in all 3 shapes: glm-prime 6-0, ds-v4.1-flash 6-0, grok-4.3 0-6, qwen3.7-flash
    0-6; p=0.0156 one-sided; every duel decisive.
  - `V1_MULTIFAMILY_DUEL.md` - 18 duels round-robin, perfectly transitive:
    grok-4.7 9-0, gemini-3.8-flash 6-3, ds 3-6, glm G3-reuse 0-9 (HANDICAP named,
    not a family verdict: it answered a sibling ask).
  - `AH10_GLM_VS_DS.md` - the owed tier-1 diagonal: glm-prime 2-0 in scored
    rounds, per-criterion 40/40 vs 10/40, one ds DNF round banked honestly.
  - Row truth: `logs/duel/duels.jsonl` (ids `w8-*`, `v1mf-*`, `ah10-*`).
- Shape: ONE merged table (family, W-L, avg criterion, per-answer metered cost,
  which receipt) plus the three standing disclosures: the W8 cycle blind spot
  (glm-vs-ds and grok-vs-qwen never met in W8; AH10 closes half), the V1 G3
  handicap, the ds thinking-off router law.

### 2.3 The LDT arc, four paragraphs (2,400 B) - we falsify our own theses honestly

One paragraph each, numbers from bytes:
- Origin, `watch/inbox/last_mile_20260930/V7_LDT_LATTICE.md`: the legality
  lattice as post-hoc projection lifts soundness 0.8830 -> 0.9862 at tau=0.7
  (val n=2000), deleting exactly the 195 cross-tier errors, keeping every
  correct answer; renorm preview 0.9806/0.9805 Pareto-dominates raw.
- v1 honest loss, `watch/inbox/last_mile_20260930/AH8_CONCEPT_LAYER.md`: the
  learned set-valued head TRADES (buys coverage +0.0050, pays soundness
  -0.0040; 46 wrong vs renorm's 38); the 1.95x data-efficiency claim does not
  transfer; no softened reading banked.
- v2 terminal, `watch/inbox/last_mile_20260930/IMP7_LDT_V2.md`: superset-target
  training TAUGHT the hedge (0 -> 555 hedges, every hedge contains the truth)
  and still trades; AH8's pre-registered falsifier fired both branches; the
  concept-layer thesis on this lattice is dead and renorm stands as the ceiling.
- Adversarial near-miss cure, `watch/inbox/last_mile_20260930/IMP9_NEARMISS.md`:
  600 propagator-verified one-edit twins; raw twin accuracy 0.2083 (250/600
  fooled to legal_gain) vs lattice 1.0000 with 0 fooled; renorm 1.0 coverage
  1.0 is a proof by construction; crown-physics tier deliberately untouched
  (originals only 0.4883 -> 0.6483).
- AE7 slot (adversarial NCP read): UNFIRED. Refire-queued with the AH queue
  (`watch/inbox/last_mile_20260930/AH_REFIRE_QUEUE.md` names it). If its receipt
  lands before assembly, it takes a FIFTH paragraph from its own bytes; if not,
  the arc ships as four paragraphs and AE7 is marked UNFIRED in the pack. Never
  summarized from the mission text.

### 2.4 The audit's health-check table (2,000 B) - the estate audits itself with fails visible

- Proves: we can see our own rot; the gap section (WHERE WE STAND) is fed by an
  instrument, not self-description.
- Byte source: `watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md` section 4,
  the 21-row table, tally 10 PASS / 8 FAIL / 3 WARN / 3 NOT RUN (run 2026-09-30,
  PowerShell + git + venv, no estate writes, no paid calls).
- Shape: the tally line plus every FAIL and WARN row compressed one-line-each
  (requirements.txt merge markers committed in HEAD; 372 dangling chain rows +
  618 evidence_lost + 2,821 amended; seed seal 56/57 with engines/key_law.py
  drift; census claim 2,436 vs 3,192 collected; 13 NEW ratchet violations;
  effect_broker denylist contains "" denying all URLs; 7 live secret values in a
  tracked trajectory file; offsite backup same-disk only). PASS rows summarized
  in one line. The point shipped to Opus: what we already know is broken.

### 2.5 Cost truth rollup (1,600 B) - every dollar counted

- Proves: cost truth is aggregated from four schemas, cross-checked, not
  estimated.
- Byte source: `watch/inbox/last_mile_20260930/IMP5_COST.md`; instrument
  `tools/cost_rollup.py` (read-only, 7 tests). Live run banked 2026-09-30:
  grand total $135.7095 over 25,376 calls across four surfaces
  (`logs/duel/duels.jsonl`, `logs/mates/*.jsonl`, `logs/hermes_gopher_burn_*`,
  `training/cost_ledger.jsonl`); independent raw-sum cross-check delta 1e-4.
- Live re-derive at assembly: `.venv\Scripts\python.exe tools/cost_rollup.py`
  and paste that day's grand total + trend.
- Pricing refs for the ask's own cost model:
  `watch/inbox/last_mile_20260930/V9_NOUS_PRICES.md` and
  `watch/inbox/game_platform_basecamp_20260929/COST_MODEL_OPUS_20260929.md`.
  This ask's model: 37,000 B prompt ~ 9.3k in-tokens at $4/M = $0.04; 64k
  max_tokens out at $20/M = $1.28 worst case; empirical anchor AA1 $0.69 at
  32k. Hard cap $5.00, carried by `tools/lensing_ask.py`.

### 2.6 Verkle chain stats (1,200 B) - the receipt fabric is real

- Proves: durable work is hash-chained and verifiable; the numbers are
  instrument output.
- Byte sources and live instruments:
  - `memory/biography/verkle_chain.jsonl` - the chain rows (byte truth at
    skeleton-writing: 8,670 lines; the audit read 8,626 leaves consistent in
    2.03s at its moment; both moments named, never differenced).
  - Pure-read verify: `mag/verkle_knot.py::_verify_chain_consistent()` (the
    audit's check 6) and `.venv\Scripts\python.exe main.py verkle-audit --dry`.
  - Party subchain: `memory/runs/party_subchain/` (audit check 9: 831 rows,
    0 errors, schema v1/v2 dual hash rule).
  - Seal: audit check 8 (19 files, 0 mismatches; pointer
    `state/seal_latest.json`).
- Shape: leaf count + consistency verdict + verify seconds + dangling/amended
  counts, each tagged instrument-and-moment. Row count always from `wc -l` on
  the file, never from a receipt's memory of it.

### 2.7 Prior frontier lensing on the meter's spec (800 B) - the ask builds on a return, not a blank slate

- Byte sources: `watch/inbox/last_mile_20260930/W4_OPUS_RETURN_20260930.md` and
  `AA1_OPUS_REFIRE.md` (same ask, sha b805548a, streaming SSE transport; $0.69
  metered; TRUNCATED at 32k: reasoning burned 29,476, sections C-G lost,
  section A complete).
- Shape: the three structural kills one line each (drift invisible inside our
  own budget; calibration certified from the wrong region; identity is a label
  not bytes) + the truncation disclosure. THE ASK's lens 1 explicitly asks
  whether these three kills generalize from the meter's spec to the whole route.

Pack budget check: 1,800 + 2,200 + 2,400 + 2,000 + 1,600 + 1,200 + 800 =
12,000 B. Matches section 1's slot.

## 3. THE ASK - wording draft (paste verbatim into section 7 of the brief)

You are lensing a route, not writing it. We hold the pen and the receipts; you
hold the judgment. Everything above is byte-backed by our own instruments; where
we mark UNPROVEN, treat it as unproven.

Answer in these six parts, each with its own header:

1. WHERE ARE WE WRONG. Name any route pitch that should not be climbed at all,
   and say what disconfirming evidence would change your mind. A pitch you
   cannot falsify, say so.
2. WHERE ARE WE WEAK. Pitch right but ordered wrong, or verified too thinly:
   name the pitch, the reorder, and the verification we should demand before
   trusting it. Our prior lensing (the meter spec return, pack 2.7) named three
   structural kills; state which of them generalize to the whole route and which
   were spec-local.
3. WHERE ARE WE BLIND. What failure mode is invisible to our instruments as
   built? Use the audit's FAIL rows (pack 2.4) as the floor, not the ceiling:
   what would a hostile operator or a captured model exploit that no receipt
   row catches?
4. PRIORITY ORDERING. Rank the route's pitches. Name the FIRST divergence from
   our order and the reason in one sentence. Cost-bind it: our metered costs
   (pack 2.2, 2.5) are the currency; a reorder must cite them.
5. THE COUNTER-ROUTE. If you held our budget and our estate, what would YOU
   climb first and why? Max three pitches, each with its falsifier and the
   instrument from our pack that would measure whether it worked.
6. MISSING BIBLIOGRAPHY. What should we be reading that our bibliography does
   not carry? Max five items, each one line on why it is load-bearing for OUR
   route, not generic.

Ask-shape laws (binding on us, from our own research): context-first, ask-last;
one shot, no follow-up turns; effort set to maximum; hostile second pass
expected - dissent plainly, sycophancy is noise we will discount; no praise; no
em-dash bytes; cite our sections by number when you touch them.

Output contract: markdown, six headers exactly as named above, each part
self-contained. Your return lands verbatim as THE_LENSING receipt; the delta
between your read and our own fleet's free-lens read of the same route is the
calibration data we are paying for, so where our fleet and you would disagree,
say so explicitly if you can infer it.

## 4. Assembly law (how the brief gets built)

1. Wait states: MC1, MC2, MC3, MC4 land + MC5 route v1 hardened (plan Phase 1).
2. Assemble `watch/inbox/mountain_climb/OPUS_BRIEF.md` by pasting dossiers into
   the section slots; regenerate the evidence pack FROM BYTES that day
   (section 2's re-derive commands); paste section 3's ask verbatim.
3. Gate: `.venv\Scripts\python.exe tools/lensing_ask.py --dry` - all four
   guards green (em-dash, size ceiling, budget headroom, sha recorded) with
   zero spend.
4. Fire ONLY on operator GO, via `tools/lensing_ask.py --fire` (streaming SSE,
   the AA1-proven transport; whole-response is dead for 32k+ Opus on this
   gateway). Nous 402 caveat carried: if the Nous pool reads dry
   (`AJ9_NOUS_402.md`), the carrier waits for credited Nous or an operator
   ruling on the Anthropic-direct route; it never silently switches routes.

## 5. Verification of this skeleton

- Every byte path named above was opened and read on 2026-09-30 from this seat.
- Chain row count measured `wc -l memory/biography/verkle_chain.jsonl` = 8,670
  (2026-09-30, skeleton-writing moment).
- Carrier dry-run executed 2026-09-30, zero spend, zero network:
  `.venv\Scripts\python.exe tools/lensing_ask.py --dry` against this skeleton as
  stand-in brief = all guards green (em-dash 0, 14,492B under the 40,960
  ceiling, worst case $1.294 under the $5.00 cap, sha asserted).
- Ratchet: zero NEW violations in tools/lensing_ask.py (283 lines, under the
  400 cap; the working tree's other NEW rows are sibling lanes' uncommitted
  files, untouched here).
- Em-dash count in this file: 0.

Skeleton written 2026-09-30 by the MC6 lane. MC5 slot intentionally empty.
