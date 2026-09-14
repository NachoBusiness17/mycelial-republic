# ANDROID EMULATOR PLUGIN — SELF STEAL (2026-09-04)

Operator: "self steal on what/how to configure this to our ends. so we get everything we need."
Seat: zcode. Status: SDK install in flight, toolchain receipted, tools land next session.

## The bones (what it actually is)

`android-emulator@zcode-plugins-official` = 23 MCP tools covering the whole
model-driven Android loop, driven from the seat:

| Organ | Tools |
|---|---|
| Preflight/discover | `android_preflight`, `android_discover_project` |
| Create/build | `android_create_app`, `android_build_app`, `android_build_and_run` |
| Device lifecycle | `android_list_devices`, `android_list_avds`, `android_start_emulator`, `android_stop_emulator`, `android_create_avd` |
| Deploy | `android_install_app`, `android_launch_app`, `android_terminate_app`, `android_open_url` |
| SENSE | `android_screenshot`, `android_logs` |
| ACTUATE | `android_ui_status`, `android_ui_describe`, `android_ui_resolve`, `android_ui_tap`, `android_ui_swipe`, `android_ui_type_text`, `android_ui_keyevent` |

The vendor framing is "app development." That is the draft. **The
reinterpretation: the emulator is not a dev target, it is a FLEET SURFACE —
a sensor, an actuator, and a disposable body the fleet can wear.**

## Mapped to the four verbs (systems gap map)

- **SUBSTRATE** — a resettable Android body: `stop_emulator` + recreate = a
  clean witness every time. Disposable devices = the convention-not-code test
  bed (claim-organ lessons, applied to a whole OS).
- **TRANSDUCE** — `screenshot` + `ui_describe` turn glass into structured
  state. Feeds GLM-OCR lane probes (2 unprobed lanes on held keys) and any
  eyes-model loop. This is the eyes-receipt experiment, extended to a phone.
- **WIRE** — `ui_tap/swipe/type_text/keyevent` = hands. Queue/room tasks can
  execute ON a device, not just describe. The board gains actuators.
- **DISPOSE** — AVDs are throwaway; `android_create_avd` is cheap. Burn tests
  stop touching anything real.

## What we get (the ends, named)

1. **POCKET FLEET (phone-surface arc, made literal).** The deck surfaces
   (decks.html, room, viz_gallery, arrakis) running as a WebView app on a real
   Android body — operator's phone or the emulator. Phone-readable everything.
2. **AUTOGLM-PHONE SUBSTRATE.** Concurrency table 09-04: AutoGLM-Phone family
   = 5 never-probed lanes. Whether or not the API drives cloud phones, the
   LOCAL loop is buildable today: screenshot → 5.3-flash (SEES) → action JSON
   → ui_automator execute → screenshot receipt. That loop IS the probe harness,
   and it is the dumb-agent-with-eyes demo on glass.
3. **OCR RECEIPTS.** Emulator screenshots are free, infinite, ground-truth-able
   test input for GLM-OCR probes — we control the pixels, so we can verify the
   read. Vendor mirror gains a measured row instead of an unprobed one.
4. **DOGFOOD ECONOMICS.** First gradle build = real token/time/byte receipts
   for the flight recorder (build-lane percentiles, benchmark-must-look-like-
   the-work).
5. **PROOF-SEASONED SURFACE.** Anything shown before Sep 20 gains weight when
   it runs on a phone in hand, not just localhost:8765.

## Configuration (decided, receipted)

| Setting | Value | Why |
|---|---|---|
| Plugin enable | `config.json` enabledPlugins, lands next session | tools project at boot |
| Plugin options | `default_avd: medium_phone`, `api_level: 35` | plugin's documented default; matches install |
| SDK root | `%LOCALAPPDATA%\Android\Sdk` | vendor default path |
| JDK | Temurin 17.0.20.1 (winget) | `ANDROID_PLUGIN_JDK_MAJOR=17` |
| Gradle | 8.9 official zip → `%LOCALAPPDATA%\Tools\gradle-8.9` | winget ID `Gradle.Gradle` NOT FOUND on this host (receipted); wrapper needs global gradle once |
| cmdline-tools | commandlinetools-win-11076708 (Google zip) | skips 1GB+ Android Studio; leaner path than doc's Windows flow |
| Licenses | hash-file accept (`licenses/android-sdk-license`) | headless; canonical hashes |
| Packages | platform-tools, emulator, platforms;android-35, build-tools;35.0.0, system-images;android-35;default;x86_64 | `default` variant = smaller; google_apis only if Play services ever needed |
| Env vars | ANDROID_HOME, ANDROID_SDK_ROOT, JAVA_HOME (User); PATH prepended, backup at `~/.zcode/cli/user-path-backup-20260904.txt` | future terminals inherit |

