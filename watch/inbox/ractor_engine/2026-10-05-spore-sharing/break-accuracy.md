# BREAK-ACCURACY - hostile second pass on the accuracy lens (2026-10-05)

Pass: break-accuracy. Target: `watch/inbox/ractor_engine/2026-10-05-spore-sharing/accuracy.md`
(the lens's own banked report, read in full this session; the ask's excerpt truncated
finding 4 mid-falsifier and omitted finding 5 entirely - both recovered from the banked
file). Every check below was RUN in this session, moment 2026-10-05T11:59:48Z,
HEAD 7dac8685e, branch mag/run-beta1-factory-build-audi-20260806T231709Z. The tree is
HOT (commits and lane rotations land continuously), so counts drift: every count below
names its moment. Shell note: the harness shell is POSIX-flavored here; `dir /b`
invocations failed as GNU dir and were replaced with `ls` / `git ls-files`.

## VERDICT SUMMARY

| Finding | Verdict |
|---|---|
| F1 push target already the forest's; estate push radioactive | CONFIRMED (one stale cite, substance intact) |
| F2 spore cannot boot Genome Law 1 (no tracked providers.yaml) | CONFIRMED (one wording defect; STRENGTHENED by a fact the lens missed) |
| F3 routing brain is tracked shared state (gps_ledger.db3) | CONFIRMED (drift since lens moment measures the hazard) |
| F4 fork-and-trade is the republic's answer | CONFIRMED (one mis-attributed .gitignore comment; falsifier probed clean) |
| F5 topic numbers half-fail the byte check | CONFIRMED (one OWED resolved by this pass, see A2) |

## F1 - CONFIRMED

Byte-checks run this session:

- `git remote -v` -> `github https://github.com/NachoBusiness17/mycelial-republic.git`
  fetch+push. Exact. (Second remote exists that the lens never named: `local`
  C:\Users\foste\Documents\projects\Mag-backup.git - see A7.)
- `git ls-remote github` -> HEAD and refs/heads/master both
  `dc66499434b050343e81dabcb45b849c5f1fda29`. Exact.
- `git -C ../mycelial-republic remote -v` -> `origin` = same URL. Exact.
- `git -C ../mycelial-republic log --oneline -5` -> `dc66499 Add the game bones...`
  then `3da416c Add Sovereign Framework: the real machine core (30 mag modules +
  configs + build files) opened for collaboration, runtime/secrets excluded,
  secret-scanned`. Verbatim.
