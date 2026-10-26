# BURN receipt: prompt-uplift-lane (2026-09-26, pass g)

## Verdict

steal

## Evidence

Checker alive and confirmed on real bytes, unpiped, true exits captured. DETAIL seed vs itself: "VERDICT: MATCH (all invariant blocks byte-identical to seed)", EXIT=0, both sha256 68d44c02...e2d57 (same hash _f recorded; seed unmutated since). RACTOR_FACE_ORIGIN (new file, 16:10 today, zero prior coverage): FROZEN PREFIX sha f9ea2538...d895b and THE KNOT sha 8329555a...cb715, MATCH, EXIT=0. NPC_HEAD multi-marker sanity: both markers MATCH, EXIT=0.

No uplift procedure is written down. README "HOW TO USE (the ritual)" is template usage, not an optimizer flow; V2 amendments state law level only: "this section is the law level only." So the wiring below is drafted, not found.

Web (2026-09-26, one search): "few direct hits" on locked sections in prompt optimization; results were generic guardrails guides (ClickHouse Jul 2026, CSA Dec 2025, Kalvium Apr 2026), titles and snippets only, nothing fetched because none addresses byte-locked sections. Kill condition (optimizer natively locking a fact block) remains untriggered.

SIX_DROPS section 5: Prompt Optimizer "takes the lazy prompt you typed and returns the structured one you should have written"; section 3 JEV: confidence-gated verdicts, "retains 99% of comparator accuracy at lower cost".

## Steal or Vacuous

Adopted: runbook draft (paper only; no prompt or config edited) plus live checker confirmation. Invocation point: uplift is agent-run, checker called before any candidate adoption. Steps:

1. PIN: pick seed `roblox/prompts/<NAME>.prompt.md`; never edit in place; record `sha256sum`. Tool: sha256sum.
2. UPLIFT: run any optimizer (external Prompt Optimizer, gemma janitor, or tier climb) on a copy; candidate lands `watch/inbox/uplift/<NAME>.candidate.md`.
3. CHECK: `./.venv/Scripts/python.exe watch/inbox/bib_launder_check.py roblox/prompts/<NAME>.prompt.md <candidate>`, exit captured unpiped (downstream-pipe exit-code capture, _f). 0 MATCH, 2 FAIL, 3 NO_INVARIANT_BLOCK.
4. REJECT on 2: discard candidate, re-uplift FROM THE SEED (never the failed candidate) with the invariant instruction prepended: "Copy every section beginning with the marker(s) byte-for-byte, whitespace and line endings included." Re-check. No repair round on the block itself (README amendment A: a corrected FACTS block is still laundered provenance).
5. FILE on MATCH: receipt in `watch/inbox/` with both hashes and the checker verdict line. MATCH is necessary, not sufficient: adoption still passes the amendment D TARA seed-paired fold gate. Exit 3 templates (ONE_SHOT_GAME): lock cannot certify, score gate only, noted in receipt.

Home stays `watch/inbox/`; promotion to `tools/` remains an operator gate.

Fresh failure caught: unmarked-section escape. NPC_HEAD carries "## INFERENCE" and "## FALSEIFIER" outside the locked pair; all four RACTOR_FACE files carry "## INSTRUMENT BINDING" and "## FALSIFIER" outside it. A candidate rewriting those load-bearing sections passes the byte lock today. Not in the prior ledger list.

## Falsifier

Pre-registered: mutate one word in NPC_HEAD's INFERENCE section (outside locked markers) and rerun the pair. Prediction: exit 0 MATCH despite the load-bearing change, proving the registry gap. If it exits 2, the failure mode claim is false.

## Bibliography

Closed. Repo: roblox/prompts/README.md and all 9 prompt files; watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (sections 3, 5); BURN_prompt-uplift-lane_20260926_f.md; watch/inbox/bib_launder_check.py; live run outputs above. Web (2026-09-26): one search results page, snippets only, no fetch.
