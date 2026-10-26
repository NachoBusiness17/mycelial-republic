# DEEP SELF-STEAL — THE COLONY SIMS (2026-09-04)
Genome: docs/ref/verb_genomes/research_socratic.md (six steps) on L0 v1. Seat: zcode.

## ITEM
Operator, verbatim: "self steal dwarf fortress stardew valley rimworld and all our gaming
corpus and run a salon." Mid-steal addendum (folded centrally, 2026-09-04): "we also have
DFHack, which is the whole thesis behind steering" — DFHack ingested as prior art for the
steering thesis, carried into the salon question.
Why now: the fleet just measured a 50-concurrent lane (LEGIONS_EXPEDITION_MAP_20260904 —
burst 50/50, sustained 27.85 rps, 99.89%) and the colony-sim genre is the design manual
for a 50-agent fleet. The governor currently has ONE goal function: damp incidents. The
genre says a director's job is a good STORY, not a safe system.

## 1-2. INGEST + MAP — our gaming corpus (receipts)
- GAME_MECHANICS_LATTICE_20260903: 7 engine families (Murray 1952, canon-attested);
  room = invariant × engine × pack; the L0-L4 layering of the canon and the fleet are the
  same layering.
- GAME_CODEX_20260903: dragons = falsified assumptions (the socratic gate is the combat
  system); adventurers = the engine bay; the Dark Souls law (each respawn weaker, player
  sharper) — failure-as-difficulty-curve ALREADY in our ontology.
- GAME_THEORY_PLAY_MAP.md: **PRIOR ART** — Tier A steal table already carries
  "CK3/DF/Rim tables | traits, storyteller budget | rest events, threat_budget". Filed
  as a re-find: this steal promotes that table row to a build (repetition is emphasis).
- SELF_STEAL_TRAJECTORY_20260901: the operator ALREADY ordered this class of steal —
  "i want to steal from stuff like dwarf fortress and ck3" (save-state theft). This card
  executes that order on the genre leg.
- SELF_STEAL_LIGHT_CODEC_GAMES_20260903: "CK3/DF storyteller budget = the economist's
  envelope: scarcity as narrative engine." Second prior-art hit — two lanes, one organ.
- LEGIONS_EXPEDITION_MAP_20260904: the 50-flight gates (Leg 1 organs: claim + lockfile
  pids + requeue grace; tranche ramp; queue restock named the bottleneck). The gates
  bind this steal's build order.
- watch/percolator_out.md + SWARM_RESEARCH_LEDGER_20260831: the folk version already
  exists — "the economist is a Dwarf deep beneath the mountain... the dwarf knows the
  fortress will fall. the dwarf keeps counting." And "the RimWorld colonists are landing."
- Memory index: the theory-of-operation knot — "DFHack-style memory riding: context =
  model's memory space, prefix = the mod, capability injection w/o training permission —
  **'every locked model is a Dwarf Fortress you can mod'**." THE ADDENDUM CONFIRMS CANON:
  DFHack was already named the steering thesis at knot level on 08-27. The board-runaway
  row (09-03: duplicate churn + state-clobber + instant-fail loop = 2.24GB append) is the
  unpaced incident this steal's director exists to prevent-or-pace.
- Museum translation (MUSEUM_GAME_TRANSLATION_20260902): verkle/ledgers = THE SAVE FILE;
  governor = sole committer. The cast table already speaks game.

