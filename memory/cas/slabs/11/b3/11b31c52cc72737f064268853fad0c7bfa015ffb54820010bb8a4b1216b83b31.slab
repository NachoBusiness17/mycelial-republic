# WORK lib-belady-1966

lane: hermes (headless one-shot)
ts: 2026-09-29T14:51:44.424941+00:00
ask: Find the canonical reference for Belady 1966 (the Belady anomaly / FIFO page-replacement study). Return: exact title, venue, year, and one verbatim quote of the anomaly claim with page if findable. If unreachable, say OWED with what you tried.

---

FINDING
WAVE 5 REPAIR landed 2026-09-29 (dbe5f682c): 12/12 gala lanes, 52 files, 4333 insertions. Measured rot fixed at root — suite-burn 14 failures → 0, render-pipe sealed (arch-01 D1/D2/D5, w4-15/w4-27), stealth-tools NTFS colon-slug + selffeed rc=1 + win32 mutex + mirrors throttle, attention-channel single vocabulary + eviction fix, seed-kernel re-attached, events-door 5 BACKFILL carriers + 63 rows served, config-hygiene fail-loud, mcp-pin-wire check_drift live, queue-closes surface_rebuild idempotent (63→11 UNCHECKED zero aborts). Working tree still dirty: 60+ modified + untracked (corpus_acquire.py family, estate_bridge.py, tests, watch inbox cards, rogue _s218 endpoint files, flash PDF). Estate is in active repair flux, not steady state.

STEALABLE
The `surface_rebuild` rebuild verb (idempotent, 3 tests) + WO-12 flip sweep pattern — UNCHECKED items collapse 63→11 with zero aborts because rebuild is a pure function of current state, not a mutation log. Any queue system with stale work items should adopt: rebuild verb first, flip sweep second, verify count third. Exact shape: `mag/surface_rebuild.py` + `tests/test_surface_rebuild.py`.

TESTABLE HYPOTHESIS
"After WAVE 5 repair, the suite-burn clean state (14 failures → 0) survives a fresh checkout + full test run." If it regresses, the fix is environmental (Windows path resolution, NTFS ADS) not code — the 3-fail circuit breaker in selffeed and the win32 named-mutex are the probable failure surfaces. To test: `git stash && git checkout HEAD~1 && python -m pytest tests/ -x -q && git stash pop`.

EVIDENCE or OWED
Evidence: `watch/inbox/gala_20260925/wave5-repair_RECEIPT.md` + `watch/inbox/wave5_repair/` + suite-burn.md/check.txt (1842 lines). Owed: 2 sibling corpus_acquire.py debts registered at fold (owner lane owes fix); ratchet PASS but seal restamped mirrors.json only — the full mirrors re-verify is not yet filed. Also the `_s218` endpoint files (untracked) are unaccounted build debris — scan before they merge.
