# OPERATIONS LENS: EXTERNAL-STEAL RACTION (2026-10-07)

Lens: operations (orchestration surgeon). Topic: the estate's self-named gaps of the
last 48h, checked against who already solved each one externally. Every claim below was
read or run this sitting; anything not verifiable is marked OWED and never asserted.
No em-dashes. Instruments are named next to every count (quantifier law).

## 0. WHAT I RAN THIS SITTING (instruments)

1. state/ listing by mtime (PowerShell Get-ChildItem, 2026-10-07 ~12:30Z): canon =
   state/CURRENT.md (mtime 04:47 local); START_BRIEF/LIVE_REPORT excluded per
   AGENTS.md load-order row 0a (machinery pages).
2. LIVE falsifier re-run: `mag.cmd context-pack` fired at 2026-10-07T12:39:55Z
   (PACK_OFFLOAD.jsonl rows carry that ts). Grep of memory/context_pack_latest.md
   (Select-String over the whole file, no truncation): MEASURED ON 0 hits, Sybil 0,
   max_concurrency 0, marathon 0, POST-DATUM 3, L0d 1. Offload rows at the same ts:
   mode full, max_chars 7200, total_chars 7571, shed_sections ["L1 bonds"] stage 3,
   then ["hard clip"] stage 4.
3. LIVE schtasks query (`schtasks /Query /FO CSV | Select-String FullScan`):
   "\Estate FullScan","N/A","Disabled" - the drain-death task is disabled as of now.
4. `git worktree list` + `git stash list` on the estate repo (git 2.55.0.windows.2):
   4 worktrees registered (main, Temp/recovery_pack/baseline detached, lsa_reboot_staging,
   worktrees/salon-arena-mvp) and exactly 3 stashes live on the shared main checkout,
   matching the HOLD-RECONCILE census in tools/stash_sweep_watch.py:9-10.
5. Reads: state/CURRENT.md; watch/inbox/DAWN_REPORT_20261006.md;
   watch/inbox/NIGHT_BURN_DESIGN_20261007.md;
   watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md;
   memory/runs/mickey17_v2/runs/dogfood2-20261007/lanes/d01-seat-boot-pack.json;
   memory/runs/mickey17_v2/runs/morning-block-20261007/lanes/m2-todo-truths.json;
   mag/context_pack.py; tools/stash_sweep_watch.py; tools/fold_prose_local.py;
   tools/thought_quantizer.py.
6. External byte-checks (WebFetch/WebSearch this sitting): github.com/iamlukethedev/Herald-OS,
   github.com/microsoft/LLMLingua, github.com/mem0ai/mem0,
   docs.litellm.ai/docs/proxy/self_serve, github.com/healthchecks/healthchecks,
   github.com/exo-explore/exo, github.com/temporalio/temporal, github.com/vlcn-io/cr-sqlite,
   git-scm.com/docs/git-worktree, TON docker prior art (ton-blockchain/ton docker README
   via search), Nomad homelab threads via search.

## 1. GAP 1: MEMORY PROPAGATION (laws shed at stage 3)

Estate bytes: full-mode budget 7200 (mag/context_pack.py:165). The "L0d rib vault
amendments" block sits second-from-last in shed_order (mag/context_pack.py:1501), so any
overflow eats mechanism laws early; the shed is loud (pack_offload.v1 rows emitted at
mag/context_pack.py:1514) but loud is not survival. Flash rows cut laws at 220 chars
before the mechanism byte (FLASH_MAX_CHARS = 220, tools/thought_quantizer.py:118). The
d01 lane re-proved zero-law inhalation on today's tree (d01-seat-boot-pack.json:6 and
:29-30: total_chars 9471 > 7200 at stage 3). My own 12:39:55Z render REPRODUCES the gap
with a twist: overflow is smaller today (7571 > 7200) so L1 bonds shed instead of L0d,
and the mechanism laws STILL render zero bytes (the 220-char flash cut and the
VAULT_RIBS omission keep them out even when the carrier survives).

External candidates:
- LLMLingua / LLMLingua-2 (github.com/microsoft/LLMLingua, MIT, active, fetched):
  token-level importance compression with absolute target_token budgets and per-section
  tags with individual rates. Tri-state: PARTIAL. Our shape is not "compress prose", it
  is "protect five named law blocks under a fixed cap"; a learned compressor adds a model
  dependency and probabilistic survival where the bug is a deterministic ordering choice.
  ADAPT (the per-section exempt/rate idea, not the model).
