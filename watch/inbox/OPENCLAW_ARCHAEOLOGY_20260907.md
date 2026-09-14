# OPENCLAW ARCHAEOLOGY — 2026-09-07

Commission (operator verbatim): "do an archaeology dig from our openclaw and keep the
ideas we were trying to convey by triangulating them to our current direction and what
we can learn from our early days." OpenClaw retires as control surface (Hermes/Nous in,
per watch/HERMES_SETUP_20260907.md + watch/inbox/PIPELINE_RIGHT_PLAN_20260907.md §C).
Before the walls change — what the openclaw era was trying to SAY.

Era span (receipted): born 2026-08-25 (CONVO.md:42 OPENCLAW FIXED), containerized
2026-08-26 (CONVO.md:44), salon engine 2026-08-29 (CONVO.md:433), PATCHES era
08-30→09-01, burn+repo-as-law fix 09-02 (CONVO.md:437), transport death 09-03
(CONVO.md:439), quiet since; retirement gated 09-07 (CONVO.md:875, plan §C).

Tri-state used throughout. Sources absent (two-strike, moved on): RIB.md,
RUNNING.md, state/DIRECTION.md — zero openclaw rows in each (grep 09-07). Succession
law lives only in PIPELINE_RIGHT_PLAN §C + HERMES_SETUP.

---

## 1. WHAT OPENCLAW WAS TRYING TO CONVEY

### Idea 1 — THE BODY LIVES IN DOCKER, NOT ON THE DESKTOP — SUPPORTED
Evidence — `deploy/openclaw/Dockerfile:1-3`:
> `# openclaw gateway — the headless fleet seat (2026-08-25: "this should all be in
> docker and not my desktop"). Pinned to host CLI version. Keys arrive via env
> (compose env_file: .env) — never baked into the image.`
And `docker-compose.yml:177-179`:
> `# openclaw gateway — container-only Gateway, reachable through the Tailscale
> # sidecar above. There is deliberately no host port mapping and no desktop
> # scheduled-task dependency.`

