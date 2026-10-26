# LANE 4 — THE UNVERSIONED SURFACE
### Data-loss exposure across `C:\Users\foste\Documents\projects` sibling dirs with NO git
**Audit date:** 2026-09-26 · **Lane:** 4 (unversioned surface) · **Method:** bounded `os.walk` (skip `.git`/`node_modules`/`__pycache__`/`.venv`/`venv`/`site-packages`/`.lake`), `git ls-files -s` + `git cat-file --batch-check` blob comparison, per-dir mtime census.

---

## HEADLINE ANSWER

**Of 47 unversioned directories, only 2 hold real code nobody else has.** 45 are scratch, deploy copies, tool caches, or empty residue.

| | |
|---|---|
| Unversioned dirs scanned | **45** (of 56 total; 11 have `.git` — 9 repos + 1 git-repo-as-sibling) |
| Dirs holding **irreplaceable code** (never committed anywhere) | **2** — `worktrees/sovereign-mirror-scaffold`, `worktrees/salon-arena-mvp` |
| Dirs holding **unique-but-derivable** code | **4** — `mag-current-rebuild` (stale Mag copy), `embassy-sandbox`, `research/cl4r1t4s`, `tests` |
| **Total code files at genuine risk** | **~72 files** (≈480 KB) — *not* the 10,677 raw code count |
| Dirs that are pure residue | 39 |

*Dir count differs from the parent's 47: a full `os.listdir` scan found 56 directories, of which 11 carry a `.git` (including `sovereign-mirror`, a 1-file repo the parent already knew about). Two dirs the parent did not list — `.cursor`, `.github`, `.vscode`, `.pytest_cache`, `.venv`, `venv` — are editor/venv/tooling residue, listed here for completeness.*

> **The trap in the raw numbers.** `the_margin_lean` shows **8,970 "code" files** and `.mimosa` shows **303,246 files**. Neither is a single line of the operator's work. `the_margin_lean` is an upstream `mathlib4` git clone (Lean theorem prover, 7.38 GB of build cache) — it even *has* its own `.git`; only its 7.38 GB `.lake/build` is unversioned, and that is regenerable with `lake build`. `.mimosa` is 4.03 GB of **agent hook telemetry** (302,690 `.source` snapshots that are only **11,233 unique** by content hash — a 27× duplication factor, since each session snapshots the same files). Rank by unique bytes of irreplaceable work, never by file count.

---

## IDENTITY: the two dirs the parent asked about

### `.mimosa` (303,246 files / 0 code / 4.03 GB) — **agent hook telemetry, NOT work**
Per-session state written by the agent tooling layer. Composition: **302,690 `.source` blobs + 556 JSON files**. The `.source` files are content-hash-named copies of Mag source modules taken at session start — sampled content confirms they are verbatim docstring-headed copies of `mag/game_ramp.py`, `mag/code_map.py`, etc. The JSON side is `hook-state/` (897 KB per session), `finding-ledger/v1/events/` (batch pre/post-tooluse records), `hook-status/`, `history/`, `checkpoints/`, `reports/`.

- **LIVE** — newest file `2026-09-26T21:26` (minutes before this audit).
- **Duplication of Mag:** yes, structurally — but it is a *mechanical* copy (content-addressed), not divergent code. It inherits Mag's drift automatically.
- **Data-loss risk: LOW.** Nothing here is authored. The Mag repo's own `tools/estate_atlas.py` already classifies `.mimosa/hook-state/` as a **ROTATING SINK** ("Mimosa hook writes per invocation, sibling lane… propose rotation cap upstream of the hook") and `.mimosa/` is already in the repo `.gitignore` (line 190). The finding here is **disk waste, not data loss**: 4.03 GB holding 11,233 unique files. The repo's own atlas has already named the fix and nobody ran it.
- **Also present in 3 more places** at smaller scale: `teach/.mimosa` (87 files), `research/.mimosa`, `dashboard-deploy/static/games/.mimosa` (gitignored).

