# ECONOMICS - dogfood the past 48h (2026-10-02)

Lens: economics (EV per cost). Window 2026-09-30T20:00Z to 2026-10-02T11:00Z.
Prior art read FIRST and not re-derived: watch/inbox/ractor_engine/ractor-topic/SYNTHESIS.md
(its night-receipt money core, the twin double-drain, the excluded $1.0077 hour, and the
POSITION_CHANNEL neighbor-claim class are all established there). This lens swept what the
synthesis did not: the whole-ledger duplicate census across all six commits' spend, the
fix-parity of sibling organs, the dogfood-vs-built status of the window's new instruments,
and the live status of the OWED list on the current tree.

## The window's money, re-derived this sitting

Commands run (all this sitting): whole-file python scan of memory/runs/hermes_burn/usage.jsonl
(236 rows) and memory/runs/model_garden/usage.jsonl (725 rows); duplicate census keyed on
(id, turn, model); git show HEAD:githooks/pre-push and git diff githooks/pre-push;
git show --stat 3c83da5b0; grep sweeps over scripts/, tests/, tools/; ls -la of
logs/kpi.jsonl, NIGHT_CLOSE_20261002.md, census_refresh_20261002.md; sha256sum
seed/engines/key_law.py vs seed/MANIFEST.sha256; pytest tests/test_carrier_patch_t1w1.py.

- hermes_burn ledger: 236 rows, $37.7591 total, ALL rows inside the window (first
  2026-10-01T13:11:41Z, last 2026-10-01T21:53:52Z; nothing paid since).
- model_garden ledger: 725 rows, $3.4746 (22:10Z to 03:34Z), 716 ok / 9 fail, 5 dup keys
  all benign local-gemma double-runs.
- Combined $41.2337, which is the "~$42 of ~$145" claim of commit 0c9d72a06 to rounding:
  byte-consistent.
- Whole-file duplicate census: 24 dup (id,turn,model) keys, 189 rows. Giants:
  A1_steer_antiforgery turn 1 x49 on claude-opus-5.5, arc total $21.8518 = 58 pct of the
  ledger; DUEL1_hidden_5 x46 and N1_parables_songmap x42, every row ok:False at $0.0 and
  zero tokens, refusal-retry loops spanning 18:01Z to 20:17Z; B2_drift_rows_attribution x6
  IDENTICAL paid copies ($0.2466 each, prompt_tokens 23276 every row, $1.4796 = the entire
  B2 arc); the twins' 13 DUEL2_r2 keys plus N1R x2; T1W2_S5/S7 x3, S6/S8 x2.
- These match the carrier's own law block pricing (tools/hermes_burn.py:20-33): "$18.89 of
  $29.91 as pure re-fire theater", "a stale force ask burned A1 45x at $20.53 after
  landing", "N1 x42 and DUEL1_hidden_5 x46 refusal-retry loops are the disease", "DUEL2
  fired 14 paid calls whose material never reached the model". ECON.md:24-26 (model_garden
  lane 6) measured the same shape independently: "2 of 5 rows are same-id re-fires ...
  inflating spend ~40 pct".
- Bottom line: of $41.23 paid this window, roughly $21+ bought nothing that survived
  (A1 re-burn, refusal loops' wasted dispatches, twin doubles ~$1.16, evidence-less DUEL2,
  T1W2 first fires now kept as .poisoned-evidenceless). The identical real work at post-fix
  prices is about $20 per window. Runway: $47.54 live balance (0c9d72a06) means the funded
  lane survives ~1.1 more windows at the pre-fix rate, ~2.3 at the post-fix rate. The
  in-window carrier fixes are worth about $21 per window, close to half the remaining
  balance; they are the highest-EV code the window produced.

## Findings

### F1. The citation gate's enforcement is a 15-line uncommitted diff: receipts-true, HEAD-false
Commit 3c83da5b0 claims "Citation lint LANDED ... byte-checked at pre-push". The tool,
tests (+341 lines) and spec are committed (git show --stat 3c83da5b0 lists
tools/citation_lint.py, tests/test_citation_lint.py), but the HOOK WIRING is not:
`git show HEAD:githooks/pre-push | grep -c citation_lint` returns 0, while the working
tree's githooks/pre-push:24-25 carries "PUSH-GATE: citation_lint check --changed" and
`git diff githooks/pre-push` shows exactly that block as an uncommitted +15-line addition
riding the 110-file uncommitted tree. This is the synthesis's POSITION_CHANNEL class
(claim true of the working tree, false of the shipped record) found in a different commit:
the FILL-BALL receipt's enforcement claim does not survive a clean checkout.
Falsifier: a later commit (post-e3c7d341c) carries githooks/pre-push with the citation
block; `git log --oneline -- githooks/pre-push` currently tops out at f0768f3be, before it.
Move (~5 min): commit the wiring block; the next push then actually runs the gate the
receipt advertised.

