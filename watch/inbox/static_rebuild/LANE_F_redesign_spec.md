# LANE F — THE REDESIGN SPEC: the better /static/

Lane: F/6 (synthesis) · 2026-09-10 · Workspace: `dashboard/static/`
Inputs sampled: viz_gallery.html, tesuji_map.html, burn_board.html, nav.js, home.html
+ known failures: wipeout-style fragmented versions, dead feeds, flat unsorted nav.

---

## THE POINT

/static/ stops being a junk drawer of 100 flat pages and becomes one organized
organism: six nested wings, every page wearing its own status and feed list like a
lab badge. Everything that already worked — the Viz Lab's attempts-as-tabs honesty,
the tesuji map's corridor-and-tri-state field grammar, home.html's evidence links —
becomes the standard, not the exception. And one state format per family kills the
wipeout class of failure permanently: pages are lenses on shared truth, never
private copies of it.

---

## 0. WHAT WE'RE BUILDING ON (evidence, not vibes)

| Artifact | The pattern it proves |
|---|---|
| `viz_gallery.html` | Tabs + attempts + honest notes ("attempt 1 — beautiful, wrong, kept as the record") + a footer that states THE POINT. The operator loves this. |
| `tesuji_map.html` | The visual bar: dark warm lab, corridors, stones colored by tri-state (SUPPORTED/DISPUTED/UNPROVEN + SHADOW), legend, "an empty corridor is data too", falsifier in the tip line, error-banner fixture. |
| `home.html` | Question-driven cards, "evidence:" links to the page that proves each number, live bytes not badges. |
| `nav.js` | The failure: 80+ flat links, no nesting, duplicates (maze_arena ×2, shadow_walk ×2, spectral_maze ×2, arena_field ×2). Duplication-as-emphasis degraded into duplicate rows. |
| `burn_board.html` | The failure: a server-stamped pre-dump with no nav, no status, no contract. Works today, orphaned tomorrow. |
| wipeout-class failures | The failure: pages keep private copies of shared state; versions drift; one edit wipes the other. |

---

## 1. IA — THE NESTED STRUCTURE

Six wings, top level. Sorted and nested, per the operator's law. One canonical path
per page; aliases redirect, never duplicate.

```
/static/
├── index.html            ← THE HUB: the six wings as cards (home.html evolves into this)
├── live/                 ← 1. LIVE ORGANISM — what is happening right now
│   ├── live.html         (overseer strip, the beating pulse)
│   ├── live_feed.html    feed.html, agents.html, fleet.html, health.html,
│   ├── lanes.html        seat.html, burn_board.html, spend.html
│   └── ...               (everything that reads a live feed and would be wrong if frozen)
├── viz/                  ← 2. VIZ LAB — every way we see the Republic (viz_gallery.html is the door)
│   ├── viz_gallery.html  (tabs = attempts, iframe stage — UNCHANGED pattern, more tabs)
│   └── ...               verkle knot wave, 3D verkle, spore fish, horse run, memory map,
│                          module map, shadow fields (room_lightmap, salon_lightmap, bad_apple),
│                          chain witness, rtfm graph, calabi-yau
├── games/                ← 3. GAMES & FALSIFIERS — probes as play
│   ├── falsifiers.html   (the falsifier ledger — the wing's index)
│   ├── maze_arena.html   arrakis.html, dungeon.html, spectral_maze.html, eraser_maze.html,
│   ├── ...               light_maze.html, tavern_brawl.html, incident_dungeon.html,
│   │                     tesuji_map.html (field map of the model), swarm/game.html
│   └── + every game page keeps its error-banner fixture (already fleet standard)
├── decks/                ← 4. DECKS — things the operator reads
│   ├── decks.html        (deck index)
│   └── decks/            salons/, keeper_voice, hardware_primer, field_quills,
│                          night book, doctrine/, museum
├── lab/                  ← 5. ARCHIVE & R&D — wrong turns kept honestly, experiments parked
│   ├── attic/            (existing attic + all *.bak-* files move HERE, stamped STALE, never deleted)
│   ├── attempts/         (superseded viz/game attempts — the "beautiful, wrong" shelf)
│   └── r&d/              half-built surfaces (wearable, self_hologram, calabi drafts)
└── data/                 ← 6. DATA — the JSON the wings render (already exists; becomes contract-bound)
```

### Nav model
- `nav.js` is rewritten as the **INDEX**: one JS manifest, one row per page:
  `{path, name, wing, status, feeds}` — the same manifest every page also embeds
  (see §2). The nav bar renders wings as groups, not a flat scroll.
- Hub (`index.html`) renders the manifest as six wing cards with live status chips:
  WORKS (cyan) / STALE (amber) / BROKEN (red) — the tri-state legend reused one
  level up. A BROKEN page is visible from the hub; nobody has to click into a corpse.
- Duplicates in today's nav.js collapse to their canonical path. Where two pages
  genuinely show the same truth through different lenses, that is EMPHASIS (allowed,
  labeled "same truth, other lens: X"), not a second copy of the data (banned, §4).

---

## 2. THE PAGE CONTRACT — self-describing pages

Every page opens with a manifest object and renders it as a standardized badge strip
under the header:

```js
const PAGE = {
  name:    "tesuji_map",
  wing:    "games",
  status:  "WORKS",                 // WORKS | STALE | BROKEN
  purpose: "GLM-5.3-flash behavior surface as a stone field",
  feeds:   ["/static/data/tesuji_map.json (poll 30s)"],   // every file it reads
  falsifier:"predictive >=70%",     // or "—, this page is a lens, see falsifiers.html"
  last_verified: "2026-09-10",
};
```

