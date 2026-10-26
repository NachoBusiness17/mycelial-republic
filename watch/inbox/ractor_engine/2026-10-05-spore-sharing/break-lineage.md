# break-lineage: hostile second pass on the spore-sharing lens report

Moment: 2026-10-05, this sitting. Tree: HEAD 7dac8685e879172056d2e156ad1e6310421bdf2d, branch mag/run-beta1-factory-build-audi-20260806T231709Z, working tree clean. Every cite below was executed or read in this sitting; commands named inline. No em-dashes.

## Verdicts

### Finding 1 "The spore push already exists and stalled" - CONFIRMED (one byte drift, one falsifier closed)

Byte-checks run this sitting:

- `git remote -v` -> `github https://github.com/NachoBusiness17/mycelial-republic.git` MATCHES. Addition the lens missed: a second remote `local C:\Users\foste\Documents\projects\Mag-backup.git` also exists.
- `git log github/master -1 --format="%H %cI"` -> `dc66499434b050343e81dabcb45b849c5f1fda29`, `2026-08-20T11:28:57-04:00` MATCHES the lens's dc6649943 / 2026-08-20.
- `git rev-list --count github/master..HEAD` -> **879**, lens said 878. HEAD moved (or miscount) between the two reads; direction and frame unchanged. Quantifier-law note: absolute counts are moment-bound.
- `git ls-tree -r github/master --name-only | wc -l` -> 225 MATCHES. Top-level names confirm "old framework/scaffolds/scrum shape": `.gitignore AGENTS.md CONTRIBUTING.md README.md configs data docs framework logs mycelia.cmd mycelia.ps1 pyproject.toml scaffolds scripts scrum selftest src tests`.
- Sibling checkout: `git -C ../mycelial-republic rev-parse HEAD` -> dc66499434b050343e81dabcb45b849c5f1fda29; `ls-tree -r HEAD | wc -l` -> 225. MATCHES.
- `git config core.hooksPath` -> `githooks` MATCHES. `githooks/pre-push:400-407` read: secret gate `--changed --baseline configs/secret_gate_baseline.json`, exit 1 blocks, catch-all fail-closed. MATCHES the lens's cite.
- **Falsifier closed by network check the lens did not run:** `git ls-remote github refs/heads/master refs/heads/main` returned `dc66499434b050343e81dabcb45b849c5f1fda29 refs/heads/master` and no main ref. The remote tip has NOT moved since the 2026-08-20 commit; the stalled-reseed frame stands. Public/private status still unverified (a successful ls-remote proves reachability, not visibility; cached credentials could serve a private repo).

### Finding 2 "The genome cannot regrow from a GitHub clone" - CONFIRMED (falsifier answered)

