# MOONSHOT-2: THE SPORE SHARING PROBLEM (2026-10-05)

Lens: moonshot. No sacred cows: the single-operator assumption, the .env model,
GitHub-as-surface, and shareability itself all went under the knife. Every
claim below was checked this sitting; the exact command is named. Anything I
could not verify is marked OWED.

## 0. THE ONE-LINE VERDICT

The estate already built its spore (`scripts/build_travel_kit.py`) and already
minted its multi-seat identity format (`memory/spore_seeds/`), but the GitHub
push as imagined would publish 56,359 tracked files including live ledgers and
the receipt corpus while carrying neither the genome (`state/` is git-ignored)
nor the lane table (`configs/providers.yaml` is git-ignored, no template). The
spore pouch exists; nobody has loaded it.

## 1. WHAT I CHECKED (instruments, this sitting)

- `git remote -v` -> `github` = https://github.com/NachoBusiness17/mycelial-republic.git
- `git branch -r` -> only `github/master`; `git log github/master -1` ->
  dc6649943 (2026-08-20), a ONE-commit orphan;
  `git rev-list --count github/master..HEAD` -> 879
- `git ls-files | wc -l` -> 56,359; `git ls-files watch/inbox/ | wc -l` ->
  17,069; `git ls-files watch/inbox/playground/ | wc -l` -> 564 (the season
  transcripts, tracked); `git ls-files memory/rib/ | wc -l` -> 55
- `git check-ignore -v state/GENOME.md state/CURRENT.md` -> both hit
  `.gitignore:40` (`state/`); the ONLY tracked file under `state/` is
  state/NIGHT_LOOP_20261005.md
- `git ls-files configs/` -> no providers.yaml template of any kind
  (providers.yaml and its .bak exist on disk only)
- `git ls-tree github/master --name-only -- configs/providers.yaml
  deploy/k8s/mag-secret.yaml .env` -> EMPTY (public tip carries none of them);
  `git merge-base --is-ancestor` for the untrack commit 5a6ffd806 AND for both
  adder commits (cd2f8e6a5 2026-08-01, eb07ad62e 2026-08-04) vs github/master
  -> all NOT ancestors. The public surface is clean TODAY; the next push
  decides what the world gets.
- mag/route_chat.py:49-53 (`_load_lanes` reads configs/providers.yaml),
  :56-72 (`_keys_for` reads os.environ, then falls back to the ONE ROOT/.env)
- tools/gps_mcp/gps_ledger.db3 IS tracked (plus .bak_pre_D2_20260930);
  ledger.py:468-470 names the concurrency defense: "hourly arena cron plus a
  manual backfill" (same-machine only); metabolism.py:44 epoch marker lives at
  tools/gps_mcp/metabolism_epoch.json (not yet stamped, per
  watch/inbox/D7_PHEROMONE_METABOLISM_20261005.md lines 49-59)
- memory/rib_bus/doctrine.json (20,363 B, tracked): single JSON object keyed
  by rib hash, rows carry {invariant, source, ts, target_rank} and NO
  owner/claim/lease field; row `c3d19a4f99a32be7` carries the operator's
  local path (`C:\Users\foste\...`, doctrine.json:53)
- `MSYS_NO_PATHCONV=1 schtasks /query /fo csv | grep -i mag` -> 17 Mag tasks
  machine-local (MagImproveDaily, MagCensusPatrolDaily, MagFtsIndexDaily,
  MagFreeLaneFleet, MagSecretScanWeekly, ...). MagFreeLaneFleet runs
  scripts/free_lane_fleet_cycle.ps1, which hardcodes `C:\Users\foste\...`
  absolute paths (lines 4-6, the ABSOLUTE PATH LAW); a `register_*` script
  exists for ~13 tasks but NOT for free_lane_fleet (checked the scripts/
  listing)
- `git rev-list --all --count -- memory/trajectory/steps.jsonl` -> 0, which
  CONTRADICTS the .gitignore:30-34 comment claiming 7 live .env values were
  committed in that file. Discrepancy recorded, neither side asserted as
  truth (OWED: either the history was GC'd/rebased against the comment's
  "history left intact", or the path in the comment is wrong)
- git status shows `queue/lanes/{builder,day_work,research}/runner_state.json`
  and `trail.jsonl` as MODIFIED TRACKED files: runtime lane state lives in
  git
