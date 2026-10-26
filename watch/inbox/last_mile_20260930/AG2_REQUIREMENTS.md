# AG2 — requirements.txt conflict resolution + cold-boot lock (audit finding #2, P0)

Date: 2026-09-30 · Owner seat: ZCode agent (file ownership: requirements.txt, requirements.lock)

## Problem

`requirements.txt` carried committed merge-conflict markers at L1/L17/L29
(`<<<<<<< Updated upstream` / `=======` / `>>>>>>> Stashed changes`), which breaks
`scripts/ensure_venv.ps1` on a fresh machine (`pip install -r requirements.txt`
fails on the marker lines).

## Resolution

- Kept the **upstream** block (15 deps). The stashed block (11 deps) was a strict
  subset — identical lines — so no merge additions were needed; the conflict was
  purely procedural.
- Upstream-only deps preserved: `chess>=1.10`, `textarena>=0.7.0`,
  `faster-whisper>=1.0.0`, `cryptography>=49.0.0` (ed25519 gwap signatures,
  M17 WAVE0 20260929 receipt comment retained on the line).
- Inline `#` trailing comments retained — legal under pip's requirements format.

## Verification (all exit 0)

1. Parse gate: every non-comment line parses via `packaging.requirements.Requirement`
   → `PARSE OK: 15 requirements`. (Two notes: `packaging.requirements` must be
   imported explicitly on this packaging version; trailing `#` comments are stripped
   pip-style before parsing, mirroring pip's line-level handling.)
2. Coverage gap found and fixed: `pip check` passed but chess + textarena were
   declared-not-installed (absent from first freeze). Installed
   `chess==1.11.2`, `TextArena==0.7.4` so the venv truly satisfies requirements.txt;
   `pip install -r requirements.txt --dry-run` now reports zero "Would install".
3. `python -m pip check` → `No broken requirements found.`
4. `pip freeze > requirements.lock` — 255 pinned lines; key pins:
   cryptography==49.0.0, faster-whisper==1.2.1, chess==1.11.2, TextArena==0.7.4.

## Cold-boot contract

Fresh machine: `pip install -r requirements.lock` (exact pins) or
`pip install -r requirements.txt` (floors) both resolve; no conflict markers remain.