- `git check-ignore -v state/GENOME.md` -> `.gitignore:40:state/	state/GENOME.md` MATCHES exactly. Read `.gitignore:38-42`: `state/`, `state/**/*`, only negation `!state/.gitkeep`. No negation for GENOME.md was missed; the falsifier's negation arm dies.
- `git ls-files state/` -> exactly `state/NIGHT_LOOP_20261005.md` (1 file) MATCHES.
- `git ls-files | findstr /i genome` -> zero tracked genome copies anywhere. The falsifier's "tracked copy elsewhere" arm dies.
- `state/GENOME.md:69-75` read: "## 3. BOOT ORDER for a cold seat / 1. This file. 2. queue/STANDING_RAILS.md. 3. The ribs (memory/rib/). 4. state/CURRENT.md. 5. The Delta Register" MATCHES byte-exact (step 1 is the file itself).
- `git ls-files memory/rib/ | wc -l` -> 55 MATCHES. `queue/STANDING_RAILS.md` tracked MATCHES. `memory/rib_bus/doctrine.json` tracked MATCHES; structured recount via `.venv/Scripts/python.exe` json load: `len(ribs) = 26` (the lens's `grep -c invariant` = 26 lines also reproduced; note grep -c counts lines, the structured count is the honest 26-rib number).
- Addition: the mechanism generalizes beyond GENOME.md. `state/organ_vitals_chain.json` exists on disk and is untracked (git ls-files finds nothing matching organ_vitals_chain); `memory/runs/**` is ignored (`.gitignore:102`) which hides the arena capability chain (see addition A6). Note: the lens's organ path "seed_chain/seeds.jsonl" is WRONG as written; the tracked seeds ledgers are `memory/seed_chain/seeds.jsonl` and `memory/seeds/seeds.jsonl` (both confirmed tracked, both read: seeds.v1 rows with `"source": "operator"` fields, single-party shape visible in the data).

### Finding 3 "The de-riddled shareable was designed three times and never applied" - CONFIRMED (two corrections, surface bigger than stated)

- `docs/archive/ZEITGEIST.md:52-53` read: "**Non-negotiables (all six, unchanged):** your beads are not the network's property - ship / code/practice, not residual by default - scalar, not central ..." MATCHES (original renders as middle-dot separators). Instrument note: the phrase line-wraps between "ship" and "code", so `grep "ship code"` misses it (my first grep did); byte-read confirms.
- `watch/inbox/SEED_PUBLIC_PACK_20260925.md` read: :11-12 "MIT license (Copyright 2026 MARKK). No real secrets: keys.json is an awaiting-operator template" MATCHES; :15-19 the 3 pyc files with `C:\Users\foste\Documents\...` baked in MATCHES; :23-25 seal 55 -> 52 rows, 52/52 verified MATCHES.
- `watch/inbox/SEED_RIB_FORMAT_v0_20260926.md` read: :36-49 roles (law/doctrine/boot/receipt/ledger/pointer) and "a pointer is a promise with a hash, never a hand-wave" MATCHES; :64-76 verifier "never invents bytes for a pointer" MATCHES.
- `git ls-files watch/inbox/ | wc -l` -> **17,070** (lens said 17,069; tree moved by 1 between reads; direction confirmed).
- `git log --all --diff-filter=A -- .env` -> empty; `git ls-files .env` -> empty; `.gitignore:272 *.env`. .env never tracked in any ref CONFIRMED.
- keys.json redacted scan (python, values never printed): 118 strings total; overall max length 166 (`/_law` header prose), then 149/122/118/117 (status prose). The lens's "3 long strings, maxlen 35, all status/role prose" reproduces ONLY under a no-whitespace len>=25 filter: exactly 3 hits (`/grok_cli/role` 35, `/grok_cash/role` 30, `/hermes_1/role` 25), all role prose, maxlen 35 matches. Claim stands under that evident methodology; the threshold was unstated in the report and the unqualified "3 long strings, maxlen 35" is false as written (18 strings >= 25 with whitespace allowed).
- `mag/route_chat.py:56-72` read: `_keys_for` reads `os.environ[env]` first, then falls back to the single `ROOT/.env` (line 67). Single-tenant .env door CONFIRMED.
- `configs/providers.yaml` lines 486, 571, 658, 706 read: 486 "dormant: true   # 2026-09-26 B2-61: generation 401-dead; operator GO flips this + re-adds to routing"; 571 "dormant: true"; 658 "dormant: true   # ... operator GO flips this"; 706 "name: Cerebras (card-gated 30-day trial, dormant pending operator GO)". ALL FOUR MATCH.
- Falsifier checked: `docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md:51` reads `| **Forest** | mycelial-republic | Public law, fork, optional republic train |`. The compass licenses shipping PUBLIC LAW to the forest; it neither licenses nor forbids shipping residual. It does not overturn the finding; it also leaves the operator-order door the lens named open.
- CORRECTION (addition A4 below): the residual shipping surface is materially larger than "17,069 watch/inbox files": `git ls-files memory/ | wc -l` -> 26,749 (memory/corpus 22,425, memory/worldline 2,159, memory/dead_drops 537, memory/continuity 395).

### Finding 4 (GPS schema / rib_bus, TRUNCATED IN THE REPORT) - visible evidence CONFIRMED; finding body NOT RECEIVED

The report ends mid-evidence at "mag/rib_bus.py:78-83 _sa"; no finding/falsifier/move text was delivered for this row, so a full verdict is impossible against the lens's own words. What was visible, byte-checked:

- `tools/gps_mcp/ledger.py:133-146` read: `CREATE TABLE IF NOT EXISTS capability` with columns model_id, task_shape, pass_rate, sample_size, cost_usd_per_call, last_measured, updated_at; `PRIMARY KEY (model_id, task_shape)` at :141. NO operator column CONFIRMED.
- `grep -n "merge" tools/gps_mcp/ledger.py` -> zero hits CONFIRMED (my combined grep shows all "claim/operator/lock" hits are evidence-hash semantics and prose comments, e.g. :95 "upsert_measurement (the fixture/operator path)", :329 "cost is seeded or updated by operators/fixtures"; no merge, no tenant key).
- `mag/rib_bus.py:78-83` read: `_save_store` does `f.write_text(json.dumps(store...))` over the whole file; `grep -n "claim|lock|lease|merge" mag/rib_bus.py` -> prose hits only (:4, :195). No claim system CONFIRMED; the store write is last-writer-wins.
- Addition A6 below sharpens this into the concrete N=2 failure at the gwap SessionLedger layer.

## Blind-spot status after this pass

1. "season ledger"/"season chain" names: STILL ZERO bytes by those names; my instrument: `grep -rln "season ledger\|season chain" --include="*.md" state/ queue/ memory/rib/ docs/` -> zero files; `grep -rln "season" --include="*.py" tools/ mag/` -> 10 files, all prose uses (e.g. mag/swarm_cycle.py:7 "wait is a season"). The lens's closest-organ list contained two wrong paths, corrected in finding 2 and addition A7. Real organs now named with bytes.
2. Fulltree secret gate: I STARTED `.venv/Scripts/python.exe tools/secret_gate.py --full` this sitting; it ran ~15 minutes without completing (whole-tree scan; help text: `--changed` is the "fast path, for pre-push", `--full` is "whole-tree scan (offline / scheduled)"); I stopped it at budget. NOT COMPLETED: whether tracked receipts would block a push remains inferred, now with the added measurement that fulltree is heavyweight by design. Flag exists at tools/secret_gate.py:117.
3. External GitHub state: CLOSED for tip movement by `git ls-remote` (finding 1). Public/private and branch protection: STILL UNVERIFIED this sitting.
4. Tutorial not drafted, no provider lane probed: unchanged, still open (out of this pass's scope).
5. N=8 concurrent behavior: no execution test this sitting either; but the N=2 mechanism is now byte-derived (addition A6), not just schema-inferred.
6. Arena cron registration: STILL UNLOCATED. My instrument: `grep -rln "arena" scripts/` -> only unrelated build scripts (build_deck.py, build_lane_game.py, vast_paces_full.py) and a mimosa hook-state blob; `queue/STANDING_RAILS.md:44` carries only the invocation row "any finished session/run | tools/arena_gwap.py <run_dir> | chain-verified capability row -> GPS"; tools/arena_gwap.py:35 mentions "dawn gwap line" implying a scheduled task. The registration byte is OWED by both passes.

## Additions (what the lens missed)

### A1. The remote-tip falsifier is closable and now closed
Evidence: `git ls-remote github refs/heads/master refs/heads/main` -> `dc66499434b050343e81dabcb45b849c5f1fda29 refs/heads/master`, no main (run this sitting). Falsifier: a moved tip or an auth failure would reopen finding 1. Move: 0 min, record and carry on; the stalled-reseed frame is the true frame.

### A2. There is a second remote the lens never named
Evidence: `git remote -v` second row `local C:\Users\foste\Documents\projects\Mag-backup.git` (fetch+push). Falsifier: if that path is dead (no bare repo on disk), it is a stale config row only. Move: 10 min, name the local backup as the first reseed target in the spore plan (fastest non-network reseed) or strike the stale remote.

### A3. The GPS capability ledger is TRACKED and ships; the lens's move wrongly lists it as pointer-only
Evidence: `git ls-files *.db3` -> `tools/gps_mcp/gps_ledger.db3`. The lens's finding-3 move lists "gps_ledger.db3" among pointer artifacts, but it is already in git: a push ships every measurement row (model costs, pass rates, evidence hashes) and two estates' rows collide on PK (model_id, task_shape) per ledger.py:141. Falsifier: if the tracked db3 is an empty/stub file, the leak is only path-level. Move: 15 min, add gps_ledger.db3 to the strip list (git rm --cached + ignore) or template it, before any spore branch exists.

### A4. The residual shipping surface is roughly double what finding 3 states
Evidence: `git ls-files memory/ | wc -l` -> 26,749; breakdown memory/corpus 22,425, memory/worldline 2,159, memory/dead_drops 537, memory/continuity 395. Combined with watch/inbox 17,070 the tracked residual is >= 43,819 files. Falsifier: if memory/corpus is classified "practice not residual" by the beads/forest split, the framing changes but the byte count stands. Move: 10 min, size the spore manifest against memory/ too, not just watch/inbox.

### A5. A live session brief is tracked
Evidence: `git ls-files memory/warm_state.json` -> tracked; structure read: top keys schema, generated, chain, deployments, session_brief, verify. It is rewritten by warm boot per AGENTS.md. Falsifier: if its content is fully generic (no URLs, no session facts), shipping it is harmless; I did not read its values. Move: 5 min, template or strip it in the spore build.

### A6. The N=2 break is byte-derivable and sharper than the lens's static claim: fail-closed denial, not corruption
Evidence: `mag/gwap_payload.py:93` `STORE = ROOT / "memory" / "runs" / "gwap"`; :728 one file per session_id (`arena-capability.jsonl`, confirmed on disk, ignored via `.gitignore:102 memory/runs/**` per `git check-ignore -v`); :761-780 `append()` does verify -> `seq = len(self._rows) + 1` -> open-append-write with no lock, no claim, no operator identity. Two concurrent writers both compute seq N+1 against the same file; the next open raises BROKEN_CHAIN (:736-739). The GPS side collides on PK (model_id, task_shape), ledger.py:141, and the tracked db3 would merge by whoever pushes last. Falsifier: an execution test with two concurrent appenders that both succeed and re-verify would kill the race claim; not run this sitting. Move: 30 min, the shareable spec must state the concurrency law: per-operator session ids plus a receipt-exchange merge (or accept fail-closed collisions as the N>1 contract), and the db3 needs an operator key before any multi-estate merge.

### A7. The lens's organ map needs three path corrections
Evidence: "seed_chain/seeds.jsonl" does not exist (`ls seed_chain/` -> No such file); tracked organs are `memory/seed_chain/seeds.jsonl` and `memory/seeds/seeds.jsonl`; "organ_vitals_chain.json" is `state/organ_vitals_chain.json` (exists on disk, untracked; nothing tracked matches). Falsifier: none pending, these are byte locates. Move: 10 min, correct the organ map before the spore manifest cites paths that do not exist.

### A8. The fulltree gate belongs on a schedule, not in a sitting
Evidence: this sitting's `--full` run: started, ~15 min wall clock, no completion, stopped; CLI help names `--full` "offline / scheduled" and `--changed` the pre-push fast path. Falsifier: a completed fulltree run over this tree under 5 minutes would make the lens's original blind spot cheap to close. Move: 15 min, hang `--full --json` off the existing daily patrol pattern (census patrol daily task shape) instead of asking any single window to block on it.

## Count-drift ledger (quantifier law)

- 878 (lens) -> 879 (`git rev-list --count github/master..HEAD`, this sitting): HEAD moved between reads.
- 17,069 (lens) -> 17,070 (`git ls-files watch/inbox/ | wc -l`, this sitting): one inbox file landed.
- Both absolute numbers are moment-bound; the lens's frames survive the drift.
