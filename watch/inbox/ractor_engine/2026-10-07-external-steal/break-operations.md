# BREAK-OPERATIONS: hostile second pass on the operations lens (2026-10-07)

Target: the operations-lens external-steal report for the estate's self-named gaps.
Method note: the report JSON arrived TRUNCATED mid-finding-3 in transit; I recovered the
full lens output from its own banked write-up, which the report cites and which exists:
watch/inbox/ractor_engine/2026-10-07-external-steal/operations.md (sections 1-6). Every
verdict below is against that file plus the ask's visible findings 1-3.

## What I ran this sitting (instruments)

1. `mag.cmd context-pack` fired by ME at 2026-10-07T13:30:11Z (PACK_OFFLOAD.jsonl rows
   carry that ts, root_short 8e5b3a6e4ea4). Post-run grep over the WHOLE
   memory/context_pack_latest.md (7394 bytes): MEASURED ON 0, Sybil 0, max_concurrency 0,
   marathon 0, POST-DATUM 3. Offload rows at 13:30:11Z: total_chars 13695 shed "L2 trail"
   stage 3, then 9404 shed "L0d rib vault amendments" stage 3, then 7758 shed "L1 bonds"
   stage 3, then "hard clip" stage 4 at 7758 > 7200.
2. Ledger read-back of the LENS's own run: grep "2026-10-07T12:39:55"
   watch/inbox/PACK_OFFLOAD.jsonl = 12 rows. Eleven stage-3 sheds 19538 -> 7571
   (L0e resonance, L0 coordination, L0 behavioral+tesuji, L0d zeitgeist, L0-continuity,
   L0b agent state, L0d proven moves, L0d solved history, L1b/L1c, L2 trail, L1 bonds at
   7571) then stage-4 hard clip at 7571. "L0d rib vault amendments" was NOT shed in that
   render: it survived, and MEASURED ON still read 0. Both shed branches now measured.
3. Law-byte census (GNU grep, this sitting): MEASURED ON rides in MOUNTED ribs
   (memory/rib/RIB_MODEL_GATES_20261001.md 2 hits; memory/rib/RIB_INFERENCE_BUDGET_20261001.md
   1 hit); Sybil rides ONLY in the UNMOUNTED memory/rib/RIB_MOSAIC_SEED_20260921.md
   (2 hits); max_concurrency rides in NO rib (0 hits in
   memory/rib/RIB_FREE_USAGE_POLICY_20260823.md).
4. Live schtasks /Query /V (this sitting): "\Estate FullScan" Status Disabled,
   Scheduled Task State Disabled, Last Result 0, Last Run 10/6/2026 9:35:01 AM, daily
   09:35; "\MagLawPackDaily" Status Ready, Enabled, Last Result 0, Last Run 10/6/2026
   9:30:01 AM, Next 10/7/2026 9:30:00 AM. The d01 quote matches byte-for-byte.
5. `git worktree list` + `git stash list` (git 2.55.0.windows.2, `git --version` this
   sitting): 4 worktrees (main + Temp/recovery_pack/baseline detached + lsa_reboot_staging
   + worktrees/salon-arena-mvp) and exactly 3 stashes on the shared checkout.
6. EMPIRICAL two-worktree stash test in a throwaway repo (%TEMP%/brk_stash, init ->
   worktree add -b wtB -> edit a.txt in main and b.txt in wtB -> stash push in wtB ->
   observe from main -> stash pop in main; scratch repo removed after):
   A) main's a.txt untouched by wtB's stash (capture containment HOLDS);
   B) main's `git stash list` SHOWS wtB's stash (refs/stash is a shared common-dir ref);
   C) stash show --stat from main lists only wtB's b.txt (content stays worktree-local);
   D) `git stash pop` run in MAIN applied wtB's b.txt change INTO the main tree and
   DROPPED the stash ref (cross-worktree pop hazard, demonstrated, silent).
