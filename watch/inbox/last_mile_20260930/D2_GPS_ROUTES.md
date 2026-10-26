# D2 GPS_ROUTES - the meter routed its first real decision - 2026-09-30

Mission (operator, "dogfooding our systems"): the GPS meter is supposed to route
model choice. MAKE IT ROUTE THIS WAVE. Ownership: this receipt +
tools/gps_mcp/router.py (extended). Verdict up front: the meter now picks duels
from its own momentum-badged table, and the answer for the next duel is BANKED:
anchor x-ai/grok-4.7 vs challenger google/gemini-3.8-flash, judge
fireworks/ember-1, receipt row 2026-09-30T23:13:38Z in
tools/gps_mcp/receipts.jsonl. Convergence with the animal rib holds everywhere
the rib has receipts; the four wave shapes are all unmeasured (the census).

## 1. The capability table, read first (pre-D2 state)

tools/gps_mcp/gps_ledger.db3 held 3 rows, all real wave work, zero of them the
seed fixtures (those were wiped when real data landed):

| model | shape | pass_rate | n | momentum |
|---|---|---|---|---|
| legality-propagator-v1 | legality-water-graph-v1 | 1.000 | 100 | STEADY, STREAK-100 |
| z-ai/glm-5.3-prime | night-judgment | 0.833 | 6 | DECLINING (1.0 start, 0.667 recent) |
| mountain-world-v0 | world-tick | 1.000 | 4 | STEADY, STREAK-4 |

## 2. The meter's answer for the four wave shapes

Live JSON-RPC through `python -m tools.gps_mcp.server`, four `ask` calls
(receipts 23:08:42Z):

- code-building -> flash-mid-1, exploration: "no ledger history"
- spec-review -> flash-mid-1, exploration
- creative-writing -> flash-mid-1, exploration
- data-extraction -> flash-mid-1, exploration

The meter had NO real recommendation for any task type this wave runs. Its
"recommendation" was the designated exploration test-double. That is the honest
pre-wire state: the meter cannot route the wave it lives in.

## 3. The wire (router.py extension, the code that made it route)

- `import_duel_bank()`: feeds logs/duel/duels.jsonl (the fleet's own bank, 74
  rows live) into the ledger via the sanctioned writer `record_verdict`, one
  verdict per (duel, contender), evidence_hash = sha256 of the canonical banked
  row (README growth item 1, verification-gate direction, cheap slice). Rubric
  is the shape key (frozen map, seven rubric sets -> five shapes, citations in
  the code: W8_MULTIFAMILY, LW9_DUEL_N30, AH10, V1). Skips named: altjudge
  rows (re-judge of already-counted answers, would double-count), TIE rows,
  unknown rubrics (refuse, never guess). Idempotent on the evidence hash.
- `pick_duel_contenders()`: the momentum-badged table picks anchor (top
  measured), challenger (highest-ranked DIFFERENT family), judge (first
  preferred judge from neither family; altjudge replay stays the second judge
  owed). No rows for the shape -> the gap is named, it refuses to pick from
  vibes.
- CLI: `.venv/Scripts/python.exe -m tools.gps_mcp.router duel-import` /
  `duel-route -s <shape>`.

First import: 62 rows fed, 124 verdicts. Re-run caught an idempotency bug I
then fixed (bare digest vs duel:-prefixed comparison never matched, re-run
double-fed; repaired byte-honestly by restoring the pre-feed backup
gps_ledger.db3.bak_pre_D2_20260930 and re-importing once; fix comment carries
the cause). Post-fix re-runs: fed 0, duplicate-skipped 63. The 63rd row is the
living-wire proof: sibling lane D6AB banked a fresh duel (d6ab-r1-glm-gem,
23:12:33Z) WHILE this lane worked, and the re-import picked it up unprompted.
Post-feed table: 24 capability rows, 236 verdict_log rows.

## 4. The routing decision (the receipt the mission asked for)

Query: `duel-route -s adversarial-review` (the shape the fleet duels most: 33
fed duels; also the tier-1 judgment shape per AH10/W8). Answer, from the
momentum-badged table, not vibes:

