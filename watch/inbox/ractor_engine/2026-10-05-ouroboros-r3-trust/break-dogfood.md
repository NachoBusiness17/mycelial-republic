# break-dogfood: hostile second pass on the dogfood lens (ouroboros R3, trust instruments)

Date: 2026-10-05. Seat: break-dogfood (this sitting). Tree: ebcd2583d + live working tree.
Method: byte-check every evidence cite, re-run the probes, attack the falsifiers, adjudicate the
drift channel the ask named unadjudicated. Every check below was RUN this sitting unless marked
OWED. No em-dashes. Python: ./.venv/Scripts/python.exe from repo root.

## Verdicts on the lens's four findings

### F1 G8 envelope-receipt exception is path-exists -> CONFIRMED (and it generalizes to the whole gate)

- Bytes: tools/workflow_gate.py:189-193. `os.path.isfile(path)` plus a `"watch/inbox" in path`
  substring test. No read of the named file, no width figure required.
- Probes run (gate invoked as `workflow_gate.py check --script <fixture> --no-register` on
  fixtures in C:/Users/foste/AppData/Local/Temp/breakdogfood/):
  - w50_nostamp (literal `max_concurrency: 50`, no stamp): G8 FAIL, exit 2.
  - w50_indexstamp (width 50 + `envelope-receipt: watch/inbox/INDEX.json`): G8 **ok**. INDEX.json
    exists (929,700 bytes, ls this sitting) and is a directory index carrying no width
    measurement. The lens's fixture result reproduces.
  - w50_missingstamp (stamp names watch/inbox/NO_SUCH_RECEIPT_20269999.md): G8 FAIL.
  - w50_variable (`max_concurrency: args.width`): G8 **ok**. Non-literal width = no width seen;
    `max_declared_width` (workflow_gate.py:288-291) returns None, so the FIRE_LEDGER row would
    record max_concurrency null. CONVERGENT with operations.md row 1 (same probe, their fixture).
  - comment_only (a file that is 100 percent comment lines, zero executable code, carrying all
    gate phrases in comments plus width 50 + the INDEX.json stamp): **workflow_gate PASS, exit 0,
    all eight checks ok**. The G8 lesson is not a G8 bug, it is the gate's architecture: every
    check is a regex over raw text including comments. CONVERGENT x3 (operations.md row 1,
    accuracy.md row 3, this probe).
- Wild census (the lens's unrun probe 5, now run): grep over .zcode/workflows/*.ts (20 files,
  non-recursive) shows every max_concurrency declaration in the live fleet is a COMMENT stamp
  ("declaration stamp, the firer still sets it at run time", .zcode/workflows/mickey17-burn.dwf.ts:48;
  .zcode/workflows/the-gala.dwf.ts:11 "Width rides max_concurrency on the run, NOT in asks").
  Declared widths: 3 (17 files) and 10 (3 files: fill-ball, gap-analysis, the-50, each stamping
  the real receipt watch/inbox/ENVELOPE_50W_HIT_20260926.md). Zero vacuous INDEX-style stamps in
  the wild today: the falsifier's census condition holds, the blindness is armed but unused.
  Structural point beyond the lens: the fired width is set at CreateWorkflow time outside the
  script, so even a byte-checked stamp binds a declaration the fleet's own convention makes
  non-binding. The FIRE_LEDGER (workflow_gate.py:495-505) joins the COMMENT value to script
  identity; it cannot see the fired shape. CONVERGENT with economics.md row 1 (same observation,
  independently derived there).
- Convergence claim check: operations.md:15 (row 1) and accuracy.md:26 (row 3) both carry the
  finding with their own fixtures; the sibling probe
  watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/probes/g8_vacuous_envelope.dwf.ts
  exists. CONVERGENT x3 verified, not just asserted.

### F2 fold loses tier-2 verdicts silently -> CONFIRMED (four distinct silent shapes)

- Bytes: tools/mickey17_v2_fold.py:330-337 (verdict compare is `.strip()` then exact
  `== "unconfirmed"` / `== "crashed"`, no casefold), :339-342 (`deep_keys` reconstructs
  `<laneId>: <first six claim words>`), :347-358 (default branch is `included += 1`).
  Producer side: .zcode/workflows/mickey17-burn.dwf.ts:352 asks the LLM to echo the minted
  row_key back; :454 writes crash fallback row_key `x.lane + ": crashed"`, a key no six-word
  claim key can ever equal, so crash rows can only join via a top-level `unconfirmed` list whose
  entries the fold reads with `x.get("claim", "")` (fold:326) - a field DeepCheck rows do not
  carry. The enum itself has a 4th value "same-chain-verified"
  (.zcode/workflows/mickey17-v2.dwf.ts:59) and the runner counts any string outside
  verified/same-chain-verified as unconfirmed (:376): producer and consumer disagree on the
  vocabulary today, benign only because the live archive happens to hold exactly
  {verified: 46, unconfirmed: 6} (accuracy.md row 5 census; not re-run here).
