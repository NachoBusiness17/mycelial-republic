# BREAK-SECURITY hostile pass, eleven doors (2026-10-04)

Writer: break-security lens (ractor engine, dwfrun second pass). Target: the lens
report on the 24-wide dig's remaining build doors and build order. The lens
report arrived TRUNCATED mid finding 5 ("...sequences zero se..."); this pass
verdicts the five visible findings on their evidence, and banks what the lens
missed. Instruments this pass actually ran: file reads (line-numbered), git grep,
wc, ls, and one executed Python falsifier through the repo venv against
tools/arena_gwap.py + mag/gwap_payload.py. Zero pytest suites were run this
session; zero files under mag/ or tools/ were modified (one throwaway script in
the OS temp dir only).

## Verdicts

### F1. Tavern half of door 1 still mints agreement theater: CONFIRMED (falsifier executed)

Every cite byte-checks:
- tools/arena_gwap.py:189-194 is verbatim the ruled-tavern branch: `ruled = bool(r.get("judge")) or verdict.startswith(("RUN","BRAWL"))`, then intent AND report both `_claim(actor, "spoke", scene, q)` with the identical `q = "ruling=" + verdict[:140]` (:191-194). One boolean, one source, two claims.
- tools/arena_gwap.py:213-214 verbatim gives the two structs different author ids (anon_id seed ":fighter" vs ":carrier").
- mag/gwap_payload.py:344 `_COMMIT_BIND_RE = re.compile(r"(commit=[0-9a-f]{8,}:|ruling=)", re.IGNORECASE)` matches ruling=, and :390-401 is the exemption return (identical order, all qualifiers bound, suspected_collusion False).
- tools/arena_gwap.py:185-187 verbatim: the dungeon path mints intent from `_speech_verb(speech)` and report from `_ruling_verb(verdict)`, real independent parses.
- Live transcript count (run this session, venv json parse): watch/inbox/playground/tavern_20261004T160335Z/transcript.jsonl holds 135 rows; 51 carry judge or verdict fields (7 judge, 44 verdict).

The lens's own falsifier was RUN this session (its blind spot #3 said this exact
run was missing). Command: `.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/break_sec_falsifier.py`
(script writes only inside the OS temp dir; repo read-only). Fabricated tavern
run, two ruled rows where the fighter speech flatly contradicts the judge ruling
("[HIT] I strike the champ" ruled "RUN (fled in terror)"; "[CHECK] I examine the
ledger" ruled "BRAWL (bottle thrown)"):

```
TAVERN contradiction run:
  engine: arena-tavern-v3-independent-cop
  agreement_score: 1.0
  verdict: VERIFIED_AGREE
  collusion: False | ledger confirmation shape: identical order of 2 claims but every qualifier is commitment-b...
  intent_struct: [('spoke', 'ruling=run (fled in terror)'), ('spoke', 'ruling=brawl (bottle thrown)')]
  report_struct: [('spoke', 'ruling=run (fled in terror)'), ('spoke', 'ruling=brawl (bottle thrown)')]
DUNGEON contradiction run (contrast):
  engine: arena-dungeon-v3-independent-cop
  agreement_score: 0.0
  verdict: DISPUTE
  intent_struct: [('attacked', 'commit=a1b2c3d4e5:1'), ('checked', 'commit=a1b2c3d4e5:2')]
  report_struct: [('spoke', 'commit=a1b2c3d4e5:1'), ('spoke', 'commit=a1b2c3d4e5:2')]
```

Verdict: the falsifier's own kill condition ("if a contradiction ever produces
DISPUTE on the tavern path, this finding is wrong") does NOT fire: the
contradiction banks VERIFIED_AGREE at 1.0 with byte-identical claims, while the
SAME contradiction shape on the dungeon path scores 0.0 DISPUTE in the same
engine. The pinned test exists and pins the theater:
tests/test_gwap_independent_cop_20261004.py:149-157 asserts
`agreement_score == 1.0` and `verdict == "VERIFIED_AGREE"` for ruled tavern.
The lens's move (port the dungeon parse pair, flip the pinned test) is proven
feasible by the dungeon half of the same run: the fix mechanism already exists
and runs in this engine.

Two sharpenings the lens did not carry:
1. The GPS inflation is prospective, not yet banked: the GWAP receipt says the
   613 old rows stay and the next --backfill banks v3
   (watch/inbox/GWAP_INDEPENDENT_COP_20261004.md:75-78), so no v3 tavern rows
   sit in the ledger today; the inflation lands with the first backfill.
2. On the live transcript the adapter's ruled predicate (judge present OR
   verdict startswith RUN/BRAWL) is satisfied by 9 of 135 rows (counted this
   session), not 51; 51 is field presence. The minting subset is small but
   every row of it banks a content-blind 1.0.

