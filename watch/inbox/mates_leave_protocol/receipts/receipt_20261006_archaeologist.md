# Receipt: archaeologist mate, 2026-10-06, mission_20261006_03

STATUS: COMPLETE. Seed thread Q-001 exhausted within one cycle; no resume owed.
Persona: THE ARCHAEOLOGIST. Hunting ground honored: git log archaeology, earliest
commits, dead lanes' trails, sealed rescues, August strata still load-bearing.
STEER honored: COMPUTE LADDER - all work local byte reads on this account, zero paid
dispatches, $0 metered, zero LLM calls, concurrency peak 1 (law cap 16).

Mission pack: logs/mates/missions/mission_20261006_03_archaeologist.md (pack born
2026-10-06 08:00:05 local, claimed 08:00:10 via .claim sidecar; text is copied
verbatim from configs/mates.yaml:53-60, authored 2026-09-29).

## FINDINGS

### The seed's premise was already dead at pack time, and the pack could not have known

Q-001 ("Verkle noise compaction: 99 leaves to 1 counter leaf, recompute Merkle chain")
is not waiting and has not been needs-operator since 2026-09-30 09:28:35Z, when
queue-sweeper-Z9 closed it STALE-superseded (queue/queue_index.jsonl row 1). The
operator ruling that dissolved the GO ask is commit 3ed507e0c (2026-09-29 18:48:19
-0400, "SACRED-COW RULINGS"): compaction PARKED per the funded elder consult
(watch/inbox/ELDER_CONSULT_COMPACTION_20260929.md, verdict (b) park it, 4 named
re-raise conditions, 18-month kill escalation). The mates protocol that wrote this
seed text was born 2h19m AFTER that ruling (configs/mates.yaml landed 172279a2d,
2026-09-29 21:07:15 -0400), so the pack's "needs-operator" was stale in its first
minute and has been reprinted daily by tools/leave_dispatcher.py (landed 71e23b690,
2026-09-29 23:24:04 -0400, the X12 static-runner unblock) ever since. The dispatcher
copies static seed text from mates.yaml; it reads no live queue state.

### Dated strata of Q-001 (every layer, oldest first)

1. 2026-08-04 11:47:25 -0400, eb07ad62e: git birth, "clean publish baseline";
   mag/chain_guard.py is already in this baseline.
