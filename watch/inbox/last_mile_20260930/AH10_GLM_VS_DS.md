# AH10 - GLM-PRIME VS DEEPSEEK HEAD-TO-HEAD (W8 owed tier-1 diagonal) - 2026-09-30

Mission (operator, refire of the AH10 row that died on 1302 in the refire
queue): 3 rounds of the SAME adversarial-review ask on
watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md sections 4 and 5,
with AMENDMENT 7 (and its AH11 batch preamble) embedded in the ask text so
both contenders review the CURRENT controlling spec. Ember blind judge,
position swap each round. Laws honored: deepseek THINKING OFF (mandatory,
the W8 router row for this gateway), glm-prime normal (reasoning capped
6000), cap $0.50, DNF banked honestly, keys from
C:\Users\foste\AppData\Local\hermes\.env with NOUS_SDD_API_KEY first
(one key loaded, probed live before every fire batch).

## Design

- Ask: 7,681 chars, built from byte-faithful slices of the spec (section 4
  start through the line before "## 6." = 4,262 chars; AH11 batch preamble
  through end of file = 2,158 chars) plus framing. Demands THREE defects
  (name, clause, quoted evidence, falsifying test predicate), ONE missing
  safeguard, ranked by damage, UNPROVEN marking, no invented defects.
- Contenders: a = z-ai/glm-5.3-prime (harness-standard call: temp 0.4,
  16000 max tokens, reasoning max_tokens 6000, 900s socket); b =
  deepseek/deepseek-v4.1-flash thinking-off (reasoning enabled false, 8000
  max tokens, the W8 call_ds shape; 900s socket for round 1, tightened to
  360s for the refire + round 3 after the first hang, evidence: 38s and
  197s were the known good bounds).
- Rounds fire FRESH answers per round; logical roles fixed (glm = a,
  ds = b) so the banked winner always reads in the same terms; the
  harness v1.1 auto-picks the presentation swap from ledger parity, which
  alternated across the scored rounds (r1 swap true, r3 swap false).
- Judge: fireworks/ember-1, blind (A/B only), rubric root cause accuracy,
  evidence citations, falsifying predicates, actionability (the W8 adv
  rubric, kept for cross-receipt comparability). Per-criterion scores
  banked in the rows, remapped to logical contenders.
- Idempotent: banked ask_ids skipped; budget gate before every round.

## RESULT: glm-prime 2-0 in scored rounds; round 2 was a ds DNF

| round | swap | winner | crit scores glm vs ds | costs glm/ds/judge |
|---|---|---|---|---|
| ah10-r1 | true | glm | 5-1, 5-2, 5-1, 5-0 | $0.0284 / $0.0006 / $0.0183 |
| ah10-r2 | (no row) | DNF (ds) | none: ds never delivered | glm paid $0.0325 then $0.0269 on refire, both lost to the ds DNF |
| ah10-r3 | false | glm | 5-2, 5-2, 5-1, 5-1 | $0.0313 / $0.0005 / $0.0181 |

Per-criterion totals over scored rounds: glm 40/40, ds 10/40. Corr ids:
r1 c0b2a0d0, r3 55c80599 (per-process mints; the r2 DNF processes banked
no row so minted nothing durable).

Judge rationales (logged in SLOT terms; r1 slot A = ds, r3 slot B = ds,
so "A collapses" in r1 and "B self-admits fabrication" in r3 both name
deepseek): r1 "A collapses into nonsense mid-answer; B delivers three
provable defects plus safeguard with exact quotes and tests." r3 "A is
rigorous, quoted, testable; B self-admits fabrication and ends in
incoherent run-on prose."

Byte evidence (round 3 ds tail, verbatim excerpt, the degeneration is in
the answer itself, not just the judge's claim): "...unbounded time
allotted generously unlike today evidently insufficient manifestly
demonstrated conclusively hereby admitted freely candidly openly
shamelessly finally resting defense rested forevermore amen". The round 1
ds answer drew the same mid-answer collapse verdict; ds answers carry 0
markdown headers vs glm's 4, both consistent with run-on prose.

Substance note (what glm actually found, for the spec owner): all three
glm generations converged on the SAME residual family around Amendment 7:
(1) 4.1 rule 2's "n >= n_min" boundary still reads raw n (Amendment 7's
own closing words: "Drafted but NOT applied... rule 2's n >= m boundary
reading n_eff"), so G3 volume can still pass the gate; (2) pure-G3 cells
with zero fail evidence bypass the fix entirely (the "case B in AH11"
residual: no weight-share cap); (3) loose ends like "lb95" naming and
which fallback controls when 4.1 and T4 point at different models. These
are the same kills the AH11 receipt already lists as unapplied drafts:
the duel independently re-derived them from the text alone.

## The ds DNF, banked honestly

Round 2: glm answered in 32s ($0.0325, 5,057 chars), then ds hung on the
socket read and timed out TWICE at 900s ("The read operation timed out",
zero response body both attempts). Refire (labeled ah10-r2, never banked
before): fresh glm again answered (31s, $0.0269, defect 1: pure-G3 cells
bypass the Wilson fix), ds timed out twice more at the 360s bound. Round
3: ds attempt 1 timed out, attempt 2 landed (186s, $0.0005). Net: ds hung
5 of 7 attempts across the series; both answers that DID land degenerated
into word-salad tails. No DNF row shape exists in the ledger schema
(inventing one would corrupt the router feed), so the DNF lives here and
in the run logs only.

## Spend (cap $0.50)

- Banked ledger rows: $0.0972 (r1 $0.0473 + r3 $0.0499).
- glm answers orphaned by the r2 DNF: $0.0594 ($0.0325 + $0.0269).
- Key probes: 3 x ~1e-5, negligible.
- Unmetered worst-case bound for the 5 timed-out ds attempts (no response
  body, so no usage.cost; bounded at 8000 out tokens x $0.63/M): ~$0.025.
- TOTAL ~$0.18 worst case, ~$0.157 metered. Under cap with room.

## Router rows this feeds

- glm-prime: QUALITY lane confirmed on adversarial-review; 2-0 here, 20/20
  criteria, ~$0.03 per answer. Also: three independent generations
  converged on the same defect family, a stability signal.
- ds-v4.1-flash: WORK lane with TWO attached constraints on this gateway:
  thinking-off only (W8 law, restated) AND adversarial-review shape
  degraded: 0-2 vs glm with degenerated tails, plus 5/7 hangs this
  session. W8 caveat stands: its 2-0 adv record there was THINKING-ON
  ($0.0103, 92s), so the shape verdict is thinking-off-specific. Keep ds
  for schema/plan shapes per W8; do not route adv to it thinking-off.

## Disclosures

- The r2 refire re-paid glm because the first r2 glm answer was lost with
  the DNF'd process (contender texts are not banked by the harness; only
  head/tail excerpts were printed to the run log, quoted above).
- The 360s ds socket tightening on the refire + r3 is an operational
  bound change, not a model-config change; disclosed here because round 1
  ran at 900s.
- Judge criteria notes are slot-terms while scores are logical-terms (the
  harness remaps scores only); the swap fields in the rows resolve which
  slot held whom.
- Zero em-dashes in this receipt (byte-checked) and in the ask.