Rules:
1. **Status is a claim the page makes about itself** and the hub audits it: a page
   whose feed 404s or is older than its declared freshness DOWNGRADES its own badge
   to STALE/BROKEN at render time. Pages cannot lie about their feeds.
2. **No feed, no page**: the strip lists dependencies; a dead feed renders the
   honest empty state ("field empty — walkers out"), never a stale number wearing
   yesterday's clothes.
3. **The strip is one shared renderer** (`page_badge.js`), so the contract costs
   each page ~8 lines, not a re-implementation.
4. burn_board-class snapshots (server-stamped HTML) are allowed ONLY in lab/ with
   `status:"STALE"` — a snapshot that pretends to be live is the sin; a snapshot
   that admits it is a record.

---

## 3. THE GALLERY PATTERN EVERYWHERE

The spore fish rule, generalized: **every organ gets an attempts history.**

- Any wing page that has iterated (a viz, a game, a deck) gets an ATTEMPTS list —
  same shape as viz_gallery's TABS: `{name, src, note}` where the note is honest:
  "attempt 1 — beautiful, wrong, kept as the record".
- Old attempts are never deleted; they move to `lab/attempts/` and stay linked from
  the current page's gallery strip. Wrong turns are the corpus (operator law:
  honest records of wrong turns kept).
- This is already proven to delight: Viz Lab is the operator's favorite page. The
  redesign just stops rationing it.

---

## 4. THE SYNC STANDARD — one shared state format per family

The wipeout lesson, made structural:

1. **One family = one schema = one file.** `games/state/*.schema.json` (game worlds),
   `fields/*.json` (field maps: tesuji, steer, arena), `boards/*.json` (burn, operator,
   swarm), `viz/*.json`. A family's pages all render from the SAME file. No page
   embeds its own copy of family state — if you find yourself inlining 60KB of JSON
   that another page also loads, you are building the next wipeout.
2. **Schema-versioned**: every state file starts `{"schema":"games.state@3", ...}`.
   A page that doesn't speak the version renders the honest refusal, not garbage.
3. **Single writer**: the mag organ that owns the family is the only process that
   writes the file. Pages are read-only lenses; mutations go through the organ's
   endpoint. (This is already how overseer.json and tesuji_map.json work — promote
   the pattern to law.)
4. **Duplication-is-emphasis clause**: two pages rendering the same family file
   through different lenses = emphasis (good). Two files holding the same state =
   fragmentation (the wipeout condition, banned).
5. Migration rule: when touching any page, if it carries private state, extract to
   the family file first. Touch-and-convert; no big-bang.

---

## 5. ELEGANCE RULES

1. **The tesuji map is the bar.** New/updated pages must look like it could live on
   the same wall: dark warm lab, monospace ink, restrained glow.
2. **The palette is tokens, not taste**: `--bg:#070d0c --ink:#c8e6e0 --cyan:#7cf5ff
   --amber:#e8c96a --dim:#6f8a82 --shadow:#ff6b6b` — shared `lab.css` so the fleet
   stops hand-picking greens.
3. **No page without a purpose line or a falsifier.** The header sub either states
   the question the page answers (home.html's `.q`) or the falsifier it tests
   (tesuji's tip line). A page that can state neither goes to lab/attic.
4. **Empty is data.** Empty corridors, empty feeds, zero-stone fields render an
   honest empty state — never a blank div, never fake filler.
5. **Error-banner fixture on every page** (already fleet standard: tesuji, home,
   games) — silent breakage is the enemy the banner exists to kill.
6. **Evidence links, not badges**: every number links to the page or file that
   proves it (home.html pattern).

---

## 6. BUILD ORDER (what to rebuild first)

1. **The spine** — `PAGE` manifest contract + `page_badge.js` + `lab.css` tokens +
   nav.js rewritten as the nested INDEX manifest. Small, unblocks everything.
2. **The hub** — index.html renders the six wings from the manifest with status
   chips; home.html's live cards fold in. First thing the operator sees daily.
3. **Exemplars first** — VIZ LAB (viz_gallery moves into viz/, gains the missing
   tabs) and GAMES & FALSIFIERS (tesuji + falsifiers.html anchor the wing). The two
   pages that already work become the templates others copy.
4. **The sync conversion** — games family and fields family to schema'd family
   files; kill the private copies (wipeout prevention, where the real risk lives).
5. **The honest sweep** — attic + *.bak-* + dead feeds into lab/ stamped STALE
   (never deleted — wrong turns are records); burn_board gets the badge strip and
   moves to live/ with an honest STALE-or-WORKS call.
6. **Decks last** — lowest churn, mostly moves + the badge strip.

Bounds: no page loses its data in the move; moves are path + manifest edits;
anything uncertain goes to lab/ with STALE, and the hub tells the truth about it.

---

## 7. FALSIFIERS (how we know the rebuild worked)

- F1: zero duplicate canonical paths in the nav INDEX (today: ≥5). Countable.
- F2: every page serves the badge strip; the hub's BROKEN chip count matches
  reality within one hub refresh (pages cannot lie about feeds).
- F3: no page outside lab/ embeds a private copy of family state (grep-able:
  family filenames appear as src/fetch, not inline blobs).
- F4: the operator can reach any wing in one click from the hub, and any page
  states its status without being asked.
- F5: nothing deleted. The wrong turns are all still there, just properly shelved.
