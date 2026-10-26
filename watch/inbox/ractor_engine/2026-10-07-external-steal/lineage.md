# LINEAGE LENS: external-steal census over the named gap inventory (2026-10-07)

Lens: lineage (the estate's own forgotten ideas + who solved each gap externally).
Method: estate bytes read this sitting (state/CURRENT.md, state/NIGHT_LOOP_20261005.md,
watch/inbox/{HERALD_OS_20261007,FOLD_FAST_20261007,RUN_CLOSEOUT_20261007,LONGRUNNER_LAW_20261007,GSTD_NODE_CENSUS_20261007}.md,
memory/runs/mickey17_v2/runs/dogfood2-20261007/lanes/d01-seat-boot-pack.json,
dogfood2 lanes d02-stash-seam.checks.json, tools/cost_rollup.py, mag/context_pack.py shed ladder,
tools/thought_quantizer.py), plus live checks I ran myself (listed inline), plus external
byte-verification by fetching the primary repos/docs on 2026-10-07. Every universal claim
names its instrument and scope. No em-dashes.

## Live checks I personally ran this sitting

1. `git stash list` = exactly 3 stashes (stash@{0} WIP on ebcd2583d GSD ORIGIN STORY /
   gstdbot image pulled; stash@{1} WIP on 23d76bb71 OUROBOROS R1; stash@{2} WIP on e0ff8cec0
   IMP+LM+AJ wave). Matches the d02 census refs 8b45fe97 / 2902e0d3 / 8baa166e in count.
2. `git worktree list` = 4 lines: the main tree plus recovery_pack/baseline (detached),
   lsa_reboot_staging [reboot-staging-20261003], worktrees/salon-arena-mvp
   [codex/salon-arena-mvp]. The estate ALREADY runs worktrees for some seats.
3. `Get-Item memory\context_pack_latest.md` mtime = 2026-10-07 08:58:55 local (12:58:55Z),
   and `Select-String -Pattern "MEASURED ON","Sybil","max_concurrency"` over that rendered
   pack = 0 hits. The newest full-mode render on this tree still inhales zero mechanism-law
   bytes. CONVERGENT with dogfood2 lane d01-seat-boot-pack.json (its 08:29:23Z run re-shed
   the L0d carrier at stage 3, total_chars 9471 > 7200 budget).
4. `watch/inbox/PACK_OFFLOAD.jsonl` tail = 3 rows stamped 2026-10-07T12:58:55Z, mode full,
   max_chars 7200: shed "L2 trail" (total 9217), shed "L1 bonds" (7571), then stage-4
   "hard clip" (7571). The shed ladder is firing on the newest render and the pack still
   lands without the law tokens.
5. `Get-ScheduledTask` filtered Full/Estate/Mag: "Estate FullScan" state = Disabled
   (live confirmation of the 10-07 disable); 30+ Mag/Estate tasks exist, all reporting
   only Ready/Running/Disabled, no outcome surface in the state column.

## FINDING 1 (gap 1, MOONSHOT): the memory-propagation gap is a priority-ordering bug
wearing a compression costume; the compression externals are the wrong tool class

The estate's own bytes: mag/context_pack.py:1468-1514 implements a shed ladder that drops
"least load-bearing first" in a fixed shed_order, and the R4-L2 comments at
mag/context_pack.py:1498-1351 deliberately rank the mounted-vault-amendments block (L0d)
to shed ahead of L1 bonds only. The flash quantizer cuts at FLASH_MAX_CHARS = 220
(tools/thought_quantizer.py:118), before the mechanism byte of any amendment (d01 lane:
rows rib1:RIB_MOD / rib2:RIB_INF carry MEASURED ON only in 1796/2065-char frontier fields).
My live check 3 above reproduces the invariant on the newest render. Three separate rounds
(R4 memory, dogfood-100m d01, dogfood2 d01) have now re-derived the same invariant.

External candidates, tri-stated:
- LLMLingua (github.com/microsoft/LLMLingua, MIT, fetched 2026-10-07): "a compact,
  well-trained language model to identify and remove non-essential tokens", up to 20x
  compression, LLMLingua-2 token classification, and structured per-section rate tags.
  PARTIAL at best for our shape: perplexity-guided dropping is exactly the mechanism that
  destroys distinctive law phrasing (laws are low-frequency-token text), and the estate
  already quantizes laws to 220-char flash rows, so the budget problem is selection order,
  not raw size. WATCH. Do NOT build compression into the law path.
- Letta (github.com/letta-ai/letta, Apache-2.0, fetched): memory-tiered stateful agents;
  the README fetch carried no block-limit mechanics (docs page 404 at my fetch path), so
  its core/archival tiering matches our rib-vault-vs-flash-pack shape philosophically but
  nothing byte-verified here beats the estate's own two-stack design. WATCH.
- Mem0 (github.com/mem0ai/mem0, Apache-2.0, fetched): April 2026 algorithm is "single-pass
  ADD-only extraction", retrieval "semantic, BM25 keyword, and entity matching scored in
  parallel and fused". PARTIAL: our gap is compile-time must-survive selection under a
  fixed budget, not runtime recall; but the fused-scoring idea is exactly the missing
  priority signal for the shed ladder. ADAPT the scoring shape, not the product.
Verdict: the cure is internal and already 90 percent built. STEAL the rerank-then-select
PATTERN (score every pack candidate by law-criticality: amendment-flagged, law-head
digest member, mechanism-token-bearing), render in score order under the budget.
One-sitting move (~45 min): in mag/context_pack.py move the L0d vault-amendments block to
the END of shed_order (shed last among sheddables) and in tools/thought_quantizer.py raise
the flash slice to 400 chars for vault-amendment rows only; acceptance = fresh
`mag.cmd context-pack` then MEASURED ON greps non-zero in memory/context_pack_latest.md
(d01's own acceptance gate) and the red test_quantized_laws_section_renders_in_default_budget
goes green (1 failed, 41 passed per d01). Falsifier: if pinning L0d last still overflows
full mode (laws alone exceed 7200 chars), the defect is budget sizing, not ordering; and if
MEASURED ON rides without the FLASH_MAX_CHARS change, the 220-char half of the diagnosis
was wrong. Moonshot frame: this is the highest recurring build-day retirement available:
it is the boot path of every seat, and the estate has re-derived its failure in three
consecutive rounds; a stolen priority-allocator retires the whole class including the
mag/rib_boot.py:90-98 VAULT_RIBS omission class (RIB_MOSAIC_SEED_20260921.md missing from
the mount list, per d01).

## FINDING 2 (gap 2): the estate already owns the isolation mechanism and leaves it
unwired; the new stash detector has no cadence, which is itself a dead-man gap

Live evidence: my `git stash list` = 3 stashes still parked on the shared tree; my
`git worktree list` = 3 non-main worktrees already in daily use (reboot-staging-20261003,
salon-arena-mvp, a Temp recovery baseline). So worktree-per-seat is not a foreign import,
it is estate-native practice that the lane runner never adopted. The 10-07 detector
(tools/stash_sweep_watch.py, 285 lines, check/census verbs, no drop or pop verb by design
per its :19-20) is verified landed and tested (dogfood2 d02 deep_tier2: census re-run exit
0, 3 rows byte-matching state/stash_sweep_watch_state.json, pytest 2 passed in 1.68s), but
the same d02 verification proved BY EXHAUSTIVE ENUMERATION that no schtask and no
governor-loop surface runs check mode (25 scheduled tasks inspected, zero
stash_sweep_watch references; grep across mag/ empty), so a future sibling sweep is caught
only at the next manual run, outside the 900s window.
External candidates: git worktrees (built into the git the estate runs; mechanism already
exercised by 3 live trees) STEAL; flock is POSIX-only, Windows needs msvcrt.locking, and
the estate already owns tools/ledger_lock.py for the advisory-lock pattern, so ADAPT not
import; CRDT/OT file sync is overkill for source trees (keep cr-sqlite spiked for ledger
copies only, where it belongs). IDE shared-edit sessions: marketing for our shape.
One-sitting move (~40 min): register MagStashWatchDaily (every 15 min) running
`.venv\Scripts\python.exe tools\stash_sweep_watch.py check` through the existing
run_hidden.vbs pattern scripts/lawpack_daily.ps1 already uses, and probe one lane on a
worktree (`git worktree add ..\lsa-wt-probe`) to price the real migration. Falsifier: if
the pre-push ratchet or the shared-surface contract (watch/inbox as durable root) cannot
resolve from a linked worktree (hooks path or absolute-root assumptions), worktree-per-lane
is falsified as the general cure and the detector-plus-cadence stands alone as the answer.

## FINDING 3 (gaps 3+4, one class): premium-402-as-PASS and the 11-day 429 storm are
the same missing external pattern: an outcome heartbeat that survives runner-green

Estate bytes: tools/cost_rollup.py:22-29 documents spend_balance.v1 (pot, armed, as_of,
spent per ledger path, balance) as "the twice-owed Oct 2 move... re-owed by
break-economics.md:377 after the 10-06 premium wall" - that is the judgment-tier fix,
landed. For the scheduler class, my live Get-ScheduledTask run shows Estate FullScan
Disabled and 30+ sibling tasks whose State column carries Ready/Running/Disabled only;
state/NIGHT_LOOP_20261005.md:144 records the R2 finding "13 dead fleet fires under
LastTaskResult 0", and LONGRUNNER_LAW_20261007.md:9-10 records run_armC burning 24.4
CPU-hours over 11 days before anyone noticed. The instrument class is clear: Windows Task
Scheduler reports exit success while payloads fail for days, and the batch burn drivers
printed PASS while premium rails were down (the ask's 5150 all-skip batch incident).
External candidates, tri-stated: healthchecks.io self-hosted
(github.com/healthchecks/healthchecks, fetched 2026-10-07): "listens for HTTP requests and
email messages ('pings') from your cron jobs and scheduled tasks", "When a ping does not
arrive on time, Healthchecks sends out alerts", with Period + Grace parameters and 25+
integrations including a Shell Commands channel. This is EXACTLY our shape: a dead-man
switch per scheduled surface. STEAL the pattern (the estate already half-invented it:
tools/freshness_check.py heartbeats and the MagLawPackDaily alert channel in
scripts/lawpack_daily.ps1 are the same idea applied to one surface each). LiteLLM budgets
(docs.litellm.ai virtual_keys page, fetched): max_budget per key/user/team,
budget_duration resets, spend auto-tracked via completion_cost() - ADAPT as the semantic
template for a pre-flight gate that reads memory/runs/spend_balance.json at burn-driver
fire time and refuses premium batches when spent crosses the pot threshold (the
rejection-on-exceed behavior of LiteLLM itself was not verifiable from the page I fetched:
OWED, does not block the local gate). Helicone: not fetched this sitting, WATCH OWED.
One-sitting move (~50 min): one heartbeat JSONL (memory/runs/task_heartbeats.jsonl) that
every Mag/Estate schtask payload appends {task, ts, exit} to, plus one MagHeartbeatPatrol
that flags any task silent past 2 periods - this single pattern would have caught FullScan
at day 1 (not 11), run_armC at hour 1 (not 24.4 CPU-hours), and gives the stash detector
its missing cadence for free. Falsifier: if the heartbeat patrol false-alarms on legitimately
idle tasks often enough to get muted (the alert-fatigue kill), the cure must move to
LastTaskResult capture per fire instead; a week of quiet logs falsifies the false-alarm risk.

## FINDING 4 (gap 5): FOLD-FAST is a sound hand-rolled fallback router; the durable-
execution engines solve a superset a solo estate should not own

Estate bytes: watch/inbox/FOLD_FAST_20261007.md - the mutex stays by design as the
10-05 collision cure; when the gate is held at fold-phase start, prose routes to the local
janitor (qwen2.5:7b) with an enforced number rule whose first live run REFUSED a summary
that reformatted numbers with punctuation (the rule bites), funded-tier review unchanged,
and mickey17-burn.dwf.ts amended with the gate PASS digest 5e3a9319cd5d. External:
Temporal/Airflow/Prefect-class engines (general knowledge, not primary-fetched this
sitting: OWED) buy durable state, retries, and schedules at the price of running an
execution service - heavy ops for a 3-machine estate whose fold path already has a
deterministic bounded half, a local fallback, and a funded verifier. Verdict: WATCH the
engines; do NOT stand one up. NOT build: no workflow engine adoption for the fold path.
One-sitting move (~20 min): make the fold log line also print queue-wait (fold-request
timestamp minus lock-acquire timestamp) so the WATCH has a tripwire number: if p95 wait
stays under 5 minutes for a month, the engines are permanently retired by measurement.
Falsifier: the WATCH verdict dies if fold queue wait exceeds the tripwire twice in one week.

## FINDING 5 (gaps 6+7): law-pack lag is an OPA-bundles-shaped distribution problem and
the Herald-OS repo read corrects the estate's own link-drop; GSTD prior art is the
network's own live census

Law-pack lag: OPA bundles (openpolicyagent.org management-bundles docs, fetched
2026-10-07): bundles "loaded on the fly without requiring a restart", "enforced
immediately", polling min_delay_seconds config, signed bundles where OPA "activates the
new bundle only if all the verification steps succeed", and last-known-good behavior on
failure ("continues using its existing bundle"). The estate's MagLawPackDaily is a daily
cron (d01 lane: Enabled, Ready, Last Result 0, compile_report.json stamped
2026-10-06T18:26:38Z at verify time) - but finding 1 shows the fresh pack STILL carries
zero mechanism bytes, so day-lag is not the binding constraint, selection is. Verdict:
ADAPT OPA's dirty-flag continuous-distribution semantics, WATCH OPA itself (Rego/bundles
are a foreign dependency for law text). One-sitting move (~30 min): have the amendment
mount path in mag/rib_boot.py append a {pack_dirty: true, ts, reason} row to
memory/corpus/quantized_thought/dirty.flag, and have scripts/lawpack_daily.ps1 check the
flag first so an hourly variant recompiles only when laws moved; keep the daily cron as
last-known-good. Falsifier: if dirty flags are written but never cleared (recompile churn)
or the hourly variant never fires, the flag channel is broken and the day-lag diagnosis
was incomplete.
Herald OS: the estate receipt watch/inbox/HERALD_OS_20261007.md marked the repo read OWED.
My fetch of github.com/iamlukethedev/Herald-OS (2026-10-07) byte-discharges the README
leg with a CORRECTION: the shipped mechanism is a four-tier PERMISSION gate (read and act
tools "run straight away and are logged"; mutate tools "ask first, and you can allow them
for the session or always"; destructive tools "ask every time"), an audit log, and
protected paths ("Some locations, such as ~/.ssh, your keychains and Hermes's own
credentials, are always refused"); MIT, "Status: alpha (0.1)". The receipt's "token-tier
implementation (what counts as native vs model)" steal target does NOT appear in the
README - that framing rode the X launch prose, so the S1 row needs re-pointing at the
permission-gate code (the herald-os-bridge plugin) before vendoring. Tri-state: approval
gate = SOLVES OUR SHAPE (the effect-broker prior art, MIT, byte-verified at README level);
Hermes desktop embodiment = PARTIAL (alpha, Linux-distro-first, the estate is
Windows-hosted); OS packaging/marketing = MARKETING for our purposes. One-sitting move
(~60 min): read the bridge plugin's gate implementation (the OWED S1 row), then vendor the
four-tier verb classification + protected-paths always-refuse into the effect broker's
registry as prior art with attribution. Falsifier: if the gate code diverges from the
README (alpha risk: README promises, code defaults), the vendoring target collapses to
WATCH. GSTD: watch/inbox/GSTD_NODE_CENSUS_20261007.md answers the "who runs these nodes"
ask from the field: 4 live census nodes including a Raspberry Pi bootstrap running
llama3.2:3b with 272 tasks completed and 47.39 GSTD earned, and a localhost-node running
qwen2.5:7b; the gstdbot repo ships docker compose with a curl /health healthcheck
(census section 2, docker compose config exit 0), and stash@{0} (my stash list) shows the
image already pulled and compose ready with ONE input owed: GSTD_WALLET_ADDRESS. Verdict:
STEAL the join (node-lite first), the fleet prior art is the network itself. Mesh lane
dispatch: exo (github.com/exo-explore/exo, Apache-2.0, fetched) is model-inference
sharding ("Pipeline sharding", "Tensor parallelism", "running models larger than would
fit on a single device", "runs on CPU on Linux" currently), NOT discrete agent-lane
dispatch - WATCH for inference partitioning, wrong tool for lanes. k3s/Nomad solve lane
scheduling but at ops cost a solo estate should not pay for 3 machines. NOT build: no
k3s, no Nomad. The honest external answer for lane dispatch across desktop + bob + Pixel
is the tailnet the estate already runs plus the mesh_delta standing wave; steal nothing
yet, price nothing yet.

## What NOT to build (exists, verified): LLMLingua-style compression inside the law path
(mangles low-frequency law tokens); a CRDT layer for source-tree contention (worktrees are
built-in and already in estate use); Mem0/Letta as a runtime memory product (compile-time
selection is the estate's shape; only Mem0's fused scoring is worth adapting); LiteLLM
proxy as infrastructure (one local pre-flight gate gets the semantics without the service);
Temporal/Airflow/Prefect for folds; k3s/Nomad for 3 machines; an OPA dependency for law
distribution.

## CORRECTION ADDENDUM (2026-10-07, post hostile second pass: finding 1's move
withdrawn and replaced; diagnosis upgraded)

The second pass correctly falsified the original finding-1 move. Re-derived from
bytes this sitting:

- Emit placement: mag/context_pack.py:1505-1514 - the shed loop rebuilds text
  AFTER removing each block (:1510-1513) and emits after removal (:1514), so
  PACK_OFFLOAD total_chars is the SURVIVING size. Arithmetic from the full
  14:09:37Z ladder (Select-String over watch/inbox/PACK_OFFLOAD.jsonl, root
  0186ab4610f4): L0d vault-amendments carrier = 13629-9338 = 4291 chars; L1
  bonds = 1646; and the post-all-sheds floor = 7692 chars against the full-mode
  budget 7200 (mag/context_pack.py:165). The mandated non-sheddable core alone
  (policy_bare + build_block + scope_block + task_small, :1511-1512) exceeds the
  budget by 492 chars, so EVERY full-mode render ends in a stage-4 hard clip that
  amputates the task tail regardless of shed order, the exact amputation the
  rung-3 comment at :1471-1477 forbids. Reordering L0d last is falsified: keeping
  the 4291-char carrier requires budget >= 11983 (core + carrier).
- Flash raise leg falsified by measurement: probe script
  watch/inbox/ractor_engine/2026-10-07-external-steal/_probe_flash_fields.py run
  with .venv python over memory/corpus/quantized_thought/instructions_flash.jsonl
  (12 rows): MEASURED ON sits at char 807 of rib1:RIB_MOD's 1796-char frontier
  field and char 846 of rib2:RIB_INF's 2065-char frontier field, absent from all
  flash fields (max 220). A 220->400 raise surfaces nothing; the acceptance law
  text is unreachable below ~850 chars of frontier.
- NEW live red found this sitting, not in d01's adjacent suite: pytest
  tests/test_context_pack_delivery.py -q = 8 failed, 21 passed - all five
  test_quantized_laws_render_in_every_mode params (janitor/route/build/audit/full)
  plus test_render_fits_budget_without_hard_clip[build/plan/full]. The estate's
  own fit-budget gate is red in three modes on today's tree; the 492-char core
  overage is not a hypothesis, it is an already-failing named gate. Also re-ran
  tests/test_context_pack_quantized_laws.py -q = 1 failed, 2 passed (assert at
  :23, rendered pack visibly ends "…(pack clipped)").
- Confirmed missed nuance: the 12:58:55Z render (root daacc7e4439d) never emitted
  an L0d row across its full ladder - the vault block was not loaded into
  sheddable, which builds conditionally (mag/context_pack.py:1482-1484 from
  pack["rib_vault"], :382), so acceptance also depends on the rendering seat
  carrying a mounted vault.
- No literal budget pin: grep -rn "7200" tests/ = zero hits.

CORRECTED MOVE (replaces the withdrawn reorder + flash-raise move): one sitting,
~90 min: (1) raise full-mode max_chars 7200 -> 8000 at mag/context_pack.py:165
(no literal test pin exists, grep-verified; the delivery-gate suite re-run is the
acceptance); (2) replace the L0d carrier body (4291 chars of amendment bodies)
with a digest of one line per mounted amendment (~5 x 60 chars), each line
extracted from the amendment sentence carrying its matched law token so MEASURED
ON actually rides; (3) move "L0d rib vault amendments" to the END of shed_order
(mag/context_pack.py:1501-1503). Acceptance: fresh full render greps MEASURED ON
non-zero in memory/context_pack_latest.md, test_context_pack_delivery.py and
test_context_pack_quantized_laws.py green, zero new "hard clip" offload rows.
Falsifier (tightened): the corrected move fails its own gate if any fresh render
still emits a hard-clip row; if the delivery-gate suite or ratchet rejects the
budget raise, the cure is NOT one sitting (the mandated core itself must shrink
below 7200 minus digest) and the finding downgrades to diagnosis-only; if
law-line extraction cannot carry MEASURED ON into the digest, the carrier must
be built from frontier substrings around matched law tokens instead.

## Blind spots

- Herald-OS: README-level byte verification only; the gate code itself unread, license
  file unconfirmed (MIT claimed at repo level), alpha-quality assessment not done.
- LiteLLM rejection-on-exceed behavior and healthchecks' license: not primary-verified
  this sitting (OWED); the dead-man mechanism and the budget semantics are verified.
- Temporal/Airflow/Prefect claims ride general knowledge, not primary fetches (OWED);
  finding 4's verdict does not depend on their internals.
- The FullScan storm counts (20432 of 20578 rows 429-fail) and the 5150 all-skip batch
  figure ride the ask's own material; I verified only the task's current Disabled state
  and the class evidence around it, not those counts.
- The 12:58:55Z pack render I read was produced by another seat's run; I did not re-run
  mag.cmd context-pack myself (it rewrites the shared memory/context_pack_latest.md).
- Letta's core-memory block size limits: docs 404 at my fetch path, README carried no
  mechanics; the Letta assessment is positioning-level only.
- External maintenance status is a point-in-time read of GitHub pages (2026-10-07).
