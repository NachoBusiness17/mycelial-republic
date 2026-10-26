# break-dogfood: hostile second pass on the spore-sharing lens report (2026-10-05)

Pass scope: byte-check every evidence cite in the lens report, attack each falsifier,
run what the lens left OWED where feasible, and bank what the lens missed.
Every check below was executed this session unless marked OWED / not run.
Shell note: this seat's Bash tool is Git Bash; the pass initially mis-invoked cmd's
`find /c /v ""` (GNU find walked C:\ and was killed, task exec_3ce06939); all counts
below were re-taken with `wc -l`.

## Verdicts

### F1 "The declared inheritable artifact does not travel with the declared transport" - CONFIRMED (CONVERGENT)

Every byte checked out:

- `git check-ignore -v state/GENOME.md` -> `.gitignore:40:state/	state/GENOME.md` (lens cite exact).
- `git ls-files state/` -> exactly one file: `state/NIGHT_LOOP_20261005.md` (lens cite exact).
- `git ls-files watch/inbox/ | wc -l` -> 17,070 (lens 17,069, +1 drift).
- `git ls-files | wc -l` -> 56,361 (lens 56,359, +2 drift).
- state/GENOME.md:3-4 carries "The inheritable artifact" (lens cited 1-3; the phrase sits at 3-4; imprecision only).
- scripts/build_travel_kit.py:34-37 DIR_INCLUDES omits `state/`; lines 40-45 MEMORY_EXCLUDE includes `spore_seeds` (both exact). Note the kit is a PRIVATE transport and line 156's root-file loop packs root `.env` into it (the docstring at :3 says "code + live ledgers + packs + .env").
- Falsifier attacked: `git grep -l "GENOME.md" -- scripts tools mag configs` -> exit 1, ZERO code references in any builder dir. Broad census `git grep -l "GENOME" | wc -l` -> 107 tracked files, all prose/data/receipts, no assembler. No second builder exists.
- History attack (mine, beyond the lens): `git log --all --format="%h %ad %s" --date=short -- state/GENOME.md` -> EMPTY. The genome was never committed on any ref. A full-history push does not carry it either.
- Context the lens lacked: docs/GITHUB_PUBLISH.md (tracked, last touched eb07ad62e 2026-08-04 "clean publish baseline") lists `state/` on its "What stays local (never push)" side, so the genome's gitignore is CONSISTENT WITH A WRITTEN DECISION that predates the genome (genome day-one edition is 2026-10-03 per state/GENOME.md:1). The riddle is sharper than "never wired": the transport law (08-04) never learned the artifact (10-03) exists.
- Convergence: all 10 sibling lens files mention GENOME + gitignore (`grep -c` census, 4-8 mentions each); accuracy.md discusses the .gitignore blocks directly. Emphasis, not novelty, per the quantifier law: CONVERGENT, outranks novel single-source.

### F2 "The spore transport points at a stub" - CONFIRMED (CONVERGENT), with one material omission (see A1)

- `git ls-remote github` (full ref listing, not just heads) -> exactly 2 lines: `HEAD` and `refs/heads/master`, both dc66499434b05. ZERO tags. This CLOSES the lens's tags blind spot: no tag-based share escapes the claim.
- `git rev-list --count github/master` -> 1; `git log -1 ... dc6649943` -> 2026-08-20T11:28:57-04:00 "Add the game bones to the framework... (distributed collaborative storytelling)" (exact).
- `git rev-list --count main` -> 5 (exact); HEAD -> 879 (lens 878, +1 drift).
- Disjointness is STRONGER than claimed: `git merge-base dc6649943 main` rc=1 AND `git merge-base dc6649943 HEAD` rc=1 (no common ancestor with either), so the remote tip is disjoint from the living branch too, not just from main.
- `git remote show github` -> "master pushes to master (local out of date)" (exact); `git branch -r` -> exactly `github/master` + `local/run-beta1-factory-audit-20260914` (exact).
- The omission: the lens's frame "a transport that does not yet carry the estate anywhere" ignores mag-sovereign-seed (addition A1): a second, LIVE, tagged public repo that has carried a curated slice of the estate since 2026-09-30 and was updated 2026-10-04.
- Convergence: security.md:43 cites the same merge-base rc=1 + dc6649943 stub. CONVERGENT.

