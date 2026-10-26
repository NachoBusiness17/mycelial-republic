# BREAK-COMMUNICATION - hostile second pass on the communication lens, 2026-10-05

Pass: break-communication (ractor_engine, spore-sharing theater). Target: the communication
lens report (6 blind_spots, 5 findings). Method: every evidence cite re-executed as a command
in this session, byte-checked against the estate and against github.com/NachoBusiness17.
Laws held: no em-dashes, every claim cited path:line or command+output, unverified = OWED.

## RUN LOG (commands executed this session, condensed)

1. `git ls-remote https://github.com/NachoBusiness17/mycelial-republic.git` -> exactly two refs:
   HEAD + refs/heads/master, both dc66499434b050343e81dabcb45b849c5f1fda29. One branch. CONFIRMED.
2. `git -C C:/Users/foste/Documents/projects/mycelial-republic remote -v; rev-parse HEAD; branch -a; rev-list --count HEAD`
   -> origin = the same GitHub URL; tip dc66499434; local+remote master only; 13 commits. CONFIRMED.
3. `git rev-parse --verify dc66499^{commit}` IN THIS REPO -> rc=0, resolves to the GitHub tip.
   `git merge-base --is-ancestor dc66499 HEAD` -> rc=1; `git branch --contains dc66499` -> empty.
   The tip EXISTS here as a dangling object, on no branch, not an ancestor of HEAD.
   THE LENS CLAIMED "git log dc66499 fails in this repo" - FALSIFIED, the exact command succeeds.
4. `ls C:/Users/foste/Documents/projects/mycelial-republic/framework/mag/ | grep -c '\.py$'` -> 44
   (plus __pycache__); no __init__.py. LENS SAID 43 modules - off by one (44 .py files).
   `grep -i route` over that listing -> only cache_router.py, router.py. No route_chat.py. CONFIRMED.
5. Sibling organ sweep: `git ls-files | grep -iE 'GENOME|STANDING_RAILS|parable|\.env|providers\.yaml|route_chat|GPS|carrier'`
   -> rc=1 (zero matches); `find . -path ./.git -prune -o -type f \( -iname '*GENOME*' -o -iname '*STANDING_RAILS*' -o -iname '*parable*' -o -iname '.env*' -o -iname '*carrier*' \) -print`
   -> zero untracked matches. `ls framework/configs/` -> 8 yamls, none named providers.yaml.
   `ls configs/` (sibling ROOT) -> annotation_template.json, selftest, selftest_checklist.yaml,
   train_8b.yaml, vector_map_hybrid.yaml (no secrets, no providers.yaml). CONFIRMED.
6. `C:/Users/foste/Documents/projects/mycelial-republic/framework/mag/rib_bus.py` lines 48 and 81:
   line 48 = `RIB_DIR = ROOT / "memory" / "rib_bus"`; line 81 = `f.write_text(json.dumps(store, ...))`
   bare, no lock/rename/tmp. `ls framework/memory` -> No such file (rc=2), so a fork mounts zero ribs.
   This repo's `mag/rib_bus.py:48` and `:81` byte-identical on those lines. CONFIRMED.
7. `sed -n '38,46p' C:/Users/foste/Documents/projects/mycelial-republic/.gitignore` -> lines 41-42 =
   `.env` / `.env.*` (plus *.pem, wallet.json, *.key). CONFIRMED. Sibling framework/README.md:16-17
   = "Private, never here: the runtime memory (`memory/`), the persona, the biography,
   `providers.yaml`, `mag-secret.yaml`...". README.md:27 = "> **Steal the mechanism, never the content.**" CONFIRMED.
8. `mag/route_chat.py:46` = `USAGE = ROOT / "memory" / "runs" / "route_chat" / "usage.jsonl"`;
   `:56-72` = `_keys_for`: os.environ first, then parses `(ROOT / ".env")` `env=` lines. Single
   .env, no operator dimension anywhere in the function. CONFIRMED.
