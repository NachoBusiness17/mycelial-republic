# U6 — UNION-ALPHA CREATIVE BUNDLE (Frontier Souls SIGNS + Soul Castle NPC voices)

- **Lane:** U6 (wave-lane) · **Date:** 2026-09-16 · **Budget:** $0 — `stealth/union-alpha` free window (ends ~2026-09-23). 402/403 or paid-wall → record and STOP.
- **Wave-lane law:** receipt FIRST (this file, before any call), append as you go, no git.
- **Worker law:** `stealth/union-alpha` on OpenRouter as drafting pen; `OPENROUTER_API_KEY` via `mag.flight_recorder.load_env`, never printed, never written to any row. This agent is the EDITOR applying fleet craft rules; best verbatim lines kept.
- **Deliverable (end of this receipt):** ITEM 1 — 8 road-sign texts for `dashboard/static/games/frontier_souls.html` (one line each, western-dry, technically true but half the story, family-friendly-dry). ITEM 2 — 4 Soul Castle NPC intro speeches (monk-doorkeeper, lamplighter, doubting knight, questioning bell; 3–4 sentences each; no em-dashes, no AI tells, plain words, reader fills the bias). Plus one line: can the stealth model hold a voice or does it flatten?

## Context consumed

| File | What it gave |
|---|---|
| `memory/game/FRONTIER_SOULS_CANON.md` | SIGNS law: "SIGNS level-up draft (8 omens, world pauses…)" — signs are level-up omens; canon fauna/events (rattlesnake 50% instakill, tumbleweed, coyotes, gangs, wishing well, grave→hermit chain, death timer, concentric rings, Death at the rim) |
| `watch/inbox/FRONTIER_SOULS_INTAKE_20260915.md` | Adam's bible: gritty not cartoonish, Arizona grays/browns, every enemy can be the end, steps→events, buzzards |
| `watch/onboard/TEAM.md` L45 | "Melissa — words: books, worlds, Soul Castle" — no prior Soul Castle lore file exists in `watch/inbox` or `memory/game`; the four NPCs + voice law in the mission are the spec |
| `mag/research_fanout.py` L146–151 | `or-union-alpha` lane: `https://openrouter.ai/api/v1`, model `stealth/union-alpha`, openai-style, free window ends ~2026-09-23 |

## Steps (append as they land)

- [x] step 1: Soul Castle lore lookup — no lore file exists; TEAM.md confirms Melissa owns the world. Mission NPC list + voice law = spec. Soul Castle creative starts from a clean page (noted for the operator: first canon seeds for that world are being laid here).
- [x] step 2: runner written — `watch/inbox/wave_20260916/u6_union_creative.py` (mirrors U2/E law: `guard_endpoint` https+allowlist openrouter.ai only, key via `load_env` never printed, raw tape append-only to `watch/salon_responses/u6_union_creative/raw.jsonl`, schema `u6_union_creative.v1`, temp 0.9, 402/403 → stop). Pen asks: 10 sign candidates (editor curates 8), 2 options per NPC ×4 (editor picks 1 each). Fired 2026-09-16: SIGNS ok 148s in=325 out=113 · CASTLE ok 134s in=367 out=438. Raw text below.

### Raw pen output — SIGNS (verbatim, stealth/union-alpha)

1. Safe passage. Bring your own luck.
2. Rest here. The dust does not sleep.
3. Well water. Mind the reflection.
4. Coyote watch. They know your pace.
5. Grave of a stranger. Do not borrow his fate.
6. Canyon rim. The view improves with breath.
7. Dead end. The road continues.
8. Snake pit. Dry heat.
9. Gang territory. Polite words are cheap.
10. Your soul. Keep it close.

### Raw pen output — Soul Castle (verbatim, stealth/union-alpha)

