# break-economics: hostile second pass on the economics lens (2026-10-02)

Sitting: byte-checked all 4 findings of the economics lens against the estate, ran every
falsifier reachable from this seat. NOT run (same admission as the lens): any provider-side
credit-balance API probe; per-provider price-sheet math; TICKET_LEDGER redemption rows.
All sums below were computed this sitting with the repo venv (scratch scripts in
%TEMP%\break_econ.py and %TEMP%\break_econ2.py) over the ledgers as they stood
2026-10-02T06:29Z; the descent driver was still live, so the two memory/runs ledgers are
append-moving instruments (row counts can only grow).

## Verdicts

### F1 (cost_rollup blind to both live ledgers, $41.23 invisible) - CONFIRMED
- tools/cost_rollup.py:42-45 is exactly the four surfaces (logs/duel/duels.jsonl,
  logs/mates/*.jsonl, logs/hermes_gopher_burn_*/*.jsonl, training/cost_ledger.jsonl); the
  adapter seam is tools/cost_rollup.py:115-116 (`_scan_jsonl`, docstring "schema adapter
  seam"). Leg-8 cite memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:54-56 byte-matches
  ("every turn banks tokens+cost (memory/runs/hermes_burn/usage.jsonl)").
- Sums reproduce exactly: hermes_burn 236 rows $37.7591; model_garden 725 rows $3.4746;
  union $41.2337.
- Falsifier ran clean the hard way: live `python tools/cost_rollup.py --days 3` scans
  exactly the four surfaces, neither memory/runs ledger appears anywhere in its output.
- Sharper than the lens said: watch/inbox/COST_TRUTH_20260930.md already names the disease
  class ("The rollup also undercounts: it scans only the four surfaces. Receipt-side burns
  with raw files elsewhere add $1.2208 today") and predates both ledgers (09-30 vs ledger
  first rows 2026-10-01T17:55Z / T22:10Z). This is the second instantiation of a receipted
  undercount in 24h, not a novel gap.

### F2 (ledger cannot mark bought-vs-theater; 67.6 pct same-turn refire; raw sums inflate ~3x) - CONFIRMED
- Group-by (id,turn) over memory/runs/hermes_burn/usage.jsonl: 24 repeat groups, 165 extra
  rows, $25.5316 - all three EXACT. A1_steer_antiforgery turn 1: 49 rows $20.9891 (lens:
  49/$20.99). 25.5316/37.7591 = 67.62 pct. First-per-group cost $12.2275; 37.7591/12.2275 =
  3.09x ("~3x" holds).
- Schema: three keysets on the 236 rows (141/89/6 split; the 89 carry `refused`, all with
  cost_usd 0.0). No bought/theater marker field exists. The 89 ok=False refusal rows are all
  $0.00, so refusal loops inflate row counts, never sums - the whole $37.76 is ok=True.
- tools/hermes_burn.py:24-25 documents the A1 disease (45x/$20.53 - historical; ledger now
  reads 49/$20.9891, the docstring figure is 4 rows stale, cosmetic); :388-395 prints the
  raw-sum total, observed live doing it: driver.log tail "HERMES-BURN: PASS ... ledger total
  $37.76" (the inflated number, printed every cycle).
- Falsifier tested and closed: memory/plans/hermes_burn_refire/A1/ask.json stages the SAME
  id "A1_steer_antiforgery" (revision:false, revision.md present) - deliberate refire
  staging exists, but same id+turn means the ledger still cannot separate sanctioned refires
  from theater, which is the finding.

### F3 (check-then-act landed-skip race, no lock; "40.8 pct of overnight hermes spend through that race, $2.25 of $5.52") - WEAKENED
Mechanism confirmed and improved; the headline number is misattributed ~2x.
- Code all byte-matches: tools/hermes_burn.py:210-218 entry output-exists check, :317 the
  call, :354-358 out_path written after; read the full file - no lock/O_EXCL anywhere.
  scripts/descent_driver.sh:14-28 loop + sleep 45, no lock; no DRIVER_STOP file exists;
  driver live (driver.beat "BEAT 2026-10-02T06:29:01Z cycle=593" at my 06:29:03Z read).
- Night subset EXACT: 43 rows $5.5208; 13 same-(id,turn) pairs; DUEL2_train_09_r2 at
  21:47:10.827196Z and 21:47:12.909771Z, identical 5944/8000 tokens, $0.0919 each.
- THE CATCH: $2.2521 is the sum of BOTH members of the 13 pairs (pair-total). The
  race-marginal duplicate is the extras only: $1.1292 = 20.45 pct of $5.5208, not 40.8.
  The first member of each pair is the ask's legitimate fire; and since the _r2 asks rode
  the turn2_only re-open door, a single-loop world still re-fires them per cycle - so even
  $1.13 overstates what the lock alone saves. The lens summed both copies of each
  double-fire and billed the pair to the race.
- STRENGTHENED beyond the lens's own admission ("did not identify the second executor"):
  the second executor is a SECOND CONCURRENT descent_driver.sh INSTANCE. driver.log
  interleaves two cycle counters from a 19:17:13Z restart onward (line 449
  "[driver cycle 1 19:17:13Z]" while loop A continues 13,14,15...; first 30 headers
  alternate 1..12 / 14,15,16 / 3,4,5...), and both sweeps fired the same _r2 asks for real
  money (log blocks at ~5330-5345 and ~5370-5385 both show train_05_r2..train_12_r2 firing
  $0.07-$0.09). driver.beat carries only ONE counter (unique cycle numbers over 583 lines;
  593 at 06:29:01Z) while the log's other counter is at ~653 - the second loop does not
  beat. The 13 pair deltas (0.5s to 60s) are two loops sweeping the same queue.
- Cleanup claim verified: 28/28 duel2 ask dirs, 0 revision.md anywhere under the plan dir;
  the string turn2_only survives in 14/28 ask.json but train_09_r2 reads revision:null,
  turn2_only:false - the door is closed by field falsification, not key removal (lens's
  "stripped of revision.md/turn2_only" is loosely worded, substance right). No code in
  tools/, scripts/, or mag/ deletes revision.md (grep) - the cleanup was out-of-band, as
  the lens said. guard_terminal (mag/inference_budget.py:343-366) banks only EMPTY_REASONING
  rows (turn=None, ok=False) and returns terminal, so there is no in-process double-bank
  path - the pairs are genuinely two fires.

### F4 (banking habit byte-exact; funded balance is prose only) - CONFIRMED
- NIGHT_CLOSE_20261002.md:52-56 reproduces to the fourth decimal AND the token counts are
  byte-exact: my sums 43/$5.5208 (hermes, ts>=21:31:24Z), 725/$3.4746 (MG), and
  5,547,496 total / 3,515,869 prompt / 1,202,028 completion / 829,599 reasoning - all four
  token figures match :55-56 exactly.
- Cheap-first: my recount of MG models is glm-5.3-flash 334 + deepseek-chat 151 +
  moonshotai/kimi-k2 121 = 606 (plus 1 "z-ai/glm-5.3-flash" alias = 607), qwen3.8-max-prime
  25, grok-4.7 25. The lens's "605/725" is unreproducible by 1-2 rows (direction unaffected;
  cheap-first is real either way).
