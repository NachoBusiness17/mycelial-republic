# OPERATIONS LENS - the 11 remaining doors, audited against live bytes (2026-10-04)

Writer: lens-operations, ractor on the Mag estate. Topic: the 24-wide dig's 11
remaining build doors and their reviser-ordered sequence (receipt
watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md, read in full this session;
door-1 receipt watch/inbox/GWAP_INDEPENDENT_COP_20261004.md read in full).
Every claim below cites what I read or ran this session. No test suites were
executed by this lens; landings are verified from git log, disk bytes, and file
reads, never re-run. No em-dashes.

## The one-line verdict

The handed sequence was stale at hand-off: 2 of the first 5 doors were already
built or cured before this ractor opened, two more doors carry unmined
self-steals that cut their sizing, and nothing on the estate claims doors, so
seats are executing the same queue concurrently with no collision surface.

## Door-by-door state (instrument: git log, git grep, file reads, this session)

- ARENA-BENCH CI TRIPWIRE: LANDED, commit 00cb15c77 at 2026-10-04 12:39:31
  -0400 (git show --stat: mag/arena_bench.py +9, tests/test_arena_bench.py +94,
  watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md +52). Fix comment at
  mag/arena_bench.py:66-72 names the 459-byte redirect stub as the real cause
  and the canonical repoint. A second seat building this door is a pure
  duplicate.
- NIGHT-CYCLE CHECKPOINT LEGS: harm CURED by 9718e812d (night shift lane 7/10,
  44 commits BELOW door 1 in git log --oneline, i.e. landed BEFORE the GWAP
  receipt recommended it as a next door at GWAP_INDEPENDENT_COP_20261004.md:83).
  _save_state is atomic tmp+os.replace (mag/lane_runner.py:124-149),
  cycle_night trails before persisting (:932-938), pinned by
  tests/test_night_march_cure_20261004.py:100-119. Residual: _save_state
  re-raises on rename OSError with no retry (:144-149), so the full-cycle
  re-run class persists, but its legs are now monitor rc=0 plus a named $0
  march rc=2 skip (:925-931), so the harm is a redundant cheap monitor run.
  Verdict: cargo-verify, not build. CONVERGENT with moonshot-2.md:213
  ("cured by 9718e812d; verify, do not rebuild").
- MONOCULTURE AGREEMENT-RATE PROXY: SELF-STEAL EXISTS, unmined by every other
  lens (grep -c roshomon across the 9 sibling lens files = 0 hits everywhere).
  mag/roshomon.py:9-19 implements the exact organ: N witnesses answer the same
  question, answers normalize into statements, the recurring core (statements
  held by >=2 witnesses) is the convergent signal; mag/roshomon_mine.py:53-65
  shows compare(domains=[...]) is parameterized and its output carries witness
  counts. The proxy is an adapter over per-lane findings plus an
  memory/attention.md alert, not a new scorer. Caution:
  tools/env_contract.py:648 also computes an agreement_rate but it is
  engine-vs-oracle on legality cases (mag-vs-law self-agreement, :620-622),
  NOT cross-lane model agreement; do not mislabel that wire as the proxy.
- WELD DOOR: the damage-map contract LANDED TODAY, after the receipt sized the
  door 1-2 days. watch/inbox/MAG_DANCE_V02_20261004.md "THE DAMAGE MAP CONTRACT
  (tools/beat_map.py damage_map)", row shape {t, zone, hp, imp, downbeat,
  strength}, deterministic, no RNG. Dependency (cop fix) landed bb0f34586;
  playground scene infra is live (watch/inbox/playground/tavern+dnd dirs in git
  status). Remaining build: the on-beat challenge loop plus gwap banking. No
  other lens cites MAG_DANCE or damage_map (grep -c = 0 across 9 files).