### F2. Decay family should steal republic.py's supersession guard: CONFIRMED

All cites byte-exact: mag/republic.py:114 (`superseded_by ... set once, by
supersede(); never edited`), :186-223 (the save() guard), :194-198 (deletion
refusal), :200-204 (FROZEN-field edit refusal), :205-208 (trail rewind
refusal), :209-213 (supersession re-point refusal), :214-218
(supersede-to-nowhere refusal). FROZEN is a module-level tuple at
mag/republic.py:59, and the guard iterates it plus the letters dict exactly as
the lens described.

Additions from this pass's census:
- `git grep -n "AppendOnlyViolation" -- mag/ tools/` returns 12 hits, ALL in
  mag/republic.py (class at :63, raises at :195-220, handlers at :634-649).
  The guard is a single organ, not yet shared, so the steal is real work and
  there is no second dialect to reconcile yet.
- The other stores' invalidation writers already exist:
  mag/mycelium.py:188 `def contradict(...)` and :265 `def decay(...)`. The
  family's steal is guard + vocabulary over existing writers, not new organs.

The falsifier (parameterize the guard over a foreign frozen-field set in under
an hour) was NOT run: measuring it means doing the refactor, which a hostile
pass that edits nothing cannot bank. Judgment from the bytes: the guard spans
38 lines (:186-223) with two store-specific clauses (trail prefix :205-208,
pending-record prefix :219-221) that would need optional hooks; plausible at
the lens's 60-minute figure but UNMEASURED. CONVERGENT flag: the 24-wide
receipt itself already ruled the one-vocabulary law from the spec side
(watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:33, the two-graphs ruling);
this finding re-derives the same steal from the code side.

### F3. Night-cycle checkpoint-legs door is cargo as specced: CONFIRMED, one evidence leg KILLED, move already banked

Code cites byte-exact: mag/lane_runner.py:932-938 (comment naming the 5x
CYCLE_FAIL re-run cause; _trail CYCLE at :937 BEFORE _save_state at :938),
:925-931 (march rc=2 honest skip, stderr tail kept at :931), :913 (docstring
"$0"). Spend check run this session: watch/monitor_lane.py:11-13,54-56 shows
monitor is free public APIs only (HN Algolia, arXiv, OpenAlex, urllib, no key);
march without .env is the rc=2 skip. The residual re-run after a mid-cycle
state-write failure is therefore $0 and trail-spam only, exactly as the lens
argued.

