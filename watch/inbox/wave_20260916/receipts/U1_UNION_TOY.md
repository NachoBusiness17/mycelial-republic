# U1 — UNION-ALPHA BUILDS THE TOY (A3 build order executed)

- Lane: U1, wave 2026-09-16 · Status: **FILED — 12/12 lanes green**
- Receipt-first per wave-lane law. No git. Worker = stealth/union-alpha on OpenRouter, free window, **cost: $0** (usage `cost: 0` in the response; total 5397 tokens). OPENROUTER_API_KEY loaded via `mag.flight_recorder.load_env`, never printed, never logged.
- Mission: execute A3's build order — strip `dashboard/static/mud.html` to THE TOY (core verb = i-frame roll: read → roll → punish), union-alpha as the code-generation worker, this agent as editor, `scripts/test_toy.js` proving 3 lanes on the fifty-lane shim pattern.

## Spec consumed

| File | What it gave |
|---|---|
| `watch/inbox/wave_20260916/receipts/A3_THE_TOY_CORE_VERB.md` | Constants (windup 0.35 / iframes 0.35 / roll 0.28 / stamina 100·30·15 / attackCd 1.2 / regen 25/s), P-LEGAL law, `toy_play.v1` shape, 3 CI lanes |

## Steps (append as they land)

- [x] step 1: read mud.html combat/input sections
  - `dashboard/static/games/mud.html` (2311 ln): input shim L33–48 (keys + `_p` just-pressed); roll L829–841 (ShiftLeft, 30 sta, rollT 0.28, rollCd 0.5, iframes 0.35, 420 px/s); swing L864–867 (Space, 15 sta, cd 0.35, arc hit); regen L933–938 (25/s, moving ×0.5 / still ×1.5); walker AI + windup L1073–1108 (`e.windup=0.35; e.attackCd=1.2; e.telegraph=0.35` at range, plants at 0.12× while winding, bite at windup end if `d < r+r+10`, rollT>0 ⇒ stumble+riposte instead of damage); walker stats L600 (hp 40, speed 70, dmg 14, r 14).
  - `scripts/test_mud_fifty.js` (496 ln): the harness pattern — DOM shim (Proxy ctx / fakeCanvas / shimWindow) → `new Function('window','document',…, code)` → `window.MUD` → `pump(n, dt)` + `keys[CODE]` pokes + lane()/assert()/eq() framework. Toy CI rides this unchanged.
  - `mag/research_fanout.py` L146–152 + `call_lane`: `or-union-alpha` lane = `https://openrouter.ai/api/v1` + model `stealth/union-alpha` + OPENROUTER_API_KEY, openai-style body, generous max_tokens (reasoning models spend budget before content), never raises — failures are recorded rows. `mag/flight_recorder.load_env` parses .env, values never logged.
  - node v22.23.1 present on PATH.
- [x] step 2: union-alpha drafts toy.html
  - Prompt filed at `watch/inbox/wave_20260916/u1_union_prompt.md` (4,941 bytes): exact constants, RNG law (`(Math.imul(s,1664525)+1013904223)>>>0`), determinism law (fixed 1/60 timestep, tape via same press/release path as live keys), event schema, P-LEGAL law, `toy_play.v1` receipt, headless `window.TOY` contract, ~200-line budget.
  - Call runner `watch/inbox/wave_20260916/u1_union_call.py` (4,105 bytes), run with `.venv\Scripts\python.exe`.
  - **Storm log:** attempt 1 (buffered): HTTP 200 after 301s, body = pure whitespace, no `choices` — the known stealth padding pathology. Degrade law applied: retried in **stream mode**, attempt 1 landed in 108.5s: 9,713 chars, `finish_reason: stop`, `cost: 0`. 429/402 count: 0. Draft filed at `watch/inbox/wave_20260916/u1_union_draft.html` (9,713 bytes).
