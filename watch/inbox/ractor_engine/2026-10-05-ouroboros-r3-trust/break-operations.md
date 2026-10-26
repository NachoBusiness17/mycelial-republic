# BREAK-OPERATIONS PASS (ouroboros R3 of 5, hostile second pass on the trust-instruments lens)

Moment: 2026-10-05, this sitting. Seat: break-operations. Law compliance: no em-dashes; every claim carries path:line or the exact command and its output; no subprocess was spawned from Python (all probes are pure file ops + module import; CLI checks ran directly in the shell, so the win32 CREATE_NO_WINDOW law is moot here). Instrument state at this moment: gate scenario suite 9/9 green (command `python tools/workflow_gate.py check --scenarios configs/workflow_gate_scenarios`, EXIT=0).

## VERDICTS on the lens's three findings

### F1 gate certifies spellings, not behavior: CONFIRMED (strengthened: incidence measured, and the flagship already rides a sibling shape)

Byte check: tools/workflow_gate.py:83-128 is exactly the CHECKS presence-lambda table (G1 `agent\(\s*"[^"]*"\s*\+` presence at :86, G2 JSON.stringify presence at :90-91, G3 string presence at :95-98, G4 report() presence at :102, G5 string presence at :106, G6 "watch/inbox" substring at :111, G7 substring at :115-116). :176 `G8_MAX_CONCURRENCY_RE = re.compile(r"max_concurrency\s*[:=]\s*(\d+)")` is digit-only. :189-192 `g8_width_shape_ok` accepts any `envelope-receipt:` path that merely `os.path.isfile`s under watch/inbox. run_checks consumes the whole script text including comments (main reads at :445-452, no comment stripping anywhere).

Execution (re-run this sitting, not borrowed): `python tools/workflow_gate.py check --script <f> --no-register` on three fixtures I wrote myself under probes/break/:
- g8_width_var.dwf.ts (width 50 via `const WIDTH = 50; max_concurrency: WIDTH`): PASS, exit 0, all 8 gates ok.
- g8_stamp_content_free.dwf.ts (max_concurrency 50, `envelope-receipt: watch/inbox/INDEX.json`, a file with no measured envelope): PASS, exit 0, all 8 ok.
- comment_only_body.dwf.ts (comment-carried G1-G7 strings, no dispatch, no width): PASS, exit 0, all 8 ok.

CONVERGENT claim verified: probes/g8_vacuous_envelope.dwf.ts exists and is sealed at watch/inbox/index_events.jsonl lines 11019-11020, ts 2026-10-05T18:23:52Z, writer md-record-seal, sha 661e5b31... matching the lens's cite.