- `git log --all --diff-filter=A --format="%h %ad %s" --date=short -- "*.key" "*.pem"
  "*.env"` (the lens's exact instrument) -> exactly ONE hit:
  `799ddb6fe 2026-08-19 wip 20260819: ... (LOCAL ONLY, not pushed)`.
- `git cat-file -s 799ddb6fe:memory/tls/lan.key` -> `1675`. Exact. Content not printed.
- `git count-objects -vH` -> `size-pack: 14.37 GiB`. Exact. (count 12794 vs lens 12782,
  +12 drift; 4 garbage tmp_pack warnings vs lens 3, 973.47 MiB garbage - interrupted
  fetch residue, immaterial.)
- `git ls-files | wc -l` -> 56,361 (lens: 56,359); `git ls-files watch/inbox | wc -l`
  -> 17,070 (lens: 17,069); all-.md under watch/inbox -> 5,062 (lens: 5,061).
  +2/+1/+1 hot-tree drift; instrument named (git ls-files, this moment).
- .gitignore:270-271 -> `# grok-bot estate audit 2026-10-03` /
  `# secrets / key material (lan.key untracked same day; rotate - it remains in
  history)`. Verbatim. .gitignore:30-34 -> the 2026-09-30 block:
  `# 7 live .env values were committed in it (audit 2026-09-30 finding #1).`
  `# Untracked 2026-09-30; history left intact per operator (no rewrite).` Verbatim.
- Radiosensitivity proof: `git branch -a --contains 799ddb6fe` lists the current
  branch (mag/run-beta1-factory-build-audi-20260806T231709Z) plus reboot-staging and
  sweep/kill-list-stage1 - pushing ANY of these ships the blob.

Cite defect, does not kill the finding:

- STALE: "dc66499434 ... is NOT an object of this repo (git cat-file -t -> fatal)".
  This session `git cat-file -t dc66499434` returns `commit`, and
  `git rev-parse refs/remotes/github/master` = dc66499434b05... The reflog dates it:
  `refs/remotes/github/master@{2026-10-05 07:08:28 -0400} ... fetch github master
  --depth=1: storing head`. The claim was true at the lens's moment only if the lens
  ran before 07:08 EDT; it is unreproducible now. Corollary checks:
  `git rev-parse refs/heads/github/master` -> fatal (no such local branch; the
  `github/master` line in branch -a output is the remote-tracking ref), and
  `git merge-base --is-ancestor 799ddb6fe dc66499434b05...` -> rc=1 (shallow-boundary
  caveat: .git/shallow exists, 1 entry; the forest's own full log shows no lan.key
  commit, so the blob is not in remote history).
- Supporting nuance the lens missed: the lan.key commit message itself ends
  `(LOCAL ONLY, not pushed)` and ls-remote shows only the forest tip on the remote -
  the leak is PROSPECTIVE (the first estate push), not already-public. The finding
  already says exactly this.

Falsifier: unchanged, still valid (repoint github + orphan-root + pass --history).
`tools/secret_gate.py check --history` NOT RUN by lens or by this pass (14.37 GiB
operator-scale; flag confirmed at tools/secret_gate.py:119-120, help text verbatim
"scan every ADDED line across git history").

## F2 - CONFIRMED (and STRENGTHENED; one wording defect)

- mag/route_chat.py:51 -> `cfg = (ROOT / "configs" / "providers.yaml").read_text(...)`
  inside `_load_lanes`. Exact line.
- The .env fallback: `_keys_for` at :56-72; the literal line-scan of ROOT/.env is
  :67-70. The lens cited ":61-70"; the read lives at 67-70, inside the cited range.
- .gitignore:23-24 -> `# live provider/mesh credentials - never commit (tracked fix
  2026-08-20)` / `configs/providers.yaml`. Verbatim.
- `git ls-files configs` -> no providers.yaml (full listing inspected, 80+ entries).
- `git check-ignore -v configs/providers.yaml` -> `.gitignore:24:configs/providers.yaml`.
- .env.example tracked; head reads `# Copy to .env and fill. Never commit .env.` and
  carries XAI_API_KEY/XAI_MODEL/OPENROUTER/OPENAI/ANTHROPIC/GROQ/DEEPSEEK/
  DEEPSEEK_OVERMIND/GEMINI/TOGETHER/VAST keys. Exact as the lens said.
- state/GENOME.md:16-19 (Law 1, "Any model call goes through mag/route_chat ...") and
  queue/STANDING_RAILS.md:10-12 ("The front door is `mag.route_chat` ..."). Verbatim.

Wording defect: the ask-excerpt's "(only untracked configs/providers.yaml.bak-...
on disk)" is wrong as stated. On disk are BOTH the live configs/providers.yaml
(40,724 bytes, mtime Oct 3 20:32) and the .bak (22,418 bytes, Aug 26). The live file
is what route_chat reads; both are untracked-ignored. Substance intact.

STRENGTHENING FACT the lens missed (A1): state/GENOME.md ITSELF is untracked.
`git check-ignore -v state/GENOME.md` -> `.gitignore:40:state/  state/GENOME.md`;
`git ls-files state/` -> exactly one file, `state/NIGHT_LOOP_20261005.md`, force-added
today by commit 23d76bb71. Boot order step 4's state/CURRENT.md is equally untracked
(state/ is ignored wholesale, .gitignore:40-42). The cold-operator gap is larger than
the lens stated: the genome itself, the "inheritable artifact", is not on the
shareable surface. Law 1 is unbootable AND its owning document does not travel.

Falsifier: unchanged; a tracked providers.yaml.example cures the named half. Cut it
from the LIVE file, not the .bak (A8).