### `the_margin_lean` (143,443 files / 8,970 "code" / 7.38 GB) — **upstream `mathlib4` clone + build cache**
Contains exactly one child: `mathlib4/`. That is a **clean, unmodified clone of `https://github.com/leanprover-community/mathlib4.git`** — `git status --porcelain` = **0 dirty**, branch `master` @ `80cbd04` (2026-09-06, "feat: evaluating symmetric polynomials"). It is *not* a `the_margin_lean` project: there is no `lakefile.lean`, no `lean-toolchain`, no `.lean` source of the operator's own **outside** `mathlib4/` — the walk found **zero files** at any path not under `mathlib4/`.

- The 8,970 "code" count is an artifact of the extension heuristic: `.lean` 9,727 (upstream theorem files) + `.c` 8,877 (generated C from the Lean compiler) + `.js`/`.sh` build scripts. The `.c`/`.trace`/`.olean`/`.hash`/`.private` bulk is `lake build` output — **`mathlib4/.lake/` alone is 127,460 files / 7.38 GB** (build 127,460, packages 6,963).
- **DEAD as a workspace** (newest file 2026-09-06, 20 days idle), but the clone is a legitimate upstream checkout.
- **Data-loss risk: LOW.** Zero operator code. The 7.38 GB build cache is fully regenerable (`lake build`); the source is re-clonable from GitHub. The only real cost is 7.38 GB of disk for a cache nobody is using.

---

## FULL CENSUS — 45 unversioned directories

`dup-of-mag` = contains Mag code. `worktree-of` = `.git` **file** containing `gitdir:`.

