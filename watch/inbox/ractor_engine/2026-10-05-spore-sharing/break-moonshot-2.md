# BREAK moonshot-2 (hostile second pass) - SPORE SHARING - 2026-10-05

Breaker: break-moonshot-2 subagent. Every cite below was re-run or re-read this
sitting, repo root C:\Users\foste\Documents\projects\local_sovereign_agent,
git bash on win32, HEAD = mag/run-beta1-factory-build-audi-20260806T231709Z.
Tree moved under me: lens counted 56,359 tracked / 17,069 inbox; I count
56,361 / 17,070 (same-day sibling landings; census law: name the moment).

## Instruments run this sitting

git check-ignore -v; git ls-files (+ counts); git branch -r / remote -v;
git log / rev-list / merge-base / diff-tree / cat-file -p; git count-objects -vH;
git fetch github master; git cat-file --batch-all-objects --batch-check;
git rev-list --objects HEAD (91,202 objects) + grep reachability;
git archive HEAD <path> | tar -t; git grep (HEAD and disk); a full local
git clone to /tmp/spore_fresh_clone (completed, then deleted); WebFetch of
github.com/NachoBusiness17/mycelial-republic and the GitHub API (repo,
branches, commits); reads of mag/route_chat.py, .gitignore, tools/gps_mcp/
ledger.py, tools/gps_mcp/metabolism.py, state/CURRENT.md,
memory/rib_bus/doctrine.json, configs/providers.yaml, .env.example,
watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md, mag/gwap_payload.py.

## Verdicts

### F1 "The spore cannot sprout as wired" - CONFIRMED

Byte-checks, all pass:
- `git check-ignore -v state/GENOME.md` -> `.gitignore:40:state/` (rule is
  .gitignore:40, reinforced by :41 `state/**/*`).
- `git ls-files state/` -> only state/NIGHT_LOOP_20261005.md.
- `git ls-files configs/` has no providers.yaml template (grep provider/env/
  example: only configs/browser_env.yaml, configs/env_tracks.yaml, a
  workflow_gate fixture). configs/providers.yaml exists on disk (40,724 B),
  ignored at .gitignore:24.
- mag/route_chat.py:49-53 exact: `_load_lanes` reads
  configs/providers.yaml via `read_text` at route_chat.py:51 at call time.
- watch/inbox/RESEARCH_SUMMARY_arena_days_one_two_20261005.md:158 exact:
  "state/GENOME.md. queue/STANDING_RAILS.md. The 26 doctrine ribs." (genome
  named first in THE INHERITANCE).

Falsifier upgrade (the lens skipped it; I ran it): full local clone
`git clone -q "$(pwd)" /tmp/spore_fresh_clone` completed. The clone's
state/ contains only NIGHT_LOOP_20261005.md; configs/providers.yaml absent;
.env absent; .env.example present; 56,361 files. `git archive HEAD state`
and `git archive HEAD configs` agree (archive content = checkout content).
route_chat('smoke') itself was NOT executed (would risk real paid calls and
needs venv wiring into the clone; reported as not run). The fail chain is
static and unhandled: route_chat.py:51 raises FileNotFoundError on the
missing lane table; with a lane table present, route_chat.py:67 reads
ROOT/.env unconditionally per missing env var, so the missing .env is a
second unhandled raise.

Refinement the lens missed: .env.example IS tracked (.gitignore:22
`!.env.example`) and ships in the clone, but it is stale against the lane
table: providers.yaml reads ~40 env names across 27 lanes; .env.example
carries 12 names and none of ZAI_API_KEY / ZAI_API_KEY_Pro /
ZAI_API_KEY_Lite, HERMES_API_KEY_1/2 (providers.yaml:158,238-239),
DEEPSEEK_SWARM_API_KEY (:366), GROQ_API_KEY_2 (:304),
OPENROUTER_API_KEY_2 / OR_API_KEY / OR_API_KEY_2 (:178).

