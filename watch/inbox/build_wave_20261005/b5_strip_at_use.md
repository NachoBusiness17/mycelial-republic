# B5: STRIP-AT-USE LAW landed on the five Bearer-from-env modules (2026-10-05)

Residual closed: watch/inbox/go_wave_20261004/CSV_VERDICT_20261004.md named
five modules that build "Bearer " + key from an env/.env load without strip.
The .env LF normalization defused the CRLF class that day; this wave makes
the permanent law byte-real at every load site.

## The five sites (surgical, load lines only)

| Module | Site | Edit |
|---|---|---|
| mag/auth_switchboard.py | probe_key (Bearer build ~:116) | `key = key.strip()` after the empty-key guard; cleans both x-api-key and Authorization |
| mag/autoglm.py | _key env branch (feeds act ~:114) | `return v.strip()` on the os.environ hit; the .env branch already stripped |
| mag/doctor.py | _probe_remote_deep (~:531) | `key = key.strip()` at function entry; one strip covers the /models GET and the chat ping (headers are shared) |
| mag/fanout.py | fire key-load (~:66) | `os.environ[pack.get("key_env", ...)].strip()` |
| mag/flight_recorder.py | api_call (~:322) + docstring example | `key = key.strip()` at entry; the module docstring's copy-me example gained the same line so future callers inherit the law |

Every strip carries the one-line cause comment:

    # strip-at-use law: 2026-10-04 CR-header outage (CRLF .env key rode into Bearer, urllib rejected the header, elder lane down 14 cycles)

Cause chain (CSV_VERDICT root-cause section): .env was CRLF, key values
carried a trailing \r into the container env, urllib rejects a Bearer header
with a CR in it, the CYCLE_FAIL echo then leaked the header into the elder
trail (KEY_SCRUB_20261004) and the elder lane sat down 14 cycles.

## Regression test

tests/test_strip_at_use_20261005.py - one shared test,
test_bearer_strip_at_use_five_sites. A key with trailing \r\n is fed through
each module's real load path (probe_key direct, autoglm via ZAI_API_KEY_Lite
env + act, doctor via _probe_remote_deep, fanout via key_env os.environ read
in fire, flight_recorder via api_call); transport is faked (capture opener +
capture urlopen record the built Request and raise), so no socket opens; the
test asserts the built Authorization header equals "Bearer " + clean key
(and x-api-key for the switchboard).

Falsifier run: the five module edits stashed (git stash push, five files),
test FAILED at the first site assertion; stash popped, test green again.
The test bites.

## Gate contract numbers

- pytest: `./.venv/Scripts/python.exe -m pytest tests/test_strip_at_use_20261005.py -q`
  -> 1 passed in 0.58s (also passed at 0.48s on the first green run).
- ratchet: `./.venv/Scripts/python.exe tools/violation_ratchet.py check --changed`
  -> scope=16 changed files; hits=12; registered=12; NEW=0; expired-exceptions=0;
  RATCHET: PASS, exit 0. Zero NEW debt on the five files.
- Added lines scanned: zero em/en-dashes (pre-existing module docstrings
  untouched). No git commit per lane laws.

## Notes for the next sit

- autoglm's `_key()` .env fallback and flight_recorder's `load_env()` already
  stripped values; the holes were the raw os.environ branch (autoglm) and
  parameter-received keys everywhere else. All five now strip at the point
  the key enters the header build.
- doctor's deep-probe headers dict is built once and reused for the chat
  ping, so the single entry strip covers both requests.
