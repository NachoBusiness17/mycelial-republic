## Five ordered implementation steps

1. `mag/duel_ledger.py` (new): a pure query API over the ledger. `fold(ledger_path) -> dict[family][shape] -> counts` reads every row of logs/duel/duels.jsonl, classifies shape from the ask_id prefix (adv, schema, plan, code, grade) with an explicit prefix table, remaps winner through the swap field, and returns wins/losses/ties/unparsed per family per shape. Pure function of file bytes; no state. Tests land with it (fixture ledger of 3 rows: A win, B win, TIE).
2. `tools/router_derive.py` (new) plus `configs/router_families.schema.json`: derives configs/router_families.json from the fold, stamps provenance (ledger sha256, row count, receipts) and prices from the V9 receipt, and refuses to write if the sha256 already matches (byte-stable, idempotent).
3. `mag/router.py` (new): `pick(shape) -> model_id`. Implements the gate metric below; among gate-passing families picks the cheapest by blend price; on no family passing, returns the configured default family and says why in the return struct.
4. Wire the CLI: add a `route` command to main.py ("python main.py route --shape schema-design") that prints the pick plus the per-family gate table, and append every production pick to logs/duel/router_picks.jsonl for audit.
5. Freshness and drift guards: router refuses entries whose derived_at_ts is older than 14 days or whose prices.as_of is older than 30 days (falls back to the default family and alerts); a weekly probe reuses the existing price-probe tool to refresh as_of.

Dependency order is deliberate: the fold (1) is testable with zero new infra; derivation (2) needs 1; the router (3) needs 2; the CLI (4) needs 3; freshness (5) closes the loop on 2 and 3.

## Gate metric

Per family per shape, from the fold: decided = wins + losses (TIE and UNPARSED excluded; ties tracked separately, unparsed tracked separately). win_rate = wins / decided. The gate clears when decided >= decided_min (8) AND the one-sided 95 percent lower confidence bound (Clopper-Pearson) on win_rate is >= 0.45. Rationale: with few samples the point estimate lies; the lower bound enforces "parity or better with margin for sampling noise", and 0.45 rather than 0.50 keeps a genuinely-at-parity family eligible (a strict > 0.50 bound would gate out families that are exactly as good as the field). Below decided 8 the family is sensing-tier only: it can be fired for data gathering but never auto-picked. UNPARSED above 10 percent of a family's rows is a judge-health alert, not a family verdict; those duels should be re-judged before the gate reads them.

## Two highest risks with mitigations

1. Judge position bias (slot A vs slot B): the ledger carries a swap field precisely so this is checkable. Mitigation: the fold computes per-family slot balance, and pick() refuses to trust a shape gate for a family whose decided sample is slot-skewed beyond 60/40 until more balanced duels land. The judge is also a single point of taste: a second judge family on a sampled subset would let the router detect judge drift.
2. Stale prices flip the ranking: quality-per-dollar is only as good as the price table. Mitigation: prices carry as_of; anything older than 30 days disqualifies cost ranking (not skill ranking); the weekly probe refreshes; the pick audit log records the price used so a bad pick is attributable after the fact.

## Rollback plan

The router is advisory first: pick() returns a struct, callers log to router_picks.jsonl, no automatic dispatch. Rollback is one config flip (router_enable.json false) which collapses pick() to the configured default family (the ledger-proven workhorse). Because dispatch logs every pick with the gate table snapshot, reverting does not lose the evidence of what the router chose and why. If a bad pick escapes into paid work, the ceiling is per-ask cost, and the audit row names the family, price, and gate values to void.

## First test predicate

`fold()` applied twice to the same ledger bytes returns equal dicts (purity), and on the 3-row fixture (A win, B win, TIE) it returns for family A: decided 1, ties 1, unparsed 0; family B: decided 1, ties 1, unparsed 0. Fails immediately if the swap remap or tie bucketing is wrong.