- [x] step 3: editor review + fixes → `dashboard/static/games/toy.html`
  - **Kept from union-alpha verbatim or near-verbatim:** the sha256 H/K constant tables (verified programmatically against computed primes — zero typos), the LCG formula, the IIFE + `window.TOY` return shape, the tape-pump/event-log/receipt architecture, the draw-index law, browser key listeners, the souls-grammar comments.
  - **Defects found in the draft (all fixed):**
    1. `sha256` was not sha256: length field appended as **6 bytes instead of 8** (broke block alignment); hashed **only the first 16-word block** (every real receipt is multi-block); **never folded working vars back into state** (no Merkle-Damgård close). Any one of the three alone makes the receipt hash meaningless; all three made it deterministic garbage. Rewrote the body as a proper per-block loop — now passes known vectors + node:crypto cross-check.
    2. **P-LEGAL matcher dead on arrival:** `hit` events carried no `enemy` field, so `hits_no_telegraph` counted every hit as illegal (probe showed "8 illegal" = all 8). Added `enemy: 0`.
    3. **P2 law broken:** dodge check used `player.iframes > 0` instead of mud's `player.rollT > 0` — fails the exact-frame case (roll at windup start ⇒ iframes just expired at bite ⇒ hit lands). Fixed to the mud grammar (L1099).
    4. **Receipt seed field logged the mutated LCG state**, not the seed. Added `seed0`.
    5. **`inputs` in the receipt was the consumed leftover tape** (shifted empty by receipt time). Added an applied-inputs log.
    6. **Stale references:** `start()` rebound `player`/`walker`/`keys`/`events`, so every exposed `TOY.*` handle went dead after reset — CI would have been testing a ghost. In-place resets now; identity is stable.
    7. **Browser unplayable:** the rAF loop only rendered — nothing ever called `pump`, so Adam would have watched a still frame. Added accumulator fixed-step stepping (wall clock never touches sim state; replays still drive `pump` directly).
    8. **Walker never planted during windup** (mud: `v *= 0.12`), destroying the read-then-punish geometry. Restored.
    9. **Roll was x-axis only** (ArrowUp/Down movement didn't set facing or move regen state). Now 2D move intent, facing = `atan2`, mud regen law intact.
  - Final file: 232 lines (12,919 bytes) — shell + render + sim + sha tables; ~200 lines of code excluding the 64-constant K table, stated honestly.
- [x] step 4: `scripts/test_toy.js` (9,718 bytes) — 12 assertion lanes grouped in the 3 ordered lanes, fifty-lane shim pattern (Proxy ctx → `new Function` → `window.TOY` → static tapes → `pump`), plus harness-side recomputation of the P-LEGAL sweep (never trusts the toy's own counter) and a node:crypto cross-check of the toy's sha256.
  - node v22.23.1 present. Run: `node scripts/test_toy.js`.

## Test output (verbatim, 2026-09-16)

```
    INPUT_FORK @ t=0.933 (frame 56): ShiftLeft press -> Space press
    VERB_FORK @ t=1.017: rolled through the bite (hit_dodged) vs ate it (hit, -14 hp)
PASS   1 A: toy compiles + window.TOY live + sha256 matches node:crypto
PASS   2 A: same seed + same tape twice -> identical event log (byte-identical JSON)
PASS   3 A: same seed + same tape twice -> identical receipt sha256
PASS   4 A: receipt sha256 is the hash of its own canonical body
PASS   5 A: batching-invariant — pump(3600) x1 == pump(60) x60 -> same sha
PASS   6 A: the verb actually fired (telegraph -> roll -> hit_dodged -> kill) and first telegraph < 3s
PASS   7 B: flipped input -> receipts diverge (sha differs, tape is load-bearing)
PASS   8 B: fork is named at the exact frame — first differing event is the flipped input
PASS   9 B: the verb fork — at the telegraph end, TAPE_A dodged the bite and TAPE_B ate it
PASS  10 C: P-LEGAL sweep on TAPE_A — harness recomputes: no hit without a rollable telegraph
PASS  11 C: P-LEGAL sweep on TAPE_C (facetank tape, same seed) — still no hit without a telegraph
PASS  12 C: divergence is legal play — same seed, different tape, different log, both P-LEGAL

12/12 lanes green
toy: 232 lines, seed 20260916, tape A sha 678ddd9d2e189555…, verdict win, duration 1.717s
```

Reference run (seed 20260916, frozen TAPE_A): first telegraph **t=0.667s** (A3 gate <3s ✓), first riposte swing t=1.350s, `hits_taken 0`, `hits_no_telegraph 0`, verdict `win`, duration 1.717s, receipt sha256 `678ddd9d2e189555567d76197d1706d2d2e5b9aff05d49d0c4750fb049027195`. Game-bytes commitment (gitless content hash): toy.html sha256 head `ca4c18beebffdb56…`.

## Honest grade of union-alpha: **REWRITTEN** (from a structurally-correct skeleton)

Not usable-as-was, and more than "needed-edits": the draft could not have passed its own CI. Three defects were fatal (sha256 not sha256; the P-LEGAL counter structurally unable to ever match a hit; a browser shell that never simulates — the toy literally would not play). The dodge law was subtly wrong in exactly the edge case the P2 lane exists to catch. That said, the skeleton was real: architecture, LCG, constant tables (100% correct), event/receipt grammar, and roughly half the pump logic survived into the shipped file. As a free-window first draft to edit against: worth the $0 and the one streaming retry. As an unedited worker: it would have shipped a toy that hashes garbage and plays as a still frame. Verdict: worker = good scaffold; editor = load-bearing.

## Deliverables (paths + sizes)

| File | Bytes | Role |
|---|---|---|
| `dashboard/static/games/toy.html` | 12,919 | THE TOY — 232 lines, served by `mag.cmd lab` at :8765 |
| `scripts/test_toy.js` | 9,718 | CI: 3 lanes / 12 assertions, fifty-lane shim pattern |
| `watch/inbox/wave_20260916/u1_union_prompt.md` | 4,941 | worker prompt (constants + P-LEGAL law) |
| `watch/inbox/wave_20260916/u1_union_draft.html` | 9,713 | union-alpha's raw draft (evidence, unedited) |
| `watch/inbox/wave_20260916/u1_union_call.py` | 4,105 | worker call runner (key never printed; storm telemetry) |
| `watch/inbox/wave_20260916/receipts/U1_UNION_TOY.md` | (this file) | receipt |

## Honest notes

- mud.html lives at `dashboard/static/games/mud.html` (mission cited `dashboard/static/mud.html`); toy.html filed beside it so `:8765` serves it.
- attackCd 1.2 starts at **windup start** (faithful to mud L1092), so the calm-after-bite is ~0.85s. A3's "1.2s recovery" reading is the same mud bytes; if the punish window should start at bite, it is a one-line change — recorded, not silently tuned.
- `mag.shared_surface validate` reports `ok:false` — **pre-existing**: hundreds of unindexed root files from 09-01..09-16; `INDEX.json` contains zero wave entries, so wave-lane subdirectories (incl. this receipt and A3's) sit outside the index's scope. This lane added files only under `wave_20260916/` per receipt-first law; index repair is a separate lane's job.
- Swing arc is ±90° (half-angle) with 4-dir facing; swing range 55+player.r+walker.r = 81px — editorial constants, deterministic, commented where they matter.

## Log
- [x] receipt skeleton written FIRST
- [x] step 1 mud.html/harness/fanout sources read (bytes, not citations)
- [x] step 2 union-alpha dispatched (1 whitespace-storm + 1 streaming success, $0)
- [x] step 3 editor pass: 9 defects fixed, skeleton retained
- [x] step 4 test_toy.js written + run: **12/12 lanes green**, node v22.23.1
- [x] grade + paths + sizes + verbatim output filed