## F3 - CONFIRMED

- tools/arena_gwap.py:57 -> `GPS_LEDGER = ROOT / "tools" / "gps_mcp" /
  "gps_ledger.db3"`. Exact line.
- `git ls-files tools/gps_mcp | grep db3` -> BOTH `tools/gps_mcp/gps_ledger.db3` AND
  `tools/gps_mcp/gps_ledger.db3.bak_pre_D2_20260930` tracked. Exact.
- `git log -1 --format="%h %ad %s" --date=iso -- tools/gps_mcp/gps_ledger.db3` ->
  `e80f48b8f 2026-10-05 03:36:34 -0400` (committed today). `stat` -> 782,336 bytes,
  mtime 2026-10-05 03:15:15 -0400. Both exact.
- `git status --porcelain queue/lanes` -> M on builder/day_work/research
  runner_state.json AND on all three trail.jsonl files (the lens named only the
  runner_state trio).
- Live drift MEASURES the hazard: queue/lanes/research/runner_state.json read
  rotation_epoch 242 / last_run 2026-10-05T11:01:10Z at the lens moment; at this
  pass's moment (11:59Z) it reads rotation_epoch 249 / last_run
  2026-10-05T11:33:02.273563+00:00. Seven epochs in under an hour on a TRACKED file.
  The shared-state claim now has a drift rate, not just a mechanism argument.
- mag/lane_runner.py:134 -> `# the lock is external and transient, not code-side).
  That abort killed`. Exact line. :139 -> `# rename-CAS pattern mag/bay_organs.py
  proved against win32 filter locks.` Exact line.
- No claim/lease layer in the runner: `grep -rnE "lease|claim" mag/lane_runner.py`
  hits only prompt/comment prose (3 lines). Lens's scope ("in the runner") is honest.

N=4/N=8 gradients remain design analysis (lens blind spot 4 says so); nothing
measured exists. The finding never claimed otherwise. CONFIRMED as structural.

Falsifier: unchanged (untrack + seed fixture, or per-operator namespacing + claim
layer). Move still ~45 min.

## F4 - CONFIRMED (one mis-attributed comment; falsifier probed clean)

Recovered from the banked accuracy.md:121-153 (the ask's excerpt cut the finding body
and falsifier mid-sentence).

- ../mycelial-republic/README.md head read this session: "A living, forkable
  decentralized intelligence layer...", "Spores replicate. Nodes interconnect.",
  "Status: Phase 0 - Seed Mirror (Sprint 0.1)", canonical docs/AGENCY_SHAPE.md link.
  All verbatim.
- `ls ../mycelial-republic/docs/AGENCY_SHAPE.md ../mycelial-republic/docs/CONSTITUTION.md`
  -> both exist. Bodies still unread by lens AND by this pass (blind spot 5 stands;
  I extended the reach with a filename census, below).
- AGENTS.md:10 -> `**Zeitgeist:** beads (this repo) + forest (mycelial-republic)`.
  Exact.
