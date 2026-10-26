# W3 — souls messages (async template-word messages for frontier_souls.html)

Wave: wave_20260916 · Lane: THE WEAVE top-10 #2 · Status: **DONE** (2026-09-16)

## Scope

Async template-word message system for `dashboard/static/games/frontier_souls.html`:
players compose messages from template fragments (bounded legal vocabulary),
messages appear in OTHER runs at the spot where the author stood, facing the
danger they warned about or taunted. Compose costs nothing; appearance is
deterministic from the seeded stream. Content from the lexicon pool only —
no free text = no moderation surface, no invention.

## Log

- [2026-09-16] Receipt opened. Canonical file located: `dashboard/static/games/frontier_souls.html` (1828 lines; `site/dist/games/frontier_souls.html` an identical copy). Harness: `scripts/test_frontier_souls.js`, 42 lanes baseline.
- [2026-09-16] Read game structure end to end: two clocks (radial rings = level, 24px steps = event clock), `window.FS` test handle, `newRun`/`seedWorld` seeding, draft-overlay world-hold pattern, chronicle + `fs_lore`/`fs_unlocks` localStorage patterns.
- [2026-09-16] **CONCURRENT WRITER DETECTED (honored, not clobbered):** mid-edit, lane W1A (THE WEAVE build order #58) landed the fleet seed law in the same file — FNV-1a(UTC day) → LCG `wrng()` stream governing passes + decor, explicit `seedRun(n)` pinning, `runSeed` exposed on `window.FS`. W3 re-anchored its plan: soul-sign appearance order keys off **`runSeed`** (the fleet stream) instead of the run counter, so souls messages ride the same seed law as the world ("same day, same desert, same words in the same order").
- [2026-09-16] Implemented souls message system (single new block + 7 integration points, details below).
- [2026-09-16] Extended harness with lanes 43–49. First run after game edits: 42/42 green (no regressions). Full run: **49/49 green** (output verbatim below).
- [2026-09-16] UI key-path smoke test (C opens slate → world holds → A/W/D/S cycle → E posts → lexicon text renders): OK, posted `RATTLESNAKES — ROLL — or fade like me`.
- [2026-09-16] Surface law honored: canonical edited → byte-copied to `site/dist/games/frontier_souls.html` (cmp clean) → `build_vislab_catalog.py` re-run (240 entries / 9 buckets / 110 health verdicts); catalog entry now `sha:71839ba9`, 94903 B, status live — matches canonical sha16 `71839ba9747a92d3`.
- [2026-09-16] Canon updated: `memory/game/FRONTIER_SOULS_CANON.md` — souls messages section + lane count 36→49.

## Implementation summary

Files touched:
- `dashboard/static/games/frontier_souls.html` (canonical game; +~130 lines)
- `site/dist/games/frontier_souls.html` (derived byte-copy)
- `scripts/test_frontier_souls.js` (+7 lanes, 42→49)
- `memory/game/FRONTIER_SOULS_CANON.md` (canon section)
- `dashboard/static/vislab/catalog.{json,html}` (derived, sha refresh)

Game mechanics added:
1. **Lexicon** — `SOULS_LEX`: three fixed pools, `danger` / `verb` / `tail`, 8 words each. `SOULS_KEYS = ['danger','verb','tail']`. A message is a 3-slot template `danger — verb — tail`.
2. **Compose UI** — `C` during play opens the compose slate; the world holds (mirrors the sign-draft hold). A/D or 1/2/3 select slot, W/S cycles the word, E posts, Q/Esc walks on. Live preview line. Costs nothing (no essence, no timer).
3. **Ledger** — `composeMessage(slots)` binds `{id, x, y, facing, run, slots}` (player position + facing at post time); validates via `validSouls` (integer indexes in pool range, finite coords within ±2860, facing ≤ 2π); persists to `fs_souls` localStorage; FIFO cap `SOULS_MAX = 60`; load filters invalid entries — **the save format cannot carry free text at all**.
4. **Spawn logic** — `seedSoulsigns()` (called in `newRun`) picks messages from **prior runs only** (`m.run < G.runs` — words never haunt the run that spoke them), caps at `SOULS_PER_RUN = 12`, and orders them by the fleet seed stream: `hash2(id*7 + runSeed*131, cell)` (W1A's stream), tie-break by id. Each sign stands at the exact recorded spot, rendered as a weathered plank with a pulsing soul-light halo, a leaning marker along the author's `facing` (toward the danger they met).
5. **Reading** — within 90px the sign shows its words glowing above it; first read writes a chronicle line ("words in the sand: …") and feeds +4s of soul timer (the dead still give a little road).
6. **`window.FS` additions** — `souls`, `soulsigns` getters; `SOULS_LEX`, `SOULS_KEYS`, `composeMessage`, `soulsText`, `validSouls`, `seedSoulsigns`.

## Harness output (verbatim)

```
PASS  1 it compiles + window.FS lives
PASS  2 Adam's three: nell strongest AND slowest, allzaban fastest
PASS  3 canyon wake: ring 1, the scorpion waits (Adam storyboard)
PASS  4 THE LAW: steps advance with movement
PASS  5 THE LAW: any direction levels you — east works
PASS  6 THE LAW: any direction levels you — west works too
PASS  7 canyon cliff holds — and the worn passes lead out
PASS  8 the pit forgives — the soul does not fade until you climb out
PASS  9 tumbleweed hurts and cannot be hurt
PASS 10 pack rat bites and steals essence
PASS 11 scorpion: attackable, dies, pays essence
PASS 12 rattlesnake: 50/50 can simply kill you (forced true)
PASS 13 rattlesnake: the roll dodges even the fatal bite
PASS 14 coyote pack closes the circle
PASS 15 cowboys: one strong OR many weak — both spawn right
PASS 16 lone gunman duels, dies, pays the fire-rate mod
PASS 17 oasis heals, refills the soul, and keeps the horde out
PASS 18 wishing well: one wish, one level
PASS 19 merchant sells a mod — the shot changes color
PASS 20 storyline chain 1: grave -> journal -> the hermit's fire
PASS 21 the death timer: fades, essence feeds it, zero ends you, scrap restarts
PASS 22 the rim: DEATH rises, and killing him is the victory
PASS 23 perf: 100 foes keep steps under 8ms
PASS 24 CHRONICLE: the run writes its own log
PASS 25 GRUDGES: survivors get named, faster, remembered
PASS 26 SIGNS: level-up offers a draft and the world holds
PASS 27 DEAD MAN'S HAND: every 8th shot doubles
PASS 28 PREACHER'S LAST WORD: cheats death once
PASS 29 RATTLESNAKE'S SECRET: the rattle never out-right kills
PASS 30 DYNAMITE: the leader lobs it, it telegraphs, it hurts both sides
PASS 31 THE COMBINE: wounded cowboys merge into THE DEPUTY
PASS 32 WHISKEY: the world drinks slow, you do not
PASS 33 REWIND: the desert gives back five seconds, once
PASS 34 CACHE: key, box, payout
PASS 35 QUICKSAND: the sand drags
PASS 36 SLEEP: nothing hunts until it sees you
PASS 37 DEATH has weight now: 900 blood, and he hunts
PASS 38 THE HUNT: the lunge closes the gap you hide behind
PASS 39 THE HARVEST: at two-thirds blood the withered rise
PASS 40 THE REAPING: death stops walking — he steps between shadows
PASS 41 the sweep drinks: he steals your soul and feeds
PASS 42 his presence withers: the timer bleeds faster in close
PASS 43 SOULS LEXICON: three bounded pools, and no path in for free text
PASS 44 SOULS COMPOSE: costs nothing, binds spot + facing, silent in its own run
PASS 45 SOULS LAW: composed in run A — it stands in run B at the recorded spot, facing the recorded way
PASS 46 SOULS LAW: same seed -> same sign order (fleet stream governs appearance)
PASS 47 SOULS READ: stand with a sign and it gives its words
PASS 48 SOULS LAW: every renderable message is inside the lexicon closure
PASS 49 SOULS LEDGER: bounded — old words blow away like sand

49/49 lanes green
```

(`node scripts/test_frontier_souls.js`, exit 0.)

## Replay-law compliance proof

- **Compose in run A → appears in run B at the spot** — lane 44: compose binds `x/y/facing/run` and is absent from the authoring run's signs (`m.run < G.runs` filter; essence unchanged = free). Lane 45: after `startRun`, a sign exists within 2px of the recorded spot with the exact author facing (`-1.2`), correct ledger id, and renders exactly `SOULS_LEX.danger[0] — SOULS_LEX.verb[1] — SOULS_LEX.tail[2]`. PASS both.
- **Same seed → same message order** — lane 46: five messages composed; `M.seedRun(4242); startRun()` twice → identical sign-id order (`JSON.stringify(ordA) === JSON.stringify(ordB)`), all 5 signs on their recorded spots. Order key is `hash2(id*7 + runSeed*131, cell)` — a pure function of the W1A fleet seed stream, so replaying the same seed reproduces both which signs show (cap 12) and their order. PASS.
- **Lexicon-only enforcement** — structural, at three layers: (a) compose API accepts only integer slot indexes and rejects out-of-range/negative/non-integer/string words/wrong arity/null (lane 43 — a word string has no path in); (b) the persisted format is `{id,x,y,facing,run,slots[3]}` — prose cannot be represented, and `validSouls` drops any tampered entry on load; (c) lane 48 proves every renderable string is inside the closed set of `8×8×8 = 512` legal pool combinations, for the whole ledger and a boundary compose. PASS.

## Final

- **Lexicon size: 3 pools × 8 words = 24 words; 512 legal messages; 0 free-text bytes.**
- 49/49 harness lanes green (42 prior + 7 new), exit 0; no prior lane regressed.
- Surfaces consistent: canonical `dashboard/static/games/frontier_souls.html` = `site/dist/games/frontier_souls.html` (byte-identical, sha16 `71839ba9747a92d3`, 94,903 B); vislab catalog entry `sha:71839ba9` live.
- Concurrent W1A fleet-seed lane detected mid-flight and honored — souls sign order rides their seed stream.