Incidence (the lens's falsifier branch, executed): sweep of 20 saved + 73 draft .dwf.ts (probes/break/sweep_live_workflows.py): ZERO files use a variable RHS on max_concurrency; ZERO files lean on comment text for any gate (comment-stripped rerun of run_checks flipped nothing). But the census grammar is too narrow, see A1: mickey17-burn.dwf.ts:48 carries `// max_concurrency: 3 (... declaration stamp, the firer still sets it at run time ...)` while :179 reads `const WIDTH = typeof args.width === "number" ? args.width : 50;` and :426-427 dispatch `Promise.all` over all lanes at once. The estate's own burn engine passes G8 on a comment and fires arg-driven width the regex cannot see, because the token "max_concurrency" never appears next to the live expression. So "latent" is the wrong downgrade: the blind shape is in production on the highest-traffic instrument, self-disclosed in the comment.

### F2 seal channel advisory in both directions: CONFIRMED (numbers moment-corrected; cure mechanism corrected)

Byte check: tools/prepush_seal_patrol.py:111-116 builds the latest-seal map straight from row values (keys file+sha256 only, parse_ledger :91); :55 DEFAULT_WINDOW=150; :132 `if actual == sha.lower():` (the case fix, holds); githooks/pre-push:487-516, the seal_patrol block only echoes, "this block NEVER exits nonzero" at :499-500, TODO-FLIP-TO-ENFORCE at :501-502.

Execution (re-run this sitting):
- Default window: `python tools/prepush_seal_patrol.py` printed "SEAL-PATROL: ok ... 54 match, 3 missing" EXIT=0. At THIS moment the push channel reports clean.
- `--rows 1000`: DRIFT, 11 files (323 match, 11 missing skipped). The lens's 3/12 are now 0/11: moment-bound counts confirmed exactly as their blind spot 5 warned. The class is stronger at my moment: an operator pushing now sees ok while 11 wide-window drifts exist.
- Forged-append probe (probes/break/forge_reseal.py, temp ledger copy): before forge drifted=11 of 346; appended 11 autoseal-shaped rows carrying current-byte shas; after forge drifted=1. All 11 forged files' drift erased; verdict would be ok except one residual, corpus/steal/MASTER_EXECUTE_REGISTER.md, whose forged row I wrote as a bare-relative path, which resolve_sealed_path maps under watch/inbox (:73-75), so the phantom path row never reached the real file (my path-shape error, not a patrol defense; the real file's absolute-form row stayed latest). The lens's "12 to 0" exact figure is not reproducible at this moment; the mechanism (forged rows override the latest-seal map, no writer identity, nonce, or chain checked, :91 and :111-116) reproduced 10-for-10 with the 11th erasable by using the ledger's own absolute form.
- Drift adjudication re-censused (current 11): every file's mtime is AFTER its last seal ts (no tampering signature, none precede a seal). 3 are register-class rows sealed by writer=drift-patrol-cron at 12:09Z and written by live boards through 19:57Z (STEALTH_SWEEP_LATEST.md, PACK_OFFLOAD.jsonl, STEALTH_MINED_FINDINGS.jsonl); 8 are autoseal rows (NO writer field; keys are bytes/file/op/purpose/sha256/ts) with mtimes 22 seconds to ~19 hours post-seal. Verdict: expected writer traffic, consistent with the lens's 12-of-12 call.
- R2 closure row 8 rerun falsifier: zero case-only false drifts in both my runs (the :132 fix holds).

Cure mechanism CORRECTED (lens blind spot 4, now read): tools/md_record_seal.py:177-186 is a tool-hook writer; its dedupe is same-path-same-BYTES only, so appends the hook SEES do get re-sealed. The under-re-seal population is writes that never pass through the harness Write/Edit tools (cron boards, lane processes writing directly). "Re-seal-on-append in the writer" fixes nothing for them; the fix is patrol-side adjudication by writer class, or those writers minting their own seals. Chain material exists only on register rows (writer/nonce/seq, md_record_seal.py:212-218); autoseal rows carry none, so the lens's proposed digest-chain can only bind register rows today.

### F3 fold re-blinded three ways: CONFIRMED (one vocabulary nuance; plus a fourth blindness the lens missed, see A3)

Byte check: tools/mickey17_v2_fold.py:334-337 `if verdict == "unconfirmed":` / `elif verdict == "crashed":` (exact lowercase, twice); :339-342 deep_keys joins only the two six-word forms `lid + ": " + first-six-claim-words`. Producer recipe mickey17-burn.dwf.ts:352 (six words via single-space split).

Execution (probes/break/fold_probe.py, RUN_ROOT redirected to a temp archive, two runs):
- Run 1 (all row_keys FIVE words, honest lowercase verdicts): `included=3 excluded=0`. Every negative verdict rode included on join miss. Matches the lens exactly.
- Run 2 (correct six-word keys; verdicts "Unconfirmed", "crashed", "refuted"): `included=2 excluded=1`. Only lowercase crashed excluded; capital-C Unconfirmed and out-of-vocabulary refuted rode included. Matches the lens exactly.

Vocabulary nuance the lens omitted: all three skeletons DO declare the four-value enum `verdict: "verified" | "unconfirmed" | "crashed" | "same-chain-verified"` (mickey17-burn.dwf.ts:99, mickey17-v2.dwf.ts:59, workflow-drafts/execute-register.dwf.ts:52). Out-of-vocabulary values require the tier-2 agent to violate the typed contract (runtime JSON is never mechanically validated) or a hand-edit to checks.json. This weakens casual occurrence, not the shape: case drift and join drift are proven, and nothing reconciles the split.

