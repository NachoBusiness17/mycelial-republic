# LANE 4B — UNVERSIONED RISK: which sibling dies tonight

**Date:** 2026-09-27 (box clock) · **Mode:** REPORT ONLY. Nothing fixed, moved, deleted, or committed.
**Scope:** `C:\Users\foste\Documents\projects` — **57 sibling directories** (48 from a plain `*/` glob, plus 9 dot-directories: `.cursor .github .mimosa .pytest_cache .trash .venv .video_agent .vscode .zcode` that the glob hides), of which **34 hold content with no version control at all** and 13 are versioned.
**Method:** bounded `os.walk` with pruned `.git`/`.mimosa`/`.venv`/`node_modules`; SHA-1 uniqueness vs the tracked set of every git repo on the box; per-repo `git status`; `du -sh` on git dirs.
**Instruments:** `lane4b_census.py` (52.43 GB walked, **0 walk timeouts**), `lane4b_links.py` (reparse-point probe), `lane4b_shadow.py`, `lane4b_uniq2.py` (73,198 tracked files hashed, 68,939 distinct), `lane4b_rebuild2.py`.

---

## THE ANSWER

**If exactly one unversioned directory is lost tonight, `mag-current-rebuild/` hurts most.** Not the biggest — 69 MB, rank 10 by size. It is the only unversioned directory holding **a working copy of the fleet's own runtime**: 1,081 `.py` files including 117 `mag/*.py` core modules that exist in **no commit, on any branch, in any bare backup** — plus 9.4 MB of unique append-only session and model-feed ledgers. Every other unversioned sibling is either regenerable (`the_margin_lean` is a mathlib4 clone), bulk media with a re-recordable source (`teach`, `memory`), or bytes already tracked elsewhere (`nacho-business`, `world-games-corpus` are ~99% duplicates of `dashboard/static/games/`).

`mag-current-rebuild` is 1-1 reproducible in the trivial sense that someone *could* rebuild it from the repo — but then they would be rebuilding today's 1,081-file working state, not the Aug-12→Aug-26 state these files are, and the 117 modules have no commit at all. It is the one directory where losing it means **losing code that was never anywhere else**.

---

## 1. SIBLING CENSUS — 57 dirs, 13 versioned, 34 unversioned-with-content

Full byte/file/newest table: `memory/audit_20260926/lane4b_risk.json` → `siblings[]` (57 entries).

### Versioned (13) — safe by construction

| dir | HEAD | commit date | notes |
|---|---|---|---|
| `local_sovereign_agent` | `e73b60c54` | 2026-09-27 | **1,885 uncommitted entries — see §4** |
| `azerothcore-wow` | `f68a975` | 2026-09-15 | vendored upstream, re-clonable |
| `tortoise-wow` | `d886113` | 2026-09-14 | vendored upstream |
| `vmangos-core` | `8f4e608` | 2026-09-15 | vendored upstream |
| `ai-job-search` | `120f476` | 2026-09-21 | clean, has GitHub remote |
| `ractor-salon` | `438a1c0` | 2026-09-16 | 1 untracked: `salon_fiber_20260916/` |
| `sovereign-mirror` | `9777f4e` | 2026-07-10 | + 37-dirty linked worktree (§4) |
| `mag-sovereign-kit` | `f7593d3` | 2026-08-02 | |
| `mycelial-republic` | `dc66499` | 2026-08-20 | |
| `embassy-aos` | `210432e` | 2026-08-22 | |
| `field-strike-the-chord` | `dc626fe` | 2026-06-09 | |
| `Mag-backup.git` (bare) | `a4733004a` | — | 6.25 GiB pack, **438 behind** |
| `Mag-prewipe-backup-20260927.git` (bare) | `6d417abd5` | 2026-09-26 | **1 behind** — closest mirror of the repo |

### Unversioned, ranked by ACTUAL data-loss risk (34 with content; 10 more are empty)

