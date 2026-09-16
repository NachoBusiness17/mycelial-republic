# FX1 — swarm.html storage + audio + seeded-RNG fix (gen-2, from G1 games audit)

- **Date:** 2026-09-16
- **Lane:** wave_20260916 / FX1
- **Target:** `dashboard/static/games/swarm.html` (canonical; `dashboard/static/swarm.html` is a stale duplicate, untouched — verified 0 SAFE_STORE refs in it)
- **Status:** DONE — dogfood 32/32 PASS, exit 0, syntax OK, zero bare localStorage

## Scope (mission)

1. FATAL: wrap all bare `localStorage` access in one safe accessor (in-memory fallback) — privacy mode must not die at load. Preserve every existing key name.
2. AUDIO: suno/*.mp3 loader must try candidates in order (`../suno/`, `suno/`, then silent-skip); a failed fetch never breaks the loop.
3. RNG: port seeded-LCG replay law from `dashboard/static/games/toy.html` to swarm's gameplay-affecting RNG sites (if ≤ ~10 sites, all; else top sites + record remainder).

## Worklog

- Receipt opened before any edit (wave-lane law).
- Fix 1 APPLIED: `SAFE_STORE` accessor inserted after canvas bootstrap (guarded `window.localStorage` access + `setItem` probe → `mem` in-memory fallback; `get/set/getJSON/setJSON` all try/catch'd). All 8 bare sites replaced — key names preserved verbatim: `swarmbest` (4 sites: boot read + 3 best-writes), `priv_charcoal` (boot read + death write), `priv_meta` (boot read + `metaSave()`). Bonus hardening: corrupt-JSON no longer fatal (`getJSON` parses under try/catch, returns default).
- Fix 2 APPLIED: audio loader rewritten as a candidate chain.
- Fix 3 APPLIED: RNG law ported (gameplay sites seeded; cosmetic remainder recorded below).
- Harness `scripts/playtest_swarm.js` now points at canonical `dashboard/static/games/swarm.html` (was reading the stale duplicate at `dashboard/static/swarm.html`).
- Tests: node --check OK; dogfood 32/32 PASS twice (before and after the forcedSeed addition); replay probe proves seed determinism.
- Findings while in file (not fixed, out of scope): `hurtFishTouch` writes `G.shake` but `G` is undefined in swarm — latent crash if a fish lunge connects (line ~561). `schedMusic` is defined but never called (dead code).

---

## DIFFS SUMMARY

### Fix 1 — SAFE_STORE (privacy mode)
- NEW block after `addEventListener('resize',rs);rs();`: `SAFE_STORE` IIFE — one guarded accessor. Bootstrap: `try{ls=window.localStorage;ls.setItem('__swarm_probe','1');ls.removeItem('__swarm_probe');}catch(e){ls=null;}` — covers both access-throwing (old Safari/blocked) and write-throwing (quota/private) failure modes. When `ls` is null or any op throws → in-memory `mem` object (session-scoped persistence).
- `swarm.html:187` boot best: `parseFloat(SAFE_STORE.get('swarmbest')||'0')`
- `swarm.html:208` charcoal boot: `SAFE_STORE.getJSON('priv_charcoal',[])` (was `JSON.parse(localStorage.getItem(...)||'[]')` — corrupt JSON was also fatal)
- `swarm.html:311` meta boot: `SAFE_STORE.getJSON('priv_meta',{bank:0,tiers:{}})`
- `swarm.html:312` `metaSave(){SAFE_STORE.setJSON('priv_meta',meta)}`
- death best-writes ×3 (`hurtFishTouch`, contact-damage death, pass rock death): `SAFE_STORE.set('swarmbest',best)` (set() stringifies — identical stored bytes)
- charcoal death write: `SAFE_STORE.set('priv_charcoal',JSON.stringify(charcoal))`

### Fix 2 — audio candidate chain
- NEW consts: `AUDIO_BASES=['../suno/','suno/']`; state `bgmUrl='',bgmTrack='',bgmTry=0`.
- NEW `bgmNextCandidate()`: error handler; advances to next base; after all bases fail for a track, tries the old `flat_beat_loop.mp3` fallback track (across bases); after that: `fallbackDisco=true` (procedural disco synth takes over) and silent-skip.
- `startBgm()` rewritten: creates ONE `new Audio()` (no hardcoded URL), sets `onerror=bgmNextCandidate` BEFORE `src=AUDIO_BASES[0]+'gift_track.mp3'`, wires MediaElementSource/analyser as before, `play().catch` → fallbackDisco. Single element kept across swaps so the analyser survives (matches the old in-code comment).
- `bgmSwap(url)` rewritten: strips a leading `suno/` from the arg (all 4 call sites unchanged), resets the candidate chain, swaps `src` on the same element; every failure path is caught or promise-caught.
- Call sites `suno/jsr_loop.mp3` (storm), `suno/gift_track.mp3` (rain, pass exit), `suno/hemisync_loop.mp3` (enterPass) unchanged.

### Fix 3 — seeded-LCG replay law (toy.html port)
- NEW law block at old `rnd` site: `let lcg=1,runSeed=0,runN=0; function seedRun(s){...} const rng=()=>{lcg=(Math.imul(lcg,1664525)+1013904223)>>>0;return lcg/4294967296;};` — same LCG constants as toy.html.
- `rnd(a,b)` now draws from `rng()` (covers ~18 call sites: spawn offsets, gem scatter, knot pillars, light walls/gates, axes, fireball/bolt positions, pass fish/rocks).
- `startGame(forcedSeed)` — new optional param: auto-seed `(Date.now()^Math.imul(++runN,2654435761))>>>0||1` recorded in `runSeed`; pass a number to replay a recorded run (all existing call sites pass nothing → unchanged behavior).
- Direct `Math.random()` → `rng()` at gameplay sites: weather fireball timer, storm duration, bolt cadence, riddle pick, spawn side, spawn type roll, flyer baseY+phase, necromancer rise chance, level-up card draw, fish lunge recovery, knife shock-chain chance, door A pick, door B pick (13 lines).
- Carve-out: bolt zigzag in `draw()` switched `rnd()` → `Math.random()` — render-context draws must not advance the replay stream.
- REMAINDER (cosmetic, left on Math.random, recorded): poof particles, hit/death particle sprays, ally wiggle phase, horse speed/timing, enemy-mutter timing/victim/line, player-mutter line, screen-shake jitter, bolt zigzag (carve-out). Note: raindrop spawn (weatherUpdate) still draws via `rnd()` — it is sim-context (deterministic under replay) but burns LCG draws on visuals.

---

## HARNESS OUTPUT (verbatim, final run)

```
=== boot+title ===
PASS  title renders 45 frames

=== core-run ===
PASS  run reaches play state  | state=play
PASS  kills happening  | kills=3
PASS  run: camera locked on player  | camX=869.3 px=1536.0
PASS  run: player in world  | x=1536
PASS  run: no NaN in player  | hp=99999
PASS  run: entities finite  | en=11 gems=3

=== gate+descend ===
PASS  gate opens at depth end  | gate=true state=play depth=1
PASS  descend increments depth  | depth=2
PASS  fresh platform set loaded  | plats=3
PASS  descend: camera locked on player  | camX=1658.4 px=2325.0
PASS  descend: player in world  | x=2325
PASS  descend: no NaN in player  | hp=99999
PASS  descend: entities finite  | en=0 gems=4

=== fish-school ===
PASS  fish school tighter (cohort centroid)  | 69.1->9.7

=== necromancer ===
PASS  necromancer raises learned dead  | allies=2
PASS  allies hunt or rest cleanly  | n=2

=== weather ===
PASS  fireball heats water  | temp=0.62
PASS  storm emerges from heat  | state=storm temp=0.59

=== tide ===
PASS  tide raises floor near gate  | 77.8 units

=== fable-room ===
PASS  chair poses riddle  | riddle=without them the ledger 
PASS  chair answers with feet  | resolved; hp 99999->99999

=== the-pass ===
PASS  entered the pass
PASS  riding the mountains  | dist=140
PASS  pass exits to deeper maze  | state=play depth=2
PASS  pass-exit: camera locked on player  | camX=-256.2 px=410.4
PASS  pass-exit: player in world  | x=410
PASS  pass-exit: no NaN in player  | hp=99999
PASS  pass-exit: entities finite  | en=0 gems=0

=== death+bonfire+charcoal ===
PASS  death happens  | state=dead
PASS  charcoal marks the death  | 0->1
PASS  bonfire souls banked  | bank=0

===== DOGFOOD VERDICT: 32/32 =====
EXIT=0
```

- `node scripts/playtest_swarm.js` → 32/32, exit 0 (also 32/32 on the pre-forcedSeed run).
- `node --check` on extracted main script: SYNTAX OK (79,332 bytes of JS).
- Seeded-run variety is visible across the two harness runs (riddle changed, kill counts differ) — auto-seed per run works; invariants all hold.

## RNG REPLAY PROBE (verbatim)

```
REPLAY1 flyer:390|flyer:-30 seed=7
REPLAY2 flyer:390|flyer:-30 seed=7
DIFFSEED walker:390|walker:-30 seed=9
REPLAY_MATCH true
SEED_SENSITIVE true
AUTO_SEEDS_DISTINCT true
```
Also: seed-42 LCG stream sampled twice → byte-identical 8-draw sequence.

## GREP PROOF — zero bare localStorage

All `localStorage` occurrences in `dashboard/static/games/swarm.html` (the ONLY two, both inside the SAFE_STORE bootstrap):

```
12:// ---- SAFE STORAGE (privacy-mode law): localStorage throws in private browsing / blocked-cookie
17: try{ls=window.localStorage;ls.setItem('__swarm_probe','1');ls.removeItem('__swarm_probe');}
```

`grep -n "localStorage\." swarm.html | grep -v "ls=window.localStorage" | grep -v "__swarm_probe"` → empty (zero bare access sites remain; was 8). Stale duplicate `dashboard/static/swarm.html`: 0 SAFE_STORE refs → untouched.

## AUDIO-CANDIDATE BEHAVIOR NOTE

Assets exist only at `dashboard/static/suno/` while the game deploys under `/games/`, so `suno/x.mp3` relative to the page 404s where deployed. Loader law now: for every track, try `../suno/` first (sibling of `/games/` → resolves to the real `static/suno/`), then `suno/` (in-tree copy layout), then silent-skip. Failure semantics: `error` events advance the candidate chain on the SAME audio element (analyser wiring survives); after both bases fail for the primary track, the old `flat_beat_loop.mp3` fallback is tried across both bases; if that also fails everywhere → `fallbackDisco=true` and the procedural 122bpm disco synth covers the beat. No fetch failure can throw into the game loop — every candidate step is inside try/catch and every `play()` rejection is promise-caught. Headless/node (no `Audio`) aborts in the first try block → straight to synth, which is how the dogfood harness runs green.

## Verification commands

```
node --check <extracted main script>        # SYNTAX OK
node scripts/playtest_swarm.js              # DOGFOOD VERDICT: 32/32, EXIT=0
grep -n "localStorage" dashboard/static/games/swarm.html   # 2 hits, both the guarded accessor
```
