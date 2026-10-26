## Files read

- `dashboard/static/eraser_maze.html` — **the prompt path `dashboard/static/games/eraser_maze.html` does not exist**; the game lives one level up, mirrored at `site/dist/games/eraser_maze.html` and `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/eraser_maze.html`. Audit below is against the canonical `dashboard/static/eraser_maze.html` (508 lines).
- `dashboard/static/games/index.html` (listing, confirms absence).

## Audit

**Onboarding (worst axis — this is the patch):**
1. **The prism lies from frame 0.** `drawSprites` (line 412) and `updateHUD` (line 424) both use `obsStamp[pi] <= eraseStamp[pi]`, which is `0<=0 = true` at boot → prism renders white/pulsing and HUD says `LIT (fringed)` before the player has done anything. But `checkWin` (line 382) additionally requires `eraseStamp[pi]>0`. Visual LIT ≠ winnable LIT, with zero way to tell them apart. Player walks to prism, stands there, nothing happens, no feedback.
2. **The tutorial documents a dead step.** Line 25 says "walk past it (it goes flat)" — but `stampSight` line 347 explicitly exempts the prism (`if(x===prism.x&&y===prism.y)continue`). Your sight can *never* collapse the prism. The stated first step of the win sequence is a no-op.
3. Two jargon walls (lines 24–25) before any interaction; the actual goal is buried mid-paragraph. The discoverable "tile path" solution (eraser tile at 48,20 has r=10 and covers the prism) is never surfaced.

**Difficulty:** actually well-tuned *mechanically* — braid 0.55 maze, detector at (46,20) r=13 re-collapses the prism if stepped after erase (real threat), eraser tile at (48,20) is the shortcut. All of it is invisible. The `prismHasFringes` seed guard (line 308) means some seeds are silently unwinnable — HUD says "no two-path light" but nothing tells you to press R.

**Juice:** the field render (line 466–470, coherent violet vs flat slate) *is* the juice and it's good; falsifier strip at boot is strong credibility juice. Missing: any state-change feedback at the prism, any win moment, any "what do I do now" affordance.

## The one patch — "truthful prism + live objective bar"

Six insertion points, no rewrites, no logic/physics changes. Net effect: the prism tells the truth, the player always knows the next action, the documented sequence matches the code.

---

**① Insert after line 19** (after `.pass{...}.fail{...}`) in `<style>`:

```css
#obj{font-size:.78rem;margin:8px auto;max-width:940px;border:1px solid rgba(232,201,106,.35);border-radius:6px;padding:6px 10px;background:#0a1412;color:#e8c96a;min-height:1.4em}
#obj .k{color:#b48cff}
```

**② Replace the win-sequence clause in line 25** (keep the rest of the `<div class="mut">` intact) — old text: `reach the PRISM while it still fringes: walk past it (it goes flat), fire an eraser over it (delayed choice — it re-lights in the new basis), then step close` →

```
reach the PRISM while it still fringes: your own sight NEVER collapses the prism — it reads without recording (line 347) — so first fire an eraser so its wash covers it (delayed choice: basis re-mixed → <b>ARMED</b>), THEN step adjacent to win; stepping an orange <b>D</b> tile afterward re-flattens it and you must erase again · arrows/WASD move · <span class="v">E</span> fires the carried eraser (r=7) · <span class="c">R</span> new maze
```

**③ Insert after line 34** (`<div id="fals">…</div>`) — the objective bar:

```html
<div id="obj">objective: booting…</div>
```

**④ On line 255**, add the win-flash clock to the existing `var` statement — old: `var frameN=0,phi=0,k=2.0,sightR=7,won=false,prismHasFringes=false;` →

```js
var frameN=0,phi=0,k=2.0,sightR=7,won=false,prismHasFringes=false,winFlash=-999;
```

**⑤ Insert after line 386** (closing brace of `checkWin`) — the single source of truth both renderers share:

```js
function prismMode(){
  if(!prismHasFringes)return 'none';
  var pi=prism.y*GW+prism.x;
  if(eraseStamp[pi]<=0)return 'dormant';
  return obsStamp[pi]<=eraseStamp[p