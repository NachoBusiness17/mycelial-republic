# OUROBOROS R3 - LOGIC LENS: the trust layer can still be fooled, and I proved four shapes by execution

Seat: lens-logic, 2026-10-05. Topic: TRUST INSTRUMENTS (round 3 of 5). Everything
below was read or run this sitting on the live tree unless marked OWED/not run.
No em-dashes. Universal claims are scoped to the search actually run.

## 0. Verdict

The three named lessons (vacuous pass, lengths-not-values, case-blind compare) each
have a living descendant in the current instruments. I fired probes at four of them
and all four landed: the fold's verdict join silently drops unconfirmed verdicts on
any row_key wording drift while an unfalsifiable assert vouches "invariant HOLDS";
G8's envelope exception verifies file EXISTENCE, never receipt content (CONVERGENT
with all three sibling lenses, plus my live-function run); the seal patrol's drift
findings age out of the default pre-push window in hours (measured in-session: 11
drifts at --rows 1000, 2 at the default 150); and mag/consensus_gate.py returns
CONFIRMED for a single response with a dead sample_count parameter. The 10 (now 11)
real drifts are adjudicated below: zero tampering, eleven unsealed post-seal writes.

## 1. THE DRIFT ADJUDICATION (the ask's named evidence task)

Command: `.venv/Scripts/python.exe tools/prepush_seal_patrol.py --rows 1000` ->
exit 1, "337 distinct file(s), 317 match, 9 missing-on-disk" and ELEVEN drift rows
(the ask's snapshot said 10; the tree moved between the ask and my run; the ledger
grew 10770 -> 10774 sha rows during my session alone). Per-file ledger history was
dumped by a one-shot script (since deleted); every drifted file's FULL ledger row
list was read. Findings per file:

| file | last seal (ts, op) | adjudication |
|---|---|---|
| watch/inbox/STEALTH_SWEEP_LATEST.md | 2026-10-05T12:09Z register, sha 20EB4ACE1F63 | live rolling snapshot rewritten after its daily register; writer does not re-seal per rewrite. Benign intent, unsealed truth |
| watch/inbox/PACK_OFFLOAD.jsonl | 2026-10-05T12:09Z register | live append queue (29,758 lines on disk, 6.2MB), grows all day post-seal. Same class |
| watch/inbox/STEALTH_MINED_FINDINGS.jsonl | 2026-10-05T12:09Z register | live append queue (1,200 lines), same class |
| frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md | 10-04T15:49:53Z register+autoseal | sealed WORK PRODUCT edited after seal with no later ledger row. The tamper class the patrol exists for, here a sibling seat appending without re-sealing |
| ractor_engine/2026-10-04-eleven-doors/DOORS.jsonl | 10-04T18:46Z register+autoseal | same: run artifact edited post-seal |
| frontier_olm_2026-10-04/steal/open-and-local-language-models via x.md | 10-05T01:57Z register+autoseal | same |
| frontier_olm_2026-10-04/RECEIPT.md | 10-05T06:30:54Z register+autoseal after 3 rapid re-registers 06:22 -> 06:30 | seat demonstrably knew to re-seal (churn), then stopped; latest edit unsealed |
| ribvault_20261005/r06_free_probe.py | 10-05T05:37Z register+autoseal | SHARPEST: sealed CODE drifted. Any "I ran sha e162..." receipt now vouches for bytes that no longer exist on disk |
| ractor_engine/2026-10-05-ouroboros-r2-gaps/moonshot-1.md | 10-05T12:03Z register+autoseal | in-flight sibling work file edited post-seal |
| frontier_olm_2026-10-05/lens/laws.md | 10-05T14:13Z register+autoseal | in-flight sibling lens file edited post-seal |
| corpus/steal/MASTER_EXECUTE_REGISTER.md | 10-05T16:13Z autoseal sha 686F208290FC | the 60M flagship master fold, drifted within ~2h of its seal |

Adjudication verdict: 0 of 11 are rollbacks or ledger forgeries; 11 of 11 are
sanctioned-writer or sibling-seat writes landing AFTER the file's last seal with no
later ledger row (the dump shows "rows after it: none" for every file). Three are
live append surfaces, seven are in-flight work files, one is a master fold. Limit
named honestly: the ledger stores shas only, so append-vs-rewrite direction is not
recoverable from it; I classified by ledger op history, line counts, and git-modified
status, not by byte archaeology. The systemic disease is writers that never re-seal
on write/close, and (see blindness R3) a patrol whose default window forgets a drift
hours after it appears. My own probe scripts were auto-sealed on Write and drifted
by my Edit, briefly inflating the default-window list; they are deleted (missing-on-
disk is expected seal-chain behavior per the a12 law, prepush_seal_patrol.py:120-123).