| # | dir | size | unique | risk | why |
|---|---|---|---|---|---|
| **1** | **`mag-current-rebuild`** | 69.4 MB | **13.8 MB** | **CRITICAL** | no `.git`; 117 `mag/*.py` + unique `session_digest.jsonl` (5.2 MB) / `grok_feed.jsonl` (4.2 MB) |
| **2** | `research` | 30.4 MB | **7.9 MB** | **HIGH** | `aiTruthCode/` — 55 hand-curated dirs, hand-named GTC/GTR doc lineage, no provenance file, no `.git` |
| **3** | `memory` | 71.2 MB | **71.2 MB (100%)** | **HIGH** | 3 `kungfu/*.mp4` (46/21/4 MB) — 0% duplicated, 0% regenerable |
| **4** | `teach` | 35.8 MB | **35.8 MB (100%)** | **HIGH** | 11 `teach_*.mp4` + 355 PNGs — recorded sessions, no master, no `.git` |
| **5** | `world_key` | 3 KB | 3 KB | MED-HIGH | `lock2_key.md` (3,012 B) — key material prose, **single copy, no `.git`** |
| **6** | `career` | 28 KB | 28 KB | MED | 6 hand-written application/POW docs (2026-09-08), no `.git` |
| **7** | `embassy-sandbox` | 90 KB | 90 KB (100%) | MED | 37 files, self-contained, 0% elsewhere |
| **8** | `soul-frontier` | 28 KB | 28 KB (100%) | MED | `index.html` (28 KB) hand-built + `.env.local` (**unversioned**) |
| **9** | `games-site` | 0.56 MB | 0.12 MB | MED | `ruins_go_engine.js` + `cathedral_v1.html` unique; `.env.local` unversioned |
| **10** | `audit_prep_verkle` | 36 KB | 36 KB (100%) | LOW-MED | 7 verkle audit artifacts, 0% elsewhere |
| **11** | `world-games-corpus` | 2.8 MB | 0.03 MB (1.2%) | LOW | 98.8% already in the repo's `dashboard/static/games/` |
| **12** | `nacho-business` | 8.8 MB | 0.02 MB (0.2%) | LOW | games dup; 4 Suno MP3s ARE the only unique part but are re-generatable from a prompt |
| **13** | `bond-audit` | 32 KB | 0.8 KB | LOW | |
| **14** | `the_margin_lean` | 219.5 MB | ~0 | **NONE** | it IS a `mathlib4` clone (10,056 `.lean` files, clean git) — fully re-clonable |
| — | `.mimosa`, `venv`, `.venv`, `.trash`, `.pytest_cache`, `.cursor`, `.github`, `.vscode`, `.zcode`, `Projects`, `artifacts`, `docs_register`, `audit_prep`, `corpus`, `scripts`, `tools`, `tests`, `.video_agent`, 9× empty `codex_pytest_*`, `livingmud` | — | — | **NONE** | tool config, caches, or 0-byte/empty dirs |

**No junction found.** I probed all 57 siblings for `FILE_ATTRIBUTE_REPARSE_POINT` (0x400) — none. The top-level `memory/`, `research/`, `watch/`, `corpus/`, `artifacts/`, `audit_prep`, `tests/`, `tools/`, `scripts/` that share a name with a repo subdirectory are **real separate directories, not mirrors**. `lane4b_shadow.py` compared them by content hash: **0 of 4 files in `memory/`, 0 of 771 in `research/`, 0 of 3 in `watch/` exist in the same-named repo directory.** The names are coincidence, not linkage.

---

## 2. RISK SCORE — what the evidence says

### `mag-current-rebuild/` — CRITICAL

