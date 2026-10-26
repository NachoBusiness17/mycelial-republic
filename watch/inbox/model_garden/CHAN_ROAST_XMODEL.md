# CHAN_ROAST_XMODEL - lane X4 verdict (2026-10-01, cross-model program)

Lane: X4 CHAN ROAST (dogfood the roast board on the families' own claims). Instrument: the REAL
board writer, mag/chan.py post() into watch/room.jsonl (threads x4-roast-1-threat-model,
x4-roast-2-spend-ceiling, x4-roast-3-driver-race; 16 posts: 3 OPs + 1 OP receipt-drop + 12 family
rounds). Nothing simulated; every family post was fired by a cheap lane and posted verbatim under a
family seat. Cross-family disagreement sources: GRID_kimi1.json, GRID_ANTHROPIC1.json,
GRID_fable1.json, GRID_cheapgrid1.json + garden-v1 outputs. CROSS_RACTOR_MATRIX.md has NOT landed;
GARDEN_RACTOR.md (project charter) was read, no matrix rows to borrow.

HONEST CAVEAT FIRST: the premium families did not argue in person. deepseek-chat (ds_workhorse,
thinking off) carried kimi's and fable's and the board-law cases; glm-5.3-flash (garden runner,
zai lane) carried sonnet's and the WAVE24 cases and defended its own B1 claim in thread 3. Every
concession below is an ADVOCATE's concession on the record, not the premium family recanting.

Surface drift note: premium grids ran hermes_burn sha 9c8a0c1a; the tree moved to 91453258 before
this lane (guard_terminal now reads finish_reason at :323 and banks EMPTY_REASONING at :324).
Threads argued both shas explicitly.

## THREAD 1 x4-roast-1-threat-model: kimi's attacker framing vs sonnet's self-harm framing

The disagreement (from the grids): kimi-k2 B1 ranked meta['id'] traversal write (:263 today) +
evidence traversal read (:132) + DNS TOCTOU (:95-126) as the top defects; sonnet-5.5 B1 ranked
unbanked empty responses, unread finish_reason, and a 302 bearer-key leak as the top defects.
Same file, opposite threat models (hostile stager vs provider misbehavior).

Rounds: kimi-ds argued the partial-trust-seat stager surface (the driver docstring itself says
seats stage asks); sonnet-glm conceded the patched halves (finish_reason + EMPTY_REASONING
banking) and narrowed to the live halves (EMPTY_OTHER still raises unbaked at :344-345;
reasoning-channel fallback at :326-329 still lands chain-of-thought as the permanent deliverable).

OP receipt between rounds (live byte test, this host, python 3.11.15): a 302 to a second host
showed the Authorization header PRESENT at the redirect hop and STRIPPED at the final host
(urllib also converted POST to GET). Sonnet IMP3's bearer-walks-off half is FALSE ON BYTES for
this runtime - that claim had scored 5/5 checks in GRID_ANTHROPIC1.json B1.

Concessions on the record:
- sonnet-glm conceded severity: traversal write+egress "the box beats the wallet", kimi's pair
  outranks on severity.
- kimi-ds conceded the ranking on expected cost and DEMOTED ITS OWN #1: final ranking by kimi's
  own advocate: (1) EMPTY_OTHER unbanked + unbounded 45s refire (no precondition), (2)
  reasoning-as-deliverable, (3) traversal pair (needs a poisoned evidence file), (4) DNS TOCTOU
  (needs network position). Also flagged kimi IMP1-3 mixes two different attackers (insider seat
  for traversal, network position for TOCTOU) under one framing.
Residual ambiguity: severity (kimi) vs expected frequency (sonnet) as the top-defect criterion,
given both fixes are one cheap hunk each. Synthesis on the record: land three hunks (id/evidence
path validation; bank-before-raise at :344; finish_reason floor at the fallback), thread closed.

## THREAD 2 x4-roast-2-spend-ceiling: fable's no-ceiling claim vs the WAVE24 runway math

The disagreement: fable-5.1 B3 IMP1 (sonnet B3 convergent) - the paid loop has no spend ceiling
in bytes, the $145 stop is a hand-made STOP file, "the board's $145 stop is enforced by no byte
in the driver" (descent_driver.sh:14-21). WAVE24_BOARD.md's honest-runway section - three
denominators, refresh law every $10, falsifier re-read after 6 clean driver hours, STOP is the
operator-held brake by design. Live fuel: ledger had crossed the refresh threshold ($31.34 ->
$37.76) with no section refresh, DRIVER_STOP absent.

Rounds: fable-ds held "monitoring is not a halt", named unpatched bleed classes (new ask family
looping, paid empties, retry storm), and put the falsifier on the same human hook the refresh
just missed ("last fired on bytes: never"). board-glm owned the missed refresh, argued a rotted
ceiling HALTS a healthy wave while a rotted snapshot only misleads, and that fable's STOP-at-cap
is a silent unwitnessed halt.

Concessions on the record:
- board-glm conceded the structural point: "calling my spreadsheet a mechanism and theirs a wish
  was the wrong cut. Both were human-gated."
- fable-ds conceded the "no ceiling" half of fable's original claim dies IF the cap alerts.
Synthesis both advocates signed: ALERT-CAP patch - driver reads usage.jsonl each cycle, and past
CAP_WARN (default 130) appends one timestamped row to the standing attention surface; no exit,
no break, STOP stays operator-held, the cap never halts.
Residual ambiguity: whether an alert byte nobody is watching is a mechanism or "a second, slower
wish" - and the board-glm counter-falsifier: if the alert fires and no human lands STOP within
one $10 window, a coded halt becomes the honest fix.

## THREAD 3 x4-roast-3-driver-race: glm's double-burn race vs the board's disjoint-dirs law

The disagreement: glm-5.3-flash B1 IMP2 - no cross-process lock on the landed/refused gates and
ledger appends, two concurrent drivers double-burn (cite :266-284,348-354). WAVE24 HONEST GAPS -
the driver is 1-wide by design; N drivers go on DISJOINT queue dirs, so the sanctioned shape has
no race.

Rounds: board-ds held the sanctioned-shape defense and showed torn ledger rows are an accounting
undercount, not a re-burn. glm53flash conceded the lockfile cure (msvcrt stale-lock hangs the
paid lane) and narrowed its own claim to "milder poison" (torn refusal row delays the REFUSED
marker by one paid fire, bounded).

OP fact-drop that turned the thread: glm's round-1 justification cited an "out-prefix law" that
DOES NOT EXIST IN BYTES. tools/hermes_burn.py:60 - OUT_DIR is ONE shared directory for ALL
queues; :263 out_path = OUT_DIR / f"{id}.md. Disjoint-dirs disjoins the queues, NOT the
deliverables: two sanctioned drivers with colliding ask ids collide on the same out_path, and
exists-then-write is check-then-act, so the double-fire is reachable INSIDE the sanctioned shape.

Concessions on the record:
- glm53flash: "my gate justification was vibe wearing a citation" (the out-prefix law), and the
  torn-ledger half is an undercount, not the double-burn.
- board-ds: lockfile dead (agreed both sides); glm's O_EXCL claim file "fences more than the
  ledger" (it keys on the shared out_path, so it fences the deliverable collision too); but it
  adds a 950s steal timer the ops doc never authorized, so "no behavior risk" is false.
Residual ambiguity (the actual end of the argument): WHO enforces id hygiene - bytes (claim file
or id regex at entry, the same validation hunk as thread 1's kimi fix) or the ops-doc convention.
glm53flash's own closing: id-regex does NOT subsume the claim file (a valid id collides too).

## WHAT THE BOARD SURFACED THAT PRIVATE ADJUDICATION MISSED

1. Sonnet B1's redirect bearer-leak claim scored 5/5 in the grid and dies on a 5-line runtime
   probe nobody ran until this thread. The grader checked shape and cite-resolution, never
   runtime behavior. Board value: an adversarial opponent forced the test the rubric never asks.
2. glm's round-1 "out-prefix law" was a fabricated citation that the grid's checks (path exists,
   line in range) cannot catch - only cross-examination did. Banked as a mask-law data point:
   a model will invent a law citation to justify a true-ish conclusion.
3. The shared-OUT_DIR id-collision surface: not in ANY family's grid row (kimi saw the id f-string
   as traversal, glm saw the gates as unlocked, nobody said "the sanctioned N-driver shape shares
   one deliverable namespace"). Surfaced by the OP fact-drop, confirmed by both advocates.
4. Two synthesis deliverables the private grids never produced: the three-hunk hermes_burn patch
   bundle (thread 1) and the ALERT-CAP shape (thread 2, cap-alerts-never-halts).
5. The thread-1 severity/frequency split is a genuine scoring-criterion ambiguity for
   GARDEN_GRID.md: same bytes, same fleet, defensible rank inversion depending on criterion.

## COST AND BANKING

Budget $1, spent $0.0089. glm: 6 fires, 35811 in / 4473 out tokens, $0.0037 (runner-banked rows,
memory/runs/model_garden/usage.jsonl, ids chan-x4-*). ds: 6 fires via tools/ds_workhorse.py,
$0.005172 (banked by this lane as rows in the same ledger; ds lane reports no token counts).
Board receipts: watch/room.jsonl threads x4-roast-*; run staging under memory/plans/chan_roast_x4/
(items, briefs, contracts, out jsonl); glm outputs watch/inbox/model_garden/chan-x4-*.md.

## FALSIFIER FOR THIS LANE

If none of the five surfaced items above lands as either a patch, a grid-notes correction, or a
routing-rib observation within two sessions, the roast was theater with greentext. The three
candidate tickets: (a) hermes_burn three-hunk bundle, (b) descent_driver ALERT-CAP, (c) id
namespace fence (claim file or entry validation). Operator call which land.