- Probe run (RUN_ROOT/LANES_DIR monkeypatched to a temp dir, 4 lane rows, 4 deep_tier2 entries):
  - exact six-word key + "unconfirmed" -> excluded 1, included 3. The mechanism works when
    shapes align.
  - seven-word key + "unconfirmed" -> silently included.
  - exact key + "Unconfirmed" (capital U) -> silently included.
  - exact key + "partially confirmed" (out of vocab) -> silently included.
  - PRISMA printed "HOLDS (4 = 3 + 1)" in all cases; no warning path exists anywhere in the
    module (whole file read; there is no unmatched-key telemetry).
- NEW silent shape (found by accident, my first fixture double-wrapped the lane id): a
  checks.json whose top level is not the flat runner shape yields "verdicts: none listed",
  zero exclusions, every row included, invariant HOLDS, no warning. The de-blinded walk is
  shape-coupled with no schema check: rename the key or nest the payload and all verdicts
  vanish. This is the same defect class the de-blinding itself fixed (ancestor fold read a list
  no runner writes).
- Convergence claim check: operations.md:17 (row 3) and accuracy.md:30 (row 5) carry it with
  their own probes. CONVERGENT x3 verified.

### F3 golden vector docstring attack -> WEAKENED (mechanism real, the stated attack is false, the real attack is different)

- Confirmed core: check_text is substring-in-raw-text (tools/prepush_golden_vector.py:69-72), no
  comment/string discrimination. Probe: a comment-only file carrying the 11 tokens -> missing []
  (green). Tool on the real target: "GOLDEN-VECTOR: ok - 11/11".
