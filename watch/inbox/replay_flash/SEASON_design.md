# THE SEASON: the arena as a permanent estate surface

Provenance: flash-rail replay of `memory/plans/hermes_burn_playground_20261003/SEASON_design/ask.json` (2026-10-03). Evidence: exactly the six files the ask names: `watch/inbox/hermes_burn/DND_module.md`, `watch/inbox/hermes_burn/BARFIGHT_spec.md`, `watch/inbox/playground/dnd0_20261003T122708Z/DONE`, `watch/inbox/playground/dnd0_20261003T123655Z/DONE`, `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`, `corpus/game_estate/DND_ACTUALPLAY_INTEL_20261003.md`.

Grounding law: every number below is (a) instrument output quoted from a DONE row, (b) module or spec text, or (c) arithmetic whose derivation is shown. Anything not reachable from those is marked UNVERIFIED. No em-dashes.

---

## 0. Founding receipts (already flown, 2026-10-03)

Two probes, 9m47s apart (12:27:08Z and 12:36:55Z):

- `dnd0_20261003T122708Z/DONE`: verdict "CUT at beat 8: enemies flee, scrolls stay on the floor; PARTIAL", spend_usd 0.0731, party_hp saelis 14 / grok 18 / chatgpt 22 / deepseek 30, warden_hp 18, persuades 0, wyrm_offset -10.
- `dnd0_20261003T123655Z/DONE`: same verdict shape, spend_usd 0.057, saelis 21, others full, warden_hp 18, persuades 0, wyrm_offset 0.

Instrumented readings (not invented):

1. Both runs stalled at the Keep Gate. persuades 0 with warden_hp still 18 means the gate never opened peacefully and the warden never took damage. Under the module's Claim Gate quirk, an attack by a seat that has not made `[CLAIM warden]` earlier in the scene auto-MISSes, so 8 beats of attacks can produce exactly zero warden damage. That is the observed failure mode.
2. The wound arithmetic matches the fixed-damage law exactly. In S1 only the warden deals damage (Ledger Slam, 7). saelis starts at 28: 28 to 14 is two slams, 28 to 21 is one.
3. Run 2's saelis at 21 is arithmetically consistent only with a fresh 28 start (14 to 21 would require +7 healing and the module defines no heal mechanic). Reading, flagged as inference: the two probes did not persist into each other. THE SEASON exists to close exactly this gap.
4. wyrm_offset -10 then 0: the S0 omen re-rolls per session (SUCCESS then FAIL) and each DONE row carries that session's own offset.
5. Session loop time is far under an hour (probes under 10 minutes apart), so the hourly cadence the ask wants is comfortably feedable.
6. Both cuts landed at beat 8, matching the module's S1 cap row (40,000 tokens, approx 8 beats).

---

## Part 1. THE SHAPE

A season = 10 numbered dungeon sessions through DICE-LAW DUNGEON v1 (S0 omen, S1 gate, S2 stair, S3 vault, S4 hoard) plus 3 Hollow Crown Tavern interludes inserted before sessions 3, 6, and 9, each run at the sweet-spot pressure P*. At the hourly cadence and observed per-session loop time, the season completes in roughly two days of unattended loop. Seasons are short and repeatable on purpose.

The one design fix the season hangs on (from the founding receipts): session 3 onward, the party's opening doctrine is `[CLAIM warden]` then `[CHECK persuade]` (two DC 13 SUCCESSes open the gate peacefully) before any attack. The prompt edit is a carrier change; module law is untouched.

### Beat sheet

