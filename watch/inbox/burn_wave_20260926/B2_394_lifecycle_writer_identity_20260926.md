# B2-394 receipt (2026-09-26)

## Verdict

LANDED. track_loop_gap now stamps every future gap row with the observing process identity (pid, executable, host, proxy env vars) appended into the existing detail field, so the next lifecycle_gap pile carries its own culprit. The writer path the brief asked to find is named from bytes: track_lifecycle_into_improve (mag/temperature_stack.py) is called from mag/lifecycle.py auto_reconcile (~line 871), which is called from mag/power.py boot (~line 523) plus whatever route surfaces the reconcile, and it writes rows with a hardcoded where="GET /api/v1/lifecycle" - a route label, not an identity, which is exactly why the 89-row pile was unreconstructable.

## Evidence file:line quotes

- The writer chain, from bytes: mag/temperature_stack.py:541 `track_loop_gap(f"lifecycle_gap:{gid}", detail=f"should be on but actual off - piece={gid}", where="GET /api/v1/lifecycle", kind="lifecycle_gap", lifecycle=...)` inside track_lifecycle_into_improve (line 528); called at mag/lifecycle.py:871-873 (`result["gap_track"] = track_lifecycle_into_improve()` inside auto_reconcile); auto_reconcile called at mag/power.py:523-525 (`lifecycle_boot = auto_reconcile(force=True)` at boot). The B2-81 gap: none of those bytes record WHICH process ran them.
- mag/temperature_stack.py after edit (track_loop_gap, detail construction): cause comment naming the 89 rows, the independent 31s-cadence poller that answered 200 at 70-90ms in the same seconds, and the hardcoded where= label; then `detail = "%s [writer pid=%s exe=%s host=%s %s]" % (detail, os.getpid(), (sys.executable or "")[:80], (socket.gethostname() or "")[:60], _proxy,)[:1000]` with proxy vars HTTP_PROXY/HTTPS_PROXY/ALL_PROXY/http_proxy/https_proxy (present ones, 80-char cap each) or "proxies=none". The identity is computed BEFORE _gap_dedupe_key, so rows from different observing processes no longer collapse into one dedupe bucket (the 89-row pile's merge is what hid the culprit).
- tests/test_temperature_stack.py::test_track_loop_gap_names_writer_identity (new pin, passes): forces a row with MAG_GAPS_LOG redirected and side sinks isolated, asserts detail carries "[writer pid=", exe, host, a set HTTPS_PROXY value, and the live pid; production GAPS_LOG byte-size unchanged (B2-86 hygiene held).
- Suite state at land: my pin + the B2-86 dedupe pin both pass (2 passed). tests/test_temperature_stack.py::test_track_lifecycle_into_improve_carries_policy_inputs currently ERRORs at `import mag.lifecycle` -> `from win_powershell import powershell_exe` (ModuleNotFoundError): mag/win_powershell.py is git-untracked and mag/lifecycle.py working-tree-modified by a sibling lane mid-flight, and the flat import needs mag/ on sys.path; that surface is not this lane's edit (my diff touches mag/temperature_stack.py + its test only) and is left for its owning lane per the claim law.

## Work done

1. Traced the writer path from the row shape backwards (where= label -> track_lifecycle_into_improve -> auto_reconcile -> power boot) so the brief's "find it" is answered with named bytes: the rows were written by whichever process executed auto_reconcile (boot most plausibly), but the code path structurally could not say so; now it can.
2. Landed the identity stamp in the existing detail field per the brief, with the proxy vars included because the proxy mechanism reproduces the B2-81 signature.
3. Moved the stamp ahead of the dedupe key so cross-process duplicate gaps stop merging (behavior change named here).
4. Added the falsifier pin; production log untouched; py_compile clean.

## Falsifier

The brief's falsifier: "a new lifecycle_gap row whose detail cannot name the writing process identity". After this landing every row through track_loop_gap carries the stamp; the pin test fails if anyone removes it, truncates the detail cap below the stamp, or computes identity after dedupe again. Historic reverse: the existing 89 rows stay anonymous (the stamp only helps future rows, as the brief scoped it). The sibling-lane import error named above is falsifier-adjacent: if track_lifecycle_into_improve's caller chain cannot even import under pytest, no new rows flow at all; that is the owning lane's to close.

## Bibliography closed

- mag/temperature_stack.py (imports + track_loop_gap detail block edited; track_lifecycle_into_improve lines 528-557 read)
- mag/lifecycle.py (auto_reconcile ~855-877, read; working-tree-modified by sibling lane, untouched here)
- mag/power.py (523-525 boot caller, read)
- tests/test_temperature_stack.py (new pin appended; B2-86 hygiene helpers reused)
- watch/inbox/burn_wave_20260926/B2_81_ollama_truth_20260926.md (the 89-row evidence, via the brief)
