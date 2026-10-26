# BUILD DISCIPLINE LAWS

Five anti-rot rules, already machine-enforced in their home estate — so they transfer
as runnable mechanics, not advice. Two of them are commands you can drop into a
pre-push hook today.

## The five rules

| # | rule | enforcement |
|---|---|---|
| 1 | **Spec before behavior change.** The doc/spec that owns a behavior is updated BEFORE the code that changes it. No orphan behavior. | review law; no tool can order this for you |
| 2 | **No timeouts papering over sync problems. No fallback-branch creep.** Found a design defect → align and fix the design; never add another guard branch to mute the symptom. | review law; delete a layer before guarding it |
| 3 | **Fix comments carry the receipt.** A bug fix's comment names the cause AND the evidence it was fixed on — not just what changed. | review law |
| 4 | **Violation ratchet at pre-push.** Registered debt passes; NEW debt blocks the push. | `python tools/violation_ratchet.py check --changed` over `mag/`+`tools/`; debt accepted by name via `baseline-update --by <who>` into `configs/violation_baseline.json`; `prune` recovers fixed debt. Never loosen the hook. |
| 5 | **Boot-freshness window.** Boot docs go STALE at >7 days while the repo has a heartbeat. Refresh with today's truth, or register frozen with reason+date. | `python tools/freshness_check.py` |

## Why a ratchet and not a ban

A ban fails the day it meets reality and gets loosened. A ratchet starts where the
estate actually is: existing debt is registered BY NAME (who accepted it, so debt has
an owner), and the only forbidden direction is backward. "Never loosen the hook" is the
whole trick — the gate may only ratchet tighter.

## Why boot docs need a freshness law

A stale boot doc is worse than none: the next session obeys it confidently. The 7-day
window with a registry escape ("frozen, reason, date") keeps the escape honest too.

## Receipt

- AGENTS.md:97-107 (estate), "Build discipline (landed 2026-09-25)" — core rules :101-105,
  ratchet command :104, freshness command :105 — read this session.
- The two commands (`tools/violation_ratchet.py`, `tools/freshness_check.py`) are cited
  from that section as the estate runs them; the seed ships the laws + command shapes,
  not those tools.
