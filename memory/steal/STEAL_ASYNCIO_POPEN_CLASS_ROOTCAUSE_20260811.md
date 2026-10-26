# STEAL — no-window subprocess.Popen patch must be a CLASS, not a function (2026-08-11)

## Symptom (ghost-daemon crash-loop after reboot)
Every `ghost-daemon`/`ghost` process died instantly on `import asyncio`:
`TypeError: function() argument 'code' must be code, not str` at
`asyncio/windows_utils.py:125 class Popen(subprocess.Popen)`.

## Root cause (found by grounding, not guessing)
`.venv/Lib/site-packages/sitecustomize.py` (the STATELESS no-window hook) patches
`subprocess.Popen = _popen` — a plain **function** — at every interpreter startup to force
CREATE_NO_WINDOW. Then `asyncio.windows_utils` does `class Popen(subprocess.Popen)` — subclassing
a function raises the TypeError, so ANY process importing asyncio crashes. This is why the daemon
could never start.

## Fix (verified)
- `.venv/Lib/site-packages/sitecustomize.py`: make the wrapper a **CLASS subclass** of the original:
  `class _Popen(_orig_popen): def __init__(self,*a,**k): k["creationflags"]=_no_window(k.get("creationflags")); super().__init__(*a,**k)`.
  Keeps CREATE_NO_WINDOW enforcement AND keeps asyncio subclassing safe. `subprocess.run` stays a function (asyncio doesn't subclass it).
- `mag/headless.py install_no_window_defaults()`: hardened — idempotent (sentinel `_mag_nowin`), and
  captures the TRUE original `_REAL_Popen` at module import so it never wraps an already-wrapped ambient.

## Verified with real data
- Fresh bare python + sitecustomize: `Popen is class` → `import asyncio` OK → `windows_utils.Popen` subclass OK → real spawn works (no-window preserved).
- ghost-daemon restarted: `Uvicorn running on http://0.0.0.0:9000`, `Application startup complete`, `:9000 health 200 status up`.

## Lesson / law (steal, gated)
- ANY no-window/process patch that wraps `subprocess.Popen` MUST be a CLASS (subclass of the original),
  NEVER a function — or asyncio on Windows breaks every process in the env. This is the durable invariant.
- Ground in the actual bytes (sitecustomize) before theorizing about the crash.
- The sitecustomize no-window hook and headless.install_no_window_defaults are DUPLICATE mechanisms; both
  must produce class wrappers.
