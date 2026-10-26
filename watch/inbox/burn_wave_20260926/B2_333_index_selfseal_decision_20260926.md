# B2-333 INDEX.json cannot pass its own verify 2026-09-26

## Verdict

Landed, arm (a): the INDEX.json self-item is invalidated as unsealable-by-design with a note event naming why, and the decision holds through repeated folds. Root cause found and named: the 2026-09-22 drift-patrol invalidate DID exist but its seq was a past-2^53 NUMBER literal (1789823567015749417), which JSON.parse quantizes (ulp 256 at that magnitude), demoting it below the 09-21 backfill register's smaller exact seq per the B2-279 total order - so the register out-lived its own invalidation and the self-item (expected B44EDE96..., actual folding bytes) sat in the mismatch list forever. This landing re-pins the invalidation with an exact-string seq (1790458344252207874): after TWO consecutive rebuilds (3650 events -> 1061 active items each) the self-item is absent and `verify` names INDEX.json zero times. No sidecar was needed; the fold-derived truth stays in the fold's own output, unregistered by design.

## Evidence file:line quotes

- Before: watch/inbox/INDEX.json items[] contained {"path": "INDEX.json", "class": "BACKFILL", "sha256": "B44EDE961AE7CE4A6DA18E66432BE86CFD24842F8EA5602A06B9A67F9357839A"} (the B2-280 receipt's mismatch: B789B40F... actual vs B44EDE96... expected).
- watch/inbox/index_events.jsonl: the stale invalidation {"seq": 1789823567015749417, ..., "op": "invalidate", "file": "/board/inbox/INDEX.json", "reason": "retire: self-referential derived file ... (patrol law 20260922)"} - a NUMBER literal past 2^53, quantized on parse (ulp 256; the rebuild WARN line names exactly this: "inexact double seq events demoted below every exact seq: 561 event(s) ... e.g. 1789823567015749376").
- scripts/index_fold_host.mjs invalidate arm: mints `seq: nextSeq(events)` as an exact string and appends before refolding; the B2-280 precedent already re-pinned one band member this way.
- After (measured): rebuild x2 both print "folded 3650 events -> 1061 active items"; INDEX.json self-item lookup = [] both times; `verify` output contains zero "INDEX.json" lines.

## Work done

1. Diagnosed why the 09-22 invalidation had not removed the item: seq-band demotion (B2-279 total order), not missing logic - the fold WARN channel itself enumerates the band.
2. Landed the invalidation through the fold's own writer (`invalidate INDEX.json "<unsealable-by-design reason naming the band-demotion cause>"`), which appends the exact-seq event and refolds atomically.
3. Proved the decision survives: two consecutive rebuilds keep the self-item out (1061 items, no self-reference), and verify names INDEX.json zero times (was: permanently mismatched).
4. Registered this receipt + LEDGER row; board flip.

## Falsifier

Dies if: (a) any rebuild re-materializes an INDEX.json item (a register event with a higher exact seq would; the band-demotion warning channel names any future band write that must win); (b) verify's mismatch list names INDEX.json again; (c) drift-patrol-cron re-registers the fold's own output (meta-files must never be hash-registered, patrol law 20260922 - the note event's reason is the standing citation).

## Bibliography closed

Read whole: scripts/index_fold_host.mjs (fold(), register/invalidate arms, nextSeq, normInboxFile, writeIndex rename publish, B2-147 writer guard), watch/inbox/index_events.jsonl (the stale band invalidate + backfill register), watch/inbox/INDEX.json items (pre/post), rebuild/verify outputs live. Nothing synthesized.
