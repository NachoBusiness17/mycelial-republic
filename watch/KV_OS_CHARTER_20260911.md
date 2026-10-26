# KV-OS CHARTER (2026-09-11, lane: zcode, operator: "We're making a kv os please help")

**THE POINT:** The fleet ran production cache economics as a tenant — riding
providers' prefix caches at 91%+ hits. A KV OS is the move from tenant to
landlord: an operating system that treats KV cache as the scheduled, paged,
shared, priced resource. Five posts + one equation were mined for nuance; they
converge on five OS functions and one unfair advantage: our cache knows
tomorrow's wave.

## The mined nuance (per link — what each contributes to the OS)

1. **@techNmak — harness engineering → the OS acceptance test.** "Project state
   had moved outside the conversation" is the KV problem stated by a harness
   engineer. His five questions become the KV-OS acceptance test: does it make
   CACHE STATE discoverable, POLICIES enforceable, PROGRESS durable, RISK
   bounded, MISSES visible? His trap is our budget law: no ever-growing pile of
   compensations — prune as models improve (V4.1's 890 B/token shrinks what the
   OS must hold).
2. **@Voxyz_ai — Astra orchestrates a Luna+Sol agent tree; per-node effort
   levels priced by pass-rate/cost/steps.** The nuance is in the top reply's
   cost warning: subagents after Astra "cost a lot more" — because tree workers
   DON'T share prefixes. Same system prompt + same repo context re-encoded per
   node. The agent tree is the KV-OS killer app: siblings should share pages,
   and the orchestrator's effort-level choice is a scheduler policy.
3. **@FeitengLi — WaveNet at 10 years: fast autoregressive inference = "custom
   state management combined with gather," built before the name KV cache
   existed.** Lineage nuance: the OS doesn't invent, it systematizes a 2016
   discipline. Second nuance: he cut theoretically-unjustified pipeline stages
   and still won — inherited cache layers persist by inertia; audit them.
4. **@mdancho84 — PROBLEM → CONCEPT → BUILD IT → USE IT → SHIP IT.** Pedagogy
   law for the charter: every KV-OS component (block store, pager, policy,
   meter) gets a from-scratch build before any framework adoption. Also the
   audience map: this is who a KV-OS writeup teaches.
5. **@itsPaulAi — MiniCPM5-2B: agentic at 2GB RAM, #1 open sub-4B; Densing Law
   (capability density ~2x / 3.5 months); JustRL II scales small models to
   128k reasoning with a critic.** Pressure nuance: at the edge, KV cache IS
   the memory budget — on a 2GB device, context length is decided by cache
   management, not parameters. Densing Law pushes capable models onto small
   boxes; the OS is what lets them run long. The 2B model is our test rig.

## The Bellman organ (the pasted equation = the eviction policy)

