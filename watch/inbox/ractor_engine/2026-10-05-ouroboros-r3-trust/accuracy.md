# OUROBOROS R3 - TRUST INSTRUMENTS - accuracy lens (2026-10-05)

Lens verdict: the trust layer's FAIL teeth were hardened by R1/R2 (stop-cert
proven, case fix landed, fold de-blinded), and every blindness this round
found is on the other face: vacuous PASS. Three of five instruments I probed
certify degenerate input as trusted, and the two CID organs disagree on the
law they both cite. Nothing here was taken from priors; every row below was
probed or read this sitting, commands named.

## Claim checks re-run at the ask's scale (all green, this moment)

- Scenario suite: `python tools/workflow_gate.py check --scenarios
  configs/workflow_gate_scenarios` -> "9 cards validated read-only", exit 0.
- Golden vector: `python tools/prepush_golden_vector.py` -> "11/11 golden
  tokens in tools/dungeon.py".
- Metadata patrol: `python tools/prepush_workflow_metadata.py` -> "scanned 92
  workflow file(s) (22 without a metadata block, skipped), 0 finding(s)".
  The ask said 86 files; the tree grew to 92 by census law (different moment,
  named, not a contradiction).
- citation_lint --changed -> ok, records=5 anchors=0 numbers-checked=2.

## RANKED BLINDNESS TABLE

