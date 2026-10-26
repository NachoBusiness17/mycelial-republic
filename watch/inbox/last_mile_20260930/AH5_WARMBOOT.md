# AH5 — WARMBOOT DEPLOYMENTS (audit §2.3) · 2026-09-30

**Lane:** last_mile AH5 · **Files:** `mag/hermes_warm_boot.py`, `configs/deployments.json` (new), `tests/test_ah5_warmboot.py` (new, 16 tests)

## What moved

`_deployments` hardcoded the Vercel URL inline (old L86-89, "Known live URLs from operator records"). The known-URL list now resolves through `_deployment_urls()` with a strict order: **env `MAG_DEPLOYMENTS` (JSON: bare list or `{"known_urls": [...]}`) > `configs/deployments.json` > the old inline literal as `_DEFAULT_KNOWN_URLS`** — so a missing config and missing env break nothing. The payload gains `known_urls_source` + `notes` (a bad env/config value is a reported note, never a crash); `known_urls` itself is unchanged shape (no external consumers: only hermes_warm_boot's own summary line reads it).

## curl -I law, mechanized

Module comment near the default carries the AGENTS.md law (Vercel URLs may 302 SSO — `curl -I` before reporting live). New `--check-deployments` flag: `check_deployments()` HEAD-probes every known URL via `_head_no_redirect` (10s timeout, no auth) with redirects **refused at the handler**, so a 302 surfaces as `status + Location` instead of silently landing on the sign-in page. Exit 0 when every URL got an HTTP status (a 302 counts as responded and prints the verify-before-live caveat); exit 1 only on transport failure (timeout/DNS/TLS).

## Evidence

- `pytest tests/test_ah5_warmboot.py -q` → **16 passed** (2026-09-30)
- `pytest tests/ -q -k "warm_boot or hermes or ah5 or ag5"` → **32 passed, 0 failed**; AG5 suite alone → 13 passed
- Live `python -m mag.hermes_warm_boot --check-deployments` → `source=configs`, URL → **302 redirect=https://vercel.com/sso-api?url=...** (the exact AGENTS.md disease, caught by the first probe), exit 0
- Live `--json` with `MAG_DEPLOYMENTS='["https://env.example/override.html"]'` → `known_urls_source=env`, override wins; without env → `configs` (file loads)
- Ratchet `tools/violation_ratchet.py check --changed`: my files add **0 NEW hits**; the 1 NEW hit (`mag/rib_cache.py:168` except-pass) is another lane's uncommitted working-tree change, untouched by AH5