| rank | model | pass_rate | n | momentum |
|---|---|---|---|---|
| anchor | x-ai/grok-4.7 | 1.000 | 9 | STEADY, STREAK-9 |
| challenger | google/gemini-3.8-flash | 0.633 | 10 | STEADY |
| 3 | qwen/qwen3.8-max-prime | 0.444 | 9 | RISING |
| 4 | z-ai/glm-5.3-prime | 0.409 | 22 | DECLINING |
| 5 | deepseek/deepseek-v4.1-flash | 0.385 | 13 | DECLINING |
| 6-7 | qwen3.7-flash, grok-4.3 | 0.000 | 2 | STEADY |

The next adversarial-review duel fires grok-4.7 vs gemini-3.8-flash under
ember-1. Operator override remains theirs (grok is $0.23/answer, slow; a
crown-defense rematch of a known 3-0 pairing is what the table says, not
necessarily what the wallet wants). The SELECTION is the deliverable: it came
through the meter with an audit row.

## 5. Convergence check vs the animal rib (RIB_MODEL_GATES_20261001)

Where the meter now has data, every rib claim holds (disclosure: the rib was
distilled FROM these same duel receipts where it cites V1/W8/AH10, so
convergence there is by construction, not independent confirmation):

| rib claim | meter row | verdict |
|---|---|---|
| grok-4.7 adversarial champion 9-0 V1 | adv 1.000 n=9 STREAK-9 | CONVERGES (circular) |
| gemini 6-3 V1 format champion | adv 0.633 n=10 | CONVERGES (circular) |
| ds: schema/plan yes, adv degraded | plan 1.000, schema 1.000, adv 0.385 | CONVERGES (circular) |
| qwen flash sensing only | 0.000 n=2 on three shapes | CONVERGES (tiny n) |
| grok-4.3 different animal, sensing | 0.000 n=2 on three shapes | CONVERGES |
| glm workhorse+judgment tier | adv 0.409 DECLINING, grading 0.750 RISING, night-judgment 0.833 DECLINING | NUANCED |

The only non-circular signal is night-judgment (not duel-derived): 0.833 keeps
glm at the top of judgment-family rows (agrees with the rib's crown), but the
DECLINING window (1.0 -> 0.667) is information the rib's flat label cannot
hold. That is the division of labor: the rib carries the animal's harness laws,
the meter carries rates, direction, and sample size.

## 6. Coverage gap census (shapes the fleet runs, the meter never measures)

Still dark post-feed, all four wave task types among them:

1. code-building (the wave's largest lane: B4 SRP6 port, B2 event ring,
   worldgen) - 0 rows
2. spec-review - 0 rows
3. creative-writing (B14 title, LM5 legends) - 0 rows
4. data-extraction (IMP10 counts, censuses) - 0 rows
5. also: summarize/yes-no shapes (seed fixtures wiped), the mates' hunt-ground
   missions, essay/ractor shapes

Pattern law: the meter only measures shapes that already have a round-trip
verdict harness (duel rubrics, legality fixtures, world ticks, night burns).
A shape with no judge stays dark forever. Closing any gap means standing up a
verdict path for it, and the duel bank feed (now idempotent, rerunnable after
every duel) is the template.

## 7. Verifications + notes

- Tests: `pytest tools/gps_mcp/test_gps_mcp.py -q` -> 41 passed (suite uses
  temp ledgers; the real ledger untouched by tests).
- receipts.jsonl: 11 rows banked this lane (4 server asks, 7 duel-routes incl.
  the 4 gap refusals).
- Semantics disclosure: duel-fed pass_rate is judged WIN-RATE on the shape
  (relative, blind judge, position-swap alternated; LW9 measured residual
  slot-A bias p=0.0436), not absolute correctness; legality/world rows are
  absolute. Code docstring + this receipt carry the distinction.
- LM7 floor observed live: gemini's adv rate reads 0.633 with 6 honest wins of
  10 because one fail landed while its window was RISING and was floored to
  the window-start rate (it logs, it does not punish); momentum still shows
  the trend. Working as designed, first live sighting.
- Debt named for the spec owner: README.md's router.py row ("ask() and
  cascade() routing rules") now understates the file (it also owns the duel
  import + duel route wiring). One-line README edit is the gps spec owner's
  call, not this lane's (ownership fence).
- Backup tools/gps_mcp/gps_ledger.db3.bak_pre_D2_20260930 (pre-feed, 3 rows)
  kept for audit; delete after the operator is satisfied.
- Zero em-dashes in this receipt (byte-checked) and in the code comments.
