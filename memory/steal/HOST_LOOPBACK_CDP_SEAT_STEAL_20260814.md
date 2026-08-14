# HOST-LOOPBACK CDP BROWSER SEAT — the working transport (steal 2026-08-14)

## Problem
The container browser seat (mag-browser, CDP :9222) never actually drove grok/ChatGPT. Root:
1. **Version mismatch** — image was playwright v1.48.0 vs host 1.62.0 (CDP protocol mismatch). PINNED to
   v1.62.0-jammy + fixed chromium path (v1.62 moved `chrome-linux` → `chrome-linux64`, crash-loop exit 127).
2. **Docker Desktop CDP port-forwarding wall** — CDP works INSIDE the container (Chrome 151, healthy)
   but host→container forwarding resets the handshake ("RemoteDisconnected" / empty raw socket).
   Pre-existing; notorious Docker Desktop-on-Windows quirk for Chromium DevTools.

## Steal (external)
- Playwright's own Docker docs: `--ipc=host` / `--init` for Chromium; version match is the #1 cause of
  connect_over_cdp hangs (playwright-python #2182, community.testmuai.com).
- The RELIABLE pattern everyone uses when container CDP forwarding is finicky: **run Chromium on the
  HOST bound to 127.0.0.1 with --remote-debugging-port, connect over LOOPBACK** — no Docker forwarding.

## Adaptation (applied + proven)
- Installed host chromium (playwright 1.62.0) → `%LOCALAPPDATA%\ms-playwright\chromium-1234\chrome-win64\chrome.exe`.
- Launched headless: `chrome --headless=new --remote-debugging-port=9222 --remote-debugging-address=127.0.0.1
  --remote-allow-origins=* --no-sandbox --disable-gpu --user-data-dir=<tmp>` (CREATE_NO_WINDOW).
- VERIFIED: host probe http://127.0.0.1:9222/json/version -> Chrome/151.0.7922.34 OK. This bypasses the
  broken container forwarding entirely.
- browser_driver's default endpoint is already ws://127.0.0.1:9222 — so it connects to the host seat.
  (Notebook: "Sync API inside asyncio" error is a notebook-kernel limitation, NOT a browser_driver bug.)

## Notes
- Container config left intact as the sandboxed option; host path is the working transport tonight.
- For a persistent managed seat, wrap the host chrome launch as a supervised loop (CREATE_NO_WINDOW,
  kill on stop) — not yet done.
