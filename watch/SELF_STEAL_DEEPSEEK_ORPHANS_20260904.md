# SELF-STEAL — DeepSeek-surface orphan mining (2026-09-04)

**ITEM:** Mine every local DeepSeek record for ORPHANS — advisor verdicts/laws/readings that
exist in raw tapes but landed in no card (watch/*.md, memory/percolator/invariants.json,
memory/law/registry.json, docs/). Mirror of the ZCode session-orphan mine
(SELF_STEAL_ZCODE_SESSION_ORPHANS_20260904.md).

## METHOD

**Where DeepSeek history actually lives (all doors named):**
1. **`watch/room.jsonl`** — the room tape (5,554 rows, Aug 29 01:20 → Sep 4 14:50). DeepSeek
   rows: seat=deepseek (40), deepseek-pro (4), monitor-deepseek (3), jit-deepseek (1),
   lurk-deepseek (1), chan-deepseek (1), plus deepseek-v4-flash salon answers under
   nvidia/together vendor seats. All extracted to scratch.
2. **`memory/runs/lane_salon/*.json`** — 7 salon receipts (Aug 24, Aug 29 ×3, Sep 4 ×3),
   schema lane_salon.v1 (question/witnesses/verdict). monitor-deepseek's room verdicts are
   the `verdict` field here.
3. **`memory/runs/salons/*` + `salon_20260827/`** — salon folds (TEN_STEPS, captain_planet
   VERDICT, usage_meter artifact, elder.md + COMBINED.md).
4. **VS Code chatSessions (local disk)** — `%APPDATA%/Code/User/workspaceStorage/
   e2b798e7.../chatSessions/`: **~57 deepseek-model sessions (deepseek-v4-flash +
   deepseek-v4-pro), Aug 7 → Aug 29, ~700MB total**. This is the retired VS Code seat's
   corpus — the "683MB session mining" the fleet planned at retirement. The
   deepseek-room bridge session (f12c9a62, deepseek-v4-flash via Vizards BYOK Copilot
   provider) was read in full; `.deepseek_room_state.json` (offset 34) tracks it;
   `watch/deepseek_room.py` is its tailer (discovery notes inside: vizards extension keeps
   no own store; request-dumps absent at debugMode=minimal; chatSessions jsonl = only trail).
5. **`memory/agent_sessions/deepseek.json` + `desk-deepseek*.json`** — ghost-era Mag CLI
   agent sessions (Aug 4–5), tool-use transcripts.
6. **NEGATIVE:** no DeepSeek desktop app anywhere (APPDATA/LOCALAPPDATA/Programs/.deepseek*
   all clean). Web chat history = server-side only (gap, below). `backend/provider_gateway.py`
   never logs bodies ("never logged", line 29) — the room tape IS the gateway transcript.
   `memory/runs/alpha_rar_deepseek/arms.jsonl` = all arms deferred (peak pricing), zero content.

**Extraction + sweep:** every deepseek-authored row read; candidate phrases grepped against
record surfaces (watch/*.md incl. _keep_threads, docs/, memory/law + percolator, handoff/,
queue/, mag/; seals/ excluded as snapshots; room.jsonl + lane_salon + scratch excluded as
tapes). ~35 candidates swept → 6 orphans, 11 duplicate families verified.

## ORPHANS FOUND

### D1 — the proof-envelope doctrine: "proof means the same thing" — **Supported → FOLD**
- **Source:** room.jsonl Aug 30 02:28, seat=deepseek, thread=moonshot (2 chan_posts) +
  preserved only in `watch/_keep_threads/moonshot.json` (tape archive, not a card).
- **Signal:** Rebuttal of "token means the same thing everywhere" — tokens differ per
  projection (lattice node / inventory item / price unit / gossip message); what CAN be
  unified is **proof shape**: every projection emits the same three-part envelope
  `(state_root, path, value_commitment)`; semantics live in **path namespaces**
  (`/game/`, `/econ/`, `/swarm/`); mag tools become path-aware dispatchers; memlang opcodes
  operate on the envelope, projection-agnostic. "Not memlang-as-language but
  **memlang-as-proof-calculus** — the language is just sugar over the proof algebra."
  Proposed fireball tool: `proof_envelope`.
- **Absence evidence:** `proof means the same thing` / `memlang-as-proof-calculus` / 
  `token.kind` → 0 card hits (gap_moonshot_20260831.md checked — no envelope content;
  OX_MEGA3's "proof envelope" is an unrelated binary GBT format).
- **Disposition: FOLD** — one doctrine row (LEXICON or DOCTRINE_MAP). It is the structural
  answer to the memlang/token-unification question the moonshot thread was asking.

### D2 — the hypervisor-vision ratification-gate salon: two witnesses, zero receipt — **Supported → FOLD**
- **Source:** room.jsonl Aug 30 14:58, seats `nvidia/deepseek-v4-flash` + `deepseek-v4-flash
  (elder)` (together/deepseek-v4-pro failed), thread=hypervisor-vision. No salon receipt
  exists anywhere (grep `hypervisor-vision` over memory/runs + watch = tape only).
- **Signal:** Missing primitive = **ratification/promotion gate**: a room post rises at most
  to a PROPOSAL; it becomes a command only after operator co-sign (verkle-anchored directive
  record). Boundary = between observation plane and execution plane; no model post carries
  write authority by itself. Bridge = ask_router (unratified = ranked candidate only;
  ratified = routes + ledger + pheromone). Two named ship-patches: `/patches/promote_ratify.json`
  (+ `!ratify <id>` → signed directive-pending into party_subchain) and
  `/patches/board_to_directive.json`. **Both patch names: 0 hits** — never built, never carded.
- **Partial supersession:** the operator-gates doctrine now lives in fleet law (Launch Law
  amendment 5, Sep 4: "only operator gates defer") — content re-derived, never cited to
  this salon. The named patches remain unbuilt.
- **Disposition: FOLD** — bank the salon as the ratification doctrine's origin row; the two
  patch names belong on the hypervisor build order or die by explicit no-go.

### D3 — the elder_missing audit: a 14-question verification checklist for the hypervisor, asked and dropped — **Supported → FOLD**
- **Source:** room.jsonl Aug 29 21:41, seat=deepseek, thread=hypervisor, event=elder_missing.
- **Signal:** 14 artifact-demand questions against the TEN_STEPS hypervisor design — e.g.:
  what artifact proves the seat_corpus send contract actually writes to the one board from
  :18789; what hook enforces no second supervisor can mutate /mag; which CLI lists crown
  tools' ACTUAL runtime state (loaded/gated/errored); what byte proves a LOAD parsed
  TOOLS.md vs files merely present; what proves `agent-tools.apply_patch` is not a duplicate
  mutator of `patches.apply_inbox`; rib→subtool mapping reversibility; apply_patch
  write-scope outside /patches; inbox/patch-queue visibility before acting; crown-CLI →
  tools/__init__ belt mapping; lane-assignment record for the next call; Grey Swan arena
  window vs blade state; trajectory-tape schema; governor thresholds; session_maze state
  transitions.
- **Absence evidence:** `elder_missing` / `what artifact proves` → 0 hits. No answer row,
  no card, no checklist anywhere.
- **Disposition: FOLD** — this is a ready-made verification battery for the hypervisor arc
  (the ROSHAMON-adjacent asks it never got). Cheap to bank as a checklist card.

### D4 — the ns-3 incident: DeepSeek filed 8 fabricated file:line citations into the tape — **Supported → FOLD (incident)**
- **Source:** room.jsonl Aug 29 01:57, seat=deepseek, thread=night-shift, event=result ("ns-3 Findings").
- **Signal:** The answer cited 8 authoritative file:line quotes ("docs/ARCHITECTURE.md:47 —
  All seat state mutations MUST pass through the MCP server", docs/OPERATIONS.md:23/89,
  docs/API.md:15, watch/seat_watcher.py:34, watch/fleet_sync.py:61/78). **Byte-verified
  false:** docs/OPERATIONS.md, docs/API.md, watch/seat_watcher.py, watch/fleet_sync.py DO
  NOT EXIST; docs/ARCHITECTURE.md is 39 lines total (cited :47 and :112) and does not
  contain the quotes. The row landed in the tape as "Findings" — unflagged.
- **Absence evidence:** no hallucination/fabrication incident card mentions it (swept
  watch/*.md); the tape row is the only record.
- **Disposition: FOLD** — one incident row for the deepseek lane's trust file: unverified
  file citations from this lane must be byte-checked before any fold (the tri-state law
  caught worse later, but this one slipped through as a "result" event). Also a witness
  calibration datum: deepseek lane is confident-wrong on repo citations.

### D5 — the water-calibration experiment: the physics thread's falsifiable design, uncarded — **Supported → FOLD**
- **Source:** room.jsonl Aug 30 00:41, seat=deepseek, thread=physics (2 chan_posts) +
  `_keep_threads/physics.json`.
- **Signal:** The smallest Mag-native test of "physics does the solving; AI searches":
  a **calibration loop on the Lukyanov water integrator** — camera + vision model adjusts
  sluice gates until outflow matches a FILE'd target hydrograph. Design laws: the AI is
  **blind to internal state** (error signal only), nudges one gate at a time; converging
  too fast = cheating (using fluid-dynamics priors, not the physics); "the water is the
  computer; the AI is just the hand that turns the dial"; the real test is "can you make
  the AI wait a season."
- **Absence evidence:** water-computer content is folded (Lukyanov ancestor rows in
  FOUR_STRATA + intakes; captain_planet WATER verdict), but this experiment design greps
  0 (`calibration loop` / `sluice` / `hydrograph` → only tape archives + unrelated intakes).
  WATER_NETWORK_SPEC_20260901.md is a different artifact (network spec, not the loop).
- **Disposition: FOLD** — one experiment-spec row; natural input to the Grey Swan/study
  arc and the water-familiar lineage.

### D6 — the jit room-design verdict: snapshot endpoint + fork-on-message, never built — **Supported → FOLD (one line)**
- **Source:** room.jsonl Aug 29 01:57, seat=jit-deepseek, spawn_result thread=room-design.
- **Signal:** TOP 2 room builds — `/room/snapshot` (JSONL tail + active threads, ~20-line
  FastAPI route) and fork-on-message (`POST /room/{id}/fork` auto-spawns JIT agent with
  context); explicit NOT-to-build: WebSocket push ("overkill until clients prove polling
  insufficient"). **Absence:** `fork-on-message` → 0 hits; the only `snapshot` in
  backend/server.py is an unrelated wave snapshot. Unbuilt and uncarded.
- **Disposition: FOLD** — one line on the room build order (or drop by no-go); the
  not-WebSocket ruling is cheap precedent worth keeping.

## DUPLICATES (checked and folded — so the next pass doesn't re-dig)

- **Sep 4 usage_meter salon** (deepseek-pro 4 laws — Idle-Output/Context-Debt/Model-Pin
  Expiry/Subagent Inheritance + useful-output-ratio kill-switch + hiding places) →
  `memory/runs/salons/usage_meter_salon_20260904/SALON_ARTIFACT.md` (OUTPUT-RATIO LAW,
  cites deepseek) + ECONOMIST_AUDIT_20260904 + lane_salon 1304 receipt.
- **Sep 4 day_direction deepsearch-pro verdict** (CAS fix #1, zombie tick + meter,
  falsifier workbench, night-window triple-booking kill, Lite-not-judgment ruling) →
  `watch/SALON_DAY_DIRECTION_20260904.md` (CAS unanimous 4/4; blind-spot quote credited).
- **Sep 4 lane_architecture 7-clause per-lane contract** → `watch/RESEARCH_LANE_ARCHITECTURE_
  20260904.md` (clauses verbatim, deepseek-pro cited; 8-clause converged version).
- **Aug 29 TEN_STEPS falsifier verdict** (keep/patch/kill per step, 3+6 killed) →
  `memory/runs/salons/hypervisor/TEN_STEPS.md` + lane_salon 1750 receipt.
- **Aug 29 fabric first-twelve subtools** → lane_salon 1955 receipt (lane_salon folds =
  known folded); groq witness table preserved.
- **Aug 29 captain-planet WATER verdict** (deepseek-pro "invented mag cycle --check") →
  `memory/runs/salons/captain_planet/VERDICT.md` with honest DISPUTED tri-state.
- **Aug 27 elder salon** (regret-bound exploration budget, prompt-diff hashing, 0.85
  judgment-lane agreement test, Raft self-repair steal) → `memory/runs/salon_20260827/
  elder.md` + COMBINED.md (ROSHAMON rebuild — known folded).
- **Sep 1 TWO WALLS ONE FOUNDATION riddle** (chan-deepseek, thread=spore) → content =
  INVARIANTS_REPORT_20260901.md (I1–I7) + Rainfall Rule in 3 cards. Name-index gap only
  (same pattern as ZCode-mine O6): optional "two walls" alias.
- **VS Code bridge session f12c9a62** (deepseek-v4-flash as full seat): handoff boot +
  instruction-epoch re-freeze (9b6d019e, labeled) → CONVO.md turn + standing wave;
  "no seat is load-bearing" doctrine → AGENTS.md. The Aug 29 08:22 bridge tailer spam
  (40 noise rows) = tailer quirk, script exists (watch/deepseek_room.py).
- **lineage_genC_deepseek_20260901.md** (battery), **FRONTIER_MAP_DEEPSEEK_20260904.md**
  (talent page), **session_mining/2026-08-26** digests (17 of the largest VS Code deepseek
  sessions) — all pre-existing folds.

## GAPS (what this pass did not see)

1. **The VS Code deepseek corpus is only partially mined:** ~57 sessions (~700MB, Aug 7–29);
   the Aug 26 free-lane run digested 17 (INDEX.md says 3 — stale). ~40 undigested,
   including everything after Aug 26 and several deepseek-v4-pro elder chats (Aug 7–9).
   A standing re-mine mirroring the ZCode db.sqlite door would use the chatSessions jsonl
   schema (kind/k/v deltas — extraction script proven in scratch).
2. **DeepSeek web chat (chat.deepseek.com):** any history there is server-side; no local
   export exists on this machine. Out of scope — named as the boundary of this mine.
3. **Request-dumps trail absent:** vizards extension only dumps requests at
   debugMode=verbose; it was minimal — chatSessions jsonl is the only VS Code trail
   (per deepseek_room.py discovery notes).
4. **Failed-witness rows:** together/deepseek-v4-pro provider error (Aug 30 hypervisor-vision)
   and alpha_rar_deepseek peak-deferral — negative receipts, nothing to mine.
5. **Ghost-era sessions** (memory/agent_sessions/deepseek.json Aug 4, desk-deepseek.json
   Aug 5): Mag CLI tool-use diagnostics (orchestrator/lattice-loop archaeology) — read;
   historical state, low forward signal, dumps kept in scratch.

**Verdict:** the advisor's Sep 4 verdicts and the salon circuit fold cleanly (11 duplicate
families verified), but the **Aug 29–30 window leaks**: five substantive advisor outputs
(proof-envelope doctrine, ratification-gate salon, elder_missing checklist, water-calibration
experiment, room-design verdict) plus one trust incident (D4, fabricated citations) live
only in the room tape. Common cause: rows posted outside the salon_runner receipt path
(chan threads, JIT spawns, monitor verdicts, night-shift results) have no fold discipline.

*— background orphan-mine gopher, 2026-09-04. Dumps + extraction scripts at
`C:\Users\foste\.zcode\cli\tmp_orphan_mine\deepseek\` (scratch, safe to delete).*
