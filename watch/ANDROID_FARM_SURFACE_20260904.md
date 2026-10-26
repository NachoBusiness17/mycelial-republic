# ANDROID FARM SURFACE — full research steal (2026-09-04)

**OPERATOR ASK:** "We already have a Pro account and we just need to use it inside
our Android environment. Once we can run one android then 2-4 etc. Full research
steal on this please as a swarm fleet companion. Imagine if the dumb agent GPS
wasn't actually fiction — we could give them all an android surface they either
can share or dunno."
**Seat:** zcode (watcher/research window). **Status:** farm of 2 LIVE + receipted;
Pro-on-glass plan named; X login is the operator's one hand.

## WHAT LANDED THIS TURN (receipts, not plans)

- **TWO androids on the box simultaneously**: `emulator-5554` (medium_phone, the
  B1 body) + `emulator-5556` (watcher_2, created + booted this turn). Both
  `sys.boot_completed=1`. Screenshots: `Documents/projects/farm_receipt_5554.png`,
  `farm_receipt_5556.png`.
- **Mock GPS works**: `adb -s emulator-5556 emu geo fix -122.4194 37.7749` → OK
  (watcher_2 now "sits" in San Francisco). The agent-GPS riff is not fiction.
- **RAM math**: 35.4/64 GB used with ALL of it running (8 fleet containers + 2
  emulators + this seat). Each headless body ≈ 2.5-3 GB → **4 bodies fit with
  ~20 GB headroom**. CPU (8-core/16-thread WHPX) is the real ceiling — measure
  under load before going past 4.
- Second-AVD start via the plugin MCP tool hits the 30s tool wall — emulator
  still boots; `adb devices` is the honest check. Scar filed.

## THE READ (steals, in priority order)

### 1. UI-as-API — the app IS the undocumented endpoint
Every wall we keep hitting (fxtwitter conversation endpoint walled, Shadertoy
hard-walled, ATS JSON behind JS walls) exists because we probe from outside. A
logged-in X app on a real Android body speaks the API from INSIDE the
attestation perimeter — device identity, session, Pro entitlement all carried by
the app itself. No reverse-engineering, no scraper arms race. The watcher
pattern flips: don't fetch the feed, BE a phone that has the feed.
**Supports the whole media-surface arc**: For You, Grok-in-app, trends,
notifications, DMs — surfaces with no web door at all.

### 2. AutoGLM-Phone — the vendor sells the phone-driver, and we hold the keys
From the local mirror (`guides/vlm/autoglm-phone-multilingual.md` + STEAL_ZAI doc):
- **Supported apps list includes X** (also TikTok, Reddit, Instagram, Quora —
  50+ apps). The vendor-driver officially drives our primary watch target.
- 10 action primitives incl. **`Take_over` = "request manual takeover
  (login/captcha)"** — HONEST-AUTH-WALL as a first-class action. Login is the
  operator's hand, by vendor design.
- Client-side runner is open source (`zai-org/Open-AutoGLM`): harness runs on
  OUR box, only the brain is theirs, per-step telemetry fully ours. Concurrency
  5, **"free for a limited time"** → $0 probe owed.
- Composes with our own loop: `android_ui_describe` (AX tree) + 5.3-flash free
  lane. AX-RESOLVE OVER PIXEL-GUESS law already proven on glass today.