The KILLED leg: "tests/test_night_march_cure.py ... is NOT on disk this
session". FALSE. The file exists as tests/test_night_march_cure_20261004.py
(131 lines, 6 tests; the AGENTS.md census bullet names it without the date
suffix and the lens's exact-name ls missed it). Worse for the door: the lens's
proposed residual move, "a 30-minute tripwire test asserting the CYCLE trail
row precedes the last_night write", is ALREADY BANKED as
test_cycle_night_trails_composite_even_when_state_write_fails at
tests/test_night_march_cure_20261004.py:100-119 (monkeypatched failing
_save_state, asserts the CYCLE row and the march tail survive). The door is
not "reduce to a 30-minute test"; it is zero minutes. Pure cargo, stronger
than the lens claimed, with one wrong evidence line.

### F4. Monoculture proxy alerts on the wrong tail: CONFIRMED

Cites byte-exact: the door spec is
watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:172 ("alert memory/attention.md
on sharp drop"); mag/mixture_of_agents.py:74 is the convergence field and :153
the avg_convergence stat. Lesson 23 exercise 2 read this session, verbatim at
corpus/library/ai-engineering-from-scratch/phases/16-multi-agent-and-swarms/23-failure-modes-mast-groupthink/docs/en.md:181:
"When it drops sharply, trigger an alert. Simulate a monoculture drift by
gradually correlating agent outputs." The sharpening this pass adds: the
inversion originates INSIDE the lesson, whose own simulation (correlating
outputs) raises agreement while its own alert watches for a drop; implementing
the exercise "verbatim" (the door spec's word) faithfully reproduces a
detector blind to its own test case. The dig's live correlated error (multiple
lanes banking vacuous FTS-zero absence claims off one broken instrument,
recorded in the receipt's instruments table at :307) was agreement-high, so a
drop-alert stays silent on it.

The named falsifier (replay the proxy over the 24 lanes' banked outputs and
check whether the FTS-zero class shows a drop) is NOT RUNNABLE as stated:
no per-lane agreement time series is banked anywhere this pass could find, and
the proxy does not exist yet. The inversion stands analytically on the
receipt's own recorded case; the replay becomes possible only after the proxy
logs agreement per lane.

### F5. Effect-broker idempotency audit absent from every greppable surface: CONFIRMED on the visible evidence (report arrived truncated)

Rerun this session: `git grep -n -i "idempot" -- mag/effect_broker.py
watch/inbox/ESTATE_GAPS_20261004.json` exits 1 (zero matches in both);
`wc -l mag/effect_broker.py` reads 911 and `git grep -c "" --
mag/effect_broker.py` reads 911 (two instruments, same number);
watch/inbox/ESTATE_GAPS_20261004.json exists. The disposition and the ~1h
estimate are verbatim in the primer at :47 (M5, "land it as a named row ...
with an owner, or drop the claim; ... about 1 hour (estimate, not measured)")
and :278 (Honesty). Caveat stated plainly: the lens's finding sentence was cut
off mid-word in the material this pass received, so only its evidence base is
verdicted, not its full claim.

## What the lens missed (additions)

1. **Door 2 already landed; the 11-door list is stale.** Commit 00cb15c77
   ("ARENA BENCH TRIPWIRE (door 2) ... 4-test tripwire landed") is in this
   tree's git log, and tests/test_arena_bench.py is on disk (checked this
   session). The ask's door list still carries the arena-bench tripwire as a
   remaining door. Honest remaining set: 10 doors, plus the EG-20 pass@K
   rider the landing commit itself says rides the bench (spec at
   watch/inbox/ESTATE_GAP_DIG_20261004.md:79, 2h, the only measured effort
   figure in the dig). Falsifier: `git log --oneline -3` showing 00cb15c77 at
   tip and `ls tests/test_arena_bench.py` failing to fail. Move: strike the
   door from the order, keep the pass@K rider on the bench.
2. **The night-cycle door's residual move is already on disk** (see F3):
   tests/test_night_march_cure_20261004.py:100-119. The door costs zero
   minutes, not thirty.
3. **The 24-wide receipt's flagship arithmetic is misquoted in its own
   headlines (no sacred cows).** The TL;DR
   (watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md:11) and the steal-door
   table row 1 (:235) both state 470 of 589 as "188 self-flagged ... plus 278
   empty-cop tavern DISPUTE", which sums to 466, not 470. The body's own
   partition (:106) closes 470 only as 188 collusion-tainted CHALLENGE + 8
   clean unrouted CHALLENGE + 274 empty-cop DISPUTE (278 DISPUTE total minus
   4 non-tavern). The union number is right; both headline compositions are
   wrong by the 8 clean CHALLENGE rows and 4 misattributed DISPUTEs. This is
   the phantom-number class the estate's own citation lint hunts, sitting in
   the dig's most-quoted figure. Supporting recount run this session (venv
   jsonl parse of memory/runs/gwap/arena-capability.jsonl): 613 rows,
   VERIFIED_AGREE 119 / CHALLENGE 204 / DISPUTE 290 / suspected-collusion 196,
   matching watch/inbox/GWAP_INDEPENDENT_COP_20261004.md:49-54 exactly.
   Falsifier: the day the ledger's clean-CHALLENGE count is 0, the 188+274
   composition and the 470 figure coincide and the wobble is cosmetic. Move:
   one-line erratum in the receipt, 5 minutes.
4. **AppendOnlyViolation is a single-organ census** (see F2): 12 tracked hits,
   all mag/republic.py. The decay family's shared-schema door has exactly one
   guard to steal and two existing invalidation writers
   (mag/mycelium.py:188, :265) to bind; nothing else in mag/ or tools/
   enforces append-only at save time under that vocabulary.
5. **Self-steal facts for doors the lens never touched** (all greps run this
   session, scope named): FSRS has zero tracked hits in mag/, tools/, tests/
   (the only match is the Godot binary, tools/godot/, a byte artifact) and
   memory/retrieval/ does not exist, so clippy-as-prober mints fresh state
   with no prior art in those roots. The string "embedding" appears in 8
   tracked mag/ files (accumulator, bare_numpy, context_compression,
   emergent_harvest, flock_scheduler, gguf_cartography, governor_autorun,
   jones_lens); whether any is a usable embedder for the three-signal door is
   OWED, not claimed. The build-once calibrator has prior art to steal beyond
   the Gero-4B card: mag/consensus_gate.py:10,31 ("The measured calibration
   ladder", AUROC of unanimity-as-correctness) is an existing calibration
   organ. mag/mcp_server.py is 565 lines (wc this session), confirming the
   MCP-lattice door extends rather than builds.
6. **The F1 falsifier execution itself** (transcript in F1): the lens's blind
   spot #3 named exactly this run as not-done; it is now done, and it doubles
   as a feasibility proof of the proposed 60-120 minute fix.

## Build-order correction (EV-per-hour, this pass's judgment)

- Cut: night-cycle checkpoint legs (cargo; cure and tripwire both on disk) and
  arena-bench tripwire (landed 00cb15c77).
- Keep at the front of the small doors: the tavern independent-parse port
  (F1, 60-120 min, mechanism already running in the same engine, unblocks the
  weld door's precondition honestly) and the monoculture high-tail inversion
  (F4, ~60 min of the door's 2-4h, self-stealing mixture_of_agents'
  convergence stats at mag/mixture_of_agents.py:74,153).
- The effect-broker idempotency read-audit stays a 1h named-row decision per
  the primer's own disposition (:47); it blocks nothing and still has no owner.
- Door 2's rider, EG-20 pass@K (2h, measured), remains the cheapest open item
  with a defined success meter.

## Honesty

Not run this session: any pytest suite (zero tests executed; the falsifier is
a direct venv script, and the 9 green tests and 65-test gwap surface are
carried from the GWAP receipt, not re-run); the republic.py refactor
measurement; the monoculture proxy replay (no banked series exists); any
write to the gwap ledger (read-only parse); any FTS query. The 529 figure is
`ls tests/*.py | wc -l`, files on disk, NOT a collected-test census. The lens
report was received truncated mid finding 5; findings beyond 5, if any exist,
were not verdicted. Foreign-repo facts (agentmemory grammar, Gero-4B card,
mem0/Graphiti claims) are carried from the primer receipt, not re-fetched.
