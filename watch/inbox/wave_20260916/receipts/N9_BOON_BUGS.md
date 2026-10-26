# N9 — Hades boon draft: max-law fix + first harness (replay-law BD lanes)

Lane: wave_20260916 / N9
Scope: `dashboard/static/games/mud.html` (boon draft subsystem), `scripts/test_mud_replay.js` (5 new BD lanes)
Claims audited: HG2 row #20 — "Known dead code: `!b.max` filter never gates (Apollo torch + Hermes speed stack forever); picks fall through to weapon swap; mines laugh at SUPERHOT"
Method: every claim probed empirically against live bytes BEFORE fixing (node probe, DOM shim from the FX4 replay pattern). Trust bytes, not reports.
Constraints honored: no git commands; Write/Edit only for source; receipt appended as work proceeded.

## Verification log (per claim, against live bytes)

- **Claim 1 (boon pool max law) — LIVE, confirmed with a twist.** Bytes: `const pool = BOONS.filter(b => !(player.boons || {})[b.id]);` — no `max` semantics exist anywhere: no BOONS entry carries a `max` field, and picks are marked `player.boons[b.id] = true` (boolean). HG2's failure direction was wrong for current bytes: boons do NOT "stack forever" — taken boons are excluded outright. The live defect is the inverse: the three boons whose applies are written as increments (APOLLO torch `boonVision += 0.18`, HERMES `bonusSpeed += 30`, CHRONOS `superBonus += 2`) can never be re-offered, and no boon is ever "removed at max stacks" because max does not exist. The filter never gates on max because there is nothing to gate — HG2's core observation holds.
- **Claim 2 (pick → weapon-swap fall-through) — NOT LIVE in current bytes.** The pick block already clears the pressed flags (`keys['Digit1_p'] = keys['Digit2_p'] = keys['Digit3_p'] = false;`) before the swap block runs (`if (keys['Digit1_p'] && !G.boonDraft) ...`). Probe: forced level-up → draft open → Digit1_p / Digit2_p → boon applied, draft closed, `weaponIdx` unchanged on both paths. The claim appears to be a fossil of an older revision (or of the design doc HG2 mined). Hardened anyway per mission: the swap is now branch-isolated structurally, not just flag hygiene (see Fix 2).
- **Claim 3 (mines immune to SUPERHOT) — NOT LIVE in current bytes.** `update(dt)` is one function: the SUPERHOT gate (`wdt = moving ? dt : dt * 0.06; ... dt = wdt;`) reassigns the parameter at the top, and the mines loop (`m.arm -= dt; m.life -= dt;`) runs downstream on the dilated dt. No `dt` shadowing exists anywhere between the two (grep: only `let wdt`/`wdt=`/`dt = wdt` in the whole function). Probe: 1.0s idle window with `G.super = 4` → mine decayed exactly 0.06s (arm and life) vs 0.80s/1.00s control without super. Mines obey the dilation law. No code change made; pinned as a regression lane instead.

Note: a stale twin exists at `dashboard/static/mud.html` (100,832 bytes, differs from canonical `games/mud.html`). The twin has the same guard (its line 1594) and the same dilation (its 948 → 1404-1405), so neither copy reproduces claims 2/3 either. Twin drift is HG2's own documented pattern (its ⚠ correction); out of N9 scope — the replay harness covers `games/mud.html`.

## Fixes