- BUT the lens's headline attack ("deleting every scene and the win gate while keeping the
  campaign() docstring still passes") is FALSE. My tokenize census (comments+strings stripped)
  confirms 10 of 11 tokens live inside string literals, yet 8 of those strings are LIVE DATA,
  not dead prose: the scene sheets at tools/dungeon.py:454, 464, 474-480 are consumed by
  _scene_sheet (dungeon.py:492-493); the WON verdict is a live assignment (dungeon.py:711); the
  --full flag is live argparse (dungeon.py:739); the scene loop tuple is live code
  (dungeon.py:630). Only 2 of 11 tokens ("scroll hoard, regrowth," at :611, "scrolls feed the
  Wyrm" at :614) are true docstring prose. The lens's per-line census mislabeled code lines as
  docstring-only, and its own falsifier ("any of the 10 also appearing on a live code line")
  actually fires: my mutation probe deleting scene-sheet heads + win verdict + --full wiring +
  scene loop returned missing = 5 tokens (S2, S3, WON, --full, scene loop). The tripwire FIRES
  on the lens's attack.
- The REAL vacuous shape (novel, probe-fired; economics.md:34 explicitly did not fire this
  class): keep every byte of scene data, gut only the wiring. My mutation deleted the
  play() -> campaign() dispatch, the root-anchor increment (dungeon.py:598-600), the
  _scene_sheet service of S2-S4, and made the win threshold unreachable: **missing = NONE,
  11/11 green with the campaign unable to run, the anchor unable to increment, and the win
  unable to fire**. The vector pins DATA, not EXECUTION. Fix changes accordingly: pin the
  executable spine (the dispatch line, the increment expression, the win comparison) and assert
  tokens on non-comment non-string lines (tokenize), keeping the docstring tier as a labeled
  second list.

### F4 seal patrol root of trust vouches for itself -> CONFIRMED (counts moment-corrected, drifts adjudicated, one laundering channel added)

- Census this sitting (moment 2026-10-05 ~20:2xZ, ledger live): 11,146 rows total, 10,875
  sha-bearing, **11 with prev_sha256 (unchanged from the lens's census: no new chain rows ever
  land)**, 7,248 with seq. The lens's 11,041 is the same file hours earlier (live writers).
- Chain-verifier census (scope: grep -rn over mag/ tools/ tests/ githooks/ scripts/, py files,
  untruncated): the only prev_sha256 chain verifier is mag/gwap_payload.py:687-711
  `verify_chain_file`, which enforces its OWN session-ledger schema (exact _ROW_KEYS, seq ==
  position, row_sha256 recompute) - a schema index_events.jsonl does not carry. All other
  prev_sha256 hits are gwap-format code and tests. tools/ledger_close_check.py reads
  index_events for timestamp freshness of burn closes only (read, :1-27). Absence claim stands
  with this scope.
- WARN-only confirmed at the hook bytes: githooks/pre-push seal_patrol block read this sitting;
  "drifted or cannot verify" share ONE warn arm, so even exit 2 (ledger missing) warns.
- Adjudication (the ask's owed work), patrol `--rows 1000` this sitting: 12 drifts (the ask's
  "10" is a prior moment; economics.md:11 measured 12 too). All 12 adjudicated by seal-history
  join (ledger ts/op per path) + git provenance + file mtime:
  - 4 are systematic autoseal mid-write races: file mtime trails the latest seal ts by seconds
    (sweep-x.md seal 15:49:53Z / mtime 15:50Z; steal-via-x.md 01:57:49Z / 01:58Z; RECEIPT.md
    06:30:54Z / 06:31Z; break-accuracy.md 20:20:23Z, a sibling lens writing its receipt during
    this pass). The writer seals before its final write, guaranteeing drift rows.
  - 2 are append-only queue lanes re-evolving after a same-day refresh (PACK_OFFLOAD.jsonl,
    STEALTH_MINED_FINDINGS.jsonl, both re-sealed 2026-10-05T12:09Z by writer
    "drift-patrol-cron", both still growing at 16:01/16:18 local).
  - 6 are post-seal edits through sanctioned channels, git-committed or live mid-run
    (STEALTH_SWEEP_LATEST.md sealed 2026-09-27, 8 days stale; DOORS.jsonl; r06_free_probe.py;
    moonshot-1.md; laws.md; MASTER_EXECUTE_REGISTER.md).
  - Verdict: 12/12 benign, zero tamper indicators TODAY. CONVERGENT with economics.md:13
    (independent adjudication, different method: theirs mtime-classified, mine adds the
    git-provenance and seal-history join).
- NEW and worse than unadjudicated: drift-patrol-cron is a LAUNDERING channel. Its daily
  "register" rows (purpose "hash refresh: static row evolved (patrol YYYYMMDD)", e.g. index_events
  ledger lines 10784/10785 at 12:09Z today) re-seal whatever the current bytes are, no judgment
  attached. A tampered queue file is re-baselined into compliance within 24 hours and the patrol
  goes quiet. Origin resolved after the first OWED (repo-wide grep for "drift-patrol-cron" over
  *.py): the string lives only in tests/test_index_fold_host.py (which pins the row SHAPE,
  "the composed-prefix case", :16) and four banked burn-wave scripts; B2_199_ledger_queue.py:13-16
  names the writer as ZCode-side automation OUTSIDE this tree ("the patrol is ZCode automation ...
  drove the daily whole-file LINKS.jsonl hash refreshes"), whose repo-side copy was a filed but
  unlanded B2-199 action item. So a root-of-trust re-baselining writer runs external to the
  estate, unpinned by anything but a test of its row shape. CONVERGENT with break-economics.md
  A3 (sibling hostile pass, landed mid-run this sitting: same laundering consequence, plus the
  bare-basename path dialect and deletion-invisibility extensions; my adjudication join hit the
  same bare-basename dialect - the two queue lanes read seals 0 under exact-path join until
  suffix matching).

## Blind spots in the lens, adjudicated

1. Consumption census (who reads gate/patrol output on decision days): still not run, no access
   log exists. OWED, unchanged.
2. memweave co-sign: RE-DERIVED this sitting, probe output in transcript:
   consensus_quality(['root anchored ok']*3) -> correlated_weak n_ind 1; same with
   independent=[True,True,True] -> strong n_ind 3; x4 -> strong eff 4.0. And consensus_gate:
   verdict(['the answer is 42'], model_params_b=27) -> CONFIRMED; verdict(['I cannot answer
   that']*3, model_params_b=27) -> CONFIRMED (unanimity-of-one + refusal-blind). Both sibling
   findings now hold with a first-hand run behind them (mag/memweave.py:165-169,
   mag/consensus_gate.py:86-98 per accuracy row 1).
3. citation_lint_io fingerprint: READ (tools/citation_lint_io.py:107-109). It is
   sha1("rule|record|anchor|detail[:80]")[:16] - a finding-identity hash for baseline
   acceptance. It is not in the credential path and has no masked-head comparison surface, so
   it does NOT share credential_shape's collision disease. Answered: no.
4. Skeleton cites: mickey17-burn.dwf.ts:352 and :454 verified byte-level (above);
   mickey17-v2.dwf.ts:59 and :376 verified. ractor-engine.dwf.ts break-file persistence: not
   audited. OWED.
5. Wild exploitation sweep: RUN (above), comment-pass convention is fleet-wide, zero vacuous
   stamps in the wild.
6. economics.md convergence: READ this sitting. It independently holds F1 (row 1), F2 (row 2),
   F4 (rows 4 + the 12-drift adjudication). The lens's unmeasured convergence is now measured:
   all three big findings are x3-verified (dogfood + economics + operations/accuracy).

## Ranked blindness table (blast radius: which blindness corrupts an operator decision first)

| # | Instrument | The fooling shape | Cheapest probe that proves it | The fix |
|---|---|---|---|---|
| 1 | tools/workflow_gate.py G1-G8 + FIRE_LEDGER | A 100 percent comment file PASSes all eight checks (proven); G8 stamp = any existing watch/inbox path; non-literal width invisible; fleet convention makes every declaration a comment while the firer sets width at run time, so the fired shape is outside the instrument and the ledger joins the comment | comment_only fixture -> PASS exit 0 (ran) | strip comment lines before run_checks; envelope stamp must match a measured-width figure + date inside the named file; FIRE_LEDGER width comes from the CreateWorkflow call site (a firer-minted row), not script-text parse; bank comment_only + INDEX.json fixtures as scenario cards that must FAIL |
| 2 | tools/mickey17_v2_fold.py verdict walk | Default-include: any key drift, capital letter, out-of-vocab verdict, or differently-shaped checks file silently rides `included` while PRISMA HOLDS; the crash fallback key can never join by construction | 4-variant fold probe (ran): 3 of 4 verdicts silently included | casefold the compare; default-EXCLUDE non-verified verdicts into a named unmapped-verdict bucket; join-hit-rate: a deep_tier2 key matching zero lane rows is exit 2; schema check: a checks file with zero list-valued keys is exit 2, not "none listed" |
| 3 | watch/inbox/index_events.jsonl + prepush_seal_patrol | 11 of 11,146 rows carry prev_sha256 and nothing verifies the chain; the channel is WARN-only including cannot-verify; autoseal seals mid-write (guaranteed noise); drift-patrol-cron re-baselines any drift, tampered or not, within 24h; the cron's source is unfindable | patrol --rows 1000 -> 12 drifts; adjudicate via seal-history + git (ran); grep census for a verifier (ran, none in scope) | genesis-chain the ledger going forward (each row carries prev_sha256 of the prior row); apply B2-277 to the seal block (exit 2 blocks, drift stays WARN until the mid-write race is fixed by sealing at write-complete); name and own the drift-patrol-cron writer or kill it |
| 4 | mag/consensus_gate.py + mag/memweave.py consensus_quality | Unanimity-of-one CONFIRMs; 3x byte-identical refusals CONFIRM; the CID guard is overridden by a caller-asserted boolean (identical bytes flagged independent -> "strong", eff 4.0) | two one-liner runs (ran, output above) | min 2 responses + honor sample_count; refusal/error strings classify UNVERIFIED before the unanimity branch; independence by construction only (distinct model or context digests), byte-identical answers cap at 1 witness regardless of flags |
| 5 | tools/prepush_golden_vector.py | Comment-satisfiable (substring over raw text) and byte-not-behavior: gut the wiring (dispatch, anchor increment, win threshold), keep the data -> 11/11 green with the campaign unreachable (ran); the lens's docstring-deletion attack actually trips 5 tokens, so the true fix is pinning the spine, not the prose | wiring-deletion mutation -> missing NONE (ran) | tokenize the target; assert spine tokens on non-comment non-string lines: the play() dispatch, the root_anchors increment expression, the win comparison; keep docstring tokens as a labeled prose tier |

Not attacked this pass (no sacred cows, just budget): tools/prepush_credential_shape.py (the
masked-head collision question was the lens's, and it lives in a different module than
citation_lint_io; its own internals unread here), tools/prepush_workflow_metadata.py,
tools/cache_kpi.py (its nominal-vs-receipted split is itself the finding surface; the deviation
"live rows await caller wiring" is already filed in commit 3f9b2c5f7), tools/citation_lint.py
CLI (only citation_lint_io's fingerprint read). OWED: each needs its own probe pass.

Scenario suite baseline for any amendment: `workflow_gate.py check --scenarios
configs/workflow_gate_scenarios` ran this sitting: 9 cards ok + pass_control, exit 0.

## Amendment to the R3 driver (one clause, round-4 relevant)

The R3 driver handed this round two soft spots that cost sibling budget and warped convergence
accounting. (a) It named mag/consensus_merge.py, a path that exists nowhere (the symbol lives at
mag/memweave.py:208; operations.md:40 and accuracy.md:97 both burned time on this). (b) Its
CONVERGENT x3 accounting accepted co-signs: the dogfood lens marked the memweave bypass
CONVERGENT without running it (its own blind spot 2), and only this pass's re-derivation made
the count true. Amendment: the R4 driver (1) byte-preflights every instrument path it names
(path resolves AND carries the named symbol) and moment-stamps every count it hands a lens
("N at moment M, re-census at fire time") - co-signed with operations.md:40; and (2) requires
that a CONVERGENT row name a probe the claiming lens actually ran: a row re-read but not re-run
files as CITED, not CONVERGENT, and the hostile pass is the designated re-runner (this pass
re-derived exactly the two co-signed probes and both held; the law should not depend on that
luck).
