# OPERATIONS LENS - THE SPORE SHARING PROBLEM (2026-10-05)

Lens: orchestration surgeon. Question: can the estate's seed actually ride
github.com/NachoBusiness17/mycelial-republic, and what breaks at N=2?
Everything below was read or run this sitting; instruments named per claim.

## FINDING 1 - The push as imagined is mechanically dead; the remote is 46 days stale (CONVERGENT with moonshot-1)

- `git remote -v` shows `github -> https://github.com/NachoBusiness17/mycelial-republic.git` already configured, plus a `local` mirror remote.
- `git branch -r` shows exactly one GitHub-tracking ref: `github/master` at
  dc66499434b0, dated **2026-08-20** ("Add the game bones to the framework").
  Nothing has ridden the remote since; the entire 46-day estate growth is
  local-only.
- `git ls-tree -r -l HEAD` census (this sitting): **56,361 tracked paths,
  18,922.7 MB at HEAD**, of which `watch/inbox` alone is **17,070 files /
  4,665.6 MB**. Seven paths at HEAD exceed GitHub's hard 100 MB file cap:
  ESTATE_INDEX.jsonl **twice** at 2,406.1 MB each (dashboard/data/ +
  watch/ESTATE_INDEX/), attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar
  2,210.9 MB, dashboard/data/ractor_board.jsonl.runaway-evidence-20260903
  2,129.3 MB, dashboard/data/ractor_board.jsonl 677.4 MB,
  training/events.jsonl 340.6 MB, artifacts/vertigo_boat_20260908/tokyo_river_depth_1080p.mp4
  255.6 MB, catalog/catalog.jsonl 235.1 MB. Any ref containing these blobs
  is rejected GH001. Also tracked: tools/godot/Godot_v4.3-stable_win64.exe +
  godot.zip and two pain_replication .pt weight files.
- Instrument note: sibling moonshot-1.md FINDING 2 counted **14.37 GiB / 54
  blobs over 100 MB** by a history-blob census; mine is a per-path HEAD
  census (18.9 GB, 7 oversized paths). Different denominators (HEAD paths
  vs history blobs), same verdict. This finding is CONVERGENT and outranks
  single-source claims.
- **Falsifier:** an actual push attempt of any ref containing HEAD to a
  scratch GitHub repo succeeds. Expected: GH001 rejection naming one of the
  seven blobs. Not run here (no scratch repo provisioned).
- **Move (one sitting, ~30 min):** declare the spore a NEW orphan-root repo
  (fresh first commit of the allowlisted seed), never a push of this
  history; record the decision in the regrow guide so no seat retries the
  doomed push.

## FINDING 2 - The spore strips its own DNA and ships the operator's diary instead

`git check-ignore -v` (this sitting):

- `state/GENOME.md` - ignored by `.gitignore:40` (`state/`). The genome,
  the file GENOME.md:1-6 calls "the inheritable artifact" whose section 3
  IS the boot order, would NOT ride the push. Exactly one state/ file is
  tracked (state/NIGHT_LOOP_20261005.md, evidently force-added).
- `configs/providers.yaml` - ignored by `.gitignore:24`. mag/route_chat.py:51
  hard-loads that exact path (`(ROOT / "configs" / "providers.yaml").read_text`)
  with no fallback and no example ship (`ls configs/*.example` -> not found).
  A fresh clone's ONE front door (queue/STANDING_RAILS.md law 1) raises
  FileNotFoundError before any fence, dormant gate, or lane logic runs.
- `watch/inbox/INDEX.json` - ignored by `.gitignore:249`, while its 17,070
  sibling receipts (4.67 GB tracked) DO ride.