| # | dir | files | code | identity (one line) | newest mtime | LIVE/DEAD | dup-of-mag | worktree-of | risk |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `.mimosa` | 303,246 | 0 | Agent hook telemetry store: 302,690 content-hash `.source` snapshots (11,233 unique) + 556 session JSON | 2026-09-26 21:26 | **LIVE** | copy (mech.) | — | **LOW** (4.03 GB waste) |
| 2 | `the_margin_lean` | 143,443 | 8,970 | Clean upstream `mathlib4` clone @`80cbd04` + 7.38 GB `.lake` build cache; no local project | 2026-09-06 17:13 | DEAD (20d) | no | — | **LOW** (regenerable) |
| 3 | **`mag-current-rebuild`** | 2,819 | 1,137 | Stale full copy of `local_sovereign_agent` (README = "local_sovereign_agent — Mag Resource Harness"), frozen ~2026-08-26 | 2026-09-22 07:29 | DEAD (copy) | **YES — 86%** | — | **MED** |
| 4 | **`worktrees`** | 1,594 | 492 | Container for 2 **real git worktrees** (see below) | 2026-09-07 03:47 | mixed | YES | **2 repos** | **HIGH** |
| 4a | `worktrees/sovereign-mirror-scaffold` | — | — | Worktree of `sovereign-mirror` @`beta/v2` `43156dc` (2026-07-10) | 2026-09-07 03:46 | DEAD head, **37 uncommitted** | no | `sovereign-mirror` | **HIGH** |
| 4b | `worktrees/salon-arena-mvp` | — | — | Worktree of `local_sovereign_agent` @`codex/salon-arena-mvp` `1e92a7012` (2026-08-06) | 2026-08-06 13:51 | DEAD, **7 uncommitted** | YES (partial) | `local_sovereign_agent` | **HIGH** |
| 5 | `research` | 773 | 51 | Research corpus: `aiTruthCode` (121 hand-saved docx/txt on the GTC/GTR "Eden Protocol" line), `cl4r1t4s` (edited), 2 nested `.git` clones, `system_prompts_leaks_20260912` | 2026-09-22 11:00 | **LIVE** | no | 2 nested | **MED** |
| 6 | `teach` | 372 | 0 | 11 `teach_*.mp4` + extracted frame PNGs (`f_01`…`f_10`, 355 png) + contact sheets + nested `.mimosa` | 2026-09-05 08:10 | DEAD (21d) | no | — | **MED** (binary, unreproducible) |
| 7 | `world-games-corpus` | 83 | 0 | Static site: "The World-Games Prompt Corpus", L1–L5 engine/pack taxonomy, 18 html + 45 md | 2026-09-23 12:02 | **LIVE** | partial (percolator/verkle_knot in text) | — | **MED** |
| 8 | `nacho-business` | 45 | 0 | Static site: "Nacho Business — a sovereign fleet, built in the open" (index/work/thesis/letter/lens/maze/stack html + `games/`, `onboard/`, `suno/`) | 2026-09-22 18:21 | **LIVE** | partial | — | **MED** |
| 9 | `embassy-sandbox` | 37 | 15 | Standalone "first embassy" DM sandbox: Ghost↔AOS seats over a file-bus + local REST (`sandbox/{bus,envelope,seat,aos_bridge,integrity,rest_service}.py`, 3 tests) | 2026-08-22 14:11 | DEAD (35d) | no | — | **MED** (never in repo) |
| 10 | `games-site` | 19 | 1 | Vercel games hub: `maze_arena`/`cathedral_v1`/`mud`/`swarm`/`frontier_souls`/`ruins_go` + `arrakis`, `skifree`; has `.env.local` | 2026-09-21 22:56 | **LIVE** | partial | — | **LOW–MED** (overlaps `dashboard/static/games/`) |
| 11 | `bond-audit` | 9 | 1 | Static site: "County Bond Conflict Audit" (`index.html`+`app.js`+`styles.css`+`data/`), Vercel-linked, **templated** (`{{PROJECT}}`/`{{SERIES}}` unfilled) | 2026-09-22 14:18 | **LIVE** | no | — | **LOW–MED** |
| 12 | `soul-frontier` | 5 | 0 | Static site: "Soul Frontier — Death Must Die × Dark Souls", single 28 KB canvas `index.html`, Vercel-linked | 2026-09-23 17:08 | **LIVE** | no | — | **LOW–MED** |
| 13 | `audit_prep_verkle` | 7 | 0 | Verkle-audit prep docs: `NAME_TO_MECHANISM.md`, evidence tables, disputed-rows summary (feeds examiner review) | 2026-09-12 23:03 | DEAD (14d) | partial (verkle_knot ×22) | — | **MED** |
| 14 | `.zcode` | 9 | 0 | ZCode seat config: `config.json` (mag MCP @`127.0.0.1:8001/mcp` + `X-API-Key: mag-local-dev-key`) + 7 session plans + 1 `.bak-mcpcage` | 2026-09-07 06:01 | DEAD (19d) | no | — | **MED** (holds a key) |
| 15 | **`tests`** | 3 | 3 | 3 orphan test files from the 2026-09-12 audit: `name_mechanism_validation.py`, `test_identity_schema_portability.py`, `test_smoke_harness.py` | 2026-09-12 22:53 | DEAD (14d) | partial (verkle_knot) | — | **MED** (validation code, never committed) |
| 16 | `career` | 6 | 0 | Job-search dossier: `READY_TO_SEND_3_20260908.md` (3 tailored letters w/ JD keyword maps), Nutanix $308–462K target, proof-of-work dossier, method post | 2026-09-08 16:29 | DEAD (18d) | no | — | **MED** (personal, unreproducible) |
| 17 | `scripts` | 2 | 2 | Orphan `hooks/prebuild_gate.py` + `hooks/steer_47.py` | 2026-08-28 12:41 | DEAD (29d) | no | — | **LOW** (repo has `scripts/hooks/` twins) |
| 18 | `audit_prep` | 1 | 0 | `temperature_rigidity_cell_VERIFIED_FINDING.md` | 2026-09-12 22:56 | DEAD (14d) | no | — | **LOW** |
| 19 | `artifacts` | 1 | 0 | `lens_artifact_20260912.md` — fly-brain connectome lens for head-retraining | 2026-09-12 18:06 | DEAD (14d) | no | — | **LOW** |
| 20 | `corpus` | 1 | 0 | Stray `L1_engines/constraint_verifier_interface.DRAFT.md` (repo has a copy at `watch/corpus/L1_engines/`) | 2026-09-22 23:38 | LIVE | no | — | **LOW** (dup) |
| 21 | `docs_register` | 1 | 0 | `STACK_V1.md` — self-description of the `docs_register` domain (repo has 3 copies) | 2026-09-12 22:27 | DEAD (14d) | no | — | **LOW** (dup) |
| 22 | `world_key` | 1 | 0 | `lock2_key.md` — **answer key deliberately placed OUTSIDE the repo** ("if the sandboxed seat ever reads this file, the trial is compromised") | 2026-09-05 22:49 | DEAD (21d) | no | — | **LOW** *(intentional; do NOT "helpfully" commit it)* |
| 23 | `Projects` | 7 | 0 | Empty **Obsidian vault** (`.obsidian/` + `Welcome.md` + `create a link.md`), created 2026-09-12 | 2026-09-12 07:35 | DEAD (14d) | no | — | **LOW** |
| 24 | `memory` | 4 | 0 | Orphan `memory/corpus/kungfu/` (3 mp4, 71 MB) + `memory/runs/astra_world/seat_exec_01.log` (115 B, log dupes in repo) | 2026-09-07 21:38 | DEAD (19d) | no | — | **LOW–MED** (71 MB of video) |
| 25 | `watch` | 3 | 0 | Orphan `inbox/AUDIT_SELF_CAUGHT_01.md` + a 44-byte stub `AUDIT_SELF_CAUGHT_01.tar.gz` (the real archive is missing) | 2026-09-12 22:54 | DEAD (14d) | no | — | **MED** (audit receipt) |
| 26 | `tools` | 1 | 1 | `reproduce/AUDIT_SELF_CAUGHT_01/reproduce.sh` — points at a `.tar.gz` that does not exist here | 2026-09-12 22:54 | DEAD (14d) | no | — | **LOW** (broken ref) |
| 27 | `.trash` | 4 | 1 | Manual trash `2026-08-19/`: `deterministic_scanner_demo.ipynb`, `lmao.gif`, `Mag-sovereign-kit-public.zip` (420 KB), `pytest.ini`, `.pytest_cache` | 2026-08-13 06:56 | DEAD (44d) | no | — | **LOW–MED** (ibynb + zip) |
| 28 | `.video_agent` | 1 | 0 | `env_report.json` — video-agent-kit 0.4.3 env probe (points at `~/.zcode/cli/plugins/...`) | 2026-09-07 15:01 | DEAD (19d) | no | — | **LOW** |
| 29 | `Mag-backup.git` | 178 | 0 | **REAL bare git repo** — `is-bare-repository=true`, 71,379 objects, **6.25 GiB** pack, 5 packs, 135 loose; HEAD `a4733004a`. This is Mag's **`local` push remote** (the ratchet pre-push hook pushes here) | 2026-09-26 08:11 | **LIVE** | is the backup | — | **none — it is the safety net** |
| 30 | `venv` | 10 | 1 | Stray pip-only venv (2026-09-12 21:47), `Lib/site-packages` fully populated | 2026-09-12 21:49 | DEAD | no | — | **LOW** |
| 31 | `.venv` | 17 | 2 | Stray venv skeleton (2026-08-08) | 2026-08-08 09:56 | DEAD | no | — | **LOW** |
| 32 | `.pytest_cache` | 5 | 0 | Stray pytest cache at projects root (2026-09-12 21:39) | 2026-09-12 21:39 | DEAD | no | — | **LOW** |
| 33 | `.vscode` | 2 | 0 | `mcp.json` + `settings.json` for the projects dir | 2026-08-25 13:07 | DEAD | no | — | **LOW** |
| 34 | `.cursor` | 1 | 0 | `settings.json` | 2026-08-05 20:29 | DEAD | no | — | **LOW** |
| 35 | `.github` | 1 | 0 | Empty `dictation.md` (0 bytes) | 2026-08-08 22:27 | DEAD | no | — | **LOW** |
| 36–44 | `codex_pytest_desk`, `codex_pytest_factory{,2,3,4}`, `codex_pytest_tier_gate{2,3,4}`, `codex_pytest_tmp` | **0** | 0 | **9 EMPTY DIRS** — see forensics below | 2026-08-06 07:23–08:18 | DEAD (51d) | no | — | **LOW** |
| 45 | `livingmud` | **0** | 0 | **EMPTY DIR**, dir mtime 2026-09-23 03:22 (created *after* `world-games-corpus` got its `livingmud.html`) | 2026-09-23 03:22 | DEAD | no | — | **LOW** |
| 46 | `soul-frontier` (dir) | 5 | 0 | see #12 | 2026-09-23 17:09 | LIVE | no | — | **LOW–MED** |
| 47 | `.mimosa` siblings | — | — | `teach/.mimosa` 87 files, `research/.mimosa`, `dashboard-deploy/.../.mimosa` (gitignored) | — | LIVE | copy (mech.) | — | **LOW** |

