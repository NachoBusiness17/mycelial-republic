# B2-272 extract the changed-path pre-push helper 2026-09-26

## Verdict

LANDED. The changed-path decision is extracted: tools/prepush_paths_changed.py carries the five cases the B2-260 caption block tested (dirty-vs-HEAD, untracked, pushed-range hit, branch-deletion zero local sha, unborn-remote zero remote sha), mirrors `git diff --quiet` verdict semantics (0 unchanged / 1 changed / 2 git broke), and NEVER reads stdin (the hook consumes the ref lines once and passes them via --refs, keeping the single-consumer contract with the downstream blocks that reuse CAPTION_PUSH_INPUT). The caption block in githooks/pre-push now calls the helper instead of its hand-rolled arms; its WARN-ONLY behavior, message texts, and the verifier invocation are unchanged. The pre-registered falsifier is pinned: --selftest runs the five-case battery in a throwaway repo and all five verdicts match the inline block's semantics (5/5 PASS).

## Evidence file:line quotes

- githooks/pre-push:143-159 (pre-edit): the inline arms (git diff --quiet HEAD, git ls-files --others, the while-loop over consumed ref lines with the two zero-sha case guards) hand-rolled the decision.
- tools/prepush_paths_changed.py: paths_changed() arms a/b/c with (d)/(e) zero-sha guards (lsha/rsha == 40 zeros or empty -> skip); docstring INPUT CONTRACT "The helper NEVER reads stdin".
- githooks/pre-push (post-edit): caption block consumes stdin (CAPTION_PUSH_INPUT) then `.venv/Scripts/python.exe tools/prepush_paths_changed.py --refs "$CAPTION_PUSH_INPUT" -- "$CAPTION_GEN" "$CAPTION_VER"`; CAPTION_CHANGED=$?; the later blocks' own `set -- $CAPTION_PUSH_INPUT` reuse (lines 215, 287) is untouched; bash -n parses clean.
- Selftest output 2026-09-26: PASS dirty-vs-HEAD rc=1; PASS untracked rc=1; PASS range-hit rc=1; PASS branch-deletion-zero-local rc=0; PASS unborn-remote-zero-remote rc=0; ALL PASS (5 cases).

## Work done

1. Authored tools/prepush_paths_changed.py with the decision function, the stdin contract, and a built-in --selftest that builds a throwaway git repo and asserts all five case verdicts against the inline block's semantics.
2. First selftest run caught a bad test case (untracked file matching none of the pathspecs); fixed the case to add a never-committed pathspec (the arm's real shape) before trusting the battery; all five then passed.
3. Claim law: githooks/pre-push is working-tree-modified, CLAIM B2-272 (21:16:17Z) before the edit; the refactor replaces only the caption block's arms, stdin capture stays in the block, downstream reuse untouched; bash -n clean.

## Falsifier

Dies if: (a) the helper's verdict differs from the inline block's on any of the five cases (rerun --selftest); (b) the helper reads stdin (it must never; another consumer owns it); (c) a zero-sha ref (branch deletion or unborn remote) is diffed instead of skipped, false-failing clean pushes; (d) a hook run where only gen.txt is dirty skips the verifier (the refactored block must still run it on CHANGED).

## Bibliography closed

Read whole: githooks/pre-push (caption block + downstream CAPTION_PUSH_INPUT consumers), tools/violation_ratchet.py changed_files (the first hand-rolled gate, pattern source), watch/inbox/burn_wave_20260926/B2_260_verifier_gate_20260926.md pointer from the brief. Bytes: selftest 5/5 observed live; bash -n parse clean. Nothing synthesized.