- memory/spore_seeds/ IS tracked: rows {timestamp, seed, seat_id, root_hash};
  seat_ids `zcode` and `testseat` already banked
- scripts/build_travel_kit.py: docstring says the kit is "code + live ledgers
  + packs + .env", 8MB per-file ledger cap, ore answered by bounded pointer
  (path + sha256), MEMORY_EXCLUDE includes `spore_seeds`

## 2. THE DE-RIDDLED SHAREABLE VERSION

STRIP (never rides): .env and every key (already ignored, .gitignore:19-22);
configs/providers.yaml VALUES (ignored, but the LANE SKELETON must ship as
providers.yaml.example, which does not exist today); the live ledgers
(tools/gps_mcp/gps_ledger.db3, memory/runs/*, queue/lanes/*/runner_state.json
+ trail.jsonl, metabolism_epoch.json when stamped); watch/inbox personal
receipts beyond a curated core; memory/biography, briefs, seals, trajectory
(already ignored); the rib-bus operator-bus chatter rows
(doctrine.json:41-68 are steering noise, not doctrine).

STAY (the seed): state/GENOME.md (MUST be whitelisted: `!state/GENOME.md`),
queue/STANDING_RAILS.md (tracked), the 55 ribs + 51 rib_bus files (tracked,
minus operator-bus noise), the parable
(corpus/canon/THE_PARABLE_OF_THE_FIELD_AND_THE_STONES.md) and the season
story (watch/inbox/THE_FIRST_SEASON_story_20261003.md, tracked), the 10
corpus steals (corpus/steal/, tracked, 32 files on disk now), the carriers
(tools/tavern.py, dungeon.py, arena_gwap.py, ds_workhorse.py, grok_burn.py,
hermes_burn.py, mag/route_chat.py), the GPS organs (tools/gps_mcp/*.py,
schema WITHOUT the db3), and .env.example (tracked).

DORMANT until needed: every lane whose key env is empty. The rails already
make this the natural state: mag/cost_truth's dormant gate refuses a lane
without an operator GO flag (mag/route_chat.py:15-16 docstring), z_ai3 sits
dormant in providers.yaml today (state/CURRENT.md:36-38). A new operator
fills .env.example slots one lane at a time and the estate wakes that lane
and nothing else. Dormancy is not a subsystem switch; it is an empty key.

## 3. N=2, N=4, N=8

What breaks at N=2, in order of violence:

1. The ledgers. gps_ledger.db3 is a tracked SQLite blob; git cannot merge it.
   ledger.py:468-470 defends double-inserts on ONE machine only. Two
   operators appending verdicts and pushing = non-fast-forward war; the
   winner's rows erase the loser's measured capability history. Same for
   every tracked runtime file (queue/lanes/*/runner_state.json,
   receipts.jsonl, usage.jsonl bank rows).
2. The bus. rib_bus doctrine.json is one JSON object; two writers appending
   ribs conflict on every concurrent push. There is no claim system: no
   owner, lease, or seat field in the row shape (doctrine.json:4-14).
3. The env. route_chat reads one process env and one ROOT/.env
   (route_chat.py:56-72). Two operators on one seat share one keyset and one
   usage bank (memory/runs/route_chat/usage.jsonl), so spend attribution is
   fiction. The estate already admits a second tenant it cannot serve: the
   docker cage owes "mount-or-env-door" and night march stays rc=2 skip
   until it (state/CURRENT.md:87-89).

What breaks at N=8 (same three, worse): the receipts.jsonl / trail.jsonl
append surfaces collide continuously; the season chain (watch/inbox/
playground/, 564 tracked files) forks into per-operator truths with no
merge rule; and the GPS capability ledger, which routes DOLLARS by measured
rate, becomes a last-writer-wins argument. Nothing at N=8 breaks in mag/
code: the code is seat-agnostic. Only the shared-state layer is
single-party, exactly as the topic suspected.

The cure is not locking. It is the split the travel kit already drew:
CODE publishes, STATE stays local, and estates exchange RECEIPTS (jsonl
with sha256 pointers, the kit's bounded-pointer law,
build_travel_kit.py docstring) through a fetch lane. Forked estates that
trade receipts. The spore_seeds format ({timestamp, seed, seat_id,
root_hash}) is already the per-seat identity stamp such a receipt would
carry, and it already has two seat_ids in it.

