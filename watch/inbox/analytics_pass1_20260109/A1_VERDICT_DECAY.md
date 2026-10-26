# A1 verdict decay - analytics pass 1

- Seat: lane A1 (verdict decay). Moment of analysis: 2026-10-08.
- Source: memory/burns/LEDGER.jsonl, 705 rows, parsed with .venv\Scripts\python.exe json.loads per line.
- Ledger window: ts min 2026-09-25T10:05:50Z, ts max 2026-09-28T19:30:00Z (3.4 days).
- Caveat up front (census law): "week buckets" are impossible on this window; buckets below are days.
- Verdict field is not a clean enum; classes below are my normalization of raw values:
  landed/built 366, steal 210, green-ish 37, erratum 23, owed/blocked 23, free-text 14, correction 9, vacuous 9 (8 exact "vacuous" plus one "hold: ...neither stolen nor vacuous" string my contains-match caught).

## Day buckets (rows per day, from ts)

- 2026-09-25: 23 rows, 95.7 percent steal
- 2026-09-26: 517 rows, 68.1 percent landed/built, 15.5 steal, 0.2 vacuous
- 2026-09-27: 108 rows, 60.2 steal, 18.5 green-ish, 1.9 vacuous
- 2026-09-28: 57 rows, 75.4 steal, 10.5 vacuous, 3.5 landed
- Join: ts[:10] groupby over all 705 rows.

## STRANGE FINDINGS

### F1. Green is an exit, not a certification
- Datum: 24 of 470 slugs have "green" as their LAST verdict. Of the 12 slugs with 10+ rows, ten terminate at their first green and are never burned again (judge-lane-spec, steering-theory, prompt-uplift-lane, queue-field, rsi-harness, third-way-game, middle-path-doctrine, world-models-multi-agent, stego-canon-pipeline, adversarial-self-probes).
- Join: per-slug ts-ordered verdict sequence; first-green index vs sequence length. Only 6 slugs have ANY row after their first green (52 post-green rows total), and those 6 are dominated by the two evergreen topics in F2.
- This is the demotion gap made measurable: no mechanism ever demotes a green topic back into the burn queue, so its decay after graduation is structurally invisible. A green that is never re-queried is unfalsifiable by neglect.
- Confidence: high (mechanical over 705 rows).
- Falsifier: find a slug with a green row followed by 2+ later rows that is NOT doctrine-owed-chase or free-resource-landscape; none exists in this ledger.

### F2. Vacuous verdicts only exist where reburning continues
- Datum: all 8 exact "vacuous" rows sit in 5 slugs, each with 15+ rows (free-resource-landscape 4, doctrine-owed-chase 1, world-models-multi-agent 1, stego-canon-pipeline 1, adversarial-self-probes 1). 6 of the 8 land on the final day 09-28. The two most-reburned topics (doctrine-owed-chase 38 rows, free-resource-landscape 35 rows) hold 5 of the 8.
- The 09-28 free-resource-landscape vacuous run reads as stale-premise decay in the one_line field: "DeepSeek in-window debt NOT fired: the boards in-window premise was STALE at execution" (02:20Z) and the Lightning credits chase (12:15Z, 12:35Z, 12:55Z, three consecutive vacuous).
- Join: vacuous rows filtered by slug and ts, joined to per-slug row counts.
- So the ledger's decay curve is a selection artifact: topics that stay in rotation get caught decaying; topics exited at green (F1) cannot. Decay is real but only observable on the survivors.
- Confidence: high for the counts; medium for the interpretation.
- Falsifier: a vacuous verdict on a slug with under 5 rows; none exists in this ledger.

### F3. The verdict enum leaked into prose
- Datum: 44 rows carry a verdict value longer than 60 characters (full landing sentences, e.g. b2-02-writer-debt-backfill at 2026-09-26T12:25:00Z). 3 rows carry free-text in fresh_failure_mode instead of a boolean (e.g. "1302 ceiling found at width 15-16...").
- Join: len(str(verdict)) > 60 scan; type check on fresh_failure_mode (True 110, False 159, absent 433, free-text 3).
- Any downstream verdict-class counter that trusts the field as an enum silently fragments into 90+ distinct values; my own normalization had to fold them.
- Confidence: high (byte lengths).
- Falsifier: a schema doc declaring verdict/fresh_failure_mode free-text by design; none found in the row shapes.

