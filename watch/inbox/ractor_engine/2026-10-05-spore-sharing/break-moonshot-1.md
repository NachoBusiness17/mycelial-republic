# BREAK PASS: moonshot-1 (the spore sharing problem), 2026-10-05

Hostile second pass. Every cite below was re-run or re-read this sitting unless
marked not-run. Instrument and moment named per the quantifier law. Verdicts:
5 findings, all CONFIRMED on evidence, with byte-nudges and one broken move.

## VERDICT 1 - "the shareable surface is inverted": CONFIRMED

- `git check-ignore -v state/GENOME.md` -> `.gitignore:40:state/  state/GENOME.md`,
  rc=0. `.gitignore:40` is `state/` (a DIRECTORY pattern); `.gitignore:41` is
  `state/**/*`; `.gitignore:42` is `!state/.gitkeep`. The moonshot text says both
  `state/` and `state/**/*` at different points; both exist, and the dir pattern
  at :40 is the operative one (see ADDITION A1).
- Counts re-run (instrument `git ls-files | wc -l`, moment 2026-10-05 this
  sitting, on the moving pre-push tree): total 56,361 (moonshot read 56,359;
  +2 is the spore-sharing pass's own landings in
  watch/inbox/ractor_engine/2026-10-05-spore-sharing/, now 11 files); memory
  26,749 exact; dist_audit 1,496 exact; memory/agent_uploads 19 exact; watch
  20,360 / watch/inbox 17,070 (moonshot read 20,359 / 17,069; +1 each, same
  drift family). Nudge: the 19 files are 18 stt-*.webm voice recordings plus
  one _smoke.wav (listing read this sitting), so "19 voice recordings" is off
  by one; "19 files under memory/agent_uploads/voice_stt/" is exact.
- queue/STANDING_RAILS.md: check-ignore rc=1 AND `git ls-files` lists it ->
  tracked. memory/rib/: 55 tracked files. corpus/canon/: 206 tracked files.
- `git ls-files state/` -> only state/NIGHT_LOOP_20261005.md. Soft-ignore proof
  stands.
- state/GENOME.md:1-4 read: "The inheritable artifact." confirmed on the page.

## VERDICT 2 - "GitHub cannot be the vessel": CONFIRMED

- `git count-objects -vH`: size-pack 14.37 GiB, garbage 4 (the four
  tmp_pack_* files, 973.47 MiB size-garbage). Exact.
- `git log --oneline --all -- dashboard/data/ractor_board.jsonl.runaway-evidence-20260903`
  -> 60b1bde7f; `git cat-file -s $(git rev-parse 60b1bde7f:<path>)` ->
  blob cdd7d4fa6a72 = 2,232,735,205 bytes. The 2.2 GB blob is in history, byte-sized.
- watch/inbox/TWO_MACHINE_SYNC_20260919.md re-read: line 3 "GitHub private repo
  was evaluated and rejected as the primary bridge"; line 5 "54 blobs over
  GitHub's hard 100 MB limit (biggest: ...runaway-evidence-20260903 at 2.2 GB)";
  line 39 "Do not push this repo's history to GitHub as-is; the push will be
  rejected and any rewrite breaks receipt hashes." Quotes verified verbatim.
- watch/inbox/DAY_SYNTHESIS_20260930.md:7-12 re-read: 7 live keys in
  memory/trajectory/steps.jsonl through 64 commits, filter-repo cut under
  operator GO. Verified. (.gitignore:34 now ignores steps.jsonl; the operator
  chose history-left-intact per :32.)
- `GIT_TERMINAL_PROMPT=0 git ls-remote github` -> dc66499434b050343e81dabcb45b849c5f1fda29
  HEAD + refs/heads/master. `git remote -v`: github =
  https://github.com/NachoBusiness17/mycelial-republic.git - the EXACT URL the
  topic names as the push target. So "the remote points at the WRONG repo" is
  loose framing: the URL is the right target; the repo's CONTENT is the forest
  (commit 2026-08-20 11:28:57 -0400 "Add the game bones to the framework...",
  `git ls-tree -r` = 225 files, top level src/ framework/ mycelia.cmd
  scaffolds/ scrum/ tests/ et al.). Unrelated lineage proven harder than the
  moonshot did: `git merge-base main dc664994...` -> rc=1, no common ancestor.
