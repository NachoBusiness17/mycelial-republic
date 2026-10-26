# DESKTOP POPUP QUIET - 2026-10-18 ~06:50-07:00 EDT (operator: "i want them to burn i just want to play a game too")

Operator ask: keep the burns running, kill the popups that took over the game, keep
gstd, do it cheaply/headlessly. NOTHING was disabled. Zero scheduled tasks touched.
gstd untouched (gstd-node container + MagGstdDrainDaily left alone).

## The three popup sources found and what was done

1. **Headed Chrome with an X tab** (pid 32204, plain chrome.exe, parented to explorer
   = opened via ShellExecute by some lane; the opener process already exited, so the
   origin seat is unnamed). This was the window taking over the fullscreen game.
   CLOSED (taskkill /PID 32204 /F). The headless scrum Chrome (pid 33732, port 9222,
   scrum_profiles/team_0) was verified headless and left burning.

2. **cua-driver cursor overlay** (pid 7700, Cua.AgentCursorOverlay.default, parent
   7380 already exited = orphaned). Process is ELEVATED - this seat's non-admin shell
   got ACCESS DENIED on kill. Minimized via ShowWindow(6); it may reshow when its
   agent acts. True cure needs an admin shell (`taskkill /PID 7700 /F` from elevated
   prompt) or a reboot, or closing whichever agent session spawned it. LEFT RUNNING
   BY NECESSITY, documented for the operator.

3. **Boot-lane console** (cmd 14832 from Startup\mag_boot_lane.cmd). Root cause: the
   queue ran every job detached EXCEPT the last - run_armC.py (the Arm C 200-leg
   longrunner) ran foreground, so a visible console stayed on the desktop for days
   per boot. CURED BOTH WAYS: this boot's console minimized to taskbar (armC keeps
   burning), and mag_boot_lane.cmd edited to `start "" /b` detach armC matching the
   queue's own convention, so FUTURE BOOTS NEVER SHOW A CONSOLE. Fix comment with
   receipt pointer landed in the file per build discipline.

## What was verified already-clean

- All Mag scheduled tasks launch through hidden wrappers (run_hidden.vbs window
  style 0, or watch/docker_watchdog.vbs same shape) - the burn fleet was never the
  popup source. MagBoxBurnNightly + MagHermesBurn247 were Running throughout and
  stayed untouched.
- mag-docker-watchdog (every 5 min) reads clean: it only probes `docker version` and
  relaunches Docker Desktop if dead. NOTE: this is the probable unpauser of
  mag-worker in DESKTOP_PAUSE_20261017.md - pause makes the worker heartbeat stale,
  watchdog-era healing would explain the unpause; no unpause code exists in the
  current ps1 (line evidence: whole file is 16 lines, engine-check only), so if it
  recurs, stream `docker events` to catch the actor live.

## The "headlessly or in a docker" answer

The estate already owns the headless browser seat: compose `browser` profile (headless
Chromium under xvfb, CDP ws://127.0.0.1:9222, cap_drop ALL). If a headed-browser lane
shows up again, the cure is pointing that lane's driver at the container seat instead
of ShellExecute-ing the user's default browser. Not done today: no driver needed
repointing - the one headed window was closed at the source.

## Owed

- Operator (optional): admin-shell kill of pid 7700 cua-driver, or ignore until next
  reboot clears it.
- If popups recur mid-game: run the window sweep again (Get-Process MainWindowTitle +
  parent trace at catch time names the opener while it is still alive).
