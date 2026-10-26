# EXTERNAL STEAL: the economics lens (2026-10-07, ractor_engine)

Lens: EV-per-cost pricer. Question: for each gap the estate named in the last
48h, who solved it externally, what is worth stealing, and what should the
estate NOT build because it exists. Every estate claim below was re-checked
this sitting; every external claim is marked byte-verified (fetched this
sitting) or OWED (not verified, never asserted).

## Instrument run this sitting

- `mag.cmd context-pack` (mode full) re-rendered memory/context_pack_latest.md
  at 2026-10-07T12:39:53Z (7277 bytes on disk); `grep -c "MEASURED ON"` reads 0.
  The memory-propagation gap reproduces on my own instrument: the pack still
  carries zero R4b/R5 mechanism bytes at the 7200-char budget
  (mag/context_pack.py:165). Matches lane d01
  (memory/runs/mickey17_v2/runs/dogfood2-20261007/lanes/d01-seat-boot-pack.json,
  "total_chars": 9471, shed L0d at stage 3, my own 08:29:23Z run).
- `Get-ScheduledTask` census: Estate FullScan Disabled; Ready with no health
  signal: Estate Cooker, Gopher, KeyAudit, Librarian, Ratchet, Spine Index,
  StealthSweep, EstateWalkDaily, mag-docker-watchdog, MagBootRegenDaily.
  Last Result 0 on schtasks means "exited", never "worked".
- `git worktree list`: the estate ALREADY runs worktrees
  (lsa_reboot_staging, worktrees/salon-arena-mvp) and still holds 3+ live
  stashes on the shared main checkout (stash@{0} is the GSD join stash).
- FullScan census read at queue/todo.md:233-234: 20,578 rows 09-24 to 10-06,
  ZERO ok:true, 20,432 "[429]" fails, kill-or-repair decision owed.

## Per-gap external candidates and verdicts

### Gap 1: memory propagation (laws shed at the context-pack render)

- LLMLingua (github.com/microsoft/LLMLingua, MIT, fetched this sitting):
  perplexity-based token compression by a small LM, up to 20x claimed, plus a
  STRUCTURED mode where sections marked with `<llmlingua>` tags get
  per-section rates or `compress=False` explicit keep. Tri-state: PARTIAL, it
  solves "critical content survives a fixed budget" generically, but it prices
  importance by perplexity unless you hand it tags. Economics: pulling torch
  plus a small LM to shed 2,271 chars from a 9,471-char pack is negative EV
  when the estate fix is two named constants (FLASH_MAX_CHARS = 220 at
  tools/thought_quantizer.py:118 per lane d01; the stage-3 shed order around
  mag/context_pack.py:1287-1328 where L0d carriers append to policy_ctx).
  Verdict: ADAPT the frame (must-keep tags, per-section budget), WATCH the lib.
- Mem0 / Letta / Zep tiering: named by watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md:56-60
  but NOT fetched this sitting. OWED: mechanism and license unverified. They
  retrieve; the estate's problem is render-priority inside one 7K-char pack, a
  smaller problem than a memory service.
- Probe (one sitting, ~30 min): reorder L0d vault-amendment carriers ahead of
  sheddable sections in mag/context_pack.py and re-run
  `mag.cmd context-pack`; acceptance = MEASURED ON greps non-zero in
  memory/context_pack_latest.md (lane d01's own acceptance gate, currently red
  at 1 failed / 41 passed). Cheapest unblock of the estate's standing queue
  top item.

### Gap 2: multi-seat tree contention (R3 stash sweep)

- git worktrees: built into git since 2.5, $0, and the estate already
  demonstrates the mechanics on two trees. The R3 incident and tonight's
  detector (tools/stash_sweep_watch.py, 284 lines) live on the shared main
  checkout while two worktrees sit idle elsewhere. Tri-state: SOLVES OUR SHAPE
  (one seat one tree) with zero new software. flock/CRDT schools attack ledgers,
  not working trees. Verdict: STEAL (from git itself, not a vendor).
- Probe (one sitting, ~45 min): `git worktree add ../lsa-lane-<slug>` for ONE
  sibling lane, rerun that lane green against the new root. Adopt only if
  lane-relative paths survive; else keep the detector and stash-disposition
  protocol as the honest cure.

### Gap 3: judgment-tier blindness (402 read as PASS)

