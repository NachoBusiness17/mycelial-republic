# THE SPORE SHARING PROBLEM - ECONOMICS LENS (2026-10-05)

Lens: EV-per-cost pricer. Verdict up front: **the spore cannot be a push and
must not be a filter**. The shareable estate is a fresh allowlist tree of a
few hundred files priced in megabytes, guarded by a scanner the estate
already owns, with one identity field added at the two write surfaces. The
shared-chain and the history-rewrite are both cluster-class asks dressed as
one sittings; both die on this lens.

All commands below were run in this sitting on the working tree at
C:/Users/foste/Documents/projects/local_sovereign_agent.

## 0. THE PRICING TABLE (measured this sitting)

| surface | measure | instrument |
|---|---|---|
| git pack size | 14.37 GiB | `git count-objects -vH` (size-pack; also 4 tmp_pack_* garbage = failed-push debris) |
| tracked files | 56,359 total, 43,818 under memory/ + watch/ | `git ls-files \| wc -l` + grep -c |
| blobs > 100MB in HEAD | 19 | `git ls-tree -r -l HEAD \| awk '$4 > 104857600' \| wc -l` |
| largest blob | 2,406.1 MB ESTATE_INDEX.jsonl, tracked at TWO paths (watch/ESTATE_INDEX/ + dashboard/data/, same blob cb1361095) | `git ls-tree -r -l HEAD \| sort -k4 -rn` |
| github remote age | last push dc6649943 2026-08-20 (46 days stale); `main` tip 5d20144e1 2026-08-04; the living line is the mag/* branch | `git log -1 --format=... github/master` |
| .env in history | 0 commits in --all | `git log --all --oneline -- .env \| wc -l` |
| full-tree secret scan | 42 critical, 15,610 high, 3,606 blocking; ANTHROPIC-KEY x420, XAI-KEY x27, DEEPSEEK-KEY x19, GITHUB-TOKEN 1, STRIPE-KEY 14; runtime 49,256s over 30.8 GiB / 2.36M files | watch/inbox/secret_gate_results/full_run_row.json (2026-09-27T18:37:19Z) |
| descent lifetime spend | 3,010 rows, $94.61; opus-5.5 $59.83/1247 rows = $0.048/ask; haiku-4.5 $2.63/664 = $0.004/ask | memory/runs/hermes_burn/usage.jsonl (computed this sitting) |
| deepseek design batch | 27 rows, $0.0724 = $0.0027/ask = **5.6% of an opus ask** | memory/runs/ds_batches/delta_judge_results_v3.jsonl (computed this sitting) |

## 1. Q1: THE DE-RIDDLED SHAREABLE VERSION (what strips, what stays, what sleeps)

**Strips:** .env (never committed, verified above; .gitignore:272 `*.env`
holds, confirmed by `git check-ignore -v .env`), session history and
personal receipts (watch/ + memory/ = 43,818 of 56,359 tracked files: do NOT
copy), the big blobs (19 over 100MB), the corpus steals (536 tracked files
that carry OTHER PEOPLE'S credential-shaped strings: the gate's blocking
sample names boe003.html:257 STRIPE pk_live, cdx_rar.json:616 GOOGLE-OAUTH
and cdx_rar.json is TRACKED, verified by `git ls-files --error-unmatch
cdx_rar.json`), and the 23 tracked .mimosa files incl. hook-state session
files (the CONNSTRING-CRED class in the gate's blocking sample; `git ls-files
| grep -c mimosa` = 23).

**Stays:** state/GENOME.md (the inheritable artifact, laws first,
boot order at section 3), queue/STANDING_RAILS.md (the rails law + drop-in
table + registered debts), the doctrine ribs (memory/rib_bus/doctrine.json +
standing-wave.json, mounted by mag.rib_bus.mount, injected by
rib_bus.inject_for per state/GENOME.md:11-14), the organs as CODE:
mag/route_chat.py, mag/rib_bus.py, mag/free_tier.py, tools/gps_mcp/,
tools/ds_workhorse.py, tools/arena_gwap.py, tools/secret_gate.py,
configs/providers.yaml (lanes + dormant flags), .env.example (decoded this
sitting: all key values EMPTY, the template is clean), the parable
(corpus/canon/THE_PARABLE_OF_THE_FIELD_AND_THE_STONES.md, named at
state/GENOME.md:61), and the tests for whatever modules ship.

**Sleeps until needed:** every lane with `dormant: true` in
configs/providers.yaml (saelis verified dormant at providers.yaml "dormant:
true   # never called"), z_ai3 (dormant since LITE_LANE_PULL per
state/CURRENT.md:36-38), the arena cron (per-seat schtasks, not portable),
the GPS ledger as DATA (ship the code, not the 782,336-byte
tools/gps_mcp/gps_ledger.db3, which is TRACKED today, verified
`git ls-files --error-unmatch`; a second operator must grow their own
capability rows or they are routing on operator A's key history).

**Move (one sitting):** `tools/spore_export.py`: an explicit allowlist copy
into a fresh orphan branch. Copy, never filter: a filter-rewrite of a
14.37 GiB pack is hours of risk on the chain; an orphan allowlist is one
script and minutes.

## 2. Q2: WHAT BREAKS AT N=2, WHAT BREAKS AT N=8

N=2 breaks at the WRITE surfaces, all verified single-party:

- **The door reads one .env:** mag/route_chat.py:67 `(ROOT / ".env")`
  hardcoded, plus os.environ fallback at :64. Two operators on one checkout
  share one keychain; two operators on two clones cannot merge .env at all
  (it is gitignored, correctly).
- **Every bank is one append file:** mag/route_chat.py:46 `USAGE = ROOT /
  "memory" / "runs" / "route_chat" / "usage.jsonl"`. Rows carry ts/lane/model
  but NO operator field (row 1 read this sitting: `{"ts": "2026-10-03T16:44:46Z",
  "lane": "deepseek", ... "ok": false}` - no cost, no owner). At N=2 a pull
  merge of two appended jsonl files is last-writer-wins on content lines.
- **The GPS capability ledger is a TRACKED sqlite:** tools/gps_mcp/
  gps_ledger.db3 in git (verified). Tracked binary + two writers = guaranteed
  merge conflict; and the rows measure operator A's keys: D7 metabolism
  slashed a 10-fail haiku streak to 0.030 (watch/inbox/
  D7_PHEROMONE_METABOLISM_20261005.md) - operator B routing on that row is
  routing on A's burned quota, a category error, not a stale read.
- **The rib bus has no claim system:** `grep -n "claim\|lock\|owner\|writer"
  mag/rib_bus.py` returns only prose at :4 and :195; publish/mount/inject
  carry no ownership field. Two seats folding doctrine ribs to the same
  memory/rib_bus/*.json is silent overwrite.

N=8 breaks at TRUST, not transport: whose receipt is law? The rails law
"if it ran, it banks" (queue/STANDING_RAILS.md:30-31) is unscoped - at N=8
the bank has no identity, so a foreign seat can bank capability rows that
route real dollars (the rails oroboros: "capability rows route the next
ask's dollars", queue/STANDING_RAILS.md:52-53). The fix is one field, not a
system: `operator_id` (env MAG_OPERATOR_ID, default nacho) stamped at the
route_chat bank row and the gwap payload. Cost ~25 minutes. The claim-system
alternative (locks, leases, merge machinery) is strictly dominated per
EV/cost: receipts are append-only identity carriers already.

## 3. Q3: THE TUTORIAL LADDER, PRICED

The ask's "~5% of paid" survives measurement on the estate's own ledgers:
$0.0027/ask deepseek design batch vs $0.048/ask opus = 5.6% (instruments in
section 0). Haiku judgment at $0.004/ask is 8.3%. The tutorial
(docs/ref/SPORE_BOOT_TUTORIAL.md, one sitting) should be priced FROM these
ledgers so the new operator audits their own ladder, and it must carry the
failover scars already paid for: flash_call 429 -> openrouter overflow
(state/CURRENT.md:32-33), z_ai3 dormancy (state/CURRENT.md:36-38), the
B2-36 cerebras card-gate (configs/providers.yaml comment block), and the
descent protocol's cheap-first + prior-art-sweep legs (RIB
memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md, cited in AGENTS.md).

**Gap the tutorial must name honestly:** the front door under-banks.
route_chat usage rows carry no cost_usd (row 1 verified), while
hermes_burn rows do. A new operator following the rails law cannot audit
their own ladder from the primary surface. Patch the bank row when the
provider returns usage: ~20 minutes, rides with the operator_id patch.

## 4. Q4: THE REGROW GUIDE

Exists in seed form: state/GENOME.md section 3 boot order (genome ->
STANDING_RAILS -> ribs -> CURRENT -> Delta Register -> act). The regrow
guide extends it with the dormancy map (section 1 above), the per-seat
declarations (own .env, own memory/runs/, own gps_ledger.db3, own schtasks
for the arena/tavern crons), and the first-bank instruction: fire one
route_chat smoke and one ds batch so the operator's own usage ledger exists
before any judgment spend. One sitting, lands as docs/ref/REGROW.md
referenced from the spore README.

## 5. Q5: WHAT THE MYCELIAL REPUBLIC IS

Priced from this repo's bytes: today it is ONE organism with a 46-day-stale
GitHub mirror (github/master @ 2026-08-20, verified). The only shape that
scales in N without building a claim system is **forked estates that trade
receipts**: each estate keeps its own chain, its own ledger, its own keys;
the cross-estate currency is the receipt, which the estate already
chain-verifies for gwap payloads (queue/STANDING_RAILS.md:44 "chain-verified
capability row -> GPS"). The inter-estate wire is NAMED but NOT BUILT:
queue/STANDING_RAILS.md:46 "gap-register rows | PARTYCHAT threads (when the
wire plan lands)". The receipt contract to make trade real is three fields
(operator_id, estate_id, chain anchor hash) stamped at the two bank
surfaces. Shared chain: needs claims + locks + sqlite merge + a trust
model; dominated. This is the genome amendment to write.

## 6. FINDINGS (lens-ranked)

1. **The push is currently impossible and the repo-as-spore is the wrong
   object.** 19 blobs over GitHub's hard 100MB cap in HEAD, largest 2.4GB;
   14.37 GiB pack. Falsifier: a measured successful push of HEAD to the
   github remote, or an LFS migration completing inside one sitting. Move:
   tools/spore_export.py orphan-allowlist copy (~30 min).
2. **The danger is not .env, it is the tracked corpus.** .env has zero
   commits in --all; cdx_rar.json (tracked) carries a high OAuth finding and
   23 .mimosa files are tracked. Falsifier: a fresh tools/secret_gate.py run
   over the exported spore tree returning zero blocking findings. Move:
   git rm --cached cdx_rar.json + mimosa paths, gate the export pre-push
   (~40 min).
3. **N=2 breaks at write surfaces; the cure is an identity field, not a
   claim system.** route_chat.py:67 + :46, tracked gps_ledger.db3, rib bus
   without owner fields. Falsifier: two-clone append test producing a
   reconciled bank without operator_id. Move: operator_id at the banks
   (~25 min).
4. **The ladder is real at 5.6% of paid and the front door cannot prove
   it.** ds $0.0027/ask vs opus $0.048/ask measured; route_chat rows carry
   no cost. Falsifier: the new operator's own ledgers three months in not
   showing ~5-10% ratios. Move: SPORE_BOOT_TUTORIAL.md priced from ledgers +
   cost_usd bank patch (~45 min).
5. **The republic is a federation of forks trading receipts; the missing
   organ is three fields.** STANDING_RAILS.md:46 names the wire as not
   built; genome section 4 selection is single-seat. Falsifier: a shared-
   chain week with two estates and zero conflict, or a foreign receipt
   failing import verification. Move: receipt contract amendment to GENOME
   (one sitting).

## 7. BLIND SPOTS / OWED (law: never fabricate)

- OWED: the live state of github.com/NachoBusiness17/mycelial-republic
  (public? empty? holding the 2026-08-20 master?) - only the local ref was
  read; needs network + auth.
- OWED: "the season ledger" as a standalone organ was NOT found. Closest
  artifacts: watch/inbox/THE_FIRST_SEASON_story_20261003.md (the day-one
  story) and the gwap ledger (266 rows per state/GENOME.md:29). If a
  distinct season ledger exists, the "what stays" inventory is incomplete.
- OWED: docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md and the sibling
  mycelial-republic tree were not read; the Q5 answer is priced from this
  repo only.
- Scope note: the 42-critical/15,610-high gate figures are the estate's own
  2026-09-27 full-tree instrument (13.7h runtime), not a rerun this sitting;
  the 2026-10-05 changed-mode gate rows (watch/inbox/secret_gate_results/
  changed_20261005T080433Z.json) show only entropy self-hits inside the
  gate's own result files.
- The arena cron registration was not enumerated on schtasks (one query
  attempt, nothing greppable returned); "per-seat, ships dormant" is
  inference from STANDING_RAILS.md:43, not a verified task list.
