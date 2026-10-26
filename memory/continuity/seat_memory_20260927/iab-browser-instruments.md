---
name: iab-browser-instruments
description: Working browser test/sight instruments on this machine — IAB
  screenshot is broken; canvas toDataURL dumps → Read tool; synthetic key
  events; resource-404 detection; cache-busting
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_cc461d2f-b0e3-4197-8520-3684da78785a
---

Proven 2026-09-14 while testing the dashboard games. The ZCode in-app browser (`iab` backend via the browser-use skill) has a **broken screenshot pipeline**: captures time out at 30s ("activity capture failed for guest"), and one stuck capture blocks the tab until you open a fresh one. What works instead:

- **Sight:** `tab.playwright.evaluate(() => canvas.toDataURL("image/png"))` → decode base64 → `fs.writeFileSync` → Read tool shows the image. Works for 2d canvases; **WebGL canvases dump solid black** without `preserveDrawingBuffer` (inconclusive, not proof of breakage). HUD/overlay canvases often carry the state even when the GL layer doesn't.
- **Runtime errors:** after load, hook `window.onerror` + `unhandledrejection` via evaluate, wait, read back. **Runtime 404s** the static sweep can't see: `performance.getEntriesByType("resource").filter(r => r.responseStatus >= 400)`.
- **Interaction without OS focus:** dispatch `new KeyboardEvent("keydown", {code, key, bubbles: true})` on `window`/`document` — tests handler logic even when the operator's Chrome holds OS focus; `tab.cua.keypress` needs the pane foregrounded and can silently miss.
- **Evaluate realm gotcha:** page top-level `let/const` are invisible to evaluate (`typeof G` is undefined even when defined) — only `window` properties cross. Games under test should expose a `window.X` handle with **getter** properties for arrays (constructors like `startGame` reassign arrays; snapshotted properties go stale). See `window.MUD` in mud.html.
- **Stale served copies:** the browser caches game/catalog pages; cache-bust with a `?v=` query + `tab.reload()`. Verify what the server actually sends with `curl -s <url> | grep -c <marker>` before blaming the cache.
- **rAF throttling (frozen-game false alarm):** a backgrounded/hidden IAB pane throttles rAF to ~0 — game loops freeze silently, injected state changes are never processed, and the canvas shows a stale frame. Before concluding a game is broken, wake the pane (`(await browser.capabilities.get("visibility")).set(true)` + `tabs.get(id)` to activate) and verify liveness with a rAF tick counter (~60/s expected). Also hook `window.onerror` BEFORE the reload/goto — load-burst errors are missed if the hook is installed after navigation. **Limits:** `visibility.set(true)` is not enough when the whole ZCode window is occluded behind other apps (the operator's Chrome was foreground — rAF stayed at 0). The definitive instrument for a game with a `MUD.step/pump` handle: pump frames deterministically from evaluate (`MUD.pump(90)`) and read state synchronously — no rAF, no focus, no pane position required.
- Never reach for computer-use display capture to check an IAB page — it shows the operator's personal Chrome ([[computer-use-display-capture-privacy]]). Recipe details also live in [[vislab-catalog-surface]]; applied example in [[mud-superhot-adam-access]].
- **Full form-driving confirmed (2026-09-18, my.telegram.org app creation):** the browser-use skill can claim a user tab (`browser.user.claimTab` after `user.openTabs()`), navigate, fill inputs by `getByRole("textbox", { name })`, `check()` radios, click, and read results from `domSnapshot()`. Gotchas: every fresh `js` call needs the full plugin-root bootstrap re-run (fresh kernel, `agent` undefined otherwise); after claiming, the tab moves from `user.openTabs()` into `browser.tabs.list()` (find by id there, not openTabs); a `waitForTimeout` inside a click-cell can throw a budget error even when the click succeeded, so snapshot the page state instead of retrying; and a my.telegram.org "incorrect?" login rejection means the phone number lacks the leading `+` (full international format).