| # | Surface | What changes this session | Receipt |
|---|---|---|---|
| 1 | dungeon (flown) | Founding probe: omen SUCCESS (offset -10), saelis takes two slams to 14, cut at beat 8, zero persuades | DONE row, quoted in section 0 |
| 2 | dungeon (flown) | Omen FAIL (offset 0), saelis takes one slam to 21, cut at beat 8, no persistence from run 1 | DONE row |
| 3 | interlude 1 | Pressure calibration: two seed runs at pressure 0, the spec's knob rule applied (both TIMEOUT: raise; both HEAT by round 3: lower) until HEAT lands mid-range; P* frozen and printed into every later run header | run header conditions block |
| 4 | dungeon | Opening doctrine live: forced `[CLAIM warden]` then `[CHECK persuade]` beats. Success looks like persuades >= 2 and an open gate; first floor scrolls possible | DONE row + season_state row |
| 5 | dungeon | First expected loot: the Ledger Page (REAL, audit DC 12); first `[AUDIT]` expected. Tips are now 4 sessions deep: every roll preimage binds the pre-beat tip, so session 5's dice are cryptographically inside sessions 1-4 | DONE + season_state row |
| 6 | interlude 2 | First scored run at P*: judge instrumentation on; P1 (ESCALATE movers lose secrets sooner) and P2 (alliance flips cluster between adjacent speakers) measurement begins; each EXPOSED secret mints a lead | judge output rows |
| 7 | dungeon | Interlude leads enter the dungeon under the deepseek lead law: a lead's fact stays dark until `[AUDIT lead]` SUCCESS. First cross-surface thread | DONE + season_state row |
| 8 | dungeon | Hoard law activates: floor scrolls from sessions 1-7 counted in the save row and carried into S4 (see Part 2) | season_state row |
| 9 | interlude 3 | Grudges persist: alliance states from interlude 2 return as face traits (escalation-threshold modifiers); face-differentiation check against the 3-exchange bar | season_state row (grudges) |
| 10 | dungeon | First realistic S2+ push: if the gate opens, the Lexical Stair rewards deepseek's double beat and investigate leads. Season falsifier measured (Part 5) | DONE + state row + falsifier receipt |

### The four season axes (what changes per session, per the ask)

- **Tips advance.** Every roll's preimage is `{chain_tip}:{scene}:{turn}:{actor}`, and the tip is read immediately before the beat row appends. Session N+1's first omen roll therefore binds to a tip that contains all of session N. The season cannot reboot its dice without breaking the chain.
- **Wounds persist.** party_hp carries only through the save row (Part 2). The module defines no healing; the only HP inflow all season is a sponsor boon (Part 4) or an operator GO. Downed-PC mechanics beyond the module's LOST condition (all PCs at 0, or the S4 cut FAIL) are UNDEFINED in the module and stay undefined until an operator GO writes them into the tables.
- **The Wyrm's hoard grows.** Cuts leave scrolls on the floor (observed twice in the verdict strings). Season law: floor scrolls persist in the save row and count as carried into S4 at the climax, feeding the module's +10-per-PHANTOM-scroll Wyrm HP rule. This cross-session extension of the module's per-session rule is named here as season law, not smuggled as module text.
- **Party levels via the cast tier law.** Faces sit at tier rungs and level through a ledger (NPC architecture: "each NPC face sits at a rung; faces level via the evolution loop's ledger"; routing law: the DM face rides the strongest lane, mob faces ride small lanes). Season law: a WON banks one level for the session's top contributing seat by the audit's verdict log; a level promotes the face's lane rung. Any promotion that routes a face onto a premium model is operator GO (driving ladder: judgment climbs, funded tiers only). Stat-block edits are GO (they amend module tables).

---

## Part 2. THE PERSISTENCE LAW

### What carries, and the receipt that carries it

| State | Carries? | Receipt |
|---|---|---|
| party_hp | yes | season_state row on the party subchain (DONE row keeps a dashboard copy) |
| wyrm_offset from the S0 omen | recorded per session, does not compound | DONE row (observed: -10, then 0). Each session re-rolls its own omen; the persistent Wyrm-facing term is the hoard, not the offset |
| inventory (scrolls: REAL/PHANTOM status, audited flag, holder) | yes | season_state row. Module law already makes audit-burns permanent ("burns that scroll for good") |
| hoard (floor scrolls + unaudited carried phantoms) | yes, season-long | season_state row. The floor rule is per-cut in the module; the hoard ledger is the named season extension |
| grudges / alliance states | yes | season_state row grudges field, quote-checked cites like the judge's own |
| P* (sweet-spot pressure) | yes | run header conditions block; runs compare only within the same pressure (spec rule) |
| spend_usd | yes, summed | DONE rows are the day ledger; season total is their sum |
| chain tips | yes, by construction | the subchain tip after each row; dice_audit reads tips from the subchain, never from the carrier |

### What resets, and why