- Correction: the moonshot's "`git cat-file -t dc664994` fails locally" no
  longer holds - the moonshot's own `git fetch github master --depth=1` landed
  the object; `git cat-file -t` rc=0 this sitting. Substance unaffected.
- Night-loop gate confirmed: state/NIGHT_LOOP_20261005.md LAWS FOR THE NIGHT
  block (~:30-32, read :25-45): "no operator-gated action fires ... no pushes
  beyond the backup pattern." The 2 h orphan-branch move is operator-gated.
- NEW (resolves the moonshot's blind spot 2): the target repo is PUBLIC.
  `GIT_TERMINAL_PROMPT=0 git -c credential.helper= -c credential.interactive=false
  ls-remote https://github.com/NachoBusiness17/mycelial-republic.git` -> refs
  returned, rc=0, no credential store, no prompt. Anonymous read works, so the
  repo is world-readable right now (instrument and moment named; GitHub
  settings can change). Any estate push there without a visibility decision is
  a public dump.

## VERDICT 3 - "multi-tenant breaks at the money and the steering": CONFIRMED

- `memory/runs/hermes_burn/usage.jsonl` line 1 keys via venv python json.loads:
  exactly [completion_tokens, cost_usd, id, model, ok, prompt_tokens, ts, turn].
  `grep -c operator_id` over the file: 0 matches (falsifier check run: no bank
  row carries a party id; falsifier fails, finding stands).
- mag/rib_bus.py:195-196 read: "canonical steer block (frontier invariants +
  operator directives + domain RIBs + grokbot seat directives) rides on EVERY
  task through this ONE drop-in." Exact. `grep -inE "claim|lease|lock"` over
  mag/rib_bus.py -> only lines 4 and 195, both prose. No claim system. Exact.
- mag/route_chat.py:61-70 read: `_keys_for` reads os.environ then exactly
  `(ROOT / ".env")`. Exact; single-tenant by construction.
- tools/gps_mcp/ledger.py: schema read :6-31 - PRIMARY KEY (model_id,
  task_shape) at :13, no operator column anywhere; :329 "cost is seeded or
  updated by operators/fixtures" verbatim. Exact.
- configs/providers.yaml: gitignored confirmed (`.gitignore:24`), but the
  moonshot's "36 lanes" is WRONG: `yaml.safe_load`, `len(d['providers'])` -> 28
  provider blocks (this sitting; the file is gitignored so my read is of the
  live local copy, which is the one that matters for the wallet claim).
  Substance (one wallet, many lanes) unaffected.