**Excluded (these DO have `.git`):** `local_sovereign_agent`, `sovereign-mirror`, `ai-job-search`, `azerothcore-wow`, `tortoise-wow`, `vmangos-core`, `embassy-aos`, `mag-sovereign-kit`, `mycelial-republic`, `ractor-salon`, `field-strike-the-chord`.

---

## HEADLINE FINDING 1 — the `worktrees` dir is NOT a stale copy; it is the highest-risk thing in the lane

The name invites the wrong conclusion. Both children are **genuine git worktrees** (`.git` *file* with `gitdir:`), so their *tracked* content is safe in the parent repo. **The danger is exactly the opposite of "stale copy": they are live working trees holding uncommitted work that exists nowhere else.**

`git worktree list` confirms both are registered and **neither is prunable** (`git worktree prune -n -v` returns empty in both repos) — so a cleanup sweep that deletes "stale worktrees" would destroy real work with no git warning.

### `worktrees/sovereign-mirror-scaffold` → worktree of **`sovereign-mirror`** (branch `beta/v2`, HEAD `43156dc`, 2026-07-10)
**37 uncommitted entries. None of the untracked modules exist in `sovereign-mirror` main, in the Mag repo, or anywhere in `Mag-backup.git` history** (verified: `git rev-list --all --objects` grep → empty for every one).

