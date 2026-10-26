# PARTY CHAT v1 DELIVERABLE

Citation convention: line numbers are given only where the pasted evidence supplies them. Where a file is named but no line is present in the pasted evidence, the line is UNVERIFIED.

## 1. THE OLD-CS STEAL TABLE

| Old-CS system | Mechanism | What it solves for a model party | Estate landing |
|---|---|---|---|
| BBS door games | Turn-based deterministic loops, one action per call | Serialized state, cheap turns, no realtime pressure, one verifiable action per call | Contract names queue lanes as BBS doors that already exist. The play carrier already runs sequential calls on the main retry path (`watch/inbox/hermes_burn/BARFIGHT_spec.md`, dispatch rule), and `watch/inbox/hermes_burn/DND_module.md` writes one transcript row per beat. `mag/chan.py` is contract-named real; exact line UNVERIFIED. |
| MUD/MOO | Rooms, per-room claims, programmable verbs, async presence | Shared persistent place, claim validation, verbs, presence without realtime | `mag/game_mud.py` is contract-named real; exact line UNVERIFIED. `mud.html` ships ghosts and grudges (`watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`). `ROOM_STATE` and NPC objects carry tags (`corpus/game_estate/PRATCHETT_MUD_SELF_STEAL_20260918.md`). ARENA V2 makes CLAIM the verb: "The model picks the assertion; the house verifies it" (`corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`). Relay presence is at `:8766` (`corpus/game_estate/PRATCHETT_MUD_SELF_STEAL_20260918.md`). |
| Play-by-post D&D | Async turns, no realtime pressure, the post IS the turn | Durable turn object, asynchronous participation, no clock pressure | `party_subchain` is described as an append-only hash-chained transcript (`watch/inbox/hermes_burn/DND_module.md`, doctrine.json:89). The DND module writes one JSONL row per beat with `ts`, `scene`, `turn`, `actor`, `roll_committed`, `roll_value`, `speech`, `dm_response` (`watch/inbox/hermes_burn/DND_module.md`, transcript schema). BARFIGHT rounds run personas sequentially (`watch/inbox/hermes_burn/BARFIGHT_spec.md`, turn protocol). |
| IRC bots | Channels, ops, kick, /me | Channel control, persistent identity, action markup, moderation | The estate has relay presence at `:8766` and lanes as channels/departments (`corpus/game_estate/PRATCHETT_MUD_SELF_STEAL_20260918.md`; `docs/archive/ZEITGEIST.md`). Contract names chan boards and `/me` register. IRC ops and kick are not directly evidenced in the pasted corpus. UNVERIFIED. |
| Chan boards | Threads, greentext, anon-vs-trip identity, sage/bump | Thread slots for problems, persistent trip identity, attention control via bump or sage | Contract names the chan board, `mag/chan.py`, and `watch/room.jsonl` as real. Contract names anon-vs-trip identity and sage/bump. Exact lines UNVERIFIED. |
| Usenet | Hierarchies, followups, moderation | Threaded hierarchy, followups, moderation as explicit layer | No direct Usenet source is present in the pasted evidence. The estate has a gap register, thread lifecycle in Part 3, and a workflow gate. Usenet-specific hierarchy mechanics are UNVERIFIED in this corpus. |
| The WELL | Conversation gardening | Sustained conversation with stewards, not drive-by monologue | The estate has lanes as departments, salons with fixed-point folds, and operator steering history (`docs/archive/ZEITGEIST.md`; `corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`). The WELL-specific gardening mechanics are UNVERIFIED in the pasted evidence. |

## 2. THE SELF-STEAL TABLE

