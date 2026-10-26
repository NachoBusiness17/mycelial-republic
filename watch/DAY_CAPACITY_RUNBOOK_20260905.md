# DAY CAPACITY RUNBOOK — Sat Sep 5, 2026 (orchestrator sweep)

Purpose: everything armed for the 11:00 EDT promo open (unlimited 5.3-flash in-ZCode,
8AM–6PM PT through Sep 20). Dogfood the fleet on itself, run at capacity, $0 beyond Max judgment.

## OPERATOR RULING — free-pool window cap (09-05, phone)
**~3 active windows is the free pool's limit; beyond that, auto-launch on Max.**
Capacity topology from here: ≤3 free-pool windows churn at once; any 4th concurrent lane
launches on the Max seat without asking. This is the overflow law — failover-to-Max extended
from failures to plain capacity.

## CAS GATE — VERIFIED OPEN (orchestrator re-run 09-05 ~09:2xZ)
`_tomb_move_if_same` at mag/bay_organs.py:180 (CAS call site :273); race harness re-run
independently by this seat: **3/3 PASS, exit 0** (RACE 20x2 double-claims=0, GRACE all true,
PARK-LIVE exactly one line). GO #1 closed. Tranche scale-up UNBLOCKED (food-gated as before).
Correction to the ponytail/lessig brief: fleet is **7 containers** measured (all healthy 9h),
not 8 — fix before it lands in the orchestrator brief.

## Fixed this morning (receipts in-repo)
| Defect | Fix | Receipt |
|---|---|---|
| "Captcha" on phone run = z.ai guest onboarding interstitial (Welcome/Google/Email/Github/Skip — NOT a captcha, no challenge) | already handled 08:12 by Android seat: load-wait poll + "Skip for now" tap | dashboard/static/phonesalon/runs/20260905T121139Z_zai_wall.png |
| Send leg blind-tapped; prompt never sent (icon-only `View` sender absent from stale dumps; Enter = newline in WebView) | confirm-and-retry: tap → input-cleared = send receipt → retry x3; desc-based fallback sender | runs/20260905T123238Z_zai_p1.png, queue/phonesalon_runs.jsonl |
| Prompt echo scooped into answer block | extract_answer skips nodes containing prompt[:30] | scripts/salon_phone.py |
| Teaching recorder ate its own pulls silently (MSYS rewrote /sdcard/... → C:\...\Git\sdcard\...) + hung 9h on an unguarded adb call | MSYS_NO_PATHCONV=1 export + per-call timeouts (200s record / 60s pull) + pull-size verification, failures now print | scripts/teach_recorder.sh — fix proven live 09-05 (guarded pull OK; unguarded rm demonstrably mangled to C:/Program Files/Git/...) |
| phonesalon/lanes/mesh_gallery invisible to shelf browsers (served-not-wired) | wired into nav.js single source | http://127.0.0.1:8000/static/nav.js (live, 200) |

## Day-review reconciliation (Android Surface seat's full accounting, folded)
- Send-field note "text, not desc" reconciled: the sender is a TEXT-labelled View ('Send Message'); the seat's probe-3 fix + this seat's input-cleared receipt/retry compose — layered fix proven by the 08:32 live run.
- **Guest lane wall (standing):** guest tier refuses Deep Think ("No response, please try again later", two-striked per law). Guest = basic prompts only; Deep Think + full quotas unlock on the operator's ~6-min login pass (never Nacho, skip Google SSO, fresh accounts per service per the ToS read).
- redroid: hardware-blocked on Win10 (no /dev/kvm in WSL2, receipted) — docked for a Linux KVM node, Rocinante day-one candidate.
- Next in lane stays: operator login pass → `--all` across six services → first real salon through the firehose.

## Runner proof (dogfood receipt)
2 end-to-end guest runs on emulator-5554: manual send validation ("Ping acknowledged —
receipt confirmed from the fleet seat runner.") + patched-runner run (answer harvested clean).
Runner laws embedded: guest-only, stop-on-challenge, jittered cadence, per-service caps, bounded window.

## State verified this sweep
- Night watch: automation-a5e12eea active, runCount 0, first fire tonight 23:00, seal folded. CronList = 2 active (night shift + vast verdict). Lite probe f9d31e30 COMPLETED Sep 4.
- Fleet: 7/7 containers up 9h, seal verified:true (01:23, OTS anchor, 19 files), chain 7,243 knots.
- Intake: gap=0, 100% dispositioned; INBOX empty.
- OpenAlex 429: patched (mailto polite pool + 3600s cooldown); IP box decays ~09:23 local — recovery confirm rides the next natural monitor pass after that. Do not re-probe before decay.

## 11:00 promo open — capacity order
1. Bulk work rides in-ZCode 5.3-flash: backlog feeds + intake cards + card-worker churn (up to 6 concurrent, $0).
2. Phone salon batches: bounded guest runs (start cap 3/service/day), zai + deepseek services; harvest feeds dashboard gallery + intake queue. Stop-on-challenge = law.
3. GA gen 3: ARMED, PENDING OPERATOR WORD (frozen arc, "resumable on your word" — not self-launched).
4. Sep 20 sovereign-benchmark build spec: the proof artifact; pull forward into the promo windows.

## Operator-hand debts (unchanged)
Lite billing-row glance (settles promo-covers-Lite) · Mir textbook (Drive wall) · PAIR install-doc read ·
scheduler re-arm fresh chat · canon README rows (Research seat's hands).

## Standing laws honored
HONEST-AUTH-WALL (never fake past login/captcha) · served-not-wired (wired at fix time) ·
liveness check in every steering pass (CronList) · lite lane dead until Sep 8 02:19Z reset ·
premium = judgment only; bulk = free lanes.