### F2 "56,359-file publication event; one-commit orphan github/master" - CONFIRMED, two corrections

Byte-checks that pass: remote github = https://github.com/NachoBusiness17/
mycelial-republic.git (git remote -v; the lens assumed this, now verified).
github/master tip dc6649943, 2026-08-20. `git rev-list --count
github/master..HEAD` = 879. gps_ledger.db3 tracked (blob 782,336 B) plus
gps_ledger.db3.bak_pre_D2_20260930 (32,768 B); tools/gps_mcp/receipts.jsonl
tracked. Lane runtime tracked: 11 lanes carry runner_state.json/trail.jsonl;
6 are tracked-modified right now (git status). Rib bus carries operator
local paths: memory/rib_bus/doctrine.json:53 embeds
`C:\Users\foste\Documents\projects\local_sover`.

CORRECTION 1 (sub-claim killed): "one-commit orphan" is a shallow-clone
artifact, not an orphan. `git rev-parse --is-shallow-repository` -> true;
.git/shallow contains dc6649943; `git cat-file -p dc6649943` shows
`parent 3da416c12...`. The GitHub API shows master = 13 commits rooted at
b2c3fd3e5 (2026-08-04, initial commit), one branch, pushed_at
2026-08-20T15:29:04Z, repo size 644 KB. What survives: merge-base
github/master HEAD fails (RC=1, genuinely unrelated histories) and the
879-ahead count stands. Lesson: check is-shallow-repository before
characterizing remote history by local count.

CORRECTION 2 (sharpens the finding): the push is impossible, not merely
heavy. `git cat-file --batch-all-objects --batch-check` + `git rev-list
--objects HEAD` (91,202 objects reachable) shows SIX reachable blobs of
1.24 to 2.36 GB: dashboard/data/ESTATE_INDEX.jsonl (2.35 GB, 1.95 GB,
1.24 GB versions), attic/20260923_mimosa_rotation/
hook-state_stale_baselines.tar (2.36 GB and 2.31 GB versions),
dashboard/data/ractor_board.jsonl.runaway-evidence-20260903 (2.23 GB).
GitHub hard-rejects any file over 100 MB at pre-receive, so `git push` of
this history fails regardless of --force. The estate cannot leak by
accident; only a purpose-built publish (new orphan history, curated tree)
lands a spore. Local pack is 14.37 GiB with 4 garbage tmp_pack files and
12,794 loose objects (git count-objects -vH).

### F3 "N=2 breaks on the ledgers, not the code" - CONFIRMED

- tools/gps_mcp/ledger.py:466-470 verbatim: the SELECT "can pass in two
  processes feeding the same triple at the same moment (hourly arena cron
  plus a manual backfill); the partial UNIQUE index is the enforcement
  layer". That is a same-machine, same-repo race backstop; two clones
  pushing the tracked binary (gps_ledger.db3) still last-writer-wins. The
  lens cited :468-470; the sentence spans :466-470.
- memory/rib_bus/doctrine.json: single JSON object, 163 lines, 26 ribs
  (`grep -c invariant` = 26, which independently matches the topic's and
  RESEARCH_SUMMARY:158's "26 doctrine ribs"), rows
  {invariant, source, ts, target_rank} (+first_ts on 2 rows), NO owner or
  claim field. The lens's :1-14 cite is a partial range of a 163-line file;
  the claim holds of the whole file. Note: the rib bus is 51 tracked files
  under memory/rib_bus/, not one file.
- Tracked lane runtime: `git ls-files queue/lanes` shows runner_state.json +
  trail.jsonl for 11 lanes; 6 tracked-modified at my moment.

Additions that strengthen it: the "season ledger" organ the topic names and
the lens never checked is mag/gwap_payload.py:679-687 (SessionLedger):
rows are keyed ("seq", "ts_utc", "payload", "prev_sha256") at :683-684 with
no seat/owner field, so the one-party assumption is byte-supported at the
class level. `git grep -nE "seat_id|owner|operator"` over tools/gps_mcp/
router.py and ledger.py returns prose mentions only, no multi-operator
concept anywhere in the routing surface.

### F4 "The .env door is single-tenant by construction" - CONFIRMED

- mag/route_chat.py:56-72 exact: `_keys_for` reads os.environ then ROOT/.env
  only; no seat, no per-tenant namespace.
- state/CURRENT.md:87: "cage .env mount-or-env-door (march stays rc=2 skip
  until then)" verified in the Owed block (lines 86-89).
