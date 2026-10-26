# AG3 — effect_broker ":".join/split(":") shred fix (2026-09-29)

Seat: AG3 (ZCode), venv `.venv/Scripts/python.exe`. Audit finding #6
(`watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md`): `mag/effect_broker.py` L33-62
built FS_ALLOWLIST / TOOL_CWD_ALLOWLIST / NETWORK_DENYLIST with
`":".join(default).split(":")`. On Windows this shredded drive paths
(`C:\…\board` → `["C", "\…\board"]`) and shredded `"::1"` into empty strings;
since `"" in url` is always True, EVERY `network_access` effect was denied
while the built-in self-test kept passing (it only tests the deny case).

## Fix (mag/effect_broker.py)

- New `_list_from_env(name, default)`: env override parsed as a **JSON list of
  strings**; validates list-ness and rejects empty entries **fail-loud**
  (`ValueError` naming the env var — malformed JSON wrapped so the var is
  named, not just the JSON offset). JSON chosen over `os.pathsep` because
  `":"`-splitting shreds `C:\…` on Windows and `os.pathsep` (`:`) shreds
  `"::1"` on POSIX (WSL/Docker surfaces); JSON keeps both intact everywhere.
  Rationale: an empty deny entry matches every url (`"" in url` always True →
  deny-the-world) and an empty allow prefix matches every path
  (`str.startswith("")`), so bad entries must fail loud, never silently
  widen/collapse the gates.
- Intended default lists now documented in comments: FS = repo
  `board/ patches/ memory/ bridge/` roots; TOOL_CWD = repo root + `/mag` +
  `/board` (container lanes); NETWORK_DENY = loopback family
  `127.0.0.1, localhost, 0.0.0.0, "::1"` — `"::1"` survives as one real entry.
- No consumer of the env vars exists in-repo (grep over py/md/json/yaml/ps1;
  only dist_audit copy + vault evidence doc), so the env format change breaks
  no caller.

## Tests (tests/test_effect_broker_fix.py — new file)

The grep rule's head-1 hit (`tests/test_organ_map.py`) only asserts organ-map
row levels (false positive), so the fallback file was created. 6 tests:

1. denylist invariants — `"::1"` present as real entry, no empty strings.
2. FS allowlist unshredded on Windows — the four whole repo roots present,
   no `"C"`/empty fragments; TOOL_CWD contains repo root.
3. **POSITIVE network** — `https://example.com/index.html` through full
   `execute()` with `urllib.request.urlopen` monkeypatched (no live network
   dependency): RECEIPT_COMMITTED, `result.ok` True, status 200.
4. **NEGATIVE network** — `localhost`, `127.0.0.1`, `[::1]`, `0.0.0.0` urls
   all denied with "denied pattern" in the error.
5. fs_write roundtrip — allowed under `memory/`, denied outside allowlist
   (temp dir), no file created on deny.
6. env override — JSON list replaces default wholesale; legacy colon format,
   empty-string entry, and non-JSON each raise `ValueError` naming the var;
   module reloaded back to real lists after.

## Results (byte-read from the commands)

- Broker self-test: `python -m mag.effect_broker test` → **5/5 passed**.
- `pytest tests/test_effect_broker_fix.py tests/test_switchboard.py -q` →
  **20 passed** (6 new + 14 switchboard regression).
- `pytest tests/test_organ_map.py` → 2 failed — **pre-existing**, proven by
  re-running with `git checkout HEAD -- mag/effect_broker.py` (same 2
  failures: `atlas` LIVE level, elder gap surface; unrelated to this fix;
  fixed file restored after the check, `_list_from_env` x4 grep-verified).
- Residue: self-test/tests commit receipts under
  `memory/runs/effect_broker/` (by-design receipt trail), test tmp file
  unlinked.
