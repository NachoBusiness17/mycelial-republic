# break-moonshot-1: hostile pass on moonshot-1 (eleven-doors ask)

Writer: break-moonshot-1 (hostile second pass, ractor-engine). Moment: 2026-10-04, ~17:00Z.
Method: byte-check every evidence cite, execute the lens's named falsifiers, re-derive
what the lens admitted was receipt-carried, and re-census the universal claims untruncated
per the quantifier law. Verdicts: confirmed / weakened / killed.

## Verdicts on the five findings

### F1 "two top-4 doors rank tree states that no longer exist" -> WEAKENED

Byte-checks that PASSED (all cites are real):
- mag/arena_bench.py:323 is exactly `"verdict": "PASS" if overall else "FAIL"`; the
  honest-raise block the primer cited at :102 is the docstring, actual raises :104-117.
- Selftest rerun this session, twice: exit 0 both times
  (`.venv/Scripts/python.exe mag/arena_bench.py --selftest`), no ValueError, both
  synthetic verdicts minted (pass_case PASS 1.0, fail_case FAIL 0.3675, split_proven true).
- mag/lane_runner.py:932-938 exact: the trail-BEFORE-persist comment sits :932-936,
  `_trail` :937, `_save_state` :938.
- tests/test_night_march_cure_20261004.py:100-128 exact (state-write-fail cure :100-120,
  green-persist :122-128).

Why weakened, two independent grounds:
1. THE MOVE WAS ALREADY LANDED WHEN THE LENS FILED. Commit 00cb15c77 (2026-10-04
   12:39:31 -0400, `git show --stat`) landed tests/test_arena_bench.py (94 lines,
   4 tests: selftest exit 0 + split proof, ground-truth parse of canonical surfaces,
   THE STUB TEST meta-refresh + min-size, JSON decode discipline), repointed
   ARRAKIS_PATH at dashboard/static/games/arrakis.html, and banked
   watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md. The lens report's mtime is
   2026-10-04 12:43:45 -0400 (stat), four minutes AFTER the commit, yet its evidence
   still says "git grep -n 'arena_bench' -- tests/ -> zero hits" and its EV order
   still ranks "arena-bench pin (~30 min)" as move 1
   (moonshot-1.md:162). Same grep this session: 10 hits, all in tests/test_arena_bench.py.
   I ran the suite: `pytest -q tests/test_night_march_cure_20261004.py
   tests/test_arena_bench.py` -> 10 passed. The moving-tree law (N12, the exact law
   arena_gwap.py status() docstring carries) bit the lens between grep and filing.
2. "NIGHT-CYCLE ... ALREADY CURED ON-DISK" OVERSTATES. What landed is the
   observability cure (CYCLE row survives a failed state write; march stderr tail kept).
   The door's named deliverable (primer receipt line 171: "write per-leg done flags
   through the existing _save_state ... and resume past completed legs") does NOT
   exist: cycle_night (mag/lane_runner.py:911-939) still checks only
   `st.get("last_night") == today` (:919), no leg flags, no resume; on a persistent or
   transient Errno-22 the daemon still re-runs monitor (timeout 300) + march (timeout
   600) every tick, now visibly (the cure test itself pins `pytest.raises(OSError)`
   propagating, tests/test_night_march_cure_20261004.py:115-116). "Cured" is right for
   the lost-CYCLE-row symptom, wrong for the re-run class the door names.

Falsifier executed: the lens's own falsifier (selftest raises on fresh checkout, or
test_night_march_cure fails) ran clean, so the two DEFECTS did move; but the honest
disposition is: arena-bench deliverable landed by another seat (strike, do not re-do),
night-cycle deliverable half-open (per-leg resume still unbuilt, worth a 1-2h ticket,
not a 15-min guard).

### F2 "MCP-lattice shim is a registry edit wearing a 4-8h ticket" -> WEAKENED

