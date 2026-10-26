# LOGIC LENS - THE SPORE SHARING PROBLEM (2026-10-05)

Lens: instrument theorist. Job: extract the inference rules the estate actually
runs and name where instruments are redundant, contradictory, or blind. The
jacket pattern (two instruments disagreeing with no adjudicator) appears THREE
independent times in this topic; that recurrence is the finding.

## What I personally read and ran this sitting

- state/CURRENT.md, state/GENOME.md, queue/STANDING_RAILS.md (all read whole)
- mag/route_chat.py (335 lines, whole), mag/rib_bus.py (274, whole)
- tools/gps_mcp/ledger.py (schema block lines 100-170), tools/gps_mcp/router.py (lines 30-60)
- watch/inbox/NACHOQUIXOTIC_MINE_20261004.md, NIGHT_SHIFT_20261005_CLOSE.md,
  SHARED_SURFACE_CONTRACT.json (read whole)
- docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md (lines 1-60), configs/providers.yaml (lane grep)
- .gitignore (whole), tools/precommit_secret_check.py (docstring + head)
- Commands run: git remote -v; git branch -r; git log -1 on github/master,
  main, HEAD; git rev-list --count for main..github/master (=1),
  github/master..main (=5), main..HEAD (=873), github/master..HEAD (=878);
  git ls-files per boot file (state/GENOME.md = 0 tracked, state/CURRENT.md = 0,
  watch/inbox/INDEX.json = 0; queue/STANDING_RAILS.md, memory/rib_bus/doctrine.json,
  tools/gps_mcp/gps_ledger.db3 = 1 each); git ls-tree --name-only github/master
  (tree is a src/ + framework/ + mycelia.cmd layout that no longer exists locally);
  git rev-list github/master --objects | grep -icE "\.key$|\.env$|secret" = 0;
  git ls-files | sed top-dir census (memory 26,749 tracked, watch 20,359 tracked);
  .venv python count of memory/rib_bus/doctrine.json ribs = 26 (matches the ask's
  "26 doctrine ribs") and standing-wave.json = 87; wc -l arena ledgers
  (arena-sessions.jsonl 60 rows, arena-capability.jsonl 730 rows).
- NOT RUN (OWED): no concurrency test executed; no fresh-clone boot attempted;
  no network probe of the remote (AGENTS.md 302-SSO caution); gps_ledger.db3
  contents not inspected (schema read from code only); the 87 standing-wave ribs
  not content-censused for personal data.

## FINDING 1 - The spore cannot regrow from its own clone (genome vs gitignore, no adjudicator)

GENOME.md section 3 (state/GENOME.md:69-75) fixes the boot order: 1. this file,
2. rails, 3. ribs, 4. state/CURRENT.md, 5. the delta register. But git tracks
ZERO of state/: .gitignore carries "state/ state/**/*" with only .gitkeep
excepted, and `git ls-files state/GENOME.md state/CURRENT.md` returns empty. The
inheritable artifact lives in the one directory the transport refuses to carry.
Meanwhile the same .gitignore does track the measured organ
(tools/gps_mcp/gps_ledger.db3 = tracked) and both rib stores (doctrine.json 26
ribs, standing-wave.json 87 ribs). The de-facto export manifest is the
.gitignore itself, grown line-by-line by incidents (each ignore line cites its
audit: 2026-08-20 tracked-fix for providers.yaml, 2026-09-30 finding #1 for
trajectory, 2026-10-03 lan.key note "rotate - it remains in history"). No
instrument adjudicates "what is the shareable cut": the genome's law "append-only,
nothing forgotten" (state/GENOME.md:82) and the secret-hygiene law (history
rewrite mandatory) cannot both hold on one artifact, and nothing decides between
them. Falsifier: execute GENOME section 3 verbatim in a fresh clone of any
branch; step 1 fails on a missing file, proving the regrow dead on arrival.
Move (one sitting, ~45 min): add a tracked state/GENOME.share.md (or move the
genome to a tracked path) and write tools/spore_manifest.py that emits the share
set + sha256s with the census-patrol fail-closed contract (0 clean, 1 leak, 2
cannot-verify).

