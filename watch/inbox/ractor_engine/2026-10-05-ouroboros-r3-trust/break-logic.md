# BREAK-LOGIC: hostile second pass on the logic lens (OUROBOROS R3, trust instruments)

Moment: 2026-10-05, ~20:20-21:00Z. Tree: branch mag/run-beta1-factory-build-audi-20260806T231709Z, sibling
sessions writing concurrently throughout (the seal ledger grew and one drift re-sealed DURING this pass, see
V3). All probes fired in-process or via `.venv/Scripts/python.exe` from the repo root; no subprocess spawns
beyond the harness shell itself, so the win32 CREATE_NO_WINDOW law had no surface to carry (nothing I wrote
spawns children). Probe artifacts kept: `probes/break_citation/` (six files, the phantom-number fixtures).
The fold probe run dir `memory/runs/mickey17_v2/runs/ouroboros-r3-breakrun/` was deleted after capture (the
lens's own convention). One fixture write was BLOCKED by the seat-law hook (two synthetic .dwf.ts fixtures
failed the workflow gate on payload, G1-G3); the in-memory probe below replaces those bytes, and the block
itself became evidence (see A2).

## VERDICTS

### V1. The fold's deep_tier2 verdict join drops unconfirmed verdicts on row_key drift; the PRISMA invariant is a tautology. CONFIRMED (strengthened: new enum-drop shape, and the divergence is between two sections of the SAME scripted output)

Byte-check, every cite correct:
- `tools/mickey17_v2_fold.py:321-337` builds `deep_unconf`/`deep_crashed` from normalized row_keys; `:339-342` `deep_keys()` computes exactly `norm(laneId + ": " + first-six-claim-words)` (two whitespace variants, nothing fuzzier); `:347-358` is an if/elif/else where every row increments exactly one counter; `:359` defines `identified = len(all_rows)`; therefore the assert at `:365-367` holds identically on every input that reaches it. Tautology confirmed by reading; no input can fire it.
- Refire path: `.zcode/workflows/mickey17-burn.dwf.ts:329-332` (the lens cited "mickey17-burn.dwf.ts:330-332"; the file lives under `.zcode/workflows/`, path was abbreviated, lines are real): tier-1 refires are ordered to "Read the file first if it exists; keep every existing key verbatim (including deep_tier2); replace only lane/supports/counts." Persisted row_keys reference OLD claim wordings while claims can be rewritten, so the join starves. Mechanism confirmed byte-for-byte.
- Certificate claim: `git log -1 4992d4085` message reads "deep_tier2 12 verified - excluded=0 is now a verified zero". The commit does cite the fold's excluded=0 as operator evidence.

