# BREAK-MOONSHOT-2: hostile second pass on the external-steal lens (moonshot-2)

- Breaker: break-moonshot-2, 2026-10-07. Target: `watch/inbox/ractor_engine/2026-10-07-external-steal/moonshot-2.md` (read in full; the JSON handed to this seat was truncated mid-finding-4, so verdicts below ride the banked write-up as the finding of record).
- Method: every estate cite re-read at path:line; the lens's greps re-run at its own scope; the two checks the lens declared skipped (acceptance pytest, mag.cmd context-pack) EXECUTED this sitting; finding 1's falsifier EXECUTED as a live worktree probe (created, tested, removed, estate state hash-verified intact after); the five external quotes re-fetched at source.
- Score: 2 CONFIRMED (spine, gap 3), 2 WEAKENED (gap 2 runner-up, gap 1), 0 KILLED. Five additions the lens missed, two of them change the moves.

## Verdict 1: gap 2 runner-up, "worktree isolation is already vendored and switched off" - WEAKENED

Byte-checked and holds:
- mag/env_registry.py:60-66 `resolve_worktree_path`, :64 the `MAG_MULTI_WORKTREE == "1"` opt-in, :108 `def ensure_worktree`, :211 `"multi_worktree": os.environ.get("MAG_MULTI_WORKTREE") == "1"` in status_summary. All four cites byte-true (Read this sitting).
- git-scm.com/docs/git-worktree quote is verbatim at source (WebFetch this sitting): "The new worktree is linked to the current repository, sharing everything except per-worktree files such as HEAD, index, etc." plus REFS: "one example is HEAD, which is different for each worktree".
- tools/stash_sweep_watch.py:2-24 docstring names the R5-named incident (r3_land_teeth.md:92-105) and its census hashes match the live repo: `git rev-parse stash@{0} stash@{1} stash@{2}` = 8b45fe97…, 2902e0d3…, 8baa166e…, exactly the three HOLD-RECONCILE stashes the docstring records.

Byte-broken:
- "ONE shared root checkout for all seats" is false as a universal: `git worktree list` shows FIVE worktrees (root + Temp/gate_canary_4z9wiml0 + Temp/recovery_pack/baseline + lsa_reboot_staging + worktrees/salon-arena-mvp, the last carrying branch codex/salon-arena-mvp). The write-up's "plus 3 unrelated worktrees" miscounts (4). The defensible claim: no seat LANE rides a worktree today; the 3 sweep stashes sit on the root branch.
- "Switched off" is imprecise: configs/env_tracks.yaml:7 and :39 configure `worktree_path` on two of five tracks (operational → mag_test_env, dashboard-v3 → mag_env_dashboard_v3); neither directory exists on disk (`ls ../mag_test_env ../mag_env_dashboard_v3` → No such file or directory). The machinery is also wired, not dead code: sync_track:143 calls ensure_worktree, activate_track:178 calls sync_track, and callers exist at main.py:5348 (env CLI), scripts/env_switch.ps1:105, mag/coding_session_runner.py:157, mag/factory_machine.py:87.

Falsifier EXECUTED this sitting (the lens asserted it from docs; here it ran):
- `git worktree add --detach %TEMP%\lsm2_probe_wt HEAD`, then dirtied an untracked file inside it. Root `git status --porcelain | grep lsm2` → NOT VISIBLE; `git -C <worktree> status --porcelain` → `?? lsm2_probe_dirty.txt`. A root-tree stash cannot sweep what root status cannot list: the R3 capture class is structurally impossible across worktrees, confirmed on git 2.55.0.windows.2.
- NEW hazard the lens missed: stash refs are SHARED across worktrees on this git. `git -C <worktree> stash push -u -m "lsm2 probe stash"` incremented the ROOT's stash list 3 → 4 (root `stash@{0}: On (no branch): lsm2 probe stash`). Any worktree seat can drop or pop the root's 3 HOLD-RECONCILE stashes. The worktree flip cures the capture class only; the ref class survives it.
- Cleanup verified: probe stash dropped (5ffa541a), worktree removed, `git stash list` back to 3 with hashes byte-identical to pre-probe, `git worktree list` back to 5.

Why WEAKENED, not CONFIRMED: the move's reach is overstated. mag/lane_runner.py (the queue-lane runner_state consumer, the fleet that actually collided in R3) has no env_registry import at all (`grep -n "env_registry" mag/lane_runner.py` → zero hits). "Set worktree_path on ONE seat track" cures the env-track seats only; the lane fleet needs one more wiring hop the lens did not name, and that is a second sitting, not 45 minutes.

## Verdict 2: spine, "healthchecks retires the silent-failure class wholesale" - CONFIRMED