7. Reads: mag/context_pack.py:150-189 and :1470-1518; tools/thought_quantizer.py:105-134;
   mag/rib_boot.py:78-104 (VAULT_RIBS = exactly 7 ribs ending RIB_MARATHON_DISORIENTATION.md,
   no RIB_MOSAIC_SEED_20260921.md); tools/stash_sweep_watch.py (whole); state/CURRENT.md;
   d01-seat-boot-pack.json; m2-todo-truths.json; HERMES_402_WALL_20261007.md:40-114;
   DAWN_REPORT_20261006.md:35-64, :105-124, :198-207; NIGHT_BURN_DESIGN_20261007.md:33-52;
   tools/fold_prose_local.py:1-45; git log -1 55cdaaa4f (FOLD GATE FLEET-WIDE, real).
8. External byte-checks (WebFetch this sitting): git-scm.com/docs/git-worktree;
   raw.githubusercontent.com/healthchecks/healthchecks/master/LICENSE;
   docs.litellm.ai/docs/proxy/self_serve; github.com/microsoft/LLMLingua;
   github.com/temporalio/temporal; github.com/iamlukethedev/Herald-OS;
   github.com/exo-explore/exo; github.com/vlcn-io/cr-sqlite/releases;
   raw.githubusercontent.com/ton-blockchain/ton/master/docker/README.md.

## Verdicts