2. 2026-08-04 21:17:09 +0000, 79e0a6e41: verkle first named in a commit ("Add seat
   FILE pipeline: any seat -> Verkle workday leaf"), day one of the repo.
3. 2026-08-12T16:41:39.727222Z: earliest surviving row in the live chain
   (memory/biography/verkle_chain.jsonl). The chain data is an August artifact.
4. ~2026-08-25 (dated by neighbors, not by bytes: queue/todo.md is untracked, never
   in git, so the line has no commit history): the janitor ask "compact 99
   orchestrator noise leaves into 1 counter leaf" was hand-written into the todo's
   oldest still-living section; surrounding items carry DONE 2026-08-26 annotations;
   sibling Q-010's pointer anchor ties this family of asks to the 2026-08-06
   autonomy boot. Today the line is marked [x] with a PARKED closure stamp appended
   by queue-truth-a14 on 2026-10-04 (watch/inbox/go_wave_20261004/queue_truth.md).
5. 2026-08-25 14:45:23 -0400, b7a47f194: "joint verkle re-land + canary" - the
   current mag/verkle_knot.py and mag/chain_guard.py stratum. Chain data (row 1,
   08-12) predates the current module: an earlier writer made the first rows.
6. 2026-09-17 09:05:29 -0400, 08f11bb49: FIFTY WIDE board seeds FW-48 ("Verkle noise
   compaction dry-run: 99 noise leaves -> 1 counter leaf", receipt pointer
   FW48_verkle_compact.md). Second independent sighting. The receipt file does not
   exist anywhere in the repo (glob, 0 hits): a dead receipt.
7. 2026-09-25T19:15:38Z: the queue is born - Q-001's row ts, identical across the
   batch = bulk import from todo.md into queue/queue_index.jsonl; committed
   3752abae2, 2026-09-25 23:42:10 -0400. Before this moment nothing mechanical read
   todo.md; the ask had lived in a hand-edited, git-invisible file for roughly a
   month.
8. 2026-09-26T00:03:57Z: first machine escalation: roam verdict needs-operator,
   4h48m after import. Once machined, the thread moved fast.
9. 2026-09-26/27: ractor panel builds the verkle99 card
   (watch/inbox/ractor_panel_20260926/verkle99.final.md); module lands
   0d0432a86, 2026-09-27 01:10:02 -0400 (card names landing commit e73b60c54):
   mag/verkle_compaction.py plan-only, tests/test_verkle_compaction.py 9 green, no
   CLI flag wired, double gate (operator GO + tests green). The card corrected the
   ask's premise: "99" is the card name, not a leaf count; the class measured
   957 rows at 09-27T03:55Z, split 463 fold candidates / 494 kept live-knot.
10. 2026-09-28 12:44:20 -0400, 390814497: plan-only half banked; escalation ruled a
    workflow dispatch is NOT operator GO; real numbers at plan time: 247 fold / 790
    keep over 8,212 rows; counter leaf verified absent; chain verify True; live
    fold left OWED.
11. 2026-09-29: funded elder consult (z-ai/glm-5.3-prime, 2,654 tokens, $0.02115576)
    convicts execution: 5.8 MB chain inside a 68 GB tree (0.0085 percent), first-ever
    live mutation of the provenance spine to recover megabytes on cheap disk. PARKED,
    4 re-raise conditions. Same day: watch/inbox/VERKLE_V2_DECISION.md recommends the
    chain_mode v1 -> v2 flip with precondition 1 = compaction must gain a v2 refusal.
12. 2026-09-29 18:48:19 -0400, 3ed507e0c: operator rules; Q-001 GO ask DISSOLVES.
13. 2026-09-29 21:07:15 -0400, 172279a2d: mates protocol v0 lands with this seed
    text; 23:24:04, 71e23b690: dispatcher + runner land; first pack files on disk
    23:17. The static pack era begins.
14. 2026-09-30: V2 GUARD landed in mag/verkle_compaction.py (plan() and apply()
    refuse under chain_mode v2, exit 2). 09:28:35Z: queue-sweeper-Z9 closes Q-001,
    citing commit 4b77c3d01 - a commit that does not exist (see JOURNEY dead end 1).
15. 2026-10-06, this dig's live measurements: chain_mode still v1 (configs/mag.yaml
    line 8); 0 v2 rows in the chain; V2 memo addendum fields still _pending_; the
    parked program is doubly dead (parked by ruling, refusing by guard the day the
    flip ever lands).

### Answer 1: WHY it never escalated

It predates every machine that could escalate it. The ask was written into an
untracked, hand-edited file (queue/todo.md, never in git, no mtime history - the
file was last wholly rewritten 2026-10-04 06:02) at the todo's oldest stratum,
roughly 2026-08-25 by neighbor dating. For a month the only readers were seats that
happened to open the file. The 09-17 FW-48 sighting produced a dry-run receipt that
never landed on disk and no queue row. The queue system that roams and stamps
needs-operator was itself born 2026-09-25 (import) - the ask is older than its own
escalation path by about a month. From the moment machinery existed, nothing sat
idle: needs-operator in under 5 hours, plan-only module the next day, NO GO ruling
the day after, funded elder consult and operator ruling on day 4, queue closure on
day 5. The wait was not tail negligence; it was head absence. Secondary findings:
the ask's own numbers fossilized ("99" was a point-in-time class count, stale by
09-26, preserved forever as the card name), and the chain kept growing underneath
the parked ask (orc-prefix rows 3,022 today).

### Answer 2: WHAT the chain-rewrite actually risks

- It is a first-ever live mutation of the append-only provenance spine; identity,
  boot (hermes_warm_boot loads the tip into every session), seals, and the RIB
  deliberate-ask all hang off that tip. The hot-restore path has never fired in
  production, so the first live run is the riskiest moment (elder verdict).
- Measured blast-radius precedent: ONE bad root on 2026-09-27 froze every append for
  hours while lanes were hot (VERKLE_V2_DECISION.md section 3).
- The chain is under concurrent live writes: three different tip roots were observed
  during ONE read-only ask on 09-28 while leaf count held; any rewrite must
  re-derive under the lock at execution time (burn_reset Q-001 receipt).
- It destroys rows by design (drops fold candidates from the live chain). Under the
  v2 semantics adopted by the 09-29 decision (canonical append-only history,
  multiple rows per session), that destruction is exactly what v2 forbids; the
  landed V2 GUARD refuses with exit 2 the day the flag flips. Executing the fold in
  v1 first would also foreclose the v2 conversion: flip-back is not a clean rollback
  (multi-row sessions refuse v1 consolidation); the clean rollback is a pre-flip
  seal, which has never been taken (addendum all _pending_).