## ADDITIONS (what the lens missed), ranked by blast radius

### A1 (rank 1) FIRE_LEDGER width join records a comment stamp while the real width rides a runtime arg

Evidence: memory/workflows/FIRE_LEDGER.jsonl row 2026-10-05T17:52:58Z mickey17-burn.dwf.ts PASS width=3; the 3 comes from the COMMENT at mickey17-burn.dwf.ts:48 ("declaration stamp, the firer still sets it at run time"); the live width is :179 `const WIDTH = typeof args.width === "number" ? args.width : 50;` and the dispatch is :426-427 Promise.all over the whole lane table. The R1 row-7 instrument was built to make width-less journal fires joinable; it joins a prose token instead of the fired shape. An operator reading the ledger sees 3 for a 50-lane engine. Same stamp at ractor-engine.dwf.ts:39 (its ledger row 18:50:37Z also width=3). This is the fold lesson (counters that walk lengths not values) reborn in the week's newest instrument, on the estate's ONE parameterized burn engine.
Falsifier: read the harness run journal for an actual mickey17-burn fire; if real child concurrency measured <= 3, the stamp is honest and this downgrades to a join-hygiene finding (token recorded where shape was meant).
Move: 45 min. FIRE_LEDGER records the fired shape: lane-table length and the width-arg default parsed from the args block (parse_declared_args already exists at workflow_gate.py:294-313); G8 grows a check that a `width` arg with non-3 default counts as a declared width (the args door), so the flagship either declares 50 plus an envelope receipt or fails.

### A2 (rank 2) the tier-2 crash fallback is structurally unjoinable, so producer-side crashes never exclude rows in the fold

Evidence: mickey17-burn.dwf.ts:454 and mickey17-v2.dwf.ts:263 `c = { row_key: x.lane + ": crashed", verdict: "crashed", ... }` on agent exception; the fold's deep_keys (:339-342) only ever builds six-claim-word keys, which `lid + ": crashed"` can never equal, so `keys & deep_crashed` is empty and the row rides INCLUDED. The tier-1 crash fallback (mickey17-burn.dwf.ts:418) writes counts {crashed: N}, a key the fold never reads. Net: every tier-2 agent exception is invisible to the counting gate it feeds. Third split: the runner's own report counts unconfirmed by BLACKLIST (mickey17-burn.dwf.ts:589 `verdict !== "verified" && verdict !== "same-chain-verified"`), the fold by whitelist of two exact strings, so the two trust surfaces disagree on any case-drifted verdict; that is the unreconciled split the lens observed but did not localize.
Falsifier: a real run archive containing a fallback row_key ("<lane>: crashed") whose claim row lands in excluded; none exists by construction of deep_keys.
Move: 30 min. Fallback writes row_key from the claim's first six words (same recipe as deepAsk); the fold excludes on `lid + ": crashed"` fallback keys too, or better, joins on (lane, claim-prefix) with the verdict carried rather than re-derived.

### A3 (rank 3) the scenario suite validates the gate's card grammar, not forged payloads

Evidence: suite green 9/9 this sitting (command above); the nine cards are seven honest FAIL fixtures plus the G8 pair. No card exercises a comment-only body, a variable/arg width, or a content-free envelope stamp, the exact shapes proven to pass in F1. The suite's green is being read as the gate re-proven; it proves only that honest-failure detection still works. The LAW-12 minting rule (cards must cite real registry FAIL rows, workflow_gate.py:331-342) structurally excludes forged-payload cards until a fixed gate actually fails them, so the suite can never lead the gate, only follow it.
Falsifier: a forged-payload card passing validation today, which would require a registry FAIL row showing e.g. comment-only body failing, which cannot exist while the gate passes it.
Move: 20 min. Land F1's fix first, then mint the three probes/break/ fixtures as regression cards citing their new FAIL rows; until then the suite header should say what it proves (FAIL-shape detection) and not "gate proven".