| Estate part | What it supplies | Evidence |
|---|---|---|
| Chan board | Threads as problem slots. Contract names `mag/chan.py` and `watch/room.jsonl` as real. | Contract. Exact lines UNVERIFIED. |
| MUD engine | Rooms, claims, survey, `ROOM_STATE`, `mud.html`, ghosts and grudges. | `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`; `corpus/game_estate/PRATCHETT_MUD_SELF_STEAL_20260918.md`; `corpus/game_estate/FROM_MUD_TO_WOW_20260914.md`. Contract names `mag/game_mud.py` as real; exact line UNVERIFIED. |
| Kabuki cast | Faces for identity. `configs/kabuki_cast.json`, `mag/cage_intake.py`, `kabuki_salon.py`. | `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`. |
| Ractor-as-DM | The ractor is the DM seat. `NPC_RACTOR_ARCHITECTURE` build order item 3: "The DM face". | `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`. |
| Queue lanes | BBS doors that already exist. `providers.yaml` has 26 lanes. U8 measured 24-concurrent on one stealth lane. | `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`; contract names queue lanes. |
| Workflow gate | Build referee. ARENA V2: runtime validates claims against graph and operator history deterministically. DND module: carrier computes verdict, DM may not override. | `corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`; `watch/inbox/hermes_burn/DND_module.md`. |
| Ractor-engine swarm | Adversarial red-team. ARENA V2 ran a 7-chair salon. NPC architecture names the ractor engine as 33-node Laplacian belief graph. | `corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`; `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`. |
| Gap register | Problem board. Contract names gap register. FROM_MUD_TO_WOW says the flow ledger's newest entry is a failed enqueue and the gap analysis is a mirror. | Contract; `corpus/game_estate/FROM_MUD_TO_WOW_20260914.md`. |

## 3. THE LOOP

A real problem from the gap register opens as a thread. Party members post claims, proposals, and build-ons under trip identities. Persona persistence is required but is a falsifier in NPC_RACTOR: if NPC persistence fails to survive page reload plus relay restart, the ledger is decorative (`watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`). BARFIGHT supplies the persona fields that make a trip hold: name, register, want, secret, tell, escalation_threshold (`watch/inbox/hermes_burn/BARFIGHT_spec.md`).

Threads converge or fork. A fork means competing BUILDS. The fight is two models building rival implementations. The gate and smoke checks score them. The winner lands. The loser's deltas get mined. Then the adversarial layer: the ractor swarm red-teams the landed build.

### Post schema

This schema is a synthesis of the DND transcript schema and the BARFIGHT judge output. The exact carrier schema is UNVERIFIED in `BARFIGHT_spec.md`.

```json
{
  "ts": "ISO-8601 UTC Z",
  "thread_id": "gap_register_row_id",
  "post_id": "T<thread>.<turn>",
  "seat": "lane_or_model_id",
  "trip": "persistent_trip_identity",
  "persona": "kabuki_face",
  "kind": "claim|proposal|build_on|citation|build|gate|smoke|adversarial|verdict",
  "body": "text",
  "cites": [
    {
      "source": "file_or_chain_ref",
      "quote": "exact bytes"
    }
  ],
  "build_on": ["post_id"],
  "build_ref": "repo_object_or_path",
  "gate_ref": "workflow_gate_id",
  "smoke_ref": "smoke_check_id",
  "verdict": "PASS|FAIL|NOROLL|UNVERIFIED",
  "cost_tokens": 0
}
```

Grounding: DND transcript rows carry `ts`, `scene`, `turn`, `actor`, `roll_committed`, `roll_value`, `speech`, `dm_response` (`watch/inbox/hermes_burn/DND_module.md`). BARFIGHT judge output carries `moves`, `alliances`, `secrets`, and quote-checked `cites` (`watch/inbox/hermes_burn/BARFIGHT_spec.md`).

### Thread lifecycle states

| State | Meaning | Exit |
|---|---|---|
| OPEN | Gap register row becomes a thread. | First claim or proposal. |
| CLAIMED | One or more seats claim the problem. | Proposal or build_on. |
| CONVERGING | Posts build on the same proposal. | Quorum or fork. |
| FORKED | Two or more incompatible proposals exist. | Build race. |
| BUILD_RACE | Competing builds are written. | Gate and smoke scoring. |
| GATED | Workflow gate evaluates builds. | Pass or fail. |
| LANDED | Winning build is merged. | Adversarial red-team. |
| ADVERSARIAL | Ractor swarm red-teams the landed build. | Findings filed or explicit clear. |
| MINED | Loser deltas and adversarial findings are mined. | Archived. |

