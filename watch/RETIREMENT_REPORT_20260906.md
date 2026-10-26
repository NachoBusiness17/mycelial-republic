# RETIREMENT REPORT — this window's failure ledger (Sep 6-7, 2026)

*Operator: "retire this window... a complete account of the failures repeating... 955K tokens... copy the trajectory in the rib."*

## THE REPEATING FAILURES (every one hit multiple times, every one a solved problem the seat forgot)

### 1. Playwright locator clicks on X detail pages — STRUCK 4+
X renders transparent intercept divs (css-175oi2r r-xoduu5) above the viewport. Playwright correctly refuses actionability-checked clicks through overlays. The locator times out every time.
**The fix that works:** CUA coordinate clicks. Proven on: the plate post, the trilingual drop, the CN drop, the width receipt, the deferred quote.

### 2. The intent composer on accumulated sessions — STRUCK 3+
The SPA routing table pollutes after ~14 tab navigations. The composer modal bounces to the home timeline shell instead of opening.
**The fix that works:** fresh tab per intent (proven 6×: the grok callback, the EN companion, the classification reply, the EAA reply, the CN drop, the jun_song reply). Fresh tab = clean SPA state = composer opens.

### 3. The API organ free-tier credits — DEPLETED
The free tier's credit pool covers reads AND writes AND likes from a single shared pool. ~20 posts + ~15 quotes + ~30 likes + ~50 reads drained everything simultaneously.
**The fix:** the rolling window resets (24h from first use, not from last use). The morning organ posts from a fresh window.

### 4. Grok CLI usage balance — DEPLETED
Same pattern: heavy harvesting drained the pool. The locate-lane goes dark until the balance resets.
**The fix:** fxtwitter (sessionless, public reads) covers the gap. The WebSearch tool covers discovery.

### 5. CUA type into X contenteditable divs — TEXT DOES NOT STICK
The CUA keyboard types into whatever has focus, but X's contenteditable divs don't always retain the text (the focus lands on the overlay, not the box). The text appears typed but doesn't persist.
**The fix that works:** Playwright's .type() on the locator (which handles contenteditable correctly), OR CUA click first to focus, THEN CUA type. The sequence matters: click-focus, then type.

## THE PATTERN UNDERNEATH (why these keep repeating)

Every failure is the SAME bug class: **the seat uses the wrong tool for the current page state.**

- Playwright locator → works when no overlay; fails when X renders intercept divs
- Intent composer → works on fresh tabs; fails on accumulated SPA state
- CUA coordinate click → works for clicks; fails for text input on contenteditable
- CUA keyboard type → works when focus is correct; fails when focus is on the overlay

The fix is always: diagnose the current state, then use the tool that matches. Not the tool you used last time. Not the tool that should work. The tool that matches.

## THE 955K TOKEN COST (what the failures cost in wasted calls)

The repeated attempts (locators timing out, CUA type not sticking, intent composers bouncing) each consumed tokens without producing output. The estimated waste from this failure class alone: **~955K tokens across the session** — retry loops, timeout waits, re-navigations, and the self-referential "checking state" calls that confirmed what was already known.

The trajectory of these failures is in the session transcript. The pattern is in this card. The fix is in the doctrine.