## FINDING 2 - The sharing instrument already fired once and rotted; N=2 already happened inside one seat

The remote named `github` IS github.com/NachoBusiness17/mycelial-republic.git
(git remote -v). github/master tips at dc6649943, 2026-08-20, and its tree
(src/, framework/, mycelia.cmd, scrum/) is a layout that no longer exists in
this working tree; local main is 5d20144e1, 2026-08-04, while the live branch
HEAD 9d3b4b572 (2026-10-05) is 873 commits ahead of main and 878 ahead of the
remote, across 38 local branches. The pushed history carries zero .key/.env/
secret blobs (rev-list --objects grep = 0), so push #1 was clean - but the
gitignore's lan.key note says the key "remains in history" locally, so push #2
of the same branch CANNOT be clean without a rewrite or an orphan cut. The
sharpest inference: the estate's real merge surface for daily work is not git
at all, it is the receipt surface (watch/inbox, 20,359 tracked files; the
48h window alone holds 96 receipts) plus the verkle chain. Git is the fossil
layer. Falsifier: if git were the living chain, a 873-commit run-branch would
have folded to main inside 2 months; it did not. Move (one sitting): register
the truth in queue/STANDING_RAILS.md (inbox receipts + verkle = the chain, git
= periodic code snapshots), then cut `republic` from HEAD with the spore
manifest applied as the first orphan commit.

## FINDING 3 - At N=2 the rib bus silently loses ribs and the GPS prior conflates seats (two more adjudicator gaps)

mag/rib_bus.py publish_rib is an unlocked read-modify-write full-file rewrite:
load store (line 156), mutate dict (163-165), save via plain write_text
(78-82). No lock, no compare-and-swap, no operator identity; the estate even
HAS a lock pattern in-repo (store_io.py exclusive(), cited by the .gitignore
"*.lock ... never commit" line) and rib_bus does not use it. Two concurrent
publishes on one domain = last-writer-wins, the loser's rib vanishes with exit
0. The GPS ledger's capability table keys on PRIMARY KEY (model_id, task_shape)
(tools/gps_mcp/ledger.py SCHEMA_SQL) - no operator/seat column anywhere in the
schema, and the router (router.py:44 MOMENTUM_RANK over ledger rows) reads the
same shared prior. Second disagreement inside the same organ: the router still
reads stored pass_rate while D7 metabolism computes the effective rate, and the
night close (watch/inbox/NIGHT_SHIFT_20261005_CLOSE.md, decisions 2-3) shows the
wiring was deliberately left undone pending the operator epoch-stamp call -
two rate instruments, no adjudicator, on purpose, logged. Falsifier: a
two-process concurrent publish_rib test on domain "general" loses one rib
deterministically at high frequency; a second operator's 10-fail streak slashes
the first operator's routing rate via the same 0.85^streak curve. Move (~30
min): wrap _save_store in the existing store_io exclusive() lock; spec the
seat_id column as an amendment, operator-gated on the production db3.

## FINDING 4 - Dormancy is already the shareable-subsystem mechanism, but the lane map itself is untracked, so a fresh clone has zero lanes

