# SPECTRAL MAZE — polish audit

**Files read:** `dashboard/static/spectral_maze.html` (canonical source; the requested path `dashboard/static/games/spectral_maze.html` does not exist — the file lives one level up). Confirmed byte-identical build copy: `site/dist/games/spectral_maze.html` (same SHA-256). No files were created or modified.

## Findings

### Juice — thin outside the solver visualization
- **The win moment is a text swap.** `checkWin()` (spectral_maze.html:715-726) writes one string into `#stats`; `updateHUD` then freezes forever (`if(won)return`, :756). No flash, no pop, no sound, no screen effect — the entire goal payoff of the game is a monospace line competing with `pos 12,7 · build 0.8ms` telemetry.
- **Blocked moves are silent no-ops.** `tryMove()` (:701-714) returns on a wall hit (:712) with zero feedback — the 95ms throttle plus 1-cell grid makes control feel unresponsive when you're hugging walls (which is most of a maze game).
- **Filter cycle has no acknowledgment.** `cycleFilter()` (:809-812) only rewrites button text; the canvas band-dim (:256-258) is instant with no transition.
- Player is a flat white rect (:749-750) — no trail, bob, or motion cue. No audio anywhere.
- Existing juice to build on: the lit-sensor sine pulse (:744) and mirror/guide glow in the composite (:242-249).

### Difficulty curve — flat, and can produce unwinnable boards
- **No curve and no variety:** boot seed is fixed `buildWorld(20260906)` (:824) → every player gets the identical first board; `R`/NEW MAZE (:817, :820) is a pure random re-roll at the same difficulty. Nothing ramps, nothing eases the first session.
- **Winnability is not guaranteed:** `buildWorld` keeps the best of 40 gen attempts by lit-sensor count and breaks at ≥2 (:690-693) — but if no attempt reaches 2, it accepts the best including **`lit=0`**. `placeSensors` marks `lit = amp>=LIT_MIN` once at build (:429) and can also return an empty array (candidates need amp≥0.05 and Manhattan ≥6 from source, :399-403). With all sensors dark or absent, `checkWin` (:717-719) can never fire → dead board.
- Sensor placement is purely "brightest amplitude wins" (:419) with spacing ≥6 (:424) — no distance shaping, so the one lit sensor may be across the map or nowhere.
- With no proximity/minimap hint, effective difficulty is aimless walking, not the optics puzzle.

### Onboarding clarity — instructions buried under physics
- Controls are **mid-sentence in the second jargon paragraph** (:21): a new player hits eikonal least-time flood / Snell-emerges copy (:20) before learning that arrows move. Win condition appears only inside the telemetry HUD line mixed with pos/guides/buildMs/HEAP CAP HIT (:767).
- On boot, `runFalsifierStrip()` (:825) fills `#fals` (:27) with a PASS/FAIL physics test report — the first thing under the canvas reads like CI output, not a tutorial.
- Buttons (:23) exist, but `TAB/E` and `R` are never surfaced except in the wall of text.

## ONE highest-value polish patch

**Patch: a banner system — boot goal/controls card (fades on first move) that re-pops as a gold win celebration + screen flash.** One patch, three insertion points, ~25 lines. Fixes the two widest problems at once: nobody reads the onboarding, and winning feels like nothing.

---

**Insertion 1 — CSS.** Insert immediately after line 15 (`<span class="pass">…` rule), before `</style>`:

```css
#banner{position:fixed;left:50%;top:50%;transform:translate(-50%,-50%);z-index:50;
  max-width:min(540px,92vw);background:rgba(6,16,14,.95);border:1px solid rgba(180,140,255,.55);
  border-radius:10px;padding:14px 18px;text-align:left;font-size:.78rem;line-height:1.55;
  color:var(--ink);pointer-events:none;
  box-shadow:0 12px 40px rgba(0,0,0,.55);
  transition:opacity .45s ease,transform .45s ease}
#banner.gone{opacity:0;transform:translate(-50%,-50%) scale(.96)}
#banner h2{margin:0 0 6px;font-size:.85rem;letter-spacing:.12em;color:var(--gold)}
#banner .keys{color:var(--accent)}
#banner.win{border