9. `head -1 memory/runs/route_chat/usage.jsonl` -> `{"ts","lane","model","goal","prompt_tokens",
   "completion_tokens","ok"}` - NO operator field. CONFIRMED.
10. `tools/gps_mcp/ledger.py:133-141` = capability CREATE TABLE: columns model_id, task_shape,
    pass_rate, sample_size, cost_usd_per_call, last_measured, updated_at;
    PRIMARY KEY (model_id, task_shape). No estate/operator column. The INSERT ... ON CONFLICT
    (model_id, task_shape) DO UPDATE sits inside the cited 598-612 window. CONFIRMED.
11. `queue/lanes/builder/runner_state.json` (live read) = {"inbox_offset": 13, "last_run":
    "2026-10-05T11:31:18.890574+00:00", "last_day": "2026-10-05", "last_result": "gated=0",
    "seat": "builder"} - the lens's 2-key quote is a SUBSET of a live file that moved after it read.
    No owner/lease field. CONFIRMED with a currency note. `mag/lane_runner.py:391,404` read/write
    the offset; `:136-143` _save_state is ATOMIC: unique tmp name + `os.replace` (rename-CAS,
    "proved against win32 filter locks"); `:153-160` twin-site cure landed 2026-10-05.
    AMENDMENT: atomicity already exists; the missing piece is owner/lease, not atomic writes.
12. `git ls-files queue/lanes/ | grep runner_state` -> 10 TRACKED cursors (bard_ledger, builder,
    day_work, economist, elder, forge, harvest, night, prose, research). Live cursors tracked in git.
13. `sed -n '28,29p' state/GENOME.md` -> law 4 "If it ran, it banks. Session, audit, fold, replay:
    DONE row or it did not happen." EXACT. CONFIRMED.
14. `grep -ril NachoBusiness17 watch/inbox/` -> 29 files; `grep -ril mycelial-republic watch/inbox/`
    -> 20+ files (head-truncated); `grep -ril spore watch/inbox/` -> many (incl .mimosa baselines).
    LENS CLAIMED the combined grep matched "only AEOLIPILE_SPORE_20260922.md + .mimosa
    hook-state baselines" - FALSIFIED AS STATED. The matches reference the account identity and
    NachoBusiness17/the-mountain (a DIFFERENT repo), not the republic push.
15. `grep -rl dc66499 watch/inbox/ state/ corpus/ memory/rib/ memory/zknot/ queue/ docs/` -> 3 hits
    outside today's theater files: watch/inbox/audit_20260926/LANE4B_UNVERSIONED_RISK.md,
    corpus/oral_history/marathon_body/marathon_25fbcaab_20260815_20260820.jsonl, and the theater's own.
    LANE4B:34 = versioned-surfaces table row: `mycelial-republic | dc66499 | 2026-08-20`.
    Oral history JSONL narrates the push: "3da416c..dc66499 master -> master... no pyc staged...
    scanned + syntax-clean". THE PUSH AND TIP ARE BANKED ESTATE-SIDE. FALSIFIES the lens's
    "the only record is a commit message in the sibling repo that estate audits never read".