| # | Instrument | Fooling shape (probed) | Cheapest probe | Fix |
|---|---|---|---|---|
| 1 | mag/consensus_gate.py | Unanimity-of-one: a SINGLE response forms a 1-element set, reads "unanimous", and at model_params_b >= 14 returns CONFIRMED. `sample_count` is accepted and never used. Identical refusal strings (3x "I cannot answer") at 27B also CONFIRM: agreement is measured, content is not. | Ran: `verdict(['the answer is 42'], model_params_b=27)` -> "CONFIRMED"; `verdict(['I cannot answer that']*3, model_params_b=27)` -> "CONFIRMED". mag/consensus_gate.py:86-98, unused param :71 | Require len(responses) >= 2 (and honor sample_count) else UNVERIFIED; classify pure-refusal/error strings as UNVERIFIED before the unanimity branch |
| 2 | mag/memweave.py consensus_quality (the ask's "consensus_merge") | The CID guard is inverted by its own honor-system flag: byte-identical echo-chamber answers marked independent=True each count as a NEW witness -> verdict "strong". | Ran: `consensus_quality(['root anchored ok']*3, independent=[True,True,True])` -> "strong"; x10 -> "strong". mag/memweave.py:163-169,178 | Byte-identical answers may only count extra witnesses when the independence flag is backed by a construction attestation (different model/context ids); otherwise cap n_ind at 1 for identical bytes |
| 3 | tools/workflow_gate.py | PASSes pure prose: a fixture with zero workflow content (all shapes in comments) exits 0 with G1,G2,G4,G5,G6,G7,G8 all "ok". G8's envelope exception verifies stamp SHAPE only: `envelope-receipt: watch/inbox/INDEX.json` (a directory index, no measurement) unlocked max_concurrency 50. Missing script exits 1, not the hard-block 2, so the direct CLI contract fails open under the estate's exit-2-only convention. | Fixture banked at watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/probes/g8_vacuous_envelope.dwf.ts; ran `workflow_gate.py check --script <fixture> --no-register` -> PASS exit 0; ran on a nonexistent path -> "GATE ERROR" exit 1. tools/workflow_gate.py:180-193, 447-449 | Scope G1-G7 shape regexes to extracted ask-string bodies, not whole file; envelope stamp must match a receipt-carrying pattern (measured width + date + token counts) inside the named file; unreadable script exits 2. Add both fixtures as scenario cards |
| 4 | tools/prepush_seal_patrol.py | Perpetual red: the window's 12 live drifts (ask said 10; 2 landed since, moment-named) mix a benign noise class with the tool's actual target class and the tool cannot tell them apart. A permanently red WARN is an ignored alarm: the 42-case-only lesson reborn one level up. | Ran `prepush_seal_patrol.py --rows 1000` -> DRIFT exit 1, 12 files; adjudicated each vs seal ts / mtime / git status (table below). tools/prepush_seal_patrol.py:108-137 | Ledger rows carry byte length; patrol splits "sealed-then-appended" (first sealed_len bytes still hash to the sealed sha) from "sealed-then-mutated" (real alarm); writers seal after final flush |
| 5 | tools/mickey17_v2_fold.py verdict walk | Latent case/enum fragility, CONVERGENT with the patrol's R2 case bug: exact-match `== "unconfirmed"` / `== "crashed"` while the runner's own enum has a 4th value ("same-chain-verified", .zcode/workflows/mickey17-v2.dwf.ts:59) and the runner counts ANY other string as unconfirmed (:376). One capital-U verdict from a child model and runner and fold silently diverge. Outside deep_tier2 the verifier table still walks lengths, not values (vc[k] += len(v) over supports/rows/entries, :278). | Ran archive census over all *.checks.json: 52 deep_tier2 verdicts, values exactly {'verified':46,'unconfirmed':6}, 0 missing row_key -> holds TODAY, unguarded tomorrow. tools/mickey17_v2_fold.py:278,330-337 | Normalize verdict with .lower() at the walk; unknown verdict values file into a named "unmapped-verdict" PRISMA bucket instead of riding included; extend the value split to every list-valued key |
| 6 | citation_lint_numbers.py + fold unbound_aggregates | The 191.8M class survives one line of prose: both engines skip any sentence/line that names NO resolvable source (or names a MISSPELLED path), so a fabricated aggregate citing a wrong path is invisible. | Code-read: `if not sources: continue` at tools/citation_lint_numbers.py:210 and tools/mickey17_v2_fold.py:171. (Not live-probed this sitting; the founding phantom only fired because its path resolved.) | A notable number on a line whose named paths ALL fail to resolve is its own finding class (UNRESOLVED-SOURCE), warn tier |

Smaller teeth, named: prepush_credential_shape.py:70-91 misses ghp_/AKIA/JWT
shapes and only one match per line per shape (:112); prepush_workflow_metadata
scans only project .zcode dirs, the global ~/.zcode/workflows archive is
outside SCAN_DIRS (checked: empty today, latent); FIRE_LEDGER.jsonl has 1 row
vs REGISTRY.jsonl 89: the width-join is dark because the write-path hook gates
a temp payload copy (its one row shows `width: "50"` riding next to
`max_concurrency: 3`, the arg-level fan-out width invisible to G8's regex).

## THE 12 LIVE SEAL DRIFTS, ADJUDICATED (window 1000, 2026-10-05 ~18:00Z)

Classes: WRITER-RACE = seal sha computed before the file's last bytes landed
(mtime - seal ts in seconds, git-clean, content a final flush); LIVE-APPEND =
append-only ledger vs point-in-time seal, perpetual by design; POST-SEAL-EDIT
= the patrol's real target class, a sealed board changed later.

| file | sealed_ts | mtime (UTC) | gap | class |
|---|---|---|---|---|
| corpus/steal/MASTER_EXECUTE_REGISTER.md | 16:13:23 | 16:36:12 | +23m | POST-SEAL-EDIT (git-clean: committed bytes diverge from their seal, ledger vs git disagree silently) |
| watch/inbox/frontier_olm_2026-10-04/RECEIPT.md | 06:30:54 | 06:31:16 | +22s | WRITER-RACE |
| watch/inbox/frontier_olm_2026-10-04/steal/open-and-local-language-models via x.md | 01:57:49 | 01:58:20 | +31s | WRITER-RACE |
| watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md | 10-04 15:49:53 | 15:50:21 | +28s | WRITER-RACE |
| watch/inbox/frontier_olm_2026-10-05/lens/laws.md | 14:13:49 | 14:15:45 | +116s | WRITER-RACE |
| watch/inbox/frontier_olm_2026-10-05/sweep/evals-self-improvement-reddit.md | 17:56:11 | 17:56:13 | +2s | WRITER-RACE |
| watch/inbox/PACK_OFFLOAD.jsonl | 12:09:13 | 17:48:20 | +5h39m | LIVE-APPEND |
| watch/inbox/ractor_engine/2026-10-04-eleven-doors/DOORS.jsonl | 10-04 18:46:05 | 10-05 13:05:26 | +18h19m | LIVE-APPEND |
| watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/moonshot-1.md | 12:03:12 | 13:22:27 | +1h19m | POST-SEAL-EDIT |
| watch/inbox/ribvault_20261005/r06_free_probe.py | 05:37:49 | 05:40:50 | +3m01s | WRITER-RACE |
| watch/inbox/STEALTH_MINED_FINDINGS.jsonl | 12:09:15 | 17:58:29 | +5h49m | LIVE-APPEND (the only M in git: drift uncommitted) |
| watch/inbox/STEALTH_SWEEP_LATEST.md | 12:09:11 | 13:50:15 | +1h41m | POST-SEAL-EDIT / live pointer board |

Verdict: zero of 12 show tampering evidence, but 12 of 12 prove the seal is
never taken over final bytes, and the 3 POST-SEAL-EDIT rows are only
separable from noise by THIS manual adjudication (mtime delta + git status),
not by the instrument. The ask's "10 real drifts" measured 12 at this window
and moment; both newer rows (evals sweep, laws.md) are R3-round siblings
landing after the R2 measurement.

## R3 DRIVER AMENDMENT (round-4-relevant)

R1 hardened FAIL teeth (vacuous-fail side: the G8 19-missing-headers lesson);
this round shows the PASS side was never probed: 3 of 5 instruments certify
degenerate input. Amendment: R4's driver must require, per instrument touched,
a vacuous-pass probe alongside any FAIL-path fixture: one degenerate input
that SHOULD be refused (single-sample consensus, echo-chamber independence
flags, comment-only workflow script, uncited fabricated number, capital-case
verdict value) asserted to produce the BLOCKING verdict, banked as a scenario
card or unit fixture in the same commit. Cost per instrument: minutes; it is
the exact probe class that found rank 1-3 here.

## CORRECTION (hostile second pass, 2026-10-05 ~20:36Z): the drift adjudication table above is superseded

The first-pass mtime+git taxonomy was wrong on 7 of the rows. The authoritative
classification is byte-level: for each drifted file, does any byte-prefix of
the current bytes hash to the sealed sha (APPEND: sealed bytes survive verbatim,
writer only added) or not (REWRITTEN: the sealed content itself was altered in
place). Command this sitting: patrol's own resolver (tools/prepush_seal_patrol.py
parse_ledger + resolve_sealed_path, window last 1000 of 10880 sha rows, moment
2026-10-05T20:36:19Z) plus an incremental sha256 over every byte prefix with
FULL-sha compare. Result:

- APPEND (benign, 3): moonshot-1.md (sealed 10664 of 13005, +2341 appended;
  byte-identical to the hostile pass's independent measurement, CONVERGENT),
  PACK_OFFLOAD.jsonl (line-boundary prefix pure to 6,207,092 of 6,280,209),
  STEALTH_MINED_FINDINGS.jsonl (sealed 512,947 of 535,089, +22,142).
- REWRITTEN (the patrol's alarm class, 9): MASTER_EXECUTE_REGISTER.md (+23min,
  git-clean: committed bytes diverge from their last seal), RECEIPT.md (+22s),
  steal/open-and-local (+31s), sweep/open-and-local (+28s), laws.md (+116s),
  r06_free_probe.py (+3m01s), STEALTH_SWEEP_LATEST.md (+1h41m), DOORS.jsonl
  (18h19m; classed LIVE-APPEND in the first pass, actually a REWRITE: a door
  registry whose sealed bytes did not survive), and this round's own
  break-accuracy receipt (sealed 20:20:23, rewritten after).

Two instrument notes the byte pass surfaced: (1) my own first scanner run was
wrong on all 12 rows (compared the full 64-char digest against the patrol's
truncated 12-char sealed sha) and was caught only by the hostile pass's
independent byte test of moonshot-1.md; the corrected scan is the falsifier in
motion. (2) Each seal event writes TWO ledger rows (one class/nonce/op/purpose/
seq keyed, one bytes/op/purpose keyed), so 10,880 sha rows is ~5,440 events and
the patrol's "last 1000 rows" window spans roughly 500 events; and
moonshot-1.md alone carries ~30 seal rows (10-02 through 10-05 20:35), an
actively re-sealed board whose drift status is a moving floor between moments.

Corrected conclusion: the permanently-red thrust survives, strengthened. The
patrol's whole-bytes compare (tools/prepush_seal_patrol.py:132) cannot make
the append/rewrite split at all; a prefix-hash split would clear exactly the
3 append rows and keep the 9 rewrites red, and 6 of those rewrites happened
SECONDS after their seal (writer lifecycle: seal computed before the final
whole-file write, so the seal is decorative for those boards) while 2 carry
hour-scale gaps (MASTER_EXECUTE_REGISTER.md, DOORS.jsonl) that no manual
mtime heuristic would have sorted correctly. The fix is two-part: patrol-side
prefix split (append vs rewrite), writer-side seal AFTER the final flush.

## Honest blind spots

- The live fold was NOT re-run: it regenerates run-0/FOLD_SECTIONS.md in the
  estate and a fresh folded_at stamp would drift the working tree from the
  committed receipt; the verdict-walk claims rest on code-read plus the
  archive census, not a live fold. Operator can run it safely on a slug copy.
- The seat-law hook's invocation source was never located (grep of project and
  user settings found nothing; only its BEHAVIOR was observed blocking two
  .dwf.ts Writes and passing a third). Whether any wiring passes a non-temp
  script path to the gate is OWED; the exit-1 fail-open is proven at CLI
  level only.
- mag/context_checkpoint.py (the cache_receipt producer behind cache_kpi's
  receipted split) was not audited this sitting.
- The ask's "three skeletons" were not located by that name; mickey17-v2.dwf.ts
  was read, mickey17-burn.dwf.ts only grepped, and the ask's
  "mag/consensus_merge.py" path is wrong on disk (the symbol lives in
  mag/memweave.py:208; separate mag/_consensus_witness.py exists, unread).
- cache_kpi --since lexicographic compare is theoretically blind to
  non-ISO ts rows; censused 77,716 rows of logs/provider_usage.jsonl: all
  ISO today, so latent, not live.
- Falsifier for the flagship: a gate version that extracts ask-string bodies
  and runs G1-G7 inside them would FAIL the banked probe fixture; a consensus
  gate requiring n>=2 would fail the unanimity-of-one probe.
