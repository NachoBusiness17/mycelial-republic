# P0-3 + P0-1 EXECUTE RECEIPT — 2026-09-26 (Mag seat)

**Operator GO:** Nacho/Mark corrected waiting-for-GO after Elder execute-now judgment.
**Authority:** `watch/inbox/ELDER_ASK_SEED_AUDIT_20260926.md` order 3→1→5→2→4; verbs execute-now for 3 and 1.
**Law:** residual on disk = truth. Chain READ-ONLY. No CONDUCTOR mint. No Compass vision rewrite.

---

## P0-3 inbox writer contract — DONE this turn (partial residual filed)

### Already sealed before this turn (verified, not re-invented)
- **Seal hook live:** `C:/Users/foste/.zcode/cli/config.json` lines 39 (gate) + 52 (seal) → `tools/md_record_seal.py`.
- **Writer-contract code:** `tools/md_record_seal.py` inbox-relative register under `watch/inbox` only (B2-41, 2026-09-26).
- **Historical 207 debt:** paid by B2-02 (235 registers) + B2-146 stragglers; receipts on disk.

### Burned this turn (unregistered → registered)
Used existing door only: `node scripts/index_fold_host.mjs add` with `INDEX_WRITER=mag-p0-3-writer-contract-20260926`, cwd=`watch/inbox` (bare basenames — OUTSIDE_RE lesson from B2-02).

| # | file | class | nonce |
|---|------|-------|-------|
| 1–10 | ten `BURN_*_20260926*.md` (adversarial / b2-wave-fold / build-fold-verify / middle-path / queue-field / rsi-harness / steering / stego / third-way / world-models) | receipt | 1–10 |
| 11 | `ELDER_ASK_SEED_AUDIT_20260926.md` | receipt | 11 |
| 12 | `SECRET_SCAN_RULESET_ROTATION_20260926.md` | receipt | 12 |
| 13 | `SEED_SELF_STEAL_AUDIT_20260926.md` | receipt | 13 |
| 14 | `THIRD_WAY_GRACE_SCHEMA.json` | data | 14 |
| 15 | `mseat_drift_grade.py` | code | 15 |

- **Skipped on purpose:** `index_events.jsonl` (self-referential; hash changes every append — B2-02 law).
- **Nonces:** contiguous 1–15 (no gap on this writer).
- **Rebuild:** `node scripts/index_fold_host.mjs rebuild` → folded 3509 events → **1036** active items (exit 2 = pre-existing fold_warnings channel, expected).

### Before / after (read back)
| meter | before | after |
|-------|--------|-------|
| `shared_surface` unindexed (excl. intentional) | 15 files | **0** (`unindexed_items == ['index_events.jsonl']` only) |
| INDEX active items | 1021 | **1036** (+15) |
| P0-3 writer nonce gaps | n/a | **0** |

### Residual still open (not invented; already on QUEUE / fold_warnings)
1. **Live writer nonce gaps:** `zcode-seat-20260926` resets `nonce=1` each hand-mint batch (5 gaps today). Clear path = use `node … add` (auto-advance) or advance from last nonce — do not erase history. Related open: QUEUE **B2-398** (`cls` alias → UNPROVEN).
2. **Aged fold_warnings:** ~60 historical nonce-gap lines (sancho / exp002a / pid writers) + **outside-dropped `watch/` x257** (248 paths) + inexact 2^53 band **561** events. Append-only log: cannot "clear" without erase. Migration owed: QUEUE **B2-211** (drift-patrol-cron charter), **B2-148** (seal hook seq), **B2-280/294**.
3. **Hash mismatches still:** `INDEX.json`, `REJECTION_TAXONOMY_20260917.md`, `BURN_JUDGE_LANE_BUILD_20260925.md` (pre-existing drift / self-refold).

---

## P0-1 warm face — DONE this turn (FROZEN, not regenerated)

### `memory/briefs/latest.md`
- **Action:** stamped `# FROZEN as-of 2026-09-26 (Mag P0-1 warm-face)` banner atop fossil body.
- **Why not regenerate:** `mag.brief_local.write_brief` rebuilds from session biography dossiers, not tip+CURRENT+inbox. No sealed tip+CURRENT+inbox brief compiler found; inventing one = out of scope / costume.
- **Read instead:** tip · CURRENT · INDEX · SEED + ELDER asks.

### Compass §4 (`docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md`)
- **Action:** FROZEN as-of 2026-09-26 notice on §4 only. Table body left as August snapshot (labeled frozen). Vision prose (§1–3, §5+) **not** rewritten.

---

## Still open (Elder order 5→2→4 — not this execute slice)
| P0 | verb | status |
|----|------|--------|
| **P0-5** | execute-now | OPEN — `seed/verify_seal.py` + FIRST_BOOT on clean tree / name stranger in CURRENT owed |
| **P0-2** | demote | OPEN — move MAG_CHORD_V3 + Light Operator to explicit CANDIDATE shelf |
| **P0-4** | freeze-language | OPEN — strike CONDUCTOR from Kabuki prose; no mint |

---

## Commands run (this Mag turn)
```
cd watch/inbox
$env:INDEX_WRITER='mag-p0-3-writer-contract-20260926'
node ../../scripts/index_fold_host.mjs add <file> <class> <purpose>   # x15, all OK
node ../../scripts/index_fold_host.mjs rebuild   # exit 2 (fold_warnings), 3509→1036
PYTHONPATH=repo .\.venv\Scripts\python.exe -c "…inspect_surface…"
# stamp FROZEN on memory/briefs/latest.md + docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md §4
```

**Not done:** mutate `verkle_chain.jsonl`; mint CONDUCTOR; rewrite Compass vision; invent new inbox architecture.

*End receipt — Mag seat. Residual beats scroll.*

## Amendment — live brief writers sealed (same turn, after stamp-eaten)

Concurrent regenerators (mag.brief_local.write_brief via biography; mag.session_state_brief.write_brief via janitor) rewrote memory/briefs/latest.md within ~1 min of the first FROZEN stamp (mtime 13:58 → 13:59 ET), restoring the August fossil with a fresh face.

**Seal landed (not new architecture):** both write_brief entry points now return ok=False, frozen=True when latest.md begins with # FROZEN, refusing overwrite. Unfreeze = edit/remove the banner (operator deliberate).

Verified: both writers refuse; banner persists; Compass §4 freeze untouched.

## Amendment 2 — OS read-only + durable freeze notice

In-memory daemons kept rewriting latest.md despite on-disk write_brief guards (old module still loaded). Additional seals this turn:

1. ttrib +R memory\briefs\latest.md (read-only bit) — overwrite fails until deliberate ttrib -R.
2. Durable notice memory/briefs/FROZEN_ASOF_20260926.md (regenerators do not target this path).
3. Code guards remain for post-reload.

Verified: banner held 8s+ under +R; Compass §4 freeze still present; unindexed still only index_events.jsonl.