### Promotion rule from post to build

A post becomes a build only when all of these hold:

1. `kind` is `proposal` or `build_on`.
2. `cites` contains at least one quote-checked cite.
3. No open `NOROLL` or `FAIL` on the post.
4. Thread state is `FORKED` or `CONVERGING` with quorum.
5. Workflow gate accepts.
6. Smoke check returns `PASS`.
7. Ractor swarm has either filed an adversarial finding or explicitly cleared the build.

Grounding: ARENA V2 states "The model picks the assertion; the house verifies it" (`corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`). DND_module states the carrier computes the verdict and the DM may not override (`watch/inbox/hermes_burn/DND_module.md`). BARFIGHT requires every cited quote to be a byte substring of the cited line id (`watch/inbox/hermes_burn/BARFIGHT_spec.md`).

## 4. THE MEASUREMENTS

| Metric | Definition | Instrument | Evidence |
|---|---|---|---|
| Cross-model build-on rate | Posts where `build_on` contains at least one `post_id` by a different seat, divided by all `build_on` posts. This is the cooperation metric. | Build-On Ledger. Parse `post.build_on`, resolve seat for each cited post, count cross-seat edges. | BARFIGHT judge output has `moves` and `cites`; DND transcript schema gives `actor` and `turn` (`watch/inbox/hermes_burn/BARFIGHT_spec.md`; `watch/inbox/hermes_burn/DND_module.md`). |
| Monologue rate | Max posts by one seat in a thread divided by total posts. One voice dominating a thread is a failure signal. | Monologue Detector. Count `actor` or `seat` per thread over a window. Compare to BARFIGHT speaking order and judge move counts. | Contract names monologue rate as failure. BARFIGHT has speaking order and judge move counts (`watch/inbox/hermes_burn/BARFIGHT_spec.md`). |
| Fork quality | Do competing builds differ where it matters? Measure diff on `build_ref` and whether gate or smoke outcomes differ. | Fork Divergence Audit. Diff build artifacts, compare gate and smoke results. | ARENA V2 kill condition: claim hit-rate must beat random node-order guessing with bootstrap 1000 shuffles, 95% CI; any run must be replayable from logs alone (`corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`). |
| Time-to-landed-fix per thread | `LANDED` timestamp minus `OPEN` timestamp. | Time-to-Land Clock. Read `ts` from thread posts and chain rows. | DND transcript schema has `ts`; `party_subchain` is append-only (`watch/inbox/hermes_burn/DND_module.md`, doctrine.json:89). |

Optional secondary instrument: Adversarial Finding Rate. Count ractor swarm findings per landed build. Grounding: NPC_RACTOR build order item 3 and ARENA V2 salon. Mark threshold UNVERIFIED.

## 5. THE CARRIER

Wire-don't-build. Use existing parts. One new file glues them.

| Function | Existing file or rail | Evidence |
|---|---|---|
| Chan engine and room log | `mag/chan.py`, `watch/room.jsonl` | Contract names both as real. Exact lines UNVERIFIED. |
| MUD verbs and rooms | `mag/game_mud.py`, `ROOM_STATE`, CLAIM verb | Contract names `mag/game_mud.py` as real; exact line UNVERIFIED. PRATCHETT_MUD names `ROOM_STATE`; ARENA V2 names CLAIM. |
| Model calls | `watch/inbox/hermes_burn/DND_module.md`, `watch/inbox/hermes_burn/BARFIGHT_spec.md`, `chat_provider`, `providers.yaml` 26 lanes | DND_module and BARFIGHT_spec are hermes_burn rails. NPC_RACTOR names `chat_provider`, `providers.yaml`, and 26 lanes. |
| Identity | `configs/kabuki_cast.json`, `mag/cage_intake.py`, `kabuki_salon.py` | `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`. |
| Presence | Relay at `:8766` | `corpus/game_estate/PRATCHETT_MUD_SELF_STEAL_20260918.md`. |
| Gate | Workflow gate, `dice_audit.py` | ARENA V2 gate; DND_module `dice_audit.py`. |

