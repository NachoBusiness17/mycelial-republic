# B2-175 ShadowLedger live DataStore leg (2026-09-26)

## Verdict

OWED, future-dated by the brief's own gate. The leg is defined as the Sep-29
run: publish the_mountain.rbxlx and run the two-client crossing plus the
B2-108 same-uid probe against a real DataStore, AFTER the Sep-29 P0 rebuild
gate. Today is 2026-09-26, the P0 rebuild gate has not run, the publish is
operator-gated to the playtest window, and running it early would bypass the
gate the brief itself names. The simulation serialization premise remains
unproven live (verified below). This receipt stages the exact Sep-29 procedure
and the flip conditions so the playtest lane can execute without re-deriving.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_30_shadowledger_live_20260926.md
  Falsifier: "The Sep-29 live run falsifies this verdict if both clients cross
  one portal, stop, rejoin on the 08:28-or-newer build and any 'took the
  portal' row is gone, or if the live service ever re-calls the transform with
  results the stub's model gets wrong (throttles, retries, cross-region
  replication are NOT modeled)." and "Filed as owed: Studio publish +
  two-client crossing on real DataStores."
- watch/inbox/burn_wave_20260926/B2_10_playtest_prereg_20260926.md:9: "Sep-29
  opens with P0 (rebuild gate) before any play."
- watch/inbox/burn_wave_20260926/B2_108_commit_gate_20260926.md:4: "t74
  live-DataStore verification remains open for Sep-29 (B2-175)."
- The serialization premise is still doc-only: B2_30's under-test build stubs
  the DataStore; the archived GlobalDataStore page snapshot 20260311133112 is
  the only UpdateAsync-semantics authority cited; roblox/README.md:67:
  "every append goes through one UpdateAsync on the player+day key". No live
  DataStore byte exists in the tree (repo grep for a live crossing receipt
  returns none; the sim artifacts are the only witnesses).

## Work done

1. Verified the gate chain from bytes: B2-10 prereg (Sep-29 P0 first), B2-108
   (commit gate landed, runtime legs open, names B2-175 for Sep-29), B2-30
   (sim verdict + filed-as-owed live leg).
2. Confirmed the simulation serialization premise is still unproven live:
   only the archived doc snapshot backs UpdateAsync transform semantics; no
   live crossing receipt exists on disk.
3. Staged the Sep-29 procedure for the playtest lane:
   (a) run the P0 rebuild gate first (B2-477 self-feed command line; B2-108
   falsifier (b) checkout-clean check);
   (b) publish the committed build (blob c43fb30663a4c3060f37939fcfa62637aca2a136,
   on-disk sha256 prefix 6eec2f99) into the live universe (B2-478 lane owns
   the publish-path verdict);
   (c) run the two-client same-portal crossing from PLAYTEST.md:23-28 (RMW
   t74 disease probe) with both clients on the 08:28-or-newer build;
   (d) run the same-uid same-UTC-day cross-server double-write probe against
   the real DataStore (B2-30 S4b residual risk closes only when no server
   runs pre-t74 code);
   (e) record DataStore service behavior during the run (throttle, retry,
   transform re-calls) since the stub models none of them.
4. Filed this receipt; LEDGER row appended; QUEUE row pointer landed.

## Falsifier

This OWED verdict is inverted if any of the following holds: (a) a receipt
dated on or before 2026-09-28 claims a live DataStore crossing ran (it bypassed
the P0 gate the brief names; the run is void per its own gate, but this
verdict's "cannot run today" reading is wrong and must be corrected);
(b) the Sep-29 window closes with no B2-175 landing receipt and no renewed
owed filing (the leg went silent, which the no-fabrication law forbids);
(c) bytes prove a live crossing already happened before this receipt (this
receipt misread the tree).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_30_shadowledger_live_20260926.md (read in
full); watch/inbox/burn_wave_20260926/B2_10_playtest_prereg_20260926.md (read
in full); watch/inbox/burn_wave_20260926/B2_108_commit_gate_20260926.md (read
in full); roblox/docs/PLAYTEST.md:23-28; roblox/README.md:64-69. No live
DataStore was touched; no Studio session opened; no web calls.
