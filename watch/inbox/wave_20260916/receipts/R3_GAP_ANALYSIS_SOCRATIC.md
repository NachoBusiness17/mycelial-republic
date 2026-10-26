# R3 — PROGRAM GAP ANALYSIS, SOCRATIC EXPANSION (2026-09-16)

Wave: wave_20260916 · Lane: R3 · Receipt-first, appended as investigation proceeded.
Method: every "current state" claim below was verified from repo bytes on 2026-09-16 (file mtimes, greps, live test runs, `gh auth status`, `git remote -v`) — not from memory or other receipts' claims. No git writes. No paid APIs. One local pytest run (`tests/test_wow_world.py`, 12 passed, 0.25 s).
Shape per program: current one-liner (bytes-cited) → target one-liner → GAP as the sharpest question → Socratic sub-questions → cheapest answering act → DOGFOOD (what the fleet should USE of itself, not just build).

---

## PROGRAM 1 — REFEREE CHAIN / SEP-20 DEMO

**Current (bytes):** the chain bones→session→adapter is complete in code — `mag/wow_bones_session.py` (kernel, receipts wow_session.v1), `mag/bones_adapter.py` (16,386 B, mtime Sep 16 13:52), `tests/test_bones_adapter.py` (17 passed per D20 verbatim; re-run green in V1 audition). The two live gates are UNCLEARED: D20 "OPERATOR GATES" — token rotation pending + #game-c-overview 403 permission click pending. The date is real: `CASTLE_TRACK_20260911.md` row 18 — "2026-09-20 · Sep-20 proof wall — the referee"; `BASECAMP_NEXT_20260916.md` line 1 — the demo is "`/bones start` in #game-c-overview — a stranger plays a turn from a phone, gets a byte-stable receipt."

**Target:** a stranger plays a turn from a phone before Sep-20 and the byte-stable receipt is the proof's face.

**GAP (sharpest question):** *Why is the fleet's most important date, four days out, blocked by exactly two human clicks — and why have they not happened since the adapter passed 17 offline tests yesterday?* Sharper still: is the operator gate load-bearing, or has it become the fleet's permission structure for not shipping?

**Socratic sub-questions:**
1. What concretely breaks if the demo boots on the pre-rotation token — is rotation a real security requirement or ritual? (If ritual, the gate is self-imposed and the fleet should say so in bytes.)
2. Is the #game-c-overview 403 a permissions bug or a five-minute Discord UI act deferred five times?
3. If both gates cleared tonight at 22:00, does ANY next blocker exist — i.e., is the chain genuinely phone-to-receipt ready, or do gates hide an untested last mile?

**Cheapest answering act:** operator's 10-minute gate pair (rotate `DISCORD_BOT_TOKEN`, grant channel permission), then `.venv\Scripts\python.exe -m mag.bones_adapter` live boot. Fleet-side half: a lane plays a full session in-channel first — the fleet as stranger zero.

**DOGFOOD:** the fleet should be its own first stranger — play real /bones sessions through the adapter so `memory/runs/wow_bones/` fills with played receipts before Sep-20; the referee should be proven under load by its own fleet, not only by tests.

---

## PROGRAM 2 — RACTOR-SALON PLUGIN

