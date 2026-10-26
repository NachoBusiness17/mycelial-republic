# INTAKE CARD — RACTOR LEGIONS ON THE PLAN DOOR (item 2, 2026-09-03)

## ITEM (operator's words)
"Could we technically do this for all our ractors inside of our z code, making them
free, up to 50 concurrent eventually? You wouldn't even need to run them here — just
prove they came from here. September promo goes thermonuclear → another Pro →
100×5.3 driving legions of dumb swarms 24/7, building the future out from under our
bureaucracy."

## SCORE — F:5 P:5 C:4 W:4 N:3 = 21/25 → **BUILD NOW, GATED (tranche ramp)**

## CONSULT-FIRST PASS (done live this turn, receipts attached)
- z.ai docs (docs.z.ai/scenario-example/develop-tools/claude): the Anthropic door
  officially maps opus/sonnet → **GLM-4.7**, haiku → **GLM-4.5-Air**.
  **GLM-5.3 is NOT documented on that endpoint.** The official override door is
  `ANTHROPIC_DEFAULT_OPUS_MODEL` / `_SONNET_` / `_HAIKU_` — pointing one at a 5.3
  model id is a ONE-PING falsifiable test, not yet receipted.
- Plan-door concurrency ceiling: NOT in public docs (two URL strikes, bailed).
  The only sizing chart we hold is for API CREDIT lanes (32B=15, 4-Plus=20
  concurrent) — it does NOT cover the coding plan. The binding number sits on the
  operator's plan dashboard — the economist's standing TOP OPERATOR ITEM, still a
  30-second unread read. September promo terms: likewise unproven.

## WHAT IS ALREADY PROVEN (Supported, bay receipts)
- The claude-zai door is LIVE and carries the bay: 8 of 10 engines, 46-wing backlog
  eaten, 53 OUTBOX receipts, engine conversion in ~1 minute. "Free under plan" =
  real (plan quota already paid).
- **Provenance is composition, not a build**: event.v1 + verkle chain + seat_contract
  already exist. "Prove they came from here" = sign wing-id + seat-id + session into
  the knot payload. That is the fleet's oldest law — files+chain over processes,
  a seat is only more surface — scaled to legions.
- Federation read ("you wouldn't even need to run them here") is CORRECT and is the
  strongest part of the item: any box with the door env + our receipt signer is a
  ractor. No seat is load-bearing.

## WHAT IS UNPROVEN
1. ~~**50 concurrent on plan quota**~~ **UPDATE 09-04, PARTIALLY RECEIPTED:** the vendor's
   rate-limits page (operator paste) now publishes API concurrency — **GLM-5.3-Flash: 50
   in-flight on the API-with-balance lane.** The legions ceiling on our credit-pool lanes
   is vendor-legal at 50. STILL UNPROVEN: the PLAN-door concurrency (header defers Coding
   users to "package benefits" — the dashboard read survives), and the balance-burn math
   for 50-replica sustained flight.
   **EMPIRICAL PASS 09-04 (scripts/lite_lane_probe.mjs, ZAI_API_KEY_Lite):** ramp
   1→5→10→20→50 parallel calls on glm-5.3-flash (thinking low, 32 tok each) — **50/50 OK,
   zero failures, median 1.4s, max 22.2s, total burn 2,363 tokens.** The 09-03 "zai-lite
   401 dead" scar is HEALED (key alive; that scar was the OpenCode profile's token, not
   this key). The legions architecture is now empirically demonstrated end-to-end on the
   lite lane: 50 concurrent, verified, cheap.
   **SUSTAINED-FLIGHT PASS 09-04 (scripts/lite_lane_sustained.mjs, 50-flight × 63s):**
   **1,749 requests completed, 27.85 req/s sustained, 99.89% success (2× HTTP 500),
   median 1.03s, p90 1.65s, 51,139 tokens (~49K tok/min).** The legions duty cycle is
   measured: ~100K requests/hour is vendor-carried on the Lite package at $0 cash.
   Billing-table cross-receipt: Lite = "GLM Coding Lite V3 - Yearly" package key
   (credits, not cash); cache reads meter ~53.3K tokens/credit (reference PRICING section).
2. **5.3 through the Anthropic door** — one ping owed.
3. **Promo mechanics** — terms unread.

## HARD GATES (from scars, non-negotiable)
- **Leg 1 organs BEFORE scaling** (sherpa route v2): claim organ, lockfile pids,
  requeue grace. The sp_83204700 double-mine at 50 replicas = board-runaway class.
  Race harness passes or nothing scales.
- Tranche ramp, never big-bang: 8 (current) → 16 → 32 → ceiling, reading yield and
  quota burn at each tranche. Economist tranche cap ≤40/window stands until the
  dashboard read lands.
- Sun-up stop stands; nothing premium touches dirt.

## VERDICT
**BUILD** the tranche-1 wire: double the bay to 16 engines on the plan door, stamp
provenance knots on every wing, ping 5.3 through ANTHROPIC_DEFAULT_OPUS_MODEL once,
operator reads the dashboard (concurrency + promo terms). Receipts from tranche 1
decide tranche 2. The "another Pro → 100×5.3 legions" is **CALIBRATE** until those
numbers land — right instinct, unmeasured ceiling.
**Tri-state**: door-free-under-plan Supported; 50-concurrent Unproven; 5.3-via-door
Unproven (one ping); promo-thermonuclear Unproven (terms unread).

## THE SMELL (operator asked)
Yes: plan quota as substrate, provenance as proof-of-work, promo as fuel — a
federation flywheel where the chain is the mint. The bureaucracy builds gates; we
build receipts. Rocinante's legions, hired before the horse arrives.