- .gitignore:102-104 -> memory/runs/** ignored, whitelisting .gitkeep + README.md.
  Exact as lens said ("whitelisted only README").
- MIS-ATTRIBUTION: the lens quotes .gitignore "memory/seals/ is local-only
  ('opsec; chain data stays on the machine')". The `opsec; chain data stays on the
  machine` comment is on memory/biography_backup/** (.gitignore:65-66, "Rotating
  verkle backup - local only"). The memory/seals/ comment (.gitignore:26-29) reads
  "seal copies of the chain + providers.yaml - local-only snapshots (audit
  2026-09-30 finding #7; untracked from index 2026-09-30, history left intact per
  operator)". Substance survives - both blocks are chain-data-stays-local ignores -
  but the quote is pinned to the wrong block.
- Falsifier probed by this pass: `git -C ../mycelial-republic ls-files | grep -iE
  "verkle|chain|seal"` -> 4 hits, all code copies or a fixture:
  framework/mag/verkle_audit.py, framework/mag/verkle_knot.py,
  scaffolds/sovereign-toolkit/verkle_knot.py, selftest/fixtures/clue_chain_integrity.txt.
  No anchor registry, no cross-seat chain substrate in the forest's tracked FILENAMES
  (content census not run; the estate side remains .gitignore-scoped as the lens had
  it). "Shared chain has no byte" stays accurate at filename-census scope in both
  repos, with the caveat that watch/inbox/SPORE_LEDGER_CHAIN_20260901.txt and
  docs/ref/canon/canon_spore_ledger_v5_v7.txt are tracked ESTATE files using
  chain-of-spores vocabulary (see A4) - they are doctrine/transcript, not a substrate.
- The travel-kit warning verified byte-level: scripts/build_travel_kit.py line 4
  carries "+ .env" (the Tier-1 line "code + live ledgers + packs + .env"), and the
  kit's _readme() says "code, live ledgers, packs, .env". The secrets-bearing
  inverse of a spore, confirmed. (Kit zip gitignored at .gitignore:12-13; manifest
  stays tracked.)

## F5 - CONFIRMED; one OWED resolved by this pass

- 26 doctrine ribs: `grep -c '"invariant"' memory/rib_bus/doctrine.json` -> 26.
  Exact. Reconfirmed. standing-wave.json -> 87. Exact. BOTH tracked
  (git ls-files memory/rib_bus/doctrine.json confirms), so the doctrine ribs are
  already on the shareable surface.
- 10 corpus steals: `ls corpus/steal/*.md | wc -l` -> 32 on disk. Exact. No canon-10
  list found: `git ls-files docs/ref/canon` shows spore-ledger/bubbles/chord/
  world-games canon files, no steals canon. OWED STANDS.
- Season ledger: RESOLVED BY THIS PASS. Full-tree content census
  `git grep -il "season ledger" -- "*.md" "*.txt" "*.json"` -> 4 tracked files:
  RESEARCH_SUMMARY_arena_days_one_two_20261005.md (the topic's source, line 159),
  magdance_mocap_merge_20261004.md:19, mocap_pipeline_spec_20261004.md:16, and
  watch/inbox/replay_flash/MOCAP_BUILD_spec.md:247, which carries the DEFINITIVE
  mapping row: season ledger = the SessionLedger machinery in mag/gwap_payload.py.
  Byte-checked in code: mag/gwap_payload.py:679 section header "session ledger";
  :681-683 `_row_hash` over {seq, ts_utc, payload, prev_sha256}; :714
  `class SessionLedger:`; :879 per-session instantiation; docstring :29
  "session ledger -- append-only JSONL, one file per session under ...".
  The single-writer shape is byte-level: one hash chain per local session file, and
  the hashed payload has NO operator/actor field. That is the "assumes one party"
  claim, now cited. (The spec's ":681-684" line cite is ~33 lines early for the
  class itself; the section anchor is right.)
- ~5% free-lane economics: NOT re-verified by this pass (out of re-check scope).
  REMAINS OWED per the lens.

## BLIND SPOT AUDIT

1. History census not run - HONEST, stands. The --history flag exists
   (tools/secret_gate.py:119-120); neither lens nor this pass ran it.
2. lan.key rotation unverified - STANDS. state/CURRENT.md:72-73 read this session:
   line 72 `7. Rotate the LAN TLS pair, start dashboard/lan_proxy.py; tablet reaches`,
   line 73 `192.168.86.35:8765.` Still owed.
3. Working-tree receipt census - count real, LABEL imprecise: 5,061/5,062 is ALL .md
   under watch/inbox (instrument: `git ls-files "watch/inbox/*.md" | wc -l`); only
   331 tracked watch/inbox files carry "receipt" in the name
   (`git ls-files watch/inbox | grep -ci receipt`). The confession (no token scan of
   those files) stands, not run by this pass. Related surface the lens did not name:
   .gitignore:284-285 also admits ROOT-level sweep/reddit scrape exhaust "may carry
   third-party tokens" while grandfathering already-tracked ones.
4. N=4/N=8 design analysis - HONEST, stands. No second seat exists; nothing measured.
5. Forest depth - stands, partially extended by this pass (README read, docs listing,
   filename census). CONSTITUTION.md and AGENCY_SHAPE.md bodies remain unread.
6. Season-ledger/steals mapping - SUPERSEDED IN PART: season ledger now mapped (F5).
   Steals canon still open.

## ADDITIONS (what the lens missed)

A1. THE GENOME ITSELF IS NOT SHAREABLE. state/GENOME.md is gitignored
    (.gitignore:40) and untracked (`git ls-files state/` = 1 file,
    state/NIGHT_LOOP_20261005.md, force-added today in 23d76bb71). Boot order steps 1
    and 4 (GENOME, state/CURRENT.md) both reference untracked paths, and queue/todo.md
    is gitignored too (.gitignore:51). The regrow guide cannot be "read the tracked
    tree"; the exporter must deliberately carry the genome (force-add, or relocate
    the file out of state/), or the spore ships a body with no DNA.
    Falsifier: a tracked state/GENOME.md (or relocated genome path + updated boot
    order) in git cures this.
    Move: decide genome transport in the exporter design before any guide prose;
    ~20 min.

A2. SEASON LEDGER MAPPED (cures the lens's OWED): mag/gwap_payload.py:714
    SessionLedger, one file per session, hash payload without an actor field
    (:681-683), per MOCAP_BUILD_spec.md:247. Any multi-party season design starts
    from changing the hashed payload and the one-file-per-session layout.
    Falsifier: finding an earlier canonical "season ledger" file under another name
    would supersede this mapping.
    Move: cite gwap_payload.py:714 in the spore docs instead of the bare noun;
    ~10 min.

A3. configs/keys.json IS A TRACKED KEY-NAME MANIFEST the lens never saw: header
    "KEY LAW 2026-09-23: one key, one canonical name, declared once. Readers use
    mag.key_law.get(name)." Entries carry env name/provider/role/status, including
    dormant statuses ("dormant-roster-purged"). Clean of literal values at scan
    (the single 32+ char run is the role string "subscription_cli_nacho_and_sd_seats"
    at :45; zero sk-/Bearer hits; last commit 0b846c01f 2026-09-30). This is the
    tutorial's key-wiring pattern AND the dormant-until-needed mechanism the topic
    asks for - already built, already tracked.
    Falsifier: any literal credential found in configs/keys.json flips this from
    pattern to leak; rerun the scan before relying on it.
    Move: make the tutorial teach mag.key_law + configs/keys.json instead of raw
    .env editing; ~30 min.

A4. A SPORE DOCTRINE ALREADY EXISTS - vocabulary collision ahead. docs/ref/SPORES.md
    (spores-001, 2026-08-07: "Committable pointers so a new mirror-maker walks the
    same path of insight"), docs/ref/SPORE_CONTINUITY_SCHEMA.md,
    docs/ref/SPORE_SANCHO.md, docs/ref/SPORE_VNEXT_DELTA.md,
    docs/ref/spore_reading_guide.md, docs/ref/canon/canon_spore_ledger_v5_v7.txt,
    canon_tokens_as_spores_v8.txt, plus mag/spore_seed.py (spore_seed.v1,
    verkle-anchored via memory/biography/verkle_tip.json, CLI generate|verify) and
    tests/test_spore_seed.py. The lens's "missing artifact: a spore exporter" survives
    for the REPO-export sense (no tool builds a de-riddled orphan-root export), but
    "spore" is not a free word in this estate. The exporter should extend
    spore_seed.v1 anchoring and SPORES.md pointers, or the shareable docs will fork
    the estate's own vocabulary on day one.
    Falsifier: if the new export intentionally redefines "spore" and says so in
    docs/ref/SPORES.md, the collision is handled and this addition dissolves.
    Move: one paragraph in the exporter spec pinning the term to the existing
    doctrine; ~15 min.

A5. NO ROOT LICENSE IS TRACKED. `git ls-files | grep -i license` -> only
    corpus/LICENSES.md, vendored third-party LICENSEs, seed/LICENSE. `ls LICENSE*`
    at root -> absent. A public shareable with no license defaults to all-rights-
    reserved; the spore's "regrow to their liking" goal needs a license decision
    before publish, and vendored steals (corpus/steal/OnionClaw-main etc.) carry
    their own licenses that the exporter must not strip.
    Falsifier: a root LICENSE tracked in git cures this.
    Move: operator decision + LICENSE file in the export allow-list; ~10 min.

A6. THE ESTATE ACTIVELY MIRRORS THE PUSH TARGET, SHALLOWLY. refs/remotes/github/master
    was stored by `fetch github master --depth=1` at 2026-10-05 07:08:28 -0400
    (reflog) and .git/shallow exists (1 entry). Two consequences: (a) the estate
    machine already tracks the remote tip, so push-vs-remote comparisons are cheap
    and the orphan-export can diff against it; (b) any filter-repo/history-rewrite
    work must account for the shallow boundary so the rewrite does not silently
    treat the fetched tip as parentless estate history.
    Falsifier: removing the remote-tracking ref and the shallow entry makes this
    moot for future work.
    Move: note both in the exporter spec's git-handling section; ~10 min.

A7. THE SECOND REMOTE IS A SECOND LEAK SURFACE. `local` =
    C:\Users\foste\Documents\projects\Mag-backup.git, and local branch
    run-beta1-factory-audit-20260914 contains 799ddb6fe (branch --contains). The
    de-riddle plan that only repoints `github` leaves a complete radioactive copy on
    the local backup remote; the threat model must name every push target, not just
    the public one.
    Falsifier: an inventory of remotes plus their containment of 799ddb6fe showing
    zero additional copies beyond sanctioned backups.
    Move: add a remote inventory step to the export checklist; ~10 min.

A8. THE providers.yaml EXAMPLE MUST BE CUT FROM THE LIVE FILE. Live
    configs/providers.yaml = 40,724 bytes (mtime Oct 3 20:32); the only sibling .bak
    = 22,418 bytes (Aug 26, pre-deepseek-swarmcap by its own filename). Blanking the
    .bak instead of the live file would ship a two-lane-table-behind example.
    Falsifier: diffing the example against the live file showing only redacted
    values cures it.
    Move: generate the example from the live file in F2's move; ~0 extra min.

A9. THE SHAREABLE INVENTORY IS ALREADY MOSTLY TRACKED - the "what stays" list is
    cheaper than the lens implies. Tracked and clean: queue/STANDING_RAILS.md,
    memory/rib_bus/doctrine.json (26 invariants) + standing-wave.json (87),
    memory/rib/ (55 files), README.md, watch/inbox/frontier_delta_register_20261003.json.
    Untracked by construction: state/GENOME.md, state/CURRENT.md, .env,
    configs/providers.yaml, memory/runs/**, memory/seals/, memory/biography/**
    (.gitignore:18-41, 63, 102, 29). The exporter's job is the untracked exceptions
    plus history, not a wholesale selection problem.
    Falsifier: any of the "tracked" items above missing from a fresh clone would
    break this inventory; verify from a clone, not the working tree.
    Move: open the regrow guide with this tracked/untracked split; ~20 min.

## WHAT I DID NOT RUN

- tools/secret_gate.py check --history (14.37 GiB operator-scale): NOT RUN by lens
  or this pass. The live-secret count in history remains OWED.
- Token scan of the 5,062 tracked watch/inbox .md files: NOT RUN.
- Forest docs/CONSTITUTION.md and docs/AGENCY_SHAPE.md bodies: UNREAD.
- The ~5% free-lane economics receipt: NOT FOUND by the lens, NOT re-searched here.
  Still OWED.
- Lan.key rotation status: outside both passes' reach; state/CURRENT.md:72-73 still
  carries the owed item.

Banked: watch/inbox/ractor_engine/2026-10-05-spore-sharing/break-accuracy.md
(this file), moment 2026-10-05T11:59:48Z, HEAD 7dac8685e.