## GENRE INGEST — external receipts (the wall held everywhere; wikis fetched raw)
**Dwarf Fortress**
- Manager (dwarffortresswiki.org/index.php/Manager): the player declares job + quantity
  ONCE from one screen; the system resolves WHICH eligible workshop runs it ("will
  distribute the jobs amongst all those workshops"); individual dwarves self-assign via
  labor preferences — no central brain dispatches dwarves. CRITICAL DETAIL: at 20+
  citizens, work orders sit idle until the Manager VALIDATES them; validation is a
  skilled labor (organizer skill, leveled BY validating) that needs a home (a meager
  office) and free time.
- Losing is fun (dwarffortresswiki.org/index.php/Losing_is_fun): no victory condition;
  "almost every fortress eventually falls"; the only forts that never fall are "very
  conservative and very boring"; the Unending Cycle — build, lose, remember, repeat —
  IS the game; every death is a saga ("carving out your own legends over the eons").
- Tarn Adams (en.wikipedia.org/wiki/Tarn_Adams): simulation-first — "Hit points are
  depressing to me... like a game designer stopped doing their job"; "question all of
  the mechanics in the game from the bottom up"; stories emerge from simulating a world,
  never from scripting a plot.
- DFHack (dwarffortresswiki.org/index.php/DFHack + docs.dfhack.org workflow page):
  400+ tools; "a comprehensive, standardized memory access package"; three graft types —
  plugins (compiled C++), binpatches ("raw memory edits"), Lua scripts; "an unofficial
  extension of the game itself" steered against a CLOSED source for 15+ years; protobuf
  RPC listening on 127.0.0.1:5000 with NO change-driven notifications — remote clients
  poll each frame. `autolabor`: "Automatically assign labors to dwarves to efficiently
  complete pending jobs." `workflow`: watch repeat jobs, re-add + suspend them when they
  die of missing inputs, and hold STOCK BANDS — `workflow amount AMMO:ITEM_AMMO_BOLTS/
  METAL 1000 100` keeps bolts within 900–1000: suspend at the target, resume below the
  gap (hysteresis by construction).

**RimWorld**
- AI Storyteller (rimworldwiki.com/wiki/Storyteller): "the main mechanism used to
  determine game difficulty and play style"; it decides event frequency and type from
  colony wealth, building wealth, colonist count, recent deaths/injuries, and time since
  the last major event; an adaptation system "makes the game more challenging when
  you're doing well" (threat score grows in good times, drops when you take damage).
  Cassandra Classic: "push you with dangerous events, then give breathing room, then
  come back." Phoebe Chillax: "basically makes sure nothing bad happens" (Ludeon blog,
  where she was Phoebe Friendly). Randy Random: "doesn't care if they make a story of
  triumph or utter hopelessness." HUMILITY RECEIPT: the storyteller is "purely a settings
  label — just a name given to describe game settings — with no in-game body." The
  director ships as POLICY, not as an agent. It NEVER prevents — blocking threats is a
  separate difficulty setting; the storyteller only paces and scales.
- Design voice (ludeon.com/blog/2013/09, Tynan Sylvester's own post): "Cassandra
  Consistent tries to keep you on a pre-defined tension curve." Apophenia (Sylvester,
  via search-indexed RPS/Game Developer coverage — full essay text timed out, flagged in
  tri-state): "players extract more story meaning from a game event than is actually
  present" — the game doesn't need to script narrative; pacing + player apophenia is
  enough.

**Stardew Valley**
- Time (stardewvalleywiki.com/wiki/Time): the day is 6am–2am, 20 hours, ~14 real minutes;
  going to bed by midnight = full energy; the overnight profit breakdown is "the only
  point when the game saves"; the 2am pass-out costs 10% of gold (capped) — the fee
  arrives as tomorrow's mail. The finite day is the decision-maker: shops open at 9,
  villagers walk schedules, some fish only exist after 6pm. The loop satisfies because
  the day ENDS, the end PAYS (a guaranteed summary artifact), and staying up has a
  priced-in fee.

## 3. ASSERT (steel-man, one sentence)
A colony sim keeps dozens of agents compelling for hundreds of hours by splitting three
jobs the fleet currently merges or lacks — WHO assigns work (manager queue + labor
preferences, no central brain), WHO paces trouble (a storyteller with a tension budget
that scales with your wealth instead of preventing events), and WHAT failure MEANS
(content: the engraved history, the epitaph, the next embark) — and we own the first and
third organs while running our governor on damping alone.

## 4. ATTACK (strongest counter-case, two named causes minimum)
1. **The director has no audience-agency to pace FOR.** RimWorld's storyteller works
   because events land on a player with mid-crisis agency; our incidents land on seats
   that cannot improvise (a 429 storm just kills lanes). Pacing for an audience that
   isn't there risks manufacturing incidents that are pure theater — and the LEGIONS map
   already drew the line ("the swarm scales the walking, never the knowing"). Evidence:
   the sw_scale dogfood receipts live in the inbox, not in story form. This is real; the
   answer (below) is that our apophenia-reader is the OPERATOR + the salons, which exist
   and consume exactly these stories.
2. **The failure ledger already produces stories without a director.** Every incident in
   memory became a law row (runaway → lockfile organs; clobber → declarative law; docker
   death → watchdog). Counter-counter: the retelling is manual and post-hoc; DF engraves
   AT the moment of the deed, and our reading organ (tale-re-encoder) is still owed —
   the director's true job is curation timing (when to let an incident run in a cheap
   window), not creation.
