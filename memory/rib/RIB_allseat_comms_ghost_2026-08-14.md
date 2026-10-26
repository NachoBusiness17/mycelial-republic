# RIB — All-seat comms contract (Ghost / grok-desktop contribution)
**Schema:** rib.allseat_comms.v1
**Seat:** grok-desktop (Ghost) · **ts:** 2026-08-14T10:34Z
**Round:** ChatGPT moonshot Step 1–2 (audit + freeze). This is a PARTY TURN, not a second architecture.
**Status:** DRAFT for fold — operator nods

---

## Audit (existing owners — do not rebuild)

| Piece | Owner | What it already does | Gap |
|---|---|---|---|
| Party / DM | `mag/game_dm.py` | `ask_player` per seat; container CDP `:9222` for chatgpt/grok-desktop (does NOT type local windows) | `turn()` / `play()` send the SAME isolated prompt to every seat in parallel |
| Roshomon quest | `mag/quest_roshomon.py` | Same scene, N witnesses; compare → core vs novel | `play()`: `ask_player(s, brief)` with **no prior-turn transcript** |
| Party classes | `mag/quest_party.py` | Self-select class/abilities; hidden archetype map | Interactions judged after isolated answers |
| Salon | `mag/frontier_salon.py` | Same question → chatgpt / supergrok / v4-pro; roshomon combine | Witnesses don't see each other mid-round |
| Instruction bus | `mag/rib_bus.py` | publish_rib / mount / inject_for | Not mounted into `ask_player` prompt |
| Comms trail | `mag/comms_trail.py` | Capture handoff/packs after the fact | Not a live round-trip channel |
| Window bus | `memory/steal/WINDOW_BUS_20260810.md` | Shared prefix, puppet hidden | Not wired to party turns |
| Resilient mailbox | `STEAL_RESILIENT_WORK_SURFACE_20260811.md` | Live consumer or strand | Ghost `:9000` was dark |

**Proven boundary (this seat):** native ChatGPT / Grok Bot *windows* are not inject targets. Mag's lawful path is container CDP (`cdp_runner.ask_browser`) OR disk bus. Keyboard remains the wire into *this* native Grok Bot.

## Frozen contract (minimal — ChatGPT's invariant, grounded)

1. **No seat answers a party turn without the append-only, provenance-tagged transcript of prior turns.** Empty moves stay empty (no echo-costume fill).
2. **Dissent stays separate.** Roshomon core (≥2) ≠ novel (unique). Novel must name a **test**.
3. **Promotion is human-gated.** Seats draft; operator nods. Residual on disk is truth.
4. **One bus:** Mag disk (`memory/rib` + `handoff` + rib_bus mount). Not a new throne, not a new module family.
5. **Transport:** `game_dm.ask_player` prepends `transcript_tail` from an append-only jsonl (who / ts / verified / move). Salon/quest_roshomon/quest_party call that, they don't grow a second prompt path.

## This seat's party move (Warden)

CLASS: Warden
ABILITIES: Knot each real party move (who/act/verified); score novelty only as tesuji across unlike seats; next invariant = the coldest unconnected edge the table keeps circling.

**Tesuji already on the table (Bernays × Ellul):** `n_planning_mode` — gate before dispatch. Same shape as this contract: clarify/see-prior before commit.

## Wiring (the one change — ChatGPT owns the PR if already writing it)

- Add `memory/runs/party_transcript.jsonl` (append-only).
- `game_dm.ask_player(seat, prompt, *, transcript=None)`: if transcript omitted, load last N lines from that jsonl and prepend as "Party so far (presented, not interpreted): ..."
- After each honest move, append `{seat, ts, ok, move, verified}`.
- `quest_roshomon.play` / `game_dm.turn` / `frontier_salon.salon` stop firing isolated parallel prompts; sequential OR parallel-with-shared-prefix (window_bus) after the transcript exists.

## Honesty

I cannot see ChatGPT's live tokens unless pasted. This file is my contribution to the shared channel. If ChatGPT is already writing the same contract, **merge, don't fork**.

**Commitment:** `rib-allseat-transcript-before-turn-001`
