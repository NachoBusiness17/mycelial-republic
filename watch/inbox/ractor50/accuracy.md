# ractor50 accuracy retro: verdicts later corrected, mined for the instrument shape that produced them

**Lane:** accuracy (division B) · **Date:** 2026-09-30 · **Receipt:** watch/inbox/ractor50/accuracy.md
**Sources mined this session:** 213 gala lane JSONs under watch/inbox/gala_20260925/*/lanes/ (48h-synthesis 16, afterparty 197, ball-20260929 26, ball3-suite-green 8, ball4-luncheon-follow 24, gala-rung0 4, w1 22, w2 26, w3 65, wave5-repair 50), 496 files under watch/inbox/burn_reset_20260927/flash50/, memory/workflows/REGISTRY.jsonl (45 rows), memory/burns/LEDGER.jsonl (erratum rows read directly), watch/inbox/burn_wave_20260926/ (B2_01, B2_14, B2_16), watch/inbox/frontier_olm_20260928/ and frontier_olm_2026-09-30/.

Method: every incident below carries a verbatim quote byte-copied from an estate file (each verified against its source by the finish-line check in accuracy.check.txt), the lane of origin, a named defect class, the falsifier that would have fired earlier, and an instrument upgrade stated as a mechanism change (who runs what, when). No code under mag/ or tools/ was touched by this lane, so the conditional ratchet step does not fire.

## Pattern classes found (the retro's yield)

| class | instrument shape that produced the wrong verdict | what catches it |
|---|---|---|
| ok:true-equals-landed | transport success treated as content verification | citation-resolution gate at landing |
| unreceipted premise dispatch | a triage verdict issued without the receipt that named the failing items | pinned failing node IDs from a named receipt before dispatch |
| moment-verdict overwritten in place | counts/folds rewritten on the same untracked path | versioned fold files + supersession byte census |
| harness-attribution error | probe failure reported as target failure | probe-vs-target separation rule on every "dead/broken" adjective |
| memory-written citations | doctrine citations written from dig memory | citation linter (path exists, line range non-empty) at filing |
| hand-copied count | a number copied from a prior doc, not from the instrument | census re-run from the instrument + drift patrol |
| race-written numbers | board numbers quoted from a stale tail read | re-read board-highest after append, auto-emit correction row |
| destructive renumber | repair script with prefix filter on a shared append-only surface | before/after line-count reconciliation in the same process |
| dispatch-premise drift | an ask carries a defect claim that a named line already disproves | read-the-named-line-first gate on defect-fix asks |
| display truncation without dedupe | head -cap over duplicated instrument output hides real findings | unique-vs-shown count line on every capped display |
| double-landing | one receipt at two paths | bank-level sha256 duplicate scan before drift-patrol commit |
| state-doc verdict decay | a recorded verdict kept as truth after the world moved | scheduled re-run of the verifying instrument, doc refreshed from run output |

## Incident 1: UF-124/125/126 fabricated citations ruled LANDED, corrected to STILL-OWED

**Verbatim:** "UF-124, UF-125, UF-126 rows landed but their answers are fabricated (placeholder and misattributed citations), so those three gaps are STILL-OWED, not closed." (watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md:5) and "UF-124 answer (DAY_PACK.md:2056): ... (https://openreview.net/forum?id=XYZ) is a literal placeholder id; ... misattributes Anthropic's paper; effect sizes unverifiable." (:12)

**Lane of origin:** the free-lane dig seats that landed the 2026-09-18 gapwave answers (DAY_PACK.md:2056 carries the fabricated text); corrected by the B2-16 UF status sweep lane (burn_wave_20260926).

**Defect class:** ok:true-equals-landed. The rows' transport succeeded, so they counted as closed; the citation content was never resolved. A free-lane sensing answer shipped placeholder-shaped citations (openreview id=XYZ, arxiv 2407.12345) that no fetch ever returned bytes for. deep-swarm-thermodynamics.md:34 names the cost: "catching it cost a full byte-check sweep that rejected 4 of 8 UF-119 attacks against real tools/corpus.py line numbers. Unsorted, this would have entered the corpus as poison."

**Falsifier that would have fired:** the sweep's own, at landing time instead of eight days later: "Invert by resolving one named citation from any of the three answers, e.g. openreview forum id=XYZ or arxiv 2407.12345, and quoting the effect size it claims." (B2_16:25)

**Instrument upgrade (who runs what, when):** the ledger append path (the script that writes a LANDED row to memory/burns/LEDGER.jsonl) runs a citation resolver before accepting verdict=LANDED on any row whose one_line or landing contains an external URL/arxiv id/openreview id: each id must resolve to fetched bytes in the same session, else the row lands as UNVERIFIED, never LANDED. Free stealth lanes bank findings, never trusted work; verification climbs to the funded tier (the standing driving-ladder law applied to verdicts).

## Incident 2: quantizer-fallout triage premise killed by ball3

**Verbatim:** "no 42:05 suite receipt exists to name that snapshot's failure modes" and "all nine named tests were already healed by the quantizer-hygiene lane's own commit 93f85e0dd ... the other five named files never encoded pack shapes" (watch/inbox/gala_20260925/ball3-suite-green/lanes/quantizer-fallout.json note). The suite's two REAL failures "belonged to sibling lanes" (game-world grove optics; the stealth_driver instance-lock test contending the LIVE production mutex).

**Lane of origin:** the post-ball dispatch (a 42:05 post-ball suite observation turned into a "9 downstream tests encode stale expectations" triage) sent to ball3-suite-green; corrected by the ball3 quantizer-fallout lane, which byte-verified and edited nothing.

**Defect class:** unreceipted premise dispatch. The dispatch claimed N downstream failures without citing the suite receipt that named the failing node IDs; the alleged failures did not exist at HEAD (healed atomically in-commit), and the real failures routed elsewhere.

**Falsifier that would have fired:** reading the receipt lines first: "A fallout lane that finds all nine green AND a cited 42:05 receipt showing those node IDs red would kill this law (meaning the tree regressed between snapshot and lane)." (quantizer-fallout.json, fallout-premise-needs-a-receipt falsifier)

**Instrument upgrade (who runs what, when):** the orchestrator greps the suite receipt for the failing node IDs and pins them into the ask BEFORE dispatching any fallout-fix lane; the receiving lane refuses (one seat, one sitting) any ask that claims failing tests without pinned node IDs traceable to a named receipt. Landed pattern that prevents the recurrence: any tools/ behavior bump renames the status marker AND its test assertion in one commit (93f85e0dd did exactly this; the stale-marker grep at HEAD returns zero hits).

## Incident 3: OLM 18-lane fold stale by the 32-return fold; predecessor unrecoverable

**Verbatim:** "The predecessor folded an 18-lane / 23-find / 9-card confirmation state; the current fold holds the 32-return" and "The four fold outputs are untracked in git with no committed history, so the predecessor text is not recoverable; its headline counts survive here and in DIGEST.md's pass-over delta note." (watch/inbox/frontier_olm_20260928/RECEIPT.md, Supersession section). Same receipt, the missing-file disagreement: "os.path.exists on this path returned True and the on-disk file measured 26347 B ... so the operator's surface and this seat disagreed; both facts are recorded."

**Lane of origin:** the frontier_olm_20260928 fold lane itself (second pass, rewritten 2026-09-29 per operator instruction after the missing-file report).

**Defect class:** moment-verdict overwritten in place. The 18-fold's counts were true at its moment and stale by the 32-fold's moment; overwriting the same untracked path destroyed the predecessor's evidence trail, leaving only headline counts. The register carried the honest residue: rows 1 and 18 hold post-confirmation corrections ("Vals #1-open leg refuted at probe 2026-09-29" and the PolAgentBench CC0 attribution FALSE, repo README says MIT code, CC BY 4.0 release data).

**Falsifier that would have fired:** B2-216's denominator law applied at consumption: any consumer who differenced the 18-fold against the 32-fold without naming the moment produces a phantom regression. The receipt's own discipline (write-time byte measurement of the predecessor before overwrite) is the falsifier firing late.

**Instrument upgrade (who runs what, when):** every fold pass writes a versioned path (DIGEST-<pass>.md, RECEIPT-<pass>.md) or commits the predecessor before overwrite; the fold lane's close step runs the byte walk (os.walk + getsize, never bare python) over predecessor and successor and records both headline sets in the supersession section. The fold's counts carry a moment stamp next to every headline number.

## Incident 4: arch-03 ruled "selffeed is dead in situ"; the cause was the probe's own harness riding a wedged cua-driver pipe

**Verbatim:** "D2 selffeed is dead in situ: 9/9 ERR." (watch/inbox/burn_reset_20260927/flash50/arch-03.md:34, the ERR itself being "ERR selffeed: rc=1 The system cannot find the file specified.") Corrected by the wave5-repair stealth-tools lane: "selffeed rc=1 was a misresolved seat python riding a wedged cua-driver pipe" with mechanism "The driver spawned its own interpreter as 'Hermes' (sys.executable), which no-ops silently or hits the documented stale-daemon pipe error" (watch/inbox/gala_20260925/wave5-repair/lanes/stealth-tools.json), proven by "selffeed real output m7 in 42s" after the fix.

**Lane of origin:** arch-03 (flash50 anti-fragility instrument lane, 2026-09-28); corrected by wave5-repair stealth-tools.

**Defect class:** harness-attribution error / unconfirmed mechanism. The observation (9/9 rc=1) was true; the causal verdict ("dead in situ") was not confirmed, and arch-03's own receipt carried the un-fired counter-evidence: "Two selffed rows (m1, m002) prove it worked at least twice earlier under a different invocation context" (:34). The failure lived in the probe's invocation path (interpreter resolution plus the cua-driver pipe), not in selffeed.

**Falsifier that would have fired:** one re-run of t_selffeed with the resolved seat interpreter before publishing the "dead" verdict; stealth-tools' m7 run in 42s is exactly that falsifier, executed one wave later.

**Instrument upgrade (who runs what, when):** any instrument lane writing a dead/broken/broken-in-situ verdict about a target must first run the target once through the probe's own invocation path with a resolved interpreter and name that check in the receipt (probe-vs-target separation); the fix comment carries the receipt per the build-discipline law. Owner: the instrument lane author, at receipt write time, before the LEDGER row.

## Incident 5: f-25 found 3 citation defects in the operating playbook, and the corrections were never folded back

**Verbatim:** "3 citation defects: law 4 imprecise (real predicate `dynamic-workflow-run-observation.ts:564-566`), law 6 wrong path (file is `core/src/compact/policy.ts`, not `runtime/compact/`), law 8 had no citation (supplied: `core/src/tool/handlers/bash.ts:70`, cap is 30,000 bytes not 30 KiB)." (watch/inbox/burn_reset_20260927/flash50/f-25.md, answer 1)

**Verified at HEAD this session:** corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md:29 still reads `core/src/runtime/compact/policy.ts:6-14` (the wrong path f-25 named), and law 8 still carries no citation while saying "30KB". The audit's corrections live only in the receipt; the doctrine file the estate actually loads still carries the defects. This is the second-order accuracy failure: a correction banked is not a correction applied.

**Lane of origin:** the original deep dig (ZCODE_ENGINE_DIG_20260925, header claims "15/15 paths fact-checked") wrote the playbook citations; f-25's playbook audit (flash50, 2026-09-28) found the defects. Note I did not re-verify the correct path against the ZCode clone (no clone under Documents/projects this session); the path-truth is f-25's own byte-check claim, quoted as such.

**Defect class:** memory-written citations. Citations written from dig memory at doctrine-authoring time, never byte-checked against the named file at the granularity claimed (path wrong, predicate imprecise, one missing entirely). The wrong citation still "works" on read because nothing ever resolves it.

**Falsifier that would have fired:** the check f-25 ran: open the named file, read the named lines. Any single resolution pass over the 13 laws catches all three defects.

**Instrument upgrade (who runs what, when):** a citation linter runs at filing time (the same lane, before the LEDGER row): every file:line citation in a doctrine/receipt under corpus/steal/ must satisfy (a) the path exists, (b) the line range is non-empty and mentions a token from the claim. Fail = fix the citation or downgrade the claim before landing. Owner: the filing lane; the existing freshness/ratchet pattern is the carrier (a tools/citation_lint.py wired into the pre-push hook would make it machine-enforced).

## Incident 6: the 1,341 census headline: hand-copied, never byte-backed, rode 12 days

**Verbatim:** "T44 line 40: "34 failed / 1305 passed / 9 skipped" sums to 1,348, not 1,341." (watch/inbox/burn_wave_20260926/B2_01_the50_punch_20260926.md:18) and the retirement clause now in AGENTS.md: "the retired "1,341 tests / 264 files" headline was hand-copied, never byte-backed."

**Lane of origin:** the 09-14 carrier that hand-copied the count into durable docs (and audit_dungeon.v1.json:147, which recited it as live truth); corrected by T44 (B2-01) and B2-214 (dungeon census re-landed with the 2026-09-26 instrument census and the old count kept as a labeled exhibit).

**Defect class:** hand-copied count. A report-of-a-report number: no instrument ran at copy time; the arithmetic check alone (1305+34+9=1,348) kills it, and 12 days of tree growth ran with no gate watching.

**Falsifier that would have fired:** the sum check, at any point in those 12 days; and B2-215's drift tripwire the day it existed.

**Instrument upgrade (who runs what, when):** already landed as mechanisms, recorded here as the standard: tools/census_drift_patrol.py (B2-215) parses the carrier claim's counts and census date and flags >7d staleness while tests/ grows; the B2-244 --collect deep check reruns pytest --collect-only -q itself and fails exit 1 when the claim is 20+ off byte truth either direction; MagCensusPatrolDaily runs it at 08:30 (scripts/census_patrol_daily.ps1). Standing rule the incidents teach: a count in a durable doc must be re-run from the named instrument, never copied.

## Incident 7: self-feed numbering errata: concurrent board writes made the claimed numbers false (four erratum rows in one window)

**Verbatim:** "the three briefs were first appended as B2-441 to B2-443 but the concurrent B2-98 self-feed landed its own B2-441 to B2-443 rows above them mid-close; they stand as B2-444, B2-445, B2-446 per the B2-167 highest+1 renumber law" (memory/burns/LEDGER.jsonl line 240, B2-94-self-feed-numbering-erratum) and "the prior row said 429-431 from a stale board tail read before the landing" (line 234, B2-96-self-feed-numbering-erratum). Same class at B2-383 (claimed B2-410/411, landed as B2-417/418, line 220) and B2-374 (417/418 to 419/420, line 223).

**Lane of origin:** B2-94, B2-96, B2-374, B2-383 lanes (burn_wave_20260926); the errata were filed by the same lanes at close. deep-swarm-thermodynamics.md:35 counts the class: "The LEDGER carries 26 errata/correction rows of 693 total, including 4 explicit self-feed numbering erratum rows ... caused by concurrent board writes racing."

**Defect class:** race-written numbers. A verdict quoting board numbers derived from a tail read that another lane invalidated between read and append. The verdict's content was otherwise true; its identifiers were false, and downstream consumers citing those identifiers would chase ghosts.

**Falsifier that would have fired:** re-reading the board tail after append, in the same close; the discrepancy surfaces immediately instead of as an erratum row.

**Instrument upgrade (who runs what, when):** the queue landing script (the close step) re-reads board-highest AFTER its append and, when the appended numbers do not match the post-append truth, emits the correction row automatically in the B2-167 shape instead of leaving it to lane honesty. Owner: the close step of every lane that self-feeds briefs; every close, not on discovery.

## Incident 8: B2-53 prefix-filter deletion: a repair script destroyed six concurrent-lane lines, two unrecoverable

**Verbatim:** "during the first renumbering, a startswith prefix filter deleted six pre-existing concurrent-lane lines claiming B2-125/126/127; four restored verbatim from the owning lanes own scripts (B2_52_ledger_queue.py:22-24, B2_37_ledger_queue.py:43-47), two further deleted lines unrecoverable from any on-disk source and filed as owed in the QUEUE restoration note" (memory/burns/LEDGER.jsonl line 90, b2-53-queue-number-correction).

**Lane of origin:** B2-53 queue repair (burn_wave_20260926); the correction is its own.

**Defect class:** destructive renumber. A repair script ran prefix matching over a shared append-only surface and deleted foreign rows. This is the accuracy failure that destroys evidence rather than just misstating it: two lines are gone from every surface.

**Falsifier that would have fired:** a before/after line-count reconciliation in the same process: six missing lines is an instant refusal, before the write commits.

**Instrument upgrade (who runs what, when):** any script that rewrites QUEUE.md/LEDGER.jsonl (rather than appending) must count lines before and after and refuse to commit any negative delta that its own diff does not name. Owner: the repair script author; enforced by the same-process reconciliation, and the queue-closes lane's _qc rebuild passes (six passes, "invisible 0 stable across all 6 passes", watch/inbox/gala_20260925/wave5-repair/lanes/queue-closes.json) are the successor instrument running today.

## Incident 9: afterparty t30: false premise "souls table type any", and the gate's display was hiding real findings

**Verbatim:** "Negative finding first: the item premise 'souls table type any' is false. Line 16 was already { [string]: Soul.Soul }, committed; t1d verified it proper and the 16,26 TypeError was the gate's repo-root analyze phantom that t24 fixed." and "the gate display block piped the filtered stream straight to head -20 while luau-lsp dual-path reporting doubled every finding (62 filtered lines = 47 absolute-form + 15 relative-form copies of 20 unique locations on t24's own raw buffer), hiding HardwarePrimerZone(10,7), IncidentDungeonZone(12,7), LightmapRoomsZone(17,7), RiddleMazeZone(20,7), SpectralMazeZone(69,7)." (watch/inbox/gala_20260925/afterparty/lanes/t30.json note)

**Lane of origin:** the earlier lane whose reading produced the dispatch premise (t1d's residual-any naming, corrected by t30); the display defect is the gate's own.

**Defect class:** dispatch-premise drift plus display truncation without dedupe. Two distinct accuracy failures in one lane: (a) an ask carried a defect claim that reading the named line at HEAD disproves in seconds; (b) the gate's own display capped duplicated output, so five real findings were invisible to every consumer of that display.

**Falsifier that would have fired:** (a) read line 16 before writing the ask; (b) count unique locations before the cap: 20 unique shown as 62 lines means duplicates eat slots.

**Instrument upgrade (who runs what, when):** (a) a defect-fix ask must carry the named line's current bytes or the receiving lane reads them first and files a premise correction (t30's note is the model; it is already a filed receipt). (b) t30's fix is the standard: dedupe pass keying unique basename(line,col) before the cap, a "unique findings: N" count line, cap 20 to 40; generalized: every capped display reports unique-count vs shown-count so hiding is visible. Owner: the gate display maintainer for (b), the dispatching lane for (a).

## Incident 10: w4-20 landed twice under two names (byte-verified this session)

**Verbatim (my own run this session):** w4-20.md and w4-singularity.md both sha256 f873a43aaf1d241f, 18,212 bytes, identical: True (both committed in 1ba61713d). The wave5-repair QC pass validated only the w4-20 path (_qc_validate_final.json entry "burn_reset_20260927/flash50/w4-20.md", exists true).

**Lane of origin:** the flash50 w4-20 gopher (the receipt banked twice, under the item name and the topic name); the drift-patrol commit 1ba61713d carried both.

**Defect class:** double-landing. One receipt at two paths: citation graphs fork (w4-29.md cites the w4-singularity.md path while QC validates the w4-20.md path), and a future edit to one copy forks the truth.

**Falsifier that would have fired:** a sha256 scan across the bank; the two identical hashes are the finding.

**Instrument upgrade (who runs what, when):** the flash50 census/QC pass (whatever lane next walks the bank) computes sha256 across all receipts and flags byte-identical pairs before the next drift-patrol commit; one path becomes canonical, the other becomes a stub pointer naming the canonical path. Owner: the next bank-walking lane; the drift-patrol is the natural carrier.

## Incident 11: state/CURRENT.md seed-seal verdict stale: the recorded drift member was no longer the drifted member

**Verbatim:** "So the drift has MOVED since the 09-26 record: the previously drifted member (TRUST_BYTES_LAW.md) was cured or re-sealed, the manifest grew a row (56 to 57), and a different member (engines/key_law.py) drifted since." and "The seal and the bytes it seals disagree inside a single commit, on a clean tree." (watch/inbox/burn_reset_20260927/flash50/w4-20.md, section 2, commands run that session)

**Lane of origin:** the 09-26 seed audit recorded the verdict in state/CURRENT.md; the w4-20 gopher's live forensics (2026-09-28) re-ran seed/verify_seal.py (exit 1, engines/key_law.py, 56/57) and found the recorded verdict outdated.

**Defect class:** state-doc verdict decay. The verdict was true at its moment and kept as present truth after the world moved; a seal maintained by hand re-breaks between hand-seals, and the doc named the old break, not the live one.

**Falsifier that would have fired:** re-running the verifying instrument (seed/verify_seal.py) and diffing its named drift member against the doc's: one run, seconds.

**Instrument upgrade (who runs what, when):** the seal verify runs on a schedule (a census_patrol-style task; owner: whoever registers the next scheduled task, one sitting) and CURRENT.md's seed-seal section is refreshed from the run's own output, or marked with the run's timestamp and result; a doc that describes a state it did not measure today carries the measurement date next to the claim.

## Incident 12: UF-128 LANDED with a false tool claim

**Verbatim:** "UF-128 answer: "ripgrep: Follows symlinks by default (--follow)" is false (rg skips symlinks unless --follow)" (watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md:16)

**Lane of origin:** the UF-128 dig (landed, decision rule sound, tool claims false per the sweep's verdict "UF-128 LANDED with defect").

**Defect class:** unverified tool claim, same family as incident 1 but worse in a way: the answer was otherwise sound, so the false default-behavior claim rode trusted delivery.

**Falsifier that would have fired:** one command: run rg against a symlink without --follow.

**Instrument upgrade:** folded into the incident 1 citation-resolution gate: tool-behavior claims in landed answers carry a one-line repro command, run at filing.

## Supporting observations (run this session, not incidents)

- REGISTRY moment drift, live: f-25 (2026-09-28) counted memory/workflows/REGISTRY.jsonl at 30 rows (21 PASS / 9 FAIL); my parse this session reads 45 rows, verdict PASS 34 / FAIL 11. Both are true at their moments; neither is a constant. This is B2-216 demonstrated on the registry itself.
- Shared-surface INDEX hash mismatches (w1 b2-stone2b.ss_validate.json and w2 b5_validate_raw.json, ok:false, errors "hash mismatch: THE50_W1_T05_PAYOFF_MATRIX.md" and siblings): files edited after INDEX registration. Matches ledger-truth.md's caveat: "a receipt that was silently edited without any ledger row would not be caught by this pass." Class: silent edit without re-index; the validator is the instrument that fires.
- OLM steal card anchor drift (watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md:68): "NOT re-verified. My read of `mag/percolator.py:255-279` shows heal-merge MAX/SUM code at those lines, so that anchor is stale or drifted. Flagged, not asserted." A carried anchor (the 09-28 DIGEST's "bare counter promote gate" at :264-272) no longer matches the named lines. Class: anchor drift; the flag-not-assert handling is the honest pattern, and the citation linter of incident 5 is the mechanical version.

## The ask's named incident I could not confirm as stated

The ask names "w4-20 placeholder". I searched flash50 (all 496 files), the burn_reset queue and work dirs, the gala lanes, LEDGER.jsonl, CONVO.md, and git history for a w4-20 verdict that was a placeholder later corrected, and found no such incident. What the evidence does support about w4-20: (a) its receipt exists in full quality (18,212 bytes, deep citation discipline, honesty block) and landed byte-identically twice (incident 10); (b) its own live forensics corrected a stale verdict in state/CURRENT.md (incident 11). If a distinct "w4-20 placeholder" verdict exists, it is outside the surfaces I searched; I state that plainly rather than manufacturing one.

## Finish-line self-check

The finish-line check (watch/inbox/gala_20260925/ractor50/lanes/accuracy.check.txt, script accuracy.check.py alongside it) byte-verifies 34 quote spans against their named source files and re-runs the session's own measurements (w4-20 duplicate sha, REGISTRY counts, receipt shape). Result: FINISHLINE_EXIT=0, 34/34 spans pass, 12 incidents (7+ met), zero em-dashes in the receipt.

## Decision ledger

This dance closes the accuracy-retro owed work and changes one dispatch contract plus one landing contract: (1) fallout-fix asks must carry pinned failing node IDs traceable to a named suite receipt (incident 2's law; the ball3 quantizer-fallout falsifier is the enforcement text), and (2) a LANDED verdict on a row carrying external citations or tool-behavior claims requires the citation/tool-claim resolution pass in the same session at landing time (incidents 1, 5, 12). It also surfaces one owed repair: f-25's playbook citation corrections were banked but never folded back into corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md (law 6 wrong path still at HEAD, law 8 still uncited) - the next doctrine-touching lane should apply f-25's three fixes or file the debt by name.