## 4. THE HERMES TUTORIAL (the ladder that costs ~5%)

Substrate verified: .env.example carries the key slots (DEEPSEEK_API_KEY,
DEEPSEEK_OVERMIND_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, GEMINI_API_KEY,
XAI, TOGETHER, VAST); the disk providers.yaml carries 24+ lanes including
z_ai/z_ai2/z_ai3/z_ai4 and the prefer-orders (scut, recall, public_summarize,
hard_code, hard_reason, default). The tutorial the repo owes:

1. Copy .env.example to .env. Fill DEEPSEEK_API_KEY first (the cheap
   workhorse; the estate's measured ~$0.001-class lane per AGENTS.md
   driving-ladder). Fill OPENROUTER_API_KEY second (overflow: lane_runner's
   flash_call already fails over to it, state/CURRENT.md:127-128).
2. GROQ_API_KEY + GEMINI_API_KEY + a z.ai key = the free lanes. SENSING only
   (AGENTS.md driving ladder: stealth/free outputs bank as findings, never
   as done). One z.ai-lite monthly chunk is the operator click
   (state/CURRENT.md:86 "$50 z.ai chunk click" was still pending).
3. Run `mag.cmd doctor`, then the genome boot order (state/GENOME.md:69-75),
   then drop the first ask into the rails: `route_chat(lane=..., goal=...)`.
   The dormant gate makes every unfilled lane refuse loudly. That is the
   whole ladder: paid judgment stays on the funded tier, everything else
   climbs free first.

OWED: the z.ai-lite and DeepSeek per-token prices were taken from estate
receipts, not re-verified against provider pages this sitting.

## 5. THE REGROW GUIDE (boot order, byte-backed)

1. `git clone` the spore. 2. Copy .env.example -> .env, fill DeepSeek +
   OpenRouter minimum. 3. Copy configs/providers.yaml.example (TO BE
   COMMITTED) -> providers.yaml. 4. Read state/GENOME.md, then
   queue/STANDING_RAILS.md, then `memory/rib_bus/` mount (genome section 3).
   5. Ledgers start EMPTY and local: gps_ledger.db3 is created by
   tools/gps_mcp/ledger.py on first verdict; the season starts when the
   first dungeon/tavern cron fires. 6. Register crons from scripts/
   register_*.ps1 (13 exist); the free-lane fleet cycle
   (scripts/free_lane_fleet_cycle.ps1) needs a register script and per-host
   path rewrite (it hardcodes C:\Users\foste, lines 4-6). 7. Bank everything;
   the epoch marker (metabolism.py:98-109) stays UNSTAMPED until the
   operator has a named drift event. The new operator regrows to their
   liking because the measurement history is theirs from zero: they inherit
   the laws, not the scores.

## 6. WHAT THE MYCELIAL REPUBLIC IS

Not a shared chain. Forked estates that trade receipts, on three byte-backed
grounds: (a) the genome's inheritance law is append-only and local
("nothing deleted", state/GENOME.md:82; "code publishes; memory stays local",
.gitignore:60-62); (b) the only cross-estate transport that exists is the
manifest+sha256 pointer (build_travel_kit.py), which is a receipt, not a
replica; (c) git history proves the estate already refuses shared surface
(github/master is a one-commit orphan; the operator nuked history once
rather than share it). GitHub is the spore pouch: dormant, keyless, read-mostly.
The chain stays on each machine; what crosses is the receipt.

## 7. FINDINGS (also returned via submit_result)

F1 spore-cannot-sprout: genome ignored + no providers template; F2 the push
is a 56,359-file publication event; F3 N=2 breaks on tracked ledgers, not
code; F4 the .env door is single-tenant and the cage is already the second
tenant; F5 the republic is forked estates trading receipts.

## 8. OWED / NOT RUN

No fresh-clone boot test (the F1 falsifier needs a 56k-file clone; not run).
No public fetch of github.com/NachoBusiness17/mycelial-republic to confirm
what the world sees today. No secret re-scan of the 17,069 tracked inbox
files (the gate's last run lives in watch/inbox/secret_gate_results/; I did
not re-run it). providers.yaml read was LANE NAMES ONLY, never key values.
The trajectory history discrepancy (.gitignore:30-34 vs rev-list=0) is
recorded, unresolved.
