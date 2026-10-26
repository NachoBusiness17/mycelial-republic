# METHODS.md - broken-screen data transfer sweep (Moto G 5G 2024, Windows 10 PC with adb)

Date: 2026-09-29. Scope: external methods research for pulling "everything" off a Moto G 5G (2024) that boots, is already unlocked/security-passed, but whose screen cannot be navigated by touch reliably. No SD card assumed. USB-C port. PC is Windows 10 with full Android SDK platform-tools (adb) installed.

Tri-state legend: [CONFIRMED] = stated by a source above or vendor documentation. [LIKELY] = consistent across multiple secondary sources but not vendor-confirmed here. [UNVERIFIED] = could not be confirmed in this sweep; treat as hypothesis and test on the device.

Note on "adb 37": any platform-tools release from 34 onward fully supports Android 14 devices; the adb version is not a factor for any method below. [LIKELY]

---

## 1. scrcpy route

### Does scrcpy work on the Moto G 5G (2024), Android 14?
Yes. scrcpy requires Android 5.0 (API 21) or higher; Android 14 is well inside support. [CONFIRMED, https://github.com/Genymobile/scrcpy README]

### Does it need USB debugging?
Yes for normal mirroring mode. The README prerequisite is "Make sure you enabled USB debugging on your device(s)". [CONFIRMED, https://github.com/Genymobile/scrcpy]
Exception: `scrcpy --otg` simulates a physical USB keyboard and mouse over the AOA/HID path and explicitly does NOT require USB debugging. It is control-only (no video mirror). [CONFIRMED, https://github.com/Genymobile/scrcpy; https://www.mcbluna.net scrcpy v2.6 notes]
This makes scrcpy itself part of the unlock path on a phone where debugging was never turned on: `scrcpy --otg` over USB turns the PC mouse into the phone's mouse, which you then use to enable Developer Options and USB debugging. [CONFIRMED for the mechanism; UNVERIFIED for smoothness on this exact Moto model, test it]

### What happens with an unauthorized / unaccepted RSA prompt?
- adb will report the device as "unauthorized" and scrcpy will fail to start until the "Allow USB debugging?" RSA fingerprint dialog is accepted on the phone screen. The dialog is a normal UI tap, so a USB mouse (OTG) or unreliable touch can accept it. [CONFIRMED, standard adb behavior; https://xdaforums.com broken-screen threads]
- Silent path: adb trust is keyed to the host's `~/.android/adbkey` / `adbkey.pub` pair and persists on the phone. If THIS Windows PC previously authorized this phone, reconnecting produces no prompt at all and `adb devices` shows "device" immediately. Keep those two files safe; copying them onto a new PC restores the trust. [CONFIRMED, adb documentation behavior]
- If unauthorized and no input path exists, adb and scrcpy are dead ends until you get an input device onto the phone. [CONFIRMED]

### Can it control with mouse and keyboard?
Yes, full mouse and keyboard control over USB or TCP/IP, including right-click = BACK and middle-click = HOME. Audio forwarding works on Android 11+. [CONFIRMED, https://github.com/Genymobile/scrcpy]

### Does mirroring work if the phone's own display panel is damaged?
- scrcpy captures the composed frame at the encoder/compositor level, not from the panel. The README lists "mirroring with Android device screen off" as a supported feature (`--turn-screen-off`), which proves capture does not depend on the physical panel being powered on most devices. A dead or disconnected panel therefore usually still mirrors fine. [CONFIRMED for the screen-off feature, https://github.com/Genymobile/scrcpy; LIKELY for the dead-panel generalization, widely reported in broken-screen threads but device-dependent]
- Known black-frame causes: secure/DRM-flagged apps (banking apps, Netflix) always mirror black. [CONFIRMED, https://github.com/Genymobile/scrcpy issue 3072]
- If the main display capture comes up black on this unit, try `scrcpy --new-display=1920x1080` (virtual display, Android 10+; renders a fresh display independent of the physical one). Also `scrcpy --no-video` for audio-only. [LIKELY, from scrcpy v2.x/4.x feature docs; test on device]
- Caveat: a small number of devices stop compositing when the panel is physically disconnected; no authoritative list exists. [UNVERIFIED]

---

## 2. Enabling USB debugging without touch: ranked options

Ranked by practical speed and reliability for this case (phone unlocked, boots, touch unreliable):

1. **USB-OTG mouse (wired, ~USD 8 adapter + any mouse).** Plug mouse into phone via OTG; a cursor appears on the phone immediately with no settings, no pairing, no adb trust involved. You then see-and-click: Settings > About phone > tap Build number 7x > back > System > Developer options > USB debugging ON > plug into PC > accept RSA dialog with the mouse. Works even if the display is partially readable; works from the lock screen on most devices. Moto G 5G (2024) supports USB OTG. [CONFIRMED for the method and widespread recommendation: https://xdaforums.com, https://android.stackexchange.com, https://www.tenorshare.com; LIKELY that this specific model supports OTG: listed in its spec sheets, verify on device]
2. **Bluetooth mouse previously paired.** If a BT mouse was paired before the break, most phones reconnect it automatically at boot, giving the same cursor without any hardware purchase. Zero cost, second fastest. [LIKELY, commonly reported; depends on the mouse auto-reconnecting]
3. **`scrcpy --otg` from the PC.** Same result as option 1 using the PC's own mouse over USB, no debugging required. Fails if adb is wedged in a weird half-unauthorized state; if it does not start, fall back to a real OTG mouse. [CONFIRMED capability, https://github.com/Genymobile/scrcpy; UNVERIFIED on this model]
4. **TalkBack + external keyboard.** Only viable if TalkBack was already enabled or the volume-key accessibility shortcut (hold both volume keys 3 s) was configured before the break; then a USB or BT keyboard can drive focus (Tab / arrows, Enter to activate) to reach Developer options. Fiddly and screen-reader-chatty, but fully non-visual. [LIKELY, accessibility docs and forum reports; UNVERIFIED that TalkBack was enabled on this phone]
5. **Blind tap sequences from memory.** Tap Build number 7x, back, System, Developer options, USB debugging, using coordinates counted from memory with unreliable touch. Works sometimes; people do land it. Highest failure risk of the no-hardware options. [LIKELY, widely described in forum guides; inherently low confidence]
6. **Cast to TV / Windows "Connect" app (Miracast).** Moto G 5G (2024) supports wireless cast; Windows 10 can receive Miracast via the optional "Wireless Display" feature. Solves visibility, not input: you still need a mouse or unreliable touch to pull down quick settings and tap the Cast tile blind. Rank last because every step before it already assumed some input. [LIKELY; UNVERIFIED tile-by-tile path on this model]

Note: adb-over-Wi-Fi (`adb connect ip:5555`) only helps if `adb tcpip` was enabled on the phone before the break; it cannot be switched on remotely. [CONFIRMED, adb behavior]

---

## 3. MTP route (no USB debugging)

- Default behavior when you plug an unlocked Android into a PC: USB mode starts as "charging / no data transfer". The PC sees nothing to browse until the phone-side USB notification is tapped and File Transfer is selected. A locked phone exposes even less. [CONFIRMED, https://drecov.pandaoffice.com broken-screen guides; standard platform behavior]
- Escape hatch: Developer options > "Default USB configuration" persists a choice. If File Transfer was set there before the break, plugging in auto-selects MTP with no tap. [LIKELY, platform behavior; UNVERIFIED what this phone had set, check by plugging in first]
- With the phone unlocked and unreliable touch, tapping the notification is realistic but error-prone; with an OTG mouse it is trivial.
- What MTP can pull (Android 14): DCIM, Pictures, Download, Documents, recordings, and `Android/media` (this includes WhatsApp chat databases at `Android/media/com.whatsapp/WhatsApp/Databases` and its media). [CONFIRMED for user storage; Android/media visibility over MTP is standard]
- What MTP cannot pull: `Android/data` and `Android/obb` are hidden from MTP on Android 11+ (strictly on 13/14), all app-private data, `/data/data` (SMS and call-log databases), and anything under app-scoped storage. [CONFIRMED, scoped storage behavior since Android 11]
- adb pull, once debugging is on, gets the entire `/sdcard` tree including `Android/data`, which MTP will not show. SMS and call-log databases still are NOT readable by plain adb shell on a production build; you need an app (see section 4) or root. [CONFIRMED]

Practical MTP-vs-adb summary: if MTP comes up for free (persisted default), use it for photos/videos/Downloads while adb is being sorted. Otherwise do not spend time tapping the notification; one OTG mouse gets you debugging, which supersedes MTP for everything except convenience.

---

## 4. What "everything" includes, best tools per category (2026 state)

| Category | Best route | Notes |
|---|---|---|
| Photos, videos, Downloads, Documents | MTP drag-drop or `adb pull /sdcard/DCIM` etc. | If Google Photos backup was on, the cloud copy already has it; check photos.google.com first. [CONFIRMED approach] |
| Full user storage incl. `Android/data` | `adb pull /sdcard/` (once debugging on) | MTP will not show `Android/data`. [CONFIRMED] |
| SMS + call logs | Install "SMS Backup & Restore" (or similar) APK via `adb install` once debugging is on, drive the app by scrcpy mouse, export XML to /sdcard, `adb pull` it | `adb install` needs no on-screen confirmation; driving the app's UI needs scrcpy or the OTG mouse. Plain adb cannot read the telephony provider on a production build. [CONFIRMED mechanism, LIKELY for zero-prompt adb install] |
| App data, general | `adb backup` is deprecated (warning printed since ~platform-tools 31; many apps opt out with allowBackup=false) but still functions on Android 14 if you accept the on-device "Full backup" confirmation dialog (tap it via scrcpy). Extract with an `.ab` unpacker (abe, hoardy-adb, zlib-flate). Expect partial coverage. | [CONFIRMED deprecated-but-works: android.googlesource.com diff, https://gist.github.com/AnatomicJC/e773dd55ae60ab0b2d6dd2351eb977c1, hoardy-adb] The post-adb-backup reality: Google One backup (Settings > Google > Backup > Back up now) carries app list plus data for participating apps to the replacement phone; per-app in-app exports cover the rest. [CONFIRMED direction, per Google guidance] |
| WhatsApp | Google Drive backup (drive.google.com shows it under Storage > Backups) + local copy under `Android/media/com.whatsapp/` pullable by MTP or adb | Restore on new phone with same number + Google account. Trigger "Back up now" via scrcpy before pulling. [CONFIRMED, https://www.imyfone.com + standard docs] |
| Signal | New (Sept 2025) Signal Secure Backups: E2E-encrypted cloud backup restored with the recovery key on the new phone; legacy local encrypted backup file also possible | Recovery key is mandatory; losing it loses the backup. [CONFIRMED, https://support.signal.org] |
| 2FA Google Authenticator | In-app: three-dot menu > Transfer accounts > Export accounts, shows QR to scan from the new phone (do it through scrcpy so you can frame it). If GA cloud sync was enabled, accounts already follow the Google account. | [CONFIRMED, https://www.allthingssecured.com, Microsoft learn guides for the parallel MS Authenticator flow] |
| 2FA Authy | Enable Multi-Device, add the new device, approve from the old device (approve tap via scrcpy or OTG mouse), then disable new-device additions. | [CONFIRMED, https://www.twit.community and Authy docs] |
| 2FA Microsoft Authenticator | No export; re-enroll each account individually. | [CONFIRMED, https://learn.microsoft.com] |
| Tailscale | App config travels with the tailnet, not the phone; nothing to extract. Re-login on the replacement or reconnect on this one (section 5). | [CONFIRMED by Tailscale's account model] |
| Offline maps | Not extractable without root (app-scoped). Re-download areas on the replacement. | [LIKELY, app-scoped storage rules] |
| Wi-Fi, accounts, settings | Google One backup covers Wi-Fi networks, apps, call history, SMS (optional), device settings; restored during new-phone setup. | [CONFIRMED, standard Android backup] |

Dead ends to not waste time on: Helium-style backup apps (dead post-Android 5), Samsung Smart Switch (Samsung-only host/device pairing, and it needs on-device consent screens), chip-off or forensic suites without root (overkill for an unlocked, working phone).

---

## 5. Tailscale angle

- Short answer: no remote wake exists. Tailscale on Android is a local VPN service; once the tunnel is down there is no external channel to tell the device to reconnect. The admin console can show it as expired/offline but cannot bring it up. [CONFIRMED by architecture and community answers; no Wake-on-LAN equivalent for Android exists, see WOLE discussion https://github.com]
- Conditional exceptions, each requiring something to have been set up BEFORE the break: adb-over-Wi-Fi previously enabled (`adb connect ip:5555`, then `am start` the Tailscale app and tap Connect via scrcpy); Termux with sshd and tailscale already installed (ssh in, reconnect from CLI); Tasker/MacroDroid automation already configured to revive the VPN. If none of these were pre-installed, they cannot be installed without screen+adb access. [LIKELY; UNVERIFIED what this phone had]
- Practical: the tailnet node is dead until the screen is navigable. Once scrcpy works, open Tailscale, toggle connect, and the node returns; its config (tailnet policy, MagicDNS name) is server-side and survives. Last-seen 17 days ago matches a phone that is simply off Wi-Fi or asleep with the VPN dead; it will also self-heal the moment the app is foregrounded and connected. [LIKELY]
- Prevention note for the replacement: enable always-on VPN, block-without-VPN, and unrestricted battery for Tailscale so this does not recur. [CONFIRMED recommendation across sources]

---

## 6. Motorola-specific

- Ready For / Smart Connect: the Moto G 5G (2024) is a budget-tier model and is NOT on Motorola's Smart Connect full-support list; those features are reserved for Edge, Razr, g100/g200, and select stylus/power variants. So there is no Moto desktop-mode backdoor for this case. [CONFIRMED for the chart's structure, https://en-emea.support.motorola.com Smart Connect Compatibility Chart; LIKELY that g5g-2024 specifically is excluded, verify the chart row before relying on it]
- USB-C to HDMI: the Moto G 5G (2024) has a USB 2.0 port without DisplayPort Alt Mode, so a USB-C-to-HDMI cable will NOT carry video. Wired external-display recovery is out. [LIKELY, model-class spec; community tables list it as no video out; UNVERIFIED against an official Motorola spec sheet]
- Wireless cast: the phone has a Cast tile (Miracast/Chromecast) independent of Smart Connect; usable only if you can tap it blind or by mouse. [LIKELY]
- Moto automatic backup: no Moto-specific device backup product; Motorola relies on the standard Google One backup (Settings > Google > Backup). Motorola Migrate was retired years ago. [LIKELY, consistent across Motorola support pages; no Moto branded backup found in this sweep]
- Broken-screen recovery, Moto-flavored: nothing Moto-specific exists beyond the generic adb/scrcpy/OTG paths; forum consensus for Moto hardware is OTG mouse, scrcpy, or a cheap temporary screen swap purely to unlock and copy. [LIKELY, https://android.stackexchange.com Moto threads]

---

## 7. Ranked action plan for THIS case (unlocked, boots, touch unreliable, Windows PC with adb, tailnet node offline)

Ordered by time-to-data. Run each gate before spending effort on later steps.

1. **Plug USB, run `adb devices` (30 seconds).** If it shows "device" (this PC authorized previously): run `scrcpy` now, skip to step 4. If "unauthorized": accept the RSA dialog with the unreliable touch or a mouse (step 3) then continue. If "no devices": go to step 2.
2. **Check MTP for free data (2 minutes).** Look at the PC for a phone entry in Explorer. If it appears with folders, the persisted Default USB Configuration was File Transfer: drag DCIM/Pictures/Download/Android media off immediately via MTP while continuing with the rest.
3. **Get a mouse onto the phone, then enable debugging (15 minutes plus any shipping time).** Fastest: `scrcpy --otg` using the PC mouse over USB, else a wired USB-OTG mouse, else a previously paired BT mouse. With the cursor: Settings > About phone > Build number x7 > back > System > Developer options > USB debugging ON. Replug; accept the RSA prompt with the mouse. Then `adb shell svc power stayon usb` to keep it awake.
4. **`scrcpy` mirror + control (5 minutes).** If the panel mirrors black, retry with `scrcpy --new-display=1920x1080`. From here every on-screen prompt is clickable from the PC.
5. **Bulk storage pull (20 to 60 minutes):** `adb pull /sdcard/` to the PC (covers DCIM, Download, WhatsApp media, Android/data). Keep the phone on the charger.
6. **SMS + call logs (15 minutes):** `adb install` SMS Backup & Restore APK, drive it via scrcpy, export XML to /sdcard, `adb pull` it.
7. **In-app exports via scrcpy (30 to 60 minutes):** WhatsApp "Back up now" to Google Drive; Signal Secure Backup (save the recovery key); Google Authenticator Transfer accounts QR captured from the scrcpy window; Authy multi-device approve; then Settings > Google > Backup > Back up now for the Google One snapshot.
8. **Tailscale last (2 minutes):** with scrcpy control, open Tailscale, connect. The node rejoins the tailnet; do this after bulk pulls so the phone is idle on Wi-Fi. Optional `adb backup -all` attempt in the background if you want the deprecated path too; expect partial coverage.

Single most important fact: `scrcpy --otg` gives the phone a working mouse over plain USB with USB debugging OFF, which collapses the entire "enable debugging without touch" problem into a few clicks; and if this PC ever authorized the phone before, `adb devices` already shows "device" and the whole job starts at step 4.

---

## Sources

- scrcpy README (prerequisites, --otg, screen-off mirroring, control, audio, TCP/IP): https://github.com/Genymobile/scrcpy
- scrcpy secure/DRM black-frame issue: https://github.com/Genymobile/scrcpy (issue 3072)
- scrcpy v2.6 --otg and audio notes: https://www.mcbluna.net
- OTG mouse / broken-screen enablement threads: https://xdaforums.com, https://android.stackexchange.com, https://www.tenorshare.com, https://drecov.pandaoffice.com
- adb backup deprecation and .ab extraction: https://android.googlesource.com (platform-tools diff), https://gist.github.com/AnatomicJC/e773dd55ae60ab0b2d6dd2351eb977c1, hoardy-adb (github)
- Signal Secure Backups: https://support.signal.org
- Google Authenticator transfer: https://www.allthingssecured.com; Microsoft Authenticator: https://learn.microsoft.com
- Authy multi-device: https://www.twit.community
- WhatsApp Google Drive restore: https://www.imyfone.com
- Tailscale no-remote-wake / always-on guidance: https://github.com (WOLE), community threads
- Motorola Smart Connect compatibility chart: https://en-emea.support.motorola.com; Smart Connect TV casting: https://en-us.support.motorola.com
- Moto G 5G (2024) no DisplayPort Alt Mode: community USB-C video tables (usbctohdmi.com), LIKELY tier