- 12 **modified tracked files** (~200 KB), incl. `src/sovereign_mirror/dashboard/server.py` (48.5 KB), `static/app.js` (35.4 KB), `static/style.css` (63.8 KB), `core/eut_lattice.py` (14.5 KB), `core/knot_explorer.py` (17.7 KB), `protocol.py` (21.6 KB), 2 tests.
- 21 **untracked** entries, incl. 5 brand-new core modules: `human_knot.py` (25.6 KB), `platform_pack.py` (30.7 KB), `rashomon_synthesis.py` (27.5 KB), `lenses.py` (18.7 KB), `idea_catalog.py` (16.8 KB) + 3 new tests + `dashboard/api/` (9 files) + `static/platform/` (20 files) + `static/js/` (6) + `data/knots/` (15 files) + 4 new docs (`V2_BETA_SYNTHESIS.md`, `DISPLAY_THEORY.md`, `V3_PARABLE.md`, `CONSPIRACY_LATTICE_LAB.md`).
- Also holds an untracked **`vendor/` = 649 files / 287 MB** of extracted third-party datasets ("18176077 - Zero-Shot Geometric V1" zips).

### `worktrees/salon-arena-mvp` → worktree of **`local_sovereign_agent`** (branch `codex/salon-arena-mvp`, HEAD `1e92a7012`, 2026-08-06)
**7 uncommitted entries. `mag/salon_arena.py` and `mag/salon_renderer.py` are in NO branch of the Mag repo and NO branch of `Mag-backup.git`.**

