# SALON BRIEF — SETUP: the per-lane agent architecture (2026-09-04)

Corpus brief for a full research salon. Compiled by the background gopher from the actual
docs (every section cites its source file; load-bearing lines quoted). Three parts: the
doctrine we intend to work by, the measured present, the operator's new thesis + open gates.

---

## PART A — HOW WE INTEND TO WORK (the doctrine)

### A1. AGENTS.md — seat identity, standing laws, current arc
Two files carry the name. The workspace boot memory (AGENTS.md at projects/) is seat
identity: "You are the zcode seat: the deep-work lane of a sovereign AI fleet" — "Depth
seat: forensics, architecture, verification, surgery... One builds, one verifies." Standing
laws live there as one-liners: SACRED COWS NOT LEGACY SHIT · tri-state claims
(Supported/Disputed/Unproven, evidence attached) · two-strike bail · consult before
reverse-engineering · "Route bulk work to the free lanes... premium tokens touch judgment
only." Current arc: this seat is "the permanent research/paste window — pastes land here,
rubric-scored, cards route to the driver," under the LAUNCH LAW: "windowed names the lane,
never a deferral." The repo-root AGENTS.md adds the harness contract: "All durable
cross-surface work lands on the shared inbox... session directory is cache only and must
never be the sole copy" — and "Model text can propose; only the switchboard/effect broker
authorizes effects."

### A2. OPERATOR_DRIVE.md — the doors + GO loop
The operator's cockpit file: "Your doors, your fleet's state, your GO menu. Derived from
today's receipts; the derived board is /chan." Doors are loopback URLs (/chan board,
hypervisor dashboard :8765, gateway room :8001 key-gated, OpenClaw webchat, Ractor board,
raw room tape watch/room.jsonl). The GO MENU is the drive loop: "word one and it fires" —
named one-line actions (ARM GUARD, VERIFY CLAUDE, RESTORE FREE_LANES, KILL VAST, REBUILD
ROOM.HTML). Doctrine: the operator drives by single words against a file he can read
anywhere; seats keep the doors verified-live and derive the board from receipts, never
from memory.

### A3. operator-corrections/SKILL.md — the 12 laws
Root cause of all failures: "act before consult, keep acting after done" — "One failure
wears five costumes." The laws (verbs, in order): CONSULT FIRST (the tool answers faster
than re-deriving) · TWO-STRIKE BAIL (fail twice → switch/consult/read, never a third
attempt) · STOP WHEN VERIFIED (against "the OPERATOR'S surface (not your own definition of
done)") · VERIFY AGAINST THEIR SURFACE ("'It works' is only true on the surface the
operator actually touches") · COMPOSE FIRST · NEVER CLAIM FIRST UNLESS READ FROM DATA ·
MEET AT THE BYTES NOT THE GLOSS · NO REPETITIVE NEGATIVE SELF-TALK (fix plainly, once) ·
RIGHTSIZE DON'T PATTERN-MATCH · NO SACRED COWS · ONE SUPERVISOR ONLY (never a second
host-side supervisor) · THE STANDARD BINDS BOTH WAYS: "The seats' duty is not obedience —
it is the standard, applied in both directions, receipts attached."

### A4. AUTONOMY_WHEEL_20260904.md — the 8 spokes + coupling law
"The pipeline is not a line — it is a WHEEL." Eight spokes: HARVEST (scout stack, nightly
zero-quota) → SCORE (intake genome, tri-state cards) → BUILD (BUILD NOWs spawn builders
same-session) → VERIFY (GAP: "the build's own word is never the receipt") → INTEGRATE
(GAP: "a build isn't done when filed; it's done when wired and its absence would be
noticed") → MEASURE (instrument exists, adoption missing) → REFIT ("THE
QUESTION-GENERATOR IS THE REFIT" — search sets regenerate from REFUTED claims and
starvation heads) → REMEMBER ("every spoke leaves typed rows; the chain is the proof
folder"). THE WHEEL LAW: "Autonomy means the wheel spins without the operator — EXCEPT the
two stops that stay his by design: KEYS (money, credentials, names) and VERDICTS
(irreversible, external, contested)." HARVEST-SPAWN COUPLING (operator-corrected, second
instance): "Harvest is NOT complete when the file is written. Harvest is complete when the
processor spawn is LIVE... Spoke 1 hands to spoke 2 by SPAWNING, never by 'queuing.'"

