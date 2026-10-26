# OUROBOROS R3 (TRUST INSTRUMENTS) - HOSTILE PASS ON MOONSHOT-2 (2026-10-05T21:22Z)

Break-moonshot-2. Mandate: byte-check every evidence cite, attack every
falsifier, find what the lens missed. Method: re-ran the lens's own probe
runner first (8/8 reproduced at my moment), then re-derived each code cite by
read, then re-censused the universal claims untruncated in the lens's scope,
then probed the instruments the lens itself flagged as unprobed (its blind
spot 3: consensus_gate, cache_kpi, the fold walk, the metadata patrol). Five
new blindness shapes found, all probed live this sitting. No repo file was
modified; every probe ran on temp fixtures. Subprocess law: the only
subprocess-spawning instrument re-run (the lens's probe runner) sets
CREATE_NO_WINDOW itself at probes/moonshot2_probes.py:23; my own probes
spawned no subprocesses.

## VERDICTS

| # | Lens finding | Verdict | Reason (byte-checked this sitting) |
|---|---|---|---|
| 1 | PHANTOM-NUMBER certifies the founding 191.8M phantom (weak int-part form + unit blindness) | CONFIRMED | tools/citation_lint_numbers.py:72 is exactly `forms.append(plain.split(".")[0])`; tools/citation_lint_io.py:277-299 `file_contains` is substring-any over lowered bytes; tools/mickey17_v2_fold.py:126-136 `carried_forms` = {num, plain, expanded} so it lacks the int-part form but shares the unit blindness, exactly as the lens stated. Probe runner re-run by me: 8/8, P1/P2 exit 0 (phantom certified), P3 exit 1 (teeth exist). Founding fixture re-grepped: `grep -c "191" watch/inbox/frontier_olm_20260928/DIGEST.md` = 0, and the tool's own docstring states the same (tools/citation_lint.py:12-13). |
| 2 | FIRE_LEDGER written by the gate, read by nobody; no fire-to-PASS join; amend-after-check fires silently | CONFIRMED (census phrasing corrected, one falsifier direction exercised) | My scoped re-census (`grep -rn -a FIRE_LEDGER tools mag githooks scripts .zcode/workflows tests`) hits ONLY the writer's own source (tools/workflow_gate.py:55,75,503-504) plus its .pyc - the lens's evidence sentence said "only the .pyc matches", which under-reports the writer's own 4 source lines; zero READERS either way, so the finding stands. Extended beyond the lens's scope: dashboard/, configs/, top-level code roots, and the .agents skills tree = zero hits; memory/ holds only journal mentions (memory/trajectory/steps.jsonl). Row counts byte-confirmed at my moment: FIRE_LEDGER 2 rows vs REGISTRY 90 (`wc -l`). PASS mint at :451 and :476-488, fire row at :495-505, stop-cert at :455-462 all read-verified. Falsifier direction run: I re-hashed both FIRE_LEDGER scripts against their certified digests - both MATCH at my moment (ractor-engine.dwf.ts 009c3ea83210, mickey17-burn.dwf.ts 977a8cbb7159), so no live amend-after-check instance exists to point at; the blindness is proven by the zero-consumer census, not by a live evasion. |
| 3 | Scenario-suite all-pass control silently optional; G6-receipts never touches the filesystem | CONFIRMED | tools/workflow_gate.py:408-409 is `control = ...pass_control.dwf.ts` / `if os.path.isfile(control):` with no else branch; the docstring contract "the all-pass control must pass clean" sits at :32-33. G6 lambda at :109-111 is pure substring ("watch/inbox" in t), zero filesystem; G8's isfile at :191 contrast read-verified. Probes P4/P5 re-run by me in the 8/8: exit 0 silent with control deleted, G6 ok=True no soft on a nonexistent receipt. |
| 4 | Credential baseline pardons secrets it never saw (fingerprint = shape+file+head4+len; one finding per line) | CONFIRMED | tools/prepush_credential_shape.py:94-99 fingerprint over name|rel|masked, :102-104 mask = value[:4] + len, :112 `rx.search(line)`. Probe P6 re-run by me (identical fp for different values). The two-keys-one-line claim independently re-derived this sitting: `scan_text('a="sk-abcd1111222233334444" b="sk-abcd9999888877776666"', ...)` = 1 finding, masked `sk-a****(len 23)`. Sharpening the lens missed: the docstring's own claim "editing the value changes the mask and re-opens triage" (:96-97) is FALSE for any edit preserving head-4 + length - the pardon surface is wider than the code comments admit. |
| 5 | Seal-patrol drift channel: 11 perpetual reds, undifferentiated classes; adjudication banked | CONFIRMED at my moment, count drifted 11 -> 12 (moment law, live) | My run: `tools/prepush_seal_patrol.py --rows 1000` = DRIFT, 12 drifted / 342 distinct / 319 match / 11 missing. The 12th is watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/break-accuracy.md - a sibling hostile-pass output minted after the lens's moment: the auditors' own outputs keep entering the drift channel, the recursion the round is named for. Sharpest adjudication row spot-checked and SHARPENED: r2-gaps/moonshot-1.md carries 4 ledger rows (register+autoseal 12:03:12 sha bbcd0453ccf9, then a RE-SEAL 13:16:42 sha a9e5e202ac2a the lens did not report), mtime 13:22:27Z, current sha a345000db1a5 matches NO historical seal, `git status --porcelain` on the file = empty (committed clean). Real divergence, not window or case artifact. |

## WHAT THE LENS MISSED (new blindness shapes, all probed live, ranked by blast radius)

| # | Instrument | Fooling shape | Cheapest probe (ran this sitting) | Fix |
|---|---|---|---|---|
| A1 | tools/cache_kpi.py (the nominal-vs-receipted split, the instrument's whole purpose) | A boolean-only receipt stamp certifies the FULL claimed cache: at tools/cache_kpi.py:182 a row stamped `cache_receipt: {"ok": true}` with NO verified_tokens contributes its entire `cached_tokens` to recv_tok (the else-branch is `cached or 0`, then clamped to the CLAIMED count at :184). Any lane can move its whole nominal cache into the receipt-verified column with a one-field self-stamp; recv_hit% then equals tok_hit% and unreceipted_tok reads 0. This corrupts cache-economics operator decisions (funding, prefix-freeze judgments) first among all my additions. | Ran `compute()` on two rows: deepseek {cached 800, cache_receipt ok:true, no tokens} -> receipt_tok=800, recv_hit=0.8=tok_hit, unreceipted=0; groq control without the stamp -> receipt_tok=0, recv_hit=0.0, unreceipted=800 | ~15 min: the else-branch at :182 becomes 0 (a boolean-only receipt verifies nothing tokenwise); recv_tok counts only numeric verified_tokens clamped to the row's claim; one regression row in the tool's tests. |
| A2 | tools/mickey17_v2_fold.py deep_tier2 walk (the R1 de-blind) | The de-blind moved from lengths to values but the exclusion JOIN is exact-string on a synthetic first-six-words key (deep_keys at :339-342 vs persisted row_key at :327-337): any divergence between the verifier's row_key and the recomputed key (a suffix token, word-order drift, or the claim edited after verification) silently re-INCLUDES the unconfirmed row, and nothing accounts for the orphan verdict - excluded 0, included 2, PRISMA invariant still "HOLDS". The v2 defect class (unconfirmed riding included) is back one string-drift away, and the fold prints no key-miss. | Ran the fold on temp lanes (2-row lane): exact key -> "excluded: 9 verifier-unconfirmed (deep_tier2): 1"; row_key with one suffix token -> "excluded: 0, included: 2"; word-order drift -> same silent inclusion | ~20 min: after the exclusion pass, subtract matched keys from the deep_tier2 key set and print a "deep_tier2 KEY-MISS" line per orphan verdict, failing the fold (or fall back to the legacy claim[:80] match before giving up). |
| A3 | tools/workflow_gate.py stop-cert (R1 row 6) | The retirement key triple (basename, path, content digest at :279-284) dies on rename-plus-one-byte-edit: a clone of a retired script under a new name mints a fresh PASS because every key changed. Sharpens lens finding 2: the stop-cert cannot block what never re-checks, AND it cannot block what re-checks under a cosmetic new identity - "never a silent re-cert" (:509) is bypassable in both directions. | Ran `stop_cert_reason` on a stops dict: original path/digest -> full reason string; renamed + re-digested clone -> "" (clean PASS) | ~25 min: the stopcert index also keys a normalized-content digest (comments and whitespace stripped before hashing) so cosmetic edits cannot mint a new identity; rename-plus-semantic-edit stays an operator-visible event by naming the nearest normalized digest. |
| A4 | mag/consensus_gate.py (the CID-law instrument) | Singleton unanimity is vacuous unanimity: `verdict(["x"], 30)` returns "CONFIRMED" because one response trivially satisfies `len(unique)==1` (:86-95); the `sample_count=3` parameter at :71 is dead code (inspect-verified: never referenced in the body). AND the census says the instrument is unwired: zero source consumers across tools/ mag/ githooks/ scripts/ .zcode/ tests/ (only 2 run-journal payload mentions) - the estate's anti-consensus-illusion law has no enforcement surface, and if wired as-is it would certify single-sample consensus at >=27B. The memweave half handles the singleton honestly (consensus_quality(["x"]) -> verdict "single"), so the two halves of the same law disagree on the singleton state. | Ran: verdict single/2x/3x at 30B all "CONFIRMED"; classify_batch single -> CONFIRMED; memweave.consensus_quality(["x"]) -> {"verdict": "single"} | ~10 min: early-return UNVERIFIED (or a distinct "single" state) when fewer than 2 non-empty responses; delete or enforce sample_count; wire one real caller or mark the module unwired in its docstring so the law stops cosplaying enforcement. |
| A5 | tools/prepush_workflow_metadata.py (the CR + typed-default patrol) | extract_block scans only the FIRST `/* zcode-workflow ... */` block (METADATA_RE.search at :66, :77): a file whose operative metadata block is not the first (an amended workflow appending a fresh header) is unpatrolled - probed: clean first block + second block carrying CR bytes AND a quoted typed default -> findings [], status "block". Corollary in the same presence-class: tools/prepush_golden_vector.py certifies token PRESENCE, not execution - all 11 golden tokens sitting in dead comments yields 11/11 ok (probed via check_text on a comment-only text -> []). WARN-only surfaces, lower blast radius. | Ran scan_file on a temp two-block file -> []; ran check_text on comment-only text -> [] | ~10 min: finditer over ALL metadata blocks and scan each; golden vector optionally requires the win-gate tokens on non-comment lines. |

## Hostile note on the lens's falsifiers

Exercised where cheap: finding 2's converse direction (point at a consumer
outside the grepped roots) - I extended the census to dashboard/, configs/,
top-level, .agents/skills: zero consumers anywhere in-repo, so the scoped
claim survives widening. Finding 2's forward direction (a fired-and-amended
pair) does NOT exist at my moment - both ledger scripts' bytes still match
their digests - which is exactly why the blindness is dangerous: the channel
reads clean today and nothing would name the first future drift. Finding 1's
falsifier (P1/P2 flip to exit 1 post-fix while P3 stays 1) is runnable as
written; I did not run it because no fix has landed.

