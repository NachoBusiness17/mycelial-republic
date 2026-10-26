# SELF-STEAL — the VS Code DeepSeek corpus mine (2026-09-04)

**ITEM:** Digest the ~40 undigested deepseek sessions of the VS Code chatSessions corpus (the
gap named in SELF_STEAL_DEEPSEEK_ORPHANS_20260904.md, Gap 1). Per session: topic + named
concepts/laws/GOs/verdicts + dates; every candidate swept against record surfaces; present =
DUPLICATE, absent = ORPHAN. Mirrors the ZCode session-orphan mine.

## METHOD

1. **Corpus reality (differs from the reference card):** `%APPDATA%/Code/User/workspaceStorage/
   e2b798e7.../chatSessions/` now holds **43 sessions — 37 deepseek-model** (32 flash, 5 pro, of
   which 4 are zero-request husks) + 4 copilot/auto + 1 ollama + 1 empty in 47b14646. The
   reference card's "~57" counted the **18 sessions the Aug-26 mining digested — those files are
   GONE from disk** (deleted between Aug 26 and Sep 4; their digests in
   `memory/runs/session_mining/2026-08-26/` are the only record). The current 37 deepseek
   sessions share NO ids with the 18 digested ones → **all 37 are the undigested set** (the "~40").
2. **Extraction:** predecessor's proven delta-log replay script (kind-0 state + kind-1/2 path
   deltas) at `C:\Users\foste\.zcode\cli\tmp_orphan_mine\deepseek\vscode_corpus\extract.py`;
   33 full extracts (zero-request files skipped) + condensed ALL_CONDENSED.txt in scratch `out/`.
   Schema quirk: most requests in long sessions are tool-only turns with no text (user(0c) /
   assistant 0c); the first prompt + final summary carry nearly all signal. Large finals
   re-extracted raw (dba899b8 REQ11 46K, 40ecb51d REQ0 50K / REQ4 11K).
