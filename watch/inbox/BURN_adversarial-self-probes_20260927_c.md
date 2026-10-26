## Verdict

green

## Evidence

Ledger row checked (memory/burns/LEDGER.jsonl tail, ts 2026-09-27T04:37:37Z, slug B2-298-patrol-persistence, verdict LANDED). Its one_line claims: "configs/drift_patrol_prompt.txt on disk 4438 bytes sha256 95a514b061f49beae3b63fa82e32bb730c17d70d072fbd11d200a1a06a71a0e9 byte-identical to this lane's fresh DB readback", "tests/test_drift_patrol_prompt_copy.py diffs copy vs DB in the freshness_check pattern, 3 passed on rerun", and a duplicate copy attempt "retracted".

Landing file read in full: watch/inbox/burn_wave_20260926/B2_298_patrol_persistence_20260926.md. Independent checks this pass, all read-only:
- sha256sum configs/drift_patrol_prompt.txt: 4438 bytes, sha256 95a514b061f49beae3b63fa82e32bb730c17d70d072fbd11d200a1a06a71a0e9. Exact match.
- configs/ holds exactly one drift-patrol prompt file; configs/drift_patrol_prompt_a7c71ad1.txt absent. Retraction claim holds.
- grep "def test_" tests/test_drift_patrol_prompt_copy.py: exactly 3 tests; line 59 is "def test_repo_copy_matches_live_db_bytes():", matching the receipt's ":59-65" quote.
- Rerun with PYTHONDONTWRITEBYTECODE=1 and pytest -p no:cacheprovider: "3 passed in 0.81s". Receipt claims "3 passed in 0.52s"; pass count matches, duration differs as durations do. The passing bytes test asserts live == db, so the DB byte-identity claim also held at check time.
Nothing in the one_line failed verification. Not independently re-hashed: the raw DB row (covered transitively by the passing assert).

## Steal or Vacuous

Steal, in PROWL canon. This was a near-distribution probe (the KL constraint held: real lane, real DB row, real test, no strawman) run against our own write surface, and the receipt survived a live false-success hunt. The B2-298 lane pre-declared its own blind channel: B2-553, the copy check "skips instead of failing" when a harness rebuild drops the DB row, exactly a false-success channel left open by design and already filed. Fleet adoption: a LANDED one_line carrying byte or sha claims is spot-checkable in minutes; tonight's run is the cost proof. The fresh web scan for 2026 external work returned snippet-grade only: an alphaXiv analysis that most self-improving LLM-agent papers claim persistent text artifacts without length-matched controls, and a dev.to "Visible Checklist Pattern" (Declare/Check). Full-text reads owed before any import, per the steering-theory lane's snippet-grade law.

## Falsifier

Pre-registered build: ledger spot-check patrol, WARN-ONLY, sampling 3 LANDED rows per day and verifying every sha/byte/existence claim in one_line against disk. Falsifier: if two consecutive weeks surface zero claim-artifact mismatches AND no lane acts on a patrol warning, the patrol is vacuous overhead and reverts to manual probes like this one.

## Bibliography

- watch/inbox/PROWL_STEAL_20260925.md (read in full)
- https://arxiv.org/abs/2605.18803 (abstract fetched; confirms the steal doc's paragraph; abstract makes no self-verification claim)
- memory/burns/LEDGER.jsonl (tail 10 rows read)
- watch/inbox/burn_wave_20260926/B2_298_patrol_persistence_20260926.md (read in full)
- configs/drift_patrol_prompt.txt (hashed)
- tests/test_drift_patrol_prompt_copy.py (grepped, executed read-only)
- [alphaXiv self-improving agent audit](https://www.alphaxiv.org) (snippet-grade, full text unread)
- [dev.to Visible Checklist Pattern](https://dev.to) (snippet-grade, full text unread)
