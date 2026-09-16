# RS_WORLDBUILD_SALON — receipt (appended as I go)

- **Lane:** wave_20260916 / RS (ractor salon)
- **Date:** 2026-09-16
- **Operator:** "send it through the ractors first, tease it out for nuance"
- **Worker:** this session (salon convener). No git. Budget: $0 — free lanes + free-window stealth if alive; probe first, degrade gracefully.
- **Subject:** `watch/inbox/WOW_CLONE_BETA_BLUEPRINT_20260916.md` (the world-build blueprint), plus W1 evidence (`watch/inbox/wave_20260916/receipts/W1_WORLD_SKELETON.md`, M0 shipped).

## Mission

Ractor salon, four witnesses, each a distinct program on a distinct live lane (doubling allowed at different temperature only if lanes are thin). Each witness: attack or extend in ≤150 words, name ONE nuance the others will miss, answer "what would you build differently". Then FOLD (Rashomon law — no averaging): divergence map, nuance list (one line each, which milestone M0–M5 it amends), verdict, amendment list ready to fold into the blueprint file.

- W1 — THE SOULS PURIST: does the combat grammar survive being the WHOLE game?
- W2 — THE MUD VETERAN: does "room as legality table" scale to a WORLD, and what's the missing abstraction?
- W3 — PLAYER ONE'S ADVOCATE (Adam's seat): first thirty seconds through Discord text — what's seen/done, first delight or confusion?
- W4 — THE REFEREE LAWYER: where do the bones laws strain when "session" becomes persistent world? What strains next?

## Steps (live log)

- [x] Receipt opened FIRST (this file).
- [x] Read blueprint + W1 receipt.
- [x] Probe free lanes (7 probed: 6 alive; mistral false-DEAD was our seed-param bug, fixed).
- [x] Witness 1 dispatched + post received (groq-oss20).
- [x] Witness 2 dispatched + post received (cerebras-qwen after retry; groq-oss-120b double on file).
- [x] Witness 3 dispatched + post received (mistral-min8 after retry; groq-oss20 double truncated, filed as row).
- [x] Witness 4 dispatched + post received (or-union-alpha, one 429 cooldown retry).
- [x] FOLD written (divergence map, nuance list, verdict, amendments).

Artifacts: driver `../rs_salon_witness_driver.py` · diversity retries `../rs3_mistral_retry.py`
· charters `../rs_witness_charters.json` · tape `memory/runs/rs_worldbuild_salon/raw.jsonl`
· posts `../rs_witness_posts/` (6 files). Blind divergence held: shared byte-stable BRIEF,
role in the tail, separate calls, no cross-visibility between seats.

## Lane probe results

- **ALIVE (6):** groq-oss20 (0.6s) · cerebras-qwen (0.3s) · groq-oss (0.4s) · or-ling3 (1.2s) ·
  or-union-alpha (9.1s — **free window still open**) · or-nemotron (9.3s).
- **False DEAD (1):** mistral-min8 probed `HTTP 422` — our bug, not the lane: Mistral takes
  `random_seed`, not `seed`. Fixed in the driver; the retry call landed clean (1089 chars).
  Probe verdicts are rows too — this one was wrong and got corrected by evidence.
- **cerebras first witness attempts returned `empty_content`** (reasoning channel burned the
  2000 max_tokens budget — the exact trap D22 recorded). Retry at max_tokens 4000 succeeded.
- z.ai lanes never called (paid wall, standing order). groq-qwen avoided (OTPM gate).
- 14 metered calls total (7 probes + 4 witnesses + 2 diversity retries + 1 cooldown retry),
  all free-tier, **$0.00** (union-alpha usage self-reports cost 0).

Final seat → lane map (distinct program per seat; doubles only by sanctioned rotation):