### F4. fresh_failure_mode collapsed after day one
- Datum: fresh_failure_mode=true was 21 of 23 rows (91 percent) on 09-25, then 57 of 517 (11 percent) on the 09-26 flood, 26 of 108 on 09-27, 6 of 57 on 09-28; 433 of 705 rows carry no value at all.
- Join: ffm truthiness grouped by ts day.
- The field that named the founding lesson (quota-number drift as fresh failure mode, row 1) essentially stopped being maintained once volume arrived; post-09-25 ffm data is too sparse to support any drift claim.
- Confidence: high.
- Falsifier: rows after 09-25 genuinely having no fresh failure modes to flag; the 3 free-text ffm values landing on 09-28 argue the field was still alive, just malformed.

### F5. ts is filing time, not event time
- Datum: 636 distinct timestamps across 705 rows; 107 rows share an exact timestamp with at least one row of a DIFFERENT slug (40 such batch timestamps); 73.4 percent of all rows (517) fall on 09-26. Recurring topics share cycle timestamps (09-27T05:02Z carries doctrine-owed-chase, world-models-multi-agent, and stego-canon-pipeline rows).
- Join: Counter over ts, cross-referenced to slug sets per ts.
- Verdict-decay-by-time here measures the scout cadence as much as the topic: a scout reburns a topic list each cycle (median recurrence gap: doctrine-owed-chase 35 min, free-resource-landscape 60 min, middle-path-doctrine 55 min; doctrine's 09-28 tail runs every 25-30 min from 13:20Z to 19:30Z).
- Confidence: high.
- Falsifier: a writer (memory/burns tooling) documenting ts as event time; the batch structure argues otherwise.

### F6. The build lane never steals
- Datum: 452 of 705 rows (64 percent) are b2-* prefixed slugs; only 11 of them (2.4 percent) are steal. The 253 non-b2 topic rows are 199 steal (78.7 percent), 8 vacuous, 20 green.
- Join: slug.split('-')[0] == 'b2' (case-insensitive) crossed with verdict class.
- Steal and vacuous are research-verdicts; build rows land or erratum. The ledger is two ledgers interleaved on one ts axis, and any whole-ledger verdict mix (F5's day buckets included) blends them.
- Confidence: high.
- Falsifier: miscount from prefix matching (e.g. a non-wave slug starting "b2"); the 11 b2 steals are the only crossover either way.

## The demotion-gap lesson, stated from bytes
- The ledger shows: green exits are permanent for 10 of 12 heavy topics (F1); vacuous decay is only detectable in the 2 topics that ignored the exit (F2); the exit rule and the decay rule never co-occur on the same slug.
- Measurable form: post-green rows exist for only 6 of 16 slugs that ever went green; the 2 slugs with the most post-green rows are the only ones holding multiple vacuous verdicts.
- One-line law candidate: a green verdict without a scheduled re-burn is a certificate that cannot expire, and every decay curve built on this ledger will undercount decay by exactly the green-exited topics.

## Recurrence table (slugs with 10+ rows)

- doctrine-owed-chase 38, free-resource-landscape 35, middle-path-doctrine 30, world-models-multi-agent 19, stego-canon-pipeline 19, third-way-game 17, adversarial-self-probes 15, rsi-harness 12, judge-lane-spec 10, steering-theory 11, b2-wave-fold 11, queue-field 11 (raw Counter over slug).
- All 13 slugs with 5+ rows reached green at least once; zero slugs with 5+ rows stayed steal-only forever. The queue does converge; it just stops checking after convergence.

- Instrument note (census law): every count above is from .venv\Scripts\python.exe json parse of memory/burns/LEDGER.jsonl, 705 rows, run 2026-10-08; day buckets and class shares are single-moment snapshots of a file that sibling lanes may still be appending.