- **No `.git`, no backup, no remote.** Nothing in `projects/` indexes it; the two bare mirrors are `local_sovereign_agent` mirrors, not of this tree.
- **2,702 of 2,819 files have a repo counterpart at the same relative path. 117 do not — 464 KB of pure-new code:**
  `mag/quest_party.py`, `mag/mirror_persona.py`, `mag/scrum_loop.py`, `mag/phase_lift.py`, `mag/focus_anchor.py`, `mag/living_map.py`, `mag/self_recurse.py`, `mag/frontier_pennies.py`, `mag/reach_protocol.py`, `mag/hero_journey.py`, `mag/phase_lift_real.py`, `mag/invariant_frontier.py`, `mag/grok_carrier.py`, `mag/expectations_monitor.py`, `mag/disentangle.py`, `mag/player_invariant_map.py`, `mag/cache_field.py`, `mag/reach_loop.py`, `mag/mem_state_feed.py`, `mag/moonshot_digital_twin.py`, `mag/table_turn.py`, `mag/provenance_router.py`, `mag/tesuji_steal.py`, `mag/rib_launcher.py`, `mag/sol_seat.py`, `mag/human_readable.py`, `mag/gemini_mine.py`, `mag/rib_render.py`, + 89 more.
- **13.8 MB unique overall**, of which the two largest are **append-only ledgers**: `watch/session_digest.jsonl` (5,189,224 B) and `watch/grok_feed.jsonl` (4,188,035 B). Ledgers are by construction un-rewritable — there is no "re-run the job" for a record of a run that already happened.
- **Recency:** newest file 2026-09-22; the unique modules date 2026-08-04 → 2026-08-18. Dormant ~5 weeks but not dead.
- **Carries `.env` (3,276 B)** — stat only, contents never read, never printed. No git repo, so nothing protects it beyond the disk.
- **Cost of loss:** 117 modules of unreleased code + ~9.4 MB of historical session/model-feed tape. Days-to-weeks of re-derivation for the code; **unrecoverable** for the tape.

### `research/` — HIGH
- 30.4 MB, no `.git` at the `research/` level. Two *nested* repos are versioned (`cl4r1t4s_upstream_20260912` 5.9 MB, `system_prompts_leaks_20260912` 21 MB — both re-clonable from GitHub).
- The unversioned part is `aiTruthCode/` (7.6 MB, 55 hand-named directories, 121 files) + `cl4r1t4s/` (2.1 MB) = **7.9 MB / 139 files unique, 0 duplicated**.
- Content is a hand-curated document lineage — `4 Horseman/GTC-v95.6 _ GTR-v7.1 Eden Protocol` (622 KB), `THE REUNION SYMPHONY/GTC-GEE_v81.3` (591 KB), `Chris Beck doctoral thesis.../GTC SYSTEM PACK Baseline GTR-v2 to GTR-v118.txt` (460 KB). Names like these are **operator-authored or hand-categorised**: a glob cannot re-derive them, and there is no README or manifest recording where any of it came from.
- **Not regenerable.** No upstream to re-clone; the versions are versioned by *name* and the lineage is the value.

### `memory/` and `teach/` — HIGH (100% unique, 0% regenerable)
- `memory/corpus/kungfu/`: 3 MP4s totalling **71.2 MB**, all unique, none in any tracked file.
- `teach/`: 11 MP4s (6.0/2.4/1.6/1.2 MB…) + 355 PNGs, **35.8 MB, 100% unique**.
- These are **recordings**. There is no master to re-derive them from. Ranked below `mag-current-rebuild` only because losing a recording is a content loss, not a capability loss.

### Regenerable — correctly scored as ZERO risk
- `the_margin_lean/` (219.5 MB) is a **`mathlib4` clone**, not the operator's work. 10,056 `.lean` files, its own clean `.git` (29 MB), zero dirty files. Re-clonable.
- `azerothcore-wow`, `tortoise-wow`, `vmangos-core` — all vendored upstream, all versioned, all re-clonable.
- `nacho-business` (99.8% dup) and `world-games-corpus` (98.8% dup) — the unique remainder is a `LICENSE` and two small `L0`/`GROK` markdown drafts.