- LiteLLM proxy (README fetched this sitting): "virtual keys, spend tracking,
  guardrails, load balancing" gateway with "multi-tenant cost tracking and
  spend management per project/user". Exact over-budget error semantics: OWED
  (docs page 404'd, README silent). Helicone, OpenRouter limits: not fetched,
  OWED. Tri-state: MARKETING at estate scale, a gateway process to watch
  ~$180-220/mo across three providers is cluster-class overkill when the cure
  already landed: spend_balance.v1, tools/cost_rollup.py:305-338, writes
  memory/runs/spend_balance.json (pot, armed, spent per ledger) on every
  completed run, landed 2026-10-07. Verdict: WATCH; revisit only if the estate
  centralizes multi-provider dispatch behind one door.

### Gap 4: scheduled-drain 429 storms (the 10x frame)

- Healthchecks (github.com/healthchecks/healthchecks, BSD 3-clause, fetched
  this sitting): dead-man's switch, "listens for HTTP requests and email
  messages ('pings') from your cron jobs and scheduled tasks ('checks'). When
  a ping does not arrive on time, Healthchecks sends out alerts"; per-check
  cron-expression schedule + grace period; 25+ integrations; self-hostable in
  Docker. Tri-state: SOLVES OUR SHAPE, the exact "nothing noticed for 11 days"
  failure mode, generalized to all 11 Ready estate tasks. The estate
  re-derives per-task health by hand at least three times
  (tools/corpus_fts_rebuild.py --check, tools/census_drift_patrol.py,
  tools/stash_sweep_watch.py); wholesale steal writes the class cure once.
  Verdict: STEAL. THE MOONSHOT: this is the gap class whose wholesale
  retirement buys back the most build days, because silent death is
  estate-wide, not FullScan-local.
- Probe (one sitting, ~60 min): run the healthchecks container, register three
  checks (MagLawPackDaily, MagFtsIndexDaily, Estate FullScan post-repair),
  append one ping line to each .ps1 payload, and route alerts to a surface an
  agent seat reads (memory/attention.md append via a watcher), not only email
  an asleep operator.

### Gap 5: fold-phase serialization

- Temporal / Airflow / Prefect: not fetched this sitting (OWED as to current
  release state; mechanisms are long-documented). Economics verdict without
  the fetch: the estate's mutex is the 10-05 collision cure BY DESIGN, queue
  depth is 4 concurrent runs, and FOLD_FAST (watch/inbox/FOLD_FAST_20261007.md,
  live proof this sitting: local qwen2.5:7b folds the prose at $0 under an
  enforced number rule, funded verifier kept, engine amendment gate PASS) already
  collapsed the latency the cheap way. A workflow server is a new longrunner to
  patrol plus migration of ~20 saved workflows to retire minutes of queueing.
  Verdict: WATCH, revisit at 10x concurrency or when a fold must survive a
  reboot mid-flight. The estate is reinventing durable workflows WELL at its
  scale.

### Gap 6: law-pack day-lag

- MagLawPackDaily is healthy (lane d01 quote: "Ready","Last Result 0",
  schtasks /Query). The lag is cadence-by-schedule, not breakage. External
  pattern: push-on-change (CI-on-commit) versus poll-on-schedule; no external
  product is worth importing for a bespoke law pipeline. Verdict: internal fix,
  ~30 min: post-commit hook invoking the quantizer compile. Note gap 4's steal
  also covers this gap's failure mode (a silently stale compile now alerts).

### Gap 7: the asks

- Herald OS (github.com/iamlukethedev/Herald-OS, fetched this sitting):
  README-verified MIT, alpha 0.1, four-tier permission gate (read/act tools run
  immediately but logged; mutate tools ask first with session/always grants;
  destructive tools ask every time; protected paths always refused), audit log
  at ~/.hermes/herald-os/audit.jsonl, rides a standard Hermes Agent install as
  the herald-os-bridge plugin, Linux Fedora ISO + macOS Apple Silicon. This
  converts watch/inbox/HERALD_OS_20261007.md S1's claims from marketing to
  bytes at the README level (source still uncloned, OWED). Verdict: ADAPT, it
  is prior art for the estate effect broker, not a dependency. Probe (~60 min):
  read the herald-os-bridge tier table and diff it against the mag effect
  broker's gate classes.
- GSTD node ops: estate bytes show staging is real and waiting on one input
  (stash@{0}: "gstdbot image pulled, compose ready, MCP already in the node
  DNA; ONE input owed: GSTD_WALLET_ADDRESS"). External prior art (TON full
  node in Docker): NOT verified this sitting, OWED, priced below the five
  findings by EV; the wallet paste is the true blocker and is operator-gated,
  so no probe belongs to this lens tonight.
- Mesh lane dispatch: already mined well this window
  (ONE_COMPUTER_MESH_STEAL_MAP_20261007.md + GPU_LADDER_20261007.md, which
  byte-kills exo on Windows/AMD via issue 434 and substitutes llama.cpp RPC).
  Convergent, no new spend from this lens.

## NOT-BUILD list (exists externally or already estate-side)

- Do not build a prompt-compression model to save the pack: reorder the
  existing renderer first; LLMLingua is the fallback, not the first spend.
- Do not build a cost gateway: spend_balance.v1 landed; a proxy server is a
  bigger system than the spend it watches.
- Do not build per-task health heuristics one more time: healthchecks writes
  the class cure once; the estate's three hand-rolled checkers stay as
  deep-checks, not as the alarm layer.
- Do not adopt a durable-execution server at 4-run concurrency.
- Do not stage a Herald node: alpha 0.1, repo source uncloned; the gate table
  is the steal, the OS is a watch.

## Blunt ranking (EV per one sitting)

1. Healthchecks dead-man switch estate-wide (gap 4 class) ~60 min, retires the
   silent-death class on 11 tasks.
2. L0d render-priority fix (gap 1) ~30 min, unblocks every fresh seat's law
   inhalation, closes a red acceptance test.
3. Worktree-per-lane (gap 2) ~45 min, prevention beats the 284-line detector.
4. Herald gate-table read (gap 7) ~60 min, effect-broker prior art.
5. Nothing on gaps 3/5/6 needs external spend this week.