- memory/runs/** IS correctly ignored (.gitignore:102) - usage ledgers stay
  local; memory/rib (55 files) and memory/rib_bus (51 files incl
  doctrine.json) ARE tracked - the ribs ride, good.
- `.env.example` exists but is stale against providers.yaml: it lists 13
  vars and lacks HERMES_API_KEY_1/2, XAI_SD_API_KEY, ZAI_API_KEY_Pro,
  OPENROUTER_API_KEY_2/OR_API_KEY, GROQ_API_KEY_2, DEEPSEEK_SWARM_API_KEY -
  every name the funded tier (driving ladder, AGENTS.md) and the free lanes
  actually read. The tutorial cannot be written from .env.example.

Net: push-as-is = the operator's 46-day diary shipped, the constitution that
explains it and the config that powers it withheld. That is the exact
inverse of a spore.

- **Falsifier:** on a fresh clone,
  `python -c "from mag.route_chat import route_chat; route_chat('ack', lane='xai', max_tokens=16)"`
  boots and acks. Today it cannot (providers.yaml missing on clone).
- **Move (one sitting, ~45 min):** three deliberate additions, nothing
  untracked: `!state/GENOME.md` + `!watch/inbox/INDEX.json` whitelist lines,
  a `configs/providers.example.yaml` generated from providers.yaml (keys and
  key VALUES stripped; lane names, base_urls, dormant flags, api_key_env
  NAMES kept), and `.env.example` regenerated from the same source.

## FINDING 3 - N=2 has no identity anywhere it matters; every append surface fails closed or blends

Read this sitting:

- GPS capability ledger PK is (model_id, task_shape) - tools/gps_mcp/ledger.py:133-142.
  No operator/estate column exists (grep for operator|owner|seat_id|host_id
  in ledger.py hits only docstrings). A second estate's upsert_measurement
  OVERWRITES the first estate's measured rate; and tools/gps_mcp/gps_ledger.db3
  is itself tracked at HEAD (0.7 MB, git ls-files), so a new operator boots
  believing someone else's 209 measured rows are their own priors - D7
  metabolism (tools/gps_mcp/metabolism.py) then decays foreign experience as
  if it were theirs.
- The season chain: SessionLedger rows are exactly {seq, ts_utc, payload,
  prev_sha256, row_sha256} (mag/gwap_payload.py:123); verification requires
  seq == row index and prev chain (gwap_payload.py:704-710); append refuses
  to extend a chain that fails verification (761-763). Row shape has no
  party field. Two writers appending to one ledger file interleave and the
  chain breaks FOR BOTH - append fails closed thereafter. The store is
  memory/runs/gwap (gwap_payload.py:93), correctly gitignored - so the chain
  cannot be shared by accident, but it also cannot be merged by design.
- route_chat usage rows carry lane/model/key_env/goal only (route_chat.py:301-311).
  No operator field: even two humans on ONE seat cannot attribute spend.
- Queue lanes: queue/lanes/research/runner_state.json is a bare
  {inbox_offset, last_run, seat, rotation_epoch} - a single-consumer file
  cursor with no claim/lease. Two processes sharing a queue dir double-consume
  or silently skip work.
- mag/mycelium.py reinforce() loads ALL edges, mutates one, rewrites the
  whole file (mycelium.py:197-227, 243-277) with no locking - a second
  concurrent writer loses updates, and the SupersedeViolation guard
  (mycelium.py:257-273) would misfire on a concurrent supersession.

- **Falsifier for the sharpest sub-claim:** spawn two processes calling
  SessionLedger("arena-capability").append() in the same second on one
  store; verify_chain() then fails at the interleaved row and both are
  locked out. Reasoned from code, NOT executed here (would mutate the real
  ledger); the repro is exact and cheap on a temp store.
- **Move (one sitting, ~20 min):** stamp estate_id at the export boundary -
  a tiny export/import pair that wraps any ledger row set in an envelope
  {estate_id, exported_at, rows} - so forked estates can TRADE receipts as
  files without any shared-write surface. No schema surgery on the live
  organs until an operator GO.

## FINDING 4 - The regrow path exists in bytes but is host-bound; dormancy is documented, the crons are not portable

- GENOME.md section 3 is the boot order (genome -> rails -> ribs -> CURRENT
  -> delta register) and ribs/rib_bus ARE tracked - a cold clone can actually
  follow it, minus the two stripped files in Finding 2.
- The arena/season runtime is host-bound: ~12 schtasks registration scripts
  (scripts/register_improve_task.ps1, register_census_patrol_task.ps1,
  register_fts_index_task.ps1, register_gap_sentinel_task.ps1,
  register_day_end_task.ps1, register_leave_task.ps1,
  register_ratchet_task.ps1, register_tip_witness_task.ps1,
  register_endpoint_news_task.ps1, register_corpus_rescan_task.ps1,
  register_gate_canary_task.ps1, register_vision_nightly.ps1). None
  re-register themselves on a new machine; on a fresh clone
  `schtasks /Query /TN MagImproveDaily` returns not-found and every cron is
  dark.
- The season chain starts at seq 0 on any clone (memory/runs/gwap ignored);
  the only sanctioned priming path is seed_fixtures.py (ledger.py docstring:
  "cost is seeded or updated by operators/fixtures", ~line 329).
- Dormancy is already a declared state, not a hack: providers.yaml lanes
  carry `dormant: true` with live-measured causes (e.g. saelis line 64, gemini
  line 486), and route_chat's dormant gate refuses without operator_go
  (route_chat.py:241-243). Subsystems-dormant-until-needed is therefore
  ALREADY the repo's native grammar - the spore ships it by keeping lane
  blocks with dormant flags, zero new mechanism.

- **Falsifier:** a REGROW.md exists in the tracked tree that a fresh-clone
  operator follows to a live arena cron without reading this receipt.
  Today no such file exists (ls of repo root and docs/ shows none named
  REGROW; not exhaustively globbed - scoped to those two dirs).
- **Move (one sitting, ~30 min):** write the regrow guide as ONE page: boot
  order (cite GENOME section 3), the three minimum-viable crons to re-register
  (improve, fts_index, arena/tavern+dungeon hourly) with their exact ps1
  invocations, and the GPS priming choice (empty ledger vs seed_fixtures).

## FINDING 5 - The strip is mostly already done by policy; what remains hot is history, zknot, and the inbox mass

- The secret gate ran clean on changed files 2026-10-05T07:56:17Z
  (watch/inbox/secret_gate_results/changed_20261005T075617Z.json:
  severity_counts all zero, blocking_count 0) - the HEAD tree's changed
  surface carries no detected key material.
- Ignored-by-policy hot material (verified via .gitignore lines): .env
  (:272), memory/runs/** (:102), memory/briefs|biography|ingest (:63-75),
  *.key/*.pem/wallet* (:252-256), memory/trajectory/steps.jsonl (:43, which
  carried 7 live .env values per its own comment).
- Still tracked and personal: 20 zknot session-history files
  (memory/zknot/*.md, git ls-files), the 4.67 GB inbox diary, and HISTORY
  blobs - sibling accuracy.md found the lan.key blob (799ddb6fe, 1675
  bytes) and admitted .env-value commits in history. CONVERGENT with
  accuracy.md. Whether lan.key is ON GitHub is unverified by me:
  github/master's tip (08-20) may predate the blob's landing; accuracy.md
  itself marks rotation status unverified.
- **Falsifier:** the spore pack ships as an allowlist build (genome, rails,
  ribs, rib_bus, mag/, tools/, docs/, corpus/canon, providers.example,
  .env.example) and a `git ls-files` of the pack contains zero
  watch/inbox/memory/zknot paths. Not yet built - this is the spec.
- **Move (one sitting, ~15 min):** write the pack manifest as an allowlist
  (scripts/build_spore.py or a plain file list), so the strip is positive
  proof per build, not a blocklist archaeology per push.

## WHAT THE REPUBLIC IS (Q5, as-built at byte level)

A single-tenant estate whose only republic-shaped artifacts are: a
fork-friendly seed (genome + ribs tracked), append-only local chains that
FAIL CLOSED on sharing (SessionLedger), a capability ledger with no party
dimension, and a git remote configured but stale since 08-20. It is
therefore today neither a shared chain nor a trading network: it is a
forkable organ donor with no transplant protocol. The honest v0 the
evidence supports: forked estates, receipt trades as identity-stamped
files, shared-write surfaces postponed until estate_id exists everywhere
spend and measurement land.

## BLIND SPOTS (honest)

- Transfer-size proof not run: no git count-objects, no actual push attempt;
  18.9 GB is a per-path HEAD census and may double-count (ESTATE_INDEX
  tracked twice) vs the sibling's 14.37 GiB history-blob census.
- The N=2 races (SessionLedger, mycelium reinforce, inbox_offset) are
  reasoned from read code, not executed; falsifiers name exact repros.
- Tutorial surface (docs/FRAMEWORK_LOAD.md, hermes_warm_boot) not read; the
  tutorial finding is limited to .env.example vs providers.yaml drift.
- Whether github/master's pushed history contains lan.key: flagged by
  sibling accuracy.md, not verified by me.
- Sibling lens files read only by grep for convergence, not in full.
