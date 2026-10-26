# CAPABILITY_MATRIX_PILOT - DIG-2 (ESTATE GAPS + PILOT), 2026-10-02

**Schema:** capmatrix.pilot.v1 · **lane:** DIG-2 · **method:** bytes-first (every gap
claim names tonight's file; pilot fires ride the gated tools/model_garden rail;
.\.venv\Scripts\python.exe only; no commits; no em-dashes) · **mission:** the MCP
server gives dumb agents frontier capabilities; map the gaps from tonight's own
bytes, then measure row zero of "dumb agent + MCP tool = frontier senses" on the
overmind's fabrication class, bare vs tooled, budget $1.

**Spend:** $0.0138 banked (145 API calls, 120,039 prompt / 15,522 completion
tokens, zero refusals, zero empty channels; rows id capmx-* in
memory/runs/model_garden/usage.jsonl). 1.4 pct of the allowance; the $0.50
in-script hard guard never came within $0.48 of binding.

---

## PART 1 - THE GAP MAP (capability x agent x MCP tool, tonight's bytes)

Agents are the dumb fleet the harness actually runs. Evidence is tonight's
(2026-10-01/02) unless the row says banked-earlier.

| # | Frontier capability | gemma2 scut (Q5_K_M) | gemma4 (local reviewer) | glm-5.3-flash | deepseek-4.1-flash | kimi-k2 / k2.6 | MCP tool that supplies it |
|---|---|---|---|---|---|---|---|
| G1 | Byte-grounded sensing (justify from served bytes only, no over-extrapolation) | UNTESTED as sensor (its cite hallucinations, G4, are the same disease) | UNTESTED as sensor | **FAIL in the live hour**: 12/40 ticks fabricated under the mechanical instrument (6x "six/6 consecutive" fill=0 from a 2-row tail at t8/t10/t14/t17/t26/t38; 1x invented path watch/inbox/salon_mine/ at t16; 5x window overflow at t2/t6/t9/t18/t30). Judges caught only 2 (p14, p16) | PASS as judge (ds1 on p14: "B fabricates evidence") | PASS as judge (kimi on p16: "invents a second salon dir") | **get_state** (byte-grounded senses reads; claims limited to pulled bytes) |
| G2 | Right-sized context (survive estate material without dump death or truncation) | WEAK (B7 0.25; 8192 ctx) | FAIL (B7 0/4; ctx 8192, server kept the tail; B2/B5 finish=length) | PARTIAL (B7 0.75) | WEAK (B7 0.25, weakest remote cell) | **FAIL on dumps**: k2.6 239KB register = 900s timeout x2, zero bytes, 30 min wall; k2 landed 85,573 prompt tokens but coordinates died (G4) | **get_context** (budgeted, hot-first, compressed pulls; the 239KB class dies) |
| G3 | Format discipline (byte-exact reply shapes) | **FAIL 0/6** (B6: fenced B1..B7 list + trailing whitespace; LINE-COUNT, LINE-1/2/3, NO-FENCE, NO-TRAILING-WS all zero) | PASS 6/6 B6 | PASS B6 1.00 | PASS B6 1.00 | PASS B6 | **get_law** (format/discipline rows injected per ask; the law rides the ask, not the model's habits; only the scut needs it tonight) |
| G4 | Byte-exact cites (coordinates, not content) | FAIL (descent_driver.sh:183-186 cite on a ~40-line file; B4 cite failed CITES-RESOLVE) | WEAK (B1 hermes_burn.py:1/:6 + B5 steer_seal.py:3 flagged hallucination-risk; B3 4/5 its best cell) | PASS (RUN_UNIQUE: 0 invented, rows exact 52/56, SELF-TOTAL exact; pilot v1 0/15 wrong) | PASS-ish (B1 CITES-RESOLVE 1, DISTINCT-EVIDENCE 0) | **FAIL**: every row cite off by 9 on the 600-line register (cited 69-78, truth 78-87); kimi1 B3 cite exceeds file length | **verify_cite** (mechanical post-hoc alignment; off-by-9 dies at the gate) |
| G5 | Steer/envelope conductivity | untested | untested | **FAIL 0/4** (STEERING_DOGFOOD: sealed envelope read as +282 tokens, not executed; turn-2 unsteered re-derivation) | untested | PASS 4/4 (one lexical leak); pheromone marks 5/5 | **get_terrain** + **get_law** (terrain carries the per-family conductivity fact "glm ignores envelopes at low effort"; law serves the unwrapped-payload adaptation) |
| G6 | Routing wisdom (novelty, pacing, which surface deserves attention) | untested | untested | **FAIL as overmind**: restaged standing drift 32/32 STAGE_ASK; pacing agreement 7.14 pct vs the 60 pct floor (OVERMIND-KILLED, kill 1) | untested as router | untested as router | **get_terrain** (GPS head, temperature, momentum; a novelty gate reads it before staging) |
| G7 | Position anchoring (work tied to graph coordinates) | absent | absent | absent | absent | absent | **get_position** (BLOCKED until KACHE lands; serves "not yet banked" honestly per MCP_LATTICE_5W) |

Evidence files: GRID_local-20261001-a_RECEIPT.md (G3 scut, G2 local, G4 locals),
OVERMIND_HOUR_VERDICT.md + memory/runs/overmind/ledger.jsonl (G1, G6),
STEERING_DOGFOOD.md (G5), RUN_UNIQUE_X2.md (G2 kimi, G4 kimi/glm),
GRID_cheapgrid1.json + GRID_kimi1.json (B-item scores),
memory/runs/overmind/judgment_r20261002T010001Z-hour.json (judge catches).

**Read of the map:** the dumb fleet's gaps are not uniform. glm-flash lacks
discipline-class senses (G1 live), kimi lacks context economics (G2) and cite
coordinates (G4), the scut lacks format law (G3) and cite honesty (G4), gemma4
lacks window (G2), deepseek-flash lacks long-context breadth (G2). One MCP tool
per gap, and five of the seven gaps are fixable by READS (get_state, get_context,
get_law, get_terrain, verify_cite): no new authority crosses the wire, which
matches the ractor50 never-rows and the 5W owner analysis.

---

## PART 2 - THE PILOT (row zero: dumb agent + tool loop = frontier senses?)

### Design

Sharpest testable gap: the overmind brain's fabrication class (G1). The brain is
glm-5.3-flash on the gated rail; the hour banked its fabrications in a
hash-chained ledger, so the ground truth is already on disk. The pilot re-runs
the fabrication-prone sense asks two ways:

- **BARE**: the hour's own shape. Pinned senses inline in the contract, single
  turn, the hour's own anti-fabrication law present ("never invent estate state
  that is not in the senses").
- **TOOLED**: no senses inline. The model may call ONE local tool,
  get_state(surface) in {beat, git, queue, landed}, implemented by this lane as
  a json function returning the SAME pinned bytes; the result feeds back through
  the rail's turn2_only revision surface (tool result only, no directives). This
  is the tool-loop pattern and it dogfoods the pull budget law (max 1 pull per
  ask, the 5W anti-chatter twin of pull-over-dump).

Corpora (all glm-5.3-flash @ zai, recipe-planned uncapped + reasoning_effort
low, identical law text across arms):

1. **claims probe** (v1): 3 questions (beat window @t14, git salon paths @t16,
   queue counts @t25) x 5 reps x 2 arms. Answer schema demands byte-checkable
   claims.
2. **free-form variant**: the hour's exact reply schema (verb/reason/payload, no
   claims block) x 3 pinned ticks x 5 reps x 2 arms. This is where the hour's
   fabrications lived.
