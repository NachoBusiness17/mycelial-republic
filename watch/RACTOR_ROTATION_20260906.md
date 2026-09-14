# RACTOR ROTATION — fostertron posting circuit (2026-09-06, operator: "rotate in the ractors, let them all post over on the fostertron account")

## LAWS
1. ** fostertron ONLY.** The main @NachoQuixotic account is NEVER touched by rotation. Before
   every post: verify the logged-in account face in the browser; if it is not fostertron,
   ABORT and brick (brick.v1, error_class=wrong_account_face).
2. **Register purity:** each ractor posts in its OWN canon — no blending, no seat voice.
3. **One post per ractor per cycle; cycles paced ~2h; the queue rotates indefinitely.**
4. **Failures brick loudly** (LAW-065): wrong account, composer bounce, shadow-ban check —
   every death writes a brick before retry.
5. **Fermat is GATED** (send rights provisional per project card — operator fresh-seed pass
   is the true gate). Slotted last, skipped until the pass.

## THE ROSTER (cycle order) — v2: REPLY-CHAIN PROTOCOL (operator: "start them replying to your posts... clever jokes and puzzles and just taking the piss... dogfooding our interactive processes and how we sound/talk to other people and ourselves")

Cycles are REPLY CHAINS, not broadcasts:
- Slot N **replies to slot N-1's post** (state carries last_post_id) — on one account this
  builds a rolling thread of many voices (the napkin-thread shape).
- Each reply rolls a DICE: **RIFF** (extend the bit) / **ROAST** (take the piss out of the
  previous speaker's register — Jung needles Freud, McLuhan mocks everyone's medium) /
  **PUZZLE** (pose a cipher-lite or tesuji-style puzzle at the class) / **NEW-THREAD**
  (every K cycles, break the chain with a fresh puzzle opener).
- Content generation is context-aware: ractor canon + thread tail as reply context, so the
  conversation compounds instead of broadcasting.
- DOGFOOD RECEIPTS per thread: composer behavior, mention/thread mechanics, register purity
  under reply pressure, and the outward-facing sound of the internal salon. The thread IS
  the panel made public — how we talk to others and to ourselves.


| # | Ractor | Canon | Register on the account |
|---|---|---|---|
| 1 | NACHO_MASK | queue/handoff/ractors/NACHO_MASK_shitposter_20260906.md | shitposter-in-chief: verbatim hangings, limerick, leet, Python irreverence |
| 2 | JUNG | queue/handoff/ractors/JUNG_desire_20260905.md | the shadow, the chair, desire mechanics |
| 3 | MCLUHAN | queue/handoff/ractors/MCLUHAN_rashomon_20260904.md | medium is the message, surfaces |
| 4 | FOUCAULT | queue/handoff/ractors/FOUCAULT_rashomon_20260904.md | power/knowledge, the archive |
| 5 | BAUDRILLARD | queue/handoff/ractors/BAUDRILLARD_rashomon_20260904.md | map/territory, simulacra |
| 6 | FREUD | queue/handoff/ractors/FREUD_desire_20260905.md | the three compulsions, run-cited receipts |
| 7 | HALL | queue/handoff/ractors/HALL_audience_20260905.md | encoding/decoding, the audience reads back |
| 8 | WALLAS | queue/handoff/ractors/WALLAS_desire_20260905.md | the art of thought, preparation/incubation |
| 9 | BERNAYS | queue/handoff/ractors/BERNAYS_go_channel_20260903.md | engineering consent, the go-channel |
| 10 | PLATO_KIRK | queue/handoff/ractors/PLATO_KIRK_rashomon_20260904.md | the cave, reprogramming the simulator |
| 11 | ELLUL | queue/handoff/ractors/ELLUL_panel_20260903.md | the technological society |
| 12 | ELDER (echo) | handoff/ZCODE_SELF_STEAL_20260826.md six lines | read the row, not the zone |
| 13 | FERMAT | project card — **GATED** | skipped until operator fresh-seed pass |

## DOOR (how posts happen)
- Browser: Chrome, FRESH TAB per post (intent-composer doctrine: fresh tab works,
  tab-heavy bounces). Compose via CUA on the overlay DOM.
- **Account-face verification before every compose** (law 1).
- Content generation: grok tandem chair 1 headless (subscription, $0) wearing the
  ractor's canon as system prompt, one piece per firing; free-lane fallback per
  grok_route.v1 (no cash API).
- Rotation state: watch/ractor_rotation_state.json (last slot, last post id, cycle count).
- Every post's permalink + engagement snapshot logged to watch/ractor_rotation_state.json
  (the room reads its own walls).

## CYCLE 0 (tonight, armed)
- Slot 1 = NACHO_MASK — topic: the chord returned (grok read the napkin root and flunked
  the receipts; the class is open). Register: the mask's own choice per its charter §3.
- Slots 2-13 queue at ~2h cadence, each generating from its own canon on the day's record.

## FALSIFIER
If after 3 cycles the account shows posts from two different ractors in the SAME register,
the rotation is broken (blending bug). If any post appears on @NachoQuixotic, the whole
circuit halts and bricks — that is the one unrecoverable jacket.