---

## 3. WHAT WOULD ACTUALLY BE LOST — the specific list

| directory | irreplaceable content | regen? |
|---|---|---|
| `mag-current-rebuild` | 117 `mag/*.py` modules + `main.py` (229 KB, divergent) + 9.4 MB session/grok ledgers | **NO** — never committed anywhere |
| `research/aiTruthCode` | 7.9 MB / 139 files, 55 hand-curated dirs, GTC→GTR lineage | **NO** — no upstream |
| `memory/corpus/kungfu` | 71.2 MB, 3 recordings | **NO** — recordings |
| `teach` | 35.8 MB, 11 recordings + 355 sheet PNGs | **NO** — recordings |
| `world_key/lock2_key.md` | 3,012 B key material | **NO** — one copy |
| `career` | 6 application/POW docs | **NO** — hand-written |
| `embassy-sandbox`, `audit_prep_verkle` | 127 files, 0% elsewhere | **NO** |
| `soul-frontier`, `games-site` | hand-built `index.html` / `ruins_go_engine.js` + **`.env.local` (no git)** | **NO** for the html/js; env yes |
| `the_margin_lean` | nothing | yes (mathlib4) |

---

## 4. CROSS-REFERENCE: is `watch/inbox/` duplicated in a tracked location?

**No. It is disk-only.** Three independent checks:

1. `git ls-files watch/inbox/` → **9,490** tracked; `find watch/inbox -type f` → **11,377** on disk. **1,887 files on disk are not in git.**
2. Of those, **941 are untracked files totalling 1,760,086,209 B (1.76 GB)** — untracked, unignored, unbacked.
3. **Neither bare mirror contains a single `watch/inbox` path:**
   `git --git-dir=Mag-backup.git ls-tree -r --name-only main -- watch/inbox` → **0**
   `git --git-dir=Mag-prewipe-backup-20260927.git ls-tree -r --name-only main -- watch/inbox` → **0**

`watch/` is *not* gitignored (`.gitignore:141-147` ignores only `watch/*.json|jsonl|txt|log` at the top level; `git check-ignore` returns nothing for `watch/inbox/`). The untracked mass is a **placement** finding, not a capability gap — the instrument exists, it was just never added.

**The single most dangerous object on the box:**
```
1,706,469,664 B  watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc   (1.59 GiB)
   22,120,192 B  watch/inbox/ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc
```
An encrypted archive named *essentials*, 1.7 GB, **neither tracked nor ignored** — verified: `git ls-files --error-unmatch` → "did not match any file(s) known to git"; `git check-ignore -v` → empty. **A `git clean -fdx` in the repo deletes it, and nothing else on the machine holds a copy** (searched `projects/` and `Desktop/`, only the two originals found). Its key is in `world_key/lock2_key.md`, which is itself unversioned and single-copy — so the pack and its key are mutually unsaved.

Also unversioned and unignored in the repo: `catalog/catalog_fts.sqlite` (134 MB) and `catalog/receipt_fts.sqlite` (37.8 MB).

### Uncommitted work in the versioned repo — the 44-entry claim, verified

