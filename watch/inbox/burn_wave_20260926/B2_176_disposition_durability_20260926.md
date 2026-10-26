# B2-176 ShadowLedger disposition() durability decision, 2026-09-26

## Verdict

DECIDED: document session-scoped (no code change). `ShadowLedger.disposition()` stays a read of the in-memory `sessionLedger` only, and roblox/README.md now carries the disposition read law saying so explicitly. The blank-on-fresh-server behavior is a documented property, not a durability bug: the durable day rows exist to satisfy the t74 write law (concurrent servers serialize, no row lost), not to back in-world verdicts, and making disposition() read the store would put an async DataStore GetAsync behind a synchronous call on the Watchful Eye (199R SKU) hot path for zero record benefit. The in-world copy already makes blank coherent ("THE LEDGER IS BLANK. THAT IS ITS OWN VERDICT."). The upgrade path is named in the spec: if cross-server verdict continuity is ever product-demanded, hydrate `sessionLedger` once at join or at Watchful Eye purchase, never per-call. Read-from-store was rejected, not deferred-by-laziness: the spec names the exact condition that would reopen it.

## Evidence file:line quotes

- roblox/src/server/ShadowLedger.luau (post-B2-30 HEAD, read this lane): line ~76 `function ShadowLedger.disposition(ofPlayer: Player): string`; next line `local list = sessionLedger[tostring(ofPlayer.UserId)]`; `if not list or #list == 0 then return "THE LEDGER IS BLANK. THAT IS ITS OWN VERDICT." end` — the gap the brief names: verdict source is memory only.
- roblox/src/server/ShadowLedger.luau durable write path (t74, from B2-30 receipt): :42 key `("p%s_day%s"):format(entry.player, os.date("!%Y%m%d"))`, :59 `store:UpdateAsync(key, function(old)`, :60-64 copy-then-append; README.md:66-69 the durable write law bullet.
- roblox/README.md (post-edit): "Disposition read law (B2-176, decided 2026-09-26): `disposition()` is SESSION-SCOPED by design. It reads the in-memory `sessionLedger` (what this server has observed), never the DataStore, so a Watchful Eye verdict on a fresh server is the blank string ... The upgrade path if cross-server continuity is ever product-demanded: one async hydrate into `sessionLedger` at join or at Watchful Eye purchase, never a per-call store read."
- watch/inbox/burn_wave_20260926/B2_30_shadowledger_live_20260926.md Verdict: "SIMULATION LANDED, LIVE PROOF STILL OWED ... 18 checks, 18 PASS, 0 FAIL" — the write law holds under the documented UpdateAsync contract; the read side was untouched by t74, which is exactly the seam this brief names.

## Work done

- Read roblox/src/server/ShadowLedger.luau whole (disposition, onLeaving, the UpdateAsync append path) and the README ShadowLedger bullet; read the B2-30 receipt for the t74 contract and what is already proven.
- Weighed the two arms: read-from-store (async per call, latency + throttle budget on a paid-SKU interaction, cache invalidation vs sessionLedger, no record upside) vs document session-scoped (zero runtime cost, blank verdict already in-world coherent, durable rows keep their record role). Chose document session-scoped.
- Spec first, code untouched: the decision and its reopen condition are written into the owning doc (roblox/README.md ShadowLedger bullet) before any code that would ever implement the hydrate arm; no orphan behavior, no new guard branch in the Luau.
- Em-dash check on the added README lines and this receipt: 0.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- If a Watchful Eye holder on a fresh server experiences the blank verdict as a product defect (refund/support signal in the Sep-29 P3 run), the session-scoped decision is wrong and the hydrate arm must be built per the spec's named upgrade path.
- If disposition() ever gains an `await`/store read without the README paragraph being amended first, the spec-first law is violated and this receipt is void.
- If the t74 durable rows turn out to be consumed by an in-world reader other than disposition() (grep finds none today), the "rows are record, not cache" premise dies and the decision must be re-briefed.
- The claim "no per-call store read exists on the Watchful Eye path" is pinned to today's bytes; any new caller of disposition() inside a yielding context invalidates the latency argument.

## Bibliography closed

roblox/src/server/ShadowLedger.luau (whole); roblox/README.md (ShadowLedger bullet, post-edit); watch/inbox/burn_wave_20260926/B2_30_shadowledger_live_20260926.md (whole); archived DataStore doc contract as quoted inside the B2-30 receipt. No web sources. Em-dash count 0.
