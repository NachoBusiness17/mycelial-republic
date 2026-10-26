# GSTD INTERNAL ECONOMY LIVE - 2026-10-12 (Phase 4 babystep 3 + the operator's economic law)

**The operator's law:** "use our rewarded currency internally to then create the ecosystem - a common economic principle." He's right, with one protocol truth locating the design: TON gas can never be paid in GSTD (TON chain-level). So the internal economy runs in GSTD **off-chain**, and the chain is touched only to net out in batches - the layer-2/exchange pattern.

**Built and dogfooded this rung:**

- `tools/gstd_accounts.py` - the internal GSTD economy: append-only ledger (accounts.jsonl), credit / statement / claim subcommands. Zero network. The internal currency is free to move.
- The drain rewired: per certified run it now **credits 25 GSTD internally** and leaves the rail untouched; the settle fires only when a worker's pending crosses the claim threshold (default 100 GSTD = 4 certified runs). The master's TON bleed per run drops 4x (0.2 -> 0.05 amortized).
- Live proof: consensus-20261012T044454Z (STRUCTURE, 0.8462 vs 0.2969) credited 25 GSTD internally, rail untouched, statement shows DESKTOP earned 25 / pending 25 / on-chain 100.

**The economics:** work -> internal GSTD (free, instant) -> claim at threshold -> one gated settle nets the batch on-chain -> reputation accrues on-chain either way. The reputation organ (on-chain) and the accounts ledger (off-chain) are the two layers of the same currency: reputation is the HONOR leg (on-chain, immutable), accounts is the MONEY leg (internal until claimed). Workers pay their own claim gas from their TON share - the master stops bleeding.

**The claim ladder when a worker crosses threshold:** one gated settle with bonus = the full pending amount; the pool pays the GSTD; the worker's TON share covers its own claim gas; the master's TON balance stops being the bonus gas source entirely at scale.

**Falsifier:** the internal economy claim dies if the accounts ledger diverges from the sum of certified runs (auditable: accounts.jsonl rows vs DONE/ receipts), or if a claim settles more GSTD than the ledger shows accrued.
