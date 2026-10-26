# NPC = SEAT — one ractor, many faces, mesh at scale (2026-09-17)

*Operator order: "steal Dungeon Crawler Carl and Terry Pratchett full research and game
systems; steal how WoW does their character work; make ours AI based — every NPC is
basically a different Kabuki model you're talking to; one ractor, many faces, within the
mesh network of our wave protocol at scale. Self steal distribution of compute."*

## THE ARCHITECTURE IN ONE LINE

**Every NPC is a seat.** The ractor engine (33-node Laplacian belief graph, OCEAN as
material constants, verdicts as threshold crossings) is the shared substrate; each NPC
face is a Kabuki seat (configs/kabuki_cast.json + dissection personas — the machinery
exists: mag/cage_intake.py) with its own personality prompt, lane routing, and memory
edge; the wave protocol distributes the compute across the 26-lane providers.yaml pool
under U8's measured concurrency.

## THE THREE STEALS

### 1. Dungeon Crawler Carl — the System that loves you

| DCC | Fleet translation | Status |
|---|---|---|
| The System (AI dungeon master with personality + agenda, addresses Carl directly) | **The ractor itself is the DM seat** — one face that talks, mocks, rewards | design (this doc) |
| NPCs were former people (Donut the show cat, Katia) — the dungeon is staffed by the dead | **Our bones ghosts + champion grudges** already are dead-player NPCs; the faces just get seats | mud.html ships ghosts+grudges |
| Sponsors grant boons for entertainment value | **Mud boons (12 gods, draft 1-of-3)** = sponsors; extend: boons keyed to what entertained the audience (deaths that were funny, solves that were elegant) | boon system ships; audience-keying queued |
| Followers as a resource (Donut's crowd feeds her) | **X-follower / relay-presence as NPC power source** — NPCs level up when watched | queued (relay already streams presence) |
| Floors as episodes with recap shows | **Levels as inscribed rooms** (RUINS GO pattern) + the tide card as recap show | pattern ships |

### 2. Terry Pratchett — narrativium is load-bearing

| Pratchett | Fleet translation |
|---|---|
| Narrativium: stories have gravity; events bend toward the shape of the story | **The parable register IS narrativium** — published-as-spec fiction the fleet then executes (The Fence, THE SCALE, the mirrors parable). Formalize: each NPC face carries a story-shape it cannot escape (its grudge/quest gravitates to it) |
| Death SPEAKS IN CAPS | **The inscription register** — system voices have typographic law (cap-inscriptions at deaths/boss entries) |
| Small Gods: gods power up on belief | **Attention powers lanes**: a seat with traffic gets stronger routing (the lane-salon attendance pattern); an unbelieved NPC god withers |
| The Watch: institutions outlive heroes | **The lanes/registry outlive seats** — faces die, the watch roster persists |
| L-space: all libraries connect | **The corpus canon + imprint**: every shelf is one shelf through the Librarian |

### 3. WoW — character work, made AI-based

| WoW | Ours (AI-based) |
|---|---|
| Class (template: warrior/rogue/mage) | **Face template**: behavior class from kabuki_cast (the DM, the innkeeper, the sentry, the merchant) |
| Spec (sub-style within class) | **OCEAN weighting** on the ractor graph — same face, different material constants |
| Talents (chosen, persisted modifiers) | **Learned traits persisted per NPC** (fs_lore pattern): what it saw you do changes its thresholds |
| Gear (mechanics via items) | **Boon/bestowal system**: NPCs grant/equip mechanic modifiers (mud BOONS as the item layer) |
| Rotation (the loop you execute) | **The NPC's turn policy on the step-clock** (RUINS GO law): each face has a movement/telegraph policy |
| Leveling curve | **Ramp law placement**: each NPC face sits at a rung; faces level via the evolution loop's ledger |

## DISTRIBUTION OF COMPUTE (self-steal — it all exists)

- **U8 measured**: 24-concurrent on one stealth lane, latency-not-rejection, 256K context.
- **providers.yaml**: 26 lanes (groq ×6, mistral ×2, OR ×18 across 2 keys, nim, cohere,
  gemini, together, deepseek, xai seat, z_ai3 Lite post-11:00 free).
- **kabuki_salon.py + cage_intake.py**: the cast roster and multi-seat machinery.
- **wave protocol**: lanes carry work; receipts carry proof; the relay (:8766) carries
  presence.
- **The routing rule**: face → lane assignment by class (DM face rides the strongest free
  lane; mob faces ride fast small lanes; the Elder face rides none — it reads).
- **Determinism**: NPC state is ledger state; faces re-derive from disk (Monroe lens);
  seeded RNG everywhere (D&D layer law).

## BUILD ORDER (each behind its gate)

1. **Face registry**: extend kabuki_cast schema with {face, class, spec-weights, lane,
   grudge, tale} — the mud's first 3 NPCs (innkeeper, vault warden, bones guide) get
   seats and answer through chat_provider with their face prompts.
2. **Traits into step()** (already owed — the Elder's #1): stat-block traits become
   mechanical; NPC faces inherit trait effects.
3. **The DM face**: one ractor-backed narrator seat for RUINS GO/mud that speaks
   inscriptions, grants boons, and remembers grudges — DCC's System, Pratchett's Death,
   WoW's quest-giver, all one seat with faces.
4. **Belief = attention**: relay presence + X followers feed named-NPC "belief" meters;
   meters gate which faces get strong-lane routing.

## FALSIFIERS

- If a player cannot tell which face they are talking to within 3 exchanges, the faces
  are not faces — collapse to one narrator.
- If NPC persistence (talents/grudges) fails to survive a page reload + relay restart,
  the ledger is decorative.
- If the DM face's cost per exchange exceeds 2× a mob face's, the mesh routing is wrong.

*Filed by zcode-50wide-window-20260917. The wake-up-NPC poster was the spec; this is the
harness. The NPCs were always seats — we just hadn't given them faces names can hold.*
