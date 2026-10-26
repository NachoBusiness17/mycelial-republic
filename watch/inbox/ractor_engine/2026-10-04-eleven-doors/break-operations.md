# BREAK-OPERATIONS hostile pass (2026-10-04)

Subject: the operations lens report on the 11-door sequence. Every cite below
was byte-checked this session against the estate (reads, greps, git, and four
test files actually executed). Instrument for every absence claim is named.
No em-dashes. Moment: 2026-10-04 ~17:30-18:30Z local afternoon.

## Verdict ledger

### Finding 1 (stale sequence, no claim registry, EG-20 second suitor): CONFIRMED

Every checkable cite held, one sub-cite unverifiable, one magnitude error
that does not touch the substance.

- git positions re-run: `git log --oneline --all | grep -nE ...` gives
  00cb15c77 at line 1, bb0f34586 at line 2, 9718e812d at line 46. Exact.
- Commit times re-run (`git show -s --format=%ci`): door 1 bb0f34586
  2026-10-04 12:23:16 -0400, door 2 00cb15c77 12:39:31 -0400. The lens said
  "door 2 landed hours after door 1": it is 16 minutes, not hours. The
  substance (concurrent seats executing a handed sequence) is untouched, and
  both doors landed AFTER the primer register (15:32:10Z = 11:32 EDT,
  watch/inbox/index_events.jsonl row for PRIMER_ADJACENT_24WIDE_20261004.md),
  so the sequence was stale at publication exactly as claimed.
- GWAP_INDEPENDENT_COP_20261004.md:82-83 re-read: "Next doors in the
  receipt's build order: arena-bench CI tripwire (1-2h), clippy-as-prober
  (2-4h), night-cycle checkpoint legs (2-4h)." Byte-true.
- PRIMER:238 re-read: the steal-door table rank 4 row is NIGHT-CYCLE
  CHECKPOINT LEGS. Byte-true.
- 9718e812d (night-march cure) timestamp 04:55:21 -0400: landed 44 commits
  and 7.5 hours before door 1, same morning. The staleness charge holds.
- ESTATE_GAPS_20261004.json: EG-20 id at :305, "status": "open" inside the
  :305-317 block. Door-2's commit message does declare "the pass@K
  diagnostic rides it". Confirmed open with a declared suitor.
- Door-claim absence re-run (my instrument: grep -rn over queue/ and
  watch/inbox/ for "pass@k" and "clippy-as-prober" plus claim-words,
  primer excluded): queue/todo.md carries zero door rows; every pass@K hit is
  a receipt or a sibling-lens analysis; economics.md:131 recommends "land the
  tripwire + EG-20 + clippy-as-prober" but names no owning seat. No door-claim
  row exists at this scope. Absence claim survives re-census.
- Convergence counts "4/5/2/4/2" (accuracy/communication/lineage/logic/
  moonshot-2): NOT reproducible. Six patterns tried (00cb15c77; "door 2";
  "door-2"; "tripwire"; "arena"; "00cb15c77|ARENA") give 3/1/0/1/2, 1/4/2/7/5,
  1/1/0/0/1, 3/8/3/10/5, 8/13/8/19/12, 10/13/8/19/13. None matches. The
  DIRECTION holds (all five files cite the door-2 landing nonzero under every
  pattern), so the CONVERGENT label stands; the count vector is unverifiable
  because the lens named no pattern. Sub-cite weakened, finding stands.

### Finding 2 (roshomon adapter + weld sizing dead): WEAKENED

First half confirmed but with its own falsifier fired and resolved; second
half's causality killed by register timestamps.

- mag/roshomon.py:9-19 docstring confirmed (core = statements held by >=2
  witnesses). mag/roshomon_mine.py:53-65 confirmed (compare(domains=...)
  parameterized, witness counts in output).
- The sibling-roshomon absence re-run: grep -c -i roshomon over the dir gives
  0 in accuracy, communication, dogfood, economics, lineage, logic,
  moonshot-1, moonshot-2, security (exactly the 9 sibling files) and 8 in
  operations.md itself (the audited lens). Claim byte-true and precise.
- tools/env_contract.py caution confirmed: :618-622 runs the real engine
  against a constraints-only oracle, :648 banks agreement_rate = agree/cases.
  It is engine-vs-oracle self-agreement, not a cross-lane proxy. Correct.
- Falsifier resolved AGAINST the letter of the finding: roshomon's dispatch
  is welded to the k8s swarm (dispatch() at mag/roshomon.py:107-117 writes
  mag.swarm_worker's queue; _answers_for() at :179-187 reads swarm results
  off the shared PVC; compare() at :189-203 errors "no swarm results yet"
  without them). An adapter over compare() CANNOT be fed lane transcripts.
  The real self-steal is the pure scoring core: _invariant_statements (:140),
  _clean (:163), _tokens (:168), _overlap (:172) are importable without the
  k8s path. "Adapter over compare()" is wrong; "adapter over the scoring
  internals" is right and cheap.