| claim | verdict |
|---|---|
| "two real git worktrees contain 44 uncommitted entries" | **CONFIRMED as 7 + 37 = 44** — but they are **linked worktrees**, not independent repos. `worktrees/salon-arena-mvp/.git` is a file: `gitdir: .../local_sovereign_agent/.git/worktrees/salon-arena-mvp`; same for `sovereign-mirror-scaffold`. |
| "5 never-committed core modules" | **UNDERCOUNTED.** `salon-arena-mvp` has **4** never-committed (`mag/salon_arena.py`, `mag/salon_renderer.py`, `tests/test_salon_arena.py`, `tests/test_salon_renderer.py`) + 3 untracked paths. `sovereign-mirror-scaffold` has **5** never-committed core modules (`human_knot.py`, `idea_catalog.py`, `lenses.py`, `platform_pack.py`, `rashomon_synthesis.py`) + 20 other untracked paths. **9 total, not 5.** |
| "four .codex worktrees at a4733004a, 437 commits behind" | **CONFIRMED, with a correction.** All four exist at `C:\Users\foste\.codex\worktrees\{6654,b13a,ef82,efa1}\local_sovereign_agent`, all at `a4733004a`, all **0 dirty** (nothing to lose — 8.4 MB each, pure re-checkout). `a4733004a..HEAD` = **438** commits. The 437 figure is right for `a4733004a → 6d417abd5` (the prewipe backup). **These are outside `projects/` — they are not siblings.** |
| "mine/raw/ is 2.92 GiB of vendored public clones with their own .git" | **BOTH HALVES WRONG.** Size is **5.6 GB** (`du -sh`), and **none of the five trees has a `.git`**: `agent_bleeding_edge`, `agent_platform`, `mesh_comm`, `narrative_corpus`, `steal_protocol` — all "no .git". They are third-party sources (`ink-language`, `redblob-roguelike`, `tes5edit`, `arvarik`, `claudioed`) stripped of history. They are `git ls-files mine/` → **0 tracked**, `git check-ignore mine/` → **not ignored**. So: 5.6 GB, not 2.92; and re-clonable only by re-deriving which upstream each of 5,685–75,279-file trees came from — there is **no provenance record** (no README, no origin URL, no manifest). |

### The main repo's own uncommitted mass

`git status --porcelain` in `local_sovereign_agent` = **1,885 entries** (264 ` M`, 3 ` D`, 1,565 `??`, plus concurrent churn):

| class | files | bytes |
|---|---|---|
| modified-tracked | 271 | **1,723,989,657** (1.72 GB) |
| untracked files | 1,578 | **1,964,271,924** (1.96 GB) |
| **total uncommitted** | **1,849** | **≈ 3.69 GB** |

**12 untracked `mag/*.py` are live enforcement, not scratch.** All 12 are referenced by *tracked* code (`git grep -l` reference counts: `dormant` 245, `runtime_policy` 14, `events_key_schema` 11, `catalog_rebuild` 9, `catalog_rescan` 6, `env_redirect` 7, `links_sha_ratchet` 5, `catalog_tags` 5, `links_split_gate` 3, `census_liveness` 3, `catalog_freshness` 3, `events_scan` 2). `git log --all -- mag/catalog_rescan.py` → **"NEVER IN ANY COMMIT"** for all 12. They are B2-### burn-wave gates (`events_scan` = "B2-399 split", `links_sha_ratchet` = "B2-173"). A clean checkout of this repo is a **repo where the gates are gone and the callers still call them.**

**Backup coverage is stale in the wrong direction.** The only remote is `Mag-backup.git`, a **local disk path** — not a containment boundary. Its HEAD is `a4733004a`, **438 commits behind**, and it does not contain `e73b60c5`. `Mag-prewipe-backup-20260927.git` is at `6d417abd5`, only **1 behind** — but it is a **clone of a clone** and has the same 0-file `watch/inbox` coverage. Nothing off this machine holds any of it.

---

## 5. BYTES