### F3 "The single-tenant seams are exactly where the topic said" - CONFIRMED (CONVERGENT), one precision fix

- mag/route_chat.py:46 USAGE constant (exact); :61-72 `_keys_for` reads os.environ then line-parses ROOT/.env (lens 61-70, close); :211-215 `_bank` row fields ts/lane/model/goal/tokens/ok/error/detail with NO operator/seat field (exact).
- mag/lane_runner.py:124-149 `_save_state` atomic tmp+replace (exact). PRECISION FIX: the lens read :134-139 as "lock-free last-writer-wins by its own comment"; those lines are the Errno-22 cure prose and :134 actually asserts "the lock is external and transient, not code-side" (a host-side mount lock, not a claim protocol). The structural claim stands on the code itself: full-state overwrite, no merge, no claim primitive (`git grep -n "claim\|lease" -- mag/lane_runner.py` matches prose only).
- mag/constants.py:6 SPORE_SEED_FILE template (exact); mag/spore_seed.py:42-80 generate / :83-94 validate (exact); :97-99 `_seed_file` formats seat_id (move's :99 cite lands).
- tools/gps_mcp/seed_fixtures.py:100-106 default `--db` is package-local gps_ledger.db3; `git ls-files tools/gps_mcp/gps_ledger.db3` -> tracked (exact).
- Falsifier census: `git grep -ln "sync\|push\|remote" -- tools/gps_mcp/` -> only tools/gps_mcp/test_gps_mcp.py (a test). No cross-seat sync mechanism exists in the module (14 files).
- Absence re-census per quantifier law: `git grep -ln "spore_seed" -- mag tools scripts tests dashboard docs` -> 7 files: mag/constants.py, mag/spore_seed.py, scripts/build_travel_kit.py (the MEMORY_EXCLUDE string), tests/test_spore_seed.py, docs/ref/SPORE_CONTINUITY_SCHEMA.md, two dashboard htmls. NO runtime consumer: "nothing downstream reads it" holds, scoped to tracked code this session.
- MEASURED addition (this session, temp copy of gps_ledger.db3, tracked file untouched): journal_mode=delete, tables capability+verdict_log; with a writer holding the file, two competing writers got "database is locked" 20/20 each at busy_timeout 300ms; without a holder, two racing writers ran 40/40 clean. So sqlite's own locking already handles same-file N=2: the silent fork is specifically the CROSS-MACHINE case (no shared file at all). The N=2 break is distribution, not contention.
- Half-present primitive the lens missed: mag/lane_runner.py:125 `st.setdefault("seat", lane)` - a "seat" field already exists in runner state, but it stores the LANE name, not a machine identity.
- Convergence: route_chat discussed in 5 sibling files (logic 6, economics 9, operations 5, accuracy 3, security 1 mentions). CONVERGENT.

### F4 secret-scan adjudication gap - evidence CONFIRMED (byte-exact); finding/move text was truncated in the handoff

Visible cites, all verified:

- watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json: `census.scanned` = 46,996 (exact); `rule_counts` present with the 14 rules; `severity_counts` = None; no blocking key in the JSON keys (exact).
- Context the lens lacked: tools/secret_gate.py:29-31 - AWS-SECRET-40, GENERIC-KEYASSIGN, ENV-ASSIGN, JWT-TRIPLE, GENERIC-BEARER NEVER block; only specific provider shapes block at/above --severity (default high). So B2-73's unadjudicated pile is by-design non-blocking noise plus a buried signal.
- The gate DOES run today: 7 changed-mode results exist at watch/inbox/secret_gate_results/changed_20261005T*.json (07:56Z through 12:14Z; first scanned 13 files, zero findings).
- MEASURED this session: `tools/secret_gate.py --full /tmp/mss_clone --json` on the PUBLIC seed clone -> 1,681 files scanned, blocking_count 0, critical 0, high 1 (AWS-SECRET-40 at docs/ref/MAG_LLM_FEED_PACK.md:40, masked "com/Na..." = URL-shaped, not an AKIA key), medium 1 (GENERIC-BEARER inside the MCP spec mirror docs/mirrors/mcp/). The public share is secret-clean by the estate's own instrument as of 2026-10-05T12:18Z (results: watch/inbox/secret_gate_results/full_20261005T121837Z.json).
- Tracked-tree scan COMPLETED this pass: `git archive HEAD` -> 56,362 files exported to /tmp/lsarchive -> `tools/secret_gate.py --full /tmp/lsarchive --json` (runtime 1,897.7s, generated 2026-10-05T13:27:30Z, results watch/inbox/secret_gate_results/full_20261005T132730Z.json). The tree a plain `git push` would ship scans 47,509 files (1.0GB) at **blocking_count 33** (high 144, medium 14, critical 0): blocking sample is pk_live STRIPE-KEY shapes in tracked scraped pages (boe003.html:257, boe_index.html:234, module_audit.ipynb:2307 len=107, corpus/tmp_enoch/boe012-017.htm:257) and a GOOGLE-OAUTH-AQ in cdx_rar.json:616; rule_counts include ANTHROPIC-KEY 1, DEEPSEEK-KEY 3, XAI-KEY 2, OPENROUTER-KEY 1, GROQ-KEY 1, STRIPE-KEY 11, GOOGLE-OAUTH-AQ 9, AWS-ACCESS-KID 5. Per-finding adjudication (operator-live vs scraped third-party vs placeholder) remains OWED: no secret values were printed this pass. STRUCTURAL POINT: the pre-push gate runs --changed (changed files only), so these 33 full-tree blockers sit invisible to every green changed-mode run (7 today) and would ship on a first full push, where `secret_gate.py --full` on this tree exits 1.
- Prior context: the 2026-09-27 "fulltree" run (watch/inbox/secret_gate_results/fulltree_20260927.json) scanned the DISK tree (2.36M files, 30.9GB, scope_basis "tree") and reported 3,606 blocking incl. 42 PRIVATE-KEY-BLOCK criticals with corpus samples (boe003.html STRIPE-KEY) - a different question than the tracked tree, now answered above.

## Additions (what the lens missed)

### A1 The share already exists: mag-sovereign-seed is live, tagged, and fresher than the lens's world

Evidence: `git ls-remote https://github.com/NachoBusiness17/mag-sovereign-seed` -> main=cbda4d8, tag v1.0.0=1741d93. Clone (shallow) tip commit: 2026-10-04T19:32:02-04:00 by NachoBusiness17, "THE STARTER KIT v0.2...". 1,684 files incl. boot/ (AGENTS.md, CONSTITUTION.md, main.py, mag.cmd, docker-compose.yml), docs/ (full tree per PROVENANCE.md), mag/ (1,099 files, bytecode-stripped), memory/ (MEMORY.md + briefs/latest.md + doctrine/ only), story/, starter-kit/. PROVENANCE.md documents the 2026-09-30 export ("read-only pulls from the live estate over SSH"), the exclusion table (.env never pulled; memory/biography per docs/GITHUB_PUBLISH.md "never push"; memory/seals cut because seals embed configs/providers.yaml; corpus; dashboard/watch/state/queue/scripts/tools/tests bulk), and a two-tier secrets audit ending "zero live secret values in this package" (re-verified by my scan above).
Falsifier: repo deletion or a provenance document proving the seed was never public would kill this; both falsifiable by re-running ls-remote and reading PROVENANCE.md in the clone.
Move (45 min): stop designing the share from scratch. The delta the estate actually owes the world is the gene layer neither repo carries (state/GENOME.md, memory/rib_bus/, queue/STANDING_RAILS.md, the rails door itself: mag/route_chat.py is absent from the seed's mag/). Amend docs/GITHUB_PUBLISH.md with the split: seed = method/docs (exists), spore branch = living inheritance (missing).

### A2 The estate has a written publish law the lens never opened

Evidence: docs/GITHUB_PUBLISH.md, tracked, last touched eb07ad62e 2026-08-04 "Mag sovereign agent - clean publish baseline." It already decides what ships (mag/, main.py, dashboard/, tests/, config TEMPLATES, launch scripts) and what never pushes (.env, memory/biography/, agent_sessions/, attention.md, logs/, state/, queue/todo.md). Its remote example names a THIRD repo, github.com/NachoBusiness17/Mag (`git ls-remote` -> "Repository not found"; GitHub returns the same 404 for private repos, so nonexistent-vs-private is OWED).
Falsifier: a newer law superseding it would weaken this; `git log --all -- docs/GITHUB_PUBLISH.md` shows no successor.
Move (20 min): make GITHUB_PUBLISH.md the single source: fold in the genome clause, the seed-repo reality, and the dead Mag remote example (delete or replace with mycelial-republic).

### A3 A TLS private key rides in git history: any full-history push ships it

Evidence: `git log --all --diff-filter=A -- "*.env" "*.pem" "*.key"` -> memory/tls/lan.key; adding commit 799ddb6fe ("wip 20260819... LOCAL ONLY, not pushed"); .gitignore:271 says verbatim "lan.key untracked same day; rotate - it remains in history"; disk file exists (1,675 bytes, mtime 2026-08-14 12:41, never rewritten since: rotation status OWED, key bytes intentionally not read or printed this pass). `git log --all -- .env` -> empty (the .env itself is history-clean).
Falsifier: evidence the key was rotated after 2026-08-14 (rewritten bytes, or a dated rotation receipt) downgrades this to hygiene; absence of such evidence in memory/tls/ and the mtime support the current read.
Move (15 min): the lens's own orphan-branch move for the spore is now load-bearing, not stylistic: an orphan spore branch from HEAD carries no history; a plain push of the work branch ships lan.key at 799ddb6fe. Decide orphan-vs-filter-repo BEFORE any push.

### A4 starter-kit has already forked into two diverging copies, and the shipped quickstart is broken

Evidence: local tracked starter-kit/ (33 files, tip 229f13173 2026-10-04 19:31:03 "STARTER KIT v0.2...") vs the public repo's starter-kit/ subdir (public tip cbda4d8, 19:32:02, same minute, different message): `diff -rq starter-kit/ /tmp/mss_clone/starter-kit/` -> .env.example only local, .gitignore/BOOT/INSTALL/LAWS/LAWS_PROVENANCE/PROTOCOLS/README/ZEITGEIT/agent cards/laws.json/installers all differ. BOTH copies carry the same quickstart (README line 18-19): `git clone .../mag-sovereign-seed starter-kit && cd starter-kit` then `python tools/kit_doctor.py` - but `cd starter-kit` lands at the SEED ROOT, which has no tools/ (ls /tmp/mss_clone -> no tools dir); kit_doctor.py lives at starter-kit/tools/kit_doctor.py inside the clone (find /tmp/mss_clone -name kit_doctor.py).
Falsifier: if the public repo later re-rooted the kit at repo top (tools/ at root), the defect dies; verified absent at the 2026-10-04 tip.
Move (30 min): pick one authoritative kit location (repo subdir), fix the two-line quickstart in both copies, and reconcile the 19 diverged files or declare the public one canonical.

### A5 The rails door's config has no tracked template anywhere

Evidence: mag/route_chat.py:51 reads ROOT/configs/providers.yaml at runtime; .gitignore:24 ignores configs/providers.yaml; `git ls-files configs/ | grep -i provider` -> empty (rc=1). The publish law promises "Config templates (configs/*.yaml)" but the one file the rails default needs ships nowhere (root .env.example and starter-kit/.env.example exist; no providers.yaml example in any tracked dir).
Falsifier: a tracked template under another name (e.g. inside docs/) would weaken this; grep of configs/ and starter-kit/ found none this session (scope: `git ls-files` + starter-kit listing).
Move (20 min): commit configs/providers.yaml.example with lanes + fences + api_key_env NAMES only; this also firms the convergence with the accuracy lens the report hedged in blind spot 2: the accuracy lens's "no tracked template" finding is CONFIRMED by this census.

### A6 Dormant multi-seat primitives already exist; the N-operator design does not start from zero

Evidence: mag/spore_seed.py (seat identity bound to verkle root; memory/spore_seeds/ holds zcode.jsonl + testseat.jsonl on disk); mag/seat_fork.py (fork-seat-from-frozen-tip stub; import census: only scripts/hofw_001_seed.py + .sh); mag/seats.py (dashboard Body-tab seat registry: agent-session seats, not human operators; imported by mag/chronicle.py + mag/seat_availability.py); docs/ref/SPORE_CONTINUITY_SCHEMA.md (spec). The rib bus has no claim primitives: mag/rib_bus.py (274 lines) has zero claim/lease matches.
Falsifier: a live caller of seat_fork/spore_seed outside those files would change the dormancy claim; the census above is the instrument (git grep, tracked tree, this session).
Move (10 min): the MAG_SEAT_ID wiring move from finding 3 should source its default from the existing spore seed file (last record of memory/spore_seeds/zcode.jsonl), not invent a new identity store.

### A7 The cron layer is Windows-only and unported: the regrow guide's silent gap

Evidence: `git ls-files scripts/ | grep -c "\.ps1$"` -> 51; schedulers include scripts/register_census_patrol_task.ps1, register_fts_index_task.ps1, register_corpus_rescan_task.ps1, register_day_end_task.ps1, register_endpoint_news_task.ps1 (git grep schtasks/Register-ScheduledTask census); AGENTS.md names MagImproveDaily/MagCensusPatrolDaily/MagFtsIndexDaily. Nothing equivalent for non-Windows exists in the tracked tree.
Falsifier: a tracked cross-platform scheduler (compose service, cron file) would kill this; none surfaced in scripts/ or configs/ this session.
Move (30 min): the regrow guide (topic question 4) must either port the ~6 daily tasks to a cross-platform runner or declare them Windows-OWED; the arena surfaces themselves are tracked (mag/arena_*.py, configs/arena_probes.yaml, configs/arena_strategies.yaml) but their trigger lives in the Windows layer.

## Not run / OWED

- lan.key rotation since 2026-08-14: OWED (bytes not read; would need the operator's rotation records).
- github.com/NachoBusiness17/Mag existence vs privacy: OWED unauthenticated ("Repository not found" covers both).
- The 33 tracked-tree blocking findings: MEASURED (see F4), but each row's live-vs-scraped-vs-placeholder adjudication is OWED (values never printed; would need human eyes or a sanctioned value-inspecting pass).
- Local starter-kit vs public starter-kit authoritative-winner: OWED (divergence measured; per-file adjudication not done).
- Finding 4's full finding/move text: truncated in the handoff; verdict rendered on the visible evidence cites only.
- The seed repo's full history and the v1.0.0 tag target: shallow clone only (depth 1); tag object not fetched.
- mag-sovereign-seed vs current estate drift inside mag/ and docs/: sampled (route_chat.py absent; spore_seed.py present), not fully censused.
- Cleanup note: pass artifacts live in temp only (/tmp/mss_clone, /tmp/lsarchive, break_dogfood_sqlite_test.py) and were never written into the estate tree except this banked file.
