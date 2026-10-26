# OUROBOROS R3 (TRUST INSTRUMENTS) - MOONSHOT-2 LENS FOLD (2026-10-05)

Lens: no sacred cows. The question asked of every instrument: what does it
CERTIFY versus what did it TOUCH. The sibling folds (accuracy, communication,
dogfood, economics, logic, operations, all read this sitting before writing)
converged on one disease: the layer grades mentions, not mechanisms. This
fold's swing is one level down: the founding phantom the whole citation
apparatus was erected against is STILL certified by that apparatus one
incidental substring away, the gate's meta-instrument (the scenario suite)
loses its all-pass control by file delete with zero mention, the fire ledger
R1 minted has zero consumers, and the credential baseline can pardon a secret
it never saw. Every claim below is probe-pinned: the runner
watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/probes/moonshot2_probes.py
reproduces all 8 expectations (8/8 at 19:55Z this sitting, exit 0).

## RANKED BLINDNESS TABLE

Rank = which blindness corrupts an operator decision first.

| # | Instrument | Fooling shape | Cheapest probe | Fix |
|---|---|---|---|---|
| 1 | tools/citation_lint_numbers.py (PHANTOM-NUMBER, blocking pre-push class) | The weak-form hole: for any decimal claim X.YM the search forms include the bare integer part X (citation_lint_numbers.py:72, `forms.append(plain.split(".")[0])`) and `file_contains` is substring-any over lowered source bytes (citation_lint_io.py:277-), so ANY incidental occurrence of "X" certifies the claim. Probed: a source carrying only "audit row 1914" certifies a claim of "191.8M tokens" -> lint exit 0. The founding fixture fired ONLY because DIGEST.md happened to carry zero "191" hits (the tool's own docstring, citation_lint.py:12-15). Second shape, same engine: the unit is never enforced -> "287.6M tokens" is certified by a source carrying only "latency 287.6" -> exit 0. Control: same sentence with a number whose no form matches -> PHANTOM fires, the teeth exist. The fold's twin engine shares the unit-blind form (carried_forms includes plain, tools/mickey17_v2_fold.py:126-136) but NOT the int-part form: two engines, different strength, same blind unit. | probes/moonshot2_probes.py P1-P3 (ran: 0/0/1 exits) | Drop the int-part form unless it is 4+ digits and unique-shaped; a unit-suffixed claim may only be certified by a unit-suffixed or expanded spelling (drop the bare decimal as a certifier of X.YM); merge _expanded_forms and carried_forms into one module so the two engines cannot diverge again. ~40 min. |
| 2 | tools/workflow_gate.py FIRE_LEDGER (R1 row 7) + the no-ungated-CreateWorkflow law | The join the ledger was minted for is written and never read: scoped census (grep FIRE_LEDGER over tools/ mag/ githooks/ scripts/ .zcode/workflows/ tests/, all extensions, 19:41Z) finds ZERO source consumers; the only hit is the writer's own .pyc. Deeper shape: the gate certifies (script path, digest) at CHECK time and nothing joins a FIRE to a PASS -> a script amended after its check fires with gate bytes stale and no instrument names it; the stop-cert cannot block what never re-checks. Blast radius: the "no ungated CreateWorkflow" law in AGENTS.md is enforced by convention alone. | The census grep above (ran, output: only tools/__pycache__/workflow_gate.cpython-311.pyc); ledger row count 2 at my moment vs REGISTRY 90 (wc -l, this sitting) | Minimum viable consumer in one sitting: a fire-audit that re-hashes every script named in REGISTRY PASS / FIRE_LEDGER rows and exits 2 on any PASS digest whose script bytes have drifted since certification (catches amend-after-check with zero harness access). The full fire-event join is OWED to harness journal reach (this seat cannot read the run journal: ListWorkflowRuns unavailable in a dwf child). ~45 min. |
| 3 | tools/workflow_gate.py scenario suite (the LAW-12 meta-instrument) | The all-pass control is optional and its absence is SILENT: run_scenarios guards the control with `if os.path.isfile(control)` (workflow_gate.py:408-417), so deleting configs/workflow_gate_scenarios/fixtures/pass_control.dwf.ts turns "the all-pass control must pass clean" (docstring :33-34) into no control at all, suite still exit 0 "9 cards validated". Probed on a temp copy. This is the G8 lesson at the meta layer: the one check that proves the gate can still PASS anything vanishes green. Corollary delta on the gate proper (CONVERGENT with all sibling rows on the class, delta on the tooth): G6-receipts hard-passes while never touching the filesystem at all -> naming watch/inbox/NEVER_LANDED_20261099.md plus a "fetched: 2026-10-05" stamp yields ok=True, no soft warn (probed, P4); G8 at least demands isfile (workflow_gate.py:191), G6 demands nothing. | probes/moonshot2_probes.py P4-P5 (ran: ok=True/no-soft; exit 0 silent) | Missing control = SCENARIOS ERROR exit 2 (flip the isfile guard's else); G6's stamp must name an existing file (same isfile the envelope stamp already uses). ~15 min. |
| 4 | tools/prepush_credential_shape.py (the baseline = the pardon surface) | Accept-by-NAME fingerprints to (shape, file, masked head) = value[:4] + length (prepush_credential_shape.py:94-104), so two DIFFERENT secrets sharing a 4-char head and length in one file mint the SAME fingerprint: baselining one silently auto-accepts the other. Probed: sk-abcd1111222233334444 and sk-abcd9999888877776666 -> identical fp. Plus one-match-per-line (rx.search at :112, probed: two keys on one line -> 1 finding), convergent with accuracy's shape-set note (ghp_/AKIA/JWT absent, SHAPES :70-91). The instrument that caught the live key day one can be pardoned around without ever loosening the hook. | probes/moonshot2_probes.py P6 (ran: True) | Store a salted hash of the FULL value in configs/prepush_credential_baseline.json (the masking law binds the WARN channel, not the private baseline file); fingerprint = shape + file + full-value hash; use finditer, not search. ~30 min. |
| 5 | tools/prepush_seal_patrol.py (the drift channel, adjudication below) | The patrol prints one undifferentiated DRIFT class over what are four measurably different phenomena, so 11 perpetual reds (my moment) train every push to ignore the channel a real tamper would arrive on (CONVERGENT with economics row 4's fatigue framing; operations row 2 and dogfood row 4 hold the ledger-forgery half). | `prepush_seal_patrol.py --rows 1000` (ran: 11 drifted, 343 distinct, 321 match, 11 missing) plus the adjudication script facts below | Patrol carries (mtime - seal_ts) seconds and git state per drift and splits the classes in output; the writer fixes are siblings' (re-seal-on-append, sealed-prefix test, chain fields). ~30 min for the display split. |

## THE 11 LIVE DRIFTS, ADJUDICATED (window 1000, 2026-10-05T19:33Z)

Method: for each drifted file, full-ledger row history (my adjudication
script), latest row ts/op, mtime UTC, `git status --porcelain`, last commit
date, and whether current bytes match ANY historical seal. NO file's current
bytes match ANY of its historical rows (cur_matches_row NONE on all 11): these
are real divergence, not window or case artifacts.

Classes and members:
- WRITER-RACE (seal stamped seconds to minutes BEFORE the final flush, then static, committed): frontier_olm_2026-10-04/sweep/...-x.md (28s), .../steal/... via x.md (31s), frontier_olm_2026-10-04/RECEIPT.md (22s, 11 rows), ribvault_20261005/r06_free_probe.py (3m), frontier_olm_2026-10-05/lens/laws.md (2m). Five of eleven.
- LIVE-APPEND (append-only boards, seal races every write): PACK_OFFLOAD.jsonl (19 rows, mtime 8 min before my run, git M), STEALTH_MINED_FINDINGS.jsonl (20 rows, same shape).
- POST-SEAL-EDIT, committed (git CLEAN: ledger and git disagree silently): STEALTH_SWEEP_LATEST.md (sealed 2026-09-26, edited and committed today), ractor_engine/2026-10-04-eleven-doors/DOORS.jsonl (sealed 10-04 18:46, edited today), corpus/steal/MASTER_EXECUTE_REGISTER.md (autoseal 16:13:23, mtime 16:36, single row, absolute-path form).
- THE ONE THAT STINGS: watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/moonshot-1.md, sealed 12:03:12, edited 13:22, committed CLEAN: a sibling LENS FOLD, this audit's own output, is a standing post-seal drift. The trust surface does not spare its auditors.

The ask said 10; my moment reads 11; siblings read 11 and 12 at theirs (moment law, oscillating with ledger appends).

## R3 DRIVER AMENDMENT (round-4 relevant)

The ask's own instrument claims were stale on arrival (86 files vs 92 at accuracy's moment; "10 real drifts" vs 11/11/12 across sibling moments; "11/11" and "9/9" unverified by any sibling at the same instant), and six lenses each re-ran the same instruments and re-adjudicated the same drifts (four adjudication tables now sit in this round dir). The round that audits trust instruments produces UNVERIFIABLE PROSE about instrument runs: nothing distinguishes a lens's "I ran X and it said Y" from a fabrication except other lenses re-running it. Amendment for the R4 driver: (a) the driver fires every named instrument itself at round open and banks a machine-readable PROBE SNAPSHOT (instrument, exact command, exit code, key output lines, moment) into the round dir; lens claims about instrument behavior must cite snapshot rows by path:line, and any claim not in the snapshot carries its own probe file under probes/ (this fold banks moonshot2_probes.py as the pattern: 8/8 expectations runnable, falsifiable by execution); (b) standing evidence (drift adjudication, census counts) is adjudicated ONCE in the snapshot, not re-derived by every lens; (c) the ask carries moment stamps next to every count it asserts, so a lens can name drift instead of re-censusing. This closes the recursion the loop is named for: the auditors' evidence becomes checkable by the same standard the auditors impose.

## Checks run this sitting (exact commands, this tree, this moment)

- ./.venv/Scripts/python.exe tools/prepush_seal_patrol.py --rows 1000 -> DRIFT exit 1, 11 drifted / 343 distinct / 321 match / 11 missing (19:31Z).
- Adjudication heredoc (full ledger 10800 sha rows, 3 malformed): per-file history, mtime, git state -> table above.
- citation_lint check --files on three temp fixtures -> exits 0 / 0 / 1 (weak form, unit-blind, control).
- workflow_gate run_checks import on a G6 text -> G6 ok=True, no soft, file absent.
- workflow_gate check --scenarios on a temp card copy minus pass_control.dwf.ts -> exit 0, 9 cards, zero mention.
- prepush_credential_shape scan_text import on two same-head keys -> identical fingerprints; two keys one line -> 1 finding.
- probes/moonshot2_probes.py -> 8/8 expectations reproduced, exit 0 (19:55Z).
- Censuses: FIRE_LEDGER consumers (scoped grep, zero in source), FIRE_LEDGER rows=2, REGISTRY rows=90, folded_at stamps 1 of 6 FOLD_SECTIONS.md (CONVERGENT with communication's 1 of 5; a 6th file appeared between moments).

## OWED (never asserted as fact)

- The harness-side fire journal (its existence, path, and payload shape): this dwf-child seat cannot reach ListWorkflowRuns or the journal store, so the fire-event join in finding 2's full fix is unverified beyond the zero-consumer census.
- Whether any consumer outside the grepped roots reads REGISTRY.jsonl PASS rows to authorize fires (scoped to tools/ mag/ githooks/ scripts/ .zcode/workflows/ tests/; the dashboard, skills tree, and anything outside the repo were not censused).
- citation_lint --changed was not run this sitting (the working tree is clean of prose changes by this seat); the probe fixtures ran under --files.

## BLIND SPOTS (honest)

- I read the sibling folds BEFORE probing, so my probes were aimed at gaps the siblings left; genuinely independent derivation is claimed only for findings 1-4's specific shapes (weak int-part form, unit-blind certification, control silent-skip, fingerprint collision), each probed live this sitting; finding 5 and the G6/G8 class are marked CONVERGENT where they overlap.
- I did not audit githooks/pre-push plumbing (which instruments the hook fires in what order) beyond what siblings quoted; taken from their folds, not re-derived.
- consensus_gate, memweave consensus_quality, cache_kpi, and the fold's deep_tier2 walk were read for convergence marking only; my probes did not re-exercise them, so I add no evidence there beyond the sibling folds'.
- The adjudication rests on one moment; PACK_OFFLOAD/STEALTH_MINED mtimes were minutes fresh, so their class could look different an hour later.