Byte-checked and holds:
- github.com/healthchecks/healthchecks re-fetched this sitting: BSD 3-clause confirmed; the lens's quotes are verbatim ("It listens for HTTP requests and email messages ("pings") from your cron jobs and scheduled tasks", "When a ping does not arrive on time, Healthchecks sends out alerts.", "Each check has configurable Period and Grace Time parameters.", "A Dockerfile and pre-built Docker images are available.").
- scripts/lawpack_daily.ps1:24 verbatim: "exits nonzero so schtasks Last Result carries it".
- The lens's grep reproduced exactly at its stated scope: `grep -n "20432\|20578" watch/inbox/*.md memory/attention.md` → one hit, watch/inbox/BURN_steering-theory_20260925_b.md:29 (alphaxiv 2512.20578, unrelated). Wider sweeps (recursive watch/inbox, and `20,432|20,578` over watch/inbox/*.md state/*.md memory/*.md) add nothing: the storm receipt does not exist on any of those surfaces. Named instrument: those greps, this sitting. The numbers ride the ask; watch/inbox/FULL_SCAN_REPORT_20260923.md is a different scanner (semantic catalog churn, run 2026-10-06, 315 records) and contains no 429/20432/20578/disable text.
- All four task names in the move are live: `schtasks //Query //FO CSV` shows MagLawPackDaily, MagHermesBurn247, MagCensusPatrolDaily, MagFtsIndexDaily, all Ready.

Additions that strengthen the spine:
- `\Estate FullScan` shows `"N/A","Disabled"` in the same task census, while state/REDBOARD.md:21 reads "Estate FullScan=ok" inside its "Not red (18)" line. The estate's own patrol surface reads a disabled task as green TODAY. That is the disease live in the patrol, and it is a second instance the witness underlay covers (a disabled task stops pinging; silence pages).
- The census is roughly 19 Ready estate tasks, not 4 (also Ready: MagBootRegenDaily, MagBoxBurnNightly, MagCorpusRescanDaily, MagEndpointNewsDaily, MagFreeLaneFleet, MagGapSentinelDaily, MagGateCanaryDaily, MagGauntletFree30, MagImproveDaily, MagLeaveProtocolDaily, MagLongrunnerPatrolDaily, MagQCaptionVerifyDaily, MagSecretScanWeekly, MagTipWitnessDaily, MagVisionNightly, MagXRadarDaily, mag-docker-watchdog). The move's coverage is five times its list at the same 3-line ping per wrapper.

Falsifier intact and honestly stated (same-desktop witness shares host blast radius). NOT RUN: any bob-side or SaaS deployment check; this seat cannot verify bob's state.

## Verdict 3: gap 1, "STEAL Letta pinned blocks; reprioritize L0d above L1b/L1c" - WEAKENED (the steal direction holds; the named move is falsified by execution)

Byte-checked and holds:
- d01 receipt (memory/runs/mickey17_v2/runs/dogfood2-20261007/lanes/d01-seat-boot-pack.json:6) verbatim carries 9471 > 7200, zero law hits, and the 1 failed / 41 passed gate read.
- The gate re-ran BY ME this sitting: `.venv/Scripts/python.exe -m pytest -q tests/test_context_pack_quantized_laws.py tests/test_rib_boot_amendments.py tests/test_boot_regen.py tests/test_thought_quantizer.py` → **1 failed, 41 passed in 11.18s**, same failing test_quantized_laws_section_renders_in_default_budget, same AssertionError "no known compiled law rode the pack", rendered tail "…(pack clipped)". (A first attempt returned 42 errors in 5.40s, transient; the clean second run is the canonical read.)
- mag.cmd context-pack re-ran BY ME at 2026-10-07T14:20:19Z: memory/context_pack_latest.md greps = MEASURED ON 0, Sybil 0, max_concurrency 0, POST-DATUM 3 (the truncated flash header lines), "pack clipped" 1. watch/inbox/PACK_OFFLOAD.jsonl tail rows: L2 trail shed at 13695 → L0d rib vault amendments shed at 9404 → L1 bonds shed at 7758 → hard clip (stage 4, 7758 > 7200). CONVERGENT with d01 (08:29Z, 9471) six hours later: still shedding, still clipped.
- External re-fetches: docs.letta.com/guides/agents/memory-blocks verbatim "always visible - no retrieval needed", per-block character limits, read_only field, shareable across agents. github.com/microsoft/LLMLingua: MIT, lossy token dropping, `<llmlingua, compress=False>` + force_tokens, latest news 24/12/13. The lens's external bytes all stand.

