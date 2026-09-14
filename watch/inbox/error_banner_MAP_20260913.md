## Finding — what your cell yields
The error_banner fixture is a **ship-with-failures-visible** doctrine: it renders runtime failures directly on the page surface so an abliteration-minded examiner (Matthew Steiniger) sees the raw system state without mediation. It is implemented as a fixed-position red banner at the top of the viewport that captures uncaught exceptions and unhandled rejections and appends them to a visible log. The fixture exists to satisfy the **hard reproducibility** frame: the examiner must see the error as it happened, not a sanitized summary.

## Evidence — what in the repo supports it (file/shape, no invention)
- Entry file: `dashboard/static/maze_arena.html` lines 16–17
  ```html
  <div id="errbanner" style="display:none;position:fixed;top:0;left:0;right:0;z-index:99;background:#5c1010;color:#ffd9d9;font:12px ui-monospace,monospace;padding:6px 10px;white-space:pre-wrap"></div>
  <script>window.addEventListener('error',function(e){var b=document.getElementById('errbanner');if(!b)return;b.style.display='block';b.textContent+='ERR: '+e.message+' @ '+(e.lineno||'?')+':'+(e.colno||'?')+'\n';});window.addEventListener('unhandledrejection',function(e){var b=document.getElementById('errbanner');if(!b)return;b.style.display='block';b.textContent+='REJ: '+e.reason+'\n';});</script>
  ```
- Same fixture replicated in:
  - `dashboard/static/home.html` lines 34–40
  - `dashboard/static/incident_dungeon.html` lines 28–29
  - `dashboard/static/maze.html` line 37 (simplified capture)
  - `dashboard/static/conservation_room.html` lines 97–98
  - `dashboard/static/bad_apple_field.html` lines 20–21
  - `dashboard/static/shadow_walk.html` lines 20–21
  - `dashboard/static/eraser_maze.html` lines 21–22
  - `dashboard/static/spectral_maze.html` line 17
- The fixture is referenced in the grounding_wave.md audit record (lines 241–243) as the mechanism that "caught its first live bug within an hour of shipping."

## Risk if wrong — what the audit breaks on if this is missed
- **Reproducibility failure**: The examiner will not see the raw error, violating the hard reproducibility frame and triggering a Disputed verdict on the fixture’s claim.
- **Sanitization suspicion**: Without the banner, the system could hide failures behind sanitized logs, making it impossible to distinguish honest failures from curated narratives.
- **Chain credibility**: The Sept-6 chain-stop incident and the 24,854 recount both hinge on transparent failure capture; missing the banner risks re-introducing the same opacity.

## The act — the concrete prep step (file/spec/number)
Create a one-page **outsider’s reading guide** for the error_banner fixture and place it at `watch/inbox/error_banner_READING_GUIDE_20260913.md` with the following structure:
- Header: **What the banner signals to an abliteration examiner**
- Section 1: **Entry points** — list the 8 HTML files where the banner is mounted (maze_arena.html, home.html, incident_dungeon.html, maze.html, conservation_room.html, bad_apple_field.html, shadow_walk.html, eraser_maze.html, spectral_maze.html)
- Section 2: **Three things to check**
  1. The banner element id="errbanner" is present and positioned fixed top 0 left 0 right 0
  2. The event listeners for error and unhandledrejection are attached and append to the banner’s textContent
  3. The banner’s style includes z-index:99 and white-space:pre-wrap to ensure visibility and readability
- Section 3: **The one trap** — the banner starts hidden (style="display:none") and only becomes visible when an error occurs; reviewers must trigger a failure to verify it works.

## Falsifier — what would prove this wrong
- The examiner navigates to any page with the banner and triggers a controlled error (e.g., `throw new Error('test')` in the console). If the banner does not appear with the exact error message, the fixture is falsified.
- The fixture’s absence from any of the listed entry files falsifies the claim that the doctrine is applied across the surface.
- A sanitized log or summary that omits the raw error falsifies the **ship-with-failures-visible** doctrine.
