# DOGFOOD LENS: topic arrived as `undefined`, so the lens ate the estate (2026-10-06 evening)

Lens: dogfood / organ mapper. Topic arg: `undefined` (the engine passed no topic; same as the
2026-10-02 run, whose write-up is archived beside this file as dogfood_20261002_prior_run.md).
Honest reading: with no topic, the lens rides its own jacket, "the finding filed but never wired",
against the freshest 48h of estate bytes. Moment of run: 2026-10-07T00:15:41Z (2026-10-06 20:15 EDT,
`date -u` and `date`), tree shared and moving, all counts moment-stamped per B2-216. Every claim
below was checked THIS session by a named command or file read. Anything not checked is marked OWED.

Organ map: F1 context pack (AGENTS.md carrier feeds every seat boot), F2+F3 gala/dispatch
(tools/hermes_burn.py is the paid carrier both the missions and the new 24/7 clock ride),
F4 percolator/gate (workflow_gate is the gala's teeth), F5 percolator + librarian (law without
instrument; relay pages are the library rotting). MCP bridge and attention market are named in
blind spots, not findings.

## F1. The census meter fires daily; the refresh leg never closes (context pack organ). CONVERGENT.

Evidence, four independent sources:
- My run this sitting: `.venv/Scripts/python.exe -m pytest --collect-only -q -p no:cacheprovider`
  read "4701 tests collected in 20.07s" (EXIT=0) at 2026-10-06 ~20:05 EDT.
- The AGENTS.md **Tests:** bullet still claims "4,358 tests [collected] / 518 files (2026-10-04 census".
- `logs/census_patrol.log` line at [2026-10-06 08:30:02]: "COLLECT-DRIFT - pytest holds 4648 vs
  carrier claim 4358 (delta +290, bar 20)", END exit=1, "ALERT appended to memory/attention.md".
- The R5 relay audit said it first: watch/inbox/ractor_engine/2026-10-06-ouroboros-r5-relay/
  operations.md:26 "the census COLLECT-DRIFT +133 red has fired daily unactioned since 10-05".
  DAWN_REPORT_20261006.md:175 names the class "a red firing with nobody actioning it" (that line is
  about freshness, which my `tools/freshness_check.py` run shows CURED: PASS, EXIT=0, machinery
  exclusion clause live; the census twin of the same disease still fires 12h later).

Attribution (partial, honest): `git status --porcelain tests/` = 7 lines at my moment: 6 untracked
(test_freshness_machinery_exclusion, test_gap_gauges, test_publish_recheck, test_stash_sweep_watch,
test_ws_mount, test_zknot_meter_alarm) + 1 modified (test_selfplay_orchestrator.py). The bulk of
+343 items since the 10-04 carrier is committed waves per git log (D3/D8/D10/D11, NIGHT CLOSED,
selfimp imp002, dogfood-100m register lanes). Full per-file arithmetic OWED (a B2-246-grade
investigation is the operator's refresh law, not a lens sitting).

Falsifier: a fresh collect reading ~4,358, or the AGENTS.md bullet already carrying a 2026-10-06
census stamp. Move (15 min): refresh the bullet in the B2-249 grammar from a fresh collect with
the landing waves named, and make the refresh ride the dawn close (the operator's one page already
exists at 07:33; the 08:30 alert landed after it, so the day's red never reached the page).

## F2. The estate's newest receipt mis-wires its own F3: the em-dash law HAS ridden the carrier face since 10-04 (gala/dispatch organ).

watch/inbox/HERMES_247_WIRED_20261006.md:23 (19:58 tonight) claims "the law is NOT riding
_system_for(model) ... next-sitting carrier amendment: append the record-law line to the system face".
The bytes contradict it:
- tools/hermes_burn.py:171-185 `_system_for` carries the deterministic law block including :181
  "- No em-dashes anywhere. Plain hyphens only." plus trust-bytes and citation lines.
- tools/hermes_burn.py:326 builds every prompt as `_system_for(model) + "=== CONTRACT ===" ...`,
  so every ask (mission or headless) rides the law block.
- scripts/hermes_burn_247.ps1:11-12 routes the hourly fire through `.venv\Scripts\python.exe` +
  `tools\hermes_burn.py`, i.e. through that exact face.
- `git log -n 4 -- tools/hermes_burn.py` = last touch 03da1ee56 2026-10-04 11:13:01 -0400;
  `git status --porcelain tools/hermes_burn.py` = empty (clean) at my read. The law line predates
  the receipt by two days.

So the receipt's prescribed amendment is a no-op, and the honest diagnosis is enforcement, not
presence: the law is asserted in-prompt and nothing scans the banked output for violations. If a
next sitting had followed the receipt literally it would have patched theater onto bytes that
already carried the law. OWED: A2's output bytes themselves (I looked: queue/hermes_247/* holds
ask.json specs only; memory/runs/hermes_burn/usage.jsonl rows carry content_chars 7959, not text),
so the leak is receipt-claimed, not byte-verified by me.

Falsifier: a commit predating 10-04 introducing :181, or a dirty tree at receipt time, or an A2
output file found clean of em-dashes. Move (30 min): add the deterministic output check to the
carrier bank path (em-dash + law-violation scan on banked content, the substance-gate class of
commit 28e7bddbf) instead of a second law line.

## F3. The 24/7 clock's premium rung: single-key carrier, first production fire burned its alert on it (driving ladder / dispatch organ).

- tools/hermes_burn.py:83-93 `_hermes_key` returns the FIRST key found in .env (loop + return);
  no per-call sibling retry exists. The receipt files this exact gap (HERMES_247_WIRED:21, F1)
  and leaves it unfixed: "no per-call retry on the sibling account".
- logs/hermes_burn_247.log [2026-10-06T23:54:15Z]: FAIL A1 "HTTP 402: 'Payment Required'",
  "HERMES-BURN: FAIL - 2/3 asks", exit 1. memory/attention.md tail row 2026-10-06T23:55:27Z
  MagHermesBurn247 exit 1. The clock's first red in production is the known-broken premium rung,
  and A1 will 402 hourly until REFUSED mints (receipt's own self-heal note).
- The log also confirms receipt F4 live: the FAIL line renders as spaced UTF-16LE chars.

Falsifier: a per-ask 402 retry in the carrier, or A1 passing on the next hourly fire. Move
(45 min): per-ask cross-key failover in run_ask (one sibling-key retry on 402) or route premium
SKUs to KEY_1 per the receipt's amendment clause; then `schtasks //Run //TN MagHermesBurn247`
to prove A1 green.

## F4. Stop-cert armed, zero teeth in production (percolator/gate organ).

- Code exists: tools/workflow_gate.py:128 `STOPCERT_STATUSES = ("retired", "superseded")`,
  :419 `load_stopcert_index`, :448 `stop_cert_reason`, blocked checks mint "BLOCKED-STOPCERT" exit 2.
- Load does not: `grep -c '"status": "retired"' memory/workflows/REGISTRY.jsonl` = 0;
  same for "superseded" = 0. The REGISTRY tail's STATUS-ROW probe rows read "status": "unknown".
- state/CURRENT.md:47-49 files it as Owed: "stop-cert armed but UNLOADED (zero registry status
  rows minted)"; the four retirement candidates (the-50, tree-doctrine-dig, music-cut, game-dig
  twins) sit operator-gated per the NIGHT_LOOP fleet-retirement row. The cert has only ever bitten
  fixtures; zero real submits have passed it.