v(cache-state) = max[ R(action) + γ · v(next-state) ]
- STATE: which prefix pages are resident, at which tier.
- ACTIONS: admit / evict / pin / demote.
- R (immediate): compute saved on a hit = tokens re-encded avoided × price.
- γ: discount by horizon remaining on the session/plan.
- Belady's algorithm (evict what's needed furthest in the future) is the
  Bellman-optimal caching policy under perfect foresight. Generic OSes can't
  know the future. WE CAN: the queue, the wave plan, the room schedule, the
  crons. **Plan-informed eviction is the novel organ** — a cache with a plan
  oracle. The DP grid in the image is the training pass: start from known
  future reuse (R=1 cells = the next wave's prefixes) and propagate value
  backward, 0.9 → 0.81 → 0.73.

## Five OS functions (the kernel map)

1. ADDRESSING — content-hash prefix blocks (chain-shaped, 40-byte-token style);
   Engram's hashed n-gram tables are the model-side twin.
2. PAGING — HBM → host RAM → SSD → remote tiers (LMCache shape = our fuel
   lanes); V4.1's SWA Bounded Replay = the readmission policy to copy.
3. SCHEDULING — wave cadence: schedule same-prefix work adjacently; the agent
   tree shares pages instead of re-encoding them.
4. POLICY — the Bellman organ above; trained on our own telemetry
   (logs/kpi.jsonl 457MB, burn board hourly, session patterns).
5. METERING — per-seat pools, the burn board as quota gauge, cache-hit
   accounting per lane (refeed_guard B1: 94% of input is re-fed reads —
   that number is the OS's revenue model).

## Honest gap (tri-state)

- SUPPORTED: the fleet pioneered cache-first ECONOMICS on provider caches
  (lane pinning, 91%+ hits, refeed measurement, $0 night at scale).
- DISPUTED→OWED: we did NOT build an OS layer; every cache we ever hit belonged
  to someone else's runtime. KV-OS closes that gap. 
- UNPROVEN: that plan-informed eviction beats generic policies on our own
  workload. FALSIFIER v2 (upgraded by FRONTIER_REVIEW_001 — the first external
  adversarial pass, adopted in full): replay ≥14 real nights, hash-chained;
  capacity arms as fractions of the working set C ∈ {0.15W, 0.30W, 0.50W} —
  at C ≥ W every policy ties and the test is void; six arms (LRU, LFU, ARC,
  Role/lifecycle, Plan-oracle = Belady MIN ceiling, Plan-noisy = the product);
  primary metric = prefill-joules avoided per night, NOT hit rate; lossless
  fixture check (a policy that evicts a pinned constitution block and changes
  one greedy token fails the arm). Stopping rules: Plan-noisy must beat LRU
  AND ARC by ≥15% relative prefill-joules at C=0.30W (bootstrap 95%) and stay
  lossless; if Plan-noisy loses to Role/lifecycle, the wave card is costume on
  a session-death cache — retire the Bellman story, keep lifecycle; if only
  Plan-oracle clears the bar, foresight we don't possess is doing the work —
  retire the product claim. Peeking at test nights or re-choosing C voids the
  run. WITNESS STAMPS adopted: every published metric ships as
  witness(claim_id, metric, C/W, head_drift, lane_histogram, n, stamp ∈
  {VALID, VACUOUS, UNDERPOWERED, PEEKED}); a morning report that cannot emit
  VACUOUS is not a report. Same-model duplication is determinism (n=1 with a
  mirror): validators must differ by weights hash.

## 🆕 GVA — the DERIVE action (appended 09-11, operator link, paper read)

Grouped Value Attention (FrontiersMind, 16pp; @akanyaani is first author Abhay
Kumar self-posting at 542 views — caught at whisper stage, paper read before
traction). Stores GROUPED VALUES only; content keys are reconstructed by a
learned linear map K = VM that **absorbs into the query at decode** — so the
hot path never materializes a key stream. A small shared decoupled-RoPE
positional key (16-24 dims/token, shared across heads) carries order.

**What it adds to the OS design:**
1. **Third POLICY action: DERIVE** — beside ADMIT and EVICT. Store a minimal
   sufficient statistic + a map; recompute the rest on demand at ~zero hot-path
   cost (the absorption trick). Storage-to-compute trade becomes an explicit,
   schedulable decision.
2. **Page table gains a FIDELITY column** — EXACT / QUANTIZED (FP4) /
   DERIVABLE (sketch+map). Eviction becomes a downgrade ladder
   (EXACT → FP4 → DERIVABLE → evict), not deletion. The Bellman organ's state
   space and action set both grow; reward unchanged (tokens not re-encoded),
   but re-encoding now has cheaper middle stops.
3. **Position/content split:** the positional stream is the un-compressible
   residue (must persist, shared); content keys compress toward derivation.
   The OS treats them as different page classes.
4. **Representation-agnostic page table:** a page is (bytes, fidelity,
   derive-cost, quality-risk). GQA, MLA, GVA, FP4-KV are page types, not
   architectures the OS cares about. That is how the OS survives architecture
   churn. (Note: at 350M scale MLA scored BELOW GQA — representation rankings
   flip with scale; another reason the OS must not hard-code one.)

**Tri-state:** SUPPORTED (paper, TOY SCALE): 45-47% scalar reduction vs GQA is
representation-level arithmetic (47% at d_r=16, 45% at d_r=24; idealized
value-only bound 50%), stated in Limitations as counts, NOT measured
serving-memory reductions; accuracy parity at 350M/30B tokens (GVA 44.35 vs
GQA 44.36, MLA 43.88). UNPROVEN: serving-memory and speed benefit (custom
kernels under evaluation), scaling past 350M, code (open-source "planned
soon"). Watch the release; bench on our rigs when it lands (P3 candidate).

## Build phases ($0 until hardware GO)

- P1 ADDRESSING PROOF — hash-chain prefix blocks over our real session
  transcripts; measure sharing entropy of the agent tree (how many tokens
  siblings re-encode). Deterministic, local, one night.
- P2 BELLMAN REPLAY SIM — replay telemetry against Belady / LRU / LFU /
  plan-oracle at fixed byte budgets; the falsifier above decides the build.
- P3 LIVE PAGER — behind operator GO (hardware/egress): ollama or vLLM+LMCache
  rig, MiniCPM5-2B at 2GB as the edge test, V4.1 Flash as the fleet brain when
  the API lands.