### A5. SYSTEMS_SALON_GAP_MAP_20260903.md — the four verbs
Thesis v3 (survived a different-mind attack that killed three predecessors): "The fleet is
not short of organs and not short of typing — it is short of COVERAGE." Measured: 887 .py
organs in mag/ with an empty organ queue; buses already ~100% typed where they exist
(383/383, 347/347) but room.jsonl is "9 typed rows in 5,325." The law: "An action that
emits no record is, to the fleet, an action that never happened." Every declared gap sorts
into FOUR VERBS: **WIRE** the half-wires (writer exists, no reader — e.g. steer receipts,
2 rows, zero consumers) · **TRANSDUCE** the ambiguous (record-makers that don't exist:
WAL-before-effect, retry-dedup, tale-re-encoder) · **DISPOSE** the built-but-unrun
(gate_v3 falsifier BUILT, never run) · **SUBSTRATE** the true waits — with the humility
clause: "Re-verify substrate verdicts before believing them" (the headless door fell to a
routing change the same night it was filed "blocked"). Kill-list convergence (four salons
independently concluding DON'T-build) is "the fleet's strongest measured signal."

### A6. STEERING_SYNTHESIS_20260901.md (head) — steering doctrine
Steering is cheap because the physics is already paid: "The Pro lane measures 99.6%
cache-hit on a warm frozen prefix at $0 marginal" — so a steer is a delta appended to a
frozen tail, never a re-render. The connector, not new organs: reuse room.jsonl as the
shared firehose (post-once, read-only) and steers.jsonl as the actionable queue
(claim-before-act, edit-before-read — the operator's law). Hint shape is compact-handoff:
{target_seat, where, why, ttl, anchor (verkle tip prefix), delta} — "A hint that points is
cheap; a hint that *attaches* a full doc is a bug." Dumb seats poll the queue and may
safely ignore hints anchored older than the tip they last saw (fork-safe).

### A7. HARNESS_SPEC.md (head) — the harness constitution
Seven articles, "as bare metal as possible so any game surface can interpret the same
data": 1) ONE stream — event.v1; "No seventh ledger, ever." 2) ONE committer — the
governor; "Surfaces never mint `kind`." 3) "Players write INTENT as signed events; the
governor writes STATE as reconciled mutations" — a surface writing state directly is a
fork, and "forks are reaped." 4) Surfaces are read-only interpreters; on conflict,
re-derive from canonical. 5) Contradictions resolve by hierarchy of invariants, not
consensus. 6) "Render free, steer paid" — no model calls in any render path. 7) "Fun is
the gate." Final form: "Players write intent. The governor writes state. Surfaces give
sight. The stream remembers. The covenant decides. Fun ships it."

### A8. INTAKE_RUBRIC_20260903.md (head) — the intake window rubric
This seat's standing order: "he pastes items HERE, we score them against the fleet and
hand the driver a verdict card, so the driving session is never bugged." Five axes, 0–5
each, 25 points: FIT (bolts onto existing organs) · PULL (advances live arcs) · COST
(pennies/free lanes, zero operator minutes) · WINDOW (feeds a starved lane tonight) ·
NOVELTY (new against memory index; re-finds scored as re-finds). Bands: 20–25 BUILD NOW /
14–19 BUILD WINDOWED / 8–13 CALIBRATE / 0–7 REMEMBER. Verdict = three verbs
(BUILD/CALIBRATE/REMEMBER) + tri-state label — "Tri-state labels survive our own fold or
the fold is a violation." Dogfood tests: INVARIANT PASS (47 percolated invariants, $0) and
STOCKFISH PASS (tool-lattice placement) always; BLIND POST / SOCRATIC GATE / ROOM TEST by
stakes. Routing law: "pointer only, never a push into his session."

---

## PART B — HOW WE CURRENTLY WORK (measured, today 09-04)

### B1. DAY_WORK_DIGEST.md — the scheduler is live (the poll organ)
"Every 30-min fire diffs the day-work surfaces, reads anything finished, and appends 'what
finished → what we answered'" — the operator's "when is anything done" surface, one file.
Fire 0: Lite verdict — one planning conversation burned 201M tok on GLM-5.3 (274 calls);
the whole 20h window: 5.3 = 205.5M/338 calls, 5.3-flash = 471.1M/2,789, 4.7-flash = 1.9M;
"Lite key keeps the BULK lanes... Max drives judgment." Fire 1 answered 8 finishes:
direction salon (CAS GO), AX-vs-pixel falsifier (47/47 vs Δy 1009px), z.ai steal (22/25,
POLL-NOT-PUSH enacted — "this scheduler IS the poll organ"), sweeps retired at shift 4,
17 intake cards batch-verified ("41 cards read at the bytes, nothing invented").

