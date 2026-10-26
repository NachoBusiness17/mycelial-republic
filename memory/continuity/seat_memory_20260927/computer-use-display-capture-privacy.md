---
name: computer-use-display-capture-privacy
description: Display screenshots on this machine capture the operator's personal
  Chrome, not the IAB — when the target is an in-app-browser page, use IAB
  instruments, never computer-use display capture
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_cc461d2f-b0e3-4197-8520-3684da78785a
---

(2026-09-14) When asked to visually verify pages, I took a `computer-use` display screenshot expecting the ZCode in-app browser pane — it captured the operator's personal Chrome session (their X/Twitter feed) instead, because the IAB pane was not the foreground window. Nothing in that capture was used, and the capture channel was abandoned immediately.

**Rule:** the display is the operator's private space. For page verification use in-browser instruments: `playwright.domSnapshot()`, `evaluate()` probes (canvas pixel sampling, performance resource-404s, error hooks), and the canvas-`toDataURL` → write-file → Read-tool sight channel (see [[vislab-catalog-surface]]). Note the IAB's own `tab.screenshot()` was timing out / failing ("activity capture failed for guest") this session, which is what tempted the display capture — resist that path; if a display capture accidentally includes personal content, stop using it and say so plainly.