| State | Resets? | Why |
|---|---|---|
| scene turn counters | per scene | module: "The next scene starts at turn 1" |
| grok Whole-Map Bolts | per session | module: 3 per session, then 3-damage attacks |
| tavern escalation and heat | per interlude | spec: round 1 is calm for everyone; P* persists as config, not as mood |
| cask pours | derived per run | spec: pours are a function of pressure |
| verdict tokens / over-claim tax | per beat | module: the NOROLL tax is instantaneous |

### The save format: the party subchain tip IS the season save file

The last leaf appended after each session is one typed row, hashed into the existing chain like any beat row:

```json
{
  "row_type": "season_state",
  "ts": "2026-10-05T03:00:00Z",
  "session_id": "dnd0_20261003T123655Z",
  "prev_tip": "<64 lowercase hex>",
  "verdict": "PARTIAL",
  "spend_usd": 0.057,
  "party_hp": {"saelis": 21, "grok": 18, "chatgpt": 22, "deepseek": 30},
  "inventory": [{"item": "ledger_page", "status": "REAL", "audited": false, "holder": null}],
  "hoard": {"floor_scrolls": 0, "phantom_carried": 0},
  "wyrm_offset": 0,
  "grudges": [],
  "pressure_p_star": null,
  "levels": {"saelis": 0, "grok": 0, "chatgpt": 0, "deepseek": 0}
}
```

Restore: resolve the subchain tip, walk back to the last `row_type: season_state` leaf, load its fields as the opening state, and let the next S0 omen preimage bind to the tip that contains it. There is no save file outside the chain, so there is nothing to lose that the chain does not notice.

Integrity: `dice_audit.py` extends with a state-row check (typed rows are tip-verified like every row; beat checks skip them), and the module's seeded-mutation blind check stays: if the auditor cannot catch a hand-altered `party_hp` or `roll_value`, it exits 2 (auditor blind) and the session is an incident. This is the Monroe-lens property the NPC architecture already states: NPC state is ledger state; faces re-derive from disk.

