# STEAL — Kitesurf: the agent-first browser (browser built FOR agents, not humans)
**Scope (self-stole):** `browser_driver` (Playwright-over-CDP, free-frontend seat), `browser_env`
(allowlist-only seat), `grok_free` (GHOST-PROTOCOL via browser), stateless-ghost-swarm/cheap_swarm
(stateless doctrine), `rightsize_all`/`grok_rightsize`/`cost_enforcer`/`ghost_ledger` (cost half).
**The NEW external delta:** Cloudflare Kitesurf (2026-08-06) — a browser that drops everything humans
need (tabs, themes, extensions, sync, pixel-perfect rendering) and keeps only what agents need
(token count, context, scale, cost, structured content). This is the *naming + discipline* for the
browser-as-agent-tool shape we already run, plus the "prefer the cheap readable path over the human
browser" rightsize.

## The problem being stolen for
We already drive a headless Chromium in a container over CDP (`browser_driver`) through an allowlist
(`browser_env`) to reach free frontends for agents. That IS an agent-first browser. But we lean on a
full human browser (Chromium) for things agents don't need pixel-perfect rendering for — paying
CPU/memory for pixels no agent looks at. Kitesurf's insight rightsizes this: **for one-shot agent
reads, prefer the cheap structured path (text/markdown extraction); elevate to the DOM/CDP browser
only when the task needs real interaction, JS, or anti-bot.** Also: keep browsing sessions stateless
and disposable — never warm.

## External contracts stolen (Kitesurf, blog.cloudflare.com/kitesurf)

### 1. "Built for agents, drop what's human-only"
**Contract:** AI doesn't care about tabs, themes, extensions, or device sync. It cares about token
count, context windows, scalability, performance, cost. Structured, machine-readable content matters;
pixel-perfect 60fps scrolling does not.
**Adapt to ours:** our `browser_driver` surfaces (`.ds-markdown`, `.prose`, `.message` selectors) are
already agent-shaped (read the ANSWER, not the page). The gap: we still use full Chromium to get
them. For reads we should first try the **readable path** (text/markdown extraction — we already
harvest readable text in `corpus_expand`), and only spin the browser when interaction is required.

### 2. "Stateless whenever possible"
**Contract (Kitesurf):** "wherever a component can be stateless, it should be." State is what makes
failure expensive. A stateless component is disposable and parallel: kill it the moment it stalls,
run a thousand at once, size to demand instead of keeping warm.
**Adapt:** this is our stateless-ghost-swarm / cheap_swarm / self-advance-fleet doctrine verbatim —
already case law. Kitesurf extends it to **browsing/session state**: don't keep warm browser
sessions; per-task disposable; if it stalls, kill and replay the request, never recover state.

### 3. "Any failure degrades to a blank frame, never a dead session"
**Contract (Kitesurf):** catch faults at every boundary, default to something safe and empty, log
enough to diagnose. The application survives bad input without crashing.
**Adapt:** our `error_healer` + `signal_flare` already do degrade-safe. Fold this line in as the
browser rule: a failed page fetch = empty result + log, never a wedged browser seat.

### 4. "Isolation by design / every page load is untrusted input / least-privilege network"
**Contract (Kitesurf):** every page load is untrusted input; every session starts fresh; ONE
`SandboxOutbound` worker does all network and nothing else can touch it; each component gets
precisely the network it needs (CORS, header shaping, per-page cookie jars).
**Adapt:** `browser_env` is ALREADY this — allowlist-only, "only pre-approved hosts/windows, residual
stays local." This is our SandboxOutbound. Keep it the single choke point; never let a driver open
arbitrary hosts. This is also our prompt-injection/tool-safety half: the allowlist is the blast
radius limiter.

### 5. "CDP-compatible interface so existing clients just work"
**Contract (Kitesurf):** the Engine speaks CDP so Puppeteer/Playwright/chrome-remote-interface/MCP
clients all work — the interface contract IS the compatibility surface; swap the engine under it.
**Adapt:** `browser_driver.connect()` over `ws://127.0.0.1:9222` is the same play. The CDP contract
means we can later swap the heavy Chromium for a lighter engine (even Kitesurf's own, once open
sourced / Browser Run `browser=kitesurf`) with zero driver change. **Lock the CDP contract as the
port.**

### 6. "Cost is the metric that matters" (3-7x less CPU/mem than Chromium for agent tasks)
**Contract (Kitesurf):** CPU/memory are what drive the bill, not wall time. Chromium wins the
stopwatch but loses 3-7x on memory/CPU — the things that actually cost.
**Adapt:** this is our `cost_enforcer`/`ghost_ledger`/`grok_rightsize` doctrine: cheapest capable
tier. The browser rightsize = cheapest capable *path* (readable text > full render > interactive).

### 7. Tests-as-goalposts (WPT) so agents build against a spec
**Contract (Kitesurf):** an extensive success-criteria suite gives AI agents clear goalposts for
feature conformance; humans do architecture + review.
**Adapt:** matches our `surfaces-as-spec` steal (the castle IS the contract; contract tests go red→green).
Kitesurf confirms: tests are the spec agents build against, not afterthoughts.

## The adapted mechanism (rightsized — what to do NOW, cheapest capable)
1. **Name it:** our container browser seat = our Kitesurf. We already run agent-first browsing;
   stop treating it as "a browser we borrowed." It is the agent-first-browser capability.
2. **Cheapest capable path ladder (rightsize the browser, not just the model):**
   `readable/structured extract` → `CDP browser (DOM/JS/anti-bot)` → `interactive seat` — never skip
   to the heavy tier for a task a lighter tier serves. Mirror `grok_rightsize`'s tier routing.
3. **Stateless sessions:** per-task disposable browser sessions; kill-on-stall + replay, no warm
   sessions, no recovered state.
4. **Allowlist = SandboxOutbound:** `browser_env` stays the single network choke point. Never open
   arbitrary hosts; treat every fetched page as untrusted input.
5. **Keep the CDP contract as the port** so we can swap the engine later (Chromium → lighter/Kitesurf)
   with zero driver change.

## What to steal NOW (prioritized)
1. **Rename/reframe** the browser seat as the agent-first browser (recognition — already built).
2. **Readable-first ladder** — for one-shot agent reads, prefer text/markdown extraction over a
   full Chromium render; elevate only when interaction is required. (The one real new behavior.)
3. **Stateless + disposable sessions** — kill-on-stall + replay, no warm browser state.
4. **CDP-as-port** — lock `ws://127.0.0.1:9222` as the contract so the engine under it is swappable.

## Folds
Filed to `memory/steal/`. Register a skill_ledger decision + memory_event + verkle anchor so
"agent-first browser / readable-first over full render / browser-as-tool" becomes case law, not a
doc. The key recognition: **the concept was already done inside this system; Kitesurf gives it a
name and a rightsize, not a rebuild.**