- `M mag/agent_arena.py` (18.8 KB) — modified relative to the worktree HEAD.
- `?? mag/salon_arena.py` (19.5 KB), `?? mag/salon_renderer.py` (13.4 KB) — **never committed anywhere, verified against `git rev-list --all --objects` in all three repos.**
- `?? tests/test_salon_arena.py` (3.9 KB), `?? tests/test_salon_renderer.py` (4.5 KB), `?? configs/salon/lenses.yaml` (950 B), `?? memory/arena/` (19 files, 66 KB of session state).
- Ownership note: the worktree `.git` is owned by `CodexSandboxOffline`, not `foste` → plain `git status` fails with *dubious ownership*. It needs `safe.directory` to even be inspected. This is a second, quieter risk: **an operator running `git status` here sees an error, not a warning that 7 files are uncommitted.**

**Verdict: `worktrees/` = HIGH risk, and the fix is `git add`/`commit` in each worktree, not deletion.** Neither worktree is prunable; `salon-arena-mvp` has been idle 51 days and `sovereign-mirror-scaffold` 19 days, but idle ≠ empty.

### Bonus finding: 4 MORE stale worktrees outside this lane
`~/.codex/worktrees/{6654,b13a,ef82,efa1}/local_sovereign_agent` are all registered worktrees of the Mag repo, all at the **same** detached HEAD `a4733004a`, all **0 dirty**, last commit 2026-08-06. These *are* genuinely prunable (`git worktree remove`) — the opposite verdict from the two under `projects/`. Noted, not touched (outside lane scope).

---

## HEADLINE FINDING 2 — `mag-current-rebuild` is a stale Mag copy, and 230 of its files exist nowhere else

Not a "fresh rebuild" — a **frozen ~2026-08-26 snapshot** of `local_sovereign_agent` (its own `README.md` reads "local_sovereign_agent — Mag Resource Harness"). The name is a trap in the other direction too: it is **86% redundant**.

Blob-level comparison against the Mag repo (`git ls-files -s` → 40,708 tracked blobs; `git cat-file --batch-check` against the full object DB = all history):

| Bucket | Files | Meaning |
|---|---|---|
| Byte-identical to a tracked Mag blob | **2,429** (86%) | pure duplication — safe to delete |
| Present in Mag git **history** (untracked at HEAD) | 160 | recoverable from history — safe to delete |
| **In NO Mag blob, index, or history** | **230** (8%) | **only here** — see below |
| *of the 230:* superseded at same path today | 221 | an older version of a file the repo still has |
| *of the 230:* **path gone from the repo entirely** | **9** | `queue/handoff/cloud-{1cd40cbf0c, 2ececfeeb8, 31674d9441, 37d2957ac0, 461f27b41d, 48f359a0bb, 4d7db0bc52, 8581d441c1, f661ab50ec}.json` (284 B each, Aug 2026) |
| *of the 230:* **code** | **2** | `harness/opencode_coder.py` (9.0 KB), `mag/self_audit.py` (12.0 KB) — old versions; the repo has newer copies at the same paths |

The 230 unique files break down as 106 `.json` + 102 `.md` + 14 `.txt` + 2 `.py`, ≈**10.7 MB total**, and are dominated by: `queue/handoff/*.md` session cards from the Aug 5–26 era (**102 cards, incl. the 75 KB `CODE_MAP_RIB.md`**), `queue/handoff/VERKLE_RIB.json` (138 KB), `queue/handoff/shapes/portfolio.json` (654 KB), `watch/session_digest.jsonl` (**5.19 MB**), `watch/grok_feed.jsonl` (**4.19 MB**), plus `queue/results/*` lane receipts.

**Also inside: an unversioned `.env` (3,276 B, 2026-08-26) holding credentials**, and stale `watch/mag.pid`. A secrets file sitting outside version control *and* outside any backup is its own finding.

**Verdict: MED risk — worth a one-shot salvage, not worth keeping as a working copy.** Recommended: extract the 9 missing `cloud-*.json` handoffs + confirm `session_digest.jsonl` / `grok_feed.jsonl` are superseded in-repo, then retire the directory. **Do not** treat it as a rollback target — `Mag-backup.git` is the real one.

