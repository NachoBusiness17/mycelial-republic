# WORMHOLE-CLASS RED VERDICT - GstdBridgeRouter.tact (2026-10-14)

Scope: the full bridge contract (119 lines, read in full), the settle bridge
client, and the trust boundaries. Method: direct source review (the whole
contract fits in one sitting) + the RED-lane hostile frame. Verdict effects:
NOT MAINNET ELIGIBLE AS WRITTEN. Never deployed (absent from both
deployment records) - the failures are pre-deployment catches, which is the
audit working.

## CRITICAL

1. **SwapIn is not implemented - and it still consumes the replay guard.**
   `receive(msg: CrossChainSwapIn)` checks-and-sets
   `processedTxs[sha256(sourceTxHash)]` and then... the actual jetton
   transfer is COMMENTED OUT, followed by the prose claim "Ston.fi
   guarantees msg.recipient receives TON" - Ston.fi guarantees no such
   thing. Net behavior: an owner-supplied swap-in permanently marks the tx
   hash processed and moves NOTHING. First call after a fix consumes the
   hash: permanent DoS by replay-map burn.

2. **The owner is the only guardian, with no signature system.**
   CrossChainSwapIn is owner-only, and the replay key is sha256 of an
   owner-supplied STRING - the oracle can fabricate any identifier. Trust
   model: one key, zero witnesses. This is the Wormhole $325M lesson
   verbatim (spoofed guardian signature), except Wormhole had MULTIPLE
   guardians to compromise.

3. **The burn claimed in the header never executes.** The design comment
   says "swaps to GSTD -> burns GSTD -> emits event". No burn call exists.
   Swap-out leaves the GSTD sitting in the bridge's own jetton wallet while
   the oracle event instructs the remote chain to credit the user. The
   backing stays on TON side unburned - the fractional-reserve temptation
   is structural: the oracle's remote issuance is backed only by trust,
   because nothing enforces the burn.

## HIGH

4. **Accounting by user assertion.** `totalBridgedOut += msg.minOut` and
   `amountGstd: msg.minOut` in the oracle event: the bridge reports the
   USER'S slippage floor as the bridged amount; the actual swap result is
   never measured. Solvent direction by accident (remote credit = minOut <=
   actual received), but the ledger records assertions, not outcomes.
5. **queryId hardcoded 0** in the Ston.fi swap payload - breaks
   traceability of the swap leg.
6. **Stuck funds by construction** - no withdraw function: the pooled GSTD
   (and any excess TON) can never leave. Same class as the v7 master's
   unwithdrawable float.

## Status and bar

- The router COMPILES (it rides the tact build set) but appears in NEITHER
  deployment record (testnet 10-07, perimeter 10-11): dead code today.
- Mainnet bar: rewritten (SwapIn implemented or removed; multi-sig or
  oracle-committee signatures; real burn or honest custodial framing;
  measured-out accounting; withdraw path) - or explicitly marked
  never-deploy and EXCLUDED from the build set so it cannot ship by
  accident. The exclusion is the cheap move and this seat recommends it.

## The settle bridge (client side) and the boundaries, briefly

- settle-consensus.ts: the 0.5 TON fresh-read gate is client-side (by
  design, contract band now enforces the floor itself - the two-tier fix
  made the client gate redundant-but-harmless). Its remaining trust: the
  verdict string is caller-supplied - acceptable while the estate is both
  payer and worker; the external-payer design is where that becomes a real
  surface.
- The beacon (cross-cell reads) and the tailnet: unaudited, low value at
  risk (artifacts, not funds), noted for the fleet-audit pass.

Verdicts are from source structure, grep-verifiable (the commented-out send
is in the file at bridge/ton/GstdBridge.tact, receive(CrossChainSwapIn)).