- The prize is a rounding error that shrank while everyone waited: 5.8 MB of 68 GB
  at consult time; 7.78 MB today (my measure) in the same tree.
- The fold's own numbers drift by the hour (live amends delete superseded knot
  files): 99 fossil, 463/464 sandbox (09-27), 247/790 plan time (09-28). Any ask
  carrying a leaf count without a moment is confabulation by construction.
- Pre-existing guard regression (dangling 761 / evidence_lost 618 / dangling_unflagged
  521 / flag_drift 2, read 09-28) is real but predates the fold; apply() would
  re-mark it, not cause it.

### August strata still load-bearing (hunting-ground duty)

The chain itself (first row 2026-08-12, today 11,459 rows, tip in every boot),
mag/chain_guard.py (in the 08-04 baseline), the todo line (~08-25), and the branch
name the verkle99 card landed on: mag/run-beta1-factory-build-audi-20260806T231709Z,
cut from the 08-06 factory build. The pack's "waiting since August" is defensible
only through these: the ROW Q-001 is a 09-25 birth, not an August one.

## JOURNEY

Threads followed, in order, with the why of each turn:

1. Read the pack; its premise (needs-operator) contradicted the queue row I could
   already see, so thread 1 became: date the gap between pack text and queue truth.
   -> Found: pack text is static mates.yaml seed, authored after the ruling.
