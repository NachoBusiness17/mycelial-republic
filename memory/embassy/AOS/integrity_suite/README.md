# Embassy Integrity Suite — clean-clone runnable

Deterministic, LLM-free, secret-free proof-of-values for the AOS partnership.
Run on a clean clone:

```
python -m venv .venv
.venv\Scripts\activate        # (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
python -m pytest tests/ -q    # -> 21 passed
```

## Layout
- `mag/embassy_integrity.py` — the integrity toolkit (stdlib only, no network).
- `tests/test_embassy_integrity.py` — 21 deterministic tests.
- `conftest.py` at root — ensures `mag` imports on a clean clone (this was the
  H1 packaging gap: the module now ships alongside its tests).

## What it demonstrates (runs, not claims)
Evidence-first tri-state claims, Verkle tamper-evident witness (evidence, not
authority), anti Self-Report-Instead-Of-Run guard, OPSEC gates G1–G8, symmetric
scrutiny, and the first-runtime inbox E2E with `promote: false`.
