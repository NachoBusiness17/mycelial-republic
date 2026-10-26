# Polish audit — `dashboard/static/games/swarm.html` (1730 lines, read-only)

## Findings

### Onboarding (worst area)
- **`swarm.html:1533` — the title actively misinforms:** `"move with A/D, everything else is automatic"` is false. Jump (`W/SPACE`, `:694`), shout (`Z`, `:121`), ult (`Q`, `:1164`), drop-through (`S`, `:699`), talk (`T`, `:1136`), and doors (`1/2`, `:116`) are all manual — and the **core progression verb is invisible**: XP comes mostly from the ground-ride harvest header (`:984-997`), which is taught nowhere. Gems actively *flee* (`:954-958`), so a player who trusts "automatic" chases fish that run away and levels at a crawl.
- Door cadence (gate at `DEPTH_LEN=45`, `:164`/`:1016`) gets one toast at the moment it happens; nothing prepares the player before it.
- Good onboarding that exists: doors screen keys (`:1561-1580`), level-up card keys (`:1593`), death-screen meta shop (`:1550-1556`), touch halves (`:137-152`, though title never mentions touch).

### Juice
- **`killMult` combo (up to 5× XP, `:597-598`) is never drawn anywhere** — invisible mechanic, also an undeclared implicit global.
- **`levelUp()` (`:654-679`) is silent** — only `shake=8` (`:678`); no `beep`. The single most-earned moment in the loop has no audio sting.
- **Enemy projectile hits (`:1175-1176`) have no sound and no shake** — flash only. Contact damage (`:912-914`) likewise silent (continuous drain, so per-tick beep would spam — but there's no low-HP heartbeat/vignette either).
- Solid already: kill particles + gridForce + damage numbers (`:614-629`), beat-pulsed grid/platforms (`:552`, `:719`), SUPERHOT audio slowdown (`:1070`), warp-grid juice (`:532-558`).

### Difficulty
- **Known fix verified present:** `mtn.speed=Math.min(46,26+mtn.t*0.45)` at `:1614` — the rock-wall speed cap from the undodgeable-rock bug is in place.
- Horde scaling: spawn floor `0.07s` reached at diffLevel 7 (`:1092`), hp `1+T/55` unbounded (`:587`), n-per-spawn grows with diffLevel (`:1093`) — steep but readable; door choices (`:172-180`) are the pacing valve.
- **Door mods stack multiplicatively forever** — `descend()` preserves `depthMods` then applies `door.f()` (`:1705-1706`); repeated HIGH ROAD / GLASS FIELD compounds `enemySpd`/`take` with no cap. Long runs get spikes, but this is design, not a bug.
- Contact damage is continuous dps with no iframes (by design, `:914`) — flash feedback is the only tell.

**Highest-value patch = onboarding**, because the title sentence is *wrong* about the core verb, and one toast queue fixes it with zero new render code.

---

## THE PATCH — first-run control coach (4 insertions, no rewrites)

### Insertion 1 — replace `swarm.html:1533`
```js
// OLD:
  ctx.fillText('a disco science skate — move with A/D, everything else is automatic',W/2,H/2);
// NEW:
  ctx.fillText('a disco science skate — A/D ride · W ollie · ride the ground to harvest',W/2,H/2);
```

### Insertion 2 — after `swarm.html:160` (`let shoutCd=0;`)
```js
// ---- FIRST-RUN COACH: fed through the existing toast channel (draw() :1522 already renders it) ----
let coached=SAFE_STORE.get('swarm_coached','0')==='1',coachI=0;
const COACH=[
 {at:5, t:'A/D ride · W or SPACE ollie · S drops through platforms'},
 {at:11,t:'RIDE the ground through the fish to harvest — stand still and they escape'},
 {at:18,t:'Z — HEY! LISTEN! shoves the horde (5s cooldown)'},
 {at:24,t:'Q when the gold bar is full — FULL SEND'},
 {at:38,t:'A GATE opens at 45s — walk through it · press 1 or 2 to pick a door'},
];
```

### Insertion 3 — after `swarm.html:687` (`if(toastT>0)toastT-=dt;`)
```js
 if(!coached&&state==='play'){
  while(coachI<COACH.length&&T>=COACH[coachI].at){toast=COACH[coachI].t;toastT=4.5;coachI++;beep(520,0.07,'sine',0.03);}
  if(coachI>=COACH.length){coached=true;SAFE_STORE.set('swarm_coached','1');}
 }
```

### Insertion 4 — in `startGame()` after `swarm.html:578` (opening toast line)
```js
 toast=DEPTH_NAMES[0]+' — they come from both sides';toastT=3.5;
 if(!coached)c