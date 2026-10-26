# INTAKE — STRACE / Execution Dependency Graphs (Microsoft, arXiv 2607.07702)

SOURCE — @marfinxx tweet 2095845582912782360 (2026-09-04, 3 photos = paper page 1,
quote = his own X article). Content-creator summary of a REAL paper:
"From Noisy Traces to Root Causes: Structural Trajectory Analysis and Causal
Extraction for Agent Optimization" (MSR + UCAS, code: github.com/noomnight/STRACE).
Claim: feeding raw agent execution traces into an optimizer LLM = low-SNR noise ->
hallucinated fixes. STRACE compiles execution spans into a causal dependency graph,
slices the failure subgraph, repairs the one guilty module. VeruSAGE-Bench 42.5%->58.5%,
turns 14.8->8.2, optimizer token burn -68%.

SCORE — FIT:4 PULL:3 COST:5 WINDOW:3 NOVELTY:4 = 19/25 (BUILD, WINDOWED)
- FIT 4: pure composition — EDG = a falsifier pattern over traces we already emit
  (chain rows, swarm runs, MAX_DISTILL epochs). No new vendor; code repo exists.
- PULL 3: feeds falsifier workbench + mining arc (failure-pattern mining = accumulator
  feedstock) + 20-lab sweep; doesn't unblock Rocinante/shadow-fields critical path.
- COST 5: free lanes read the paper + steal the parser; $0 operator.
- WINDOW 3: falsifier workbench is live and starved for structure; EDG slicing is its
  missing diagnosis step.
- NOVELTY 4: new paper (Jul 2026), not on the watch shelf; index sweep skipped (time-box).

VERDICT — BUILD (windowed, lane: falsifier workbench / trace mining) + tri-state:
- Supported: EDG causal slicing beats full-dump and sliding-window on VeruSAGE-Bench
  (paper + code receipt).
- Unproven: the tweet's OWN "our trace engineering harness, 135 runs, 42.5%->61.8%"
  — author's claim, zero artifact. Note tweet number-drift vs paper page 1
  (engagement inflation, dose accordingly).
- Wall-blocked: replies/community notes not mined (fxtwitter exposes none; Amendment 2
  owed a re-pass if operator re-delivers = emphasis).

DOGFOOD — invariant pass: composes with tri-state + receipts law (a falsifier IS a
causal slice); stockfish pass: opcode = diagnosis-before-optimization on the tool
lattice, sits beside microsoft/Trace (related, distinct). Room test: the dragon is
"100k-token trajectory dumps"; the mechanic is slice-the-graph, don't re-read the log.

LAUNCH WIRE (Amendment 5) — builder-ready, one paste to the driver:
"Spawn tree: steal STRACE EDG (arXiv 2607.07702, github.com/noomnight/STRACE) into the
falsifier workbench — parse local_sovereign_agent run/trace JSONL into an execution
dependency graph, emit the minimal causal slice per failure. Free lanes. Under 3 min
time-box, partial fine."

FILED — watch/INTAKE_STRACE_EDG_20260904.md + room.jsonl thread "intake"