- Nudge: state/CURRENT.md z_ai-dormant is at :35 ("z_ai3 dormant in
  providers.yaml"), not :36 as cited.

## VERDICT 4 - "forked estates trading sha256 receipts": CONFIRMED

- scripts/build_travel_kit.py read :1-12, :46-59, :180-198: bounded pointer
  "path + sha256" at :5-6; ARCHIVE_TIERS at :52-59; manifest dict at :184-192
  with `"schema": "travel_kit.v1"` at :185; per-file sha256 at :198. Exact.
- watch/inbox/TWO_MACHINE_SYNC_20260919.md:15, contract item 1: "Drive cannot
  merge two writers, and nothing can merge two `.git` dirs." Verified; the
  moonshot's "nothing can merge two .git dirs" quote is real and it IS item 1.
- tools/gps_mcp/ledger.py:57 "an evidence_hash is never stored on trust"
  verified at :57 (and restated :331-337) - the moonshot's ":60-66 region" cite
  is legitimate. (I suspected a phantom cite; the byte-check killed my
  suspicion, not the lens's.)
- Dormant-native mode: queue/STANDING_RAILS.md:11-12 "dormant gate" in the
  route_chat front door; AGENTS.md "Hermes dormant but dispatch-capable"
  (workspace context). Confirmed.
- Caveat the lens missed: this finding's falsifier is unfalsifiable by
  construction - its firing condition (two estates appending to one shared
  verkle tip) is barred by the very contract item 1 the finding cites. The
  finding is the estate's own law applied consistently; fine, but name it.

## VERDICT 5 - "the tutorial ladder exists as config; the play cron is
un-regrowable": CONFIRMED

- configs/providers.yaml (live gitignored copy) read: :14 z_ai "FREE
  cache-mined GLM ... the default"; :17 openrouter "18 lanes x 1000/day (the
  big free capacity)"; :37 deepseek "PAID fallback"; :41 xai; :150 nous block.
  All exact.
- .env.example tracked (`git ls-files` lists it) with XAI_API_KEY :3,
  OPENROUTER_API_KEY :6, GROQ_API_KEY :9, DEEPSEEK_API_KEY :10. Exact.
- queue/STANDING_RAILS.md:43 "a play hour | tools/tavern.py + tools/dungeon.py
  (hourly cron)" verbatim; the dormant gate is :11-12. Exact.
- `grep -rln "tavern" scripts/ mag/` -> scripts/dm_tools_dual_research.py plus
  mag/.mimosa/hook-state cache blobs only. Matches the moonshot's scoped claim.
- `ls scripts/register_*.ps1` -> 13 today (census_patrol, corpus_rescan,
  day_end, endpoint_news, fts_index, gap_sentinel, gate_canary, improve, leave,
  ratchet, tip_witness, vision_nightly, x_radar). The moonshot enumerated 9 of
  the 13; the conclusion holds: none registers play.
- Live schtasks re-run this sitting, same instrument class: `schtasks /Query
  /FO CSV | grep -ic "mag"` -> 0. Shell-scoped absence, correctly scoped by the
  lens; stands as "no Mag rows visible from this shell", not "no tasks exist".
- `ls corpus/steal/*.md | wc -l` -> 32 (topic said 10; moonshot right).
  memory/rib_bus/doctrine.json: ribs count 26, updated 2026-10-04T22:50:05Z
  (venv python). The topic's 26 confirmed.

## BLIND-SPOT DISPOSITIONS

- Rotation OWED: WEAKENED by in-repo evidence the lens skipped.
  watch/inbox/DAY_SYNTHESIS_20260930.md:9: "ROTATED. The operator rotated; the
  repo .env holds the post-rotation pair... hermes's own env still carried the
  pre-rotation pair, the NACHO slot dead 401, all four cross-pairs NO MATCH
  (AJ9_NOUS_402.md)." watch/inbox/last_mile_20260930/AJ9_NOUS_402.md exists and
  is the post-rotation probe receipt (fingerprint-only, 4 Nous keys). AG1:25
  ("rotate the 7 keys... until rotation") is the same-day PRE-rotation operator
  call. Provider-console state remains OWED in the strict sense, but the
  moonshot's premise "assume the old values may be live somewhere" is
  contradicted by the estate's own 401 probes.
- public/private: RESOLVED this sitting - public (anonymous ls-remote rc=0,
  credential helper disabled, no prompt; see VERDICT 2).
- schtasks inventory: reproduced zero from this shell; the moonshot's scoping
  was correct; remains a shell-scope absence.
- .zcode/workflows DWF carriers: content untouched per the fence
  (state/NIGHT_LOOP_20261005.md ownership bullet, ~:32-37, executor
  dwfrun-e9656e14; "R1 amendments to .zcode/workflows are disjoint"), but the
  TRACKING metadata is checkable without touching content - see ADDITION A4.
- Third-party clones: unknowable from this repo; stays OWED (nothing run).
- ~5%-of-paid economics: topic-given; not verified this sitting either; OWED.

## ADDITIONS (what the lens missed)

A1. The moonshot's finding-1 move is broken as written: `!state/GENOME.md`
    cannot re-include the genome while `.gitignore:40` excludes the `state/`
    DIRECTORY - git refuses re-inclusion under an excluded parent. Evidence:
    the estate already carries the corpse - `.gitignore:42` has
    `!state/.gitkeep`, state/.gitkeep exists on disk (0 bytes, Aug 4), yet
    `git ls-files state/` shows it untracked. Empirical scratch-repo test this
    sitting (outside the estate, $TEMP/negtest_break1, since removed): with
    `state/` + `!state/.gitkeep`, `git status --porcelain` hides both files;
    with `state/*` + `!state/GENOME.md`, state content becomes visible.
    Falsifier: a git version or pattern shape where `!` re-includes under a
    dir-excluded parent (would contradict gitignore docs and my test).
    Move: 10 min - change `.gitignore:40` from `state/` to `state/*` (keep
    :41-42), add `!state/GENOME.md`, verify with `git check-ignore` rc=1 and
    `git status` listing the genome; not the moonshot's 30 min as written.

A2. "git ls-files is the spore manifest" contradicts the moonshot's own
    arithmetic: stripping 19 uploads + dist_audit (1,496 files) leaves ~54,846
    tracked files riding (17,070 watch/inbox + 26,749 memory untouched). The
    estate already holds the right manifest: TWO_MACHINE_SYNC_20260919.md:45
    tier-1 "Fleet proper" = ~4,000 files < 0.1 GB (mag 1,881, scripts 211,
    tools 48, queue 715, configs 52, docs 528, tests 275, live ledgers, .env),
    implemented by scripts/build_travel_kit.py. Falsifier: a spore that
    deliberately ships all 47k+ scar files as payload (nobody wants this).
    Move: 30 min - derive the orphan spore branch from the travel-kit tier-1
    file list plus the named doctrine surfaces (genome, rails, rib_bus,
    memory/rib selected, canon selected), not from the full index.

A3. The spore's "keys stripped" leg is already mostly machine-enforced, which
    the lens never said: `.gitignore:19-22` ignores .env and whitelists only
    .env.example; `.gitignore:24` ignores configs/providers.yaml (the real
    wallet); tools/precommit_secret_check.py fail-closes on live .env values
    (DAY_SYNTHESIS_20260930.md:11-12, two live catches). An orphan branch
    built from the tracked tree inherits these guarantees. Falsifier: a live
    key shape in the tracked tree that precommit_secret_check cannot match
    (the gate's own honesty clause, DAY_SYNTHESIS:14: substring-match is only
    as wide as today's .env). Move: 15 min - run the tracked-tree key-shape
    sweep the AG1 receipt describes before any push, and bank the result in
    the spore receipt.

A4. The topic's spore list says "the arena carriers", but the arena's workflow
    side barely rides git: `.gitignore:198` ignores `.zcode/` entirely, and
    exactly ONE file under it is tracked - .zcode/workflows/the-gala.dwf.ts
    (`git ls-files .zcode` -> 1, `git check-ignore -v .zcode/workflows`
    reports nothing because tracked paths are exempt from ignore reporting).
    Content untouched per the night-loop ownership fence. Falsifier: a
    tracked-file census of .zcode/workflows reading >1 file (then the carriers
    do ride and this narrows). Move: 10 min, post-fence - the spore spec must
    enumerate .zcode/workflows explicitly (they do not ride by default) or
    drop the claim from the spore's payload list.

A5. Visibility is now a DECISION, not a discovery: the push target
    github.com/NachoBusiness17/mycelial-republic is publicly readable
    (anonymous ls-remote, credential helper disabled, rc=0 this sitting) and
    currently hosts the forest's unrelated 225-file game-bones lineage
    (merge-base with main: rc=1). Falsifier: the repo flips private or gains
    estate ancestry (re-run the two commands; either result kills a clause).
    Move: 15 min operator call - the orphan-spore plan must name its repo and
    visibility explicitly (private spore repo vs public one), because the
    current target is public and occupied.

## ONE-LINE VERDICT

The lens's five findings all survive byte-checking - every number I re-ran came
back exact except "36 lanes" (28) and two off-by-one line/file nudges - but the
finding-1 move would have silently done nothing (dead negation under a
dir-excluded parent, proven by the estate's own dead `!state/.gitkeep`), the
spore manifest it names still ships 47k scars, and the two scariest blind spots
(public repo, unrotated keys) were resolvable from this seat: the repo is
public, and the keys were rotated 09-30 with 401-probe receipts on file.