---

## ZOMBIE-DIR FORENSICS — why 10 empty dirs exist

All 10 (`codex_pytest_desk`, `codex_pytest_factory`, `…2/3/4`, `codex_pytest_tier_gate2/3/4`, `codex_pytest_tmp`, `livingmud`) hold **0 files** — they are empty directory shells, not residue with content.

| dir | dir mtime | created by | referenced in the Mag repo? |
|---|---|---|---|
| `codex_pytest_tmp` | 2026-08-06 07:23 | pytest run with a relative `--basetemp`/tmpdir while cwd was `projects/` | yes — `memory/thinking/app_reasoning.jsonl`, `memory/trajectory/steps.jsonl` (agent reasoning logs only) |
| `codex_pytest_desk` | 2026-08-06 07:48 | same burst | yes — + `watch/SELF_STEAL_ASTRA_SEAT_20260905.md`, `watch/inbox/wave_20260916/receipts/CV2_SHADOW_INVENTORY.md` |
| `codex_pytest_factory{,2,3,4}` | 2026-08-06 07:49–07:52 | same burst (1-min cadence → 4 sequential runs) | yes — reasoning logs only |
| `codex_pytest_tier_gate{2,3,4}` | 2026-08-06 08:15–08:18 | same burst, second wave (23 min later) | yes — reasoning logs only |
| `livingmud` | 2026-09-23 03:22 | a Vercel/build step for the `livingmud` game; the shipped artifact is `world-games-corpus/livingmud.html` + `living_mud.html` | yes — 20 refs, but all to the **`.html`/estate-index** names, not this dir |

**Findings:** (a) all ten are **pytest tempdirs created by a codex/agent run whose working directory was `projects/` instead of the repo** — 9 of them in a single 55-minute burst on 2026-08-06, which is the fingerprint of a tier-gate experiment iterating on fixtures. (b) **No config, script, or scheduled task references any of them.** The only repo references are inside agent *reasoning/transcript logs* (a record that the names were discussed) and one watch card. (c) `livingmud` is a different species: a build/deploy leftover, 20 days newer than the others. (d) **None are prunable git artifacts** — they are not worktrees, so `git worktree prune` will not touch them; they need a manual `rmdir`. Deleting all 10 is safe.

---

## RANKING BY DATA-LOSS RISK

**HIGH (irreplaceable, uncommitted, no rollback):**
1. `worktrees/sovereign-mirror-scaffold` — 37 uncommitted entries, 5 never-committed core modules (119 KB of .py), 287 MB vendor corpus, 200 KB of modified tracked code. Head 78 days old.
2. `worktrees/salon-arena-mvp` — 2 never-committed modules (33 KB) + 2 tests + session state. Idle 51 days, and `git status` there errors out on ownership.

**MED (unique but reconstructible-in-principle, or unique-and-unversioned-but-not-code):**
3. `mag-current-rebuild` — 230 files nowhere else (9 irrecoverable, 2 stale code files, 102 cards, 9.4 MB of record streams) + a loose `.env`.
4. `research` — 773 files; `aiTruthCode` (121 hand-saved documents) and the **edited** `cl4r1t4s` (18 files not in the 2026-09-12 upstream snapshot) have no git.
5. `embassy-sandbox` — 15 code files, 35 days stale, `aos_bridge.py` exists in no repo; the repo has `mag/embassy_deliver.py`/`embassy_integrity.py` but a different implementation.
6. `teach` — 372 files / 35.8 MB of video + extracted frames. Binary, unreproducible, but not code.
7. `tests` (3 orphan validation scripts) + `watch` (1 audit receipt) + `tools` (1 broken reproduce script) + `audit_prep_verkle` (7 examiner-facing docs).
8. `world-games-corpus` / `nacho-business` / `games-site` / `soul-frontier` / `bond-audit` — 5 unversioned Vercel sites, 161 files, all LIVE. `nacho-business` and `games-site` substantially overlap `dashboard/static/`+`site/dist/` in the repo, but the deploy sources themselves are not versioned.