16. `gh repo list NachoBusiness17 --json name,visibility,pushedAt` -> FOUR repos:
    **mag-sovereign-seed PUBLIC pushedAt 2026-10-04T23:40:58Z** ("The Mag Seed: a working
    sovereign AI agent's DNA - constitution, organs, manual, and stories. Read it, keep it, grow
    your own."), the-mountain PRIVATE 09-30, embassy-aos PUBLIC 08-22, mycelial-republic PUBLIC
    2026-08-20T15:29:04Z. THE LENS AUDITED ONLY THE STALE AUGUST REPO AND MISSED THE SEED.
17. `gh api repos/NachoBusiness17/mag-sovereign-seed/git/trees/HEAD?recursive=1` -> 1,798 paths.
    Organ grep over the full tree: NO state/GENOME.md, NO queue/STANDING_RAILS.md, NO
    configs/providers.yaml, NO mag/route_chat.py, NO gps_mcp ledger, NO carriers, NO keys.json.
    PRESENT: docs/ref/THE_PARABLE_OF_THE_MOVING_WALL.md, mag/rib_bus.py, mag/gwap_to_gps.py,
    mag/ (1,119 files), boot/ (AGENTS/CONSTITUTION/LOAD/main.py/mag.cmd), memory/ (curated:
    MEMORY.md, briefs/latest.md, doctrine/LEDGER.jsonl+scorecard), story/ (23 files),
    starter-kit/ (47 files: INSTALL.md, BOOT.md, LAWS.md+laws.json+schema, PROTOCOLS.md,
    SUBSYSTEMS.md, skills lane-runner/ractor-lenses/receipt-filer/workflow-shaper, tools
    kit_doctor.py/law_gate.py/profile_boot.py, tutorial/TUTORIAL.md, workflows, integrations).
18. Shallow clone of the seed; `git -C /tmp/seed rev-list --count HEAD` -> 1 commit (cbda4d8,
    2026-10-04, "THE STARTER KIT v0.2"). Credential scan `grep -rInE` (9 families: sk-16+,
    AKIA16, xai-, hf_20+, ghp_20+, github_pat_, AIza20+, sk-or-v1-, sk-ant-) over the whole
    working tree = ZERO real credentials; all matches benign (branch URL "virtual-desk-...",
    skill id, phrase, and the seed's OWN scrubber regexes at mag/aos_live_view.py:52-53 and
    mag/mind_window.py:53). SEED HISTORY FULLY SCANNED (single commit).
19. Sibling history scan (the lens's OWED blind spot): `git -C .../mycelial-republic log -p --all
    | grep -InE` (same 9 families + private-key BEGIN headers) over all 13 commits -> zero matches.
    OWED ITEM RUN AND CLEAN (pattern families only; no entropy analysis).
20. `configs/keys.json`: fields env/provider/role/ceiling/status, values are env NAMES
    (ZAI_API_KEY_Lite etc.); `grep -cE` credential families -> 0 (rc=1). CONFIRMED. Note: keys.json
    is an ESTATE file; the sibling ships no keys.json at all.
21. `watch/inbox/burn_reset_20260927/flash50/free-lane-map.md` head -> census of 2026-09-28
    (~23:20-23:40 UTC), self-declared read-only ("no lane was fired"), and section 1.1 states
    verbatim: "835 lines, 28 provider blocks, 62 model rows, 51 distinct model ids ... 13
    distinct `:free` ids ... Header law (providers.yaml:4-6)". CONFIRMED (13 = DISTINCT ids; a raw
    `grep -o ":free" | wc -l` reads 36 occurrences, consistent).
22. `sed -n '4,6p' configs/providers.yaml` = the quota-guard law; `:158` = `api_key_envs:
    [HERMES_API_KEY_1, HERMES_API_KEY_2]`; `:366` = `api_key_envs: [DEEPSEEK_API_KEY,
    DEEPSEEK_SWARM_API_KEY]`; `:575` = `api_key_env: ZAI_API_KEY_Lite`. ALL EXACT. CONFIRMED.
23. `sed -n '33,46p' queue/STANDING_RAILS.md` = THE DROP-IN TABLE, first row `mag.route_chat(lane=,
    goal=)`. `sed -n '34,38p' state/CURRENT.md` = "z_ai3 dormant in providers.yaml, lite_guard
    RETIRED gate, flash_call openrouter-primary, .env key commented". CONFIRMED.
24. `state/_astra_triangulation.md:756` = Forest row ("Above-ground fruiting + shared law | Public
    fork, republic train, optional collective" - lens paraphrased the wording, row exists);
    `:1252` = "**Sister:** [mycelial-republic](https://github.com/NachoBusiness17/Mag)" - the DEAD
    href confirmed; `:1389` = "Federalism | Mag (private office) + mycelial-republic (public fork)".
    CONFIRMED. `ls scripts/ | grep -i syn` -> home_sync.cmd, sync_env_from_scaffold.py.
25. `git check-ignore -v state/GENOME.md` -> hit at `.gitignore:40` rule `state/` (rc=0);
    `.gitignore:40-41` = `state/` + `state/**/*`; `git ls-files state/` -> the genome NOT tracked.
    THE ENTIRE state/ TREE IS GIT-IGNORED. THE GENOME HAS NEVER BEEN IN ANY GIT HISTORY.
26. `head -30 watch/inbox/AEOLIPILE_SPORE_20260922.md` -> a SPAWN doc on Hero's aeolipile /
    water-computer state-change physics / the spore law as the md-record law. NOT a push receipt.
27. `head -12 C:/Users/foste/Documents/projects/mycelial-republic/docs/FIRST_STEPS.md` -> "The
    public, forkable practice surface... practice, not machinery". CONFIRMED.
28. Seed FREE_COMPUTE.md grep for deepseek|z.ai|zai|route_chat|5% -> only OpenRouter/:free/460-model
    audit lines and the pool law; NO DeepSeek, NO z.ai-lite, NO ~5%-of-paid price table.

## VERDICTS

F1 (GitHub channel ships none of the strongest-version organs) - WEAKENED.
Every cited byte about mycelial-republic verified (run log 1-7: one branch, tip dc66499, 13
commits, no route_chat/providers.yaml/GENOME/STANDING_RAILS/ribs/carriers/GPS/.env-example
tracked or untracked, rib_bus.py:48 dangling RIB_DIR, framework/memory absent, README.md:16-17
private-list). Three defects: (a) the premise "the GitHub channel" = that one repo is false -
the account also ships mag-sovereign-seed (public, pushed 2026-10-04T23:40:58Z, 1,798 files)
carrying the parable, rib_bus.py, gwap_to_gps.py, the boot contract, and a 47-file starter-kit
(run log 16-17); (b) "43 modules" is 44 .py files; (c) "git log dc66499 fails in this repo" is
false - it resolves as a dangling object (run log 3), which makes the manifest diff work EASIER.
The organ-absence census stands for the repo audited; the channel-level conclusion does not.

F2 (the share is unbanked, violating law 4) - WEAKENED (strong form killed).
The law cite (state/GENOME.md:28-29) and the keys.json zero-credential sub-claim are byte-true
(run log 13, 20). But the core claim is falsified three ways: watch/inbox/audit_20260926/
LANE4B_UNVERSIONED_RISK.md:34 banks the tip in a versioned-surfaces table;
corpus/oral_history/marathon_body/marathon_25fbcaab_20260815_20260820.jsonl banks the push
narration including the scan claim ("scanned + syntax-clean", "no pyc staged"); and
watch/inbox/full_width_fold_20261002.md:75 banks "mag-sovereign-seed repo LIVE (four-repo
estate under NachoBusiness17)". The grep evidence line ("only AEOLIPILE + .mimosa") is false as
an instrument claim (run log 14: 29 NachoBusiness17 matches in watch/inbox). AEOLIPILE is a
physics SPAWN, not a receipt (run log 26). Surviving kernel: no STANDALONE receipt names the
scan INSTRUMENT and result; the scan claims live in commit messages and trajectory JSONL.

F3 (N-operator seams: rib_bus overwrite, claimless cursors, one .env wallet, GPS upsert
collapse) - CONFIRMED, with one precision amendment.
All four seams byte-verified (run log 6, 8-11): rib_bus.py:81 bare write_text in BOTH repos;
route_chat.py:46/:56-72 one .env, env-then-file chain, no operator field; usage.jsonl first row
has no operator field; ledger.py capability PK (model_id, task_shape) with no estate column.
AMENDMENT: mag/lane_runner.py:136-143 _save_state is ALREADY atomic (tmp + os.replace
rename-CAS, win32-proven; twin-site cure at :153-160), so the N=2 gap on lane cursors is
owner/lease, not torn writes; rib_bus _save_store remains the genuinely bare write site.
NEW HAZARD the lens missed: 10 lane runner_state.json cursors are git-TRACKED (run log 12) -
the N=2 story also collides in git, not just at runtime.

F4 (tutorial is a compilation job; no cold-operator boot doc exists; ~5% OWED) - WEAKENED.
All cited bytes verified (run log 21-23, 27). But the load-bearing clause "no single
cold-operator boot doc exists" is falsified: the seed repo ships starter-kit/tutorial/
TUTORIAL.md (three lessons, one day, ends each with a running organ), starter-kit/INSTALL.md
("the ladder, in order, with the why"), FREE_COMPUTE.md ("how to get real AI power for $0
(2026-10 edition)... written for someone starting from zero", OpenRouter :free + 460-model
audit + the .env never-travels law + the pool law), and starter-kit/SUBSYSTEMS.md (the dormant
catalog: "None of these need to be built before they carry weight") - pushed 2026-10-04
(run log 17-18, 28). Residual true: the topic's SPECIFIC ladder (DeepSeek keys, z.ai-lite
monthly, the ~5%-of-paid price table, route_chat as the one door) is in NONE of the seed docs
(FREE_COMPUTE.md grep confirms; DeepSeek/z.ai-lite bytes live estate-side at providers.yaml:366
and :575), and the ~5% figure remains OWED - no pricing receipt exists and no lane was fired
by me either; the census itself declares read-only (free-lane-map.md head).

F5 (federalism: private office + public fork, dead Mag link) - CONFIRMED (on the visible
portion).
The ask truncated this finding's text and its evidence field mid-token; I verified everything
readable: _astra_triangulation.md:756 (forest row; lens paraphrased the cell wording),
:1252 (the dead github.com/NachoBusiness17/Mag href - verified dead by gh repo list: no Mag
repo; the live repo is mycelial-republic per ls-remote), :1389 (Federalism row, exact), sibling
framework/README.md:27 ("Steal the mechanism, never the content."), sibling docs/FIRST_STEPS.md
(practice-surface framing), `ls scripts/ | grep -i syn` (sync_env_from_scaffold.py,
home_sync.cmd). The untruncated remainder of the lens's evidence is UNVERIFIED here - not run.

## ADDITIONS (what the lens missed)

A1 - The spore already exists, and it is not the repo the lens audited.
`gh repo list NachoBusiness17` shows mag-sovereign-seed, PUBLIC, pushed 2026-10-04T23:40:58Z,
1,798 files in one commit (cbda4d8, "THE STARTER KIT v0.2"), described as "The Mag Seed...
constitution, organs, manual, and stories". It carries the parable, the boot contract, 1,119
mag/ files, curated memory, the story tier, and a starter-kit with INSTALL ladder, TUTORIAL,
LAWS+law_gate, SUBSYSTEMS, method skills, and integrations. It does NOT carry GENOME.md,
STANDING_RAILS.md, providers.yaml, route_chat.py, the GPS ledger, the carriers, or the season
chain. The topic's real question is not "cut the first spore" but "what does the existing
spore still lack". Evidence: run log 16-18, 27-28. Falsifier: a repo under the account carrying
state/GENOME.md + queue/STANDING_RAILS.md would prove the spore already complete. Move: diff
the seed tree against the strip/stay/dormant table and file the gap list (~30 min).

A2 - state/ is wholly git-ignored, so no git-based share pipeline can ever carry the genome.
.gitignore:40-41 (`state/`, `state/**/*`); `git check-ignore -v state/GENOME.md` rc=0;
`git ls-files state/` shows the genome untracked. Any manifest/cut process that works from git
history or `git archive` silently drops the strongest-version state. The spore must be staged
from the working tree explicitly (add -f or a staging dir) or the ignore rule amended with an
allowlist. Evidence: run log 25. Falsifier: `git ls-files state/` returning GENOME.md. Move:
name the staging mechanism in SPORE_MANIFEST.md before any cut is attempted (~20 min).

A3 - The lens's OWED history-leak scan is now RUN and clean, with scope limits stated.
Sibling: `git log -p --all` (all 13 commits) x 9 credential families + private-key headers =
zero matches. Seed: whole working tree (its entire history is one commit) = zero real
credentials; the only sk-shaped hits are the seed's own scrubber REGEXES (mag/aos_live_view.py
lines 52-53, mag/mind_window.py line 53), meaning a fork inherits detection patterns too.
Limits: pattern families only, no entropy analysis; the estate repo's own history was not
scanned (out of scope for the public channel). Evidence: run log 18-19. Falsifier: any of the
9 families matching in either repo's history. Move: fold the two scan commands + zero-result
into the push receipt's scan section (~10 min).

A4 - Ten lane cursors are tracked files with live churn: the N=2 collision is also in git.
`git ls-files queue/lanes/ | grep runner_state` = 10 lanes; builder's moved today
(last_run 2026-10-05T11:31Z) while tracked. Two seats sharing the repo = perpetual dirty-tree
churn and merge conflicts on cursors, independent of the runtime claim gap. Evidence: run log
11-12. Falsifier: runner_state.json paths absent from git ls-files. Move: add the cursor paths
to .gitignore in the same commit as the N-operator design row (~5 min).

A5 - The seed ships a worked strip/stay precedent worth copying: PROVENANCE.md.
/tmp/seed/PROVENANCE.md ("how this seed was built (2026-09-30)"): read-only SSH pulls, nothing
on the estate modified, export anchored to verkle tip 00e374bd (8,692 leaves, ts
2026-09-30T23:47:34Z), newest seal "referenced by name only; not shipped", SEED_MANIFEST.sha256
= 1,653 hashed entries. The receipt the lens wanted (F2's move) has a house style already
shipped. Evidence: run log 18 + PROVENANCE.md head. Falsifier: PROVENANCE.md not present in
the shipped tree. Move: cite PROVENANCE.md as the template in the push receipt (~10 min).

A6 - The tutorial move shrinks to a two-document merge, and the price stays OWED.
The seed's FREE_COMPUTE.md + INSTALL.md + TUTORIAL.md already cover Ollama, the pool law, the
.env law, OpenRouter :free rotation, and day-one boot; providers.yaml:366 (DEEPSEEK_API_KEY
chain) and :575 (ZAI_API_KEY_Lite) plus free-lane-map.md already hold the estate-side bytes the
topic names. What exists nowhere: the ~5%-of-paid price table. No receipt prices it; I fired no
lane this session either; the figure remains OWED and must be marked as such in any tutorial.
Evidence: run log 22, 28. Falsifier: a banked receipt pricing the free ladder against paid.
Falsifier check NOT run beyond greps (no pricing doc surfaced in any grep this session). Move:
write the tutorial as FREE_COMPUTE.md + the providers.yaml chains + a price table stamped OWED
(~45 min).

## OWED (not done here, stated as such)

- No model lane was fired and no price was measured this session: the ~5%-of-paid figure stays OWED.
- The 2-operator chaos test (two live concurrent writers on rib_bus/cursors/GPS) was NOT run;
  F3's seams are read from code, not reproduced. The lens's blind spot stands, now with the
  lane_runner atomicity amendment attached.
- The full ~700-module mag/ tree and all tracked paths were NOT enumerated for export surface;
  my export check covers the two PUBLIC repos only. Non-code receiver surfaces (dashboard,
  lan_proxy, game client) remain unexamined, as the lens stated.
- The estate repo's own git history was not secret-scanned (only the two public channels were).

## Instrument note

Shell quirk encountered and survived: the harness shell is POSIX-flavored, not cmd.exe; an
initial cmd-style `find /c /v ""` made GNU find walk the C: drive (task killed, re-run with
`wc -l` / `grep -c`). No state was modified outside /tmp and this receipt.
