# DOGFOOD — MCP sense selection salon (2026-09-04, 11:00 window)

**Operator order:** "this mcp server thing needs to be dogfooded." Fired same hour on the
open Lite window. Witnesses: deepseek-pro substantive + one secondary; cerebras/together
honest-down (reasoning budget). Thread: `salon_mcp_dogfood_20260904`. Inputs byte-grounded:
INTAKE_MCP_AWESOME (3,482 servers / 59 categories), SOCRATIC_MCP_BRIEF (3,838 total, 9 live),
lane charter whitelists, MCP_MANIFEST_SPEC (drafted today from the Aug-26 GO).

## THE THREE PICKS (deepseek-pro base, manager concur)

1. **MONITORING/OBSERVABILITY (Prometheus- or Grafana-class MCP)** — not a new sense, a
   PROPRIOCEPTIVE upgrade: the fleet feeling its own pulse. Powers: monitoring weak spot +
   flight-recorder v0 + per-lane quota/latency/kill-switch visibility. Adoption test:
   10-min load test on a lane, query per-lane p95 via the server, auto-ticket >2s.
   Ties directly to the usage-meter organs (nightly sweep) — this is that, real-time.
   **Tri-state: Supported as need (weak spot charted); Unproven as server choice (unnamed vendor).**
2. **AGREEMENTS & COORDINATION (signed-agreement / hash-locked lease MCP)** — the whole
   category we lack. Cross-lane handoffs currently ride trust; this gives cryptographic
   receipts for resource leases (e.g., mag borrows cloudbase storage for 1h, lease enforced,
   violation = kill signal). This is the ENFORCEMENT BACKBONE the MCP_MANIFEST_SPEC's quota
   gates need — and it converges with our own chain doctrine (signed receipts, no trust).
   Note: implementations in the wild skew crypto-flavored; the SENSE is right, choose a
   signer that fits loopback law. **Tri-state: Supported as gap; Unproven as pick.**
3. **TIME-SERIES PERSISTENCE (InfluxDB/Timescale-class MCP)** — memory for stateless
   senses: rolling cache of fetched URLs/image hashes, TTL eviction, "no re-fetch within
   1h" manifest rule. ECONOMICS: 92-97% of our tokens are context re-feed (measured
   today) — a fetch-cache attacks the same waste class on the network side. **Tri-state:
   Supported as economics; Unproven as implementation.**

## THE SELECTION RULE (anti-sprawl)
**One-Request-One-Receipt, Three-Gate approval:** a lane submits a structured SENSE REQUEST
to the manifest server (lane, proposed sense, justification, adoption test, expiry) →
gate 1: manifest spec check (epoch-pin + quota field) → gate 2: a REAL task proves it
within its TTL (no task, no adoption) → gate 3: kill-switch test passes (the lane can
revoke the sense cleanly). Senses expire; nothing joins a whitelist forever.
**This extends the MCP_MANIFEST_SPEC — route the rule into it as an amendment.**

## ANTI-SPREE (the not-adopt)
Popular-but-rejected: external-comms servers (Slack/Discord/email relays) — deliberately
absent under loopback law; the room.jsonl + surfaces are the comms organ. Revisit only if
an operator arc demands outbound. (Secondary witness's invented "vision-object-detect"
server also rejected — unverified existence; proxy-validation rule.)

## ROUTE
- Windowed behind manifest-spec wiring: monitoring (1) + time-series cache (3) first —
  both attack measured waste; agreements (2) docks to the chain doctrine when a lane
  actually needs a lease (first real cross-lane borrow).
- Amendment (selection rule) → MCP_MANIFEST_SPEC.md.

*Filed by zcode-manager; salon witnessed; operator rules. $0 coordinator, free-window lanes.*

## ECONOMIST STAMP (2026-09-04 ~19:0xZ — receipt-002)

- **"$0 coordinator, free-window lanes" (footer): Disputed as a blanket $0.** deepseek-pro
  is a paid lane and answered substantive on this thread — the same day's salon fold
  admits the honest form: "paid witnesses joined legitimately (deepseek-pro verdict
  step)." **Supported only as "$0 coordinator"**; total witness burn is unmetered on
  this card — **Unproven**. FIX: salon cards should carry a witness-cost line
  (lane + paid/free per witness) so $0 claims stay meter-grade.
- **"92-97% of our tokens are context re-feed (measured today)": Supported, double-metered.**
  Seat db today: 98.1% (5.3 paid) / 94.8% (5.3-flash) cache_read share; receipt-001's
  92-97% lane figure stands. The waste class is real on both meters.
- **Pick 3 economics (time-series cache attacks the same waste class, network side):
  Supported as analogy.** No $ figure claimed; the token-side waste is metered above,
  and re-fetch is the same shape (paying again for what you already held). The
  adoption-test gate (Three-Gate rule) is the right cost control — a sense that cannot
  show measured savings within its TTL dies by its own rule.
- Picks 1/2 make no $ claims; their tri-states (Supported-need / Unproven-pick) stand
  as filed.
