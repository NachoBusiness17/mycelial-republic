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

**Defect class:** moment-verdict overwritten in place. The 18-fold's 
... [PREMIUM AUTOPSY REPLAY SIZING: file truncated, showing head 7875 + tail 2625 of 27272 chars; method head75+tail25, moment 2026-10-01; the premium original saw the full bytes] ... ...
was silently edited without any ledger row would not be caught by this pass." Class: silent edit without re-index; the validator is the instrument that fires.
- OLM steal card anchor drift (watch/inbox/frontier_olm_2026-09-30/steal/open-and-local-language-models.md:68): "NOT re-verified. My read of `mag/percolator.py:255-279` shows heal-merge MAX/SUM code at those lines, so that anchor is stale or drifted. Flagged, not asserted." A carried anchor (the 09-28 DIGEST's "bare counter promote gate" at :264-272) no longer matches the named lines. Class: anchor drift; the flag-not-assert handling is the honest pattern, and the citation linter of incident 5 is the mechanical version.

## The ask's named incident I could not confirm as stated

The ask names "w4-20 placeholder". I searched flash50 (all 496 files), the burn_reset queue and work dirs, the gala lanes, LEDGER.jsonl, CONVO.md, and git history for a w4-20 verdict that was a placeholder later corrected, and found no such incident. What the evidence does support about w4-20: (a) its receipt exists in full quality (18,212 bytes, deep citation discipline, honesty block) and landed byte-identically twice (incident 10); (b) its own live forensics corrected a stale verdict in state/CURRENT.md (incident 11). If a distinct "w4-20 placeholder" verdict exists, it is outside the surfaces I searched; I state that plainly rather than manufacturing one.

## Finish-line self-check

The finish-line check (watch/inbox/gala_20260925/ractor50/lanes/accuracy.check.txt, script accuracy.check.py alongside it) byte-verifies 34 quote spans against their named source files and re-runs the session's own measurements (w4-20 duplicate sha, REGISTRY counts, receipt shape). Result: FINISHLINE_EXIT=0, 34/34 spans pass, 12 incidents (7+ met), zero em-dashes in the receipt.

## Decision ledger

This dance closes the accuracy-retro owed work and changes one dispatch contract plus one landing contract: (1) fallout-fix asks must carry pinned failing node IDs traceable to a named suite receipt (incident 2's law; the ball3 quantizer-fallout falsifier is the enforcement text), and (2) a LANDED verdict on a row carrying external citations or tool-behavior claims requires the citation/tool-claim resolution pass in the same session at landing time (incidents 1, 5, 12). It also surfaces one owed repair: f-25's playbook citation corrections were banked but never folded back into corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md (law 6 wrong path still at HEAD, law 8 still uncited) - the next doctrine-touching lane should apply f-25's three fixes or file the debt by name.
