## Path note

`dashboard/static/games/tavern_brawl.html` **does not exist**. Read the live file instead: `dashboard/static/tavern_brawl.html` (copies also at `site/dist/games/tavern_brawl.html` and `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/tavern_brawl.html`). All citations below are to `dashboard/static/tavern_brawl.html`.

## Audit findings

### Juice
1. **All dialogue renders on one line (the big one).** `:302` — `H - 80 - f.y*0 + (floaters.indexOf(f))*-0`: both multipliers are `*0`, so every floater draws at y=600, x=12 and overwrites the previous. Provocation lines, initiative rolls, HEAD SHOT ×2 bonuses, "WHAT IS NOW TRUE" — the entire feedback layer is a smudge.
2. **SUPERHOT silently dies forever.** `:211` — `if (p.type === "bubble") continue;` skips move *and* offscreen cull, so GOPHER's SOAP SHIELD projectiles (`:132`) accumulate unbounded; gate `:335` `projectiles.length > 0` then never lets time freeze again.
3. **Non-salt traps never expire.** `:233-236` decrements `ttl` only when `kind==="salt"`; the `ttl:600` traps from `:181` pile up forever (visual soup + O(n) per ractor per frame at `:170-175`).
4. `r.headLine` (`:225`) is never defined — every headshot uses the same fallback line; no hit flash or shake anywhere.

### Difficulty
1. **No fail state.** Attacks target other ractors only (`:122`); the player has no HP, no loss, no score/win — the brawl is a spectator sim.
2. **Trap damage is never applied.** `t.dmg` is written at `:181/:188/:327` and read nowhere; only salt *slow* applies (`:170-175`). The `[G]` god-trap (`:327`) is cosmetic.
3. **Knockouts last ~1.2 s, not 12 s.** `:240` — `frame - r.downAt > 12*3` = 36 ticks at 33 ms, contradicting the comment at `:237`. Should be `12*30`.
4. **SHOUT feeds the enemy.** `:321` adds `agit+8` to nearby ractors, and `agit >= THRESH` is exactly what makes them fire (`:198`) — the operator's power tool arms their guns.

### Onboarding
1. **HUD lies about the input.** `:17` says "click a ractor to provoke: [I]·[M]·[P]·[Q]" but click picks a **random** kind (`:346-347`); keys only land within 60 px of the cursor ghost (`:355`). First-time players get no mapping between prompt and behavior.
2. Nothing explains why P/Q exist — they *lower* agitation (`:90-91`), delaying the brawl the HUD just told you to cause.
3. SUPERHOT freeze has zero visual state — frozen looks like a hang; `T` toggle also shows no indicator.
4. Because of Juice #1, even the tutorial-style dialogue (initiative, "WHAT IS NOW TRUE") can't be read.

## ONE highest-value polish patch

Highest value = Juice #1: it is the game's entire readable-feedback channel, it blocks onboarding, and the fix is 7 lines at one insertion point. No rewrite.

**Insertion point:** replace lines **298–304** of `dashboard/static/tavern_brawl.html` (the `// dialogue` block inside `draw()`, between the combat-log box draw and the `#cast` textContent update) with:

```js
  // dialogue — newest at the bottom, older lines stack upward, never overlap
  const fStart = Math.max(0, floaters.length - 6);   // cap: 6 visible lines
  for (let i = fStart; i < floaters.length; i++){
    const f = floaters[i];
    const newest = i === floaters.length - 1;
    const fade = Math.max(0, Math.min(1, (150 - f.t) / 40));
    cx.globalAlpha = fade * (newest ? 1 : 0.7);
    cx.fillStyle = newest ? "#ffd76a" : "#8fb3a9";
    cx.font = newest ? "bold 12px Consolas" : "12px Consolas";
    cx.fillText(f.text.slice(0, 110), 12, H - 96 - (floaters.length - 1 - i) * 15);
    cx.globalAlpha = 1;
  }
```

**Expected effect:** provocation results, initiative rolls, HEAD SHOT multipliers, the shout confirmation, and "WHAT IS NOW TRUE" each get their own line — newest in bold gold at y=584, older dimmed and stacked upward 15 px per line, max 6 lines (bounded, so initiative bursts can't flood the screen), still alpha-fading after t=110. Reads as a proper combat log tail instead of one overwritten string; the HUD's promised cause→effect