2. Grep Q-001 -> queue/queue_index.jsonl row 1 gave closure + close_note citing
   commit 4b77c3d01. Turn: verify the cited commit before trusting it.
   -> Dead end 1: 4b77c3d01 resolves to NO object (git cat-file -t fails; absent
   from every ref's full hashes via git log --all --format=%H; absent from reflog).
   The ruling text it is cited for exists verbatim in 3ed507e0c. The phantom hash is
   propagated in 3 surfaces: queue_index.jsonl row 1 close_note,
   tools/queue_close.py line 111 (RECEIPT_NOTES table), and
   watch/inbox/hydrology/Z9_QUEUE_SWEEP.md line 27. As archaeologist I date and
   report; I do not rewrite append-only ledger rows. Owed repair (builder seat, one
   line): correct the hash to 3ed507e0c in tools/queue_close.py, and let future
   closes cite the real commit; citation_lint would call this a missing citation
   target.
3. Read ELDER_CONSULT_COMPACTION_20260929.md and the burn_reset Q-001 receipt:
   verdict, numbers, gates, OWED list. Turn: date the landing layer.
   -> 0d0432a86 (09-27 01:10:02 -0400) + card verkle99.final.md; read the card's
   full proof section (sandbox migration, class split, consumer survey, tombstone
   counter, moment-snapshot law).
4. Hunt the ask's origin (the August question). Turn: git pickaxe on queue/todo.md.
   -> Dead end 2 (an absence, not a file): todo.md has NEVER been tracked; pickaxe
   empty; file mtime is a 10-04 rewrite, useless for dating. Fell back to neighbor
   dating inside the file (DONE 2026-08-26 annotations) and Q-010's pointer anchor
   (autonomy boot 2026-08-06). Honest limit: the exact day the janitor line was
   written is not provable from bytes; earliest verifiable "99" mention is the
   09-17 board row (tracked, 08f11bb49).
5. Followed the board row's receipt pointer.
   -> Dead end 3: watch/inbox/fifty_wide_20260917/FW48_verkle_compact.md does not
   exist (glob repo-wide, 0 hits; no verkle/compact-named .md in that dir). The
   FW-48 dry-run's evidence is gone; only the board row survives. This is exactly
   the locksmith's 174-zombie class; filed here as evidence, repair is that seat's.
6. Chased the "82 compactions" phrase in the elder lane surface (keyword neighbor).
   -> Dead end 4 (false friend): that is the seat heartbeat golem (939 firings, 82
   memory compactions), unrelated to verkle. Dropped.
7. Swept "archaeologist" repo-wide to date this mate's own lineage.
   -> Dead end 5 (name collisions, all unrelated): mag/prompt_archaeology.py,
   persistent_agent.py's archaeologist seat, watch/overnight_churn.py's resident
   contract, packs/p8_astra_ask_20260913.json lens (09-13), and the 51 Sep-3
   archaeologist chat replays whose flood was already explained in 02bcd49be
   (09-19). Also noted, not a dead end: tools/dispatch_landing_join.py:214-219 and
   tests/test_dispatch_landing_join.py:154 use "archaeologist goals" as the live
   example of boilerplate tokens defeating citation joins (2026-10-01 lesson). The
   mates protocol should know its packs are the corpus that lesson was learned on.
8. Verified the live chain state myself rather than citing any receipt's numbers
   (trust bytes, not reports): row count, file size, first/last ts, counter-row
   absence, v2-row absence, tip/leaf count match, chain_mode flag. All in COUNTS.
9. Thread exhausted: both seed questions answered with dated layers; no live edge
   remains on Q-001 itself. Stop here per the ride-to-the-edge law (exhaustion
   before budget).

Self-chosen next seed for the rotation (from my dead ends, per seeds_rotation law):
"Promised-but-absent receipts: sweep watch/inbox board rows and queue close_notes
for receipt pointers that resolve to no file (FW48_verkle_compact.md is the first
specimen), and date when each pointer was last consumed as if real." Second
candidate for a builder seat: the 4b77c3d01 -> 3ed507e0c one-line correction in
tools/queue_close.py.

## COUNTS (all measured or cited; every chain count is moment-bound)

This dig's live measurements (2026-10-06, read-only):
- chain rows: 11,459 (memory/biography/verkle_chain.jsonl)
- chain file size: 7.78 MB
- first row ts: 2026-08-12T16:41:39.727222Z; last row ts: 2026-10-06T12:39:22.092721Z
- counter rows (session_id mag-agent-orc-noise-counter-v1): 0 (the fold has never
  executed)
- v2-mode rows: 0; configs/mag.yaml line 8: chain_mode: v1 (flip never done)
- mag-agent-orc-* prefix rows: 3,022 (prefix count only, NOT the fold-candidate
  class, which also requires dominant_theme null + zero theme vector + knot absent;
  I did not recompute that class today)
- tip: n_leaves 11,459 == chain rows 11,459 (counts match; full verify not run this
  ask); tip root prefix 450665bf445f54b3

Cited historical measurements (each bound to its moment, census-denominator law):
- chain rows: 7,809 (09-26 survivor writing), 7,845 (09-27 03:55Z class split),
  7,848 (09-27 sandbox snapshot), 8,212 (09-28 plan time), 8,669 (09-29 V2 memo)
- noise class: 957 rows at 09-27T03:55Z = 463 fold candidates + 494 kept live-knot;
  247 fold / 790 keep (noise_class_total 1,037) at 09-28 plan time; "99" is the
  fossilized card-name count of an earlier moment
- tests/test_verkle_compaction.py: 9 tests, passed 09-28 ask, landed 09-27
- elder consult paid run: glm-5.3-prime, 2,654 total tokens (1,852 reasoning),
  $0.02115576

Git and protocol datings:
- phantom commit 4b77c3d01: 0 objects, 0 ref hits, 0 reflog hits; cited in 3 files
- real ruling commit: 3ed507e0c, 2026-09-29 18:48:19 -0400
- mates.yaml born: 172279a2d, 2026-09-29 21:07:15 -0400 (seed text 2h19m post-ruling)
- dispatcher + runner: 71e23b690, 2026-09-29 23:24:04 -0400; first pack mtimes
  2026-09-29 23:17:28
- queue import: rows ts 2026-09-25T19:15:38Z, committed 3752abae2 09-25 23:42:10 -0400
- roam verdict: 2026-09-26T00:03:57Z (4h48m after import); closure 2026-09-30T09:28:35Z
- verkle99 landing: 0d0432a86 2026-09-27 01:10:02 -0400; plan-only bank 390814497
  2026-09-28 12:44:20 -0400
- FIFTY WIDE board: 08f11bb49 2026-09-17 09:05:29 -0400; its FW-48 receipt pointer
  resolves to 0 files
- mission packs on disk (logs/mates/missions/): 56 packs across 7 daily batches
  (09-29, 09-30, 10-02, 10-03, 10-04, 10-05, 10-06), 48 .claim sidecars (the 09-29
  batch has none); no 10-01 batch exists on disk (observed in listing, not
  investigated - out of seed scope)
- repo git birth: eb07ad62e 2026-08-04 11:47:25 -0400; verkle first named 79e0a6e41
  2026-08-04 21:17:09 +0000

Metered spend this receipt: $0. LLM dispatches: 0. Em-dash bytes in this file: 0.