- Balance prose-only, verified: no spend_balance.json or any deriving file exists (find over
  the tree); `git grep -nI "47\.54"` text hits are timestamp substrings
  ("2026-08-12T07:24:47.546609Z" in biography verkle backups) and PDF page-stream noise -
  no prose anchor. The figure lives only in commit 0c9d72a06's message ("$47.54 live
  balance", "Ledger ~$42 of 145"); AGENTS.md carries $220 armed (line 5) and $180 Nous
  (line 32); tools/hermes_burn.py:3 says "spend 70+$". Three-plus unreconciled money
  figures, zero ledger-derived ones - as the lens said.
- Not re-verified by me (accepted from the lens + NIGHT_CLOSE:30-33): the TICKET_LEDGER
  redemption/promotion split.

## What the lens missed (additions)

1. The second executor is named now: two concurrent descent_driver.sh instances (evidence
   in F3). Move: before or with the 40-min lock, stop one instance (touch DRIVER_STOP,
   restart a single loop) - the lock alone leaves two loops doubling sweep pressure on the
   same queue. ~10 min.
2. Restate F3's headline: race-marginal cost is $1.1292 = 20.45 pct of night hermes spend,
   and the turn2_only per-cycle re-fire door (which re-fires even single-looped) owns part
   of that; $2.25/40.8 pct double-bills the pair. The right split for the receipt: door cost
   vs race cost, not pair-total vs night total. ~0 min (a correction line).
3. tools/model_garden.py:233-243 ships the SAME unlocked _landed_skip (out_path.exists()
   entry, turn2_only re-open, no lock), and the model_garden ledger has its own repeat
   disease my pass found: 8 repeat (id,turn) groups, 21 extra rows, $0.6834 = 19.7 pct of MG
   spend (garden-v1-B1 n=3 $0.6834, B5 n=3 $0.6817, B6 n=7). Both the lock fix and the
   bought/theater split must cover the MG writer or it re-fires the same disease. ~15 min
   extra on each move.
4. The refire marker the lens proposes to invent already exists in-repo: 5 MG rows carry a
   literal refire field (garden-v1-B6/B8, local gemma rows at $0.0). Reuse that convention
   for the hermes backfill instead of a new sidecar schema. ~0 min (design note).
5. COST_TRUTH_20260930.md makes F1 a recurrence, not a discovery: the rollup's undercount
   was receipted 09-30 and two new ledgers opened unplugged the next day. The durable move
   is a surface census in cost_rollup (fail loud on any *.jsonl under memory/runs/ carrying
   cost_usd that is not a registered surface), not hand-adding two paths. ~30 min.
6. Cosmetic but quote-risk: tools/hermes_burn.py:25 still cites the A1 disease as "45x at
   $20.53"; the ledger reads 49 rows / $20.9891. Future seats quoting the docstring as
   current will bank a stale number. ~5 min.

## Checks run this sitting (the ask's scale)

- Ledger sums/group-bys: repo venv python over both ledgers (236 + 725 rows, full-population,
  not samples): totals, keysets, (id,turn) repeats, night cut at 2026-10-01T21:31:24Z, token
  sums, model mix, MG repeats, refire rows.
- Code reads: tools/cost_rollup.py, tools/hermes_burn.py, scripts/descent_driver.sh (full),
  tools/model_garden.py (gates + bank paths), mag/inference_budget.py guard_terminal,
  memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:40-75, watch/inbox/NIGHT_CLOSE_20261002.md
  (full), watch/inbox/COST_TRUTH_20260930.md (head + coverage grep).
- Greps/censuses: driver.log cycle-header interleave + duplicate census + bracket headers;
  driver.beat duplicate census + tail; DRIVER_STOP existence; duel2 ask-dir census (28 dirs,
  0 revision.md, 14 turn2_only strings with train_09_r2 field-level read); refire plan dir
  ids; spend_balance find; git grep "47\.54" (all + text-only).
- Live run: `python tools/cost_rollup.py --days 3` (four surfaces only, unparseable: none).

Filed by break-economics, 2026-10-02T06:4xZ. No em-dash bytes.