**Current (bytes):** `C:\Users\foste\Documents\ractor-salon\` — own git repo, commit `70e2d89` "ractor-salon v0.1.0", 18/18 tests (P1 verbatim), NO remote (`git remote -v` empty), `gh auth status` this session → "You are not logged into any GitHub hosts." OWNER placeholders still live at `plugin.json:8` and `README.md:64`. The P1 publish checklist (7 steps) awaits operator execution. The showcase salon exists (P2: 10 answers, 25 metered calls, $0, privacy-scan clean; showcase pick = union-alpha T0.2).

**Target:** public repo + release v0.1.0 + catalog PR against `NousResearch/hermes-agent`.

**GAP (sharpest question):** *Why is a finished, scrubbed, tested package sitting one `gh auth login` away from public — and why does the fleet that built it still not use it (P2 imported `mag.research_fanout` in-repo, not the package)?*

**Socratic sub-questions:**
1. Is the wait the human scrub review (real names/paths risk) or just the two OWNER placeholders? If the automated sweep is clean and the review de facto done, the remaining act is 10 minutes, not a decision.
2. The catalog PR is maintainer-reviewed — what actually changes if the repo is public today vs next week? (If nothing: the gate is emotional, not procedural.)
3. If the extraction is not load-bearing for its maker, why would it be for anyone else — should the next concert run through the packaged CLI as its own admission test?

**Cheapest answering act:** P1 checklist steps 1–2: edit the two OWNER placeholders, `git commit --amend` + re-tag (still free while unpushed), `gh auth login` — then the scripted create/push/release list runs itself.

**DOGFOOD:** switch one future salon (next concert's BREADTH movement) to run through the packaged `ractor-salon` CLI instead of `mag.research_fanout` direct. The plugin eats its own dogfood or it isn't a product.

---

## PROGRAM 3 — MYCELIUM CUBE (C17 / CONCERT)

**Current (bytes):** `watch/inbox/physical_computing/receipts/C17_CUBE_INSTRUMENT_PLAN.md` — pre-registered 3-stage kill ladder; stage 0 ≈ $31 electronics-only; line 82: "two-eyes pending; stage-0 spend requires operator word"; line 295: "PROPOSAL until two eyes sign it and the operator funds stage 0." CONCERT001 (closed 2026-09-16, 28 answer cells, 0.15 Lite credits) returned three program changes: concurrent instrumented dead twin from stage 0, SHT31 +$4 promoted to stage-1 required with nuisance-regressor check, rung-2 re-scoped from printed lattice to grown barrage zones. **Byte-finding: grep of the entire `physical_computing/` tree for `SHT31|barrage|concurrent` returns EMPTY — the three amendments exist only in the CONCERT receipt, not in the plan they amend.** The shopping list still carries the pre-concert DHT22 skeptic rider.

**Target:** a signed, amended plan; funded stage 0 ($31–45); a stage-0 noise dataset on the trail.

**GAP (sharpest question):** *Why did the program's first four-substrate review produce three concrete amendments announced as changing the program — yet not one byte of the plan they amend was touched? Is CONCERT001 a revision of the program or a performance about it?*

**Socratic sub-questions:**
1. If the amendments are right, folding them into C17 before stage-1 data closes is a pre-registration obligation, not paperwork — does NOT folding quietly invalidate stage 1's own kill law?
2. Which gate is real: the two-eyes signature (a human review act — has anyone asked the second eye?) or the $31 (money)? The plan treats them as one gate; they are two different conversations.
3. The skeptic rider prices full defenses at ~$45–60 and the concert adds ~$9 — is "$31" still the program's number, or a stale anchor the gate now protects instead of the experiment?

**Cheapest answering act:** $0 — fold the three CONCERT amendments into C17 as a dated amendment section (pre-stage-1), which simultaneously makes the plan signable and the gate honest. Then the two-eyes ask.

**DOGFOOD:** the plan's own law (dashboard heartbeat tile, trail rows, myco-bit as a literal file the fleet reads) cannot run until data flows. The $0 dogfood now: write a synthetic stage-0-format noise JSONL through the trail/tile consumption path, so the pipe that will eat myco-data is proven before the ear is built.

---

## PROGRAM 4 — PHYSICAL COMPUTING PACK (EXTROPIC LANE 2 / HYDRAULIC XOR / ETCH)

**Current (bytes):** `PHYSICAL_COMPUTING_PACK_20260916.md` (25,426 B) is the working doc; §6.8 "Extropic Lane 1: the audit corrected US first"; Lane 2 (metered joules, full ACF curves) = "own ceiling first" and line 242: "canonical-check writers, hydraulic XOR spec — all requeued behind the drain, not abandoned." C18 landed the two-bucket XOR: **BOM $13.04** with pre-registered sim predictions (Appendix B), falsifier target = pack §4.5 (break the Hermes circularity attack: "the sim is its own spec"). Etch path: `DESIGN_ETCH_STONE_ONE_20260916.md` line 146 — "Budget to produce Stone One: $10 (door C, plate only) – $700 (door A, full canon path)"; the waveguide lane already KILLED ("decoration wearing a physics costume").

**Target:** one physical artifact whose behavior the in-MUD sim predicted in advance, then measured — the $13.04 XOR is exactly that artifact.

**GAP (sharpest question):** *Why does the program's own falsifier demand a physical artifact to break sim-circularity, while that artifact's BOM ($13.04) and its pre-registered predictions already exist — and the only missing inputs are two buckets, tubing, and an afternoon? Is the $700 etch path a research program, or a way to defer the $13 experiment that would actually test the fleet?*

**Socratic sub-questions:**
1. Did U3's hydraulic sim emit its numbered falsifiable predictions BEFORE any physical measurement — or are Appendix B predictions still sim-authored and only nominally pre-registered?
2. Extropic Lane 2's "own ceiling first" (measure our joules/op before comparing) — real prerequisite, or infinite regress that hides the absence of any measurement harness?
3. If the physical XOR disagrees with the sim, is there a written law for what happens to "The Clear Pipes" MUD keep — or would a failed prediction be absorbed silently?

**Cheapest answering act:** operator $13.04 + half a day — build the two-bucket XOR and run it against Appendix B. ($0 interim: finish the MUD sim stone so the predictions are readable in-engine first.)

**DOGFOOD:** "games as work" — the fleet plays The Clear Pipes and reads the hydraulic predictions as MUD content; the sim must be a playable keep, not a script, before the physical XOR is trusted to falsify it.

---

## PROGRAM 5 — STATIC ESTATE

**Current (bytes):** D21 DONE — `dashboard/static/estate_walk.lod.html` (683,614 B; zone sums reconcile exactly: 233 nodes / 111 corridors / 1200 stars), main `estate_walk.html` 599,197 B untouched; `dashboard/mud_relay.py` 6,113 B now has `GET /mud/state` spectator (6 s expiry live-verified). Honest D21 note: the .lod.html is LARGER than the original — the win is startup parse cost only. Authority gap: the relay is presence-only (lanterns expire in 6 s; no server-side sim); D21's own next-stone: "Relay v2 (authoritative server-side sim) remains"; blueprint M1 = "the relay graduates from presence to state."

**Target:** an estate with authoritative server-side state (M1), the spectator as a window onto real physics, not a guestbook of ghosts.

**GAP (sharpest question):** *Why does the estate have a spectator endpoint before it has a physics — who or what is being watched, if the only thing that ever moves is 6-second-old ghosts? Is the relay a world or a guestbook?*

**Socratic sub-questions:**
1. Does `POST /mud/state` have ANY live producer right now — is anything actually reporting lantern state, or did every smoke test POST synthetically? (If no producer exists, the spectator watches nothing, and shipping it was UI before infrastructure.)
2. Blueprint scope law freezes M0-only until the demo ships — so is relay-v2 (M1) correctly frozen, and is tonight's spectator work a lawful preview or a freeze violation in the other direction?
3. The .lod.html grew past the original — is the real debt the 683 KB embedded payload, and does stripping lane `events` from the inert block (D21's own shrink note) dissolve the criticism entirely?

**Cheapest answering act:** $0 — point one real producer (a lane heartbeat, or demo-session presence) at `POST /mud/state` so the spectator watches something true; same hour, strip lane events from the .lod.html inert block.

**DOGFOOD:** the fleet inhabits its own estate — bones sessions and watch cycles POST real lantern presence, and the LOD index becomes the fleet's own map of its work rather than a demo page nobody lives in.

---

## PROGRAM 6 — DOCTRINE DEBTS

**Current (bytes), each debt measured tonight:**
- **Memory index fossils:** H1 OPEN — `mag.shared_surface validate` fails: 388 of 443 inbox files unindexed, 84 pointers to missing files (54 historical `/board/` drift), 13 hash mismatches, INDEX root wrong. D24: `memory/biography/cards/` is a frozen 2026-08-07 projection with **no surviving `.card.json` writer**; `bio_card.v1` spec approval-ready, operator gate pending.
- **Sampler kill closure:** refutation filed on tape — pack §6.1: rho +0.327 replicated "past the +0.3 refutation line… the salon is a diversity pump, not a quality sampler"; U5: "We filed the refutation anyway"; D23: 11 of 17 witnesses still tried to SAVE the analogy, and no doctrine-surface closure receipt exists anywhere — the kill lives in lane artifacts only.
- **Kill-list memo unmoved:** `attic/kill_list_20260908/MANIFEST.md` ("Moved, not deleted. Reversible") — 8 days untouched; D24 then wrote a SECOND memo (`TRIAGE_MEMO_20260916.md`, 52 KILL-ready, 22 `_`-probe files named "safest first bite") — "No deletions performed." Two memos, zero executions since Sep 8.
- **34 failing tests unmoved:** AGENTS.md:27 census (2026-09-14: 1305 passed / 34 failed / 9 skipped, ~12 min); no newer census, no fix lane, no owner. SHERPA corrected the prose lie ("39 deterministic green") but the 34 failures themselves have no lane.

**Target:** doctrine matching bytes — index validate green or honestly bounded; sampler analogy closed in doctrine, not just on tape; one executed kill bite; the 34 owned.

**GAP (sharpest question):** *Why does the fleet keep writing NEW audits of its old debts (D24 is the third module triage; H1 the second index repair) faster than it executes any single one of them? Is auditing how the fleet avoids acting — is a receipt about a debt a way of not paying it?*

**Socratic sub-questions:**
1. What would clearing the 22 `_`-probe kills actually cost today — if the answer is "one script + one pytest run," what precisely prevents it?
2. Sampler kill: is the missing closure receipt blocking anything real, or is the analogy already dead in practice (does any lane still get chosen by decorrelation)? If practice already moved, the receipt is a gravestone, and gravestones are cheap — write it.
3. The 34: has anyone READ them since Sep 14? Are they 34 distinct bugs or 3 bugs wearing 34 test names? (Nobody knows, which is itself the debt.)

**Cheapest answering act:** execute D24's "safest first bite" — archive-first the 22 `_`-probe files (reversible per kill-list law), run the touched test files, file ONE closure receipt. One lane, one hour; the first doctrine debt actually paid since Sep 8.

**DOGFOOD:** make `mag.shared_surface validate` a standing daily patrol line in the existing 08:00 task (`scripts\register_improve_task.ps1`) — the index confesses or heals daily; promote the D24 probes from one-off scripts to a census command the fleet runs itself.

---

## PROGRAM 7 — WORLD BUILD (BLUEPRINT M0–M5)

**Current (bytes):** `watch/inbox/WOW_CLONE_BETA_BLUEPRINT_20260916.md` — M0 bones-world skeleton, M1 authoritative room server, M2 player files, M3 zone/enemy/loot, M4 /play Discord, M5 fifty-wide playtest; scope law line 57: "Scope freezes through Sep-20 (the witness's law): M0 only until the demo ships." Byte state tonight: **M2 DONE** (`mag/wow_player.py` + tests, audition green, 24 passed; falsifier "state survives restart byte-identical"). **M0 LANDED BUT UNCLOSED:** `mag/wow_world.py` (16,902 B) + `tests/test_wow_world.py` (7,445 B) appeared 16:52 tonight; my run: **12 passed in 0.25 s**; W1 receipt's verification steps still unchecked — the receipt was never closed with final numbers.

**Target:** M0 closed on its falsifier (same seed + same moves → byte-identical receipt), then a hard STOP until the demo ships.

**GAP (sharpest question):** *Why did the fleet build M2 while its own blueprint freezes scope at M0-until-demo? Either the freeze law is real and M2 is a violation, or the law is not real — and then what else written in the blueprint is fiction?*

**Socratic sub-questions:**
1. Does `test_wow_world.py` actually assert M0's falsifier (byte-identical replay of same seed + same moves), or does "building" mean the core claim is still unverified?
2. Was M2 built because it was unblocked while M0 waited on editor passes — a dependency inversion worth writing down, or scope drift worth stopping?
3. What exactly remains between tonight's 12 green tests and a CLOSED W1 receipt — is closing the receipt itself the whole remaining work?

**Cheapest answering act:** $0, tonight — run the M0 falsifier explicitly (same seed, same move tape, twice; diff receipt bytes), then close the W1 receipt with the real numbers. That converts "building" into "done-or-defect" before midnight.

**DOGFOOD:** the fleet plays its own world — sessions run through wow_world rooms, receipts land in the trail; and the W1 pattern already proven (union-alpha drafts graded by fleet-run tests after grade-B self-checks were caught wrong-signed) IS the dogfood: the fleet verifying its own generators instead of trusting their self-reports.

---

# MASTER QUESTION LADDER (all programs)

1. **Demo:** why is the Sep-20 proof blocked by two operator clicks, four days out, when the code chain passed 17 tests yesterday?
2. **Salon:** why is finished v0.1.0 one `gh auth login` from public — and why does its own maker still not run salons through it?
3. **Cube:** why were the concert's three amendments announced as changing the program, yet not folded into the plan bytes they amend?
4. **Pack:** why does the $13.04 falsifier-executing artifact wait behind a $700 path and a sim that already made its predictions?
5. **Estate:** why does the estate have spectators before it has physics — what is the relay actually for?
6. **Doctrine:** why does the fleet audit its debts faster than it pays any of them — is a receipt about a debt a way of not paying it?
7. **World:** why did M2 ship while the blueprint freezes at M0-until-demo — is the scope law real, and if not, what else in the blueprint is fiction?

# THE 3 QUESTIONS THAT COLLAPSE THE MOST OTHERS

- **Q-A — THE FOLD LAW:** "Why do verdicts (CONCERT amendments, sampler kill, triage memos, bio_card spec) get FILED but never FOLDED into the canonical bytes they revise?" — collapses #3 entirely, #6 entirely, half of #2 (P2's own salon concluded "publish protocols; keep keys private" — the fleet hasn't even published), and warns #7.
- **Q-B — THE GATE LAW:** "Is the fleet treating operator-gated human acts (two clicks, one login, one signature, $13–$31) as done-adjacent, and building downstream of them instead of clearing them?" — collapses #1, #2, the funding half of #3, and all of #4.
- **Q-C — THE FREEZE LAW:** "What is actually gated by Sep-20 — and is this week's spend elsewhere a violation of the fleet's own scope law, or is the law already dead?" — collapses #5 and #7, and orders #1 against everything else.

# SINGLE NEXT ACT PER PROGRAM

| # | Program | The one act |
|---|---|---|
| 1 | Referee/Sep-20 | Operator clears the two gates (rotate token + channel click); a fleet lane then plays stranger-zero in #game-c-overview. |
| 2 | ractor-salon | OWNER edits + amend + re-tag + `gh auth login` (10 min); the scripted publish list runs from there. |
| 3 | Mycelium cube | Fold the three CONCERT amendments into C17 as a dated amendment ($0, pre-stage-1) — then ask for the two-eyes signature. |
| 4 | Physical pack | Buy the $13.04 BOM; run the two-bucket XOR against Appendix B's pre-registered predictions. |
| 5 | Static estate | Wire one real producer into `POST /mud/state`; strip lane events from the .lod.html inert block. |
| 6 | Doctrine debts | Execute the 22 `_`-probe archive bite + one closure receipt (one lane, one hour, reversible). |
| 7 | World build | Run the M0 falsifier explicitly tonight and close W1 with real numbers. |

**Dogfood line, one sentence:** the fleet should USE its own outputs this week — play through the adapter, run a concert through the package, feed mock stage-0 data through the cube's tile pipe, play the Clear Pipes keep, lantern the estate with real lane presence, let the validator patrol daily, and play its own M0 rooms — because every program above contains a thing built for others that its builder has never once consumed.

*— R3 closed 2026-09-16. All claims bytes-cited; tests: 12 passed (`test_wow_world.py`, this session); no git; no paid APIs.*