- Mem0 (github.com/mem0ai/mem0, Apache-2.0, active, fetched): ADD-only extraction,
  retrieval-time fused scoring. Tri-state: MARKETING for this gap. It assumes storage
  abundance and filters at read time; the context pack is a fixed-budget render at boot,
  the inverse shape. WATCH (possible later fit for warm_state tiering).
- RAG rerankers / context-budget prioritizers: named by the ask, not separately verified
  this sitting (OWED).

Verdict: ADAPT. One-sitting probe (estate-local, zero deps): exempt "L0d rib vault
amendments" from the sheddable list entirely (mag/context_pack.py:1479-1503) and raise
FLASH_MAX_CHARS for law rows or shorten the five amendment flash fields
(d01-seat-boot-pack.json:41 names the same move). Acceptance: the red test
test_quantized_laws_section_renders_in_default_budget goes green
(d01-seat-boot-pack.json:38, currently "1 failed, 41 passed") and MEASURED ON greps
non-zero in a fresh mag.cmd context-pack render. 20 minutes.
NOT build: no compression model on the boot path. The laws are ~2k chars; this is budget
arithmetic and shed policy, not compression research.

## 2. GAP 2: MULTI-SEAT TREE CONTENTION (the R3/R5 sweep class)

Estate bytes: the detector landed tonight with NO drop or pop verb by design
(tools/stash_sweep_watch.py:16-23); 3 stashes still live on the shared checkout (my
git stash list this sitting); sibling-stash risk stands open (state/CURRENT.md:56-59);
two mid-landing sweeps in one night are on record (watch/inbox/DAWN_REPORT_20261006.md:113-116);
the founding incident captured "another lane's eleven executor files"
(tools/stash_sweep_watch.py:5-8).

External: git itself, now EMPIRICALLY verified this sitting (hostile second pass
demanded it; throwaway two-worktree repo on the estate's own git 2.55.0.windows.2,
temp dirs Temp/gwt_probe + Temp/gwt_probe_wtB, removed after). Three measured
results: (1) capture containment HOLDS - with main's a.txt modified and wtB's b.txt
modified, wtB's `git stash push` captured b.txt only (`stash show --name-only` run
from main = "b.txt") and main's " M a.txt" survived untouched: the R3 capture class
is contained by per-seat worktrees. (2) refs/stash is SHARED: main's
`git stash list` lists wtB's stash ("On wtB: wtB-stash"), consistent with
git-scm.com/docs/git-worktree (refs under refs/ are shared except bisect/worktree/
rewritten). (3) the pop/drop surface is NOT contained: `git stash pop` run in MAIN
applied wtB's b.txt edit into main's checkout (b.txt reads "wtB-edit", status
" M b.txt") and dropped the ref ("Dropped refs/stash@{0} ...") silently. Detector
consequences, byte-checked in tools/stash_sweep_watch.py: the recent-write window
stats root/rel in the MAIN checkout only (:88-105, stat at :100), seen refs are
never re-evaluated (:171-172), and absent-from-main paths fire as "deletion
captured" (:185-186), so a cross-tree stash is mis-scored BOTH ways (quiet when it
should alarm; false deletion-captured when the path is wtB-local-new); and no
census-decrease path exists (check() :144-212 handles new refs only; census()
:215-239 is print-only). Today's 3 live stashes were all minted on the main branch
(labels read "WIP on mag/run-beta1-..." per my git stash list), so current rows
score correctly; the CHARTER ITSELF creates the mis-scored population, which makes
the detector amendment a precondition of the charter, not polish.
Verdict: STEAL the topology + KEEP the detector, adapted. One-sitting probe:
(a) charter line "seats boot into their own `git worktree add ../lsa-seat-<name>`,
never into the main checkout, and NEVER pop or drop a stash whose label names
another branch" (labels carry "On <branch>:", so provenance is human-readable);
(b) amend stash_sweep_watch: alert on census DECREASE (a seen ref vanishing = the
only symptom of a silent cross-tree pop), classify each live stash's minting tree
from its label vs the running checkout's branch, and score the recent-write window
against the owning worktree when they differ. Acceptance: in a two-worktree drill,
a wtB-minted stash popped in main fires the decrease alert and the census row
names wtB. 60 minutes.
NOT build: no flock protocol, no OT/CRDT file sync, no shared-edit sessions for
the capture class. The pop/drop surface cannot be fixed by topology at all (the
ref namespace is shared); it holds only as a protocol clause plus the decrease
alarm.