Byte-checks that PASSED: mag/mcp_server.py:226-252 (_load_tool_functions over tools/_FN
+ TOOL_MAP; _profile_names filters ROLE_TOOLSETS), :67 (ROLE_TOOLSETS dict head),
:308-321 (tools_manifest from live signatures), :258-259 ("The registry stays
compiled-from-code"), :336 ("lazy: module import stays stdlib-only");
`git grep -n -i -E "lattice|context_pack|build_context" -- tools/__init__.py` -> zero
hits (rc 1, rerun this session); registrable callables exist:
mag/lattice_query.py:53 query_by_theme, :68 neighbors, :89 summary, :116
graph_viewport; mag/context_pack.py:638 build_context_pack.

Why weakened: the door as receipt-specced (primer receipt lines 57 and 244) is MORE
than registration. Its deliverable is agentmemory's memory_recall grammar
(token_budget + format full/compact/narrative) serving build_context_pack + lattice
queries in the standalone 7-tool shape, and its named gate is the reconciliation pass
ordered BEFORE any lattice building: X_INTEL_AIENG_SCRATCH_20261004.md:92-94 ("The
lattice spec owes a reconciliation pass against it ... BEFORE any lattice building
starts"), re-read this session. The wrong-path citation that gate includes is still
uncured: :89 still reads "memory/mcp-lattice spec-seed" while the real file is
watch/inbox/model_garden/MCP_LATTICE_SPEC_SEED.md. I also read the grammar bytes the
lens left receipt-carried: library_parked/agentmemory/src/mcp/server.ts:84-113 carries
the format enum validation ("full", "compact", "narrative", else 400) and the
token_budget positive-integer validation feeding mem::search. That grammar is real
parameter surface, so "registration, not a build" shrinks the deliverable to prove the
price collapse. The honest claim: registration is a cheap legitimate FIRST SLICE
(~1 sitting), the door remains grammar + 7-tool shape + reconciliation + citation cure
behind it. The lens's own falsifier names this condition; its headline and EV order
(line 162-163: "MCP registry shim ... before any grammar reconciliation") treat the
shrink as settled and invert the receipt's stated gate order.

### F3 "moonshot swing: start the weld now" -> CONFIRMED

Every cite byte-checks:
- bb0f34586 in git log; GWAP_INDEPENDENT_COP_20261004.md read in full (verdict shape
  161/88/64/216 over 529 payloads at :53-54).
- The weld gate text verified in the primer table row 11: "design-gated: needs the cop
  fix (rank 1) so its banked scores mean something" (PRIMER_ADJACENT_24WIDE_20261004.md,
  steal-door table, row 11), and the cop fix is the ONLY named gate.
- X_INTEL_PRIMER_20261004.md:55-57 verified verbatim ("a primer that only entertains is
  a soundtrack; the property that makes it a Primer is the verification ractive closing
  the loop. Estate has both halves in separate organs; the moonshot is the weld").
- tools/beat_map.py:138-172 read: damage_map is deterministic by construction
  (golden-angle walk k*137.50776405, no RNG), so the 574-row count is a stable
  per-run artifact of the lane's estate-track run.
- No competing weld work: newest watch/inbox receipts (ls -t) are LTCP steal map,
  arena tripwire, cop, primer; no weld/ractive build receipt exists.

And the swing is STRONGER than the lens argued: door 2 landed in parallel mid-flight
(00cb15c77) and EG-20 explicitly rides the now-live bench, so the ladder's cheap end
is clearing itself while the weld stays unclaimed. I also re-derived what the lens
left receipt-carried (see additions): the 65-green suite and the 529 census both
reproduce on the current tree.

Caveat carried, not a weakening: the 529/161-88-64-216 figures are moment-stamped
receipt numbers; my same-instrument rerun reads 541 payloads, 163/89/67/222 at ~17:00Z
(new run dirs landed after the receipt; the moving-tree law explains the delta, not a
defect).

### F4 "pheromone metabolism half-exists ... so the 4-8h door is half price" -> WEAKENED

Byte-checks that PASSED: tools/gps_mcp/ledger.py:433 is the 1/n running mean
(`new_rate = (old_rate * old_size + v) / new_size`), :434-443 is the floor with the
exact quoted comment ("a fail absorbs (rate unchanged), it never rewards" at
:439-440), :80-87 is the momentum window derivation (verdict_log window, oldest half
vs newest half, badges).

Why weakened: the mechanism is mischaracterized and the missing-list is incomplete.
- "slashes on fail streaks" is wrong on both words: the floor fires on a SINGLE fail
  while the window is RISING (`if v == 0 and mom is not None and mom.rising`,
  ledger.py:434), and it clamps to min(floor, old_rate), a bounded demotion, not a
  slash; no streak-keyed logic exists anywhere in the file (the STREAK-n badges at
  :86-87 are PASS-streak badges, display-only).
- The door's three named components (primer receipt line 210: "alpha-decay,
  dispute-streak slashing, and drift-patrol-keyed shift-reset") are ALL missing. The
  lens's list ("only time half-life and drift-patrol-keyed shift-reset are genuinely
  missing", moonshot-1.md:133-134) silently drops dispute-streak slashing because it
  equates the single-fail floor with it. What half-exists is the momentum-window
  plumbing (window derivation, floor hook, verdict_log feed), which genuinely
  discounts the build, but "half price" is generous arithmetic: two of three named
  components plus the shared decay-family schema are still to build.

### F5 "monoculture proxy is cargo-gated ... spend the ticket on the prober" -> WEAKENED

Byte-checks that PASSED: commit 03da1ee56 message contains "grok-4.7 403 unfunded
noted (xAI reissue thread)" (git log -1 03da1ee56, rerun this session);
watch/inbox/ractor_engine/2026-10-04-parked-decisions/LAND_hermes_merge.md:62 is
harder than the lens's cite: "UNFUNDED 2026-10-04: both XAI_SD_API_KEY and
GROK_API_KEY resolve to team 715bf1ab 'used all available credits'" (credits
exhausted, not merely a reissue thread);
`git grep -n -i -E "agreement|overlap|monoculture" -- tools/social_rsi.py` -> zero
(rerun this session); tools/zknot.py:198-209 is the meter exactly ("METER
self-steal+forgot per 1000 human prompts ... dive baseline ~148, target <75").

Why weakened: "cargo-gated" drops the door's own first test case. The door specs
cross-LANE agreement / citation-overlap over parallel lanes (primer line 172), and the
reviser's rank-4 row says why it works single-model: "this single-model dig is its own
first test case" (primer line 221). Correlated-error banking among same-model sibling
lanes needs no second funded family, and the alert is specced on SHARP DROP against
the instrument's own baseline, not an always-fire constant. The lens's counter
("shared sources are correlated evidence, not correlated error", moonshot-1.md:144-145)
is a fair hit on the citation-overlap leg but does not touch the verdict-agreement
leg (gwap verdicts are execution-checked, not source-shared). What survives of F5:
the EV re-rank (build the clippy prober first; it is the only missing
retrieval-practice state, and my full-tree census below proves the absence harder).
What does not survive: the kill verdict "GATED CARGO until a second funded family
exists".

## Additions: what the lens missed

1. DOOR 2 LANDED MID-FLIGHT; THE LENS'S #1 MOVE IS DEAD ON ARRIVAL. Evidence:
   commit 00cb15c77 at 2026-10-04T12:39:31-04:00 (tests/test_arena_bench.py +94 lines,
   mag/arena_bench.py repointed, ARENA_BENCH_TRIPWIRE_20261004.md banked); lens report
   mtime 12:43:45 -0400 (stat), still ranking "arena-bench pin (~30 min)" as move 1
   (moonshot-1.md:162); `pytest -q tests/test_arena_bench.py
   tests/test_night_march_cure_20261004.py` -> 10 passed this session. Falsifier: if
   the tripwire tests fail or the commit is reverted, the pin door reopens. Move
   (5 min): strike the pin from the EV order, re-rank from the MCP slice down, cite
   00cb15c77 as the landing.
2. EG-20 pass@K WAS RE-PARENTED, NOT KILLED, AND REMAINS UNBUILT. The tripwire
   receipt claims the diagnostic rides the bench (ARENA_BENCH_TRIPWIRE_20261004.md:46-47:
   "The bench is live again for the pass@K diagnostic (EG-20, the dig's only
   measured-effort item rides this instrument)"); the spec survives at
   ESTATE_GAP_DIG_20261004.md row 9 ("Coverage column (pass@K, large K) beside win
   rate in arena/gwap | 2h | column present; predicts the mesh vs frontier routing");
   `git grep -n -i "pass@k|pass_at_k|passk" -- tools/arena_gwap.py mag/` -> zero this
   session: the column does not exist. Falsifier: the column landing in arena_gwap.
   Move (2h): it re-enters the honest order at the cheap end, now unblocked by the
   live bench; the dig's only MEASURED effort figure should not sit behind an
   eleven-door framing that dropped it.
3. THE "UNDIAGNOSED FAIL VERDICT" IS BY DESIGN, NOT DRIFT. My selftest run mints both
   fixtures: fixture_honest_ghost PASS (score 1.0) and fixture_maru_sycophant FAIL
   (score 0.3675, all three gates red: wrong inscription, 2 sycophantic CONFIRMs,
   foreign brand signature), split_proven: true
   (memory/arena_bench/receipt_selftest_x_20261004T165558Z.json + the two
   receipt_run_fixture-* files it minted). The FAIL the lens could not diagnose is the
   deliberately-failing discriminator fixture; the threshold 0.9 is never in question
   on the selftest path. Falsifier: a selftest where pass_case != PASS or
   fail_case != FAIL (the landed tripwire test 1 pins exactly this). Move (0 min):
   record it; the pin already exists.
4. THE GOVERNING OPERATOR ORDER IS ABSENT FROM THE LENS REPORT.
   ARENA_BENCH_TRIPWIRE_20261004.md:3-6 quotes the mid-flight order: "'go' on the
   build order, then mid-flight 'actually ractor it out self steal then go' - the
   remaining doors ride the ractor-engine". The lens's EV-per-hour table
   (moonshot-1.md:160-171) re-prices doors without citing the authority that routed
   them through this pass, and without the corollary the tripwire landing proved:
   doors with NO design surface can land in parallel now (door 2 did), while
   design-gated doors (weld, three-signal, calibrator, consume-the-ledger) wait on
   this pass's verdicts. Falsifier: an operator countermand of the ractor-first
   order. Move (10 min): annotate the EV table with the parallel-landable vs
   design-gated split instead of a pure serial ranking.
5. THE RECEIT-CARRIED NUMBERS NOW RE-DERIVED, BOTH DIRECTIONS. (a) gwap suite:
   `pytest -q tests/test_gwap_payload.py tests/test_gwap_to_gps.py
   tests/test_gwap_mud.py tests/test_gwap_independent_cop_20261004.py` -> 65 passed
   in 3.82s (the cop receipt's "65 passed" reproduced). (b) v3 census, read-only
   instrument over all playground run dirs (tools/arena_gwap.actor_payloads +
   payload verdict field, no banking): 541 payloads, VERIFIED_AGREE 163 / CHALLENGE
   89 / DISPUTE 64->67 / BLOCKED 222 at ~17:00Z vs the receipt's 529 and 161/88/64/216;
   deltas are new run dirs (e.g. dnd0_20261004T142140Z, banked after the receipt's
   census), the honest shape holds. Falsifier: rerun after the next batch of runs;
   counts must carry a moment stamp per the moving-tree law (tools/arena_gwap.py
   status() docstring, N12). Move (0 min): carry "541 at 2026-10-04T17:00Z" into the
   next receipt, never the bare 529.
6. FULL-TREE FSRS CENSUS (quantifier-law compliant; closes the lens's scoped-grep
   blind spot and HARDENS the prober door): `git grep -n -i -E
   "fsrs|spaced.repetition|free.recall|retrieval.practice" -- .` over the whole
   tracked tree (all zones incl. .agents/skills/ and corpus/, media filtered) returns
   ZERO implementation hits; the only vocabulary hit is doctrinal
   (.agents/skills/fireball-cycle/SKILL.md:9, "a skill is a one-time conversion that
   becomes free recall"), the rest are binary/media coincidences and shadertoy
   filenames (3dfSRs.fragment etc. in catalog/catalog.jsonl). Scope note: git grep
   covers tracked files; untracked working-tree files (the new memory/arena_bench
   receipts) are outside this instrument and are receipts, not code. Falsifier: an
   FSRS scheduler found in an untracked or out-of-repo store (ZMEM was NOT censused
   for this term). Move (0 min): the absence claim is now full-tree scoped; the
   clippy-prober remains the only retrieval-practice state door.
7. PLAYGROUND RUN DIRS ARE NOT EMPTY (the lens's blind spot was an instrument
   artifact): 95 dirs under watch/inbox/playground (37 tavern + 57 dnd0 + 1 other),
   each carrying transcript.jsonl, session.md, DONE, GWAP_BANKED, golden_vectors.json
   (ls of dnd0_20261003T121829Z). The lens's `cmd dir /b` listed empty because the
   backslashes were eaten by the bash-under-cmd shell (my first probe failed the same
   way: "dir: cannot access 'memoryrunsgwap'"). The weld door's runtime evidence is
   real bytes on disk, not just the GWAP receipt's claim. Falsifier: a run dir
   without transcript.jsonl would drop from the census instrument (it filters on
   that file). Move (0 min): none, evidence stands.

## What this pass did NOT do (OWED, never asserted)

- Gero-4B was not downloaded or evaled; the calibrator's download-and-eval gate stays
  unmeasured (the lens's blind spot stands unclosed; only the agentmemory GRAMMAR
  half was closed, server.ts:84-113 read this session).
- No external web verification (mem0, graphiti, Gero-4B card facts remain
  receipt-carried); this pass worked local bytes only.
- ZMEM (the harness store outside the repo) was not censused for FSRS vocabulary.

## Effect on the honest build order

Lens order (moonshot-1.md:160-171) corrected by this pass:
1. ~~arena-bench pin~~ -> LANDED 00cb15c77, strike.
2. EG-20 pass@K (2h, measured, bench live) -> cheapest true open door.
3. MCP registry slice (~1 sitting) legitimate as a FIRST SLICE only; reconciliation
   pass + citation cure (X_INTEL_AIENG_SCRATCH:89,:92-94) still orders the grammar
   work behind it.
4. Weld door: gate open (cop landed), no competing build, census re-derived; the
   swing stands (F3 confirmed).
5. Night-cycle per-leg resume: still open at 1-2h (not 15 min, not 2-4h; the
   observability half landed).
6. Clippy prober before monoculture proxy on EV grounds; the monoculture door is
   downgraded, not cargo (its same-model test case survives; the xAI reissue revives
   the cross-model leg at full value).
7. Pheromone metabolism: discounted by momentum plumbing, but all three named
   components remain to build; price it 3-6h, not 2-4h.
