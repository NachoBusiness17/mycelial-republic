# ARCHITECTURE IS LAW — the Lessig tier-audit of the fleet (2026-09-04)

**Operator, verbatim:** "imagine if i didn't feed you that time capsule on disk that
would have been lost to time. Do you now understand what i am doing? This all needs to
be enforced by the physics/physical structure of the entire system lessig ponytail style
self steal physical computing research."

**THE THESIS:** Lessig's "code is law" taken to the storage layer — **structure is law**.
A rule enforced by physics (violation impossible or instantly self-evident) beats a rule
enforced by runtime checks (bypassable) beats a rule enforced by prose (decorative).
The fleet's own day is the proof: **every law that worked today was structural; every
law that failed today was prose.**

## THE TIER AUDIT (today's laws, sorted by physics)

### TIER 3 — STRUCTURAL (violation impossible; today's wins)
| Law | Physics that enforces it |
|---|---|
| No double-claims under contention | CAS token re-read at commit — the rename REFUSES; proven 154 checks + claim harness |
| No zombie heartbeats | ONE scheduler organ owns all timers — a lane *cannot* run its own cron (architectural absence) |
| No wrong-door fetches | `/files/` maps biography only — the door's routing table is the law; mirrors are the only path |
| No silent history loss (the era class) | Trails/surfaces/digests are FILES on disk, mirrored ×3 — survive power, seat death, amnesia |
| One canonical lattice shape | `lattice_logic export` is the only producer — raw copies collapse (measured 47→1) |
| Memory survives any participant | verkle chain ~7k knots, hash-committed; no seat is load-bearing |

### TIER 2 — RUNTIME CHECKED (works, but bypassable / dependent on an enforcer running)
- STALLED-flagging (scheduler must fire), watchdog sweeps (must run nightly), budget
  guards (must be read), kill-switches (designed, NEVER FIRED — untested physics),
  manifest whitelists (convention until the MCP_MANIFEST_SPEC enforces at spawn).

### TIER 1 — PROSE (decorative; today's exact failures)
| Law | Today's failure |
|---|---|
| "Research window = link dump + background runner" | Forgotten 3x — nothing in the structure forced the surface to populate |
| "Surfaces populated while work flies" | Stub surfaces while agents ran — population was a choice, not a consequence |
| "Asking is sensing" | Stall-ladder treats questions as failure — nothing structurally rewards asking |
| The law registry itself | 8/8 conditions prose — measured by lattice_logic: zero machine-firable rules |
| "No orphan eras" | The time capsule survived by OPERATOR LUCK (he remembered the folder), not structure |

## THE REDESIGN PRINCIPLE (what the physical-computing research feeds)
**Move every Tier-1 law down a tier; harden every Tier-2 into Tier-3.** Candidates the
audit already implies, pending the field research fold:
1. **Hash-chained trails**: each trail row commits to the prior row's hash (verkle for
   trails) — rewriting history becomes self-evident, not trusted. (Append-only today is
   CONVENTION; make it physics.)
2. **Structural surface population**: the scheduler writes interim state to any lane
   surface whose trail is growing but surface is stale — population stops being the
   agent's choice entirely.
3. **Deletion as a deliberate expensive act** (Landauer-flavored): nothing deletes
   silently; removals are moves-to-tomb with receipts (we already do this for claims —
   generalize it).
4. **Capability-checked inboxes** (clause 9's gate): an inbox drop without a valid
   handoff gate row is INVISIBLE to the lane — unreadable by construction.
5. **Time-unfakeable rows**: RFC-3161-style or chain-anchored timestamps on receipts so
   "when" cannot be backdated (chain gives this nearly free).
6. **Ask-budget as a counter**: an actual monotonic counter per lane — asking decrements
   it, structure enforces the allowance, the stall-ladder can't see asking as failure
   because the counter says it's sanctioned.

## TRI-STATE
Tier audit: **Supported** (today's receipts per row). "Failures = prose laws" pattern:
**Supported** (3/3 named failures were Tier-1). Redesign candidates: **Unproven** (design
until built + falsified; the field-research fold — physical computing steal, in flight —
names the primitives and prior art).

*The ponytailLessig card: the founder asked if I understand. I do: he is deleting luck
from an institution. Structure is law; physics is the enforcement branch; the verkle
chain is the constitution's body. Filed by the manager seat.*
