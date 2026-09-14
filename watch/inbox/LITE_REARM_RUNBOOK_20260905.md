# LITE RE-ARM RUNBOOK — forward track `lite-rearm-sep8`

# 🚨 DO NOT EXECUTE BEFORE 2026-09-08 02:19Z (weekly pool reset ~02:19Z; early execution burns metered credits against an empty pool)

Written 2026-09-05 by worker `rearm` (5-worker concurrency probe). RUNBOOK ONLY — this file
executes nothing. GO-gates apply: credential writes are OPERATOR-HAND ONLY. $0 at write time.

Gate of record: **B1 refeed-guard** (`watch/inbox/REFEED_GUARD_B1_20260905.md` once landed;
B1 row in `watch/WEEKEND_BURN_BOARD_20260905.md` — "Sep 8: Lite re-arms THROUGH B1's guard,
not before"). Registry row: `configs/auth_tracks.yaml` → `lite-rearm-sep8` (due
2026-09-08T02:19Z) — verified present 2026-09-05.

## PRECONDITIONS (all must hold at T-0; verify, never assume)

- [ ] **P1 — B1 receipt exists with a verdict.** `watch/inbox/REFEED_GUARD_B1_20260905.md`
      present + `mag/refeed_guard.py` on disk and wired into the `mag/lite_guard.py` tripwire.
      STATUS AT WRITE TIME: receipt ABSENT, `mag/refeed_guard.py` ABSENT — expected (B1 worker
      in flight). NO VERDICT = NO RE-ARM. If B1 slipped past Sep 8, re-arm waits for it.
- [ ] **P2 — meter clamp armed.** `mag/lite_guard.py` DEFAULT_CEILING = 1400 credits/day
      (law 15: 10,000/wk paced over 7 days). B1 tightens this to ~1,228/day (surviving pool
      after the refeed tax) — post-B1, expect the dynamic ceiling to read ~1228. Ledger
      `state/fuel/lite_pacing.jsonl` is created on first gated ride (absent at write time = OK);
      provider-side meter log `state/fuel/lite_quota_log.jsonl` live (757 B, 09-05 15:15).
- [ ] **P3 — registry row present.** `configs/auth_tracks.yaml` track `lite-rearm-sep8`,
      provider `builtin:zai-coding-plan`, due 2026-09-08T02:19Z. PRESENT (verified).
      NOTE: registry path is `configs/auth_tracks.yaml` — there is NO `state/auth_tracks.yaml`.
- [ ] **P4 — swarm default OFF Lite.** `mag/swarm_worker.py:54` →
      `DEFAULT_PROVIDER = "cerebras"` (Lite unhooked 09-05). Re-grep at T-0.
- [ ] **P5 — origin snapshot intact.**
      `state/auth_switchboard/20260905T161700Z_post_swap_broken_20260905/MANIFEST.json`
      sha256s match live files; marker `.mag_active_auth` = `post_swap_broken_20260905`.
- [ ] **P6 — key identity without echo.** `ZAI_API_KEY_Lite` resolvable via
      `mag/lite_guard.py:_key()` (fallbacks ZAI_API_KEY_L / _LITE / ZAI_API_KEY).
      Fingerprints only — NEVER print or paste the key (secrets-never-echoed law).

## RE-ARM STEPS (execute after 2026-09-08 02:19Z, in order; abort on first unexpected result)

1. **Provider meter read ($0, key-only, no browser).**
   `python -c "from mag.lite_guard import provider_quota; print(provider_quota(force=True))"`
   EXPECT: weekly pool refilled (remaining ≈ 10,000 credits / fresh subscription window).
   If 429 code 1310 "Weekly/Monthly Limit Exhausted" persists → ABORT, lane stays parked,
   file a drift row on the room board (reset time was wrong).
2. **One minimal lane probe.** Single short completion on `glm-5.3-flash` through the z_ai3
   path. EXPECT: HTTP 200 + real content. This lane is METERED — one ping, no bursts, no
   sustained probe scripts tonight.
