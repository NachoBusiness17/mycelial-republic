# break-logic pass - spore-sharing lens report, 2026-10-05

Hostile second pass. Every cite byte-checked against the estate by commands run THIS session
(shell is git-bash; environment header said cmd.exe - noted honestly in §5). Repo:
C:\Users\foste\Documents\projects\local_sovereign_agent, HEAD 7dac8685e (branch
mag/run-beta1-factory-build-audi-20260806T231709Z, tip 2026-10-05 07:19:24 -0400). The tree is
live (sibling lanes commit during audits); every count is moment-stamped with its instrument.

Moment: 2026-10-05, post night-shift close (NIGHT_SHIFT_20261005_CLOSE.md exists; close 08:50Z).

## 0. VERDICT TABLE

| # | Finding (short) | Verdict |
|---|---|---|
| 1 | Spore cannot regrow from its own clone | CONFIRMED (falsifier EXECUTED, passed) |
| 2 | Sharing instrument fired once and rotted | CONFIRMED (+1 count drift, 2 cite nits named) |
| 3 | Rib bus loses ribs at N=2; GPS prior conflates seats | CONFIRMED (race now MEASURED: 96-98% loss) |
| 4 | Dormancy is the mechanism; the lane map is untracked | CONFIRMED (falsifier's exception name corrected) |

## 1. FINDING 1 - CONFIRMED

Cite byte-checks (all run this session):

- `git ls-files state/GENOME.md state/CURRENT.md configs/providers.yaml tools/gps_mcp/gps_ledger.db3 queue/STANDING_RAILS.md`
  returned exactly `queue/STANDING_RAILS.md` + `tools/gps_mcp/gps_ledger.db3` - GENOME.md,
  CURRENT.md, providers.yaml absent. Lens claim "returns empty for the two state files": TRUE.
- `git ls-files state` -> exactly one tracked file: `state/NIGHT_LOOP_20261005.md` (committed
  23d76bb71, 2026-10-05 06:48:04 -0400). state/ is not literally zero-tracked; the exception does
  not touch the finding (GENOME/CURRENT still untracked).
- `git check-ignore -v state/GENOME.md state/CURRENT.md` -> `.gitignore:40:state/` for both.
  .gitignore:40-41 are `state/` + `state/**/*` (with `!state/.gitkeep` at :42). Lens cite TRUE.
- state/GENOME.md:69-75 = section 3 BOOT ORDER, verbatim: "1. This file. 2. queue/STANDING_RAILS.md.
  3. The ribs (memory/rib/). 4. state/CURRENT.md. 5. The Delta Register ...". :82 = "Memory: the
  verkle chain and watch/inbox - append-only, nothing forgotten." Both exact.
- Tracked genes: `memory/rib_bus/doctrine.json` ribs = 26, `memory/rib_bus/standing-wave.json`
  ribs = 87 (python json count; exact match to the lens). memory/rib_bus/ has 49 more tracked
  domain files; `git ls-files memory/rib | wc -l` = 55.
- `tools/gps_mcp/gps_ledger.db3` tracked, 782,336 bytes, NOT gitignored (`git check-ignore -v`
  no rule). Ships in any clone.
- `git ls-files watch | wc -l` = **20,360** at my moment (lens: 20,359; +1 live-tree drift,
  instrument named).

Falsifier EXECUTED (the lens only proposed it): `git clone --depth 1 --no-hardlinks . %TEMP%\spore_break_20261005`
(git warns --depth ignored on local clones; checkout completed, 56,361 files). Results:

```
state_DIR_PRESENT      (only because state/NIGHT_LOOP_20261005.md is tracked)
GENOME_MISSING
CURRENT_MISSING
DOTENV_MISSING
DB3_PRESENT
PROVIDERS_MISSING
RAILS_PRESENT
RIBBUS_PRESENT
PARABLE_PRESENT        (corpus/canon/THE_PARABLE_OF_THE_FIELD_AND_THE_STONES.md)
CLONE_WATCH = 20360    (git -C <clone> ls-files watch | wc -l)
```

`find <clone> -iname '*GENOME*'` returns only unrelated genomes (.agents/skills/verb-genomes,
basecamp/CACHE_FARMING_GAME_GENOME.md, docs/ref/verb_genomes, watch/GAME_PROMPT_GENOME_LEAD_20260901.md,
watch/inbox/burn_reset_20260927/flash50/deep-tool-genome.md). No estate GENOME copy ships.

GENOME section 3 step 1 ("This file") dead-fails in the fresh clone exactly as the lens predicted.
Refinement that strengthens the finding: the machine genes DO ship (tracked), so what is lost is
precisely the prose genome + live-truth CURRENT - the inheritance law's named artifact.

## 2. FINDING 2 - CONFIRMED

- `git remote -v` -> `github  https://github.com/NachoBusiness17/mycelial-republic.git` exact;
  also a second remote `local -> C:\Users\foste\Documents\projects\Mag-backup.git` (lens did not
  mention it; irrelevant to the claims).
- `git log -1 github/master` -> dc66499434b050343e81dabcb45b849c5f1fda29, 2026-08-20 11:28:57 -0400.
  `git ls-tree --name-only github/master` -> .gitignore, AGENTS.md, CONTRIBUTING.md, README.md,
  configs, data, docs, framework, logs, mycelia.cmd, mycelia.ps1, pyproject.toml, scaffolds,
  scripts, scrum, selftest, src, tests. Locally: src MISSING, framework MISSING, mycelia MISSING.
- `git log -1 main` -> 5d20144e1, 2026-08-04 15:33:07 -0400 (stale, as claimed).
- Counts: main..github/master=1 (lens 1 OK), github/master..main=5 (5 OK), main..HEAD=**874**
  (lens 873), github/master..HEAD=**879** (lens 878). Uniform +1: tip 7dac8685e landed 07:19:24
  EDT inside the audit window. Same-day drift, substance exact.
- `git branch | wc -l` = **38** (same instrument as lens, incl. the current-branch marker line). OK.
- Pushed-history keyscan, lens's exact instrument: `git rev-list github/master --objects |
  grep -icE '\.key$|\.env$|secret'` = **0**. Extended beyond the lens's regex, all 0 in pushed
  objects: providers.yaml, mag-secret.yaml, memory/seals, trajectory/steps.jsonl. The untrack
  commit is local: 5a6ffd806 "2026-08-20 security: untrack providers.yaml + mag-secret.yaml
  (live creds), gitignore them" (byte-matches .gitignore:23 "(tracked fix 2026-08-20)").
- Local history IS dirty as claimed: `git rev-list --all --objects | grep -i lan.key` -> 1 object
  `f5e6dea5f... memory/tls/lan.key`; reached via 2 commits (add33ba72, 799ddb6fe), both NOT
  ancestors of github/master (`git merge-base --is-ancestor` -> NO). .gitignore:270-271
  "lan.key untracked same day; rotate - it remains in history" byte-checks. So the move's premise
  (local history cannot push as-is) is object-proven, not just comment-proven.
- Receipt-chain claim: watch tracked 20,360 OK; **"96 in the last 48h" is NOT reproducible** at my
  instruments: `git log --since=2026-10-03T00:00:00Z --oneline -- watch/inbox | wc -l` = 90
  commits; `--diff-filter=A --name-only` over the same window = **1,479 paths** added. The 96
  names no instrument; the substance (receipts are the growing chain) holds and is stronger.
- Cite nit: "daily work rides a 2026-10-05 branch" - the branch is NAMED
  mag/run-beta1-factory-build-audi-20260806T231709Z (Aug-06); its TIP commit is 2026-10-05.
  Newest other branch by committerdate: reboot-staging-20261003.
- Manifest-comment honesty check: .gitignore:30-32 says "7 live .env values were committed in it"
  (memory/trajectory/steps.jsonl) - but that path has **0 blobs and 0 commits in ALL reachable
  history** (`git rev-list --all --objects | grep -ic 'steps\.jsonl'` = 0; pathspec log = 0;
  58,244 lines live on disk). The de-facto manifest's own provenance comment is not byte-true at
  my instrument; does not move the verdict (pushed-clean holds on every probe; local-dirty is
  proven via lan.key).

## 3. FINDING 3 - CONFIRMED, and the race is now MEASURED

Code cites: mag/rib_bus.py:156-167 is the load->mutate->save in publish_rib (exact; `store =
_load_store(domain)` at :156, `path = _save_store(store)` at :167); _save_store :78-82 is a plain
`f.write_text` (:81), no lock anywhere in the module. The unused lock pattern is named at
.gitignore:264-265 ("store_io OS locks (server/store_io.py exclusive()) - never commit", `*.lock`) -
the lens's "cited in .gitignore" byte-checks.

RACE MEASURED (falsifier executed this session; two real subprocesses, spawned with
creationflags=CREATE_NO_WINDOW; RIB_DIR monkeypatched to a temp dir, domain "breaktest",
fold=False/publish=False so the verkle chain and bus publish are untouched; NO production file
read or written; temp dirs deleted after):

```
round 1: rcs=[0, 0] final_ribs=6    expected=600 lost=594
round 2: rcs=[0, 0] final_ribs=24   expected=600 lost=576
round 3: rcs=[0, 0] final_ribs=12   expected=600 lost=588
```

The lens falsifier said "loses one rib at high frequency"; measured reality at max contention is
~96-98% loss (last-writer-wins full-file rewrites). The finding's mechanism is not just plausible,
it is demonstrated. Scope refinement (not a downgrade): this is a SAME-SEAT multi-process hazard
TODAY (crons + lanes + seats all call publish_rib on one machine); two CLONED operators never share
the store file at all - memory/rib_bus/*.json are TRACKED (49 files), so cross-seat sync turns the
race into git merge/clobber. Either way the bus has no claim system; the N=2 headline overstates
locality but the mechanism and consequence stand.

GPS side: tools/gps_mcp/ledger.py SCHEMA_SQL (:132-142), PRIMARY KEY (model_id, task_shape) at
:141, no operator column - byte-checks. Live db3 opened READ-ONLY (sqlite3 mode=ro): capability
has exactly the 7 documented columns, 30 rows; verdict_log 703 rows (ts 2026-09-30T01:24:56Z to
2026-10-05T07:15:15Z), 13 distinct models. tools/gps_mcp/router.py: MOMENTUM_RANK is at **:50**
(:44 is the LM7 comment intro; lens cite off by 6 lines - substance correct, the rank reads stored
verdict history). Deliberate-unwired state byte-checks: watch/inbox/NIGHT_SHIFT_20261005_CLOSE.md
"Decisions owed to the operator" #2 (epoch stamping "Deliberately NOT stamped overnight ... the
operator's call") and #3 ("Router wiring: the router still reads stored pass_rate; wiring it to
effective rates (metabolism) is one import away and a separate act").

Evidence nit: the lens's "(grep for operator/tenant/lock over ledger.py+router.py returns only
'claimed hash' hits)" is garbled - my grep (`grep -inE 'operator|tenant|lock'`) returns 11 hits,
all prose/comments (ledger.py:78,95,329,358,588,590; router.py:44,326,331,519), none a schema
column or a lock primitive. Substance (no operator concept, no locking) stands; the grep
description does not.

## 4. FINDING 4 - CONFIRMED (one falsifier detail corrected; text arrived truncated)

Note: the finding's prose is cut mid-sentence in the ask ("so a fre..."); the verdict rests on the
evidence block, which is complete.

- mag/route_chat.py:241-243 dormant refusal - exact (`if lane_cfg.get("dormant") and not
  operator_go: raise RuntimeError(f"lane {lane} is DORMANT (B2-133 gate); " "operator GO required")`).
- mag/route_chat.py:238-240 unknown-lane raise - exact.
- configs/providers.yaml:62-64 "dormant is a declared STATE, not a failure" + `dormant: true` -
  exact. :170 `openrouter:` exact, api_key_envs 4-entry chain at :178
  [OPENROUTER_API_KEY, OPENROUTER_API_KEY_2, OR_API_KEY, OR_API_KEY_2] - exact. :298 groq, :359
  deepseek, :451 gemini - all exact.
- providers.yaml untracked (`git ls-files configs/providers.yaml` empty), since 5a6ffd806
  2026-08-20 - byte-checks .gitignore:23.
- Single-.env door: route_chat.py:56-72 `_keys_for` reads os.environ then falls back to the ONE
  `(ROOT / ".env")` (:67) - the lens's scoped claim confirmed by read.
- Falsifier correction: a fresh clone has NO configs/providers.yaml at all (clone test:
  PROVIDERS_MISSING; no example/template tracked anywhere under configs/ - `git ls-files configs
  | grep -i 'example\|template'` empty). So the clone dies at route_chat.py:51
  (`providers.yaml).read_text(...)` -> FileNotFoundError) BEFORE the :240 unknown-lane raise.
  "raises 'unknown lane' with no key ever read" is the wrong exception for the clone case; the
  dead-end is earlier and harder. The move (tracked providers.yaml.example) is still the right one.

## 5. PROCESS NOTES (honesty)

- The environment header said Shell: cmd.exe; the actual shell is git-bash. Two early cmd-style
  chains used `find /c /v ""`, which GNU find parsed as "walk C:\" - both tasks were killed within
  seconds, and their oversized logs (1.2GB + 2.4GB) deleted. No repo file was written by them.
- Remote reachability was NOT fetched (no network touch; AGENTS.md 302-SSO caution respected).
  All github/master claims come from local git objects only - same limitation the lens declared.
- Not run: any code against the verkle chain (lens blind spot 1 stands, still OWED); tutorial
  economics pricing (lens blind spot 5: my ledger probe - memory/runs/route_chat/usage.jsonl has
  19 rows, 8 mentioning deepseek; memory/runs/hermes_burn/usage.jsonl has 3,010 rows, no deepseek
  cost series - the ~5%-of-paid claim stays OWED with the instrument now named).
- db3 personal-data OWED (lens blind spot 4): RESOLVED this session - see Addition 3.

## 6. ADDITIONS (what the lens missed)

1. **The GitHub push physically fails before secrets even matter.** Tracked HEAD tree = 18.5 GB
   over 56,361 paths (`git ls-tree -r -l HEAD` census); 19 blobs >100MB and 4 blobs >2GB, led by
   watch/ESTATE_INDEX/ESTATE_INDEX.jsonl (2,406.1MB) and dashboard/data/ESTATE_INDEX.jsonl
   (2,406.1MB), attic/20260923_mimosa_rotation/hook-state_stale_baselines.tar (2,210.9MB),
   dashboard/data/ractor_board.jsonl.runaway-evidence-20260903 (2,129.3MB). GitHub rejects files
   over 2GB at the receive hook (and flags >100MB), so "push it to GitHub" is impossible as-is
   regardless of the lan.key question; the orphan-branch cut in finding 2's move must be a
   tree-level diet, not only a history rewrite. Falsifier: a `git push` of HEAD to a GitHub remote
   succeeding with the four >2GB blobs present. Move: give the spore manifest a max-blob rule
   (cut or pointer-ize >50MB; the four >2GB are non-optional), same sitting, +20 min.

2. **The secret gate already exists - ride it, do not rebuild it.** tools/secret_gate.py is
   TRACKED and has two modes with receipts: full tree 2026-09-27
   (watch/inbox/secret_gate_results/full_run_row.json: schema secret_gate_beat.v1, 2,356,207 files
   scanned, blocking_count 3,606, runtime_sec 49,256) and changed-scope 2026-10-05T11:27:35Z
   (changed_20261005T112735Z.json: 31 files, blocking 0). The spore manifest's fail-closed 0/1/2
   contract should be a scope_basis of THIS gate (scope_basis is already parameterized: "tree" vs
   "worktree+untracked"), not a new instrument. Falsifier: a leak ships while secret_gate
   spore-scope reads green. Move: add a "spore" scope_basis that emits the manifest sha256 set,
   ~45 min.

3. **db3 OWED resolved: the tracked GPS ledger is clean of personal data at my instrument.**
   Read-only probe (sqlite3 mode=ro): capability 30 rows / 7 columns exactly as SCHEMA_SQL;
   verdict_log 703 rows (2026-09-30 to 2026-10-05); 13 distinct models; username 'foste' hits = 0
   in EVERY column (cast-as-text LIKE), absolute local paths in evidence_source = 0. It ships
   without personal data; the manifest's db3 decision is a machine-state policy call, not a
   privacy call. Falsifier: a semantic read of the 703 evidence rows surfacing operator-identifying
   content the substring probe missed. Move: record the probe as the manifest's whitelist
   rationale, 10 min.

4. **Personal-identifier census the cut must own: 4,187 tracked files carry the username.**
   `git grep -Il foste | wc -l` = 4,187 (2,745 outside watch/), including TRACKED
   watch/inbox/SHARED_SURFACE_CONTRACT.json (canonical path "C:/Users/foste/..."), AGENTS.md,
   TOOLS.md. There is no "strip personal receipts" cut that survives unless the handle itself is
   accepted as pseudonym or rewritten. Falsifier: a spore branch with zero 'foste' hits while
   keeping AGENTS.md and the contract intact. Move: pseudonym-vs-scrub decision encoded as a
   manifest rule, ~30 min.

5. **The N=2..8 extension point already exists as a tracked machine contract.**
   watch/inbox/SHARED_SURFACE_CONTRACT.json (tracked, schema shared_surface.v1) defines 9 client
   aliases (mag_host, mag_container, openclaw, vscode, cursor, z_code, grok_powershell, codex,
   linux_or_wsl), read_first INDEX.json, and a machine validator
   (`.venv\Scripts\python.exe -m mag.shared_surface validate`) - a multi-SURFACE, single-OPERATOR
   protocol with zero operator axis. Multi-operator should be one new axis here (operator_id on
   receipts, per-operator INDEX namespaces), not a new protocol; it also partially answers the
   ask's question 5 - today the republic is a shared surface plus unshared forked state: receipts
   are the only thing that already crosses seats. Falsifier: the contract or the validator already
   carrying an operator concept. Move: extend shared_surface.v1 with operator_id + validator rule,
   ~45 min.

CONVERGENT flag (quantifier/duplication law): my executed clone-falsifier (Finding 1) and race
measurement (Finding 3) independently re-derive conclusions the sibling lenses in this same run
also reached (the spore dir carries 10 sibling lens reports plus a driver verifier
_verify_break.py, which byte-checks the lens cites with masked output). Those two upgrades outrank
single-source claims per the standing law.