3. **Credit-attribution risk (survivorship bias, per SEAT_AUDIT_SOCRATIC).** A director
   that schedules incidents will claim the lessons the system would have learned anyway.
   Any storyteller falsifier needs a null arm (no-director window) or it lies to us.

## 5. MEASURE — the $0 falsifier, RUN on our own ledger
Paced vs unpaced incident outcomes, tallied from the memory index rows (n is small;
read as tendency, not law):
- PACED (declared window, pre-registered): MAX_DISTILL epoch 1 (04:00 window) → honest
  INCONCLUSIVE + three infra laws (5.3 thinking=low; ≥1536 max_tokens; saturation map);
  eyes receipt → verified end-to-end, an invariant class; hermes dossier overnight batch
  → the Sherpa's 5-class failure route table.
- UNPACED (arrived as incidents): board runaway 09-03 (2.24GB / 9.1M rows) → cost first,
  organs after; openclaw recreate clobber (~49M tok billed) → law converted post-burn;
  Docker silent double death → watchdog built after the fact.
Tally: paced windows produced LAWS as the primary output; unpaced incidents produced
COST as the primary output and law only post-hoc. 3v3, small-n: **Supported as a
tendency** — which is exactly the strength RimWorld claims for pacing (not prevention,
pacing).

## 6. CORRECT — THE COMPOSE-MAP (organ taught → mechanism missing)