## 3. GAPS 3+4 AS ONE CLASS: GREEN LABELS OVER DEAD REALITY

Estate bytes: FullScan ledger census (m2-todo-truths.json:8-21): 20,578 parsed rows
09-24 to 10-06, ok:true ZERO, 20,432 [429] fails, 47 TimeoutError, while the schtask
read "Last Result 0, Status Ready"; my live query shows it finally Disabled. The
free-lane fleet sat dark for 13 scheduled fires under LastTaskResult 0
(watch/inbox/DAWN_REPORT_20261006.md:41-43). The burn driver printed PASS on all-skip
batches and read the reserve-wall 402s as "2 OK asks" (HERMES_402_WALL_20261007.md:55-57),
cured tonight by TERMINAL markers, split summary, and spend_balance.json
(HERMES_402_WALL_20261007.md:48-70, falsifier at :101-105).

External:
- Healthchecks (github.com/healthchecks/healthchecks, BSD-3, self-hostable, fetched):
  dead man's switch; jobs ping on success; alert fires when a ping is late by
  period + grace. Tri-state: SOLVES OUR SHAPE (the contract; the server itself is
  optional). STEAL.
- LiteLLM (docs.litellm.ai/docs/proxy/self_serve, fetched): max_budget per
  key/user/team with budget_duration resets, tpm/rpm caps, soft-budget alerting; budget
  exceed blocks calls (exact exception name from LiteLLM's issue tracker via search
  summary; byte OWED). Tri-state: PARTIAL for a solo estate (a proxy is heavy), but the
  CONTRACT is the cure: cost state must be an input the runner reads BEFORE dispatch,
  not a post-hoc receipt. ADAPT.
- Helicone: named by the ask, not verified this sitting (OWED).

Verdict: STEAL the dead-man contract in one sitting: every schtask wrapper
(scripts/lawpack_daily.ps1, scripts/box_burn_nightly.ps1, scripts/census_patrol_daily.ps1)
appends one heartbeat row (ts, task, exit, ok-count) to a single memory/ops/heartbeats.jsonl
on SUCCESS only, and the existing daily patrol fails when any registered task's heartbeat
is older than its period + grace. ~60 lines reusing the R2 liveness-tripwire pattern
(DAWN_REPORT:41-43). 60 minutes.
MOONSHOT: this class is the 10x frame. It ate 11 days of FullScan firing into a dead
429 storm, 13 dark fleet fires, and an uncounted run of PASS-on-all-skip burn batches.
Every cure so far is bespoke (stash detector, TERMINAL markers, freshness gate, one
liveness tripwire). Stolen wholesale, the class retires permanently: exit code +
success-ping + spend balance become the only truth surfaces, enforced by ONE patrol
instead of one detector per incident. The next incident will be a different seam;
the patrol shape is seam-independent.
NOT build: no new per-task watcher script. Each bespoke detector is a promise that the
next seam gets its own detector.

## 4. GAP 5: FOLD-PHASE SERIALIZATION

Estate bytes: cross-run fold mutex landed as commit 55cdaaa4f
(watch/inbox/DAWN_REPORT_20261006.md:50-51); FOLD-FAST routes contended fold prose to
the local janitor (watch/inbox/NIGHT_BURN_DESIGN_20261007.md:41-43) under a hard
no-half-write law with one-shot bounded timeout and exit-3 cloud fallback
(tools/fold_prose_local.py:12-31).
External: Temporal (github.com/temporalio/temporal, MIT, active, fetched): durable
execution with automatic retries and a single-process dev mode (`temporal server
start-dev`). Tri-state: SOLVES THE GENERAL SHAPE, but the estate's serialization is BY
DESIGN (the mutex is the contract) and the hang class is already cured by local routing.
Verdict: WATCH. Do not import a durable-execution server for a solo desktop; steal only
the two semantics the fold lacks: idempotent re-entry keys (already implicit in the
slug keying) and worker heartbeats (absent; the prose leg hung silently until an
operator noticed). Falsifier: any recurrence of a fold hang WITH FOLD-FAST active flips
this to ADAPT (Temporal start-dev behind the fold gate).

## 5. GAP 6: LAW-PACK DAY-LAG