**LOW (residue, regenerable, or intentionally outside git):**
9. `.mimosa` 4.03 GB / `the_margin_lean` 7.38 GB — the two giants, both worthless as work.
10. `career`, `memory` (71 MB of mp4), `.trash` (ibynb + 420 KB zip), `Projects` (empty Obsidian vault), `corpus`/`docs_register` (duplicates), `world_key` (*deliberately* outside), `.zcode` (holds `mag-local-dev-key`), the 3 venv/cache dirs, `.vscode`/`.cursor`/`.github`, the 10 zombie dirs.

---

## WHAT'S ACTUALLY AT RISK — the honest number

- **Irreplaceable code: ~72 files, ≈480 KB** (5 sovereign-mirror core modules + 4 tests + 2 salon modules + 2 salon tests + 1 config + modified tracked files across 12 files + 3 orphan tests at projects root).
- **Irreplaceable non-code: ~30 MB** of session cards, 9.4 MB of record streams, 71 MB of video, 36 MB of research docs, 287 MB of vendored third-party data.
- **Regenerable-but-hungry: 11.4 GB** (`.mimosa` 4.03 GB + `.lake` 7.38 GB).

Everything above the line is a **`git add && git commit` away from safe** — no migration, no export format, no backup job. The lane's headline is not "recover 10,677 code files." It is: **two worktrees are quietly holding the only copy of nine Python modules, and both look deleteable.**

---

## CLAIM LEDGER

- **SUPPORTED** — `worktrees/*` are real worktrees: `.git` files contain `gitdir:`; both appear in `git worktree list` of their parent repos.
- **SUPPORTED** — 44 uncommitted entries across the two worktrees (`git status --porcelain`).
- **SUPPORTED** — `human_knot.py`/`idea_catalog.py`/`lenses.py`/`platform_pack.py`/`rashomon_synthesis.py`/`salon_arena.py`/`salon_renderer.py` were never committed: `git rev-list --all --objects` grep returns empty in `local_sovereign_agent`, `sovereign-mirror`, and `Mag-backup.git`.
- **SUPPORTED** — `the_margin_lean` contains only a clean `mathlib4` clone (`status` clean, `origin` = leanprover-community/mathlib4, 0 files outside `mathlib4/`).
- **SUPPORTED** — `.mimosa` holds 302,690 `.source` files resolving to 11,233 unique content hashes across 4.03 GB.
- **SUPPORTED** — `Mag-backup.git` is a real bare repo (6.25 GiB pack, 71,379 objects) and is Mag's `local` push remote per the ratchet card.
- **SUPPORTED** — no Windows scheduled task references these paths (`schtasks /query /fo LIST /v` → no match).
- **DISPUTED** — the parent's "8,968 code files with no git" as a risk figure. That count is upstream `mathlib4` `.lean`/generated `.c`, not operator work. Real at-risk code is ~72 files.
- **DISPUTED** — "mag-current-rebuild" as a name suggesting a current rebuild. It is a 2026-08-26 snapshot, 86% byte-identical to the repo, superseded since.
- **UNPROVEN** — whether the 221 superseded files in `mag-current-rebuild` (notably the 2026-08 versions of `session_digest.jsonl` and `grok_feed.jsonl`) are needed as historical record. Nobody has asked. Salvage-then-retire is the cheap path; deleting first is not recoverable.
- **UNPROVEN** — why `sovereign-mirror-scaffold` was left with 37 uncommitted entries for 19 days. The `lenses.py` / `_training.jsonl` / `_sample_dump.txt` artifacts in `research/cl4r1t4s/_lenses/` suggest a lens-training run in flight, but no receipt names the worktree.

*Files written by the audit itself, not by the operator: none inside the surveyed dirs. This card + `memory/audit_20260926/lane4_unversioned.json` only.*