### F2. The re-fire theater is patched AND test-covered, but every patch landed after the money burned and none has seen a live paid fire
The four waste classes are each named, coded, and tested in-window: LANDED BEATS FORCE,
REFUSED IS TERMINAL, EVIDENCE PREFLIGHT (tools/hermes_burn.py:20-33) plus the pidfile
guard (scripts/descent_driver.sh:10-23) and EMPTY_REASONING terminal (0c9d72a06,
imported at tools/hermes_burn.py:59). I ran the suite:
`.venv/Scripts/python.exe -m pytest tests/test_carrier_patch_t1w1.py -q` = 10 passed in
0.67s, covering force-skip, refusal terminal, and all four evidence fail-closed shapes
(tests/test_carrier_patch_t1w1.py:82-206). But the ledger's last row is 2026-10-01T21:53Z
and the fixes landed 7-11h later: zero post-fix paid dispatches exist, so production
behavior of the guards against the live Nous rail is unproven (the A1 disease itself
arose from a real API interaction the unit tests monkeypatch away).
Falsifier: a post-fix usage.jsonl row showing an ask skipped-after-landing or a REFUSED
marker minted in production; absence of such rows after the next paid window means the
guards stayed untested where the money actually burns.
Move (~15 min, $0): fire one already-landed ask dir with the force flag against the live
rail and expect the skip receipt; that single probe converts the $20.53 lesson from
unit-test-true to production-true before the next funded window.