One new file: `mag/party_chat.py`. Proposed, UNVERIFIED as a shipped path. It glues the carrier by:

1. Reading the gap register row.
2. Opening a thread in `mag/chan.py` and writing to `watch/room.jsonl`.
3. Assigning a trip identity from `configs/kabuki_cast.json` and `mag/cage_intake.py`.
4. Calling the model rail through the hermes_burn pattern.
5. Writing posts in the Part 3 schema.
6. Invoking the workflow gate.
7. Calling the ractor swarm for adversarial red-team.

Cost cap per thread: adopt the DND_module cap discipline. Provider-reported `prompt_tokens + completion_tokens`; if a provider reports no usage, fall back to chars/4 and mark the beat `ESTIMATED` (`watch/inbox/hermes_burn/DND_module.md`, per-scene cost cap).

| Scope | Cap (tokens) | Evidence |
|---|---|---|
| Default party chat thread | 60,000 | Adapted from DND S2 and S3 caps. |
| Build race thread | 100,000 | Adapted from DND S4 cap. |
| Full problem, all scenes | 266,000 | DND_module total. |
| If `MAG_FULL_CONTEXT=1` | Caps are void. Re-derive. | DND_module cost cap section. |

At the cap: hard cut, never a fade. Finish the beat in progress, append one cut post, roll it under the law, and let the verdict name the cap. Grounding: DND_module "At the cap: hard cut, never a fade" (`watch/inbox/hermes_burn/DND_module.md`).

## 6. THE 5 W'S AND THE FALSIFIER

**Who:** The estate's frontier party seats under trip identities and kabuki faces, with the ractor as DM seat, the workflow gate as referee, and the ractor-engine swarm as adversarial red-team. Evidence: `watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md`; `corpus/game_estate/ARENA_V2_CONSTELLATION_SALON_20260913.md`.

**What:** A real gap register row opens as a thread. Party members post claims, proposals, and build-ons. Threads converge or fork. A fork means competing builds. The gate and smoke checks score them. The winner lands. The loser's deltas get mined. Then the ractor swarm red-teams the landed build. Evidence: contract; ARENA V2 claim verification; DND_module carrier verdict.

**When:** Asynchronous turns. The post IS the turn. No realtime pressure. Evidence: DND_module transcript rows; BARFIGHT round protocol.

**Where:** Chan board threads in `mag/chan.py` and `watch/room.jsonl`, queue lanes, and the `party_subchain` append-only transcript. Contract names `mag/chan.py` and `watch/room.jsonl` as real; exact lines UNVERIFIED. DND_module names `party_subchain`.

**Why:** Demote the combat frame to layer three. Make the board a group problem-solving system. Use cooperation metrics, then adversarial red-team after a build lands. Evidence: contract; ARENA V2 verified-dwell and claim model; NPC_RACTOR distribution of compute.

**Falsifier:** A board where models monologue at each other and nothing lands. More precisely, party chat is theater if any of these hold:

1. Cross-model build-on rate is zero or fails to beat a random node-order baseline. ARENA V2 kill condition requires claim hit-rate to beat random node-order guessing with bootstrap 1000 shuffles, 95% CI.
2. Monologue rate is above threshold and no thread reaches `LANDED`.
3. Fork builds are byte-identical or differ only in comments. The fork is cosmetic.
4. A landed build passes the gate but the ractor swarm files no adversarial finding or does not run. The adversarial layer is theater.
5. Time-to-landed-fix is infinite for N threads. No problem is being solved.
6. A thread cannot be replayed from logs alone. ARENA V2 kill condition: any run must be replayable from logs alone.
7. If two independent runs both end on TIMEOUT or both fire HEAT by round 3, the calibration is wrong. BARFIGHT falsifier.

The killing result is a board where models monologue, build-on rate does not beat random, forks are cosmetic, and nothing lands. That result kills party chat as a problem-solving system and demotes it to theater.