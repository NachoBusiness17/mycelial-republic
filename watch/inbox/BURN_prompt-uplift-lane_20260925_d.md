# BURN receipt: prompt-uplift-lane (2026-09-25, pass d; filed 2026-09-26)

## Verdict

steal

## Evidence

The ledger names the patch but never ships it. Pass a: "optimizer may touch structure and instructions only; FACTS and bibliography lines are carried byte-verbatim into every candidate; any delta there is FAIL(BIB_LAUNDER)." Pass b scoped it: "No bibliography guard exists anywhere in the class." Pass c confirmed: "FAIL(BIB_LAUNDER) from pass a stands unchallenged: no bibliography guard exists in GEPA either."

The wider field has the same hole. Fresh search (2026-09-26): "The specific concept of an 'optimizer' that rewrites prompts while preserving invariant/protected sections against injection doesn't appear as a well-indexed named work" (WebSearch result summary). Closest adjacent hit, snippet only: "Recent work (2024 to 2026) has converged on a strategy for defending tool-using LLM agents against indirect prompt injection" (arXiv, June 2026, titled "Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection"). Agent-domain, not optimizer-domain; no prior art to steal; drafted in-house.

Enforcement seat, decided by canon (roblox/prompts/README.md law 5): "The LLM calls verifiers; it never is one."

## Steal or Vacuous

Drafted patch. DRAFT ONLY: roblox/prompts/ untouched.

(a) One line per file, in each CONTRACT (NPC_HEAD: under FROZEN PREFIX):

- README.md, amend law 4: "Uplift invariance: any optimizer or uplift pass may rewrite structure and instructions only; FACTS and Bibliography sections are invariant and must survive byte-for-byte into every candidate; any delta is FAIL(BIB_LAUNDER)."
- DETAIL.prompt.md, item 6: "Uplift invariance: the `## FACTS` block (closed bibliography) is invariant under any optimizer/uplift rewrite; byte-for-byte or FAIL(BIB_LAUNDER)."
- PORT_GAME.prompt.md, item 6: "Uplift invariance: `## SOURCE TRUTH` is invariant under any optimizer/uplift rewrite; byte-for-byte or FAIL(BIB_LAUNDER)."
- CLONE_WHEEL.prompt.md, item 6: "Uplift invariance: `## THE WHEEL TO CLONE` and the item 2 source lines are invariant; byte-for-byte or FAIL(BIB_LAUNDER)."
- ONE_SHOT_GAME.prompt.md, item 8: "Uplift invariance: this prompt ships no FACTS block; a rewrite that introduces one, or any sourced-looking claim, is FAIL(BIB_LAUNDER)."
- NPC_HEAD.prompt.md: "Uplift invariance: the FROZEN PREFIX and THE KNOT are this head's facts; byte-for-byte or FAIL(BIB_LAUNDER)."

(b) Check: extract each invariant block by fixed marker (header through next header); sha256 the seed's blocks; per candidate, re-extract and hash; compare against the SEED hash, never the previous candidate (anchor clause, pass a). Empty diff is the only pass. No whitespace or unicode normalization (launder vectors). Any mismatch is FAIL(BIB_LAUNDER), rejected regardless of score, no repair round (a "corrected" FACTS block is still laundered provenance).

(c) Home: a pre-flight script (draft name tools/bib_launder_check.py, exit 2 on fail), not a judge-seat instruction. Byte-equality is mechanical; a judge asked to verify bytes will paraphrase-verify, reintroducing the named failure. Judge seat keeps one line: scores never rehabilitate a FAIL(BIB_LAUNDER).

## Falsifier

none proposed

## Bibliography

Closed. Repo: roblox/prompts/README.md, DETAIL.prompt.md, PORT_GAME.prompt.md, CLONE_WHEEL.prompt.md, ONE_SHOT_GAME.prompt.md, NPC_HEAD.prompt.md; watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (sections 3, 5); BURN_prompt-uplift-lane_20260925.md, _b.md, _c.md. Web (2026-09-26): one WebSearch result summary (invariant-section preservation absent as a named work; adjacent out-of-band-defense hit snippet-level). OWED: the arXiv ID of that out-of-band paper (title lookup 429'd twice); still carried: VisualPrompter OpenReview full text, Kim CVPR 2026 PDF.