**(1) Max-stacks law** — `dashboard/static/games/mud.html`:
- `max: 3` added to the three stack-designed boons (torch, hermes, time); all others default `max || 1`.
- Taken-tracking is now a count: `player.boons[b.id] = (player.boons[b.id] || 0) + 1;` (was `= true`).
- Pool filter restored: `BOONS.filter(b => (taken[b.id] || 0) < (b.max || 1))` — a boon at max stacks is removed from the offered pool; a stackable below max re-offers. (The previously dead `const taken = player.boons || {};` is now load-bearing.)
- Snapshot-compat verified: the replay snapshot joins `Object.keys(p.boons)` (keys only — counts don't change its shape); draft-card render never reads `player.boons`.

**(2) Pick/swap isolation** — the draft pick block now sets a `draftPick` flag and both weapon-swap lines are gated `if (!draftPick && keys['DigitX_p'] && !G.boonDraft)`. The input event a boon consumed can never reach the swap block, structurally, independent of flag hygiene. Behavior-preserving (the old flag-clear already suppressed it — lane 15 pins both the guarantee and a control proving plain swaps still work).

**(3) Mines/SUPERHOT** — no code change (verified compliant; measured 0.06x). Pinned by lane 16.

## Harness — the system's first lanes (scripts/test_mud_replay.js, BD section)

Draft offers were already routed through the seeded LCG (`let roll = rng() * total`, comment-tagged `// gameplay:`) and boonDraft ids ride the replay snapshot's `g` field — so drafts replay under the existing F1 law. Five dedicated lanes added: offers seeded (same seed → identical offer sequence), offers legal (known ids, ≤3 cards, no in-offer dupes), max law end-to-end (stackables re-offer below max, maxed boon never re-offered, pool drains to no-draft), pick-never-swaps (both digit paths + live-swap control), mine dilation (0.06x idle law + real-time window tick).

## Harness output verbatim (`node scripts/test_mud_replay.js`, post-fix)

```
    evlog: 13 events over 1800 steps (clear, death, hurt, room, run)
    INPUT_FORK @ step 160 (t=2.667s): Space press -> KeyA press
    STATE_FORK $.p[0]: 333.33333333333303 -> 329.9999999999997
    EVENT_FORK @ evlog[4]: {"t":6.75,"e":"hurt","d":14,"hp":86} -> {"t":6.3,"e":"hurt","d":14,"hp":86}
    first divergence vs alt seed at step 0; evlog run stamps differ, full logs differ
    mine under superhot: 0.060s arm decay vs 0.800s control (0.06x law); window ticked 1.000s real
PASS  1 R: game compiles + window.MUD live + startGame(forcedSeed) records runSeed
PASS  2 R: stream law — post-seed LCG state is a function of the seed alone
PASS  3 R: stream law — the LCG advances during play and reseeds on startGame
PASS  4 F1: same seed + same tape twice -> byte-identical event log (evlog)
PASS  5 F1: same seed + same tape twice -> byte-identical state trace (all 1800 step digests)
PASS  6 F1: the run actually lived — event log is non-vacuous (activation + combat/hazard events)
PASS  7 F2: flipped input -> state trace diverges (the tape is load-bearing)
PASS  8 F2: the fork is NAMED at the exact step of the flipped input
PASS  9 F2: event logs diverge too — first differing event named
PASS 10 F2: both forked runs keep their recorded seed — inputs never touch the stream seed
PASS 11 G: different seed + same tape -> different run (the seeded stream is load-bearing)
PASS 12 BD: draft offers are seeded — same seed + same level-up presses -> identical offer sequence
PASS 13 BD: offers are legal — known ids only, at most 3 cards, no duplicate within one offer
PASS 14 BD: max law — stackables re-offer below max, and a maxed boon leaves the offered pool
PASS 15 BD: picking a boon never swaps the weapon (both digit paths, with a live-swap control)
PASS 16 BD: mines dilate under SUPERHOT with the rest of the world (idle 0.06x law)

16/16 lanes green
mud: 2372 lines, seed 20260916, 1800 steps @ 60fps, tape A 13 events, runSeed 20260916
```

## Per-bug before/after evidence

**Bug 1 — max law.**
- BEFORE (probe, forced level-ups picking card 1): `picked sequence: thorns,wave,berserk,chain,cloud,hermes,time,dash,arc,torch,leech,crit` — `any id taken twice: false`; stack-designed boons (torch/hermes/time) unobtainable a second time; no `max` field exists on any BOONS entry; pool filter has no max term.
- AFTER (same probe): `picked sequence: wave,leech,thorns,hermes,arc,time,dash,time,crit,hermes,berserk,cloud,hermes,time` — `per-id counts: {"wave":1,...,"hermes":3,...,"time":3,...}` — stackables re-offer and cap at exactly max=3; no id exceeds max. Harness lane 14 asserts the full law including pool drain → `eq(forceDraft(M), null, 'a draft still opens after the pool drained — max law dead')`.

**Bug 2 — pick/swap fall-through.**
- BEFORE (probe): draft open, Digit1_p → `card0=thorns applied=true draftNow=closed; weaponIdx before=0 after=0 — SWAP did not fire`; Digit2_p path identical. Claim already dead in bytes (flag-clear existed); fixed structurally with the `draftPick` branch per mission.
- AFTER: lane 15 green — Digit1 pick holds `weaponIdx=1`, Digit2 pick holds `weaponIdx=0`, and the control proves a plain Digit1 press (no draft) still swaps to slot 0 (guard not over-strong).

**Bug 3 — mines vs SUPERHOT.**
- BEFORE (probe, 1.0s idle, `G.super=4`): `mine arm decayed 0.06 | life decayed 0.06` vs control `arm decayed 0.8 | life decayed 1`. Law already held — HG2 claim refuted by measurement.
- AFTER: unchanged by design; lane 16 green with the window-tick assertion (`window ticked 1.000s real`).

## Gate

- Pre-fix baselines (bytes as found): `test_mud_replay.js` 11/11 green · `test_mud_fifty.js` 58/58 green.
- Post-fix: `test_mud_replay.js` **16/16 green** (11 original + 5 new BD lanes) · `test_mud_fifty.js` **58/58 green** (the mud gate; grown from 51 by earlier lanes — no boon lanes existed before N9).
- Concurrency note: `games/mud.html` was edited by another lane mid-audit (+248 bytes); fix sites re-verified in bytes immediately before each Edit; post-fix gates re-run on the final bytes.
- Python pytest suite not run: no Python touched (JS game + JS harness only).

## Weave moves left open

- Port the max law + draftPick branch to the stale twin `dashboard/static/mud.html` when the twin-dedupe lane lands (HG2 ⚠).
- HG2 row #20's unify move stands: mud boon draft + frontier SIGNS draft → one draft engine, two skins.
