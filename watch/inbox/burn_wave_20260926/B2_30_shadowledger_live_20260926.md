# B2-30 ShadowLedger live-DataStore check (2026-09-26)

## Verdict
SIMULATION LANDED, LIVE PROOF STILL OWED. Studio automation was unavailable on
this box (no publish, no two live clients), so per lane order the maximum
verifiable static equivalent ran: the REAL ShadowLedger.luau bytes (HEAD) and
the REAL pre-t74 bytes (git 5e291421a) executed under the repo's own
tools/bin/luau/luau.exe against an in-memory DataStore stub implementing the
documented UpdateAsync contract. 18 checks, 18 PASS, 0 FAIL. The t74 logic
holds given the documented contract; the live two-client crossing stays owed
to the Sep-29 P3 run. Two estate findings: the shipped rbxlx now carries the
fix, and B2-10's P3 as written cannot detect the t74 bug at all.

## Evidence
- roblox/src/server/ShadowLedger.luau:59 `store:UpdateAsync(key, function(old)`;
  :60-64 copy-then-append (`rows[i] = old[i]`, `rows[#rows + 1] = entry`);
  :42 key `("p%s_day%s"):format(entry.player, os.date("!%Y%m%d"))`; :13 store
  `ShadowLedger_v1`; README.md:66-69 spec bullet (t74 durable write law).
- Doc contract (archived official GlobalDataStore page, snapshot
  20260311133112; live page is JS-rendered, prose unreachable): "The function
  will be called as many times as needed until the data is saved or until the
  callback function returns nil"; "The callback function cannot yield";
  SetAsync "may cause data inconsistency if two servers attempt to set the
  same key"; UpdateAsync "is safer for handling multi-server attempts because
  it reads the current key value (from whatever server last updated it)".
- Harness (18/18 PASS): S1 key resolves to p8675309_day20260926 (UTC). S2 old
  bytes, get|get|set|set interleave, 1 row (lost update reproduced on real
  history). S3 same pressure, new bytes, 2 rows. S7 fuzz, 180 shuffled
  schedules, 2-4 writers: old path lost 311 rows, new path lost 0. S5 retry
  law: double transform call appends once; a mutating control double-appends.
  S6: pre-law array passes through with one row appended.
- Build bytes: the_mountain.rbxlx (rebuilt 2026-09-26 08:28, B2-29) greps
  UpdateAsync = 2 hits, GetAsync(key) = 0; HEAD's committed copy still has the
  old shape, so P0 is cured in the working tree, not yet committed.
- P3 discriminator finding: the old module also passes the two-uid portal
  crossing (S4) because two clients write two different keys; no race exists
  per key. The discriminating probe is same-uid, same-UTC-day, cross-server
  double write (S2/S3), or mixed fleet where an unfixed server's late
  SetAsync clobbers the fixed row (S4b).

## Work done
- make_under_test.py composes combined_sim.luau: stubs + real KSpace.luau
  (sha256 23714a6e identical) + both ShadowLedger variants with ONE documented
  delta each (line 10 require to global handoff) + driver.luau. sha256s
  printed at build; deterministic rebuild.
- driver.luau scenarios S0-S7; scheduler yields only at store network
  boundaries, UpdateAsync read-transform-write atomic per the doc sentence.
- Artifacts: watch/inbox/burn_wave_20260926/B2_30_sim/ (builder, driver,
  combined chunk, under-test copies).

## Falsifier
- The Sep-29 live run falsifies this verdict if both clients cross one portal,
  stop, rejoin on the 08:28-or-newer build and any "took the portal" row is
  gone, or if the live service ever re-calls the transform with results the
  stub's model gets wrong (throttles, retries, cross-region replication are
  NOT modeled). S4b names residual risk while any server runs pre-t74 code.
- Filed as owed: Studio publish + two-client crossing on real DataStores.

## Bibliography closed
watch/inbox/gala_20260925/afterparty/lanes/t74.check.txt; B2_10 receipt;
ShadowLedger.luau HEAD + 5e291421a; KSpace.luau; README.md:64-69;
the_mountain.rbxlx (worktree + HEAD); archived GlobalDataStore page snapshot
20260311133112; tools/bin/luau/luau.exe; B2_30_sim/*; QUEUE.md;
memory/burns/LEDGER.jsonl.