Falsifier: any retired/superseded row in REGISTRY.jsonl, or a BLOCKED-STOPCERT verdict from a
non-fixture gate run. Move (10 min operator pen + 5 min fire): sign the four fleet verdicts, mint
the status rows, run one real `workflow_gate.py check --script` on a named-retired script to see
the cert block outside the scenario suite (which my run tonight shows 9/9 green, exit 0).

## F5. The publish-time re-derivation law has no instrument, and the disease recurred within hours (percolator + librarian organ).

- Law filed: state/CURRENT.md:55-56 "publish-time re-derivation law (R5 communication lens):
  every fold deliverable re-derives its own citations before publishing".
- No instrument: my `grep -rn "re-deriv|rederiv" mag/ tools/ --include=*.py` returned only
  unrelated comments (mag/agent_cli.py:2602, mag/aos_agent.py:7, mag/arrival.py:85,
  mag/bay_organs.py:30); `grep -rn citation_lint tools/fold_gate.py tools/workflow_gate.py
  mag/governor_autorun.py` = zero hits (citation_lint rides pre-push only, per githooks).
- Recurrence: DAWN_REPORT_20261006.md:197-199 records a fresh rot same day: "the citation
  memories/session/next-window-handoff.md:69 above rotted when the economics append landed above
  it: the XAI 403 anchor now sits at line 80". The founding incident (R5's six blocking citation
  defects in the relay's own pages, commit ba03060bb) was the reason the law was filed.

Falsifier: a fold-close or publish step that invokes citation_lint (or any line-anchor re-check)
on deliverables. Move (30-45 min): wire citation_lint into the lens banking step / fold_gate
release so ractor_engine deliverables re-derive citations at publish time, not at pre-push.

## Method note

Checks run this sitting (all EXIT observed): pytest collect-only (4701, 20.07s), freshness_check
(PASS 0), corpus_fts_rebuild --check --deep (fresh, 0), workflow_gate --scenarios (9/9, 0),
greps named inline, git log/status reads, log tails. The FTS wire is the healthy contrast: the
09:00 daily task detected stale, rebuilt through the sanctioned writer, and my independent
--check --deep read fresh. That is what a fully closed wire looks like; F1 and F5 are its
unhealed siblings. No subprocess-spawn of mine exercised the win32 CREATE_NO_WINDOW law.

## Blind spots (honest)

- A2's output text unverified (OWED above); the em-dash leak rests on the receipt's claim.
- I ran collection, not execution: the +343 items' pass/fail health is unmeasured this sitting.
- My own spawning engine's script (.zcode/workflows/ractor-engine.dwf.ts, gitignored) unread;
  my harness view is indirect (its REGISTRY row 2026-10-06T22:29:05Z digest d8d63f619ab9 reads PASS).
- Unopened organs: mag/llama_cpp_bridge.py (modified in git status), tools/query_broker.py
  (librarian lattice), configs/lanes.yaml (gala lanes), dashboard server pointer door (the R5
  caveat numbers at DAWN_REPORT:179-184 are unverified by me).
- The $94.64 hermes ledger is spend-side only (receipt's own caveat); API-side meter unread.