- Weld-half causality KILLED: the lens claims the 1-2 day weld sizing "died
  when MAG_DANCE v0.2 landed the deterministic damage-map contract today".
  Register order says otherwise: MAG_DANCE_V02 registered 2026-10-04T11:38:57Z,
  PRIMER registered 2026-10-04T15:32:10Z (watch/inbox/index_events.jsonl,
  register rows read this session). The primer was published four hours AFTER
  v0.2 and its weld door already cites the damage rows as existing input
  ("the damage-map rows (574 deterministic... from tools/beat_map.py:139-172)",
  PRIMER:124). The sizing was made with the damage map in hand; v0.2 did not
  post-date it. What the lens may have half-seen: the primer carries the
  STALE v1 figures (PRIMER:106 "123.05 BPM / 574 beats" vs the v0.2 commit
  f1b3d791f correcting dance.mp3 to 129.20 true BPM), so the reviser's sizing
  did not fully price v0.2's 6-test determinism contract. Honest verdict:
  the weld door's sizing SHRANK (playback half exists in
  dashboard/static/mag_dance.html, damage rows tested), it did not "die":
  my greps over tools/arena_gwap.py, mag/gwap_payload.py, mag/lane_runner.py
  for beat/damage/weld wiring return zero matches (git grep + grep -l, exit
  1), so the learner-answer capture + gwap banking half is genuinely unbuilt.
  2-4h is plausible, not proven; 1-2 days is now conservative.

### Finding 3 (decay-family pre-gate already satisfied one organ over): CONFIRMED, one wording correction

- mag/republic.py:15 area (house-chain law, superseded never deleted),
  :57-58 (FROZEN comment, superseded_by among only two mutable fields), :114
  ("set once, by supersede(); never edited"), :207-213 (AppendOnlyViolation
  enforcement): all byte-confirmed.
- supersede() read in full (mag/republic.py:396-419): mints a successor
  retraction letter, points old.superseded_by at it, bans double-supersede
  and re-pointing. The lens's falsifier resolves FAVORABLY: the mechanism is
  store-generic (int successor pointer + append-only + save-time
  enforcement), portable to edge-id pointers; it is not welded to the letter
  DAG shape in any way that blocks the port.
- Absence grep re-run: `git grep -n -E "superseded_by|valid_at|invalid_at"
  -- mag/mycelium.py tools/gps_mcp/ledger.py mag/river.py mag/swarm_tools.py`
  -> exit 1, zero matches. Exactly as claimed.
- tools/gps_mcp/ledger.py:430-443 confirmed: running mean at 1/n with the
  mom.rising window_start_rate floor ("a fail absorbs... never rewards").
- mag/mycelium.py:265-277 confirmed: decay() sets e["decayed"]=True through
  _rewrite_edges (a whole-file rewrite), log-only, no successor lineage.
- moonshot-2.md:214 confirmed verbatim ("already defined; port, do not mint").
- CORRECTION the lens missed: its move says "porting superseded_by/valid_at
  from mag/republic.py". republic.py carries ZERO valid_at/invalid_at/
  expired_at (grep over mag/republic.py, exit 1). Only superseded_by is
  estate-held; the valid_at/invalid_at bi-temporal axis must still be minted
  from the Graphiti spec. The pre-gate is satisfied ONE organ over
  (supersession), not two. The 1-day move stands; its wording overclaimed.

### Finding 4 (night-march cure / lane_runner, text truncated mid-sentence in the handed report): CONFIRMED on every visible cite

The report arrived cut off ("_save_state re-raises on the r..."); verdict
covers the visible portion only.

- mag/lane_runner.py:124-149 confirmed: atomic tmp+os.replace, the comment
  names the Errno-22 bursts, lane_scheduler.log 2026-09-14..2026-10-04, and
  the 5x CYCLE_FAIL 2026-10-03 -> ~100s re-run class.
- Trail-before-persist confirmed at :933-938 (_trail then _save_state), with
  the in-code comment carrying the same harm narrative.
- tests/test_night_march_cure_20261004.py:100-119 confirmed:
  test_cycle_night_trails_composite_even_when_state_write_fails pins the
  ordering and keeps the march tail.
- cycle_night (:911-939) confirmed: monitor and march run unconditionally;
  the only gate is the whole-cycle last_night date. No per-leg flags exist.
- Residual the lens left unstated: the cure is CLASS-scoped, not total. The
  pinning test itself proves that when _save_state still raises, last_night
  never sticks (pytest.raises(OSError) with the CYCLE row kept), so a
  persistent tmp-write failure would still re-run monitor+march. The atomic
  save removes the observed O_TRUNC class only. Moonshot-2.md:212 converges:
  "Per-leg checkpoint flags: the class was cured by 9718e812d; verify, do
  not rebuild."

## Additions (what the lens missed)