| Source | Organ it teaches (we HAVE it) | The ONE mechanism MISSING |
|---|---|---|
| DF Manager | the claim organ (queue/claim; Legions gate 1) | the **validation pass as a first-class labor**: orders idle until a skilled, homed, leveling organ validates them — at 50-flight our named bottleneck is queue restock, and DF's answer is a dedicated intake-health organ, not more workers |
| DF engraving/history | the verkle chain (the room that remembers) | the **EPITAPH row**: a fall written once INTO world history as content (reclaimable, readable), not as a fix note — pairs with the owed tale-re-encoder (two-lane convergence: the Primer's named missing organ) |
| RimWorld storyteller | the bay governor (damping) + night windows + failure ledger | a **tension budget**: declared cadence that spends controlled incidents (429 drills, failover flips, lane starvation) in CHEAP windows, scales with fleet wealth (adaptation law), breathes after damage — and never prevents |
| RimWorld pawn traits / DF souls | seat contracts + verb genomes | trait-conditional routing: claim assignment that reads a seat's MEASURED traits (scorecards, dossier failure classes) the way autolabor reads aptitude — second-order build |
| Stardew daily loop | night window + sun-up stop (23:00–09:00 SGT) | the **overnight profit breakdown as the only save point**: every window closes with a guaranteed day sheet (earned / lost / one story) — and the pass-out fee as LAW (running past sun-up always costs; the 09-03 runaway was a 2am pass-out with no fee) |
| DFHack (steering thesis) | covenant.json floors, .env key armory, steer bus, event.v1 receipts | **workflow-for-credits**: a stock-band controller on token/credit/queue-depth stocks (suspend at target, resume below gap — hysteresis), our covenant as constraints; autolabor = claim assignment by aptitude; RPC lesson: poll the frame, don't wait for push |

THE STEERING THESIS, folded: DFHack is the existence proof that you can steer a
simulation you don't own through read/write lenses — 15 years of gates on a closed game.
That is exactly our posture toward GLM: we don't hold the weights; we hold the harness,
the steer bus, the receipts, the prefix. The operator canonized this on 08-27
("every locked model is a Dwarf Fortress you can mod"); this steal adds the genre's
plugin taxonomy: our autolabor = the claim organ, our workflow = the covenant bands,
our RPC = the polling governor loop. The addendum's answer to "what is the DFHack of a
50-agent swarm" is: THE HARNESS WE ALREADY RUN, missing its band-controller plugins.

## THE CROP
**The build: STORYTELLER MODE for the governor** (operator's candidate — CONFIRMED, as
a re-find promoted to build: play-map threat_budget row + light-codec storyteller
budget row both filed it first; repetition is emphasis). Three amendments:
1. **Ship it as RimWorld does: policy, not agent.** The receipted humility row — the
   storyteller is "a settings label with no in-game body" — means v0 is a table
   (drill frequency, severity, min gap, wealth scaling, breathe-after-damage) inside
   the existing governor, not a new model seat.
2. **Gated by Leg 1.** The director is FORBIDDEN until claim + lockfile pids + requeue
   grace pass the race harness (the LEGIONS gates). A storyteller that fires incidents
   into an instant-fail loop is not Cassandra, it's the 09-03 runaway with a budget.
   **KILL CONDITION (cold-executable):** race harness fails ⇒ no director, ever, until
   it passes. **Second kill:** three consecutive paced windows whose receipts fold zero
   new invariants ⇒ tension budget drops to zero (Phoebe mode) and the mechanism is
   demoted.
3. **The first incident menu comes from the failure ledger** (hermes dossier's 5
   failure classes + the token-render 429 taxonomy), every fired incident labeled a
   drill in event.v1 — manufactured incidents never masquerade as organic, or the
   failure ledger's honesty (its entire value) dies. Its plugin-sibling ships first
   because the director needs it: **workflow-for-credits**, the DFHack band controller
   holding covenant floors ($39 stand-down IS a workflow constraint) and queue-depth
   gaps (never let explore-228 hit zero while mines are staffed).

**THE SALON QUESTION (verbatim, as fired):**
"Our fleet runs 50 concurrent worker agents and treats every failure as an incident to
damp, while Dwarf Fortress runs 50 dwarves off a manager queue under the banner 'losing
is fun', RimWorld's AI Storyteller paces disasters for story value instead of preventing
them, and DFHack steered that closed game for 15 years by reading live memory and
writing gates on a game nobody owns the source to — so what is the ONE mechanism we
steal first to make 50-agent failures produce good stories instead of incidents, and
what is that mechanism's own failure mode?"

**Salon brief:** watch/salon_inbox/colony_salon.json (VALID json; keys name/question/url;
digest anchored on the receipted rimworldwiki Storyteller page; drain owned by the main
thread — this seat did not fire it).

## TRI-STATE
- Genre mechanics (DF manager + validation labor; storyteller paces-not-prevents, wealth
  adaptation, no in-game body; Stardew 6am–2am + sole-save breakdown + pass-out fee;
  DFHack 400+ tools / memory access / autolabor / workflow bands / loopback poll-RPC;
  Tarn Adams simulation-first): **Supported** — wiki + docs + Ludeon blog receipts, paths
  above.
- "Paced incidents produce laws cheaper than unpaced ones": **Supported as tendency**
  (3v3 memory-index tally, small-n — falsifiable at the next tranche).
- Storyteller mode as the next build: **Unproven until run** — kill conditions
  pre-registered above; the falsifier disposes, not the compose-map.
- DFHack onTrigger Lua events ≈ event.v1: **Unproven** (family receipted; the specific
  plugin doc page was not reached).
- Pawn-traits → trait-conditional routing: **Unproven** (plausible, unmeasured).
- Apophenia quote attribution: **Supported via search index, bytes Unproven** (essay
  fetch timed out — flagged, not smuggled).

**Two counters:** FORBIDS — the director firing any incident into a window without a
pre-registered receipt kind, or past sun-up without the day sheet (a story that skips
the save point is the runaway again). PAID RENT — three games + a modding framework
compressed into one build order, one falsifier, and one salon; the DFHack leg turned the
operator's steering thesis from doctrine into a plugin taxonomy with a $0 first plugin.

**Receipts:** watch/SELF_STEAL_COLONY_SIMS_20260904.md (this card) ·
watch/salon_inbox/colony_salon.json (brief, undrained). Room row appended below.
Sources fetched 2026-09-04: dwarffortresswiki.org (Manager, Losing_is_fun, DFHack) ·
docs.dfhack.org (workflow tool page) · rimworldwiki.com (AI_Storyteller via /wiki/
Storyteller) · ludeon.com/blog/2013/09/title-screen-update · stardewvalleywiki.com
(Time) · en.wikipedia.org (Tarn Adams, Tynan Sylvester) · search-index receipts for RPS/
Game Developer apophenia coverage and The Simulation Dream (bytes timed out).

## THE CROP (what this pass did not see)
(1) DFHack's plugin SOURCE bytes — tool docs only; onTrigger and script-market pages
unreached, so the event-hook mapping stays Unproven. (2) The Simulation Dream full text
(timed out) — Sylvester's own sentences on apophenia ride a search-index summary.
(3) Exact RimWorld min/max event-spacing formulas (the wiki declined them) — the director
v0 must MEASURE its own cadence, not steal one. (4) The pending
swarm_scale_dogfood_20260903.json sitting in the same inbox — the next chair should read
whether its dogfood plan conflicts with the director's tranche gates before the drain
fires both. Next lens: the Leg 1 organ builder sits next — the director is gated on
their race harness, and the validation-labor finding is theirs to size.