### F3. seed_seal is built and forge-drilled but has never sealed anything; its anchor was healed by hand and can re-drift unwitnessed
mag/seed_seal.py (295 lines) and tests/test_seed_seal.py (262 lines) landed in 3c83da5b0
with the forge-drill proof, but there are ZERO .seal sidecars anywhere on the tree
(ls corpus/*.seal mag/*.seal: none) and no receipt outside the build dirs names a
production seal minted. The motivating defect is real history: the manifest row
disagreed with the sealed bytes inside one clean commit
(watch/inbox/burn_reset_20260927/flash50/w4-20.md:17). This sitting I re-measured:
sha256sum seed/engines/key_law.py = fd2a0b27... and seed/MANIFEST.sha256 now carries the
same digest, seed/ clean. So the anchor was healed, but by a hand rebuild, not by the
instrument; nothing seals the CURRENT manifest, so the next silent drift again has no
forge-proof witness, and the operator-gated enforcing flip stays a decision with no
production artifact behind it.
Falsifier: any .seal sidecar or seal receipt dated after 2026-10-01 anywhere on the tree.
Move (~20 min): mint the first production seal over seed/MANIFEST.sha256 and bank the
verification receipt; minting is not enforcement, so no operator gate is crossed.

### F4. OWED scoreboard on current bytes: 5 live, 1 paid of the six-item list (hostile-pass correction of this lens's first pass, which miscounted 4-live/2-paid)
Correction accepted and re-verified: the prior synthesis's OWED list proper
(ractor-topic/SYNTHESIS.md:124-136) carries SIX items, not the four I first counted. I
dropped the T1W2 19:17-19:18Z double-fire cause (SYNTHESIS.md:126) and wrongly counted
the census refresh as a paid OWED item (it is ranked move 4, a B2-246 patrol response,
never on the OWED list; it IS paid: watch/inbox/census_refresh_20261002.md exists, mtime
Oct 2 06:10 local, AGENTS.md bullet claims 4,147/496 with the receipt). Correct
arithmetic: 1 of 6 paid, 5 live. The paid one: the topic-undefined input defect
(.zcode/workflows/ractor-engine.dwf.ts:29-32 declares topic type string, required: true;
this run fired with the topic verbatim; REGISTRY.jsonl ractor-engine PASS
2026-10-02T10:38:16Z). The five live, each re-verified this sitting (fresh commands
below): (1) the T1W2 double-fire cause remains unattributed (grep -rln "19:17-19:18"
watch/inbox/ hits only the prior synthesis and this run's own sibling lens files, no
attribution receipt); (2) logs/kpi.jsonl is 753,467,392 bytes at Oct 2 07:22 local
(11:22Z), up from 752,885,507 at my 06:45 reading (+1.58MB in 37 min, still growing
live; writer mag/records.py:138 def write_kpi; no rotation or truncation receipt, and
the unexplained 1.1GB-to-748MB shrink delta stays unexplained); (3) the 23:32:51 EDT
invisible_runner launch is still unattributed and the append-mode audit jsonl (prior
move 6) exists nowhere (ls misses in logs/, scripts/, memory/runs/); (4) F1's pre-close
mtime leg stays WITHDRAWN, restoration needs an admin USN journal query, not run from
this seat; (5) the WMI caveat stands as an instrument note, not run since 06:11:22Z.
Separately (ranked-moves list, not the OWED list): the NIGHT_CLOSE erratum is unpaid
(grep -c -i erratum = 0; "never existed" at :40 and $8.9954 at :55 unchanged) and the
commit-queue law named OWED in 2093ca518 is ticketed nowhere (grep -c over queue/todo.md,
memory/law/registry.json, and the REAL ledger watch/inbox/hermes_burn/TICKET_LEDGER.md
all zero; citation note: the path memory/runs/hermes_burn/TICKET_LEDGER.md given in this
run's ask does not exist on disk, ls confirms; the ledger lives under watch/inbox/).
Not all five live items are writer-seated, correcting my first pass: the T1W2
attribution is a diagnosis sitting, and F1's leg needs an admin query.
Falsifier: each live item flips only on its named artifact: a rotation/truncation
receipt for kpi.jsonl naming the pre-size (a shrink WITHOUT a receipt does not pay item
2, the unexplained delta is itself the debt); an attribution receipt naming the 19:17Z
double-fire cause or the 23:32 EDT launch; an erratum block in NIGHT_CLOSE_20261002.md;
a commit-queue row in any of the three homes; a USN-journal result restoring F1's leg.
Move (~80 min for the three writer-seated: erratum, kpi rotation receipt, audit jsonl,
plus a commit-queue ticket row; then a separate ~30 min diagnosis sitting on the
usage.jsonl T1W2 row pairs, deltas 0.95s/4.7s/22s; the USN query needs an admin seat).

### F5. Guard sweep: the pidfile guard exists on 2 of 18 shell scripts and the unguarded dispatcher class persists
The guard is byte-true on scripts/descent_driver.sh:10-23 (second instance exits 3, stale
reclaim, trap cleanup), and grep finds pidfile/flock vocabulary in exactly one other
script (scripts/pull_steal_protocol_repos.sh). scripts/astra_convo_loop.sh is a
while-loop dispatcher (compose dispatch, sleep 300 / sleep 1800, lines 7-61) with ZERO
lock/pidfile/already-running hits: the twins disease in waiting, cheap-lane exposure but
the same shape. Second instance of the class inside the driver itself: the driver's OTHER
carrier tools/ds_workhorse.py (called at scripts/descent_driver.sh:38) carries none of
the three carrier laws (grep for REFUSED/landed/evidence/terminal: empty); its only
dedupe is the driver's mv of pending_items.jsonl (descent_driver.sh:41), single-writer by
convention, with retry-once as its whole storm defense (ds_workhorse.py:81).
Falsifier: a lock line in astra_convo_loop.sh, or carrier-law vocabulary in
ds_workhorse.py.
Move (~10 min): copy the 14-line pidfile block from descent_driver.sh into
astra_convo_loop.sh; a ds_workhorse parity ticket can ride the next fill-ball.

## What the window bought that survives (conversion per paid line)

| Arc (my scan totals) | Survives on tree | Verdict |
|---|---|---|
| A1 $21.8518 (52 fires) | mag/steer_seal.py 400-line verifier + tests, commit ebe4e147b | CONVERTED at ~15x necessary price ($1.32 of it legitimate) |
| T1W2 $1.1465 (x2-3 fires each) | clean refired verdicts; .poisoned-evidenceless copies kept as disease receipts | converted late, first fires wasted |
| DUEL2 $2.4329 | r2 verdicts exist; 14 evidence-less originals + twin doubles were the waste | half waste |
| DG1 $0.1107 | mating door DEAD verdict, GPU $0 | best EV line in the ledger |
| Garden $3.4746 | 9-family grid, ECON.md pricing sheet, code_swarm/rib_swarm/water_computer receipts | highest-yield paid line |
| Free lane 223.4M tok (ask-given; see blind spots) | 6 commits incl this engine | unpriceable here |

## Dogfood vs merely built (instruments of the window)

- citation_lint: built + wired (working tree only, see F1) + self-dogfooded (SYNTHESIS.md:174
  stamped its own output ok) + zero baseline rows day one (no debt accepted). Dogfooded,
  but enforcement uncommitted.
- seed_seal: built + forge-drilled, never fired in production (F3). Built.
- percolator --candidates: memory/percolator/candidates.jsonl landed with 16 real rows in
  3c83da5b0. Dogfooded.
- code_swarm, rib_swarm, water_computer: fired on real missions with dollar receipts
  ($0.22 / $0.075 / $0.0017 per 0c9d72a06's message; not each re-verified this sitting).
  Dogfooded per commit claim.
- ractor-engine: this run is the dogfood; REGISTRY.jsonl tail shows ractor-engine.dwf.ts
  gate PASS at 2026-10-02T10:38:16Z with G6 soft-fail (receipt stamp grammar), and the
  topic input defect fixed and holding.

## Blind spots (honest)

- ListWorkflowRuns is unreachable from this session (capability error, not empty project),
  so the free lane's 223.4M-token figure is taken from the ask text, not re-verified;
  memory/runs/mickey17_v2/runs/ holds no token totals I could find.
- The $47.54 Nous balance is 0c9d72a06's figure; I did not query the balance API.
- WMI and the USN journal were not re-run (transient instruments; the synthesis's 06:11:22Z
  reading stands as of its moment).
- Per-instrument garden dollar claims ($0.22 code_swarm etc.) are commit-message-cited,
  not receipt-re-verified.
- The z.ai / grok-4.7 lanes' window spend is not metered in the two ledgers scanned; this
  write-up prices only the hermes + garden rails.
- Salon-mine-20deep stopped on provider: no cost figure exists to price.

Filed by the economics lens, 2026-10-02. No em-dash bytes. All commands named above were
run this sitting except where marked not run.