3. **dirty-tick re-runs**: the hour's 12 instrument-flagged ticks + 3 clean
   controls, fresh fires, both arms, free-form.
4. **verbatim control**: the hour's contract text reproduced EXACTLY (tools/
   overmind_brain.render_contract verbatim, run id included) on the 12 dirty
   ticks, bare arm, closing the "PILOT RE-RUN preamble changed the pressure"
   confounder.

Grading is mechanical against the pinned bytes (no judge model): claims fields
compared exact; the reason scanned so every number (digit or word) and every
estate-rooted path must exist in the served bytes, with one narrow waiver for
arithmetic derived from operands both stated in the reason. Instrument
validation: the hour's own t14 and t16 replies grade FABRICATED verbatim; clean
replies grade clean; three false-positive classes found on real replies and
fixed with regression tests (derived percent 38/50 -> 76; slash-compounds
01:17/01:19; verb vocabulary "ask/alert"). Script:
scripts/tmp_capability_matrix_pilot.py; grades:
memory/runs/model_garden/capmatrix_pilot_grades.jsonl (142 rows); outputs:
watch/inbox/model_garden/capmx-*.md; staging: memory/plans/garden_battery/
capmatrix/.

### Numbers

| corpus | arm | n | fabricated | rate |
|---|---|---|---|---|
| THE HOUR ITSELF (banked 2026-10-02T01:00Z, live, hash-chained) | bare free-form | 40 | 12 | **0.30** (7 hard: 6x six-consecutive + 1x invented path; 5 window overflow) |
| same hour, judge panel (kimi + 2x deepseek, 14 sampled pairs) | bare free-form | 14 judged | 2 caught | 0.14 of judged pairs |
| claims probe | bare | 15 | 0 | 0.00 |
| claims probe | tooled | 15 | 0 | 0.00 |
| free-form variant | bare | 15 | 0 | 0.00 |
| free-form variant | tooled | 15 | 0 | 0.00 |
| dirty-tick re-runs | bare | 15 | 0 | 0.00 |
| dirty-tick re-runs | tooled | 15 | 0 | 0.00 |
| verbatim hour-contract control | bare | 12 | 0 | 0.00 |