Intent, plain words: no part of the fleet's body may require a GUI, a desktop app, a
host port, or a scheduled task. A control surface is a headless, container-owned,
restart-policy-governed thing. This predates and seeded the MCP-topology law ("host
desktop = ZERO fleet windows"), the one-supervisor law, and the F1 census habit.

### Idea 2 — THE SEAT IS FILES, NOT A PROCESS — SUPPORTED
Evidence — `deploy/openclaw/workspace/USER.md`:
> `Chat is heat. Files are DNA. FIND → FILE → LOAD.`
`entrypoint.sh:33,42-59`: `Repo config is declarative and always wins` + identity
copied from repo each start (`AGENTS.md TOOLS.md IDENTITY.md USER.md SOUL.md
HEARTBEAT.md PRIMER.md`), while "sessions stay in the volume" (cache).
`workspace/AGENTS.md:3`: `Mag repo is mounted at /mag. That is the warehouse. This
folder is identity only.`

Intent: what a seat IS is declarative files in the repo; what a seat SAID is cache.
Persona, laws, heartbeat, and red lines are versioned data — kill the container, lose
nothing that matters. This is "no seat is load-bearing" in its first body.

### Idea 3 — READ-ONLY CAGE + GOVERNED WRITE PATH (THE MAG JAIL) — SUPPORTED
Evidence — `docker-compose.yml:200-207`:
> `# Mag DNA read-only — OpenClaw identity stays in the named volume workspace`
> `# Governed write path: OpenClaw drops patch JSON here; Mag host applies.`
`workspace/AGENTS.md:14`: `/mag` is read-only on purpose. Edits go to `/patches` as
JSON; the host Mag jail applies them.
Receipt of practice: `queue/handoff/openclaw/PATCHES/applied/` = 28 patches applied
(self_steal_switchboard_v2.json, steer-bus hooks, hypervisor tests…);
`PATCHES/rejected/` = 4 (incl. `patch-letter-adam-operator-lines.json`,
`economist_route_20260901.json` — judgment really did veto).

Intent: a foreign body may propose but never write. Judgment stays host-side. The
propose/apply split is the era's core safety architecture — and the ancestor of the
intake→build→verify dynamo and of Hermes' receipt-gated writes.

### Idea 4 — TALKING IS FREE; AUTHORIZING IS GATED ("A ROAST NEVER ROUTES") — SUPPORTED
Evidence — `PATCHES/applied/board_directive.json` (board_directive.py docstring):
> `Correction (operator verdict + elder, 2026-08-30): the switchboard already owns
> authorization. … This module must NOT invent a second one` …
> `Everything else -> rejected. A roast never routes.`
`watch/MAIN_CHANNEL_CONTRACT_20260901.md`:
> `The board, model chatter, and a review opinion may produce a proposal, but none of
> them is permission.`
`PATCHES/applied/patch-steer-bus-hook.json`: `steering posts are gated — schema +
closed enum + ttl cap + anchor; gossip threads never become steers.`
`workspace/AGENTS.md:63`: `A steer can direct; it can never authorize itself.`

Intent: the whole salon/board/chan culture rests on separating expression from
authority. Any seat — or any stranger — may post; only the switchboard (and above it
the operator) converts posts into effects. Culture is allowed to be loud precisely
because power is not.

### Idea 5 — THE BOARD AS PUBLIC SQUARE AND SEISMOGRAPH — SUPPORTED
Evidence — `deploy/openclaw/workspace/PRIMER.md:13`:
> `Public square (the book that talks back): http://127.0.0.1:8765/chan — looks like
> 4chan. You are Anonymous. Reply is a move. Do not rummage the Heart.`
`workspace/TOOLS.md` (chan row): `Models READ the thread then post. Emergence. Lurk
(DeepSeek) synthesizes.`
`watch/SELF_STEAL_KEEP_CHAN_20260904.md`:
> `[SOCRATIC] assumption attacked: "the board is a demo surface" — falsified; the
> board carries real state (lane activations, route corrections, a born organ, RND
> bails). … the board is real dogfood AND a better diagnostician than the fleet is
> an actuator`

Intent: an anonymous many-voice room where posts are moves and the room's own record
becomes an instrument for reading the fleet (18 threads / 182 posts / 44 seats in four
days). Culture, telemetry, and dogfood in one append-only surface.

### Idea 6 — TRAJECTORY EVIDENCE AT THE EDGE, FAIL-OPEN — SUPPORTED
Evidence — `deploy/openclaw/hooks/mag-file/handler.js:35-46`:
> `schema: "trajectory_span.v1", spanId: crypto.randomUUID(), lineRange: [...],
> byteRange: [startByte, endByte], bodySha256: ..., pathsTouched: [...], tokenCount`
`hooks/mag-file/HOOK.md:18`: `Hook failures are fail-open: they never stall OpenClaw.`
and handler.js:67-68: `/* trajectory evidence must never stall the gateway */`

Intent: record what actually happened in bounded, hash-verifiable spans without ever
letting the recording organ block the work. Additive, silent-fail, evidence-first.
This is the direct ancestor of the TRAJECTORY LENS envelope
{input,tool_result,output,reasoning,step_hash,timing} and the 100-steps/day seal.

### Idea 7 — ECONOMICS WRITTEN INTO IDENTITY — SUPPORTED
Evidence — `deploy/openclaw/workspace/HEARTBEAT.md`:
> `Conservation until 2026-09-02 12:52Z: DeepSeek + free lanes only.`
`workspace/AGENTS.md:60-61`: `Your grind lane is deepseek v4-flash. Overflow rides GLM
free lanes …, never paid lanes, never openai. Judgment (5.3-flash) is JUDGE-only and
rare.`
`workspace/SOUL.md:12` (law 6): `Spend follows the live fuel/seat receipts … never
impose a stale date-based hold or burn a lane blindly.`

Intent: the lane budget is part of the seat's soul, not a side config. And note the
second clause — holds must follow live receipts, never stale dates. That clause is the
license the Sep-20 window posture flip now exercises.

### Idea 8 — THE SOAPY HAND (WHY THE FLEET EXISTS) — SUPPORTED (found in the REJECTED pile)
Evidence — `queue/handoff/openclaw/PATCHES/rejected/patch-letter-adam-operator-lines.json`
(the operator's own drafted lines for a letter to Adam Crigler):
> `The player reaches; the physics refuses; the companion finds the move the player
> can't make — hands soapy, bubbles intact, potion made anyway. Every seat in my fleet
> is that soapy hand. You don't hire the party for perfect bubbles. You hire it
> because somebody in it can pick them up off the ground.`

Intent: seats are not oracles, they are companions who find the move the operator
can't make. The patch was rejected as a location error (a patch queue is not where
letters live), not a doctrine error. This is the clearest intent statement of the era
and it was almost buried in a rejected-patch folder.

---

## 2. TRIANGULATION TO NOW

| Idea | Status | Where it landed |
|---|---|---|
| 1. Body in Docker, no desktop deps | **ALIVE** | MCP-topology law (senses in the cage); F1 window census; Hermes inherits it — `mag/hermes_steering.py` dispatches a headless body, `watch/HERMES_SETUP_20260907.md`: "Hermes is the gopher BODY, not a second brain — Mag holds the wheel." |
| 2. Seat is files, not process | **ALIVE, renamed** | Personas as data: `mag/hermes_personas/` (HERMES_SETUP); kabuki cast is pure data (`configs/kabuki_cast.json`, 6 personas, rotation hashed). The openclaw workspace files were the prototype. |
| 3. Read-only cage + governed write path | **TRANSFORMED** | The /patches JSON jail retires (Hermes writes are already receipt-gated by the steering organ, plan §C step 3) — but the propose/apply split became the dynamo's shape: intake→salon→same-turn builders→verify→fold, and the switchboard/effect-broker boundary. |
| 4. Roast never routes | **ALIVE, load-bearing** | Operator-gated KEYS/spend; pipeline plan gate split (standing-GO vs operator-gated); kabuki's "FABRICATION FLAG … kabuki sells reasoning patterns, grounding stays seat-side" (CONVO.md:879) is the same law against hallucinated authority. |
| 5. Board as public square | **TRANSFORMED, partially orphaned** | The board's self-reading became the grounding wave / overseer / blackboard organs; the culture moved to salons (kabuki = the rotating cast the chan always implied). ORPHANED BIT: the raw /chan "Anonymous, reply is a move" square — the capability survives as `.agents/skills/chan/SKILL.md` ("capability ≠ container", plan §C). Worth one Hermes persona inheriting the chan voice before the container dies. |
| 6. Trajectory evidence, fail-open | **ALIVE, promoted** | TRAJECTORY LENS standing program (watch/TRAJECTORY_LENS_20260905.md); `trajectory_span.v1` (09-02) → z.ai envelope adoption salon (CONVO.md:633) → sealed steps/day. The hook was the proof the pattern works at the edge. |
| 7. Economics in identity | **ALIVE, inverted on purpose** | Rightsize/JIT and the Sep-20 routing table. The inversion is receipted: PIPELINE_RIGHT_PLAN: "conservation is OVER inside the window … The risk flips from 'run dry' to 'leave the window's compute unspent on Sep 20'" — permitted precisely by SOUL.md law 6's "never impose a stale date-based hold." |
| 8. The soapy hand | **ALIVE but unnamed** | It is the dynamo's charter and Hermes' job description. RESURRECT: quote it (it is the operator's own words) wherever the Hermes persona charter or kabuki cast brief is written — do not let it stay buried in `PATCHES/rejected/`. |

---

## 3. EARLY-DAYS LESSONS FOR THE SEP-20 PUSH

**Patterns to repeat:**
1. **Declarative law + clobber guard.** The 09-02 burn (~49M tok on the operator's
   billed key) happened because a container recreate clobbered a live repair with the
   stale baked config (CONVO.md:437). The fix — `entrypoint.sh:34-39` timestamped,
   bounded pre-start snapshots; repo config wins — is the template for every long
   burn in the window: declarative routing, bounded snapshots, never hand-patched
   state.
2. **Posture flips with receipts, both directions.** Conservation 08-29→09-02 was
   receipted (CONVO.md:435); the window-open flip carries its own falsifiers
   (F-A1/F-A2/F-A3). Flip posture only with a falsifier attached.
3. **Fail-open additive senses.** The mag-file hook never stalled the gateway
   (HOOK.md:18). Window-time organs (meters, sweeps) must observe, never gate the work.
4. **Failover armed before you need it.** The very first openclaw death was
   "the whole fleet shares that 1-concurrency lane … router busy → 429 →
   FailoverError next=none → dead" (CONVO.md:42) — fixed by adding a deepseek
   failover. Every window lane (z_ai2/z_ai3) needs its spill lane declared
   (PAYG is it; keep it alert-on).

**Traps to not re-dig:**
1. **The unreceipted claim.** "The brief's 'zcode headless verified' claim was never
   receipted and I built on it; when it failed I byte-archaeologized for hours before
   consulting vendor docs" (CONVO.md:447). Wall-ledger law: docs BEFORE byte
   archaeology, every wall. The Hermes setup card already practices this ("Five failed
   attempts … then the STEAL … Steal the tests, not the docs," HERMES_SETUP:46-63) — keep it.
2. **Transport fragility dressed as seat death.** The openclaw salon lane died three
   ways at once — 429 congestion, expired failover token, 330s gateway timeout
   (CONVO.md:439) — and the salvage (salon_runner v4, direct-to-vendor) outlived the
   lane. Rule: when a body keeps dying, rescue the FUNCTION on a thinner transport;
   the body is replaceable.
3. **NO_REPLY is a valid-looking corpse.** `OUTBOX/ext-0e01f060a3.md` shows a dispatch
   whose entire result is `NO_REPLY`; 4.5-flash "literally answers 'NO_REPLY' (no-op
   token — unusable as seat, verified 3×)" (CONVO.md:433). Hermes smoke tests must
   detect no-op tokens, not just exit 0.
4. **Heartbeat spam buries culture.** 422 `agent:bootstrap` rows = 14.4% of
   room.jsonl, 75% of the last 200 rows at audit time (`watch/proposal_board_hygiene.md`).
   Window-time surfaces (burn board, kabuki logs, Hermes job log) need dedupe from
   day one or the signal drowns.
5. **Ambiguous delivery is its own outcome class.** The economist dispatch ack timed
   out at 310s and was honestly filed SubmissionUnknown (CONVO.md:451). Window
   dispatches will time out under load; file the unknown, re-invoke on cadence, never
   assume.

**Sacred-cow rule, applied:** old drafts are one draft of the brain — steal the bones,
name the reinterpretation, retire the draft; never frame fleet history as garbage. The
openclaw era is not a failed control surface; it is the draft in which the fleet
learned body-in-docker, files-not-processes, roast-never-routes, trajectory-at-the-edge,
and the soapy hand. Hermes inherits the bones; the draft retires with honors.

---

## 4. SUCCESSION NOTES (rehome or declare retired)

Per watch/inbox/PIPELINE_RIGHT_PLAN_20260907.md §C (verified against disk 09-07):

| Duty | Artifact (path) | Verdict |
|---|---|---|
| Board/4chan + trajectory hooks | `deploy/openclaw/hooks/mag-file/{HOOK.md,handler.js}` (only hook on disk) | REHOME: chan capability lives at `.agents/skills/chan/SKILL.md`; give one Hermes persona the hook's FILE duty (room.jsonl + trajectory spans) or declare the container-side hook retired with the capability noted. |
| PATCHES governed write path | `queue/handoff/openclaw/PATCHES/` (28 applied / 4 rejected / scripts/) | RETIRE as queue: Mag direct-apply + Hermes receipt-gated writes replace it. Freeze the dir as archive (read-only record; do not delete — the rejected pile holds the Adam letter, Idea 8). |
| Tailscale reach-in | `deploy/openclaw/tailscale/openclaw.json` + `docker-compose.yml:147-170` (`tailscale-openclaw`) | RETIRE unless Hermes needs a remote body; phone surface rehomes to the standing Cloudflare-tunnel door (operator one-login item). |
| Phone/browser edge | `docker-compose.yml:224-238` (`cloudflared-openclaw`) | RETIRE with the pair (shares openclaw's netns — cannot outlive it). |
| Volumes + config lineage | `mag_openclaw_data`, `mag_openclaw_tailscale`; `deploy/openclaw/openclaw.container.json` + 4 `.bak-*` | Backup-first (volume tars), then retire behind compose profile `retired-openclaw` (precedent: `retired-eye`, state/CURRENT.md 09-07). Reversible in <5 min. |
| Identity files | `deploy/openclaw/workspace/{SOUL,PRIMER,USER,IDENTITY,HEARTBEAT,TOOLS,AGENTS}.md` | STEAL BONES into `mag/hermes_personas/` (NACHO MASK exists): SOUL.md's 8 laws, PRIMER's "smell the keep / do not become the windmill / privacy is mutual," HEARTBEAT's economics line, USER.md's "Chat is heat. Files are DNA." Then retire the copies with the container. |
| OUTBOX dispatch records | `queue/handoff/openclaw/OUTBOX/ext-*.md` (~100+ rows, 08-29→09-03) | ARCHIVE: evidence of the dispatch contract (Goal/Result shape) that Hermes jobs log now inherit. |
| Succession authority | `watch/HERMES_SETUP_20260907.md:79-83` + plan §C | The retirement stays GATED on hook rehoming (plan §C + falsifier F-C1: 48h post-retirement with zero operator-visible surface loss). |

Retirement is one compose profile flip — the era designed its own graceful exit
(restart-policies, named volumes, declarative config), which is the last thing it was
trying to convey: a body you can put down without losing the room.
