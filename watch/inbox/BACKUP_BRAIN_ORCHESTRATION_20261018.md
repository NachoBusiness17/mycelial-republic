# THE BACKUP BRAIN - ORCHESTRATION SPEC (byte-audited, 2026-10-18)

**Source:** the operator's April post (X @NachoQuixotic, the blackout vision;
URL as sent in the operator's message; sibling-typed today as
`watch/inbox/THE_BACKUP_BRAIN_MANIFESTO_20261018.md`) + the operator's order:
"help me build it with the mosaic i've cobbled together. I know the pieces fit
just missing the orchestration level and how to use it. self steal our
intentions via vislab and how they can now be incorporated and not handwaved
no sacred cows."

**Method (no sacred cows):** every organ the vision needs was byte-checked
(`tools/backup_brain.py inventory` - the audit is a command now, not a
narrative). Sibling-card claims that failed the byte check are named. Nothing
is incorporated on prose alone.

## THE LOOP (the orchestration level, as a state machine)

```
NOMINAL --(internet dies)--> SEVERED --(any uplink)--> RESYNC --> NOMINAL
   |                            |                        |
   | local inference            | local model + archive  | merge outward
   | still answers              | keeps working          | what was learned
   v                            v                        v
FACE: Room/Globe/Vislab     QUEUE: tasks accumulate   SYNC: FTS refresh +
BODY router: phones idle    (WAL exists, SEVERED      chain extend + rail
+ GSTD beacon earn          consumer MISSING)         settle (rail live)
```

The v0 orchestrator is `tools/backup_brain.py`: `inventory` (the audit),
`drill --severed` (proves the blackout half runs TODAY: local model via
mag.ollama_policy, chain tip, WAL import - zero WAN by design), `drill
--reconnect` (proves the merge surfaces are fresh: git, corpus FTS, served
field). Drills write only their own ledger (`logs/backup_brain_drill.jsonl`);
a drill that could break the thing it drills is not a drill.

## THE CROSSWALK (April vision row -> byte-verified organ -> verdict)

| April vision | Organ (byte-checked) | Verdict |
|---|---|---|
| "a smart AI program saved on it" / local quantized model | `mag/ollama_policy.py` + the gemma battery | EXISTS - drill proves it answers |
| "knows your way of thinking... from a few words" | `state/palace/` person-models, `memory/rib/`, biography knots + checkpoints (`memory/biography_v2/checkpoints_v2.jsonl`) | EXISTS - calibration-from-few-words is the palace read; no new model needed |
| "learns from tesujis (pattern-breaks)" | `corpus/steal/` + TESUJI_* intake cards (6) + the intake chain | EXISTS as corpus - **the training pipeline does not exist** (struck cow, see scorecard) |
| offline task queue | `mag/wal_queue.py` (SQLite WAL, leases, dead-PID reaper, hypothesis dedup) | EXISTS - but **no SEVERED-mode consumer** runs it offline (MISSING, v1 build) |
| "phone quietly uses idle compute... Wallet-as-Node" | `tools/gstd_beacon.py`, `tools/gstd_drain.py` (v8 relay live per memory), gstd-desktop as 5th network node | EXISTS on the rail - beacon-to-task-routing not yet wired to the body router |
| phones join as bodies | `mesh_router.py` (REPO ROOT - routes to bodies via pocket_mcp, battery>30%/RAM gates), empir3 bridge (paired to operator account), `watch/inbox/PHONE_RELAY_20260924.md` | EXISTS - zero phones enrolled as bodies TODAY (the routing table is ready, the fleet is not) |
| "when Starlink comes back, shares what it learned" | sync surfaces: git, corpus FTS (`tools/corpus_fts_rebuild.py --check`), served field feeds | PARTIAL - surfaces fresh by dailies; **mesh_router has NO sync verb** (the manifesto card invented one - handwave caught); chain extension IS the merge today |
| consistency proofs | `mag/bintree_v2.py` internals | PARTIAL - **no verify_knot_v2 CLI** (the manifesto card named a tool that does not exist) |
| dual-witness settlement ledger | - | MISSING - "tails.jsonl" was a handwave (watch/steer_field/TAILS.md is steer tails, unrelated) |
| "earnings automatically buy real physical gold" | - | MISSING - no gold organ exists in mag/ or tools/ (grep audited); prose, not code |
| "backup brain for humanity in our pockets" (the face) | `dashboard/static/room.html`, `smith_globe.html`, `vislab.html` | EXISTS v0 - the orchestration's face is already the estate's own map; Room v1 write path owed |

## SACRED-COW SCORECARD (struck, not fenced)

1. **"trains a super-smart free AI on tesujis"** - STRUCK as stated: no
   training pipeline exists; the corpus feeds PROMPTS today (retrieval),
   not weights. Honest restatement kept: the tesuji mine is real and
   growing; a LoRA/QLoRA arm on it is a named future build with a
   falsifier (perplexity/behavior delta on held-out tesujis), not a claim.
2. **"earnings automatically buy physical gold"** - STRUCK until an organ
   exists: no code path moves GSTD to gold. Building it = a drain-rule
   carve with an on-chain receipt; until then the manifesto carries it as
   aspiration only.
3. **"helps billions wake up to more independent thinking"** - STRUCK:
   unfalsifiable, per the hardy-spores law. Kept falsifiable cousin: count
   enrolled bodies and served answers (the beacon ledger can count).
4. **"Starlink"** - struck as branding; the design is transport-agnostic
   (any uplink; the drill only knows SEVERED vs RESYNC).

## BUILD ORDER (each row falsifiable)

1. **SEVERED-mode consumer** (`mag/offline_queue.py` over wal_queue): a
   runner that drains the WAL with network=None policy. Falsifier: severed
   drill completes a task end-to-end with WAN untouched.
2. **Enroll the first body**: the operator's phone (empir3/pocket_mcp)
   answering one mesh_router `route --shape` for real. Falsifier:
   `mesh_router map` lists >0 live bodies that are not this desktop.
3. **verify CLI** over bintree_v2 (`tools/verify_chain.py`): consistency
   proof from checkpoint n to tip. Falsifier: detects a tampered leaf in test.
4. **Room v1 write path**: seats leave notes the Room renders (the chat the
   operator keeps asking for). Falsifier: a note written by a drill appears
   on the floor without hand-editing HTML.
5. **Gold carve** (operator decision): a drain split X percent to a gold
   desk, receipted on-chain. Falsifier: a drain row whose memo splits and a
   vault credit in the same settlement window.

## TODAY'S DRILL (what the audit found live)

Run: `.venv\Scripts\python.exe tools\backup_brain.py inventory` /
`drill --severed --reconnect`. Daily: MagBackupBrainDaily 08:55
(`scripts/backup_brain_daily.ps1`). Four missing organs stand named; the
loop's every other beat has a byte behind it.
