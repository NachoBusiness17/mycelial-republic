# BREAK-ECONOMICS: hostile second pass on the spore-sharing lens (2026-10-05)

Pass: ractor_engine spore-sharing run, break-economics seat.
Instrument of record: `watch/inbox/ractor_engine/2026-10-05-spore-sharing/_verify_break.py`
(run via `.venv/Scripts/python.exe`, CHECK-01 through CHECK-18, all output masked, no secret
values printed), plus the individual commands cited inline below. Every number in this file
was run or read THIS sitting unless marked OWED.

---

## VERDICTS

### F1 "The spore cannot be a git push; it is a fresh orphan allowlist tree built by copy" - CONFIRMED (two count corrections)

Reproduced this sitting:

- `git count-objects -vH` -> `size-pack: 14.37 GiB`, `garbage: 4` named `tmp_pack_7VSjsR`,
  `tmp_pack_fYXCQT`, `tmp_pack_SFNqKc`, `tmp_pack_Vl6Sd1` (973.47 MiB). Matches the lens.
- Blob census (`git ls-tree -r -l HEAD`, untruncated, CHECK-01): 56,358 blobs in the HEAD
  tree, exactly **19 over 104,857,600 bytes**. Top: `watch/ESTATE_INDEX/ESTATE_INDEX.jsonl`
  at **2406.1 MB**, same blob sha `cb136109569b` at `dashboard/data/ESTATE_INDEX.jsonl`
  (dual-path confirmed). Others include `attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar`
  2210.9 MB, `dashboard/data/ractor_board.jsonl.runaway-evidence-20260903` 2129.3 MB,
  `tools/godot/Godot_v4.3-stable_win64.exe` 126.8 MB. Matches the lens.
