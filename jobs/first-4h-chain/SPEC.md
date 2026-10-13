# SPEC — first-4h-chain

**Salon:** `memory/runs/salons/long_horizon/SALON_ARTIFACT.md` (bind, do not reinvent)  
**Job ID:** `first-4h-chain`  
**Contract:** `jobs/first-4h-chain/seat_contract.json`  
**Law:** files-not-chat · disk supervisor · no new process

## Goal

One 4h-class chain as **bounded cages** under this job ID. Prove the seat contract on grok+codex before adding seats. Fails fast. Uses organs already on disk (`launch_vast.py`, covenant, blade rails, fuel_feed, verkle).

## Invariants

- Frozen spec at hour 0 (this file + JSON). Chat is heat.
- Each cage writes `trail_core_N` atomically: completed, hashes, tests, failures, budget, **one** next action, **resume_command**.
- Next seat loads contract + SPEC + last core only.
- `resume_command` is the driver interface.
- Covenant from `state/vast/covenant.json` (blade ≤ $0.12/hr, 4h lifetime, floor as filed).
- Single-flight: one cage in flight.

## Forbidden

Host `python main.py lab`. New supervisor. Chat as DNA. All-frontiers every prompt. Re-ask blocked machines. Buy under floor. Start cage n+1 without trail_core_n.

## The chain

| Cage | Name | Exit |
|------|------|------|
| 0 | scaffold (this beat) | JSON parses; SPEC exists; trail_core_0 contains literal `resume_command` |
| 1 | blade launch+gate | probe+instances; one blade at/under cap **or** stand-down FILE if no legal deal |
| 2 | bootstrap | qwen3:8b (or blade contract model) serves; one smoke chat |
| 3 | drain batch | one bounded drain of real fleet prompts (not /health) |
| 4 | receipt+knot | hashes + trail core + knot/receipt on disk |

## Acceptance commands (cage 0)

See `seat_contract.json` → `acceptance_commands.cage_0`.

## Checkpoint / handoff

Schemas live in the JSON. Trail cores: `jobs/first-4h-chain/trail_core_N.md`.

## Resume

```
.\.venv\Scripts\python.exe state\vast\launch_vast.py probe
```

That string is `resume_command`. Firing it starts **cage 1**.
