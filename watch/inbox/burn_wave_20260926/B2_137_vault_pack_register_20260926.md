# B2-137 register the vault pack 2026-09-26

## Verdict

Closed, byte-verified. The INDEX.json artifact row for watch/inbox/ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc exists (exactly 1 row, class artifact), and this lane independently recomputed the full sha256 from file bytes: ADA2F62926F432ED4EA01FDCE867BC572860BFA181F5C59D35B958F8AB587C87 over 22,120,192 bytes, matching the INDEX row, the index_events register row (seq 1789823567015749391, ts 2026-09-26T13:16:10.243Z, op register), and the trajectory prefix citation (memory/trajectory/steps.jsonl:22168, ada2f62926f432ed4ea01fdc). The registration itself was landed by the B2-146 lane (its row purpose names "closes the B2-137 registration ask ... verified B2-146"); this receipt is the independent from-bytes proof the ask asked for, so no duplicate row was appended (a second INDEX row for the same path would corrupt the fold's one-item-per-file shape).

## Evidence file:line quotes

- Byte measurement this lane: size 22120192; sha256 ADA2F62926F432ED4EA01FDCE867BC572860BFA181F5C59D35B958F8AB587C87; prefix equality with steps.jsonl:22168 prefix ada2f62926f432ed4ea01fdc is True.
- watch/inbox/INDEX.json items[]: {"path": "ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc", "class": "artifact", ... "sha256": "ADA2F62926F432ED4EA01FDCE867BC572860BFA181F5C59D35B958F8AB587C87"}; purpose text ends "closes the B2-137 registration ask"; bytes sha == row sha is True.
- watch/inbox/index_events.jsonl: {"seq":"1789823567015749391","ts":"2026-09-26T13:16:10.243Z","op":"register","file":"ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc","sha256":"ADA2F629...","class":"artifact",...} (exactly 1 event naming the file).
- watch/inbox/burn_wave_20260926/B2_18_stone2b_20260926.md:13 named the file unindexed at B2-18 run time: "2 unindexed (ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc, index_events.jsonl)".
- memory/trajectory/steps.jsonl:22168: the creating command context, ts 2026-09-26T11:41:14.468+00:00, matching the row purpose "created 2026-09-26T11:41Z".

## Work done

1. Located the pack on disk (watch/inbox/ESSENTIALS_PACK_VAULT_20260926.tar.gz.enc) and re-read the B2-18 naming.
2. Computed the full sha256 from bytes in 1 MiB chunks and confirmed size 22,120,192; confirmed prefix match against steps.jsonl:22168 and full match against the standing INDEX row.
3. Confirmed exactly one INDEX.json item and exactly one index_events register row for the path, so the ask is already closed by B2-146 and no append is owed; appending would duplicate the item.
4. Filed this receipt as the independent verification record; LEDGER row appended; QUEUE row flipped with this pointer.

## Falsifier

Dies if: (a) the file's bytes ever diverge from ADA2F62926F432ED4EA01FDCE867BC572860BFA181F5C59D35B958F8AB587C87 while the INDEX row still stands (rehash catches it); (b) a second INDEX.json item for the same path appears; (c) the size departs from 22,120,192 without a fresh register event naming the change.

## Bibliography closed

Read/verified: the pack bytes (chunked sha256), watch/inbox/INDEX.json (item lookup), watch/inbox/index_events.jsonl (register row), memory/trajectory/steps.jsonl:22168, watch/inbox/burn_wave_20260926/B2_18_stone2b_20260926.md, watch/inbox/SHARED_SURFACE_CONTRACT.json. Nothing synthesized; no index bytes written by this lane (registration pre-existed, verified instead).