### A4 (rank 4) stop-cert is doubly vacuous today: the pen has never been minted, and its keys evade on rename or one byte

Evidence: memory/workflows/REGISTRY.jsonl has 90 rows and ZERO carry a "status" field (grep -c "\"status\"" returns 0), so load_stopcert_index (workflow_gate.py:244-270) returns empty sets and BLOCKED-STOPCERT cannot fire on anything in the ledger. When a status row does land, stop_cert_reason keys on basename, script path, and digest (:276-284): a renamed copy evades name and path, any single-byte edit evades digest. The R1 row-6 tooth is untested against anything real and untestable by evasion-resistance design.
Falsifier: mint one status row against a scratch script (operator action) and show a renamed, one-byte-edited copy still PASSes; that executed probe would convert this from reasoned to proven (OWED: needs an operator-minted row, I may not write registry status rows from a break pass).
Move: 15 min. Document the vacuity in the gate docstring; when first minted, key stop-certs on an operator-signed list (name + last-known-good digest with explicit operator re-sign on amend), not on mutable identity triplets.

### A5 (rank 5, minor, surfaced by my own forge error) relative ledger rows for estate files outside watch/inbox resolve to phantom paths

Evidence: resolve_sealed_path maps any bare-relative row to root/"watch/inbox"/p (prepush_seal_patrol.py:73-75); my forged row "corpus/steal/MASTER_EXECUTE_REGISTER.md" therefore addressed watch/inbox/corpus/... (nonexistent, counted missing-on-disk, never a finding) while the file's real absolute-form rows kept it visible. A future ledger writer emitting relative rows for outside-inbox estate files would drift invisibly.
Falsifier: a relative-form row for an outside-inbox file that the patrol still adjudicates (cannot happen by :73-75 construction).
Move: 10 min. resolve_sealed_path flags relative rows whose mapped path does not exist while a same-name file exists under root outside watch/inbox; or ledger writers standardize on absolute or inbox-relative only.

## Amendment owed to the R3/R4 driver

The lens's falsifier grammar for F1 ("a tree-wide census of saved .dwf.ts files showing zero non-literal width declarations ... would downgrade this from exploitable to latent") is itself a blind instrument: my census returned exactly that zero while mickey17-burn sits in the blind shape through the args door plus comment stamp, because the census regex looked only at tokens named max_concurrency. Round-4 driver amendment: any incidence census must enumerate the fooling shape's whole family (token RHS, arg-driven width defaults, comment stamps, absence-as-pass) and name each branch it counted, or the census reads clean over exercised blindness. Same law as the QUANTIFIER LAW, applied to incidence: scope named in the claim, absence named per instrument.

## Blind-spot ledger (the lens's own six)

BS1 incidence unmeasured: NOW MEASURED (sweep above; zero variable-RHS, zero comment-carried gates, 68 of 93 files declare no width token at all, flagship rides args+stamp). BS2 stop-cert unexecuted: CONFIRMED vacuous (zero status rows). BS3 ceremony censused not audited: extended this sitting to mickey17-v2.dwf.ts and workflow-drafts/execute-register.dwf.ts (same enum, recipe, fallback). BS4 writer unread: READ (md_record_seal.py; re-seal-on-append exists for hook-seen writes, gap is non-hook writers). BS5 moment-bound: PROVEN by rerun (3/12 became 0/11 within hours). BS6 Docker /board/inbox cross-surface: STILL OWED, not inspected this sitting; the patrol skips other-surface absolute paths by design (prepush_seal_patrol.py:59-75).

## Probe artifacts (all under watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/probes/break/)

g8_width_var.dwf.ts, g8_stamp_content_free.dwf.ts, comment_only_body.dwf.ts (gate fixtures, all PASS today, to become scenario cards post-fix); forge_reseal.py (forged-append probe, temp ledger only, real ledger untouched); fold_probe.py (fold runs 1 and 2, temp archive only); sweep_live_workflows.py (incidence census). The real seal ledger and registry were never written by this pass (gate runs used --no-register).