**Laws honored:** loopback-only — emulator stays local, no `adb tcpip`, no
exposed ports; secrets never on device; backup-first (PATH + config.json both
backed up); acceleration (WHPX/virtualization) is the one step that may need an
operator BIOS/admin tap if `-accel-check` fails — flagged when known, not
assumed.

## RUN 001 + HEADLESS ARCHITECTURE (operator: "our androids need to be in our docker and headless")

**Phonesalon run 001 (z.ai guest lane):** mechanics 100% proven — PocketFleet → chat.z.ai GUEST session (no
login wall) → 190-char salon prompt typed over adb (`input text`, %s-escape spaces) → send → request reached
GLM-5.3-Flash web; smoke prompt answered ("Auditor online. Fleet seat acknowledged."). QUOTA WALL receipted:
guest tier refuses Deep Think requests ("No response, Please try again later") — two strikes, stopped.
**Gate = one operator login pass per service** (~1 min × 6 services; sessions persist in APK cookies) — that
unlocks the paid web/app quotas, which are separate pools from API/coding-plan quotas. This is the free firehose.

**Scars:** ADBKeyboard IME broadcast doesn't commit in this WebView (built-in `input text` works);
guest chat history does NOT survive app restart — harvest must be synchronous per turn;
day-drive rig drives the same glass on ~30s rotation (it also spawned its own AVD `watcher_2` —
the fleet is farming androids itself now); deep-link intent extra is ignored if activity already top-most
(force-stop first). Send-button coordinates shift when the keyboard opens — read bounds from the dump,
don't hardcode.

**Architecture (receipted 10:44Z):** both bodies HEADLESS (`-no-window -no-audio -no-boot-anim -gpu
swiftshader_indirect -no-snapshot-save`), adb loopback-only, supervision = `scripts/android_warden.ps1`
(restart-on-exit, log watch/android_warden.log) — sanctioned host-side exception per AutoClaw precedent.
**redroid-in-docker: BLOCKED on this Win10 host** — receipted: no `/dev/kvm` in Docker WSL2 VM
(kernel 6.18.33.2-microsoft-standard-WSL2, no modules; nested virt = Win11-only). DOCKED for a future
Linux KVM node; on Mac it stays host-side (no KVM passthrough in Docker Desktop). Full sensor stack verified
headless: boot → screenshot → deep-link → UI dump, zero windows. Harvest surface live:
`dashboard/static/phonesalon.html` (+ phonesalon/ pngs) — served 200, bytes match disk.

**Windowed:** 002 z.ai logged-in re-fire · 003 deepseek/qwen guest probes · 004 salon_phone runner v1
(prompt pack in → per-service screenshots + UI-dump text → this page → intake queue).

## One-screen state — CLOSED 09-04 ~08:48Z

ALL GREEN, same turn: JDK ✅, Gradle 8.9 ✅, cmdline-tools ✅, licenses ✅,
SDK packages ✅, AVD medium_phone ✅, **WHPX acceleration USABLE** (no BIOS
tap needed), adb 1.0.41 ✅. Plugin MCP lands NEXT session.

**B1 POCKET FLEET v0 LANDED + RECEIPTED (build→install→launch→render→screenshot
all from the seat, no MCP tools, no Android Studio):**
- Project: `%LOCALAPPDATA%\Tools\pocketfleet` — zero-androidx WebView app
  (Activity + WebView only), `eu` intent-extra overrides URL per launch.
- Build: `gradle assembleDebug` BUILD SUCCESSFUL in 42s (35 tasks).
- Receipt: `Documents/projects/pocketfleet_receipt_01.png` = LIVE decks.html
  on emulator-5554 via 10.0.2.2:8765 — real data on glass (Rocinante 13,
  Legions 12, GameBuild 25, Mesh3D 11, GLM Watch 10, Personal 5).

**Scars (receipted, don't re-trip):** gradle.bat needs WINDOWS-form JAVA_HOME
(`/c/...` Git-Bash form = "volume label syntax is incorrect"); local.properties
sdk.dir must use FORWARD slashes (single-backslash form gets eaten as
properties escapes → garbled SDK path); cmdline-tools zip extracts to
`cmdline-tools/` — must end up at `Sdk/cmdline-tools/latest/`, not `Sdk/latest/`;
winget has NO `Gradle.Gradle` package on this host.