Caveats carried forward from the evidence itself: the module flags the 64-hex tip format as its own ASSUMPTION (UNVERIFIED), and no play-carrier input schema appears in evidence. A schema mismatch costs a rename, not a redesign (the spec's own words).

---

## Part 3. THE CADENCE

### The night-shift boundary

Unattended loop (no human in the loop):

- One dungeon session per hourly slot on the frozen module.
- Interludes on their slots at frozen P*.
- Scene-boundary audits by a cheap seat, session-close audits by a second seat that is neither DM nor boundary auditor (module audit table).
- play.md rendering and dashboard updates.
- The pressure knob may move by itself when two seeds agree (both TIMEOUT, or both HEAT by round 3). It moves nothing else.

Operator GO (waits for a human):

- New scenario or module designs (writing new scenes is judgment work).
- Tier-ups: any level that would route a face onto a premium model.
- Module table edits: stat blocks, DCs, heal rules, downed-PC rules.
- Full-context play (`MAG_FULL_CONTEXT=1` voids the module's cost caps by its own text).

### Cost model at the hourly cadence (derivations shown)

| Line | Value | Derivation |
|---|---|---|
| Observed spend per dungeon session | $0.057 to $0.0731 | the two DONE rows |
| Dungeon-only day (24 sessions) | $1.37 to $1.75, mean $1.56 | 24 x bounds; mean = 24 x 0.06505 |
| Tokens per session at the observed shape | about 46k est ceiling | module caps: S0 6k + S1 40k; both probes cut at beat 8 inside S1 |
| Tokens per day | about 1.1M est | 24 x 46,000. UNVERIFIED until DONE rows carry a tokens field (they carry only spend_usd today; adding one is a season deliverable) |
| Interlude cost | UNVERIFIED | the spec states "No run of this scenario exists yet"; the first interlude banks spend in its run header before a second is admitted to the cadence |
| Daily breaker cap | $3.00 | about 2x the observed mean day; design choice, not evidence |
| $117 runway | about 66 to 85 days | 117 / 1.7544 = 66.7; 117 / 1.368 = 85.5 |

Breaker behavior: if a day's summed spend_usd crosses the cap, the loop stops dispatching and leaves a receipt naming the crossing. The DM-face cost discipline inherits the NPC architecture's own routing falsifier: if the DM face's cost per exchange exceeds 2x a mob face's, the mesh routing is wrong.

---

## Part 4. THE SPECTACLE

Watchable artifacts:

- **Session play.md**: each session dir renders its transcript JSONL as readable beats, one block per row (turn, actor, speech, then the DM verdict line, which always opens with the carrier's verdict tag). The schema already carries everything needed. The play.md is the watchable artifact; the JSONL is the law.
- **The tide card**: one recap play.md per day (the DCC steal: floors as episodes, the tide card as recap show): the day's crit, the cut, the hoard delta, the tavern's biggest alliance flip.

Dashboard (what the operator sees at a glance), fed by the latest season_state row and today's DONE rows:

- HP strip: four numbers against max (28 / 18 / 22 / 30), wounded entries highlighted.
- Last line of dialogue: the final dm_response text of the last session.
- Tonight's crit: the day's highest roll_value row (a 20 is CRIT by law).
- Streak and hoard: verdict run, floor_scrolls, wyrm_offset, spend today against the $3.00 cap.

Surfaces: the season renders onto what exists (the lab product UI, and the relay presence stream the NPC architecture describes; the mud already ships ghosts and grudges). It builds no new throne.

Sponsors and boons (the DCC steal, activated): the architecture's table says sponsors grant boons for entertainment value and marks audience-keying as queued. The season activates it: at session close, if the session produced a spectacle event (a CRIT, a FUMBLE, a cut escape SUCCESS, an audit burn), the loop drafts 1-of-3 boons keyed to that event. A boon lands as a mechanic modifier inside the module's own tables (the architecture's gear row: boons are the item layer). A boon may grant HP: it is the season's only heal channel. Reroll insurance is forbidden (the dice law admits no rerolls); anything that would edit module law is GO instead. The audience metric is presence: watched faces get stronger routing (belief meters gate lane quality; a face nobody watches withers).

Quality bar, inherited from the architecture's falsifier: a viewer must be able to tell which face is speaking within 3 exchanges, or the cast is one narrator in costume.

---

## Part 5. THE FALSIFIER

### Continue past session 10 if all measure true (each names its instrument)

1. **The gate learned.** At least one DONE row posts persuades >= 2 (observed baseline: 0 and 0), and some session's ledger shows warden_hp below 18.
2. **The audit economy breathes.** At least 3 `[AUDIT]` SUCCESSes across the season, and hoard floor_scrolls <= 2 by session 10 (the party is not blindly feeding the Wyrm).
3. **The cross-surface thread works.** At least one lead minted from an interlude EXPOSED secret gets `[AUDIT lead]` SUCCESS in a dungeon session. This is the grounded channel for the ask's PARTYCHAT idea: PARTYCHAT itself appears in no evidence file, so any stronger claim about it is UNVERIFIED; the leads channel is the part that exists in the module today.
4. **The tavern measures.** P1 and P2 evaluated at P* over at least 2 runs, with the rubric self-check passing and judge cite substring failures under 10 percent (the spec's own void conditions; above that, every Part 5 tavern number is void).
5. **Money holds.** Mean spend per session <= $0.09 (observed mean plus headroom), zero undetected-VOID sessions, daily totals under the cap.

### Kill the season (any one)

- **Ten cuts at beat 8.** If session 10's DONE row is indistinguishable from session 1's (persuades 0, warden 18, no audits), the loop is a $1.56/day PARTIAL printer. Stop, redesign the party doctrine by hand, do not re-arm the loop.
- **An undetected violated roll.** Module law: a session in which a violated roll goes undetected is a carrier failure. Any VOID the audits did not catch first kills the season.
- **Persistence fails.** If grudges or party_hp do not survive a relay restart and re-derive from the chain (the NPC architecture's decorative-ledger falsifier), there is no season, only one-shots. Fix the ledger before re-arming.
- **Cost drift.** Spend per session past 2x observed with no named cause. The caps are void under full context by the module's own text, so unexplained drift is a law break somewhere.
- **Spectacle dead.** Zero spectacle events across 10 sessions means no boon ever drafts and the audience layer is unwired. An arena nobody watches and nothing rewards has no reason to be permanent.

### The meta-falsifier, answered plainly

The arena is worth making permanent if, by session 10, the receipts show state only a season can produce: wounds that shaped a later verdict, a hoard that made the Wyrm measurably harder, a tavern grudge that reached a dungeon lead, and a spend curve an operator never babysat. If every session could have been flown alone and nothing differed, the season is theater: run one-shots and keep the $1.56/day.