Byte-broken:
- Citation off-by-ones: FLASH_MAX_CHARS = 220 is tools/thought_quantizer.py:118, not :117 (:117 is FRAGMENT_MIN_CHARS = 25). VAULT_RIBS spans mag/rib_boot.py:90-98, not :91-99 (:99 is LAW_HEAD_CHARS = 1200).
- THE MOVE IS A NO-OP: mag/context_pack.py:1486-1503 already sheds "L1b/L1c skills + ijl + mirror/clue" at position 10 and "L0d rib vault amendments" at position 11 of shed_order; earlier in the list sheds sooner, so the vault amendments are ALREADY more protected than skills, per the R4-L2 comment at :1498-1500. "Reprioritize L0d above L1b/L1c" is already the code's state.
- DEEPER (my addition): the offload ladder shows the unsheddable floor busts the ceiling. After the LAST sheddable block (L1 bonds) drops, the pack is still 7758 > 7200 (max_chars, mag/context_pack.py:165) and stage-4 clip fires. No shed-order permutation can put a law byte into the pack while the core alone exceeds the budget. The real cures are the d01 row-3 alternates the lens dropped: raise the full-mode budget, shrink the vault block at the compiler (the 220-char flash cut at tools/thought_quantizer.py:118), or pin the vault block into the unsheddable core (the Letta pattern applied for real). Executing the lens's probe as written would burn the one sitting and stay red on its own acceptance.

## Verdict 4: gap 3, "WATCH the products; the estate is ahead; spend_balance pre-flight is the remaining cure" - CONFIRMED

Byte-checked and holds:
- watch/inbox/hermes_burn/HERMES_402_WALL_20261007.md: probe ladder bounded key-2 balance [0.16, 0.17) (:34), all 8 candidate balance endpoints 404 on both keys (:22-25), TERMINAL rails + cost_rollup spend_balance.v1 landed ("What landed" items 1-2).
- tools/cost_rollup.py:22-23 (spend_balance.v1 writer doc), :59 (SURFACE_HERMES_BURN), :62 (SPEND_BALANCE_RELPATH) all byte-true.
- github.com/BerriAI/litellm README re-fetched this sitting: the lens's README-level quotes are present ("virtual keys, spend tracking, guardrails, load balancing", "multi-tenant cost tracking and spend management per project/user"), and the README contains the word "budget" NOWHERE and says nothing about exceed-to-429 behavior. The lens's OWED flag was exactly right and its WATCH verdict survives my fetch.

NOT RUN: the pre-flight move (spend_balance.v1 as a paid-lane input) is prose; nothing landed to byte-check. tests/test_spend_balance_v1.py exists untracked; the 402-wall receipt's 61-passed claim was not re-executed this sitting.

## Blind-spot adjudication (the lens's six)

1. Herald gate code unread: stands, still OWED; I did not read the external plugin code either (outside estate reach this sitting).
2. LiteLLM exceed-to-429: my fetch confirms the README carries no budget-exceed behavior at all; still OWED, correctly flagged.
3. TON/gstd + Ollama composite absence: unresolved; I made no web-search attempts this sitting, so the re-census is still owed before anyone asserts "no prior art".
4. Acceptance test + context-pack not re-run: CURED by this pass; both re-executed, d01 reproduced byte-for-byte in shape (1 failed / 41 passed; shed ladder + hard clip + zero law greps).
5. FullScan receipt unlocated: confirmed absent from watch/inbox top level, state/*.md, memory/*.md (instruments named above); the only estate-side byte added is the schtasks Disabled state.
6. Mechanism-class-only dispositions (rerankers, k3s, Ray, Temporal, Prefect, Helicone, flock, OT/CRDT): stand as OWED; not byte-checked here either.

## What NOT to do (carried and sharpened)

- Do not run the lens's L0d reorder probe: it is a no-op against mag/context_pack.py:1486-1503 and cannot pass its acceptance while the unsheddable floor is 7758 > 7200.
- Do not claim the worktree flip retires stash_sweep_watch.py: stash refs are shared across worktrees on git 2.55.0.windows.2, so the ref-space hazard (any seat dropping or popping the 3 HOLD stashes) survives the flip; the detector demotes to tripwire for the capture class only.

## OWED (carried forward, by surface)

- LiteLLM exceed-to-429 mechanism (needs a docs fetch with working search).
- Herald gate code read (plugins/herald-os-bridge).
- TON/gstd + Ollama composite prior-art re-census (needs working web search).
- Byte checks for the mechanism-class candidates (rerankers, k3s, Ray, Temporal, Prefect, Helicone, flock, OT/CRDT).
- The storm receipt: 20432/20578 has no estate-side receipt on any surface this seat grepped; whoever disabled Estate FullScan should bank one.
- Lane-fleet worktree wiring design (mag/lane_runner.py has no track-root path; the R3 parties are not env-track seats).

RECEIPT: this sitting executed two pytest runs (one transient-errored, one canonical 1 failed / 41 passed in 11.18s), one live mag.cmd context-pack render (14:20:19Z, offload rows banked in watch/inbox/PACK_OFFLOAD.jsonl), the lens's grep at its scope plus two wider sweeps, a full schtasks census, one worktree isolation probe with full cleanup (estate stash hashes and worktree count verified unchanged after), and five external re-fetches. No repo files were edited; the probe artifacts were removed.