| seat | lane (voice) | temp | note |
|---|---|---|---|
| RS1 souls purist | groq-oss20 (gpt-oss-20b) | 0.35 | primary, first try |
| RS2 mud veteran | cerebras-qwen (qwen-3.8-27b) | 0.55 | diversity retry after empty_content |
| RS3 player one | mistral-min8 (ministral-8b) | 0.80 | diversity retry after probe bug |
| RS4 referee lawyer | or-union-alpha (stealth) | 0.25 | primary; one 429, cooldown retry held |

Rotation doubles kept on disk/tape as supplementary testimony (Rashomon: filed, never averaged):
`RS2_mud_veteran.md` (groq-oss-120b @0.55 — converged with cerebras from a different angle) ·
`RS3_player_one.md` (groq-oss20 @0.8 — TRUNCATED mid-sentence, finish=length, reasoning ate
the budget; filed as a row, no nuance parsed from it).

## Witness posts (verbatim, filed in `../rs_witness_posts/`)

### RS1 — THE SOULS PURIST (groq-oss20)

> POST: Add a second verb: "defend" or "counter" to combat. The current system is a simple dodge game that will become stale after 10 minutes. By introducing a defensive verb, players can choose to block or counter telegraphed attacks, creating a risk‑reward dynamic. Additionally, boss phases with changing telegraph patterns will keep the game interesting.
>
> NUANCE: The 0.35s telegraph window is too short for human reaction, so latency must be accounted for, amends M3.
>
> DIFFERENT: I would design combat as a two‑verb system: "attack" with telegraph and "defend" with block or counter, adding phase‑based boss mechanics and environmental hazards to sustain interest beyond ten minutes.

### RS2 — THE MUD VETERAN (cerebras-qwen)

> POST: Room-as-table survives 50 rooms only if the table is adjacency, not behavior. If each room carries rows for open, unlock, key, portal, you are back to an opcode swamp. The missing abstraction is the door: a first-class, stateful legality object with a typed condition, effect, and target. Rooms list exits; the gate resolves VERB against the exit's predicate, not against room-specific rows. Locks are door state, not room status. Portals are exits with a target and a condition. Keys are capabilities. Refusals stay typed because the failing predicate is named. This keeps movement RNG-free and replayable: same seed, same moves, same door state. If you don't split topology from legality, M3's zone will be a patchwork of special cases and the replay receipt will hide the rot.
>
> NUANCE: The receipt must hash door and lock state, not just room id, or a key used in one process can vanish in another; amends M1
>
> DIFFERENT: I'd build a tiny exit DSL: rooms declare exits; exits have predicates and effects; the gate evaluates predicates. No per-room verb rows. This lets locks, keys, portals, and timed doors be data, keeps refusals typed, and makes replay receipts smaller because state changes are explicit.

(supplementary, groq-oss-120b: "hierarchical rule graph — zones contain rooms, rooms inherit a
base legality schema, locks/keys/portals are components attached to nodes"; its nuance: key
acquisition must be a separate ledger event to survive room reloads, amends M2.)

### RS3 — PLAYER ONE'S ADVOCATE (mistral-min8)

> POST: Adam types `/play` in Discord. The bot replies: **BONES-LEGAL WORLD** — `> [ROOM] [001] The Blackroot Depths` / `> [EXITS] North: [locked] / East: [typed refusal] / South: [002]` / `> [VERBS] [move] [examine]`. Adam types `south`. `[001] → [002]`. Bot: `> [ROOM] [002] … / > [VERBS] [move] [search]`. Adam types `search`. Bot: `> [LOOT] Found: [Rusty Dagger] (signed receipt: 42a1b3)` / `> [INVENTORY] [Rusty Dagger]`.
> **Delight:** The verb `search` yields concrete loot with a cryptic signature — proof of replayability. **Confusion:** No visuals; "typed refusal" feels like a silent block, not a rule.
>
> NUANCE: The "typed refusal" exit is a legality table edge case — it forces players to type `refuse` to acknowledge the rule, not just ignore it. Amends M0.
>
> DIFFERENT: I'd preemptively hint locked exits with `[locked: /unlock]` in the `[EXITS]` line, not force a typed refusal. Less friction for the first 30 seconds.