- `git log -1 github/master` = `dc6649943` 2026-08-20 11:28:57 -0400; `git log -1 main` =
  `5d20144e1` 2026-08-04; `git log -1 HEAD` = `7dac8685e` 2026-10-05 (the living line is the
  mag/* branch). Matches the lens. Aug 20 -> Oct 5 is 46 days: the "46 days stale" arithmetic holds.
- `git remote -v`: `github https://github.com/NachoBusiness17/mycelial-republic.git`. The named
  remote exists exactly as claimed.

Count corrections (QUANTIFIER LAW): tracked total reads **56,361** (lens: 56,359; +2, tree
drift, immaterial) and memory/ + watch/ reads **47,109** (lens: 43,818; **off by 3,291, does
not reproduce**; `git ls-files`, CHECK-02). Direction of the claim survives (83.6% of tracked
paths are memory/+watch), but the lens's figure is not byte-clean and should be re-cited from
a fresh census at export time.

Blind spot CLOSED with live network: `api.github.com/repos/NachoBusiness17/mycelial-republic`
returns public, `default_branch: master`, size 644 KB, `pushed_at: 2026-08-20T15:29:04Z`,
description: **"Public practice surface (no private machinery)"**. The local sibling clone
`../mycelial-republic` sits at the same tip `dc66499` with 225 tracked files and `origin`
pointing at the same URL, so the ref `github/master` IS the remote tip. The remote is real,
public, tiny, and 46 days stale, exactly as the lens inferred without network.

Falsifiers NOT run this sitting: no push was attempted, no filter-repo was attempted. The
100MB cap is GitHub's documented limit, not something measured here. The verdict stands on
the byte evidence above.

### F2 "The secret danger is not .env but the tracked corpus" - CONFIRMED (one sub-claim KILLED)

Reproduced this sitting:

- `watch/inbox/secret_gate_results/full_run_row.json` matches the lens **byte-for-byte** on
  every figure: generated_utc 2026-09-27T18:37:19Z, critical **42**, high **15,610**,
  blocking **3,606**, ANTHROPIC-KEY **420**, XAI-KEY **27**, DEEPSEEK-KEY **19**,
  GITHUB-TOKEN **1**, STRIPE-KEY **14**, `runtime_sec: 49256.0`,
  `bytes_scanned: 30,868,243,622` (30.8 GiB).
- The gate's own `blocking_sample` names `cdx_rar.json` line 616 rule GOOGLE-OAUTH-AQ masked
  `AQTA2T...(len=32)`, and my byte read of line 616 of the tracked `cdx_rar.json` (repo root,
  1,001 lines) finds exactly that: a CDX row carrying a 32-char token starting `AQTA2T`
  (masked output only). The lens cite is confirmed at byte level. My first narrow regex scan
  of the file missed it and returned a false negative; the gate row plus a direct `AQTA2T`
  probe settles it. `git ls-files --error-unmatch cdx_rar.json` succeeds.
- `boe003.html` line 257 contains `pk_live` (STRIPE-KEY, masked len 42), file tracked. So are
  `boe_index.html` and `module_audit.ipynb` (the other named blocking samples): all four
  blocking samples at repo root are TRACKED.
- `.env`: `git log --all --oneline -- .env` = **0 commits**; `git check-ignore -v .env` ->
  `.gitignore:272:*.env`. Matches the lens exactly.

Sub-claim KILLED: "23 .mimosa files (the postgres connstring class) are tracked." Census
(CHECK-02 + connstring scan): **0 tracked files end in `.mimosa`**; **25** tracked paths
contain the substring `mimosa` (lens said 23); **0 of those 25 contain a postgres
connstring** (they are hook-state session JSONs, receipts, and
`attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar`). The CONNSTRING-CRED hits
the gate sampled live under a **root `.mimosa/` directory that is gitignored**
(`.gitignore:200:.mimosa/`, `check-ignore` rc=0) and therefore untracked. The lens's move
"git rm --cached the 23 mimosa paths" aims at a class that is not in git. The standing purge
program already exists: `watch/inbox/PURGE_LIST_MERGED_20260927.md` (tracked) and the
2026-09-27 gate-fix commit `d15bc960d` name the boe/stripe harvest families.

### F3 "N=2 breaks at the write surfaces, all single-party by construction" - CONFIRMED (strengthened)

Reproduced this sitting:

- `mag/route_chat.py:46` `USAGE = ROOT / "memory" / "runs" / "route_chat" / "usage.jsonl"`;
  line 64 is `if os.environ.get(env):` and line 67 reads `(ROOT / ".env")`. Nuance: the order
  is env-var FIRST, `.env` as fallback, so the lens's "hardcoded .env, os.environ fallback"
  inverts the precedence; the substance (one hardcoded seat-local .env) holds.
- Untruncated bank census (CHECK-06): `memory/runs/route_chat/usage.jsonl` has **19 rows**
  (8 ok_true, 11 ok_false), **0 rows carry a cost field, 0 rows carry any
  operator/owner/id/seat/session_id field**. Union of keys across ALL rows:
  `[completion_tokens, content_chars, depth, detail, error, finish_reason, goal, key_env,
  lane, model, ok, prompt_tokens, reasoning_tokens, thinking_sent, ts]`. The lens's falsifier
  escape hatch ("rows already carry a merge-surviving identity field") is CLOSED: none does.
- `tools/gps_mcp/gps_ledger.db3` tracked, **782,336 bytes**. Schema (sqlite, read-only):
  `capability(model_id, task_shape, pass_rate, sample_size, cost_usd_per_call,
  last_measured, updated_at)` 30 rows; `verdict_log(ts, model_id, task_shape, verdict,
  evidence_hash, evidence_resolved, evidence_source, evidence_bytes)` 703 rows. **Zero
  operator-ish columns.** The lens missed that a SECOND copy is tracked:
  `tools/gps_mcp/gps_ledger.db3.bak_pre_D2_20260930`.
- `watch/inbox/D7_PHEROMONE_METABOLISM_20261005.md` lines 44-45: "haiku arena-agreement
  stored 0.047 with a 10-fail streak -> effective 0.030." Matches the lens.
- `mag/rib_bus.py` is 274 lines; my wider grep (claim|lock|owner|writer|lease|reserv|ticket)
  hits only lines 4, 158, 195, all prose or comment (line 158 is an AH19 comment the lens did
  not list; it is not a mechanism). No claim system. Confirmed.
- `queue/STANDING_RAILS.md` read whole (74 lines): no multi-operator, per-seat, or claim
  concept anywhere. The lens's line pointer is one off: line 43 is the tavern/dungeon
  "(hourly cron)" row; the arena row is line 44.

### F4 "The ladder economics" - CONFIRMED on every ledger computation (finding text arrived truncated in the ask; verdict covers the three cited computations)

Recomputed this sitting from raw jsonl (CHECK-10, CHECK-11):

- `memory/runs/ds_batches/delta_judge_results_v3.jsonl`: **27 rows**, cost_usd total
  **0.072444**, per ask **0.002683** (lens: 27 / $0.0724 / $0.0027). Match.
- `memory/runs/hermes_burn/usage.jsonl`: **3,010 rows**, cost_usd total **94.6085** (lens:
  3,010 / $94.61). Per model: opus-5.5 **1,247 rows / $59.8293** = $0.048/ask (lens:
  $59.83/1247); haiku-4.5 **664 rows / $2.635** = $0.004/ask (lens: $2.63/664). Match.
- Ratio scoping the lens did not state: ds $0.002683 is **5.6% of opus** ($0.048) but **68%
  of haiku** ($0.004). "~5% of paid" is true against the premium rung only; the tutorial
  should say which rung.
- The auditability gap is real at census level: the route_chat door (the rails' mandated front
  door, STANDING_RAILS.md law 1) banks **zero** cost fields in 19/19 rows, while
  hermes_burn/ds_batches rows do carry cost_usd. A new operator auditing their own ladder
  through route_chat rows cannot compute $/ask without joining token counts to a price table.

---

## BLIND-SPOT DISPOSITIONS

1. GitHub live state: **CLOSED** (see F1). Public, master, 644 KB, pushed 2026-08-20T15:29:04Z,
   charter line in the description: "no private machinery".
2. Season ledger as standalone organ: **CLOSED-NEGATIVE**. None exists in code. Grep census of
   mag/ + tools/ for SEASON_STATE: no writer (only prose at `tools/dungeon.py:715`, "the
   season continues"). Season state lives in design prose
   (`watch/inbox/hermes_burn/SEASON_II_arc.md`, `SEASON_design.md`: "the party subchain tip IS
   the save file") and in the gwap SessionLedger chains (`mag/gwap_payload.py:714`,
   `STORE = ROOT / "memory" / "runs" / "gwap"`, :92-93). The topic's "season ledger assumes one
   party" is design prose, not a bank that exists.
3. Compass + sibling tree: **CLOSED**. `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md:40` "You can
   fork the repo and run `:8765` without our permission"; :51 "Forest | mycelial-republic |
   Public law, fork, optional republic train"; :199 "Forkable - no permission required". The
   sibling's `docs/CONSTITUTION.md` v0.1.1 section 1 (Fork equality): 1.1 no canonical core,
   1.2 a complete fork has equal standing, 1.4 interconnect must not hard-code a privileged
   registry. Q5's "forked estates trading receipts" is binding doctrine in bytes, not a guess.
4. The 42/15,610 figures: **verified from the gate row** (byte-exact). A fresh gate run over an
   export set: **NOT run this sitting, OWED**. Standing infrastructure exists:
   `MagSecretScanWeekly` scheduled task (weekly, `scripts/secret_scan_weekly.py`, schtasks XML
   dumped this sitting).
5. Arena cron: **PARTIALLY CLOSED, with a negative result.** schtasks census (246 tasks,
   CHECK-17): 16 Mag* tasks + `mag-docker-watchdog`; **zero tasks named tavern/dungeon/arena**.
   `MagFreeLaneFleet` runs every PT30M -> `scripts/free_lane_fleet_cycle.ps1` ->
   `python -m tools.free_lane_fleet --cycle`, and `tools/free_lane_fleet.py` contains no
   tavern/dungeon/arena call (grep). No host found in `main.py`, `mag/offpeak.py`,
   `mag/loop_audit.py`; `tools/tavern.py:279` and `tools/dungeon.py:770` are `__main__` CLIs.
   So STANDING_RAILS.md:43's "(hourly cron)" has **no registered carrier** in the surfaces
   checked; "the arena cron" a spore would ship dormant does not exist as a task to ship.

---

## WHAT THE LENS MISSED (additions)

A1. **The two crown organs are gitignored.** `configs/providers.yaml` is ignored at
`.gitignore:24` and `state/GENOME.md` falls under `.gitignore:40` (`state/`); both are absent
from the HEAD tree (`git ls-tree` empty for both). The genome and the lane manifest, the
exact things a spore exists to carry, are working-tree-only. Any git-shaped share (orphan
branch of tracked files, archive of HEAD) ships without them. Falsifier: a git-based export
containing both files. Move: spore_export.py reads the allowlist from the working tree, never
from git, and asserts both ignored organs present. +15 min on the lens's 30.

A2. **The tracked `.env.example` predates the entire current ladder.** It carries 13 keys vs
56 in `.env`; missing include `ZAI_API_KEY/_2/_3/_Pro`, `XAI_SD_API_KEY`, `GITHUB_TOKEN`,
`HERMES_API_KEY_1/2`, `OPENROUTER_API_KEY_2`, `GROQ_API_KEY_2`, `MAPBOX_TOKEN`, the `X_*`
OAuth set (key NAMES only; values never read; CHECK-13). No suspect real values in the
example. Falsifier: a route_chat boot on the example alone reaching deepseek + z.ai + xai-SD.
Move: write the tutorial's example fresh from `.env` key names. +20 min.

A3. **The gwap chain schema is strict; operator identity is a version bump, not a field.**
`mag/gwap_payload.py:123` `_ROW_KEYS = {"seq", "ts_utc", "payload", "prev_sha256",
"row_sha256"}`; append refuses any drift and verifies the full chain first (class SessionLedger,
:714). The lens's "add operator_id to the gwap payload" in ~25 min underprices the
`mag_gwap_payload.v1` -> v2 bump plus a v1-compatible reader. Falsifier: append a row with an
extra key without bumping SCHEMA and pass verify_chain. Move: schema v2, one-directional
reader, tests. +45 min.

A4. **A second operator-A capability artifact is tracked.** `tools/gps_mcp/
gps_ledger.db3.bak_pre_D2_20260930` (git ls-files, CHECK-02). The strip list must name both
db3 files. Falsifier: an export census finding zero `gps_ledger*` paths. Move: +2 min.

A5. **The allowlist candidate set scans clean for key material.** 12 regex families
(sk-ant/sk-proj/openai-sk/AIza/xai/pk_live/sk_live/ghp/github_pat/GOCSPX/AKIA/postgres-conn)
over 52 ribs + providers.yaml + GENOME + STANDING_RAILS + compass + the parable + route_chat +
rib_bus + gps_mcp/*.py + ds_workhorse* + arena_gwap* + secret_gate* + `.env.example`:
**zero hits** (CHECK-12). The lens's allowlist move is safe at pattern level. Falsifier: a hit
from the same instrument on those paths. Move: fold the scan into spore_export.py as a
pre-copy gate. +10 min.

A6. **Personal identity markers ride the export set in prose.** `configs/providers.yaml`
comments name the operator's second accounts (openrouter block "account 2 = free tier
(fostertron/ox)" around :176, xai block "Nach... + sd20645547" around :501, nous note "the
Hermes sdd/nacho accounts" around :258). Not secrets (A5 scan clean); a persona-scrub decision
the lens never surfaced. Falsifier: grep `fostertron` on the exported tree returning zero.
Move: scrub or accept in one commit. +10 min.

A7. **Per-seat is already physical in the task layer.** `scripts/free_lane_fleet_cycle.ps1:5-6`
hardcode `C:\Users\foste\...` under the file's own ABSOLUTE PATH LAW comment, and the
schtasks census shows the Mag task fleet is registered against those absolute paths. A new
operator does not migrate a cron; they re-register tasks from scripts with their own paths.
Falsifier: a scheduled task or ps1 in the tree with no absolute personal path. Move: regrow
guide gets a re-register section listing the 16 Mag* task names. +15 min.

A8. **Inventory counts the spore doc should cite, byte-backed this sitting.** Doctrine ribs =
**26** exactly (`memory/rib_bus/doctrine.json`, `ribs` dict length 26; GENOME.md section 0
names this file as the machine-readable genes). `memory/rib/*.md` = 52 files (47 `RIB_*`).
`corpus/steal/` = 32 top-level .md, 40 .md including nested subdirs (two instruments). The
topic's "10 corpus steals" matches neither census; which ten is **OWED**.

---

## OWED (not run this sitting)

- Fresh `tools/secret_gate.py` run over the exported spore tree (F2's standing falsifier);
  only the 12-pattern allowlist scan ran.
- A measured push of HEAD to `github` and a filter-repo timing (F1's falsifiers).
- A two-clone append/reconcile exercise (F3's falsifier); settled instead by the untruncated
  row census showing zero identity fields.
- Resolution of "which 10 corpus steals" (A8).
- The remote's exact file list was taken from the sibling clone at the same tip (dc66499,
  225 files), not from an independent remote fetch.

## Files

- Bank: `watch/inbox/ractor_engine/2026-10-05-spore-sharing/break-economics.md` (this file)
- Instrument: `watch/inbox/ractor_engine/2026-10-05-spore-sharing/_verify_break.py`
