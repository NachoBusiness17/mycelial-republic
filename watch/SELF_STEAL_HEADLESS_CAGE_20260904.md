# SELF-STEAL — the headless-cage topology fix (2026-09-04 evening)

**ITEM:** Operator fired mid-boot: "OUR AGENTS ARE SPAWNING TERMINALS WHICH IS FINE BUT
THEY SHOULD BE HEADLESS AND THEY SHOULD BE IN THE CONTAINERS." → then "its still doing
it… self steal its probably sacred cows… you have mem." The order: debug the
terminal-spawn class as a SELF-STEAL (our own history holds the answer), and move all
recurring work headless + in-container. This card is the autopsy + the fix receipt.

## ROOT CAUSE — a sacred cow wearing new clothes

- The 09-04 "lanes visible" law (ZCode scheduled tasks as lanes) resurrected the
  **desktop-era pattern**: fleet work = host-side sessions that boot visible consoles.
  The BONES of the lane law (scheduled cadence, free flash, prompts-in-files,
  rebuildable) were right; the RUNTIME was the sacred cow.
- Two standing laws already banned this exact shape and were not consulted at design:
  - `feedback-docker-not-desktop` (2026-08-25): "this should all be in docker and not
    my desktop" — persistent fleet work never on the host desktop.
  - `feedback-headless-only` (2026-08-26): "windows keep popping up, fire headless" —
    any recurring host-side task = ZERO visible windows.
- Measured at 18:07 EDT: 13 ZCode.exe + ~40 console children (cmd/conhost) — every
  session (app window, automation fire, spawned background agent) boots the full MCP
  fleet as console-attached children. The automation fires (night shift ×17 runs,
  23/2/5) plus spawned background agents (6 dig workers 09-04 morning, my own 4
  cancelled Explore agents) = the window storm. Not a runaway loop — a birthright of
  the session model.
- mag/ core was ALREADY compliant (`mag/headless.py`, `guard_registry.py` enforces
  CREATE_NO_WINDOW on every spawn site) — the non-compliance lived OUTSIDE the guard's
  reach: harness session spawns + 19 spawn sites in watch//scripts/ that skip the law.

## THE FIX — the cage is the runtime (all receipted tonight)

`mag/lane_runner.py` (new): the in-cage, headless lane engine. Runs INSIDE
mag-sovereign via `docker exec -d`, one daemon (`--daemon`), no window on any OS.

- **Lanes in-cage:** research (monitor_lane + gated inbox triage), builder (ADOPT-2
  handoff gate on every drop), economist (hunger ledger + LAW-056 sweep escalation),
  bard_ledger (day ledger rows), elder (flash lens on newest cards), day_work (mirror
  + STALLED flags), night (composite, 23:00-09:00 window guard).
- **ADOPT-2 DELIVERED AS PART OF THE FIX:** `gate_drop()` = the charter-clause-9
  handoff gate — schema/ttl/anchor validation, tri-state trail row per drop, before
  the lane acts. Both builder ADOPT drops gated PASS tonight (gated=2).
- **LAW-058 pin baked in:** the only model door = Lite key (ZAI_API_KEY_L,
  glm-5.3-flash), reasoning_effort low + 1536 tokens (5.x law), endpoint SSRF-guarded,
  redirects refused. No paid lane reachable by construction.
- **Single-daemon guard:** pidfile lock (`logs/lane_scheduler.pid`) — the respawn-law
  lesson applied to my own organ (a racing double-daemon was caught and killed
  tonight; two elder rows at the same second was the tell).
- **Night automations DELETED** (automation-7e147056 night shift, automation-59704218
  night wheel) 30 min before their 23:00 fire — the window-source class is dead; their
  mechanical work lives in the cage night cycle. Deck narration (browser-bound) and
  android (adb-bound) stay seat/manual lanes BY DESIGN.
- **The six ZCode lane automations from the boot order: NOT armed** — superseded by
  this order before arming. Visibility moves to the surfaces that never sleep: lane
  trails + surfaces (mirrored to dashboard/static every cycle), dashboard lanes board,
  DAY_WORK_DIGEST.