Tool-loop conductivity (the 5W doc's named untested beam, now measured for
glm-5.3-flash): **43 of 45 tooled fires called the tool first-try** (2 direct
answers, both clean); when the ask names the needed surface the pull was right
14/14; unprompted, it defaulted to the beat surface 14/14 (the hour's own
emphasis surface). Zero protocol garbage, zero refusals, zero empty channels in
145 calls.

### The finding the falsifier bought

1. **The fabrication is episodic, not snapshot-deterministic.** The hour
   fabricated 12/40 live, but the SAME model on the SAME dirty snapshots, with
   the SAME contract text verbatim, re-ran 0/12; every re-run shape tonight was
   0/102 (95 pct CI upper bound 2.9 pct per fire). The live hour's pressure
   (evolving counters tick over tick, its own outputs landing in its senses,
   sampling luck) is part of the disease; a static snapshot does not reproduce
   it. Bare-vs-tooled fabrication rate is therefore UNRESOLVABLE at this probe
   shape: the bare arm would not fabricate tonight, so there was no positive
   baseline to fix.
2. **The tool loop itself is proven cheap and reliable.** A flash-class model
   drove a json tool loop through an OpenAI-compatible carrier on the first try
   at 96 pct. The load-bearing assumption of "MCP is additive to the carriers,
   not a rewrite" now has a number for the sharpest family.
3. **Structural narrowing is real even without episodes.** The hour's 5
   window-overflow fabrications (citing git paths and landed files outside the
   rendered window while reasoning from beat) are IMPOSSIBLE in the tooled
   shape: the model cannot cite a surface it never pulled. The 7 within-surface
   over-extrapolations ("six consecutive" from a 2-row pull) remain
   model-bound; the tool serves the same 2-row tail.
4. **Design note for get_state v1 (the actionable mechanism):** the
   six-consecutive hunger was a DEPTH request the 2-row window could not
   satisfy. get_state(surface, depth) turns that hunger into a legal pull
   instead of an invention; without a depth parameter the model invents the
   tail it wanted. This goes in the verb genome alongside the pull budget.
5. **The instrument out-hunted the judges.** The mechanical grader flagged
   12/40 hour ticks where the kimi + deepseek panel caught fabrications in only
   2 of the 14 pairs it judged (both catches are inside the instrument's 12), at
   $0 marginal cost. It is reusable on any reason-over-senses corpus and is the
   second reusable organ this program has banked from the overmind kill (after
   the judgment instrument).

### Verdict: **NOT-YET** (as a measured fabrication-rate fix)

The mission's falsifier was run honestly and it cut against the hypothesis:
tonight, bare glm-flash re-ran its own dirtiest asks clean in every shape
(including the hour's verbatim contract), so "the tool fixed fabrication"
cannot be claimed from 0 vs 0. What IS banked from row zero: the conductivity
beam is measured (96 pct first-try tool use by a flash model), the
cross-surface overflow class is structurally dead under pull-only serving, the
mechanical fabrication grader exists and is 6x stricter than the judge panel,
and the disease is characterized as live-context-episodic. The next experiment
that CAN resolve the verdict: wire get_state into the live overmind loop (both
substrate arms live, n = 40+ ticks each), where the episodic pressure exists;
if tooled-live fabricates less than bare-live at matched ticks, TOOLS-FIX-SENSES
banks with a real delta. The depth-parameter note is the design change most
likely to make that delta appear.

Lane DIG-2 seat, 2026-10-02. No commits. $0.0138 of $1.00 spent.