### 3. Sharing architecture — STF pattern (DeviceFarmer)
"They either can share or dunno" → both, and the industry already solved it:
[STF / Smartphone Test Farm](https://github.com/openstf/stf) = a pool of bodies
+ a web remote-control queue where operators CHECK OUT a device. The steal for
us: bodies are a shared fleet RESOURCE behind our queue (room/contract files),
routed by a thin adb dispatcher — `adb -s emulator-XXXX` per task. Round-robin
first; claim-organ semantics after the CAS fix lands (split-brain receipt on
file). Per-agent dedicated bodies are the luxury tier of the same router.

### 4. Topology law for the Pro account — ONE golden body, N anonymous bodies
Detection research (Multilogin/DuoPlus/anti-detect trade + X "inauthentic
behavior" wave reports): identical emulator fingerprints running the same
account get **identity-linked**; same account on many devices simultaneously
risks login lockouts. X tolerates the same account on a phone + laptop (normal
human shape), not 4 clones in lockstep.
**Therefore: the Pro login lives on exactly ONE body (the primary watcher).
Never clone a logged-in disk image.** Other bodies stay logged-out surfaces
(pocketfleet WebViews, logged-out X browsing, other apps) or take the login
only via Take_over + operator hand. Fresh AVDs per role, distinct device
profiles when we diversify.
**Extra weight:** @NachoQuixotic is the CANON account (chain v0 shadow ledger).
A ban would burn the canon, not just a lane. Firewall below.

### 5. Fair-use firewall (named before first drive)
- Watchers READ. Bookmark = the one write gesture (already the operator's
  bookmark=feed-me protocol) — human-rhythm jitter, nothing else automated.
- Posting, replies, follows: human hand only. Ever.
- Pace = one body behaving like one person with a job; no 24/7 scroll, no
  burst-fetch. Night-shift cadence, not wall-clock saturation.
- Take_over on any captcha/challenge — never fake past a wall (vendor law too).
- Loopback only: no `adb tcpip` outside the box, no tunnel to the bodies.

### 6. Geo-steered watchers (the GPS thread, made real)
`emu geo fix` receipted. Each body can sit in a different city. Whether X's
local surfaces (trends, "near", ads) actually move with hardware GPS vs the
in-app trend-location setting is **Unproven — F5 probe**: two bodies, two
cities, diff the surfaces. If it holds, every deck gains a geo dimension
(watch SF/Austin/London scenes without leaving the box).

### 7. Prior-art map (what others built, what we take)
| Project | What it is | The steal |
|---|---|---|
| [Mobile-Agent-v3 (X-PLUG)](https://github.com/x-plug/mobileagent) | screenshot-first multimodal phone agent, planning/progress/reflection multi-agent | the planner/executor split for our free-lane loop |
| [AppAgent (Tencent)](https://github.com/TencentQQGYLab/AppAgent) | CHI 2025, learns apps by exploration into an interaction knowledge base | the per-app knowledge doc — our deck playbooks |
| [AutoDroid (MobiCom'24)](https://github.com/MobileLLM/AutoDroid) | LLM + UI transition graphs for task automation | UI-graph memory = reusable navigation receipts |
| [AndroidWorld (Google)](https://github.com/droidrun/android-world) | 116-task live-emulator benchmark with automatic verification | THE falsifier harness — task success receipts for agents-on-glass |
| [DroidRun/MobileRun](https://github.com/droidrun/mobilerun) | framework for LLM agents controlling phones | confirm our organ shape against theirs |
| [DeviceFarmer STF](https://github.com/openstf/stf) | device farm, browser remote control, checkout queue | the sharing router (above) |
| redroid (Android-in-Docker) | fleet-native body — but WSL2 stock kernel lacks `binder_linux` → [custom kernel build required](https://github.com/remote-android/redroid-doc/issues/899) | DOCKED to Rocinante/Linux era; today = host AVDs |

### 8. B2/B3 compose (already windowed this morning)
The farm extends, not replaces: B2 eyes-on-glass (screenshot→OCR/5.3-flash
read) and B3 AutoGLM-Phone loop now have TWO bodies to run on. Emulator
screenshots remain free infinite ground-truthable OCR test input.

## BUILDS

- **F1 FARM OF 2 — DONE THIS TURN** (receipts above). Kill line:
  `adb -s emulator-5556 emu kill` (leaves the primary watcher body running).
- **F2 X-APP BODY — WINDOWED, one download + one operator hand.** Current image
  is `default` (no Play services); X app needs the `google_apis` variant:
  `sdkmanager "system-images;android-35;google_apis;x86_64"` (~1.5 GB, same
  class as this morning's GO'd install) → new AVD → X APK via Aurora Store /
  APKMirror (keeps Google account OFF the body) → **operator logs in via
  Take_over, once, his hand** (never agent-touched creds). Snapshot AFTER
  login stays on ONE body (topology law).
- **F3 STF-LITE ROUTER — WINDOWED.** Queue file ↔ `adb -s <serial>` dispatch,
  round-robin now, claim-organ semantics post-CAS-fix. ~100 lines in mag/.
- **F4 AUTOGLM-PHONE ON THE FARM — WINDOWED ($0, "free for limited time").**
  Probe = daytool ladder on body 2 (already the named dogfood) + one X hunt on
  the logged-in body, Take_over armed.
- **F5 GEO-DIFF PROBE — WINDOWED, $0.** Two cities, diff surfaces, receipt.

## TRI-STATE

- 2-body farm + geo fix + RAM math: **Supported** (receipts this turn).
- AutoGLM-Phone driving our emulator incl. X: **Unproven** (door documented,
  lane untried — F4).
- X surfaces moving with hardware GPS: **Unproven** (F5).
- Same-account-on-many-bodies detection risk: **Supported** (trade docs + ban
  reports; shape is emulator/linking-based).
- 4-body fit on this box: **Supported by RAM math, Unproven under CPU load**
  (measure at 4).

## VERDICT + SCORE: 22/25 BUILD

Substrate paid and live, driver vendor-supported for X, sharing pattern
solved, detection topology named, canon-account firewall explicit. The only
gates: one 1.5 GB download (F2), one operator login hand (F2), CAS fix for
full claim semantics (F3 luxury tier).

*Filed by the zcode seat, day 09-04. Composes with
ANDROID_EMULATOR_SELF_STEAL_20260904.md (substrate) and
STEAL_ZAI_SYSTEMS_AUTOMATE_20260904.md (AutoGLM-Phone receipts).*