- tools/gps_mcp/metabolism.py:98-109 exact: reset_epoch is an "Explicit act
  by design" by "a seat or the patrol operator"; EPOCH_PATH =
  tools/gps_mcp/metabolism_epoch.json (:44), a local file, per-seat by
  construction.
- Usage banking has no attribution axis either: route_chat banks to
  memory/runs/route_chat/usage.jsonl (route_chat.py:22,46), gitignored via
  .gitignore:102.
- The finding's move text arrived truncated in the copy I was given; the
  verdict rests on the stated claims only.

## Additions (what the lens missed)

1. The push is mechanically impossible. Evidence: batch-all-objects +
   rev-list --objects HEAD reachability, six blobs 1.24-2.36 GB reachable
   (paths in F2 correction 2). Falsifier: a successful `git push github
   HEAD:master` of this history, or any of those blobs served from the
   public repo. Move: the public builder must commit a NEW orphan history
   from a curated tree (git archive -> fresh repo), never push refs; base
   it on scripts/build_travel_kit.py (exists and is tracked), one sitting.

2. A live secret rides history. Evidence: lan.key blob f5e6dea5 appears in
   `git rev-list --objects HEAD` output as memory/tls/lan.key; added in
   799ddb6fe (diff-tree status A; 799ddb6fe is an ancestor of HEAD), deleted
   in add33ba72 (status D). .gitignore:271 itself says "rotate - it remains
   in history". Falsifier: `git rev-list --objects HEAD | grep f5e6dea5`
   returning nothing. Move: rotate the key per the estate's own comment and
   make any publish profile orphan-history so the blob is unreachable;
   rotate ~15 min, the builder design carries the rest.

3. The public repo is a distinct product, not a stale mirror of this
   estate. Evidence: WebFetch + API: 13 commits, 644 KB, MIT, README "A
   living, forkable decentralized intelligence layer", Phase 0 Seed Mirror,
   tree = mycelia.cmd/mycelia.ps1/scaffolds/src/mycelial_republic (matches
   `git ls-tree --name-only github/master`). A --force push would replace a
   shipped product (and would die on the 100 MB blobs first anyway).
   Falsifier: the API listing estate content on master. Move: operator
   decides replace-vs-new-repo; `git fetch github --unshallow` first so no
   seat reasons from the clipped view; ~10 min.

4. The inheritance organ census, all six organs. Evidence: state/GENOME.md
   ignored (.gitignore:40-41); force-add precedent exists (state/
   NIGHT_LOOP_20261005.md added by 139f5198f under the same rule,
   `git check-ignore -v --no-index` shows .gitignore:40 matches);
   queue/STANDING_RAILS.md tracked; 26/26 doctrine ribs tracked;
   corpus/steal has 61 tracked files (the inheritance's "10 corpus steals"
   set does not resolve to a named 10: OWED); season ledger = SessionLedger
   class above (data file not located: OWED); Delta Register candidate
   watch/inbox/frontier_delta_register_20261003.json tracked. Also: the
   spore machinery the regrow guide should reuse already exists:
   docs/ref/SPORE_CONTINUITY_SCHEMA.md:17-24 defines
   generate_spore_seed(seat_id, timestamp, root_hash) with append-only
   memory/spore_seeds/{seat_id}.jsonl; mag/worldline_dungeon.py:328-343
   defines the five hashed slabs (GENOME, INVARIANTS, ORGANS, RECORD,
   POSITION); docs/ref/SPORES.md tracked. Falsifier: any organ's tracked
   status flips under `git ls-files <path>`. Move: write the regrow guide
   on top of spore_seeds + slabs + build_travel_kit instead of inventing a
   fourth sharing mechanism; one sitting.