3. **Auth map sweep.** `python -m mag.auth_switchboard status --all`
   EXPECT: `builtin:zai-coding-plan` PASS; dead set unchanged vs the 16:24Z receipt
   (`builtin:zai` code=1000, `builtin:zai-start-plan` 401 — those heal only via the
   operator's Google-tap / key paste, NOT via the weekly reset). Any NEW dead lane = ABORT.
4. **FREE_LANES row check (read-only).** `mag/fuel_feed.py` line ~77:
   `("z_ai3", "z_ai3", "glm-5.3-flash")` uncommented (it is already live — the lane died as a
   pool, not a row); CACHE_LANES resolves to `[z_ai3]`. Do NOT repoint anything yet.
5. **Guard gate dry-run.**
   `python -c "from mag.lite_guard import check; print(check('lite_rearm_manual'))"`
   EXPECT: `ok=true`, `ceiling` 1400 (≈1228 once B1's clamp lands), `spent` near 0.
6. **Refeed guard live check.** B1's ledger shows fresh rows with `refeed_ratio < 0.15`.
   Falsifier of record: >15% persisting 2 days WITH the guard live ⇒ guard is vapor, delete
   it, re-park Lite until rebuilt.
7. **Freeze the re-armed state.** `python -m mag.auth_switchboard snapshot lite_rearmed_20260908`
   (auto-appends a trail row to `memory/runs/auth_switchboard_trail.jsonl`, sets marker).
8. **Grow the registry, not the grammar.** Append a status line to the `lite-rearm-sep8` row
   in `configs/auth_tracks.yaml` citing this receipt + the probe outputs.

## VERIFICATION SUMMARY (command → expected output)

| Command | Expected |
|---|---|
| `python -c "from mag.lite_guard import provider_quota; print(provider_quota(force=True))"` | pool refilled, no 429/1310 |
| single glm-5.3-flash probe via z_ai3 | HTTP 200 + content |
| `python -m mag.auth_switchboard status --all` | coding-plan PASS; no NEW dead lanes |
| `python -c "from mag.fuel_feed import CACHE_LANES; print(CACHE_LANES)"` | `[('z_ai3', ...)]` |
| `python -c "from mag.lite_guard import check; print(check('lite_rearm_manual'))"` | `ok=true`, ceiling 1400/≈1228 |
| `python -m mag.auth_switchboard trail 3` | new snapshot + status rows post-02:19Z |

## ROLLBACK (re-park Lite — exact edits/commands)

1. `mag/fuel_feed.py` line ~77: comment the row —
   `# ("z_ai3", "z_ai3", "glm-5.3-flash"),   # PARKED 2026-09-08 (429 code 1310 wall persisted post-reset)`
   (mirror of the 08-29 pull; backup-first: the git-less repo convention is edit-after-snapshot, step 3).
2. `python -c "from mag.fuel_feed import CACHE_LANES; print(CACHE_LANES)"` → EXPECT `[]`.
3. Freeze forensics: `python -m mag.auth_switchboard snapshot lite_parked_20260908`.
   NEVER delete `state/fuel/lite_pacing.jsonl`.
4. NO daemon to kill (no-daemons law): in-flight explicit z_ai3 calls ride out; new enqueues
   default to cerebras (`mag/swarm_worker.py:54` stays untouched).
5. ⚠️ DO NOT set `LITE_DAILY_CREDITS=0` to park — that DISABLES the ceiling (unlimited spend,
   `mag/lite_guard.py:17`), the exact opposite. Operator emergency lever only.

## SPEND-GUARD ROW (standing, not step-scoped)

**Never let Lite hold automatic defaults — metered-until-receipted.** `DEFAULT_PROVIDER`
stays `cerebras`; rib_chat cache-mining stays off z_ai3 unless an explicit call; every Lite
credit is billable until a monitor read or billing row proves otherwise (the "zero-metered
night window" belief was falsified 09-05). Drift surface found 09-05: `mag/free_tier.py:52`
still lists z_ai3 with stale models `["glm-4.7-flash","glm-4.5-flash"]` — audit before any
door reads free_tier. Seats run `status`/`snapshot` only; `use` is typed-RESTORE, operator
hand only (never-edit-own-credentials law).

## TRI-STATE vs MEMORY OF RECORD (2026-09-05, evidence attached)

- **DISPUTED — "z_ai3 pinned glm-4.5-flash (08-27 audit)"**: stale. Current law:
  glm-5.3-flash, RELIT 09-04 "Calcifer", PACE-GUARDED 09-05 — `mag/fuel_feed.py:69-80`.
- **DISPUTED — "meter clamp 1,228/day live"**: live clamp is **1400/day** (`mag/lite_guard.py:35`);
  1,228/day is B1's post-guard tightening target (`watch/WEEKEND_BURN_BOARD_20260905.md` B1 row).
- **CORRECTED — registry path**: `configs/auth_tracks.yaml`, not `state/auth_tracks.yaml` (absent).
- **SUPPORTED — memory correct on**: coding-plan lane PASS / apikey code=1000 / start-plan 401
  (`state/auth_switchboard/20260905T162449Z_dogfood_b/MANIFEST.json`); organ
  `mag/auth_switchboard.py` status/snapshot/use (typed RESTORE, GO-gated)/trail;
  `DEFAULT_PROVIDER="cerebras"`; 4 snapshots pairwise hash-identical (determinism falsifier run 2).