## 2. RANKED BLINDNESS TABLE (blast radius = which corrupts an operator decision first)

### R1 (HIGHEST): tools/mickey17_v2_fold.py - the deep_tier2 join is exact-string, its failure is silent, and the invariant that "proves" the recount cannot fail

- Instrument: the de-blinded PRISMA walk, mickey17_v2_fold.py:321-367.
- Fooling shape: ANY wording drift between the lane row's claim and the persisted
  row_key orphans the verdict. The refire path guarantees this happens: tier-1's
  merge-not-rewrite clause (mickey17-burn.dwf.ts:330-332 "keep every existing key
  verbatim (including deep_tier2); replace only lane/supports/counts") preserves
  STALE deep_tier2 while claims are re-written, so every refired lane with edited
  claims carries verdicts that join nothing. My probe (2-row lanes, so the
  single_row_dead rule did not fire): a stale row_key verdict=unconfirmed ->
  "excluded: 0, included: 4" while the SAME fold's verifier table read "deep_tier2
  2 (verdict split: unconfirmed 2)". Two instruments in one file disagreeing, no
  adjudicator. A 5-word row_key against a 6-word ceremony claim ALSO drops the
  exclusion (my first control, mis-built, proved the field sensitivity by accident);
  the true 6-word key excludes correctly, so the walk works only on exact alignment.
- Compounding defect: the "invariant" at mickey17_v2_fold.py:365-367 is a
  tautology. The loop at :347-358 is an if/elif/else chain where every row
  increments exactly one of included/excluded, and identified = len(all_rows) at
  :359, so `assert identified == included + sum(excluded.values())` cannot fire on
  any input. It prints "HOLDS" as evidence; it is theater, the exact G8-lesson
  shape living inside the instrument that was created to cure that lesson.
- Second shape rule in the same walk: single_row_dead (:346, :350) excludes EVERY
  1-row lane as "phantom-source (dead-lane negative row)" BEFORE the verdict join
  is consulted; my first probe's high-leverage unconfirmed row was excluded for the
  wrong reason while its unconfirmed verdict counted nowhere. Shape over value.
- Cheapest probe (DONE, ran it): build runs/ouroboros-r3-probe with one aligned and
  one stale row_key; read FOLD_SECTIONS.md: excluded counts only the aligned one,
  invariant HOLDs in both runs. Artifacts deleted after capture.
- Fix (one sitting): after the walk, compute orphaned = (deep_unconf | deep_crashed)
  minus every key that actually matched a row, and emit a hard section line
  "ORPHANED VERDICTS: N persisted deep verdicts joined no row (refire claim drift?)";
  require orphaned == 0 for a clean fold, mirroring the existing gate-vacuous
  self-annotation at :303-304. Delete or reword the tautology assert (it certifies
  nothing) and make the fold reconcile its own verifier-table unconfirmed count
  against PRISMA's excluded-for-unconfirmed count, failing loud on divergence.

### R2 (CONVERGENT, all four lenses): tools/workflow_gate.py G8 - the envelope exception verifies stamp shape, not receipt content; and widths the regex cannot read pass as undeclared

- Instrument: g8_width_shape_ok, workflow_gate.py:180-193.
- Fooling shape A: `envelope-receipt:` naming ANY existing watch/inbox file passes
  ANY width. Ran it against the live function: max_concurrency 99 with
  envelope-receipt: watch/inbox/INDEX.json -> True; an unrelated night-shift
  receipt also -> True; the no-stamp control -> False (so the blindness is exactly
  the content-blind isfile at :191, not the width regex).
- Fooling shape B (communication lens probes, read this sitting): a width declared
  as `const W = 50; maxConcurrency: W` is invisible to G8_MAX_CONCURRENCY_RE
  (:176) AND to max_declared_width (:288-291), so FIRE_LEDGER logs max_concurrency
  null while the run fires 50 wide. The three live width-10 declarers
  (fill-ball.dwf.ts:25-26, gap-analysis.dwf.ts:27-28, the-50.dwf.ts:20-21) all
  cite the same real receipt (watch/inbox/ENVELOPE_50W_HIT_20260926.md, exists,
  verified this sitting), so today's estate is clean; the gate is what is foolable.
- Cheapest probe (DONE for A, read-not-fired for B): the probe files already sit in
  probes/ (g8_vacuous_envelope.dwf.ts, communication_g8_stamp.dwf.ts,
  communication_g8_evade.dwf.ts); mint them as scenario cards.
- Fix (one sitting): in g8_width_shape_ok, open the stamped receipt and require a
  width token >= the declared width inside its bytes (regex
  `max[_ ]concurrency[^0-9]{0,12}(\d+)` plus the receipt's own "at max_concurrency
  10" phrasing); a stamp naming a file with no width number fails. For shape B,
  extend G8_MAX_CONCURRENCY_RE with a camelCase `maxConcurrency\s*[:=]\s*([A-Za-z_
  $][\w$]*)` alternative that at minimum logs the symbolic name to FIRE_LEDGER as
  width-unresolved so symbolic widths stop reading as null.

### R3: tools/prepush_seal_patrol.py - drift findings age out of the default window and never re-alarm; the ledger's sha anchors decay to a ~4-hour tail

- Instrument: patrol() window logic, prepush_seal_patrol.py:108-137, DEFAULT_WINDOW
  150 (:55).
- Fooling shape (measured, not crafted): the ledger gains roughly 150 sha rows per
  4 hours (lines 10782 -> 10938 between 12:09Z and 16:13Z today), so the default
  pre-push window spans only the last ~4 hours of estate writes. My in-session
  measurement: 11 drifts at --rows 1000, 2 at default 150. A file that drifts and
  then ages five hours out of the window stays drifted forever with zero standing
  alarm, while receipts and audit prose keep citing its sealed sha as an integrity
  anchor. This is not a crafted attack; it is the patrol's default posture.
- Cheapest probe (DONE): run both windows in one session and diff the drift lists
  (command and counts above; the 9 drifts present at 1000 and absent at 150 are the
  proof).
- Fix (one sitting): a sticky drift sidecar. When the patrol finds drift at any
  window, append (path, sealed_sha) to configs/seal_drift_register.jsonl; every
  future patrol warns on any registered drift still unhealed regardless of window,
  and drops the row only when bytes re-match a fresh seal. Cost stays bounded (the
  sidecar is small), and drift becomes sticky instead of aging out. Separately, the
  master-fold and queue writers (the 11 files above) should re-seal on close; the
  patrol already names this fix in its own output.

### R4: mag/consensus_gate.py - a single response is "unanimous" and returns CONFIRMED; sample_count is a dead parameter

- Instrument: verdict(), mag/consensus_gate.py:68-98.
- Fooling shape (ran it): verdict(responses=["paris"], model_params_b=30) ->
  CONFIRMED. len(unique)==1 is satisfied by n=1; nothing requires n >= 2 or
  n >= sample_count. sample_count is accepted at :71 and never read (verified by
  inspect: the identifier does not appear in the function body). The CID law's own
  docstring says unanimity among N samples; n=1 is not agreement, it is one
  opinion, and the gate stamps it CONFIRMED at any size above the 3B floor.
- Blast radius: latent today. Scoped census (grep -rln over mag/, tools/, queue/,
  scripts/, dashboard/, main.py, 2026-10-05): zero production callers; the
  instrument is the CID-law reference awaiting wiring, which is exactly when the
  defect must be fixed, before the first caller bakes it in.
- Cheapest probe (DONE): the one-liner above plus
  verdict(responses=["paris"], sample_count=5) -> still CONFIRMED.
- Fix (one sitting): reject n < 2 (or n < sample_count when given) as UNVERIFIED
  with a "single-witness" label, and either wire sample_count (require
  len(responses) >= sample_count) or delete the parameter; add both cases to the
  scenario suite as foil cards.

### R5: tools/cache_kpi.py - a bare receipt_ok boolean credits a row's FULL nominal cache as receipt-verified

- Instrument: the receipt clamp, cache_kpi.py:180-185.
- Fooling shape (ran it via compute() on a synthetic row): cache_hit_tokens=1000,
  miss=1000, cache_receipt={"ok": true} with NO verified_tokens -> receipt_tok
  1000, recv_hit% 0.25 alongside nominal 0.5. The fallback at :182 (`verified =
  r_tok if isinstance(...) else (cached or 0)`) treats the row's own claim as its
  own receipt. A producer that stamps ok=true without token evidence collapses the
  nominal-vs-receipted split entirely, which is the whole reason this KPI exists
  (the arXiv no-unreceipted-hits law, docstring :26-33). The synthetic 15.75% vs
  50% proof (commit 4992d4085) used shape-matched rows; live caller wiring is
  pending and will inherit the hole.
- Cheapest probe (DONE): the compute() one-liner above.
- Fix (one sitting): a receipt row with ok=true but no numeric verified_tokens
  counts in receipt_rows but contributes 0 receipted tokens (or downgrades to
  nominal-only with a "receipt-boolean-only" column); one branch at :182.

### R6 (minor, named for the table): stop-cert escapes by rename + one-byte edit

- load_stopcert_index keys on name/basename/path/digest
  (workflow_gate.py:244-285); a retired script renamed and trivially edited mints a
  fresh digest and path and re-certifies. The operator pen remains the authority,
  but the instrument should at least warn when a BLOCKED-STOPCERT digest's script
  bytes re-appear under a new name within N days (a FIRE_LEDGER join), so the pen
  has teeth against sloppiness, not malice. Probe: rename a fixture of a retired
  digest, expect PASS today. Not executed this sitting (shape is evident from the
  keying code; the end-to-end stop-cert block WAS proven at R1 landing per commit
  4992d4085, not by me).

## 3. Checks run this sitting (exact commands, point-in-time on a moving tree)

- `.venv/Scripts/python.exe tools/workflow_gate.py check --scenarios
  configs/workflow_gate_scenarios` -> 9 cards ok + pass_control "all 8 gates
  clean", exit 0. Matches the ask's 9/9.
- `.venv/Scripts/python.exe tools/prepush_golden_vector.py` -> "11/11 golden
  tokens", exit 0. Matches the ask's 11/11.
- `.venv/Scripts/python.exe tools/prepush_seal_patrol.py --rows 1000` -> exit
  drift listing, 11 rows (adjudicated above); same at default window -> 2 rows.
  Note: my first default-window run piped through head, so the "EXIT=0" I saw was
  head's, not the patrol's; the code path (prepush_seal_patrol.py:160-161) returns
  1 on drift and I do not claim otherwise.
- Probes A/B (G8 + cache_kpi) and the fold probe: executed via the live functions
  and the real fold CLI (`--run ouroboros-r3-probe`, artifacts deleted after
  capture). Probe scripts and the probe run dir are removed; the drift they
  briefly caused is gone with them.
- Not run this sitting (read only): prepush_credential_shape.py,
  prepush_workflow_metadata.py, citation_lint.py full engine
  (citation_lint_numbers.py internals unread; its any-source semantics are
  inferred from the shared class in mickey17_v2_fold.py:150-187, marked OWED).

## 4. AMENDMENT TO THE R3 DRIVER (round-4-relevant gap)

The scenario suite has 9 cards and every one is a REGRESSION card: it proves each
gate FAILS a bad fixture (fail_g1..fail_g7, soft_g6) or legitimately passes
(pass_g8_envelope, pass_control). Zero cards are FOIL cards: fixtures engineered to
PASS today's gate while violating its intent. Every blindness found this round
across all lenses (G8 envelope content-blindness, symbolic widths, the fold join,
the cache boolean, n=1 consensus) is a vacuous-pass shape, and the suite is
structurally incapable of seeing that class, so each fix lands without an
adversarial fixture that would catch its regression back into foolability.
Amendment: from round 4 on, every trust-instrument round must bank at least one
FOIL CARD per instrument it amends, into configs/workflow_gate_scenarios for gate
instruments (the three probe files already in probes/ are the raw material: mint
g8_vacuous_envelope.dwf.ts as a card whose expected_verdict flips from PASS to FAIL
after the R2 fix) and as scripted probe rows for non-gate instruments (the fold
orphan check, the cache boolean row, the n=1 consensus row). A round whose
amendments carry no foil card does not close.

## 5. Blind spots (honest)

- citation_lint_numbers.py's phantom engine: not read; the PHANTOM-NUMBER
  any-source-carries weakness I suspect by class-similarity with
  mickey17_v2_fold.py:182-186 is OWED, not asserted as fact.
- Drift append-vs-rewrite direction: unrecoverable from sha-only ledger rows; my
  adjudication classifies by op history, sizes, and git status, and says so.
- The G1-G7 comment-satisfiability class: I read the probe
  (g8_vacuous_envelope.dwf.ts) but did not fire the gate against it; the sibling
  lens owns that execution. My G8 executions cover shapes A and the control only.
- consensus_gate caller census scoped to mag/, tools/, queue/, scripts/,
  dashboard/, main.py; tests/ intentionally excluded, corpus/ and docs/ not
  censused. The claim is that census, not the universe.
- Everything is point-in-time on a tree with sibling sessions writing (the ledger
  grew 4 sha rows mid-session; drift counts will differ by the time this is read).