5. Tracked-tree secret triage is not clean (scoped census, instrument
   named: `git grep -I` at HEAD, two regexes). Evidence: key-shaped string
   in HEAD:watch/inbox/burn_wave_20260926/B2_88_crawl_map.json
   ("sk-EGKn8d...", prefix only); env-assignment-shaped strings in 8
   tracked files incl watch/inbox/frontier_olm_2026-10-04/sweep/
   _amc_harvest_LocalLLM.jsonl and sw2_full.jsonl (tracked despite the
   2026-10-01 never-track warning at .gitignore:268-269); LINKS.jsonl hits
   are word fragments ("sk-specif", "sk-succes"), false positives. NOT
   claimed as live secrets; triage OWED. Falsifier: the estate secret gate
   (tools/precommit_secret_check.py) run over the 9 named files comes back
   clean. Move: run the secret gate on the named files, ~20 min.

6. The tutorial's exact wiring is now verifiable and .env.example cannot
   carry it. Evidence: z_ai lanes verified in configs/providers.yaml:
   z_ai:541 ZAI_API_KEY, z_ai2:553 ZAI_API_KEY_Pro, z_ai3:575
   ZAI_API_KEY_Lite with `dormant: true` (:571) and LITE_LANE_ACTIVE=1
   re-arm (:568) and an operator-personal comment (:565-566, names "adam"),
   z_ai4:585; fence is code-side (mag/route_chat.py:75-88 from lane
   base_url) plus .gitignore-side defaults (providers.yaml:9
   never_remote_tiers), no per-lane fence entries. .env.example is stale
   (F1 refinement). Falsifier: .env.example's 12 names cover every
   api_key_env(s) in the 27-lane table. Move: generate .env.example and a
   configs/providers.yaml.example FROM the live lane table with values
   stripped, ~40 min.

## Blind-spot cures

1. providers.yaml lane entries: CURED (addition 6; lane names verified as
   fields, not just keys; z.ai env names verified).
2. F1 falsifier: RUN at file level by me (clone); the model-call step not
   executed (paid-call and env risk), stated as not run.
3. Public repo surface: CURED (WebFetch + API + `git fetch github master`).
4. Secret re-scan of tracked inbox: PARTIALLY CURED (scoped git grep
   census, addition 5; not a full secret-gate run).
5. schtasks vs register_* census: NOT ATTEMPTED this pass. Still OWED.
6. Vendor pricing: NOT VERIFIED this pass. Still OWED.
7. .gitignore:30-34 contradiction: RESOLVED. The comment names
   memory/trajectory/steps.jsonl as the carrier of the 7 committed .env
   values. `git log --all --oneline -- .env` is EMPTY and
   `git log --all --oneline -- memory/trajectory/steps.jsonl` is EMPTY:
   no commit in any current ref touches either path, so the 7 values are
   in no pushable history (the "history left intact" note means on-disk
   objects, unreachable). The push-relevant history secret is lan.key
   (addition 2), a different vector.

## OWED (not done, not asserted)

- route_chat('smoke') executed inside the fresh clone.
- The "10 corpus steals" resolved to a named set (61 tracked files under
  corpus/steal/).
- Season ledger data-file path (class + SEASON_design.md:87-101 cited via
  watch/inbox/replay_flash/MOCAP_BUILD_spec.md:247 only).
- schtasks inventory vs the 13 register_* scripts.
- Current vendor prices for the tutorial math.
- Secret-gate verdict on the 9 files named in addition 5.