The ask's "subsystems dormant until needed" is not a new mechanism: the B2-133
dormant gate refuses any dormant lane without operator_go (mag/route_chat.py
241-243), and providers.yaml treats dormant as a declared state, not a failure
(configs/providers.yaml:62-64 saelis comment). The tutorial ladder maps 1:1
onto existing lanes: deepseek (line 359, DEEPSEEK_API_KEY + DEEPSEEK_SWARM_API_KEY
failover), openrouter (line 170, FOUR key envs: OPENROUTER_API_KEY,
OPENROUTER_API_KEY_2, OR_API_KEY, OR_API_KEY_2), groq (line 298), gemini (451),
nous/Hermes (150-158). But configs/providers.yaml is untracked (`git ls-files`
= 0, ignored since the 2026-08-20 tracked-fix), so a fresh clone's front door
has an empty lane map: _load_lanes returns {} and every call dies "unknown lane"
(route_chat.py:238-240) before any key is consulted. The tutorial (ask Q3) and
the regrow guide (Q4) are both blocked by one missing tracked artifact.
Falsifier: fresh clone + route_chat("ack", lane="deepseek") raises "unknown
lane" with no key ever read. Move (one sitting): track
configs/providers.yaml.example - every remote lane present with dormant: true
default, key fields as env NAMES only - and it unblocks tutorial, regrow, and
the dormant-gate demo in one file.

## FINDING 5 - What the republic is, byte-level: one estate with a 47-day-stale fork door, not a shared chain and not yet forked estates trading

The compass declares three houses: Beads (this repo, private office), Forest
(mycelial-republic, "Public law, fork"), GSTD (docs/ref/
MAG_MYCELIAL_REPUBLIC_COMPASS.md house table), and the sovereignty pillar
promises "You can fork the repo and run :8765 without our permission". But the
git instrument contradicts the house split: beads' own remote named `github`
points at the republic URL - one repo wearing two declared identities. The
receipt-trade primitive already exists and is identity-free by design: the GPS
evidence gate retains evidence bytes (cap 64KB, ledger.py MAX_EVIDENCE_BYTES),
re-hashes them against claims, and issues trivalent verdicts RESOLVED /
MISMATCH / UNVERIFIED - so a forked estate COULD push verdict rows with valid
hashes today and they would be accepted. What does not exist is the who-measured
layer: no seat_id, no operator provenance, and the only multi-writer adjudicator
in the estate (SHARED_SURFACE_CONTRACT.json: read-first INDEX, classify
FACT/INFERENCE/PROPOSAL/UNPROVEN/RECEIPT, receipt-before-promotion) is scoped to
one physical directory on one host (all client_aliases resolve to
C:/Users/foste paths). Falsifier: a second clone appending hash-valid verdict
rows to gps_ledger.db3 is accepted with zero identity checks - demonstrating the
trade channel exists while the identity layer does not. Move (one sitting): add
seat_id to the route_chat bank row (the row already carries key_env at
route_chat.py:303, so the field slot exists), then write the two-line law into
STANDING_RAILS: receipts trade by evidence hash, provenance by seat_id.

## PATTERN STATEMENT (the jacket, three times over)

1. GENOME inheritance law vs .gitignore secret law - no export adjudicator.
2. router stored-rate vs metabolism effective-rate - wiring deliberately
   unadjudicated pending an operator call (documented, at least).
3. Beads-vs-Forest house doctrine vs the single remote wearing both names -
   no naming adjudicator between the compass instrument and the git instrument.

The estate's 0/1/2 exit-contract discipline (precommit_secret_check 0/1/2,
census patrol fail-closed, gate exit-2 blocks) is the house style for
adjudicators; the spore problem is precisely the set of surfaces that never got
one. The single sitting that cures the most is the spore manifest instrument
(Finding 1's move), because it forces every other cut decision (what ships,
what sleeps, what trades) to be named row by row instead of inherited from an
incident-grown ignore file.

## Blind spots of this lens

- No code executed against the verkle chain (verkle_knot/verkle_bus read only
  through rib_bus's usage and commit messages); chain-sharing claims are
  second-hand.
- The two-process rib race is argued from code, not measured.
- The remote's public reachability and its Aug-20 content were inspected
  through local git objects only; no fetch was made.
- The tracked gps_ledger.db3's actual rows were not opened; personal data
  inside it is OWED, not asserted either way.
- Tutorial economics (the ~5%-of-paid claim) unpriced; no usage ledger math
  was run for the DeepSeek/OpenRouter/free-lane ladder.
- 87 standing-wave ribs not content-censused for personal receipts; only the
  count was verified.