1. THE EMBEDDING LANE ALREADY EXISTS (three-signal broker). The lens hedged
   "may still be mintable from an unchecked module"; it was. mag/
   flock_scheduler.py:57-76 _ollama_embed queries local Ollama
   (localhost:11434, nomic-embed-text, 8s timeout) and :33-56 _embed wraps it
   with a deterministic sha256-geometric fallback ("never crash"). The
   broker's "new embedding lane" is a wire to this organ at full dimension
   (take the vector before _normalize's dim-3 reduction). The primer's kill
   falsifier ("any network or external-DB dependency kills it") resolves
   favorably: localhost only, no external DB. The 1-2 day sizing dominated
   by "the embedding lane choice" shrinks. Falsifier: if nomic-embed-text is
   not pulled in the local Ollama instance, every call silently falls back to
   hash-geometric (the docstring admits weaker clustering); run `ollama list`
   before the recall@5 baseline. Evidence: mag/flock_scheduler.py:33-76 read
   this session.
2. ROSHOMON'S PURE INTERNALS ARE THE REAL STEAL. compare() dies on lane
   transcripts ("no swarm results yet", mag/roshomon.py:203) but
   _invariant_statements/_clean/_tokens/_overlap at :140-177 are importable
   pure functions. A monoculture proxy is an import + a ~30-line lane-feed,
   not a compare() adapter. Falsifier: any adapter design that routes
   through dispatch() or _answers_for() inherits the k8s PVC dependency and
   dies outside the cluster. Evidence: mag/roshomon.py:107-203 read this
   session.
3. MOONSHOT-2.md:212 IS CONVERGENT WITH FINDING 1 AND THE LENS DID NOT CITE
   IT: "Per-leg checkpoint flags: the class was cured by 9718e812d; verify,
   do not rebuild." The lens cited :214 for finding 3 only. The
   stale-sequence finding now has an independent sibling ruling on its
   sharpest instance. Evidence: moonshot-2.md:210-215 read this session.
4. THE PRIMER CARRIES STALE v1 BEAT FIGURES the honesty section does not
   list: PRIMER:106 banks "123.05 BPM / 574 beats / 574 deterministic damage
   rows" for dance.mp3, but commit f1b3d791f (MAG DANCE v0.2) corrects
   dance.mp3 to 129.20 true BPM ("v1 read 64.6 below its own lo=80... v2
   reads 129.20 true"). The primer registered at 15:32Z, after v0.2 at
   11:39Z, so this is an erratum of the revision pass, not of a lane.
   Evidence: PRIMER:106 read; git log f1b3d791f read; index_events.jsonl
   register rows read.
5. THE WELD DOOR HAS A NAMED CONSUMER IN THE ESTATE'S OWN RECEIPT, uncited
   by lens and primer: MAG_DANCE_V02_20261004.md:91 "game_brawl pressure-line
   wiring: damage rows as a Mountain brawl feed (owed wiring)". The ractive
   challenge loop has a second estate consumer beyond gwap banking, which
   changes the door's EV numerator. Evidence: MAG_DANCE_V02_20261004.md:88-91
   read this session.
6. TESTS NOW EXECUTED (the lens's blind spot #1, cured): .venv/Scripts/
   python.exe -m pytest -q over tests/test_arena_bench.py +
   tests/test_night_march_cure_20261004.py + tests/test_gwap_independent_cop_
   20261004.py + tests/test_beat_map_v02.py -> 25 passed in 4.59s. All four
   pinning suites (doors 1 and 2, the night-march cure, and the MAG_DANCE
   damage contract) are green on the current tree.
7. THE MCP GRAMMAR IS THIN (the lens's blind spot #2, sized): agentmemory
   src/mcp/server.ts:75-120 memory_recall validates exactly query (required
   string), format (full|compact|narrative), token_budget (positive int),
   agentId (optional), limit (default 10), then delegates to
   sdk.trigger("mem::search"). standalone.ts:18-26 confirms the 7-tool set.
   The estate's mag/mcp_server.py PROTOCOL_VERSION 2025-06-18 is inside
   agentmemory's SUPPORTED_PROTOCOL_VERSIONS list. Grammar-side port is
   ~40 lines of validation; the real cost is the token-budget trimming
   backend (their functions/context.ts, which the estate partially owns as
   context_pack). The primer's 4-8h sizing survives. Evidence: both files
   read at C:/Users/foste/Documents/projects/library_parked/agentmemory/.

## Cargo check (the ask's standing question)

No door is pure cargo after this pass, but two shrink: NIGHT-CYCLE
CHECKPOINT LEGS (harm class cured 9718e812d; residual is a persistent-
mount-failure re-run, low EV against 2-4h) and THREE-SIGNAL-QUERY-BROKER
(the dominating cost, the embedding lane, is a wire to flock_scheduler).
The DOORS ledger move (30 min, finding 1) remains the cheapest and gates
every other race.

Writer: break-operations (hostile second pass, eleven-doors ractor engine)
fetched: 2026-10-04