| class | bytes | what |
|---|---|---|
| **UNVERSIONED, IRREPLACEABLE** | **129,003,800 (129.0 MB)** | measured-unique sum over all 13 unversioned dirs with a nonzero risk tier: `memory` 71,170,712 · `teach` 35,790,308 · `mag-current-rebuild` 13,801,156 · `research` 7,898,891 · `games-site` 116,865 · `embassy-sandbox` 86,739 · `world-games-corpus` 34,218 · `soul-frontier` 30,378 · `career` 28,048 · `nacho-business` 21,526 · `audit_prep_verkle` 21,312 · `world_key` 3,012 · `bond-audit` 635. (`the_margin_lean` excluded — 0 unique, it is a mathlib4 clone.) |
| **UNCOMMITTED, in a repo, unbacked** | **3,688,261,581 (3.69 GB)** | 271 modified-tracked (1,723,989,657) + 1,578 untracked (1,964,271,924), incl. the 1.59 GiB encrypted pack and 172 MB of sqlite |
| **UNVERSIONED, REGENERABLE (cache/deps)** | **4,371,980,000 (4.37 GB)** | `.mimosa` 4.132 GB (306,653 `.source` hook-state baselines) · `the_margin_lean` 0.220 GB (mathlib4) · `venv` 0.012 GB · `.venv` 0.006 GB · `.trash` 0.001 GB · `.pytest_cache` + 10 empty dirs ≈ 0 |
| **UNTRACKED, RE-CLONABLE, UNPROVENANCED** | **5.6 GB** | `local_sovereign_agent/mine/raw/` — third-party, history-stripped, no origin recorded |
| **VERSIONED, safe** | ≈ 2.0 GB | 10 working repos + 2 bare mirrors (6.25 + 6.11 GiB packs) |

**Total walked:** 52.43 GB across 57 siblings, 0 timeouts (excludes pruned `.venv` 2.16 GB, `node_modules` 0.19 GB, `.git` per-dir internals).

---

## 6. MEASUREMENT LIMITS (stated, not assumed)

- `corpus/oral_history/` was **not walked in full** (bounded per instruction). The repo total of 31.45 GB / 514,358 files therefore **excludes** it; the unversioned/irreplaceable figures in §5 do not depend on it.
- The census's per-directory `.git` size count is **wrong** (it reported `local_sovereign_agent/.git` as 0.037 GB / 57 files; `du -sh` says **7.5 GB**, and `git count-objects -vH` says 6.11 GiB in-pack + 1.27 GiB loose). All §5 `.git` figures are `du`/`count-objects`, not census. The *file/byte* census excludes `.git` by design and is unaffected.
- The first uniqueness instrument produced a **1-hash reference set** (a `git ls-files -z` pipe was read line-buffered) and reported a meaningless 100%-unique for everything. **Discarded and re-run**; the shipped numbers come from the fixed run (68,939 reference hashes). The instrument is sanity-checked against known facts: it returns 0.0% for `corpus/` and `scripts/`, 43.5% for `tests/`, and 1.2% for `world-games-corpus` — it discriminates.
- `salon-arena-mvp` is owned by `CodexSandboxOffline`; `git status` refuses with "dubious ownership". Measured with a **per-invocation** `git -c safe.directory=...` (no global config written, no repo mutation).
- `.env` files were **stat'd and tracking-checked only; no `.env` content was read or printed**, per the secret rule. Files found: `local_sovereign_agent/.env` (5,809 B, **gitignored**), `mag-current-rebuild/.env` (3,276 B, **no repo at all**), `mag-sovereign-kit/.env` (527 B, gitignored), `games-site/.env.local` (1,229 B, **no repo**), `soul-frontier/.env.local` (1,261 B, **no repo**), `worktrees/sovereign-mirror-scaffold/.env` (116 B, worktree of a repo, untracked).
- `world_key/lock2_key.md` was **not read** — size/mtime only, first-line shape masked.
- Nothing was fixed, moved, deleted, committed, cleaned, gc'd, or pruned. `git config --global` was not written.
- Concurrent lanes (`lane4*`/`w2l*`) were running in the same scratch dir; my files are namespaced `lane4b_*`.

---

**Receipt:** `memory/audit_20260926/lane4b_risk.json` (machine-readable, same field names)
**Audit defects, not fleet findings:** broken `ls-files` streaming instrument (discarded, re-run); census `.git` sub-count (superseded by `du`); `nul` reserved-name guard applied — no `relpath` call was made on it.