- PHEROMONE METABOLISM + MYCELIUM-V2 (decay family): the family pre-gate
  "define the vocabulary once" is ALREADY SATISFIED one organ over.
  mag/republic.py:15 (house chain law: "superseded by another, never deleted
  or edited"), :57, :114 (superseded_by field, "set once, by supersede(); never
  edited"), :209-213 (immutability enforcement). My scoped grep over
  mag/mycelium.py, tools/gps_mcp/ledger.py, mag/river.py, mag/swarm_tools.py
  for superseded_by|valid_at|invalid_at returns zero: the vocabulary lives in
  the republic letter chain, so the family PORTS it, it does not mint it.
  CONVERGENT with moonshot-2.md:214 ("already defined; port, do not mint"),
  which reached the ruling independently; my addendum is the byte cite
  (mag/republic.py:114) and the hook: tools/gps_mcp/ledger.py:433-443 already
  banks a momentum object (mom.rising, window_start_rate floor) that
  decay/reset keys onto. mycelium decay() exists log-only
  (mag/mycelium.py:265-277, boolean, no successor lineage).
- CLIPPY-AS-PROBER: genuine build. git grep -i for
  fsrs|spaced.repetition|free.recall over mag/*.py, tools/*.py, gps_mcp,
  tests/*.py returns ZERO hits; memory/retrieval/ does not exist on disk (ls).
  CONVERGENT with accuracy.md:68 ("NOT HELD").
- BUILD-ONCE CALIBRATOR: split the door. tools/oracle_calibration.py:14-27,124
  implements ECE/MCE/Brier, temperature fitting, per-domain drift flags,
  stdlib-only, with an --input JSONL row shape {confidence, correct,
  decision_class} (:35-37 per moonshot-2's read; docstring and :124-176 read
  by me). The calibration-flag half is a 2h adapter (moonshot-2.md:128-133
  names the wire: router ask receipts joined to gwap verdicts; its 15-min
  join-key falsifier must run first). The Gero-4B download gate (4-8h, no
  published evals, X_INTEL_PROPER_SCORING_20261004.md:44-45) is cargo until
  the second-price revelation layer is actually demanded. CONVERGENT with
  moonshot-2.md:208.
- MCP-LATTICE SHIM: gated and the gate is unstarted. No reconciliation receipt
  exists in watch/inbox/model_garden/ (only MCP_LATTICE_SPEC_SEED.md and
  MCP_LATTICE_5W.md; ls this session); mag/mcp_server.py serves none of
  build_context_pack/lattice_query/memory_recall (git grep = 0). The estate-side
  self-steal map already exists: MCP_LATTICE_5W.md (2026-10-02) reads "the
  estate already owns every organ the lattice needs except the four verbs and
  the meter" (TOOL_MAP 42 tools, zero get_law/get_terrain/get_position/
  get_context). The door is a tool surface over existing organs AFTER the
  agentmemory grammar pass ordered at X_INTEL_AIENG_SCRATCH_20261004.md:92-94.
- THREE-SIGNAL QUERY BROKER: gated as specced. The embedding lane is genuinely
  unminted so far as I could check: 8 mag/ modules mention "embedding" but a
  def-level grep over 3 candidates (bare_numpy, context_compression,
  gguf_cartography) found no reusable embed function; I did NOT check all 8
  (blind spot). The recall@5 falsifier must run before any fusion is built.
- CONSUME-THE-LEDGER WIRE: genuine build, gated. mag/flock_field.py:158-161
  steer() computes only goal/separation/alignment/cohesion; no p_best/g_best
  term exists (read this session).

## Findings (ranked)

1. CONVERGENT, ops-primary: the handed sequence was stale at publication and
   doors land concurrently with no claim registry. Evidence: 9718e812d sits 44
   commits below bb0f34586 (git log --oneline --all, grep -n positions 1, 2,
   46), yet GWAP_INDEPENDENT_COP_20261004.md:82-83 ranks night-cycle legs as a
   next door and PRIMER :238 ranks it #4; door 2 landed hours later
   (00cb15c77) with the door-2 commit message declaring "the pass@K
   diagnostic rides it" while EG-20 status is still "open" in
   watch/inbox/ESTATE_GAPS_20261004.json:305-314, a second suitor on the same
   next door. Instrument for the absence claim: grep -rn for
   clippy-as-prober/pass@K claims over queue/ and watch/inbox/ (excluding the
   primer) found only receipts and lens files, no claim row. Falsifier: a
   door-claim row naming the owning seat for pass@K or clippy-as-prober
   anywhere on disk would cure this; re-grep before building either. Move
   (30 min): land a DOORS ledger (one jsonl in this directory, or flip EG
   statuses in ESTATE_GAPS_20261004.json) recording door, status
   (landed/cured/open/claimed), commit, seat, seeded from this audit; every
   door-commencing commit cites its row.
2. NOVEL: two doors carry unmined self-steals that collapse their sizing. The
   monoculture proxy should be wired from mag/roshomon.py compare (N witnesses,
   convergent core, parameterized domains) over per-lane findings, alerting
   memory/attention.md on core-size drop; and the weld door's 1-2 day sizing
   died when MAG_DANCE v0.2 landed the deterministic damage-map contract today
   (row shape banked, dependency landed, playground live), leaving only the
   challenge loop plus gwap banking. Falsifier: roshomon.compare's dispatch
   may be welded to the k8s swarm witness queue such that lane transcripts
   cost more than a fresh 50-line overlap scorer (read mag/roshomon.py
   dispatch, 15 min, before wiring); for the weld door, one rerun diff of
   damage_map output falsifies the deterministic-rows contract the challenge
   loop depends on. Move (2-4h total): roshomon adapter + attention alert;
   challenge loop over damage rows into arena_gwap banking.
3. CONVERGENT with moonshot-2, byte-extended: the decay family pre-gate
   ("define valid_at/invalid_at/superseded_by once, first") is already
   satisfied at mag/republic.py:114 with enforced immutability (:209-213), and
   the GPS ledger already carries the momentum hook (mom.rising,
   window_start_rate floor, ledger.py:433-443). Falsifier: if republic's
   supersede() cannot express edge-level supersession (it was built for the
   house-chain letter DAG), the port dies and the family mints its own fields;
   read supersede() before the first decay commit. Move (1 day, both stores):
   one amendment porting superseded_by/valid_at into lattice_edge.v1 and
   mycelium edges, then pheromone decay keyed to the existing mom window plus
   drift-patrol resets, then mycelium-v2 reusing the same fields.
4. Door-2/night-cycle addendum (CONVERGENT landing, my residual quantified):
   the checkpoint-legs door's harm was cured at the write path; the unbuilt
   per-leg resume now guards only a redundant monitor run. Falsifier: if
   post-cure os.replace failures appear in lane_scheduler.log through the cage
   bind mount (the rename-CAS proof cited in the comment was win32 filter
   locks, a different kernel path than the Linux cage), the re-run harm
   returns and the door re-earns its 2-4h rank. Move (15 min): grep the
   scheduler log for post-9718e812d rename failures; reopen the door only on
   evidence.
5. Ops-honesty: the receipt's own disposition orders are theater. The effect
   broker idempotency flag was ordered "land as a named row or drop"
   (PRIMER :278); my grep for idempoten over watch/inbox/ESTATE_GAPS_20261004
   json returns zero hits, so neither happened. The build-order table's EV
   ranking rides reviser estimates (footnote at PRIMER :231) while only EG-20
   carries a measured figure; today the estimates for two doors (night-cycle
   2-4h, weld 1-2d) died against landed bytes, which is the estimate class
   failing in real time. Falsifier: an amended gaps json row or a landed
   idempotency audit receipt cures it; recheck before citing the primer's
   honesty section as closed. Move (10 min): erratum commit landing the EG row
   or striking the claim, plus estimate-status marks in the DOORS ledger.

## Honest build order by EV-per-hour (operations verdict, this session's bytes)

1. EG-20 pass@K: 2h MEASURED at spec (ESTATE_GAP_DIG :79, the only measured
   figure), dependency landed (bench live), status open, and a rival seat has
   declared it: claim it in the ledger FIRST, then build.
2. clippy-as-prober (2-4h): zero existing bytes, banks the FSRS probes the
   decay family's retrieval store needs.
3. monoculture proxy as the roshomon adapter (1-2h after the 15-min dispatch
   check).
4. weld challenge loop (2-4h; the 1-2 day sizing is dead post-MAG_DANCE).
5. decay family as a PORT (republic.py fields): pheromone metabolism then
   mycelium-v2, one shared amendment.
6. calibrator split: the oracle_calibration adapter (2h, join-key check first,
   moonshot-2.md:131-133); Gero-4B download is cargo.
7. MCP-lattice: the agentmemory reconciliation pass first (ungated, cheap,
   produces the grammar decision), then the 4-verb surface per MCP_LATTICE_5W.
8. three-signal broker (gated: embedding lane check + recall@5 falsifier).
9. consume-the-ledger (gated: flock semantics change).
Cargo: door-2 rebuild, night-cycle per-leg flags (verify-only), Gero-4B
download, the define-the-vocabulary pre-gate, and the primer's stale sizings
for night-cycle and weld.

## CORRECTION ADDENDUM (hostile second pass, same session)

Finding 2 above was verdicted weakened; both halves re-examined against bytes.

ROSHOMON HALF: survives, narrowed. My own falsifier fired:
mag/roshomon.py compare() is welded to the k8s swarm queue. dispatch()
(:109-134) enqueues through mag.swarm_worker to the mag-swarm CronJob;
_answers_for() (:179-186) reads sw.collect() from the shared PVC; compare()
errors "no swarm results yet (dispatch + let the k8s CronJob drain)" at
:200-203 when the queue is empty (all read this session). The adapter target
is the importable pure primitives: _invariant_statements (:140-160),
_clean/_tokens/_overlap (:163-176), plus the grouping loop that lives INSIDE
compare() at :205-209 (statement groups by token overlap >= threshold). The
proxy imports those and reinstantiates the ~15-line grouping loop over
per-lane findings; it does NOT call compare(). Census re-run this ask:
roshomon appears in zero of the 14 sibling lens files other than this file
and its break-operations mirror (grep -c over the 16 files now in the
directory, including the break-* set that landed mid-session). The
env_contract mislabel hazard stands (tools/env_config.py agreement_rate is
engine-vs-oracle at :620-622).

WELD HALF: the "sizing died" causality is WITHDRAWN. Register order
(watch/ESTATE_INDEX/ESTATE_INDEX.jsonl row 21376: MAG_DANCE_V02 mtime
2026-10-04T11:38:57Z; PRIMER file mtime 11:53:33 -0400 = 15:53:33Z) puts the
primer ~4h AFTER the damage-map landing, and PRIMER:124 already cites the 574
damage rows as EXISTING challenge input, so the 1-2 day sizing was made
knowing the map exists; nothing died. Byte-supported restatement: the input
half is done and tested (deterministic rows, 8-track library at
dashboard/static/index_data/beat_map_<stem>.json, tests/test_beat_map_v02.py
6 passed per MAG_DANCE_V02:81-85), the playback half is wired (mag_dance.html
v0.2 per-beat zone flash + HUD, MAG_DANCE_V02:70-77), and the banking half is
fully unwired: git grep -i -E "beat|damage" over tools/arena_gwap.py and
mag/gwap_payload.py returns zero hits (the only lane_runner.py hits,
:1148-1159, are the unrelated scheduler-heartbeat counter), and learner
response capture does not exist. My earlier "2-4h" move figure is withdrawn
with it: no sizing instrument ran, and it was the same reviser-estimate class
I indicted in finding 5. Not adopted from the critique either: its "stale v1
figure (123.05 vs 129.20)" sub-claim fails on bytes. dance.mp3 reads 123.05
under BOTH v1 and v2 (MAG_DANCE_V02:59, "v1 held (123.05)"); 129.20 is
flat_beat.mp3 / flat_beat_loop.mp3 (:60-61), a different track. PRIMER:106's
figure is v2-consistent, not stale.

Corrected move: proxy = 1-2h adapter importing the roshomon primitives (the
15-min dispatch pre-check is now DONE, replaced by this read); weld = build
the capture+banking loop and MEASURE it before quoting hours, with
tools/arena_gwap.py actor_payloads read first (if beat-indexed claims cannot
bind without a transcript-row shape change, the primer's 1-2d stands).

Corrected falsifiers: proxy = run the adapter on the 24-wide receipt's own
lane chapters (the dig is its own first test case, PRIMER:221); if the 0.55
overlap threshold groups all-or-nothing on findings prose, the 1-2h estimate
dies. weld = the actor_payloads shape check above.

## Blind spots

- No tests or selftests were executed by this lens; every landing is verified
  from git bytes and file reads, not re-runs.
- The agentmemory grammar itself (server.ts memory_recall) was not read; the
  MCP-lattice door's port cost is unsized by me.
- The embedding-lane check covered 3 of 8 candidate modules at def level;
  the broker's lane may still be mintable from an unchecked module.
- Sibling lens files landed WHILE this audit ran (dogfood.md appeared between
  two dir listings); convergence counts are moment-scoped to roughly
  12:39-13:10 local 2026-10-04.
- The 24-wide receipt's research claims (external systems, corpus censuses)
  were read but not re-derived; only the door surfaces were re-grounded.