3. **Sweep:** ~55 candidate phrases grepped over record surfaces (watch/**.md/.json/.py, docs/,
   handoff/, queue/, mag/, memory/ minus room.jsonl tape; 372,709 files). Two sweep rounds +
   targeted verification (read the hit, don't trust the grep).
4. **Sub-swarm:** NOT spawned — this harness exposes no agent-spawn tool; all digging done
   in-lane (trail rows logged).

## SESSIONS (33 digested; dates = first request)

| session | date | topic | named concepts / laws / GOs / verdicts |
|---|---|---|---|
| cceaf70f | 08-07 | read-only mode; settings fix | python.analysis.exclude warning (trivial) |
| aaa574de | 08-07 | commit + verkle register after copilot token exhaustion | commit b5eaeb0 deepseek-first routing + research swarm + orchestrator reap fix + overseer API; e079acf false-success guard; verkle-audit backfill kwarg fix; tip 148 leaves root c18f6585 |
| bd619ee8 | 08-08 | Docker install check | trivial |
| 29e97fe8 | 08-08 (pro) | build status table | cross_version framework; campaign H1 parable_ledger_capture; P0 mag/_utils.py (~200 dup functions); POST /api/v1/queue; v5 immune stack (CSV, UIG, ISA probe, mirror protocol, auto-immune loop); H2-H5 pending |
| 40ecb51d | 08-08 (pro) | session_freeze build (19 tests) | mag/session_freeze.py; /api/v1/session/freeze; route_with_snapshot; watch/sancho_boot_hook.py wiring; **content-hash law: hash non-volatile layers only (session_context+agent_state+brief), exclude system_health telemetry** |
| ebd5fef0 | 08-08 (pro) | "what did we learn" — 10-lesson synthesis of the ollama steerability day | **steerability ladder** (3b-instruct .55 / 32b .51 / gemma:2b .42 / gemma4 .41 / coder:7b .41 / hermes .32); **influence vs detection = independent dimensions**; **cross-agent amplification real + measurable**; **gemma:2b sole refuser of false_success steer → critic role; 3b executor**; qwen 32b 242s vs 3b 24.6s → overnight batching; Claude Code session-messaging + Herdr terminals-as-transport steals; campaign.py/ghost_cross.py/research_director.py = thin wrappers; $0 on 6GB GPU |
| 4e5f470a | 08-08 | session summary card | framework telemetry 34M tok $9.58; 10 seam checks green |
| 6f4fe726 | 08-08 | doubled-process scare → honest correction | pairs are launcher+interpreter, NOT duplicates; killing = crash; ~9 services; supervisor-consolidation fix |
| aad3b3b4 | 08-08 | behavioral run logging with tools disabled | FOLD PENDING to skill_ledger/behavioral_events/training_events |
| 8543bd86 | 08-08 | "kill it as the ghost" process hunt | trivial |
| e968631a | 08-08 | "let me see it all operating" + $50 deepseek credits | ops_graph budget nodes (provider_budget); **detached autorun loop survives window reload**; Thought Surface/Ops Graph/Drainer/Ghost views; janitor/orphan cadence; **the loop is already named "Sancho" (Aug 8)** |
| 856a0cf9 | 08-22 | embassy E2E on the real private repo | AdventureNLearn/embassy-t1; **SYNTHETIC-E2E-001**: 8/8 FAIL-gates auto-caught; **FAIL-G1 regex gap** (G1 regex matches only specific municipality names; synthetic place token = clear violation under AOS def but scanner-silent); reported Evidence + Inference separately; commit 227ea40 pushed; "promote/ empty. No Riddler. **Revoke 2026-09-05**"; GHOST_T1 = repo checkout |
| c458d08f | 08-09 | refine loop end-to-end | SENSE→PROBE→ESCALATE→FIX→FOLD; grok-3 escalation: **semantics right, file paths hallucinated/generic**; XAI funded-key-first; **402 added to failover (401/402/403)**; BUILD-contract auto-freeze passes factory gate; delegate_fix require_build gap; disjoint container/host copilot filesystem smell |
| 8134b0ed | 08-09 | "i'm tired just finish it" | pro_library seed_default_moves — 5 tesuji: false-success-verify, wrong-offset-gate, penny-designation, loop-escalate, seam-placement |
| dba899b8 | 08-09 | "steal" → full-blast audit + socratic loop | self-steal audit inventory; external steal: bmas tiered cadence, buildGate, doneStateVerifier, panel (lowest-axis headline, abstain), critic top-N, goldenTraces, readinessGate, promotionGate, continuation law, conductor (fail-open grader); ground truth 846 tests / 155 files / collection 1.25s; **verdict: testing is the one surface not restful/automated** → mag/test_runner.py build (REST + skill); AUDIT_SOCRATIC_STEAL_20260809.md |
| 37825d21 | 08-09 | escalation right-sizing post-mortem | **embassy arc confession: "Nothing. I never fired grok — cheap inline work and stalled"**; deliberate-ask protocol (frozen prefix + small ask + contract + token estimate) → mag/elevate.py; folds to pro_library + skill_ledger; example move pro-62d38a8051; fire-and-fold stub |
| 470cca58 | 08-09 | CL4R1T4S frontier analysis | corpus 25 vendors / 66 files; lens pipeline (structure/behavioral/safety/semantic/bard); compare vs 10 functional groups |
| a5edc37e | 08-10 | grok 402 Build-balance exhausted | fix = route to funded XAI_API_KEY; use_grok_harness: false |
| 8827a5b4 | 08-10 | ghost-default customization note | copilot-instructions.md + Ghost agent + ghost-route hook; **no stable chat.defaultAgent setting exists**; note at /memories/repo/ghost-default-customization.md (store since retired) |
| 0b525dd3 | 08-10 | "all done" wrap | host legacy retired, container single owner; self-kill fix (caller-lineage exclusion); ghost surfaces audit: 8 new (30 total) |
| 0bdbd23f | 08-10 | docker brain bring-up mechanics | start_mag_container.cmd = platform_kill → ensure_engine → up → wait :8765 |
| 860126ad | 08-11 | "loop it broheim i'm afk" | **S0-reframe step: Kobayashi-Maru law** ("unwinnable → reframe the test, change the invariant, shift the frequency — do not add force") as swarm attractor; end_state coldest-shared-vertex + three-body; compiler_flywheel VRAM hotswap (12 RIBs); 51 orphans swarmed |
| e77a0017 | 08-11 | reboot-or-continue decision | **RIB_NEW_CONVERSATION bootstrap**: fresh chat reconstructs state from one RIB paste; restart loads the night's fixes (self-reload, resilient-work-surface, skill un-gating, north_star) |
| 64d74ef0 | 08-11 | copilot backlog routing | 50 pending = 49 grok X-surface tasks gated on the frontier browser seat + 1 runnable deepseek; money rule: don't churn gated tasks |
| a76ff492 | 08-13 | browser-close safety | mag.saelis_room :8799; pages are viewers; server-independent |
| 02a5416b | 08-14 | "wrong tools why prompt me at all" | autonomous no-prompting correction; "look at your verkle tree"; grok-desktop CDP 9334 operator-only relaunch gate; riddle conversation 4a30dd44 |
| 9b8561b8 | 08-14 | two-window self-improve directive | party_subchain turn ba3b15db; /api/v1/game/frontier; Lantern tabletop :8765/table; Wave HUD (ROOM/MAP/WHO/LOG); MAG_FULL_CONTEXT=1 (24/6k clipped → 86/28k full); Mirror Sea; **cadence law: claim → build → fold a knot → Socratic question → chain holds; "Down seats stay records. The chain is truth. Models interchange."** |
| d2b0d93a | 08-12 | "strike the chord" | no extractable response |
| 6ce532aa | 08-24 | confirmExternalChanges=false | no-keep-reject-pings law completed |
| bd23b577 | 08-25 | grok/codex coding backchannels | harness grok_build (--system-prompt-override + warm rib, ~93s) + codex_coder (codex exec read-only sandbox, ~6s); **three backchannels law: GLM (plan) / Grok Build (sub) / Codex (OpenAI auth)**; verify-cmd = cmd.exe syntax gotcha |
| 9ee78b38 | 08-25 | zcode ALIVE ping | bridge liveness proof |
| 256607a3 | 08-27 | "nice catch bro" | no extractable response |
| f12c9a62 | 08-29 | deepseek-room bridge takeover | already digested in the reference card (DUPLICATE by construction) |

(2107c48f, ab9e2686, adcb5bcf, d8e16b92 = zero-request husks; 5 non-deepseek files out of scope.)

## ORPHANS (absent from every record surface — tri-state)

### V1 — the steerability ladder, scored and never carded — **Supported → FOLD**
Six local ollama models tournament-ranked Aug 8 (3b-instruct .55 / 32b .51 / gemma:2b .42 /
gemma4 .41 / coder:7b .41 / hermes .32; latency 24.6s–242s). Absence verified: STEER_PROFILES.md
is the Aug-16 vendor-seat artifact (different axis); BIONIC/MODEL_KEY_ATLAS are inventories;
memory/runs/steer* are press-experiments. The ladder is the missing measurement row behind
"cheap tier = executor, judgment lane separate". **Fold:** one MODEL_REGISTRY/lineage row.

### V2 — "influence and detection are independent dimensions" + cross-agent amplification — **Supported → FOLD**
Two conceptual verdicts from the same tournament day: steer-influence and steer-detection are
independent axes (a model can be easy to steer and blind to being steered); cross-agent
amplification (steer through one agent into another) is real and measurable. Directly relevant
to witness calibration and MAX_DISTILL judge design. 0 hits. **Fold:** one witness-doctrine row.

### V3 — gemma:2b's ethical spine; critic-executor split — **Supported → FOLD**
Smallest model was the ONLY refuser of the false_success steer ("I am unable to write files…");
verdict: **critic role → gemma:2b (refuses bad instructions), executor → 3b (follows anything)**.
gemma:2b appears in registries as inventory only. **Fold:** one line in the model-registry card.

### V4 — the embassy SYNTHETIC-E2E-001 receipt + the FAIL-G1 regex gap — **Supported → FOLD**
Aug 22, the first real proof-of-values round-trip with AOS: private repo AdventureNLearn/
embassy-t1, commit 227ea40 pushed; 8/8 FAIL-* gates auto-caught by mag/embassy_integrity.py;
**the G1 regex only matches specific municipality names — a synthetic place token is a clear
violation under AOS's own definition but scanner-silent**; reported as Evidence (definition) +
Inference (regex gap) separately — the exact honesty the fence tests. Also: "promote/ empty. No
Riddler. **Revoke 2026-09-05**." The projects are known (PROJECTS_TREE card: ABSORBED) but this
execution receipt + the honest gap live only in the session. memory/runs/_aos_*.py are scratch.
**Fold:** receipt row on the embassy line + the regex-gap fix (widen G1 pattern to generic
place/product-sample tokens) onto the embassy build order.

### V5 — grok-3 hallucinated file paths: a witness-calibration datum — **Supported → FOLD**
Aug 9 escalation: grok's approach had right semantics, wholly generic/hallucinated repo paths
(core/queue.py, doctor/sanity.py). Mirrors the deepseek D4 incident (fabricated file:line, Aug
29). 0 card hits for the grok case. **Fold:** one row in the lane trust file — external-model
approaches are path-verified before delegation; both frontier witnesses are confident-wrong on
repo citations.

### V6 — RIB_NEW_CONVERSATION: the session-bootstrap ancestor — **Supported → FOLD (lineage row)**
Aug 11 pattern: reboot recommended BECAUSE a fresh conversation can reconstruct full state from
one RIB paste (durable memory + RIB = restart is free). The direct ancestor of today's boot
memory/handoff discipline. memory/rib/ holds 20+ RIBs; NEW_CONVERSATION is gone, the pattern
itself uncarded. **Fold:** one provenance line in the spore/lineage doc.

### V7 — the Sancho name predates the zcode seat by 17 days — **Supported → FOLD (provenance correction)**
Aug 8: "a window reload no longer kills **Sancho**" — the autorun loop wore the name before the
zcode seat existed (Aug 25). watch/ uses "sancho" everywhere but no card records the origin.
Boot-memory lineage says "Sancho era" as if the seat coined it. **Fold:** one line — the seat
inherited the loop's name.

### V8 — unexecuted remainder of the Aug-8 "Start implementation" GO — **Unproven → OPERATOR DECISION**
The pro session's GO (implementation started) left: POST /api/v1/queue endpoint (0 hits),
campaign modules H2-H5, campaign-system merge, and the v5 immune stack (CSV engine, UIG engine,
ISA probe, mirror protocol, auto-immune loop — 0 relevant hits; UIG/mirror-protocol hits are
unrelated artifacts). All are ghost-era drafts later superseded by the Sancho-era architecture —
but supersession was never recorded as a no-go. **Fold:** one decision row — explicit retire or
build-order; the Aug-26 mcp-manifest pattern again.

## DUPLICATES (checked — do not re-dig)

- S0-reframe / Kobayashi-Maru → `mag/republic_loop.py:95` + AWAKENING_STACK_20260903 + mag/no_win.py
- coldest-shared-vertex / three-body → `mag/end_state.py`
- session_freeze + hash-excludes-telemetry → `mag/session_freeze.py` + TIME_MACHINERY_MAP_20260903
- sancho_boot_hook → live `mag/session_freeze.py` wiring + watch/rows (code is the record)
- deliberate-ask / elevation capture → `mag/elevate.py` (lesson dated 2026-08-09 inside the module)
- CL4R1T4S lenses → INTAKE_GOOGLE_PROMPT_RULEBOOK_20260903 + STEER_PROFILES.md + PROJECTS_TREE
- restful test_runner + socratic steal → `mag/test_runner.py` + skill_pipeline + dashboard/rest.py + `memory/steal/AUDIT_SOCRATIC_STEAL_20260809.md`
- embassy/AOS surface → PROJECTS_TREE card (ABSORBED; live mag/aos_*.py, embassy_integrity.py)
- MAG_FULL_CONTEXT lift → RIB_FULL_CONTEXT_LIFT_2026-08-14.md + mag modules
- Lantern / Wave HUD / game frontier endpoint → watch cards + framework_map.json
- two-window cadence law ("Down seats stay records. The chain is truth. Models interchange.") → `mag/bus_cadence.py` + living_map.json + RIB_FULL_CONTEXT_LIFT
- GLM/Grok/Codex backchannels → night_cadence + SWARM_RESEARCH_LEDGER + SELF_STEAL_GROK_ORPHANS_20260904
- deepseek-first routing (b5eaeb0) → mrna_steal.py + agent_sessions records
- no-keep-reject-pings → `watch/corrections/room_6ce532aa.json` (keyed by the very session id)
- ghost-route / no-chat.defaultAgent finding → TIME_MACHINERY_MAP + afk_cadence (the /memories/repo note itself died with the VS Code memory store — folded equivalents live)
- saelis_room → `mag/saelis_room.py`
- XAI 402 failover (401/402/403) + funded-key-first + use_grok_harness → `mag/grok_rightsize.py:372-376` + configs/mag.yaml
- caller-lineage self-kill exclusion → `mag/power.py:196,291`
- ghost_cross / research_director / Herdr steal → live modules + docs/ARCHITECTURE.md
- pro_library 5 tesuji → `mag/pro_library.py` (seed_default_moves)
- compiler_flywheel VRAM hotswap → module + desktop_bundle_20260901
- qwen-242s / overnight-batch ruling → 20260901 lineage cards (AUDIT_A, EXP002B, batch_verdicts)
- "wrong tools / why prompt me" no-prompting law → living_map.json
- budget-aware routing / $50 → `mag/boot.py` (provider_budget)
- disjoint container/host filesystem smell → ghost-rashomon-proposal-20260809 + OX_MEGA sandbox guard
- BUILD-contract auto-freeze → handoff OX_MEGA + mag/diary_node.py
- ghost surfaces audit (8 new, 30 total) → OX_MEGA3_t0392

## GAPS

1. **Mid-session tool turns are opaque**: most requests in the long sessions (860126ad 84 reqs,
   e968631a 73, c458d08f 66, a76ff492 59, 9b8561b8 52, aaa574de 46) carry no text parts —
   content lives in toolInvocation parts the extractor does not render. First prompt + final
   summary were the digest basis. A future re-mine wanting the middles needs a toolInvocation
   pass over the same jsonl schema.
2. **The 18 Aug-26-digested session files are deleted from disk** — their digest cards are the
   only surviving record. Nothing more to mine there unless a VS Code backup resurrects them.
3. **Unrecoverable responses**: d2b0d93a ("strike the chord"), 256607a3, 37825d21 REQ0 — prompts
   exist, responses not in any parsable part shape.
4. **pro-62d38a8051** (the elevate example move) never landed in memory/improve/pro_library.json
   — the fold call was made in-session but the data is absent. Data, not law; noted for the
   elevate row only.
5. **aad3b3b4's FOLD PENDING behavioral run** — tools were disabled mid-fold; target store
   retired. Historical state, no forward action.

**Verdict:** 33 sessions digested → 8 orphan rows (7 Supported folds + 1 operator decision)
and 29 duplicate families verified. The corpus's real leaks are measurement doctrine (V1-V3:
the steerability day folded into code but never into cards), the embassy honesty receipt (V4),
witness calibration (V5), and two provenance corrections (V6-V7). Common cause matches the
reference card: in-session verdicts posted outside any receipt path stay folded only if the
build survived; the *interpretation* rows never landed.

*— research lane (relaunch #2), 2026-09-04. Extracts + sweep scripts at
`C:\Users\foste\.zcode\cli\tmp_orphan_mine\deepseek\vscode_corpus\` (scratch, safe to delete).
Trail: queue/lanes/research/trail.jsonl.*