### RS4 — THE REFEREE LAWYER (or-union-alpha)

> POST: "First successful non-movement verb" is underspecified: does inspect wake the boss? Can success depend on an encounter not yet loaded? Define eligible verbs, scope encounters by instance ID, and commit verb acceptance plus load atomically. Two clients must not double-load. Leaving, disconnecting, and restarting must not reset encounters. DONE requires an authoritative victory predicate, not merely IN_PROGRESS.
>
> Next fractures: Signed packs prove issuance, not ownership or unspentness. Transfers and consumption need atomic, uniquely identified ledger events; copied receipts cannot duplicate items. · Death needs one durable transition covering losses, rewards, and respawn. Disconnect cannot cancel it. · Resume must reconcile player and world history at a committed sequence; independent files invite forks. · Seed plus moves is insufficient once scheduling and time matter: record authoritative ordering, timer events, and rules versions. · Turn limits belong to encounters or leases, never world lifetime.
>
> NUANCE: A 0.35-second server telegraph can expire before Discord displays it; rollability needs a declared delivery-and-input timing contract, not just timestamps (amends M3).
>
> DIFFERENT: Build a durable, sequenced world-event log before player files. Player ledgers and signed receipts become projections of committed events, not competing authorities. Use idempotent commands, transactional encounter transitions, and explicit timeout policy. Test crash-between-steps, simultaneous activation, receipt reuse, and disconnect-before-death before adding content.

(honesty note: RS4's POST + fracture list runs ~160 words — slightly over the 150 cap; kept
verbatim because the fracture list is the seat's core testimony.)

## FOLD (Rashomon law — no averaging)

### Divergence map

The four programs do not agree on where the blueprint lives or dies, and the disagreement is
the finding:

- **RS1 attacks M3's longevity** (one verb = "a simple dodge game," stale past ten minutes;
  wants defend/counter + boss phases) — a design-culture attack from the FromSoft seat.
- **RS2 attacks M1's scaling** (tables survive only as adjacency; behavior rows re-create the
  opcode swamp; the missing abstraction is the DOOR as first-class stateful object) — a
  data-model attack. Its rotation double attacked the same wound from the other side
  (hierarchical rule graph, zones + inherited schema + components): **convergent diagnosis,
  two remedies** — split topology from legality, however you encode it.
- **RS3 attacks the surface, not the bones** (the thirty seconds WORK — walk south, search,
  get a signed dagger — and the delight is the receipt signature itself; the confusion is that
  typed refusals read as silent blocks with no path forward) — a player-experience attack on
  M0's refusal law as seen from M4.
- **RS4 attacks the alone-decision directly** (underspecified load trigger, no atomicity, no
  instance scoping, no disconnect law, DONE without a victory predicate) and then re-attacks
  the persistent-world frame itself: packs prove issuance not ownership; death has no durable
  transition; resume reconciles nothing; seed+moves under-specifies once time matters; turn
  limits must not bind a world.

**Independent convergence (recorded, not averaged):** RS1 and RS4 — different vendors, different
temps, blind to each other — both found the SAME nuance: the 0.35s telegraph is a *timing
contract* problem in the Discord medium (RS1: too short for human reaction once latency is real;
RS4: may expire before Discord even displays it; rollability needs a declared delivery-and-input
contract). Two seats arriving at one wound from opposite directions is the salon's strongest
signal, and it amends M3.

**Second convergence:** RS3's "[locked: /unlock] hint" and RS4's "refusals stay typed because
the failing predicate is named" are the same law from both sides of the screen — the typed
refusal is load-bearing for the referee AND must teach the player.

### Nuance list (one line each)

1. **amends M3** — the 0.35s telegraph must be tuned against the real Discord round-trip, not
   local constants; latency is part of the combat grammar (RS1).
2. **amends M1** — session receipts must hash door/lock STATE, not just room id, or a key used
   in one process vanishes in another (RS2).
