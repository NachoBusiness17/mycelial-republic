# RESIDENT STEERED WORKERS v0 — the gophers stop being re-prompted (2026-09-02)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: ~5 resident steered workers (bounded beat loops on byte-stable cached genome prefixes, steer-packet task channel) eliminate the cold-prompt waste, ~90% of prompt cost never recurring — UNPROVEN (design doc citing existing bones; no W1–W5 run receipts in card) · falsifier: workers launched and measured prefix hit-rate/beat economics fall far short of the ~90% claim, or drain_worker + steer_bus don't compose as tabulated
*Operator: "why are we reprompting gophers every time — wouldn't it be cheaper to launch ~5 bounded workers
you just pass shit to, using our steering mechanisms and riblang/memweave." Self-stolen bones below.*

## THE WASTE (measured shape)
Every dispatch today = cold prompt: full genome + context re-sent per task. The canon's prefix-exactness law
says the opposite: stable contract cached, only the delta travels. We cache-mine the lanes for everything
EXCEPT our own gophers.

## THE DESIGN (each bone already exists)
| Bone (exists) | Role in the resident worker |
|---|---|
| scripts/container/drain_worker.py (bounded beats, WORKER_BEAT, pidlock, worker.off) | the worker BODY: bounded beat loop, atomic heartbeat, container-safe |
| steer_bus (landed today: closed enum, ttl, anchor, receipts) | the TASK CHANNEL: steer packets (nudge/clamp/purge/route), no free text |
| night_cadence.py (4-task pidlocked cadence) | the MULTI-WORKER precedent: N bounded loops, one host |
| RIB / memlang | the TASK FORMAT: deterministic task description; memlang anchors as compact organ references |
| verb_genomes L0 contract | the CACHED PREFIX: byte-stable genome + constitution, hits provider cache every beat |
| covenant.json + water ledger | the BUDGET: beats cost pennies; caps enforced at the gate |

## THE LOOP (one worker, one beat)
1. read steer queue (watch/steer_bus queue or /board steers.jsonl) — closed-enum packets only
2. resolve packet -> verb genome (L0 cached prefix + verb pack) + target tail
3. execute bounded (timeout, max tokens)
4. sign: artifact + room receipt + steer_bus ack nonce
5. sleep; heartbeat to state/ worker_heartbeat.json

## THE FIVE (per operator)
W1 wing-miner (read-only AppData dig, corrections ledger) · W2 museum-curator (manifest + plaques) ·
W3 burn-guard meter (post-recreate only) · W4 canon-librarian (L3 packs, wash receipts) ·
W5 socratic-gate scribe (two-counter ledger). All deepseek pennies; all steering via packets; all receipts signed.

## ECONOMICS (spore ledger math, applied)
A 2K-token stable prefix at 100 beats/day on deepseek auto-cache (~0.1x reads): ~90% of prompt cost
never recurs. The prefix IS the spore; the steer packet is the rain; the beat is the germination.

## LAWS
- One writer per queue file (pidlock). No config edits without the covenant mutex. Worker.off pauses all.
- Prefixes are byte-stable (no timestamps — the spore cell wall). Steer packets carry ttl + anchor.
- Visible socratic: one [SOCRATIC] block per reply, then the answer. Repetition of a block = a bug.


## THE TIERED LANGUAGE LAW (operator, 09-02: "i read english they do not; cheap and full fidelity = baremetal")
- HUMAN SURFACE: English, legible, glossed — reports, museum captions, room posts the operator reads.
- WORKER SURFACE: baremetal — memlang anchors, RIB task packets, event.v1 kinds, steer packets, hashes.
  Cheap (compact = few tokens), full fidelity (canonical encoding is lossless), byte-stable (cache-friendly).
- TRANSLATION: deterministic compile/decode at the boundary only (riddler compile, memlang anchors, surface render).
  English is never the wire format between machines; baremetal is never shown to the operator unglossed.
- The spore ledger's rule, restated: sporulate only what you can canonically encode — the baremetal protocol
  IS the canonical encoding. English prose is the vector for mutation; it rides surfaces, never wires.
