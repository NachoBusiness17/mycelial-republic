# FLEET MIX LAW — 6% frontier, 94% mass · 2026-09-22

_Operator's doctrine, naval frame: "if we could get 6% frontier running with 94% of our
actual fleet." The U.S. Navy keeps ~290 deployable combat vessels — few, exquisite —
where WWII peaked near 1,200 mass-built hulls; a numbered fleet runs 50–70 ships.
Ours: a numbered fleet is a fifty-wide wave, and the mix below is now law._

## The law

1. **≥94% of any wave's lanes run on the mass tier** — deepseek-flash, GLM flash,
   ollama local. Mass is the fleet; receipts say it can carry: a full DeepSeek day =
   **$0.43**, 1,798 requests, 95.7% cache-hit ratio, zero missed hours.
2. **≤6% of lanes — and ≤6% of spend — may be frontier tier**, and frontier seats are
   summoned only at NAMED GATES: referee on contested adjudication, fold-verification
   on wave synthesis, anything the smith chart cannot meter with bytes.
3. **The frontier allowance lives inside the $250 iron circle** — 6% ≈ $15 per cycle.
   A frontier seat that cannot name its gate does not launch. The carrier exists for
   gate sorties, not patrols.
4. **Every wave's smith chart reports the mix** (mass vs frontier lanes, cost per
   lane-tier) — the cockpit line rides the cost-ledger ingest on GO.
5. **Surge is the shipyard:** 195 GB of local weights (ollama + LM Studio) = wartime
   hull production at zero marginal cost; Kev-0.8B fine-tune = the escort-carrier
   program (mass-produced hulls that hold a station alone).

## Today's honest mix (baseline for the law)

- Sept 21 fleet tasks: 72 created, steady 2–4/hour, spike 11 at 19:00Z — the wave.
- Frontier spend: **$0.00** — the referee GO is still unspent; the carrier never left
  the pier. Mass carried 100% of the night: the 50-wide lift is pure mass tier.
- So "6% frontier" is a cap and a target for where frontier seats EARN their keep —
  not a floor to fill. First lawful sortie: the tiebreak referee (one carrier, one
  gate, still owed since yesterday).

## Verification receipt (the "bug?" question, closed)

Swarm-key usage = estate task fleet, confirmed: 72 tasks on the day ≈ 1,798 API calls
(~25 per agentic session), hourly shape matches task creation 1:1, 95.7% cache-hit
matches rolling sessions on stable prefixes. The 62 "unlabeled" records carry their
provider inside `cmd` (`--provider z_ai --model glm-5.3`), not as a field. Hygiene fix
owed (one line): stamp provider top-level at task save so mix queries don't re-parse
command lines.

---
_Filed by the ZCode seat, 2026-09-22. Naval frame: operator. Numbers: billing exports +
5,415 task records + tonight's smith chart._
