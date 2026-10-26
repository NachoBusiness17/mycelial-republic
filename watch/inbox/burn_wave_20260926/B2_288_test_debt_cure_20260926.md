# B2-288 receipt (2026-09-26)

## Verdict

LANDED. All three briefed failure surfaces root-caused and fixed in tests; combined run of the four touched files is 43 passed, 0 failed. The drift_dashboard half arrived already cured in bytes (see Falsifier), so no baseline-update was owed for it.

## Evidence file:line quotes

(a) order interaction (test_zai_burst.py + test_loop_death_guards.py):
- tests/test_loop_death_guards.py:176 (before fix): `monkeypatch.setitem(sys.modules, "mag.fuel_feed", fake_fuel)` alone.
- mag/work_loop.py:281: `from mag import fuel_feed` inside the fuel branch. Python resolves `from X import Y` through the parent package ATTRIBUTE first; replacing only sys.modules leaves the real module pinned on the `mag` object once anything has imported it.
- Mechanism probe (fresh interpreter): after `from mag import fuel_feed`, `hasattr(mag, "fuel_feed")` True; after `sys.modules["mag.fuel_feed"] = fake`, a second `from mag import fuel_feed` returned the REAL module (identity check False), proving the bypass.
- Polluter proof: probe plugin `pytest_sessionfinish` after `tests/test_zai_burst.py` alone printed `MAGFUELATTR: True SYSMOD: True`; the burst lane transitively performs the first real `mag.fuel_feed` import, so the work_fuel test then bypassed the fake and ran a REAL openrouter-a1 lane call (observed answer: quality 0.79, 4808 chars of KV-cache anchor text) instead of raising into the guard. Real external spend happened on every poisoned run; that is the finding beyond the assert.
- Fix: tests/test_loop_death_guards.py work_fuel branch now also does `monkeypatch.setattr(mag, "fuel_feed", fake_fuel, raising=False)` next to the setitem, with the cause comment. Pair rerun: 33 passed; file alone: 25 passed.

(b) standalone failures:
- tests/test_voice_shadow.py::test_start_kicks_thread failed with `AssertionError: assert 'running' == 'ready'`. Root cause measured, not guessed: scripted reproduction outside pytest reached "ready" in 3.35s; the test polled a fixed 30 x 0.05s = 1.5s. The daemon thread performs the first import of mag.voice_dig_board (note_scout_ready call at mag/voice_shadow.py inside _run_scout) on the cold path, and the transition must clear that import before save_shadow flips status. Flake source = fixed short deadline over a cold import, deterministic on this box. Fix: pre-import mag.voice_dig_board on the main thread and poll up to 300 x 0.05s with early break; named cause comment left in the test.
- tests/test_voice_turn.py::test_handle_voice_turn_heavy_auto_deepseek failed with `assert 'local' == 'deepseek'`. Root cause: NOT pollution; the expectation is stale. mag/intention_brief.compile_intention on the exact test text returns `{depth: heavy_code, seat_recommend: handoff, mode: handoff, why: "handoff_non_blocking; depth=heavy_code"}` (verified live), and mag/voice_turn.py gates on `brief.get("seat_recommend") == "handoff"` before seat selection, so the turn routes to the async handoff lane: spoken ack from local while DeepSeek files in background (mag/voice_handoff.py try_handoff_reply returns seat "local", route "handoff", provider "voice_handoff"). Reproduced deterministically outside pytest: `ok True seat local route handoff provider voice_handoff`. Fix: test renamed to test_handle_voice_turn_heavy_auto_handoff and now pins the handoff contract (route handoff, provider voice_handoff, seat local), with HANDOFF_DIR/INDEX_PATH monkeypatched to tmp_path so no handoff card lands in the repo during tests; cause comment left in the test.

(c) ratchet half:
- tools/drift_dashboard.py:35-38 carry a receipt comment from lane B2-216: "the original `except Exception: pass` guard here was NEW debt (ratchet run 2026-09-26, sig 59b703f590d8c52a, filed by lane B2-216); replaced with an explicit capability check". Current bytes: grep for `except.*pass|except Exception` over tools/drift_dashboard.py hits only the receipt comment line 35, no live swallow. The debt this brief ordered registered does not exist anymore; registering a nonexistent claim would pollute configs/violation_baseline.json, so per the ratchet law (register only real debt, by name) no baseline-update was run for it.

## Work done

1. Reproduced all three briefed failures with byte-level evidence before touching anything.
2. Fixed the sys.modules-only fake injection (parent-attribute patch added), the voice-shadow deadline/cold-import flake, and the stale voice-turn expectation (renamed, handoff contract pinned, handoff writes sandboxed to tmp_path).
3. Verified the drift_dashboard debt is cured in bytes and declined to register a ghost claim; documented why.
4. Left a cause-and-receipt comment at each fix site per the build-discipline law.
5. Cleanup: removed the temporary probe plugin used for the polluter proof.
6. Final combined verification: pytest tests/test_zai_burst.py tests/test_loop_death_guards.py tests/test_voice_shadow.py tests/test_voice_turn.py = 43 passed.
7. Ratchet `check --changed` at land time: the only NEW hit is `file-too-long: mag/shared_surface.py:402`, a concurrent lane's edit, not this lane's surface; left for its owning lane to accept or fix by name.

## Falsifier

- (a): revert tests/test_loop_death_guards.py to the setitem-only line, run test_zai_burst.py before test_loop_death_guards.py in one process; the work_fuel case again bypasses the fake and either fires a real lane call or fails the halt assert. The fix also falsifies if a future work_loop changes `from mag import fuel_feed` to plain attribute-free import in a way that dodges both patch surfaces; the double patch covers both known resolution paths.
- (b) shadow: set the poll back to 30 iterations with mag.voice_dig_board absent from sys.modules and a cold interpreter; the standalone failure returns within the old 1.5s window on this box.
- (b) voice_turn: if the intention compiler or the handoff gate changes so heavy_code stops routing to handoff for seat-less auto turns, the renamed test fails and the DeepSeek auto-answer contract must be re-pinned by whoever makes that change.
- (c): if a lane believes a live swallow remains in tools/drift_dashboard.py, grep the current bytes; a hit other than the line-35 receipt comment reopens the baseline-update this brief asked for.

## Bibliography closed

- tests/test_loop_death_guards.py (work_fuel branch, lines 172-197 post-fix)
- mag/work_loop.py:281-296 (fuel branch + guard)
- tests/test_zai_burst.py (polluter, transitively imports mag.fuel_feed)
- tests/test_voice_shadow.py (post-fix file, 59 lines)
- mag/voice_shadow.py _run_scout/start_shadow_scout/shadow_status; mag/voice_dig_board.py note_scout_ready/_save_state
- tests/test_voice_turn.py (renamed test, lines 105-140 post-fix)
- mag/voice_turn.py _voice_seat (208-225), intention gate (~1421-1435), handoff gate (1354+); mag/intention_brief.compile_intention (live call quoted); mag/voice_handoff.py try_handoff_reply (413-459), HANDOFF_DIR (25-26)
- tools/drift_dashboard.py:35-38 (B2-216 receipt comment); configs/violation_baseline.json (no edit)
- QUEUE.md row B2-288 (line 332 at lane start)
