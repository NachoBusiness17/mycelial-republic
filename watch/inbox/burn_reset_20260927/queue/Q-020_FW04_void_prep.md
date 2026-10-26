# Q-020 / FW-04 — Row-122 VOID prep packet (dry-run doc only)

- Date: 2026-09-28 · seat: queue-gopher2-Q-020 (workflow gopher) · cost: $0
- Plan: `memory/plans/fifty_wide_20260917.md:15` — "Row-122 VOID prep packet: second-seat nomination form + expected post-VOID linkage state, dry-run doc only"
- **Status change this packet records: the prep target already fired.** The plan staged this packet on 09-17 while the operator's word was pending; the operator's word landed 2026-09-27 ("No sacred cows these were all the best ideas we had at the time") and the VOID executed 2026-09-27T18:33:50Z. What follows is therefore (A) the nomination form as it was meant to be filled, kept reusable for the next defect, and (B) expected-vs-actual post-VOID linkage state, so the packet doubles as the retrospective the executed VOID never got.

## A. Second-seat nomination form (per the v4 admission law, `mag/grounding_wave.py:277-285`)

A void row only COUNTS when **cross-signed**: a later `kind:"witness"` row with `signs == <the void row's hash>` and `seat == <the void row's "witness" field>` — the void names its second seat; that seat must show up and sign the void itself. A void that is never cross-signed sits in `pending_voids` forever (a staged, inoperative act). Void-of-void is the reversal verb (same form, `voids:` the void's hash).

| Field | Value for the row-122 case |
|---|---|
| Target | `line:122` (the hashless row gets addressed by line number; `key()` falls back to `line:{i}`) |
| Reason code | `MALFORMED` (row 122: `prev` matches nothing, no hash key, truncated evidence — frozen that way 2026-09-16) |
| Author seat | zcode |
| **Second seat (nomination)** | **the operator** — a void of a SUPPORTED-tagged canon row is exactly the class the ladder reserves for the operator's word; the fleet's own seats are disqualified as second seat on the author's own row (the U5 lesson: witnesses catch folds, they don't pre-authorize them) |
| Execution verb | `python -m mag.grounding_wave void line:122 --reason-code MALFORMED --reason "…" --witness operator` (dry-run first) |
| Closing move | operator posts the cross-sign witness row signing the void's hash — `signs 52db99d28297 g1=True` is the shape |
| Falsifier | if the operator declines the word, the void stays pending and row 122 stays in the tape as a marked MALFORMED row — containment is never self-granted |

## B. Expected post-VOID linkage state (written as the 09-17 prep expectation) vs ACTUAL (verify run 2026-09-28)

| Expected (prep-time) | Actual (`python -m mag.grounding_wave verify`, exit 1, run this session) |
|---|---|
| `LINKAGE-PASS: N posts intact` — row 122 stays in the tape (append-only law: the VOID buries, it never deletes) | **MATCH** — "137 posts intact, tip=fc3c32be6f26" |
| row 122 defect reported as **"hashless defect contained by void"** (reported, not failed — `grounding_wave.py:738-740`) | **MATCH** — verbatim in the verify line |
| row 123's `prev` defect (the orphan head) reported **"prev defect contained by void"** | **MATCH** — verbatim |
| rows 124+ orphans: contained or **"re-anchored past voided stretch"** as fresh rows re-anchor the tip | **MATCH** — rows 129/130/132 re-anchored; 131 contained |
| ADMISSION shows ≥1 voided, **0 pending voids** after the cross-sign | **MATCH** — "3 voided, 0 contested, 0 corroborated, 0 pending voids, 3 propagation-flagged" |
| expected exit 0 (defect contained, evidence intact) | **MISMATCH — exit 1, but for an unrelated, pre-existing reason**: EVIDENCE-MISSING tokens on rows 75/76/86, whose files all exist on disk (checked by `ls`; the resolver just doesn't map the bare relative tokens). Verified in `Q-020_FW03_grounding_verify.md`. |

Full verify output quoted in `Q-020_FW03_grounding_verify.md`. Dry-run discipline held: nothing in this packet touched the chain — no rows appended, no render rebuilt.

## What the executed VOID actually looked like (for the record)

- Void row hash `52db99d28297…`, `voids: "line:122"`, `reason_code: MALFORMED`, `witness: "operator"`, evidence field carries the operator GO quote + the "Socratic equivalence grant (repair-with-receipt = ablation-with-rollback)" framing; cross-signed by the operator 2026-09-27T18:34:14Z (`watch/GROUNDING_WAVE.md` head rows).
- Same wave also voided: `d13acb95259e` (EVIDENCE_DEAD), `5b456eda969d` (SUPERSEDED), `ab48302c90a7` (EVIDENCE_DEAD), `d2c81c2dc98a` (MALFORMED — row 122's twin, the empty-prev variant).

## Form reuse note

The form above (target / reason code / author / nominated second seat / execution verb / closing cross-sign / falsifier) is the reusable packet — point it at the next `line:N` or hash the day one appears. The row-122 instance is closed and needs no further hands.