### Finding 1 (gap 1, memory propagation): CONFIRMED
Every cite byte-checked: mag/context_pack.py:165 (full-mode max_chars 7200), :1501
("L0d rib vault amendments" second-from-last in shed_order), :1514 (stage-3 offload emit);
tools/thought_quantizer.py:118 (FLASH_MAX_CHARS = 220); d01-seat-boot-pack.json:6 and
:29-30 (9471 > 7200, shed ["L0d rib vault amendments"] stage 3) and :38 ("1 failed, 41
passed" incl. test_quantized_laws_section_renders_in_default_budget); the lens's own
12:39:55Z ledger rows byte-exact (L1 bonds 7571 + hard clip 7571). My independent
13:30:11Z render reproduces zero-law inhalation through the OTHER branch the lens's
falsifier named: this render overflowed to 13695, shed the L0d carrier at stage 3, and
STILL hit the stage-4 hard clip at 7758. Zero laws under both shed branches confirms the
multi-suppressor mechanism (shed policy is not the only hole; the 220-char flash cut and
the VAULT_RIBS omission act even when the carrier survives). LLMLingua externals verified
(MIT; absolute target_token; per-section rate tags incl. compress=False opt-out).
CORRECTION to the move, not the finding: "two-line edit, 20 minutes" undercounts. My
13695 render proves the stage-4 hard clip is a SECOND amputation point: exempting L0d
without budget headroom can still clip it on a heavy day, and the stated acceptance is
reachable for MEASURED ON only (its carriers are mounted ribs); Sybil needs the
VAULT_RIBS += RIB_MOSAIC_SEED_20260921.md edit (mag/rib_boot.py:90-98, verified missing)
and max_concurrency needs a minted rib (it is in no rib, 0 hits). d01:47-50 already names
these; the lens's gap-1 move dropped them while its own falsifier predicted them.

### Finding 2 (gap 2, multi-seat tree contention): WEAKENED
Estate bytes all confirmed: 4 worktrees / 3 stashes (live), stash_sweep_watch.py:4-8
(eleven executor files), :9-10 (3-stash HOLD-RECONCILE census), :16-23 (no drop/pop
verb), state/CURRENT.md:56-59, DAWN_REPORT_20261006.md:113-116 (two mid-landing sweeps).
Doc quote verified verbatim: git-worktree docs say worktrees share everything except
"per-worktree files such as HEAD, index, etc." and mention stash only as a see-also in
EXAMPLES (the lens's silence claim is accurate). I then ran the OWED empirical test.
Result: the sweep-CAPTURE class is contained by worktree topology (wtB's stash push never
captured main's a.txt; captured paths are wtB-local), so "STEAL the topology" stands.
But the lens's "retire the detector family" is KILLED by measurement: refs/stash lives in
the shared common dir, so the stash LIST is cross-worktree (main sees wtB's stash) and a
cross-worktree `git stash pop` in main silently applied wtB's held change and dropped the
ref. The falsifier's predicted signal fires in a third state the lens did not enumerate:
the list grows with another tree's entry while captured paths stay local. The charter line
survives with one added clause: never pop a stash you did not create in this worktree;
`git stash show` first. The detector stays, adapted: it must warn on census DECREASE
(a pop/drop happened somewhere) and its check-mode mtime intersection stats paths against
the main root only, so a stash minted inside another worktree is judged against the wrong
tree (false-negative surface it does not know it has).

### Finding 3 (gaps 3+4, green labels over dead reality): CONFIRMED
m2-todo-truths.json:8-21 matches exactly (20,599 raw / 20,578 parsed, ok:true 0, 20,432
[429], 47 TimeoutError, schtask "Last Result 0, Status Ready"); my live schtasks query
reads Estate FullScan Disabled (the ask's "disabled 10-07" confirmed); DAWN_REPORT
20261006.md:40-43 (13 dark fires under LastTaskResult 0) confirmed; HERMES_402_WALL
20261007.md:55-57 ("2 OK asks" when both were $0.00 skips), :48-70 (TERMINAL rails +
spend_balance.v1 writer, grand_total_usd 231.0322 over 28,553 calls) and :101-105
(falsifier) all confirmed. healthchecks BSD-3 verified from the LICENSE text; LiteLLM
max_budget per team/user/key + budget_duration resets + tpm/rpm verified on self_serve;
soft-budget alerts and the exact block-on-exceed exception are NOT on that page and stay
OWED exactly as the lens flagged. All three named wrapper scripts exist on disk
(scripts/lawpack_daily.ps1, box_burn_nightly.ps1, census_patrol_daily.ps1), so the
heartbeat move has real anchors. The MOONSHOT (one seam-independent patrol) survives
contact: the estate already runs patrol-shaped surfaces, and the probe's new code is the
heartbeat append, not another detector.

### Finding 4 (gap 5, fold-phase serialization): CONFIRMED (WATCH verdict sound)
Commit 55cdaaa4f verified real (FOLD GATE FLEET-WIDE: cross-run fold mutex, holder-string
identity, 45-min stale-break, JSONL audit); DAWN_REPORT_20261006.md:50-51 confirmed;
NIGHT_BURN_DESIGN_20261007.md:41-42 (FOLD-FAST routes contended fold prose to the local
janitor) confirmed; tools/fold_prose_local.py:12-31 carries the hard laws (literal
127.0.0.1:11434, verbatim sections, one-shot bounded timeout, never half-write, exit-3
cloud fallback). Temporal verified (MIT, active, `temporal server start-dev`). WATCH is
the right verdict: the mutex is by-design serialization, the hang class is locally cured;
steal only worker-heartbeat semantics, which fold_prose_local genuinely lacks.

### Finding 5 (gap 6, law-pack day-lag): CONFIRMED (WATCH verdict sound)
MagLawPackDaily verified live: Enabled, Ready, Last Result 0, daily 09:30 (byte-matches
d01:20-24); DAWN_REPORT_20261006.md:203-207 confirmed ("the four-law grep now reads 2 of
12 flash rows, was 0 of 12"); VAULT_RIBS omission confirmed at mag/rib_boot.py:90-98.
Same two render bugs as gap 1, correctly diagnosed; no external steal needed for a
single-receiver estate. WATCH stands.

### Finding 6 (the asks): CONFIRMED, lens's OWED flags stand
Herald-OS README verified: four-tier gate (read/act run immediately and logged; mutate
asks per-session or always; destructive asks every time; ~/.ssh, keychains, own
credentials always refused), MIT, audit at ~/.hermes/herald-os/audit.jsonl, and usage is
a provider-plan panel with a 90 percent warning, which confirms the lens's CORRECTION
(permission tiers, not token tiers). Gate CODE remains unread: the lens's OWED stands
before any code-level steal. TON docker README verified verbatim: "The TON node, whether
it is validator or fullnode, requires a public IP address" plus the NAT/k8s ports
requirement, so the tailnet-only caveat holds and lite-server client mode is the honest
node-lite shape. exo verified: Apache-2.0, "Currently, exo runs on CPU on Linux", no
Android documented (README covers macOS/Linux only), topology-aware model splitting with
OpenAI/Claude/Ollama-compatible endpoints. BLIND-SPOT CLOSED (partial): cr-sqlite
releases feed shows v0.16.3 (Jan 17), v0.16.2 (Jan 6), v0.16.1/v0.16.0 (Dec 16), 48 open
issues, 8 open PRs: the dependency is alive as of that page snapshot; the year of the
Jan 17 tag is inferred, not byte-proven, so downgrade "unknown health" to "alive as of
January, no commit-date byte". Helicone, Ray, k3s, TUF, Nomad: NOT re-verified this
sitting, still OWED. The lens's 724 MB aborted-probe log: NOT investigated by me either,
still OWED.

## Additions (what the lens missed)

1. SHARED STASH REFSPACE (empirical, this sitting). refs/stash is a common-dir ref:
   stash list is cross-worktree and a cross-worktree pop silently applies and drops
   another seat's held work (test D/E in instruments). Evidence: the throwaway-repo
   transcript above; `git -C "$B/main" stash list` showing "On wtB: wtB-stash" and
   "Dropped refs/stash@{0}" after pop in main. Falsifier: if a repo configured with
   per-worktree refs (git config extensions.worktreeConfig + ref relocation) shows
   isolated stash lists, the shared-refspace mechanism claim is wrong for that config.
   Move: 30 min. Extend stash_sweep_watch with a census-decrease alert (a pop/drop
   happened somewhere) plus the charter clause "never pop a stash minted outside this
   worktree"; fix the root-tree mtime intersection for non-main worktree stashes.
2. STAGE-4 HARD CLIP IS A SECOND AMPUTATION POINT. The lens's falsifier guessed at
   independent suppressors; my 13:30:11Z render measured one more: after all 3 stage-3
   sheds the pack was still 7758 > 7200 and the tail got clipped. Evidence: PACK_OFFLOAD
   rows at 13:30:11.352179Z ("hard clip", stage 4, 7758). Falsifier: a fresh render with
   L0d exempted and no budget headroom, on a >=13000-char overflow day, still greps
   MEASURED ON 0; if it greps non-zero, the clip never reaches the amendments block and
   this addition is wrong. Move: 15 min. After the two edits, run the acceptance render
   at the heavy shape (13695-char day), not the light shape (7571), or add budget
   headroom so the clip line sits below the amendments block in the layout order.
3. LAW-BYTE RESIDENCE MAP (determines which acceptance targets are reachable).
   MEASURED ON lives in two MOUNTED ribs (RIB_MODEL_GATES 2 hits, RIB_INFERENCE_BUDGET
   1 hit); Sybil lives ONLY in the unmounted RIB_MOSAIC_SEED_20260921.md (2 hits);
   max_concurrency lives in NO rib (0 hits in RIB_FREE_USAGE_POLICY). Evidence: the grep
   census in instruments 3. Consequence: the gap-1 acceptance "MEASURED ON non-zero" is
   reachable with the flash-cap fix alone; "Sybil non-zero" additionally needs the
   VAULT_RIBS edit; "max_concurrency non-zero" additionally needs a minted rib, which is
   an operator decision (d01:50), not a bug fix. Falsifier: any of these greps finding
   the token in a different file class (e.g. Sybil in a mounted rib) breaks the map.
   Move: 10 min. Sequence the acceptance as four separate gates (flash-cap -> L0d
   survival -> VAULT_RIBS mount -> max_concurrency mint decision) so a green test cannot
   hide an unmounted law family behind a single token.

## Not run / carried OWED

- pytest suite not run (no code changed this sitting; break pass is read-and-measure).
- The 724 MB background log from the lens's aborted probe: not located, not read.
- Nomad/Helicone/Ray/k3s/TUF, LiteLLM soft-alert + exact exception name, Herald-OS gate
  code, Herald-OS bridge plugin source: unchanged OWED.
- cr-sqlite commit-date byte: releases feed read, exact recency still soft.

No em-dashes. Every claim above names its instrument; counts name scope (whole-file
grep over memory/context_pack_latest.md, 7394 bytes, post-render).