## R3 DRIVER AMENDMENT (delta on the lens's proposal)

The lens's PROBE SNAPSHOT amendment is right and I confirm its trigger with
live data: the ask arrived saying "10 real drifts" and "86 files" while my
moments read 12 drifts (two sibling moments apart) - the round's own input
was stale on arrival. My delta for R4: (a) the driver banks the snapshot AND
every lens's probe runner must be adversarially RE-RUN by the hostile pass,
not just read - this sitting re-ran moonshot2_probes.py to 8/8, the first
full adversarial re-execution of the pattern, and it held; (b) a banked probe
runner must exit nonzero when an expectation drifts (moonshot2_probes.py:100-106
already does - make that a requirement, not a convention), so a future
instrument change that breaks a banked blindness probe fails loudly instead
of leaving the fold's claims unfalsifiable.

## Checks run this sitting (exact commands, this tree, moment 2026-10-05T21:22Z)

- ./.venv/Scripts/python.exe watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/probes/moonshot2_probes.py -> 8/8 expectations reproduced, exit 0.
- grep -rn -a "FIRE_LEDGER" tools mag githooks scripts .zcode/workflows tests -> writer source + .pyc only; dashboard configs *.py *.md *.json -> zero; .agents -> zero; memory/ -> memory/trajectory/steps.jsonl (journal).
- wc -l memory/workflows/FIRE_LEDGER.jsonl memory/workflows/REGISTRY.jsonl -> 2 / 90.
- sha256[:12] re-hash of .zcode/workflows/ractor-engine.dwf.ts and mickey17-burn.dwf.ts vs ledger digests -> both MATCH.
- grep -c "191" watch/inbox/frontier_olm_20260928/DIGEST.md -> 0.
- scan_text two-keys-one-line -> 1 finding, masked sk-a****(len 23).
- Probe blocks A-E and the fold probe (full commands in this sitting's transcript; all via ./.venv/Scripts/python.exe heredocs on temp fixtures): cache_kpi boolean receipt (800/800 vs 0/0 control), golden vector comment-only ([]), metadata second-block ([]), stop-cert clone (""), consensus_gate singleton (CONFIRMED; sample_count dead by inspect), consensus_quality singleton ("single"), deep_tier2 exact/drift/word-order (excluded 1 vs 0 vs 0).
- ./.venv/Scripts/python.exe tools/prepush_seal_patrol.py --rows 1000 -> DRIFT: 12 drifted / 342 distinct / 319 match / 11 missing.
- Adjudication spot-check on r2-gaps/moonshot-1.md via index_events.jsonl: 4 rows (12:03:12 bbcd0453ccf9 x2, 13:16:42 a9e5e202ac2a x2), mtime 13:22:27Z, current sha a345000db1a5 matches none, git clean.

## OWED (never asserted as fact)

- The full-tree untruncated FIRE_LEDGER grep outside code roots was stopped at ~20 minutes of runtime (corpus/ and .zcode/workflow-runs payload size); the no-consumer claim is scoped to every code root in-repo + dashboard + configs + top level + .agents skills + memory journal check, not to a whole-tree byte scan.
- Which metadata block the workflow facade actually reads (first vs all) is harness-side and unreachable from this dwf-child seat; A5's scope claim is proven patrol-side only.
- The patrol's own exit code at my moment went unmeasured (its stdout was piped through head; the DRIFT class was read from the header line).
- The tier-1/tier-2 verify ceremony inside mickey17-burn.dwf.ts and the other skeletons was not read this sitting; A2's probe covers the fold-side walk only.
