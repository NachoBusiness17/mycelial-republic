# B2-277 receipt: pre-push census block treats blind as stale (2026-09-26)

## Verdict

LANDED. The census block in githooks/pre-push now splits handling by exit class: exit 1 (STALE/COLLECT-DRIFT, the gate SAW the carrier and can name growth and counts) stays WARN-ONLY per the t40 no-lockout precedent and the block's own TODO-FLIP-TO-ENFORCE note (which now applies to the exit-1 flip only); exit 2 (cannot-verify: broken carrier grammar, future-dated census, git failure, the gate saw NOTHING) writes its full output to .git/census_blind_last_push.txt and blocks the push with exit 2. The law is in the comment next to the code: a blind gate is worse than no gate, because every push passes in silence (the 12-day-stale disease in a new costume); the operator response to a blind block is to fix or re-parse the carrier, never to bypass in silence.

## Evidence file:line quotes

- githooks/pre-push:58-62 (pre-edit): "tools/census_drift_patrol.py now states that bar in numbers ... WARN-ONLY first landing per t40 precedent: no lockouts without operator, so this block NEVER exits nonzero. TODO-FLIP-TO-ENFORCE (2026-09-26): once the patrol survives a few weeks of pushes clean, flip the handling below to `|| exit 1` ..." and the block itself (79-87 pre-edit): `out=$(...census_drift_patrol.py 2>&1) || true` with a case that only prints (the brief's exact disease).
- githooks/pre-push (post-edit, census block): `census_rc=0` / `out=$(...census_drift_patrol.py 2>&1) || census_rc=$?` ... `if [ "$census_rc" -eq 2 ]; then printf '%s\n' "$out" > .git/census_blind_last_push.txt; ... exit 2; fi` with the law comment "STALE (exit 1) keeps the t40 WARN-ONLY treatment ... BLIND (exit 2 cannot-verify ...) is a different disease: the gate saw NOTHING ... a blind gate is worse than no gate, so exit 2 is distinguishable on disk AND blocks".
- tools/census_drift_patrol.py:30-32: "Exit codes: 0 = census inside the bar; 1 = STALE or COLLECT-DRIFT ...; 2 = cannot verify."
- Falsifier transcript (this lane): after corrupting the carrier marker (`**Tests:**` -> `**Tests**`), the patrol exits 2; the new block prints "PUSH-GATE: census BLIND (exit 2 cannot-verify): push blocked, evidence at .git/census_blind_last_push.txt" and the evidence file lands on disk with the full cannot-verify output ("no parsable **Tests:** census line in AGENTS.md (need the claim shape: N tests [collected] / M files (YYYY-MM-DD census ...)"). Pre-change, the same broken state fell to the print-only WARN arm and the push proceeded.
- Restore proof: AGENTS.md sha256 head 0872c972aea95d38 before and after the falsifier act; post-restore the patrol is green (exit 0, "CENSUS-PATROL: ok - census 2026-09-26 (1910 collected / 303 files)").

## Work done

1. Claimed githooks/pre-push (QUEUE.md CLAIM SW-05, 20:42:52Z, census block only, no other block touched) before editing, per the shared-file claim law; the hook is working-tree-modified (+224 uncommitted lines from today's lanes).
2. Rewrote the census block: explicit exit-code capture (no more `|| true`), WARN arm unchanged for non-ok non-blind verdicts, new blind arm (evidence file + exit 2) for cannot-verify, header comments updated so the law travels with the code and the TODO-FLIP-TO-ENFORCE note now scopes to exit 1 only.
3. bash -n syntax check passed; falsifier executed for the blind arm (broken grammar -> exit 2 -> block + disk evidence) and the green arm (restored carrier -> exit 0 -> ok arm); the stale arm (exit 1 WARN-ONLY) is covered by the census self-test's hook-pairing groups ("hook pairing: stale run exits 1", "stale output falls to the WARN arm, never the ok prefix", 30/30 PASS in the B2-365 run earlier today) since the live carrier is currently green and manufacturing a stale carrier was unnecessary.
4. Retired the claim line (CLAIMED with this receipt pointer) at landing.

## Falsifier

Decidable today, decided today for the blind arm: break the AGENTS.md census grammar and run the hook body with the hook active. Before the change the push proceeded with only a WARN line; after the change the block writes .git/census_blind_last_push.txt and exits 2 (blocks). The split dies if: (a) the hook regresses to `|| true` or a print-only case; (b) an exit-2 from the patrol is ever treated as WARN (grep the block for census_rc); (c) the exit-1 WARN arm starts blocking (that flip is an operator decision reserved by the TODO-FLIP-TO-ENFORCE note, not this lane's call); (d) the evidence file path moves without a same-commit comment update.

## Bibliography closed

All read this lane: githooks/pre-push (census block pre + post, freshness and caption blocks untouched), tools/census_drift_patrol.py (exit mapping, run() output contract), tools/census_patrol_selftest.py hook-pairing groups, QUEUE.md B2-277 row + claim line, watch/inbox/burn_wave_20260926/B2_249_shape_law_20260926.md (pointer), AGENTS.md carrier (corrupted and restored byte-identical, sha 0872c972aea95d38 both sides).