Estate bytes: MagLawPackDaily verified armed by the d01 lane (Enabled, Ready, Last
Result 0, daily 09:30 fire, d01-seat-boot-pack.json:20-24); the pack recompiled 10-06
carrying 2 of 12 law rows (watch/inbox/DAWN_REPORT_20261006.md:203-207 amendment).
External: continuous-policy-distribution / GitOps / OTA channels assume a fleet of
receivers; the estate has one receiver and now a daily compile. The residual lag is not
distribution, it is two render bugs: the 220-char flash cut
(tools/thought_quantizer.py:118) and the VAULT_RIBS list that never mounts
RIB_MOSAIC_SEED_20260921.md (mag/rib_boot.py:90-98, d01-seat-boot-pack.json:47).
Verdict: WATCH (no external steal). Probe: the two estate-local edits above; acceptance
= the d01 grep goes non-zero. NOT build: any OTA or config-drift-watchdog machinery for
a single-box estate.

## 6. THE ASKS

- Herald-OS (github.com/iamlukethedev/Herald-OS, MIT, alpha 0.1, repo fetched): the
  gate is real and matches the effect-broker shape: read/act tools run immediately but
  logged; mutate asks first (allow per-session or always); destructive asks EVERY time;
  protected paths (~/.ssh, keychains, credentials) always refused; audit at
  ~/.hermes/herald-os/audit.jsonl. CORRECTION to the ask's premise: its tiers are
  PERMISSION tiers, not token tiers; usage/quota is a provider-plan panel with a 90
  percent warning. Verdict: ADAPT. Probe: map the four tiers + always-refused paths +
  audit.jsonl schema onto the estate's switchboard/effect-broker contract as a one-page
  spec diff, then wire ONE estate effect class (schtask changes) through
  ask-per-session gating. One sitting.
- GSTD node ops: official prior art exists: ton-blockchain/ton ships a docker/
  directory with fullnode/validator compose (search-verified), and the official docker
  README carries the constraint that a TON fullnode REQUIRES a public IP address
  (NAT/k8s needs extra setup). The estate's own stash@{0} message (my git stash list
  this sitting) records gstdbot image pulled, compose ready, MCP already in the node
  DNA, one input owed (GSTD_WALLET_ADDRESS). Verdict: STEAL the official compose shape;
  do not hand-roll a node image. Caveat for the desktop full-node ambition: tailnet-only
  addressing will not satisfy the public-IP requirement; lite-server client mode is the
  honest node-lite shape (lite-server semantics from docs.ton.org family; byte OWED
  this sitting).
- Mesh lane dispatch: exo (github.com/exo-explore/exo, Apache-2.0, active, fetched)
  auto-discovers devices and splits MODEL layers (topology-aware autoparallel) with
  OpenAI/Ollama-compatible endpoints; Linux is CPU-only today. It shards models, not
  agent lanes: wrong layer for lane dispatch, possible fit for a node-lite inference
  fleet. WATCH. Nomad: single binary, combined server+client agent, raw_exec drivers,
  GPU stanza (search-verified HashiCorp discuss threads): the right shape IF bob +
  desktop ever need scheduler semantics; until then the estate's lane runner at measured
  widths beats a cluster server on a 2.5-machine mesh. ADAPT-LATER/WATCH. Ray, k3s:
  named by the ask, not separately verified this sitting (OWED).

## 7. BLIND SPOTS

- RESOLVED in the second pass: the two-worktree empirical test ran this sitting and
  the results are in section 2 (containment holds; refs/stash shared; cross-tree pop
  silently bleeds). Remaining sub-blind: the pop/drop cure is a PROPOSED protocol
  clause plus an unlanded detector amendment; until they land, a cross-tree pop
  stays silent on the estate's real tree.
- The LLMLingua probe is unexecuted; compression quality on law prose is unknown. The
  ADAPT verdict rests on its documented per-section/target_token mechanics only.
- Helicone, Ray, k3s, TUF, generic rerankers: candidates the ask named that I did not
  byte-check this sitting.
- cr-sqlite: repo fetched (MIT, multi-writer CRDTs via crsql_as_crr + crsql_changes)
  but the page exposed no commit-date bytes; the estate's ledger-copy spike rides a
  dependency whose maintenance status I could not confirm (OWED: check the releases feed).
- The Pixel phone seat: no candidate verified for phone-side dispatch (exo does not do
  Android today per its README).
- I did not read the Herald-OS bridge plugin source itself (README + structure only);
  the "token-tier" correction comes from the README, and the gate code is OWED before
  any code-level steal.
