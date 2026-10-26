# MOONSHOT-1: the estate named its gaps; here is who solved each one externally (2026-10-07)

Lens: moonshot. Order: the operator's descent protocol leg 1 (never relearn a known
lesson expensively). Every external claim below was fetched or read THIS SITTING
(2026-10-07, urls named inline); every estate claim is path:line or a dogfood2 lane
byte I read this sitting. Anything I could not verify is marked OWED. No em-dashes.

## THE MOONSHOT FRAME (which steal retires the most build days)

The estate is hand-rolling a POLICY DISTRIBUTION ENGINE and calling it a context
pack. OPA (Open Policy Agent, CNCF, Apache-2.0) shipped the whole contract years
ago: policy compiled into a versioned bundle (.manifest carries a revision string,
e.g. a git commit hash, per https://www.openpolicyagent.org/docs/latest/management-bundles),
activation is all-or-nothing, a failed verification "continues using its existing
bundle" and reports failure via the status API, and agents poll with ETag/304 so an
unchanged pack costs nothing. Stealing the CONTRACT (not the Java-style server)
retires TWO gap classes at once:

- GAP 6 (law-pack day-lag): the estate recompiles once daily (MagLawPackDaily
  9:30, d01 lane: "Last Run 10/6/2026 9:30:01 AM, Next Run 10/7/2026 9:30:00 AM")
  so a law written at 10:00 waits 23 hours. OPA's shape is event-driven publish
  with revision stamps and cheap polling; the estate already stamps revisions
  (compile_report.json restamped live this window, d07 lane: "report restamped
  2026-10-07T08:51:19.502719+00:00 (was 2026-10-06T18:26:38Z)").
- GAP 1 (memory propagation): the estate loses laws at RENDER time, the worst
  possible moment. The shed ladder at mag/context_pack.py:1486-1503 lists
  "L0d rib vault amendments" as a rung-3 shed candidate, and the d01 lane
  measured the loss live: "total_chars 9471, shed_sections ['L0d rib vault
  amendments'], stage 3" with MEASURED ON / Sybil / max_concurrency at 0 hits in
  the rendered pack. OPA never drops a policy at enforcement time; an oversized
  bundle fails at BUILD. "Fail at compile, never at render" is the one law that
  closes the class.

Honest tri-state on OPA: the CONTRACT is byte-verified and maps (solves our
shape as a pattern); the PRODUCT is not adoptable as-is for a solo Windows
estate (a policy server with bundle signing is overkill), and the delta-bundle
feature is data-only ("Delta bundles currently support updates to data only and
not policies", same docs page), so it does NOT solve law deltas directly. ADAPT.

## PER-GAP EXTERNAL CANDIDATES (byte-verified this sitting)

### GAP 1: MEMORY PROPAGATION (laws shed at stage 3)

- LLMLingua-2 (microsoft/LLMLingua, MIT, pip install llmlingua):
  "trained via data distillation from GPT-4 for token classification with a
  BERT-level encoder", 3x-6x faster than LLMLingua-1, supports force_tokens and
  structured compression (https://github.com/microsoft/LLMLingua). It compresses
  a block to FIT a budget instead of dropping the block. Tri-state: partial, it
  guarantees a compression ratio, not that the three named law tokens survive;
  the estate's shape needs a PINNED sub-block (law heads + amendment mechanism
  bytes) that never sheds, with LLMLingua-2 compressing the remainder. ADAPT.
- Letta/Mem0 tiering: the estate's own steal map
  (watch/inbox/ONE_COMPUTER_MESH_STEAL_MAP_20261007.md:56-60) already
  tri-stated them: "they retrieve, the lance plants", memlance's aimed
  injection is a shape none center. CONVERGENT, do not build a retrieval MCP
  server to fix a rendering bug. WATCH.
- The estate organ that must change: mag/context_pack.py:165 sets the full
  budget at 7200; mag/context_pack.py:1279-1284 (R4-L2 comment) deliberately
  made the vault block sheddable ("The block sheds only ahead of L1 bonds"),
  which reads correct in isolation and is the bug in composition: the pack is
  chronically over budget, so the block sheds essentially always (d01 measured
  it twice on two days, "reproduces byte-for-byte on today's tree").
- One-sitting probe (45 min): budget-gate the compile. In
  tools/thought_quantizer.py compile (the one sanctioned writer, d07 lane),
  compute the would-be L0d carrier size and exit 1 when the pinned law set
  exceeds 7200, then compress the carrier prose with llmlingua-2 (rate 0.5)
  until the pinned set fits. Acceptance: a fresh mag.cmd context-pack greps
  MEASURED ON non-zero in memory/context_pack_latest.md, and the red test
  test_quantized_laws_section_renders_in_default_budget (d01: "1 failed,
  41 passed in 10.76s") goes green.

### GAP 2: MULTI-SEAT TREE CONTENTION (sibling stash swept the tree mid-landing)

- git worktree (built into git, docs https://git-scm.com/docs/git-worktree):
  "Manage multiple working trees attached to the same repository"; each linked
  worktree has its own HEAD and index, shares the object database and
  refs/heads/, and a branch "cannot be checked out in two worktrees at once".
  A stash pushed in one worktree cannot capture another worktree's files
  because they are separate working trees. Tri-state: solves the git-level
  sweep shape outright; partial for the estate because many organs bind to the
  single repo root (tools/stash_sweep_watch.py:26 ROOT =
  Path(__file__).resolve().parents[1] and every watch/inbox/ + memory/ write
  assumes one tree). STEAL, one seat per sitting.
- The detector (tools/stash_sweep_watch.py, born from the R3/R5 incident per
  its docstring, "The tool has NO drop or pop verb by design") stays as the
  tripwire; its open residual is cadence (d02 lane: "no patrol cadence runs
  check mode... caught only at the next manual run").
- flock/OT/CRDT/Figma-style shared edit: wrong altitude for a git estate; the
  CRDT answer belongs to LEDGERS not the working tree, and the estate already
  spiked exactly that (steal map P2: cr-sqlite on a copy of gps_ledger.db3,
  "kills the stash-sweep class for ledgers"). WATCH for trees, STEAL the
  cr-sqlite spike for ledgers (convergent, steal map lines 47-52).
- One-sitting probe (30 min): git worktree add ..\lsa_worktree_probe -b
  seat/worktree-probe, run tools/stash_sweep_watch.py + freshness gate inside
  it, file whether estate organs bind per-tree; green means sibling seats
  migrate to linked worktrees and the sweep class dies structurally.

### GAP 3: JUDGMENT-TIER BLINDNESS (402s read as PASS)

- The estate cure already landed: tools/hermes_burn.py:34-41 "TERMINAL IS
  TERMINAL" with the receipt "watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md:
  The 10-06 23:54Z .. 10-07 08:00Z provider 402 wall fired MagHermesBurn247
  hourly ~8 times", plus tools/cost_rollup.py:305-335 spend_balance.v1
  ("landed 2026-10-07" per its own docstring).
- LiteLLM budgets (docs verified at https://docs.litellm.ai/docs/proxy/customers):
  budget objects carry max_budget, soft_budget, budget_duration, tpm_limit,
  rpm_limit; GET /customer/info returns live "spend"; alerting webhook pushes a
  "spend_tracked" event with projected_spend; budget objects cache 60s. The
  budget-exceeded HTTP status is NOT stated on the page I fetched (OWED, do not
  assert). Tri-state: the estate does not run a LiteLLM proxy, but the CONTRACT
  (spend is a queryable first-class object with propagation delay and a push
  event) is exactly the class fix. ADAPT.
- Herald OS independently embodies the same signal: usage tracking "shows what
  Hermes used this week and this month with a warning at 90% of your plan"
  (https://github.com/iamlukethedev/Herald-OS README, fetched this sitting).
- One-sitting probe (30 min): give every batch runner one contract line: read
  memory/runs/spend_balance.json before the batch and emit a TERMINAL-class
  marker when the armory is below the batch's projected floor; acceptance = a
  dry run with an artificially low pot prints the marker and exits nonzero.

### GAP 4: SCHEDULED-DRAIN 429 STORMS (20432/20578 rows 429-fail, dark 11 days)

- Note on evidence: the storm numbers ride the ask's authority; I could NOT
  find the 20432/20578 receipt in my greps of watch/inbox/, state/ and queue/
  this sitting (grep for "20578|20432" across those roots returned only
  unrelated olm sweep files). The nearest estate byte is
  watch/inbox/FULL_SCAN_REPORT_20260923.md, whose newest run line reads
  "run 2026-10-06T13:39:33 records: 315 ok: 221 fail: 94", a different, much
  smaller surface. The storm receipt is OWED to whoever files the disable.
- Healthchecks.io (https://healthchecks.io/docs/, fetched this sitting): dead
  man's switch, "raises an alert as soon as a ping does not arrive on time",
  and the ping URL accepts /start, /fail and /<exitcode>; a start without a
  success inside grace alerts. The honest nuance: a BARE dead man's switch
  would NOT have caught the storm (the task exited clean while yielding zero
  ok rows for 11 days). The steal is the /fail vocabulary with an ASSERT:
  ping /fail when ok_rows == 0 and total_rows > threshold. Tri-state: partial
  product (external SaaS, estate runs local), exact shape. ADAPT.
- Circuit-breaker schedulers (Temporal retry policies, resilience4j, Polly):
  same state machine, heavier substrate. WATCH; the estate needs 5 lines in
  the wrapper, not a workflow engine.
- One-sitting probe (30 min): in the scan/drain wrapper, after each batch:
  if ok_rows == 0 and total_rows > 100, append one RED line to
  memory/attention.md (the alarm surface stash_sweep_watch already uses,
  tools/stash_sweep_watch.py docstring) and exit 1 so schtasks Last Result
  goes nonzero (the surface the d01 lane already reads via
  "schtasks /Query /TN MagLawPackDaily /V").

### GAP 5: FOLD-PHASE SERIALIZATION (mutex queues folds by design)

- The estate cure is already a micro durable-runtime: FOLD_FAST_20261007.md
  (mutex stays by design, "the hang-prone half is the CLOUD FOLDER ASK",
  local qwen2.5:7b route with "Model failure = exit 3 = engine falls back to
  the cloud folder", verification never downgrades).
- DBOS Transact (https://github.com/dbos-inc/dbos-transact-py, MIT, ~1.6k
  stars): "lightweight durable workflows built on top of Postgres",
  @DBOS.step/@DBOS.workflow, and on failure "all your workflows will
  automatically resume from the last completed step". Requires Postgres; the
  estate core is SQLite and jsonl. Temporal: a server plus database,
  heavyweight for a solo estate. Tri-state: solves the resume-on-crash class
  the estate does NOT have yet (the mutex + local fallback cures duration and
  saturation, not mid-fold checkpointing); the substrate cost is real.
  WATCH; steal only the step-journal pattern (an idempotent step writes its
  result before the next starts, resume reads the journal), which the estate's
  FOLD_SECTIONS.md + fold_history already half-are.
- Verdict on "reinventing badly or well": WELL. The mutex is a deliberate
  collision cure (FOLD_FAST lines 4-8 cite the 10-05 collision), and the
  honest gap is queue-depth visibility, not orchestration. Do not adopt
  Temporal/DBOS/Airflow for this.

### GAP 6: LAW-PACK DAY-LAG (new laws wait ~a day for the flash pack)

- Covered by the moonshot frame above: OPA's event-driven publish with
  revision + ETag polling is the pattern; the estate's cure is to make the
  compile event-driven (law-write path or a 15-min hash-check task modeled on
  tools/thought_quantizer.py --check, which d07 verified "reads the packs
  fresh at 0.0d") instead of the 9:30 daily fire. OTA-for-models and
  GitOps (Argo/Flux) are the same shape at wrong scales. ADAPT.

### GAP 7: THE ASKS

- GSTD node ops: the prior art is ALREADY IN THE ESTATE: the gstdbot clone
  (reference/gstdcoin/gstdbot, remote github.com/gstdcoin/gstdbot.git, tip
  e0bbe48 per watch/inbox/GSTD_NODE_CENSUS_20261007.md:11-17) ships a Docker
  compose with memory 536870912, a healthcheck "curl -sf
  http://localhost:8080/health" interval 30s, and a gstd-data volume
  (same receipt lines 26-47, docker compose config verified exit 0). The live
  census names the shape's proof: 4 nodes registered, ONE earner (the Pi,
  llama3.2:3b, 272 tasks, 47.39 gstd earned, last seen 2026-10-07T12:33:47Z,
  lines 57-75). Tri-state: the swarm itself is the byte-verified mechanism
  for "desktop full-node + node-lite fleet"; TON-specific full-node hardening
  is unverified here (OWED). STEAL: the compose shape verbatim for the
  desktop node.
- Herald OS (https://github.com/iamlukethedev/Herald-OS, MIT, alpha 0.1, 62
  commits, 35 stars, fetched this sitting): CORRECTION to the estate receipt
  watch/inbox/HERALD_OS_20261007.md. Its four tiers are PERMISSION tiers, not
  token tiers: "read tools (system info, file search) and act tools (opening
  an app) run straight away and are logged. mutate tools (create, move,
  rename) ask first, and you can allow them for the session or always.
  destructive tools (stopping a process, moving files to the Trash) ask every
  time", with sensitive paths "such as ~/.ssh, your keychains and Hermes's own
  credentials" always refused, and an audit log at
  ~/.hermes/herald-os/audit.jsonl. The estate
  receipt's S1 row ("read the repo's approval-gate + token-tier
  implementation") and its OWED license-confirm row are now substantially
  verified by this sitting's fetch; what remains OWED is reading the actual
  gate source (the README description is the author's own). STEAL the
  permission-tier ladder + audit.jsonl shape for the estate effect broker.
- Mesh lane dispatch: CONVERGENT with tonight's steal map
  (ONE_COMPUTER_MESH_STEAL_MAP_20261007.md:39-56) and measured by tonight's
  spike: exo (https://github.com/exo-explore/exo, Apache-2.0, 47.8k stars,
  libp2p auto-discovery, topology-aware partitioning) is macOS/Linux-first
  ("Linux currently runs on CPU"), so on this Windows 10 desktop it is
  WATCH; llama.cpp RPC is the measured door (RPC_SPLIT_SPIKE_20261007.md:
  "split 5.94 to 6.25 tok/s vs single 6.01 to 6.48, within noise" single-box,
  so the door opens only cross-machine, lines 63-75), and the bob-side
  one-liner is banked at lines 79-98. Nomad/k3s: named by the steal map as
  the scheduler tier, unverified deeper this sitting (OWED beyond the map's
  pointers). Ray: same class, not fetched.

## DO NOT BUILD (it exists)

1. Do not build a retrieval memory server to fix law propagation (Letta/Mem0
   retrieve; the bug is a render budget, and memlance's aimed injection is the
   differentiated shape the steal map already guards).
2. Do not build a policy server (OPA product) for one desktop; steal the
   revision + fail-closed + ETag contract into thought_quantizer compile.
3. Do not adopt Temporal/DBOS/Airflow to fix a mutex that is a deliberate
   collision cure; steal the step-journal pattern only.
4. Do not build a new multi-seat file-lock protocol; git worktree + the
   existing detector (as tripwire) + cr-sqlite for ledgers covers the class.
5. Do not expect exo GPU clustering on this Windows fleet; the measured door
   is llama.cpp RPC cross-machine (bob first).

## OWED (asserted nowhere, carried honestly)

- The 20432/20578 storm receipt bytes (not found this sitting; ask-borne).
- LiteLLM budget-exceeded HTTP status code (page did not state it).
- Herald-OS gate SOURCE (README claims fetched; source read still OWED per
  the estate receipt's S1).
- Whether a fresh llmlingua-2 compression actually keeps MEASURED ON/Sybil/
  max_concurrency tokens at rate 0.5 (probe would answer; no pip install run
  this sitting).
- TON/gstd full-node hardening specifics beyond the cloned compose.

## BLIND SPOTS

- I did not re-run the d01 greps myself; my "0 hits in the rendered pack"
  claims cite the d01 lane's instrument (memory/context_pack_latest.md render
  at 08:29:23Z), not a fresh grep of my own.
- I read tools/stash_sweep_watch.py head + targeted lines only (d02's full
  285-line read is second-hand).
- schtasks enumeration was unavailable in this sandbox (empty result), so the
  FullScan disable state is ask-borne.
- The Pixel/mobile body leg of mesh dispatch got no external pass this sitting.
- I did not measure what fraction of the 625-row pack the flash header
  actually carries (the 220-char FLASH_MAX_CHARS truncation, d01 row 4, is
  cited from the lane, verified only at tools/thought_quantizer.py:118 by the
  lane's pointer, not re-read by me).
