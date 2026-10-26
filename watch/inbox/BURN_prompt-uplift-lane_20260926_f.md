# BURN receipt: prompt-uplift-lane (2026-09-26, pass f)

## Verdict

steal

## Evidence

The owed item existed and this pass executed it. README V2 amendments: "Still owed: the per-template contract lines and the checker script from pass d (a)/(b)/(c); this section is the law level only." Pass d specced the mechanics: "compare against the SEED hash, never the previous candidate (anchor clause, pass a). Empty diff is the only pass. No whitespace or unicode normalization (launder vectors)."

Markers learned by reading the files, not the README shorthand: DETAIL "## FACTS", PORT_GAME "## SOURCE TRUTH", CLONE_WHEEL "## THE WHEEL TO CLONE", NPC_HEAD two blocks "## FROZEN PREFIX" + "## THE KNOT", ONE_SHOT_GAME carries none.

Ledger discrepancy: this pass was told a 20260926_e receipt exists; no such file is on disk. Latest prior receipt is _d. Nothing was carried from a phantom row.

Fresh search (2026-09-26, one WebSearch): null. Surfaced junk (SWI-Prolog 1990 PDF, an Android e2fsprogs repo matching "byte/inode", an OSRS guide); two refined queries inside the same call also returned nothing on invariant-section preservation under LLM prompt rewriting. Consistent with _d's negative; kill condition (a shipped optimizer natively locking a fact block) remains untriggered.

## Steal or Vacuous

Adopted: watch/inbox/bib_launder_check.py (stdlib only, byte-exact span extraction, multi-marker, exits 0 MATCH / 2 FAIL(BIB_LAUNDER) / 3 NO_INVARIANT_BLOCK). Executed tabletop outputs:

1. DETAIL identical copy: both sha256 68d44c02...e2d57, "VERDICT: MATCH", exit 0.
2. DETAIL one word flipped inside FACTS ("verified" to "CORRUPTED"): exit 2, first divergent line reported at block line 3, the placeholder line, showing "paste CORRUPTED numbers" against "paste verified numbers".
3. NPC_HEAD knot word flipped: FROZEN PREFIX block still MATCHed, THE KNOT diverged at block line 5, exit 2. Multi-marker isolation works.
4. PORT_GAME with the SOURCE TRUTH block deleted outright: "launder by deletion", exit 2.
5. ONE_SHOT_GAME: exit 3 NO_INVARIANT_BLOCK, correct because it ships no block by design; the byte checker does not fake a MATCH there.

Coverage runs on PORT_GAME, CLONE_WHEEL, NPC_HEAD identical copies: all MATCH.

Fresh failure caught mid-pass, name it "downstream-pipe exit-code capture": running the checker through `tail -1` made `echo exit=$?` report tail's 0 instead of python's 3, so a no-block case read as pass. Re-ran unpiped to get the true code. Any harness piping a verifier through a formatter must capture the verifier's own exit.

Home: built at watch/inbox/ per this pass's order; pass d drafted tools/bib_launder_check.py. Promotion to tools/ stays an operator gate; inbox home keeps it on the shared surface meanwhile.

## Falsifier

Pre-registered: seed-mutation anchor test. Append one byte to the seed's FACTS block and rerun the same candidate pair; the earlier MATCH flips to FAIL with neither candidate changed. Prediction if the instrument is honest: verdicts are only valid against a byte-pinned seed, so every receipt must record the seed's sha256 next to the candidate verdict.

## Bibliography

Closed. Repo: roblox/prompts/README.md, DETAIL.prompt.md, PORT_GAME.prompt.md, CLONE_WHEEL.prompt.md, NPC_HEAD.prompt.md, ONE_SHOT_GAME.prompt.md; watch/inbox/SIX_DROPS_JOBHUNT_JUDGE_WAVE_20260925.md (sections 3, 5); BURN_prompt-uplift-lane_20260925_d.md; watch/inbox/bib_launder_check.py. Web (2026-09-26): one WebSearch call, null result, no usable links.