Executed re-derivation (my own probe, not the lens's): a 4-row lane with 3 persisted `verdict=unconfirmed`
row_keys, one exactly aligned, one off by one word (5-word key), one stale refire wording, plus one aligned
key carrying `verdict="refuted"`:
- CLI output: `lanes=1 rows=4 included=3 excluded=1`.
- Same run's FOLD_SECTIONS.md: verifier table line 28 reads `deep_tier2 4 (verdict split: refuted 1, unconfirmed 3)` while PRISMA lines 41-42 read `excluded: 9 verifier-unconfirmed (deep_tier2): 1, included: 3`. The two scripted sections of one file disagree about the same bytes; nothing alarms.
- MY DELTA over the lens: an UNKNOWN VERDICT ENUM is silently ignored. `:334-337` files only `unconfirmed` and `crashed`; any other verdict string (`refuted`, `failed`, empty, typo) joins nothing and the row lands included. The lens's finding named wording drift; the enum drop is a second, independent silent pass-through in the same walk.
- The lens's falsifier ("join fuzzier than exact first-6-words") is DISPROVEN by execution: the 5-word key did not join.
- Probe cost was ~10 minutes including cleanup; artifacts deleted.

### V2. G8's envelope exception checks file EXISTENCE, never content; symbolic/camelCase widths pass undeclared. CONFIRMED (CONVERGENT, and my independent re-derivation agrees)

Byte-check: `tools/workflow_gate.py:176` `G8_MAX_CONCURRENCY_RE = max_concurrency\s*[:=]\s*(\d+)` (snake_case,
numeric literal only); `:189-192` the stamp test is `("watch/inbox" in path ...) and os.path.isfile(path)`;
docstring at `:184-185` admits "a stamp counts only when the named path exists". Cite `:180-193` correct.

Executed this sitting (live function import, not a mock):
- `max_concurrency: 99` + `envelope-receipt: watch/inbox/INDEX.json` -> `g8_width_shape_ok: True`, `max_declared_width: 99`. INDEX.json is a real file carrying no width measurement: any existing watch/inbox path authorizes any width.
- `const W = 50; maxConcurrency: W` -> True with `max_declared_width: None`: invisible to the gate AND logged as null width to FIRE_LEDGER.
- Controls behave: bare `max_concurrency: 99` -> False; stamp naming a missing file -> False.
- Estate-clean claim verified: `.zcode/workflows/fill-ball.dwf.ts:26`, `gap-analysis.dwf.ts:28`, `the-50.dwf.ts:21` all stamp `envelope-receipt: watch/inbox/ENVELOPE_50W_HIT_20260926.md` (grep this sitting) and the receipt exists. The gate is foolable; today's fleet is not fooling it.
- Convergence cite verified: `communication.md:50-56` names all sibling lenses and their probes A/B (camelCase/variable evade, INDEX.json unlocking mc 50).
- Honest scoping (quantifier law): FIRE_LEDGER census this sitting = 2 rows total, both `max_concurrency: 3`, both verdict PASS. The null-width evade surface is EMPTY at this moment; the ledger is younger than the amendment. Shape proven, zero live instances.

### V3. Seal-patrol drifts age out of the ~4h default window and never re-alarm; the live drifts are unsealed post-seal writes. CONFIRMED (counts updated 11 -> 12 at my moment; the ask's 10 is also stale; adjudication now DONE, all 12)

Byte-check: `tools/prepush_seal_patrol.py:55` DEFAULT_WINDOW 150; `:112` `for row in rows[-window:]` builds
`latest` ONLY from windowed rows, so a file whose last seal fell out of the window is not merely unalarmed,
it is unchecked; `:120-135` the compare loop; WARN-ONLY contract in the module docstring `:35-39`.

Executed this sitting:
- `--rows 1000`: 10874 sha rows, 346 distinct, 323 match, 11 missing-on-disk (skipped per a12 law), TWELVE drifted.
- default 150: 56 distinct, ONE drift visible. Eleven of twelve real drifts are invisible at the default window right now: the aging blindness demonstrated live, not inferred.
- Aging rate, my own ledger lines: sha-row 10784 at 12:09:13Z to sha-row 10938 at 16:13:23Z = 154 rows in 4.07h, so the 150-row window expires in roughly 4 hours. Matches the lens's number with my bytes.
- The ask said 10 real drifts, the lens measured 11, I measured 12: the tree moved twice mid-round. The +1 is `watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/break-accuracy.md`, a sibling hostile-pass artifact that was sealed, edited, and then RE-SEALED (register row at ledger line 11145, ts 20:20:23Z) while I was adjudicating it. Counts on this surface are point-in-time by nature; the finding is not.

ADJUDICATION of all 12 (the ask's demanded evidence; full-ledger per-file history dump, my own script, plus
git numstat for tracked files). Classes, zero tampering, zero rollbacks, and NOT ONE of the 12 has any later
ledger row:

| file | last seal (op, ts) | disk mtime | class |
|---|---|---|---|
| watch/inbox/STEALTH_SWEEP_LATEST.md | register 09-26T11:10Z (only seal ever) | 10-05T13:50Z | live queue, 9 days unsealed writes |
| watch/inbox/PACK_OFFLOAD.jsonl | register 10-05T12:09Z (19th seal) | 20:01Z | live queue; git numstat +84/-0 = pure append |
| watch/inbox/STEALTH_MINED_FINDINGS.jsonl | register 10-05T12:09Z (20th seal) | 20:18Z | live queue; git numstat +13/-0 = pure append |
| frontier_olm_2026-10-04/sweep/...-x.md | register 10-04T15:49:53Z | 15:50Z | in-flight edit ~1 min after seal |
| ractor_engine/2026-10-04-eleven-doors/DOORS.jsonl | register 10-04T18:46Z | 10-05T13:05Z | next-day write, never re-sealed |
| frontier_olm_2026-10-04/steal/... via x.md | register 10-05T01:57:49Z | 01:58Z | in-flight edit ~1 min after seal |
| frontier_olm_2026-10-04/RECEIPT.md | register 10-05T06:30:54Z (11th seal) | 06:31Z | sealed 11x that day, final edit unsealed |
| ribvault_20261005/r06_free_probe.py | register 10-05T05:37:49Z | 05:40Z | sealed probe script edited ~2 min post-seal |
| ractor_engine/2026-10-05-ouroboros-r2-gaps/moonshot-1.md | register 10-05T12:03:12Z | 13:22Z | R2 artifact edited ~80 min post-seal |
| frontier_olm_2026-10-05/lens/laws.md | register 10-05T14:13:49Z | 14:15Z | in-flight edit ~90 s post-seal |
| corpus/steal/MASTER_EXECUTE_REGISTER.md | autoseal 10-05T16:13:23Z | 16:36Z | FLAGSHIP: drifted 23 min after autoseal; git shows NO unstaged diff, current bytes == HEAD, so the sealed sha was a pre-final intermediate; direction (append vs rewrite) genuinely unrecoverable from the sha-only ledger |
| .../ouroboros-r3-trust/break-accuracy.md | register 10-05T20:20:23Z | 20:20Z | sealed-edited-resealed DURING this pass (the race, live) |

Corrections/nuance to the lens: (a) its "a sealed probe script whose 'I ran this sha' receipts now vouch for
nonexistent bytes" names r06_free_probe.py; the drift is real and adjudicated, but I did NOT verify that any
receipt actually cites that sha, so the receipts-vouch half stays the lens's claim, not mine. (b) The missing
flip side: drifts also silently HEAL when a writer re-seals (break-accuracy.md did, mid-pass), which is the
sanctioned path; the blindness is that neither direction is ever reported as an event, only as a
window-resident state. (c) The lens's blind-spot "append-vs-rewrite direction is unrecoverable" is TRUE for
untracked inbox files and PARTIALLY FALSE for tracked ones: git numstat recovered direction for both live
queues this sitting; the flagship register's direction stays unrecoverable because the sealed bytes exist
only as a sha.

## LENS BLIND-SPOT DISPOSITIONS

1. citation_lint_numbers.py never read (suspicion OWED): CLOSED BY EXECUTION, and the suspicion was right in
   substance but the laundering is stronger than the lens guessed. See A1.
2. Drift direction unrecoverable: WEAKENED to scoped truth (tracked files recover it via git; untracked and
   sealed-intermediate-vs-committed cases do not).
3. G1-G7 comment-satisfiability probe not fired ("belongs to the sibling lens"): I fired it, it passes ALL
   EIGHT gates. See A2. It no longer belongs to anyone; it is banked.
4. consensus_gate caller census scope: stands as scoped; my own grep over mag/, tools/, main.py (tests
   excluded) finds ZERO live callers, only the module docstring's own example. Note the ask's path is wrong:
   the instrument is `mag/consensus_gate.py`, not `tools/consensus_gate.py`; and `mag/consensus_merge.py`
   was NOT FOUND by two untruncated finds this sitting (the first find, `-name consensus_gate.py -o -name
   consensus_merge.py`, returned exactly one hit). If consensus_merge exists it is not in this tree; the
   ask's cite is unverified and marked OWED to the ask, not asserted absent beyond the scope named.
5. Point-in-time counts: demonstrated three separate ways this sitting (11->12 drifts, ledger growth
   mid-command, a drift that healed mid-adjudication).

## RANKED BLINDNESS TABLE (the ask's required return)

Rank = which blindness corrupts an operator decision first.

| # | instrument | the fooling shape | cheapest probe that proves it | the fix |
|---|---|---|---|---|
| 1 | tools/citation_lint_numbers.py + citation_lint_io.py (PHANTOM-NUMBER engine; same carry shape in mickey17_v2_fold.py:184 `--check-master`) | SUBSTRING and FRAGMENT carry: a number is "carried" if any named source contains its digits ANYWHERE, including inside a DIFFERENT number ("5,000" is carried by a source saying 50,000 via the comma-stripped arm, citation_lint_io.py:299-301; "191.8" is carried by "1191.83" via the raw-substring arm); plus ANY-SOURCE laundering: the attributing source can lack the number while a co-named decoy carries it (citation_lint_numbers.py:226-237, first hit breaks) | 5 min, executed this sitting: probes/break_citation/record2.md names source50k.md (contains "50,000") and claims "5,000 verdicts", source_sub.md (contains "1191.83") and claims "191.8 spent", source_clean.md and claims "3,333 verdicts". Result: numbers checked 3, findings 1; ONLY the nowhere-carried 3,333 fired. The founding 191.8M class has a residual laundering channel | boundary-aware carry: match each form with `(?<![0-9.])FORM(?![0-9.])` in both arms (also after comma-stripping); when the sentence has an attributing source (nearest path before the number), require IT to carry, demote co-named carry to WARN; apply the same boundary regex in fold `--check-master` |
| 2 | tools/workflow_gate.py G1-G8 as a whole (and the seat-law write hook that re-runs it on payload) | TEXT-SATISFIABILITY: every check is a regex over raw script text, comments included; a 10-line comment-only block passes all eight gates with zero warns and mints a PASS row while FIRE_LEDGER logs max_concurrency 99 from a comment | 2 min, executed this sitting: run `run_checks()` on a comment-only string carrying the markers (`// agent("x-" + item)`, `// JSON.stringify(res)`, `// reported these issues`, `// report(part);`, `// artifact.markdown(...) conclusion:`, `// watch/inbox ... observed_at: 2026-10-05`, `// no em-dashes; never fabricate; judge-model: provider/model`, `// max_concurrency: 99`, `// envelope-receipt: watch/inbox/INDEX.json`): failed=[], warned=[], verdict PASS. Confirmation from the environment: the seat-law hook blocked my marker-less .dwf.ts fixtures and would pass them with the markers added | strip comment spans (// lines and /* */ blocks) before matching G1-G7 markers (stamps like envelope-receipt and judge-model stay raw so prose stamps keep working); mint my comment-only fixture as a scenario FOIL card alongside e04's G8 cards; long term, parse the AST instead of regexing text |
| 3 | tools/prepush_seal_patrol.py | WINDOW AGING + no adjudication owner: drift visibility is a pure function of ledger recency (rows[-window:], :112), expires in ~4h at current write rate, never re-alarms, never reports heal events; unsealed post-seal writes are the NORM (12/12 this sitting), so sealed shas in receipts vouch for bytes that no longer exist, including the flagship master fold 23 min after its autoseal | already run at ask scale this sitting: `--rows 1000` (12 drifts) vs default (1 visible), plus the full-ledger per-file dump above; rerun cost ~4 min | add a `--since-ts` mode keyed on seal ts rather than row count; on drift, emit an ADJUDICATION-OWED line naming the file's last-seal ts and writer op so no round ships unadjudicated drifts; optionally persist a drift ledger so aging and healing are events, not states |
| 4 | tools/workflow_gate.py stop-cert (R1 rows 6+7) | STRING-IDENTITY RETIRE PEN: stop-cert keys on exact name, exact path, exact 12-hex digest; rename the file plus any one-character amendment (the amend-not-rewrite norm makes content drift constant) and every key misses; a retired workflow re-certificates as PASS | 3 min, executed this sitting in-memory: with a stops dict mirroring a retired row, `stop_cert_reason('probes/dangerous.dwf.ts','aaa111bbb222',stops)` returns the full block; renamed+edited variant returns '' (no stop). Note: a 1-char edit ALONE stays blocked via name/path keys; the evade needs rename+edit or a new --name | add a normalized-body digest key (hash of the script with comment spans and whitespace stripped) and a title-token key (basename minus -v2/-r3-style suffixes) so cosmetic amendments and renames do not mint fresh identity |
| 5 | tools/prepush_workflow_metadata.py TYPE-DEFAULT | INDENT-KEYED PARSING: ARG_HEADER_RE (:71) matches exactly two spaces, so an args block indented 4 spaces (or tabs) is invisible to the typed-default check; the CR check still sees it, so the file reads "checked" | 2 min, executed this sitting in-memory: identical bad defaults, 2-space block fires TYPE-DEFAULT, 4-space block returns []. Scoped: census of live .zcode/workflows metadata blocks found ZERO 4-space arg headers this moment (shape proven, prevalence zero; drafts dir not censused) | loosen ARG_HEADER_RE to `^[ \t]+(name):[ \t]*$` with indent captured from the args header line and props required to sit deeper |
| 6 | tools/workflow_gate.py FIRE_LEDGER | NULL-WIDTH JOIN FAILURE: symbolic/camelCase widths log `max_concurrency: null`, so the ledger's whole purpose (join fires to width) fails exactly on the evaders; today 2 rows, both mc=3, surface empty | read the ledger and grep for null widths; 1 min | when G8 finds no snake_case declaration but the text matches `maxConcurrency` or a symbolic width, log `"width-unresolved"` with the raw token instead of null; patrol null/unresolved rows as findings |
| 7 | tools/prepush_golden_vector.py (noted, no probe fired, OWED) | TOKEN PRESENCE IS NOT BEHAVIOR: 11/11 tokens can remain present while the win gate they name goes dead behind a changed condition | would need a live campaign run, which the tool's own B2-328 law forbids at push time | operator-side spot rerun on a free lane at intervals, outside the hook |
| 8 | mag/consensus_gate.py (noted, no probe fired) | CALLER-DECLARED TIER: `model_params_b` is an argument, so the CID routing (small-model unanimity -> UNVERIFIED) trusts the caller's stamp; zero live callers exist today (my grep), so the instrument currently guards nothing | grep callers, then call verdict() with params_b=30 on three identical 2B strings | when a caller lands, bind params_b to the dispatching model registry, not the call site |

## R3 DRIVER AMENDMENT (one, round-4 relevant)

Round 4's driver must require every hostile pass to FIRE the instrument it attacks at the ask's scale, and
must assign the adjudication legs a named owner inside the ask itself. This round proved the rule three
times over: the lens read the fold and suspected the join, but only a fired probe produced the
verifier-table-vs-PRISMA divergence and the enum-drop; the ask's own parenthetical ("THE 10 REAL DRIFTS ARE
UNADJUDICATED") arrived after the lens had already run, and the count was stale (10 -> 11 -> 12) before
anyone adjudicated; and the G8 vacuity survived R1 precisely because a card suite re-proved prose while
nobody fired the gate at a hostile payload. Read-only hostile passes are how vacuous trust instruments stay
vacuous across rounds.

## OWED (never asserted)

- Receipts actually citing ribvault r06_free_probe.py's sealed sha: not verified (V3 correction a).
- consensus_merge.py: not found in this tree by two finds; the ask's cite stands unverified.
- Golden-vector behavior probe (table row 7) and consensus_gate fired probe (row 8): not fired this sitting.
- The lens's G8 "unrelated night-shift receipt -> True" variant: not rerun verbatim; my INDEX.json run is
  the same proof shape (an existing file with no width measurement).
- Citations of "42 -> 10" in the ask: the 42->17-real number pair belongs to the r2-gaps B7 lens per
  prepush_seal_patrol.py:126-131; the 10 was already 11 (lens) and 12 (mine) by read time.
