# communication.md - relay audit of the 24-wide door sequence (2026-10-04)

Lens: communication (relay auditor). Question under raction: the 11 remaining
build doors, self-steal first, hostile pass per falsifier, honest EV-per-hour
order, cargo call. My beat: what actually reached the operator versus what the
receipts claim was communicated. Instruments named per claim; counts carry
moment and denominator per B2-216.

## The relay state as of this sitting (byte-checked)

- Door 1 (independent-cop) landed bb0f34586 at 2026-10-04T12:23:16-04:00
  (`git log -3 --format="%h %cI"` run this sitting).
- Door 2 (arena-bench tripwire) ALSO landed 00cb15c77 at 2026-10-04T12:39:31-04:00,
  16 minutes after door 1. So the ask's "11 remaining" is already 10: the ask's
  own door list is stale (it lists arena-bench as remaining). Door 2 receipt:
  watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md:1-6 explains why it landed outside
  the ractor ("a pure defect fix + test addition with no design surface").
- I re-ran the door-2 tripwire myself: `.venv/Scripts/python.exe -m pytest
  tests/test_arena_bench.py -q` -> 4 passed in 3.00s. Green at my sitting.
- I re-censused the gwap primary (memory/runs/gwap/arena-capability.jsonl,
  json parse, this sitting): 613 rows, ts 2026-10-03T13:10:34Z to
  2026-10-04T16:09:39Z, verdicts VERIFIED_AGREE 119 / CHALLENGE 204 /
  DISPUTE 290, suspected_collusion flag on 196 rows all inside CHALLENGE,
  zero rows banked after the landing (last row 16:09:39Z vs landing
  16:23:16Z). Door 1's receipt numbers (GWAP_INDEPENDENT_COP_20261004.md:51,
  119/204/290/196) are byte-true at the primary. Verification POSITIVE.

## Finding 1 - the door sequence reached git but no operator routing surface,
## and the only actionable "next doors" line diverges from the reviser's table