### B2. SALON_DAY_DIRECTION_20260904.md — today's direction
4/4 independent witnesses (groq, cerebras, together, deepseek-pro; 2 honest-down) put CAS
fix first: "It is not scheduled. That is a governance failure, not a technical one."
(deepseek-pro) — LAUNCHED same turn, one-builds-one-verifies. Binding constraint: FOOD not
lanes — night sweeps 5–7 "returned already-held material: 'the fleet's arcs have outrun
the public discourse.'" The blind spot (deepest read): "the difference between a law that
is written and a law that is enforced" — lattice_logic measured 8/8 law-registry
conditions as prose, zero firable. Direction ordered: 1 CAS fix → 2 output-ratio meter as
enforcement (tick kill now triple-stamped: meter + economist + salon) → 3 window throttle
organ ("night windows are triple-booked... One primary per window, claimed by file") → 4
falsifier workbench (WINDOWED) → 5 sweep retirement.

### B3. DAY_CLOSE_20260904.md — the day card
Phone-read, one screen. Verdict: "Lite can't drive the seat... about half your hourly Lite
compute. Max drives judgment; the Lite key keeps the bulk lanes." Built and live today,
all tested: the 30-min scheduler; DAY TOOL on the Android emulator ("Verified on glass,
not a blank 200"); lattice_logic ("47 invariants, 8 laws, 29 shadertoy rules — first
parser ever — 161 knots"); the embodied falsifier (AutoGLM missed a tap by 1,009 px; the
accessibility tree "walked the full 70-step ladder to 47/47. Law: AX-resolve over
pixel-guess"). The z.ai self-steal in one line: "they sell organs, never chains — zero
webhooks in all 86 doc pages — so our scheduler IS the missing chain organ, and their
phone-brain runs OUR harness." Waiting on the operator: tick kill · B2 eyes · omen $10 ·
Max #2.

### B4. USAGE_METER_SELF_STEAL_20260904.md (head) — the zombie heartbeat + 5 laws
First fleet doc to read `~/.zcode/cli/db/db.sqlite`. "The seat burned 2.84B tokens in 10
days; the single biggest burner was a zombie heartbeat" — tick e2c00e27 fired 939 times
into a session pinned to paid 5.3-full; "1,296 of 2,609 premium turns output <200 tokens
('nothing to do, exiting') and still re-fed ~95K context each: 740M tokens of no-op";
useful output = 11 posts, all Aug 27–28; useful-output ratio ≈ 7e-7 (kill line 1e-2). The
five laws: OUTPUT-RATIO (retire when useful÷billed < 0.01 per 24h rolling) · MODEL-PIN
ISOLATION (subagents never inherit premium pins) · CONTEXT-DEBT (compaction + re-feed ≤ 3×
peak useful output) · HEARTBEAT-THROTTLE ("'exit fast' is not free when context re-feed
dominates") · MODEL-PIN EXPIRY (premium pin >72h without a completed task ⇒ demote). "The
deep law: no surface ever compared BURN to OUTPUT. The meter existed per-turn on disk the
whole time; nothing queried it."

### B5. ECONOMIST_AUDIT_20260904.md (head) — economy verdicts
Mandate: "prove by Sep 20 the fleet burns two Max plans usefully." The march: 657/657
signals, 0 errors, ~$0.09 out-of-window, $0.00 in-window — "~$0.00014 per signal... the
whole 228-signal explore backlog = one coffee — food, not compute, is the binding
constraint." Burns: 2 (backlog) + 4 (verifier) + 5 (canon) UNLOCKED NOW; 3 (shadertoy KG)
"PARTIALLY STARVED on data, not tokens" (Shadertoy 403 wall); 6 (gamebuild) horse-gated.
CAS fix: "cost of fix ≈ one seat-afternoon, $0 cash" vs "every grace-expiry under hungry
engines double-mines" — "the cheapest lever on the board... GO, this week." Utilization:
"~12% of weekly credits (17K/140K)"; Max key #2 "STARVED by the ledger's own law." At 10x,
in order: FOOD breaks first, then the claim organ, then host orchestration ("one Windows
box herding 50 lanes... sustained-hours unproven").

### B6. mag/seat_dispatch.py (head) — how seats get tasked today
"One command tasks any seat," two shapes. HEADLESS (openclaw, opencode): "spawn the
verified command, capture output, finalize_external(done), fold the result with a tri-state
claim. Fully autonomous — no paste, no ping, the result just lands on the chain."
MAILBOX (zcode, autoclaw-desktop): "GUI-only, so the task lands in their INBOX (the zcode
bridge pattern); the operator asks them to work it." CLI: `task "goal" --seat X` / `route
"intent"` / `status`. Honesty guard: openclaw's NO_REPLY sentinel "lets the gate score it
Disputed instead of a phantom pass." Note the asymmetry — the manager seat today is tasked
by INBOX drop, not driven remotely.

### B7. The X-surface precedent — how the operator BROWSES surfaces
The operator's pro surface is a deck fleet: 8 X Pro decks (Legions, Rocinante, Mesh3D, GLM
Watch, Cache Econ, GameBuild, MAG, Personal), each deck TWO adjacent columns — RAW then
FILLED (min_faves-filtered) — because "the filter alone deletes exactly the breaking
signal you want"; the valve lives in FILLED only, RAW never valved. He drives by GESTURE,
not command: bookmark = feed me, like = noise, paste into the window = full 72-step
treatment; the GO MENU is "word one and it fires." The pattern's law: surfaces are
pre-tuned by the fleet (deck setup card = paste-and-click), then BROWSED by the operator
while agents harvest underneath — "the harvester narrates each deck on rotation → monitor
flags/harvests/steers → intake scores → driver drives. The decks feed live; the wheel
drinks." Automation boundary, receipted: X's option-list click defeated the automation
budget (two-strike bail) — setup is a manual card, browsing stays human-paced.

---

## PART C — THE NEW THESIS + WHAT'S OPEN

### The operator's words (verbatim, today)
> "i just gave you a shitload of mcp servers. i think that's the key i can smell it. now i
> have each lane built. Each one needs its own agent and logic/automations you control/set
> remotely you are the manager of all of them you browse them like we did the x surface of
> pro. it's the same thing."

### The operator's lane board (his ZCode sidebar, TODAY, verbatim)
Day Work · Builder · Bard/Ledger · Elder · Research · Android Surface · Economist ·
Scheduled tasks: Day-work scheduler (30-min) [firing now]

### The MCP surface this seat currently holds (verbatim)
mag (run_python/run_shell/vision/blackboard/research swarm + pheromone) · computer-use
(desktop GUI control, a11y-first) · android-emulator (23 tools:
build/install/screenshot/UI-describe/tap) · browser-use (web-gui-tester + control) ·
node_repl (browser kernel) · web_reader · cloudbase (37 tools, Tencent cloud) ·
image_search · mimosa (security scan) · 4_5v vision · video-agent-kit · github skills ·
document-skills

### Open gates
- tick kill e2c00e27 — operator-gated (evidence triple-stamped: meter + economist + salon)
- B2 eyes — KEY-gated (operator's key)
- window throttle organ — salon direction #3, unbuilt (night windows triple-booked)
- output-ratio meter — salon direction #2, unbuilt (the nightly usage-db sweep organ)
- falsifier workbench — WINDOWED behind CAS fix + window throttle
- claim FINDING 2 — corrupt claims unsweepable (CAS fix's sibling finding)
- field_smith.json — pending

### Today's enforced laws relevant to this setup
POLL-NOT-PUSH · AX-RESOLVE OVER PIXEL-GUESS · NORMALIZE AT THE BOUNDARY · ONE CANONICAL
MIRROR SHAPE · OUTPUT-RATIO · MODEL-PIN ISOLATION · CONTEXT-DEBT · HEARTBEAT-THROTTLE

---

THE RESEARCH QUESTION: design the per-lane agent architecture — each lane (Day Work,
Builder, Bard/Ledger, Elder, Research, Android Surface, Economist) gets its own agent +
logic + automations, wired through MCP servers, remotely managed and browsed by the zcode
seat as manager (the X-deck pattern applied to our own lanes). What is the minimal correct
architecture, what breaks first, which lanes light up first, and what does the manager
surface look like?