3. **amends M0** — a typed refusal must hint the legal path forward inline (`[locked: /unlock]`);
   a refusal that doesn't teach reads as a silent block (RS3; lands with M4's surface).
4. **amends M3** — rollability needs a declared delivery-and-input timing contract: a telegraph
   that expires before display is not a telegraph (RS4).
5. **amends M2** (supplementary, RS2-double) — key acquisition is its own ledger event, not a
   room-side status edit, or it does not survive room reloads.

### Verdict

**The blueprint SURVIVES — with amendments. No milestone dies.**

- M0's shipped skeleton is accepted by all four seats (RS3's walk succeeds on it; RS2 attacks
  scaling, not the gate; RS4 audits laws, not the shipment).
- M3 is the most strained milestone (two of four seats hit it), but it is strained, not dead:
  its own falsifiers (first-punish <60s, P-LEGAL sweep) already encode the test that would
  catch the purist's ten-minute failure mode. It lives **gated on evidence** — the second verb
  is drafted but ships only if Adam's playtest shows fatigue, which respects the A3 locked rule
  (fix the verb before new systems) rather than contradicting it.
- The alone-decision survives RS4's audit in direction but not in wording: it needs a written
  spec (eligible verbs, atomicity, instance scoping, disconnect semantics, victory predicate)
  before M3 builds on it. W1's flag was justified — the panel says the same.
- The deepest amendment is RS4's architecture note: the authoritative room server (M1) should
  be a sequenced world-event log with player files and receipts as projections. This reframes
  M1; it does not invalidate shipped M2 (the ledger already is an event log in miniature —
  the projection law is the natural generalization, not a demolition).

### AMENDMENTS (ready to fold into `watch/inbox/WOW_CLONE_BETA_BLUEPRINT_20260916.md`)

1. **[M0/M3 — alone-decision spec]** The encounter-load law is amended to a written contract:
   an explicit eligible-verb list may load an encounter (movement never); load is scoped by
   instance id; verb acceptance + load commit atomically; two clients cannot double-load;
   leaving, disconnecting, and restarting do not reset an IN_PROGRESS encounter; DONE requires
   an authoritative victory predicate, not merely the IN_PROGRESS state. *(RS4)*
2. **[M1 — door abstraction]** Before the world scales past the demo zone, exits become
   first-class legality objects (typed condition + effect + target): rooms list exits, the
   gate evaluates exit predicates, per-room verb rows stop growing. Locks are door state, not
   room status; keys are capabilities. *(RS2)*
3. **[M1/M2 — state in the receipt]** Session receipts hash door and lock state alongside room
   id; key acquisition is its own ledger event in the player file. *(RS2 + RS2-double)*
4. **[M3 — timing contract]** P-LEGAL gains a delivery-and-input clause: a telegraph counts
   only if it remains rollable within the observed Discord round-trip budget; the 0.35s window
   is re-tuned against measured round-trip before /play ships. *(RS1 + RS4, independent)*
5. **[M3 — second verb, evidence-gated]** A second combat verb (defend/counter) is drafted but
   does NOT ship before the playtest cadence shows ten-minute fatigue; first-punish and receipt
   evidence remain the judge. *(RS1, gated by the A3 locked rule)*
6. **[M4 — teaching refusals]** Refusal text names the legal path forward inline
   (`[locked: /unlock]`); typed refusals serve the referee and the player. *(RS3)*
7. **[M1 — architecture note]** The authoritative room server is specified as a durable,
   sequenced world-event log; player ledgers (M2) and session receipts become projections of
   committed events. Named falsifiers added: crash-between-steps, simultaneous activation,
   receipt reuse, disconnect-before-death. *(RS4)*

— RS_WORLDBUILD_SALON closed 2026-09-16 · $0.00 · 14 free-lane calls · posts + tape are the
bytes; this receipt is the map. Operator gate: fold amendments 1–7 into the blueprint or veto.
