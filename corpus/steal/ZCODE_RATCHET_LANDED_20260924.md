# ZCODE RATCHET LANDED — 2026-09-24

Steal-execution record. Source pattern: zai-org/ZCode's executable architecture gate
(`scripts/architecture/index.mjs`, fingerprint ratchet + baseline register), surveyed in
[ZCODE_REPO_STEAL_MAP_20260924.md](ZCODE_REPO_STEAL_MAP_20260924.md) via dwfrun-91e94ae0.
Recreated from shapes in our own hand per Picasso law — Python, stdlib-only, estate
conventions. No ZCode code imported or read as text during the build.

## What landed

- `tools/violation_ratchet.py` (~210 lines, stdlib only)
- `configs/violation_baseline.json` — the register: 191 accepted claims (lives in tracked
  `configs/`, next to `keys.json`; first draft in `state/` moved out — state/ is gitignored
  and the register must be tracked)
- `mag/spore_seed.py` — syntax repair (see receipts)

Law of the tool: **today's debt is a registered claim; only NEW violations fail.**
The register grows only via `baseline-update` (a named human/agent act with `--by`/`--note`),
shrinks via `prune` (fixed debt leaves). Exceptions may carry `expires: YYYY-MM-DD` and rot
into violations when the date passes. Fingerprint = `sha256(rule\0file\0detail)[:16]`;
detail is line-free so unrelated edits never churn the register. One claim per (rule, file)
— teeth = "no NEW file acquires this disease."

Rules v1: `file-too-long` (>400 lines, the ZCode cap), `bare-except`, `shell-true`,
`todo-undated` (TODO/FIXME without a year), `parse-error`, `unreadable`.

Commands:
```
.venv/Scripts/python.exe tools/violation_ratchet.py check [--changed]
.venv/Scripts/python.exe tools/violation_ratchet.py baseline-update --by WHO [--note NOTE]
.venv/Scripts/python.exe tools/violation_ratchet.py prune
```
Exit: 0 pass, 1 new debt, 2 gate broken (git failure in --changed mode refuses to guess).

## Execution receipts (2026-09-24, .venv python 3.11.15, estate root)

1. **Virgin check → FAIL, exit 1**: scope=1,111 files (mag 1,005 + tools 105); hits=192;
   registered=0; NEW=192. Gate refuses to pass unregistered code.
2. **baseline-update → ADDED=192**, register = configs/violation_baseline.json.
3. **Check after register → PASS, exit 0** (192 registered, 0 new).
4. **Probe planted (`mag/_ratchet_probe.py`: bare except + undated TODO) → `check --changed`
   FAIL, exit 1**, NEW = `5182f04c02189a6f bare-except` + `0a03d2e6d672669a todo-undated`.
   (Probe v1 with `shell=True` was blocked by Mimosa's scanner — correct call, probe v2 used.)
5. **Probe removed → `check --changed` PASS, exit 0.**
6. **Prune no-op**: register stays 192 → later 191 after the spore fix below.
7. **Live-loop receipt**: after repairing `spore_seed.py`, `prune` dropped the dead
   `parse-error` claim (192→191) and the changed-gate immediately surfaced the NEXT error in
   that file as NEW — fix, prune, next — exactly the loop the tool exists to enforce.

## Haul: the ratchet paid for itself on day one

`mag/spore_seed.py` was **unparseable** — the whole module dead (unterminated f-string at
line 170/171, plus `ver_parser.add_parser.add_argument` typo at 162, plus nested
double-quotes inside f-strings at 175/177, illegal on Python 3.11). All repaired; module now
PARSE OK. **Residual (open, not fixed):** `from verkle import verkle_knot, get_chain_tip` —
no `verkle` module exists (sibling is `verkle_knot.py`); the spore parses but cannot import
until its import path is rewired. Left for the spore's next pass — repair beyond syntax
without knowing the intended wiring would be invention.

Also registered as day-one debt (now legal-but-counted): 188 files >400 lines (largest:
`game_campaign.py` 4,765, `ghost.py` 4,244, `voice_turn.py` 1,777), 2 `shell=True`
(`mag/bash_local.py:223`, `tools/pupeteer_gauntlet.py:558`), 1 bare except
(`mag/bay_organs_liveness_test.py:132`), 1 undated TODO (`mag/max_distill.py:89`).

## KeyAudit wiring — resolved NOT-APPLICABLE

The original candidate "wire --changed into KeyAudit" is answered by reading `mag/key_law.py`
(107 lines): it audits key manifest vs environment, not files — per-file change scoping
doesn't map. The changed-scope need for estate code is now owned by this ratchet.

## Standing use

Run `check --changed` before commits touching mag/ or tools/; run full `check` in the daily
sweep if wanted. NEW output names file+line+rule — fix the disease, or accept it by name via
`baseline-update --by <who>`. Never let the gate grow the register silently; never refresh
the baseline as a side effect of any other command.