- 1A (doorkeeper): Set your pack on the step, where I can see your hands. I have kept this door since the oak was pale. Some folk I turn away come back with less to carry.
- 1B (doorkeeper): You may knock once; I am old, not deaf. Before I lift the bar, tell me who knows you have come. There is a bench here for those who need time to answer.
- 2A (lamplighter): Mind the oil tin by your foot. I light these lamps from the gate to the tower, then walk back to see which have gone out. If you leave after dark, I will be on that round.
- 2B (lamplighter): Stand near the lamp while you look for your name on that list. They write the names small, and rain gets under the glass. I have asked for a roof over it, but they gave me a brighter wick.
- 3A (doubting knight): Keep to my left; the sword hangs on my right. I can hold this gate against six men, if the hinges hold. I used to know why six men would want it.
- 3B (doubting knight): You have come without a shield. There are spare ones in the guardroom, though you will have to scrape off the names. Mine belonged to a man who taught me what we were guarding, but he is dead, and no one gives the same answer now.
- 4A (bell): Did you hear me on the road? When the sound stopped, did you stop too? What brought you the rest of the way?
- 4B (bell): Can you see the rope beside the gate? Will you pull it once for the keeper, or twice for the dead? Have they left no way to ring for someone who is lost?

- [x] step 3: editorial pass (fleet craft rules). Kept verbatim: signs 1/3/7 whole; sign 4's second sentence; castle 1A, 2B, 3A whole; bell 4B questions 1–2. Cuts and why:
  - sign 2 "does not sleep" → "won't" (boards are short; same truth, harder stop).
  - sign 5 "Do not borrow his fate" CUT — it tells the lesson, violating the half-the-story law. Rebuilt as "He stopped here too." (true; lets the reader hear the warning themselves).
  - sign 6 "improves with breath" CUT — muddy. "The view is free." (true at the rim; everything else up there is Death).
  - sign 8 "Snake pit. Dry heat." CUT — joke with no teeth. Rebuilt on the game's own canon law (rattle warns ≤170px before the strike): "Rattlesnakes. They warn you first." Half the story: the warning does not save you.
  - sign 4 "Coyote watch" → "Coyote country" (sign idiom); second sentence kept verbatim.
  - sign 9 dropped (flattest of the ten), sign 10 dropped ("Keep it close" is greeting-card, on-the-nose where the law wants restraint).
  - bell 4B third question CUT ("Have they left no way to ring for someone who is lost?" — tangled). Replaced with "Will you answer when I ring for you?" (still a question; lands what the bell is for; reader fills the rest).
  - Craft sweep on all finals: no em-dashes, no AI tells (delve/tapestry/testament absent), no modern slang, family-friendly-dry throughout.

- [x] step 4: FINAL TEXTS (filed here; the receipt is the durable artifact on the shared inbox).

## DELIVERABLE 1 — Frontier Souls: 8 road-sign texts (for `dashboard/static/games/frontier_souls.html`)

1. Safe passage. Bring your own luck.
2. Well water. Mind the reflection.
3. Rest here. The dust won't.
4. Coyote country. They know your pace.
5. Stranger's grave. He stopped here too.
6. Rattlesnakes. They warn you first.
7. Rim ahead. The view is free.
8. Dead end. The road continues.

Every sign technically true: the road is passable (luck not included), the well grants the wish (look at yourself first), rest is possible (the world never rests), coyotes do trail your stride (in packs), the stranger did stop (the grave is where the journal is), rattles always warn first (it strikes anyway), the rim view costs nothing (the rim is Death), and the dead end was real for whoever painted it.

## DELIVERABLE 2 — Soul Castle: 4 NPC introductions (Melissa Hallman's world)

**THE MONK-DOORKEEPER** *(pen verbatim, 1A)*
Set your pack on the step, where I can see your hands. I have kept this door since the oak was pale. Some folk I turn away come back with less to carry.

**THE LAMPLIGHTER** *(pen verbatim, 2B)*
Stand near the lamp while you look for your name on that list. They write the names small, and rain gets under the glass. I have asked for a roof over it, but they gave me a brighter wick.

**THE DOUBTING KNIGHT** *(pen verbatim, 3A)*
Keep to my left; the sword hangs on my right. I can hold this gate against six men, if the hinges hold. I used to know why six men would want it.

**THE BELL** *(pen 4B, third question replaced)*
Can you see the rope beside the gate? Will you pull it once for the keeper, or twice for the dead? Will you answer when I ring for you?

## Voice verdict

The stealth model can hold a voice: given a named law it produced real parable lines verbatim-worth keeping ("Some folk I turn away come back with less to carry", "they gave me a brighter wick", "I used to know why six men would want it") and obeyed the no-em-dash/no-tell rule completely; it only flattens when asked for aphorism (signs drift to moral tags and greeting-card closes), so use it for voices and edit its morals.