## Mimosa findings honored in-artifact (7 blocks, all real)

SSRF ×3 (inbox URL fetch → https+public-IP+no-redirect guard `_safe_https_url`;
flash endpoint → same guard; urlopen → no-redirect `_OPENER`). Path traversal ×2
(cage hunger copy → pathlib resolve + parent containment). docker cp of source ×2 →
Write-tool staged copy in `watch/cage_bin/` instead.

## ORPHANS FOUND (each with a disposition)

- **O1 — usage sweep is HOST-DB-BOUND — OPERATOR DECISION (one word deep).** It reads
  `~/.zcode/cli/db/db.sqlite`, which no container can see. The cage reads its OUTPUT
  (watch/usage_sweeps/) and carries the LAW-056 escalation (fired tonight: 6 flags in
  the Sep-4 report, escalated once). Options: (a) read-only `~/.zcode` mount into the
  sovereign (compose change + recreate), or (b) ONE sanctioned VBS-hidden schtask per
  the headless-only pattern. Until then the sweep runs only when a seat is open.
- **O2 — march_228 in-cage needs an env door — WINDOWED.** march reads `.env`
  (unmounted in-cage) for its key; the cage night cycle logs its rc honestly. Same
  door as O1(a) fixes it (container env already HAS the keys — a tiny env-reading
  patch to march works tonight if wanted).
- **O3 — ADOPT-1 (tool-description tester) — QUEUED** in builder lane, gated PASS,
  ttl 09-06. Next in-cage build shift claims it via window_throttle.
- **O4 — daemon dies on container recreate — KNOWN, RE-ARMABLE.** One line re-arms:
  `docker exec -d mag-sovereign sh -c "python /app/mag/lane_runner.py --daemon >> /app/logs/lane_scheduler.log 2>&1"`.
  Recorded in RUNNING.md. The compose/entrypoint home for it is the durable fix
  (next container maintenance window, operator GO — restarts carry the bind-mount
  disease risk, not done tonight).
- **O5 — 19 spawn sites in watch//scripts/ skip CREATE_NO_WINDOW — ROUTED to builder
  inbox** (host-side scripts only matter when seats run them, but the guard registry's
  law should cover them; batch fix + guard extension).
- **O6 — lane cadence question — OPERATOR DECISION.** Cage defaults: research 15m,
  builder 30m, day_work 30m, economist 06:00, bard 20:00, elder 12:00. Different than
  the boot order's */15+*/30 for ZCode tasks — same intent, now container-side. Say
  the word and I reschedule in `SCHEDULE` (one dict, one line each).

## DUPLICATES (checked, folded — don't re-dig)

Windows-flash fix pattern → `feedback-headless-only` (VBS wrapper; not needed in-cage).
Container supervision → respawn law (ONE supervisor, in the cage — the lane daemon is
a worker organ holding a lock, not a supervisor). Free-lane call shape → march_228 +
fuel_feed (reused verbatim). ADOPT-2 → folded INTO lane_runner (this fix).

## GAPS / coverage

Did not audit: systemd/entrypoint in-cage persistence for the daemon (O4 covers the
re-arm), the ZCode app's own session-host spawn behavior (app-side, unreachable from
the repo), and whether other seats' open sessions still spawn background agents
(seat discipline note: this seat spawns NONE until the operator says otherwise).

**Verdict:** 1 sacred cow (host-session runtime) identified, killed at the source
(2 automations deleted before fire), and replaced by a cage-native engine that is
already doing real work (monitor rc=0, hunger rc=0, gates 2/2, elder lens 24s real).
Tri-state: the defect class = Supported (operator-observed + process census); the fix
= Supported (smoke receipts above); "windows never return" = Unproven until a night
passes with zero fires and the operator confirms a quiet desktop.

*— Sancho (flash-drive seat), 2026-09-04 22:3x local. Trail: queue/lanes/day_work/trail.jsonl.
Scratch: none — all work landed in-artifact.*