Evidence (all run this sitting):
- watch/inbox/INDEX.json (2,969 items, last item DRIFT_PATROL_20261004.md, so
  the index IS maintained today) carries ZERO of the four dig receipts. The
  estate's own validator, `.venv/Scripts/python.exe -m mag.shared_surface
  validate`, lists them by name under "unindexed inbox files":
  GWAP_INDEPENDENT_COP_20261004.md, PRIMER_ADJACENT_24WIDE_20261004.md,
  PRIMER_ADJACENT_24WIDE_20261004_NUMBERS.md, ARENA_BENCH_TRIPWIRE_20261004.md
  (the warning block also names ~30 older receipts back to 10-02, so the
  backlog is a standing surface disease the dig rode, not caused).
- state/CURRENT.md:8 (updated 2026-10-04T09:30:00Z, BEFORE both landings)
  carries no door content; its "Next big move" (line 24-25) is still the
  post-reboot sequence. The door sequence never hit the live-truth doc.
- watch/room.jsonl (15,426 lines, alive to 2026-10-04T16:33:02Z, monitor-poll
  traffic): zero hits for independent-cop / primer_adjacent / arena-bench ci
  (full-file python scan this sitting).
- The GWAP receipt's "next doors" relay (GWAP_INDEPENDENT_COP_20261004.md:82-83:
  "arena-bench CI tripwire, clippy-as-prober, night-cycle checkpoint legs")
  diverges from the reviser's own ranked table (primer
  PRIMER_ADJACENT_24WIDE_20261004.md:216-225 and :233-247): it drops EG-20
  pass@K (table rank 3, the ONLY door with a measured effort figure, 2h at
  spec; re-relayed as riding the now-live bench at
  ARENA_BENCH_TRIPWIRE_20261004.md:46-47) and hoists clippy-as-prober (table
  rank 7, gate "same family schema" at primer :241) ahead of night-cycle and
  past its own gate. It was also stale on arrival: arena-bench landed 16
  minutes after door 1.

Falsifier: if INDEX.json were the wrong contract surface for receipts (it is
the catalog the machine contract points every client at, AGENTS.md boundary
table), or if the GWAP next-doors line actually matched the primer order, this
finding dies. Neither holds on the bytes above.

Move (15 min): land a one-screen DOOR_LEDGER (done: 1, 2; next: EG-20, then
night-cycle, then monoculture AFTER the channel fix in finding 3), index the
four receipts, and correct the GWAP receipt's next-doors line with an erratum.

## Finding 2 - the flagship decision counts are moment-unstamped: 188 vs 196
## for the same class across two same-day receipts, both true, neither dated

My census (613 rows, this sitting) confirms the later number: 196
suspected_collusion rows, all CHALLENGE, matching GWAP receipt :51 and the
commit message ("cures the 196 self-flagged rows"). The primer's flagship
(:106, :218, :235) says 188 flagged / 589 rows / 470 poisoned (79.8 percent),
true at its earlier moment (chain grew 589 -> 613 between the dig recount and
the door-1 build). Neither receipt stamps the census moment on the flagship
line, and the two receipts do not cross-reference each other's counts. A
future reader differencing 188 vs 196 without re-running the instrument would
call it a fabrication smell; it is a live-chain snapshot delta, exactly the
B2-216 law (name instrument, moment, delta) the dig's own honesty section
quotes (primer :287: "any future count must re-run the instrument").

Falsifier: a moment-stamped pair of counts showing the two receipts censused
the same tree at the same moment would make one of them wrong instead of
merely unstamped. I cannot rule that out without the receipts' own run logs
(they name no moments); my census only proves the LATER figures byte-true now.

Move (10 min): one erratum line in the GWAP receipt stamping the census (613
rows at 16:09:39Z pre-landing) and pointing the primer's 589/188/470 figures
at their earlier moment.

## Finding 3 - the alert channel the monoculture door targets is read-blind at
## the boot surface, and it already holds a decision-relevant alarm no door
## carries

The monoculture-proxy door (reviser step 4, primer :172) banks its sharp-drop
alert to memory/attention.md. Mechanics verified this sitting:
- Writers append at the file tail: newest block "Tip witness fired
  2026-10-04 09:30" sits at attention.md:549-563; today's provider probe at
  attention.md:526.
- The boot-time consumer reads the HEAD only: mag/context_pack.py:311-315
  `_clip` returns `path.read_text()[:600]`, :687 clips attention.md at 600
  chars, :1005 ships `att[:400]` as attention_tail to every seat pack. Today
  those chars are the 03:00 session-record header plus the first lines of a
  ~130-line 2026-09-26 probe-alarm flood preserved below the marker at
  attention.md:13. Tail-appended alerts, including any future monoculture
  alert and today's "provider_probe DOWN mlx-cluster,ollama,xai; QUOTA-DEAD
  nous (run 2026-10-04)" (attention.md:526), never reach a booting seat.
- The stale 09-26 flood is the channel's noise floor: 800 dupes were
  suppressed 2026-10-03T23:50Z (attention.md:417) but the surviving 09-26
  lines still occupy the head region the pack actually reads.

Material side-fact: QUOTA-DEAD nous (attention.md:526) touches the funded
judgment carrier of the driving ladder ($180 Nous credits, AGENTS.md). No
door receipt carries it into its EV calculus; any door planning paid
dispatch should re-probe first. I read the alarm line only, not the
underlying memory/improve/provider_health/2026-10-04.json (OWED below).

Falsifier: if another boot-path consumer reads attention.md's tail (I checked
context_pack fully; daemon.py's "attention" is a policy action with a daily
cap, mag/daemon.py:91-98, not this file), the blindness claim narrows to
context-pack-only. I did not classify all 12 consumer files (blind spot).

Move (30 min, before building the monoculture door): fix the channel once,
either rotate the newest alert block to the head at write time or clip the
tail in context_pack; clear the 09-26 flood; wire the nous probe result into
any paid-dispatch door's plan.

## Finding 4 - self-steal: the decay-family vocabulary already exists as
## enforced law in mag/republic.py, and FSRS ground is genuinely empty

The reviser's two-graphs ruling (primer :33: "define
valid_at/invalid_at/superseded_by ONCE... or the estate grows two dialects of
the same law") misses that a THIRD dialect already exists, in code, enforced
at save time: mag/republic.py:15 ("a retracted letter is superseded_by
another, never deleted or edited - house chain law"), :114
(`superseded_by: int | None = None  # set once, by supersede(); never
edited`), and the immutability guard at :209-217. The mycelium-v2 door (table
rank 8, 4-8h) and the family schema should steal republic's field name and
save-time guard as store zero rather than minting fresh vocabulary; the
receipt's own "define once" ruling, applied honestly, must include it. The
other half of the self-steal check came back empty as claimed: my grep over
mag/, tools/, .agents/skills/ for fsrs|spaced repetition|retrieval state
returned zero hits and memory/retrieval/ does not exist, so clippy-as-prober
builds on empty ground (the primer's implicit claim survives my hostile
pass). Door 2's landing is itself a CONVERGENT self-steal correction of the
primer: the "shape drift" diagnosis was actually a 459-byte redirect stub
since 09-22 (ARENA_BENCH_TRIPWIRE_20261004.md:8-19), i.e. the primer's
leverage claim was right, its mechanism wrong.

Falsifier: if republic's supersede() carries no timestamp or validity-window
semantics (it is a pointer-swap on letters, not bi-temporal), only the field
name and append-only guard are stealable and the bi-temporal half of
mycelium-v2 remains new build; that does not kill the steal, it scopes it.

Move (1h): the decay-family schema pass starts from mag/republic.py's guard
as the base pattern, names republic letters as store zero in the schema doc,
and only then instantiates GPS/mycelium/retrieval.

## Finding 5 - honest EV-per-hour order and the cargo call, on relay grounds

Order (mine, from evidence above, not the receipt's estimates):
1. EG-20 pass@K first: 2h MEASURED at spec (primer :237), its instrument
  proven live by my own 4-passed run, and it is the door most at risk of
  being lost by the relay (dropped from the GWAP next-doors line, from the
  ask's 11-door list, present only in the primer table and the arena
  receipt's tail).
2. Night-cycle checkpoint legs (2-4h): documented 5x re-run harm in the
  runner's own comments (primer :238), no design gate.
3. Monoculture proxy ONLY after finding 3's channel fix; an alert into a
  read-blind channel is theater by construction.
4. Decay-family shared schema (1h of design) then pheromone metabolism,
  clippy-as-prober, mycelium-v2 in the receipt's order, the schema seeded
  from republic.py (finding 4).
5. The five design-gated doors stay gated (primer :223) - the receipt gated
  them honestly; they are sequenced-later, not cargo.
Cargo call, communication grounds: THREE-SIGNAL, WELD, and CONSUME-THE-LEDGER
are each 1-2 days of seat time before any operator-visible decision surface
changes, and with the relay surfaces as they stand (findings 1 and 3) their
value would land into blind channels. They are the cargo risk class until
the relay fix lands; the cheap tripwires are not cargo by evidence (door 2
already paid off: bench live, stub class pre-push-gated).

## Blind spots (honest)

- The operator GO primary: room.jsonl and the repo carry no byte of it; two
  receipts quote it by content ("do it", GWAP :3; "go" + mid-flight
  "actually ractor it out self steal then go", ARENA :3-5, which spawned this
  ractor run dwfrun-3b5af1ac). Corroboration by content, primary OWED in a
  session transcript outside the repo.
- The 529-payload new-instrument measurement (GWAP :53-54) was not re-run
  (playground dirs, not censused this sitting).
- attention.md consumer classification covers context_pack (fully) and daemon
  (action-cap only); act.py, chronicle.py, biography.py, estate_bridge.py and
  the rest of the 12 greps are unexamined.
- ESTATE_GAP_DIG_20261004.md (the EG-20 spec) was cited but not read this
  sitting; its success meter is taken from the primer's citation :237.
- memory/improve/provider_health/2026-10-04.json (the QUOTA-DEAD nous probe)
  not opened; alarm line only.
- The shared_surface validate output was read as its tail 15 lines (errors +
  warnings lists); exit code and summary head not captured.
- ZMEM and the exec-log stores are outside this sitting's scope.

## Correction block (hostile second pass, this sitting): F4 re-derived in full

The second pass weakened F4 because the finding text arrived in the handoff
truncated mid-sentence, making the claim unverifiable as passed (the verdict
confirmed the three evidence cites byte-check). Re-derived below, every check
re-run this sitting:

The full claim: the decay-family vocabulary the 24-wide reviser ordered
defined once (valid_at/invalid_at/superseded_by for lattice_edge.v1 and
mycelium edges, PRIMER_ADJACENT_24WIDE_20261004.md:33) already exists as a
code-enforced instantiation in a third store the ruling never names:
mag/republic.py's Republic-of-Letters letter book (state/republic_letters.json),
where superseded_by is set once by supersede() and never edited
(mag/republic.py:114), save() is the writer gate guarding append-only with
six AppendOnlyViolation raise sites (mag/republic.py:186-221: frozen-field
edits :200-204, trail edits :205-208, supersession re-points :209-213,
dangling superseders :214-218, plus :195 deletes and :220 pending edits), and
the read side already routes on the field (mag/republic.py:341-345: a
superseded letter stops collecting replies, with the routing error naming
the successor). The mycelium-v2 and family-schema doors should steal the
field name, the save-time guard shape, and the read-side rule as store zero
rather than minting a fresh dialect. Scope limit, stated inside the claim:
supersede() is a pointer-swap with no valid_at/invalid_at time semantics, so
the bi-temporal half of mycelium-v2 remains new build; only the vocabulary
and its enforcement pattern are stealable. The FSRS/retrieval-state ground
stays confirmed empty (re-run this sitting: git grep -ln for
fsrs|spaced.repetition|retrieval.state over mag/ tools/ .agents/skills/
listed no files; ls memory/retrieval/ -> No such file or directory).

Checks run this sitting, commands and outputs:
- Read mag/republic.py:13-16 (docstring: "a retracted letter is
  superseded_by another, never deleted or edited - house chain law, enforced
  at save time (the guard is in code, not in prose)"), :114 (field with
  comment), :198-221 (the guard block), :341-345 (reply routing on
  supersession).
- git grep -n "def save\|AppendOnlyViolation" -- mag/republic.py ->
  class :63, save() :186, raises :195/:202/:206/:211/:216/:220, catches
  :634/:640.
- grep -n -i "republic" watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md ->
  exactly ONE hit, at :33, and it is "the mycelial-republic steering graph"
  (the mycelium's nickname in the same paragraph as the ruling); the ruling
  sentence itself names only lattice_edge.v1 and mycelium edges. The miss is
  real and now precisely scoped: the word appears once, as a different
  referent.
- git grep -c "AppendOnlyViolation" -- tests/ -> no output (zero test files
  name the exception). Behavioral coverage of the raise paths is UNVERIFIED:
  the five test files matching "supersede" (test_census_zero_collect,
  test_citation_lint, test_doctrine_arbiter, test_eid_dedup,
  test_grave_classify) were not opened, and the two probed republic test
  files (test_coordination.py, test_game_entry.py) carry zero
  supersede/AppendOnlyViolation hits.

Falsifier (tightened): the finding dies if (a) the decay-family ruling
already names the letter book (disproven this sitting: the primer's only
republic hit at :33 is the mycelial-republic nickname and the ruling names
two stores), or (b) a save path writes state/republic_letters.json without
passing save()'s guard, making "enforced" theater (not found this sitting:
save() :186 is the only writer gate located, but every import/copy path was
not exhaustively traced), or (c) the guard is dead code with zero behavioral
coverage (unresolved: no test names the exception; not ruled out that a
RuntimeError-shaped assertion exercises it). A timestamp-less supersede()
does not kill the finding; it only scopes the steal as stated above.

Move (1h, unchanged, now with the test leg): the decay-family schema pass
starts from mag/republic.py's save-time guard + superseded_by field +
reply-routing read rule as store zero, names the letter book in the schema
doc alongside lattice and mycelium, and pins the guard with one
AppendOnlyViolation test while touching it.

Writer: lens-communication, ractor run dwfrun-3b5af1ac, 2026-10-04.
