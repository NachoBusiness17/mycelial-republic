# GHOST BROWSER DRIVER — STEAL (2026-08-10)

**Context:** "browsers in vs code are bound by vs code rules. ghost is not." The VS Code browser
tab is sandboxed and can't drive grok.com. Ghost drives its OWN container browser over CDP. Steal
the mechanism that makes ghost→grok actually work.

## External grounding (cited)
- **Playwright Authentication**: store authenticated browser state via `storageState` (cookies,
  local storage, IndexedDB, WebAuthn passkeys) to a gitignored `.auth` file; reuse it so sessions
  start already-authenticated — authenticate once, reuse many. (Warning: state contains sensitive
  cookies; keep out of repos.)
- **browser-use** (browser_use agent, 108k★): an AI browser agent that drives a real browser like a
  human — opens pages, fills forms, clicks, extracts; handles auth + CAPTCHA; supports persistent
  filesystem/memory and remote Playwright browsers; LLM-driven. This is the browser-agent pattern.

## Self-steal (already inside the Republic)
- `mag/browser_driver.py` (browser_driver.v1): Playwright-over-CDP driver for the CONTAINER browser
  (ws://127.0.0.1:9222). Already defines the `grok` surface (url grok.x.ai, textarea, `.message`),
  plus deepseek/perplexity. Host only needs `playwright`; the container owns the browser.
- `mag/browser_env.py`: host_allowlist enforced (free frontends only).
- `mag/grok_free.py`: "free grok surface = the grok desktop (grok.com), driven by the GHOST PROTOCOL
  via the browser"; CLI/API bill the working team.
- `mag/ghost_whisper.py`: the public grok.com "mag" project (under nachoquixotic) — the persistent
  authenticated grok space.

## The synthesis — why ghost can drive grok but VS Code can't
- VS Code browser = sandboxed by editor rules → can't automate login/web.
- ghost = standalone daemon driving its OWN container browser over CDP (Playwright connect_over_cdp),
  like browser-use — types, clicks, reads the real answer from the live DOM.
- Missing piece was PERSISTENT AUTH: grok.com must be logged in in ghost's browser. Fix: keep the
  container browser's user-data-dir/profile (or storageState .auth file) so the grok login persists
  → auth once, drive many (the "mag" project already exists under nachoquixotic).

## Invariants folded (source=browser_steal)
1. browser:persistent-auth-state — reuse storageState in a gitignored .auth dir; no re-login.
2. browser:ghost-drives-over-cdp — container browser over CDP like browser-use; never VS Code browser,
   never hanging headless CLI.
3. browser:drive-like-a-human — fill/click/read the live DOM; selectors are a starting point.
4. browser:persistent-profile — keep user-data-dir so grok login persists (auth once, drive many).
5. browser:allowlist-frontends — only drive allowlisted free frontends (per browser_env); grok free =
   ghost's browser session.

## To launch the frontier cross-check
Get ghost's container browser logged into grok.com once (operator signs in via the noVNC/CDP seat,
or the "mag" project session persists), then:
  python -m mag.browser_driver ask "<our batch findings>" --surface grok
and read the real frontier answer. That finally registers a REAL grok call.
